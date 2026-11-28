#!/usr/bin/env python3
"""Atalaya: eurodiputados españoles (legislaturas II a X del Parlamento Europeo, desde 1986) y resultados de las elecciones europeas.

Fuente de personas: API de datos abiertos del Parlamento Europeo (https://data.europarl.europa.eu/api/v2/):
  /meps?parliamentary-term=N&country-of-representation=ES   quién fue eurodiputado en cada legislatura
  /meps/{id}                                                  fecha de nacimiento, sexo, lugar y membresías con fechas (legislatura, partido nacional, grupo)
  /corporate-bodies/{id}                                      nombre del partido nacional o del grupo político europeo
Fuente de votos (opcional): atalaya/data/resultados/europeas-AAAA-MM/ (los genera build_interior.py a partir de los .zip del Ministerio
del Interior «Parlamento Europeo · Resultados por municipio», descargados a mano a data-private/interior/).

Salida: atalaya/data/parlamento/europarlamento.json
  legislaturas {num: {nombre, inicio, fin, actual, eleccion}}, personas {id: {n, nac, sexo, lugar, foto}},
  mandatos [{p, l, pt: partido nacional, g: grupo europeo, alta, baja, vig}],
  resultados {eleccion: {nombre, fecha, partidos: {sigla: nombre}, total: {sigla: votos}, prov: {cod: {sigla: votos}}, validos, votantes, censo}}
Principio del proyecto: NUNCA se borra nada. Lo que deja de aparecer en la fuente se conserva marcado con «ausente».
Uso (raíz del repo): python3 scripts/atalaya/build_europarlamento.py
"""
import json, sys, time, urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import build_parlamento as P

RAIZ = Path(__file__).resolve().parents[2]
OUT = P.OUT
RES = RAIZ / "atalaya/data/resultados"
API = "https://data.europarl.europa.eu/api/v2/"
HOY = date.today().isoformat()
ROMAN = {2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI", 7: "VII", 8: "VIII", 9: "IX", 10: "X"}
# legislatura -> (inicio, fin, elección en España que la inaugura). La II arranca en 1984, pero España entra en 1986 y vota en 1987.
LEGS = {2: ("1984-07-24", "1989-07-24", "1987-06"), 3: ("1989-07-25", "1994-07-18", "1989-06"), 4: ("1994-07-19", "1999-07-19", "1994-06"),
        5: ("1999-07-20", "2004-07-19", "1999-06"), 6: ("2004-07-20", "2009-07-13", "2004-06"), 7: ("2009-07-14", "2014-06-30", "2009-06"),
        8: ("2014-07-01", "2019-07-01", "2014-05"), 9: ("2019-07-02", "2024-07-15", "2019-05"), 10: ("2024-07-16", None, "2024-06")}
ACTUAL = 10
MESES = {"01": "enero", "02": "febrero", "03": "marzo", "04": "abril", "05": "mayo", "06": "junio", "07": "julio", "08": "agosto", "09": "septiembre",
         "10": "octubre", "11": "noviembre", "12": "diciembre"}


def get(ruta, **q):
    url = API + ruta + "?" + urllib.parse.urlencode({"format": "application/ld+json", **q})
    for i in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": P.UA})
            with urllib.request.urlopen(req, timeout=40) as r: return json.loads(r.read())["data"]
        except Exception as e:
            err = e; time.sleep(2 + 3 * i)
    print("   fallo", ruta, err, file=sys.stderr); return None


def titulo(label):
    """«Esther HERRANZ GARCÍA» -> «Esther Herranz García»."""
    return " ".join(w.capitalize() if w.isupper() and len(w) > 2 else w for w in label.replace("’", "'").split()).replace(" De ", " de ").replace(" Del ", " del ")


def org_nombre(oid, cache):
    if oid in cache: return cache[oid]
    d = get("corporate-bodies/" + oid.split("/")[1])
    n = None
    if d:
        n = d[0].get("label") or (d[0].get("prefLabel") or {}).get("es")
    cache[oid] = n or oid; return cache[oid]


def periodo(m):
    t = m.get("memberDuring") or {}
    return t.get("startDate"), t.get("endDate")


def ficha(i):
    d = get("meps/" + i)
    return i, (d[0] if d else None)


def personas_y_mandatos():
    ids = {}
    for t in LEGS:
        lista = get("meps", **{"parliamentary-term": t, "country-of-representation": "ES", "limit": 400})
        for x in lista or []: ids.setdefault(x["identifier"], x["label"])
        print(f"   legislatura {ROMAN[t]}: {len(lista or [])} eurodiputados")
    with ThreadPoolExecutor(6) as ex: fichas = dict(ex.map(ficha, ids))
    cache = {}
    pers, mand = {}, []
    for i, f in fichas.items():
        if not f: print("   sin ficha:", i, ids[i], file=sys.stderr); continue
        ms = f.get("hasMembership", [])
        pers[i] = {"n": titulo(f.get("label") or ids[i]), "nac": f.get("bday"), "lugar": f.get("placeOfBirth"),
                   "sexo": {"FEMALE": "M", "MALE": "H"}.get((f.get("hasGender") or "").rsplit("/", 1)[-1]), "foto": f.get("img")}
        nac = [(m["organization"], *periodo(m)) for m in ms if m.get("membershipClassification") == "def/ep-entities/NATIONAL_POLITICAL_GROUP" and m.get("organization")]
        grp = [(m["organization"], *periodo(m)) for m in ms if m.get("membershipClassification") == "def/ep-entities/EU_POLITICAL_GROUP" and m.get("organization")]
        for m in ms:
            if m.get("membershipClassification") != "def/ep-entities/EU_INSTITUTION" or m.get("role") != "def/ep-roles/MEMBER": continue
            org = str(m.get("organization", ""))
            if not org.startswith("org/ep-"): continue
            t = int(org.split("-")[1])
            if t not in LEGS: continue
            a, b = periodo(m)
            fin_leg = LEGS[t][1] or "9999"

            def activo(lst):  # el partido o grupo vigente al final de su mandato en esa legislatura (si cambió, el último)
                c = [x for x in lst if (x[1] or "") <= (b or "9999") and (x[2] or "9999") >= (a or "")]
                c.sort(key=lambda x: x[1] or "")
                return org_nombre(c[-1][0], cache) if c else None
            mand.append({"p": i, "l": t, "pt": activo(nac), "g": activo(grp), "alta": a, "baja": b, "vig": t == ACTUAL and b is None})
    return pers, mand


def resultados():
    """Votos de las europeas ya importados por build_interior.py (si existen): total por candidatura y por provincia."""
    out = {}
    ind = json.loads((RES / "indice.json").read_text(encoding="utf8")) if (RES / "indice.json").exists() else {"elecciones": {}}
    for eid, e in ind["elecciones"].items():
        if not eid.startswith("europeas-"): continue
        aaaa, mm = eid.split("-")[1:3]
        prov, total, val, vot, cen = {}, {}, 0, 0, 0
        for f in sorted((RES / eid).glob("[0-9][0-9].json")):
            pv = {}
            for m in json.loads(f.read_text(encoding="utf8"))["mun"].values():
                val += m["validos"]; vot += m["votantes"]; cen += m["censo"]
                for s, v in m["v"].items(): pv[s] = pv.get(s, 0) + v
            prov[f.stem] = pv
            for s, v in pv.items(): total[s] = total.get(s, 0) + v
        if not prov: continue
        out[eid] = {"nombre": e["nombre"], "fecha": f"{aaaa}-{mm}", "partidos": e["partidos"], "total": total, "prov": prov,
                    "validos": val, "votantes": vot, "censo": cen}
    return out


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    pers, mand = personas_y_mandatos()
    if not mand: print("europarlamento.json SIN DATOS: no se sobrescribe", file=sys.stderr); return
    legs = {str(t): {"nombre": f"{ROMAN[t]} legislatura ({LEGS[t][0][:4]}–{(LEGS[t][1] or '')[:4]})", "inicio": a, "fin": b, "actual": t == ACTUAL, "eleccion": e}
            for t, (a, b, e) in LEGS.items()}
    nuevo = {"fuente": "https://data.europarl.europa.eu/", "capturado": HOY, "legislatura_actual": ACTUAL, "legislaturas": legs, "personas": pers, "mandatos": mand}
    viejo = P.cargar("europarlamento.json")
    d = P.fusionar(viejo, nuevo, lambda m: (m["p"], m["l"]))
    res = resultados()
    d["resultados"] = {**((viejo or {}).get("resultados") or {}), **res}          # nunca se borra una elección ya importada
    (OUT / "europarlamento.json").write_text(json.dumps(d, ensure_ascii=False, separators=(",", ":")), encoding="utf8")
    act = [m for m in d["mandatos"] if m["l"] == ACTUAL]
    print(f"europarlamento.json: {len(d['personas'])} personas, {len(d['mandatos'])} mandatos, legislatura actual: {len(act)} ({sum(bool(m.get('vig')) for m in act)} vigentes), "
          f"sin partido: {sum(not m.get('pt') for m in d['mandatos'])}, elecciones con votos: {len(d['resultados'])}")


if __name__ == "__main__":
    main()
    from manifest import marcar
    marcar("europarlamento")
