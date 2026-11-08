#!/usr/bin/env python3
"""Atalaya: Congreso de los Diputados y Senado (legislatura actual e histórico desde 1977).

Fuentes oficiales:
  Congreso: https://www.congreso.es/es/opendata/diputados  (DiputadosActivos, DiputadosDeBaja, Diput = histórico por legislatura)
  Senado:   listado «senadores desde 1977» + ficha XML de cada senador de la XV legislatura (ficopendataservlet)

Salida: atalaya/data/parlamento/congreso.json y senado.json
Principio del proyecto: NUNCA se borra nada. Cada ejecución se fusiona con lo ya guardado: lo que deja de aparecer
en la fuente se conserva marcado con "ausente" (fecha en que se dejó de ver) y las capturas previas no se tocan.

Estructura de cada fichero:
  fuente, capturado, legislaturas {num: {nombre, inicio, fin, actual}},
  personas {id: {n: nombre, ...}},
  mandatos [{p: id persona, l: legislatura, c: código provincia INE | null, cn: territorio, g: grupo, pt: partido, e: estado, alta, baja, ...}]
Uso (raíz del repo): python3 scripts/atalaya/build_parlamento.py
"""
import json, re, subprocess, unicodedata, sys
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from html import unescape
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
OUT = RAIZ / "atalaya/data/parlamento"
HOY = date.today().isoformat()
UA = "Mozilla/5.0 (compatible; atalaya-bot/1.0; +https://emirodgar.es)"
ROMAN = {"Const.": 0, "I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7, "VIII": 8, "IX": 9, "X": 10, "XI": 11, "XII": 12, "XIII": 13, "XIV": 14, "XV": 15, "XVI": 16}
NOMBRE_LEG = {0: "Constituyente"}  # el resto: «{romano} Legislatura»
INV = {v: k for k, v in ROMAN.items()}

def curl(url):
    for _ in range(3):
        r = subprocess.run(["curl", "-sk", "-m", "90", "-A", UA, "-L", url], capture_output=True)
        if r.stdout: return r.stdout
    return b""

def norm(s): return re.sub(r"\s+", " ", unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()).strip()
def fixmoji(s):
    if not isinstance(s, str) or "Ã" not in s and "Â" not in s: return s
    try: return s.encode("latin1").decode("utf8")
    except Exception: return s
def iso(d):  # dd/mm/yyyy -> yyyy-mm-dd
    m = re.match(r"(\d\d)/(\d\d)/(\d{4})", d or ""); return f"{m[3]}-{m[2]}-{m[1]}" if m else None
def titulo(s):  # "ABAD BÉCQUER, FERNANDO" -> "Fernando Abad Bécquer"
    if "," in s: ap, no = [x.strip() for x in s.split(",", 1)]; s = f"{no} {ap}"
    return " ".join(w.capitalize() if w.lower() not in ("de", "del", "la", "las", "los", "y", "i", "da", "do") else w.lower() for w in s.split())

# ── territorio ──
IND = json.loads((RAIZ / "atalaya/data/indice.json").read_text(encoding="utf8"))["prov"]
PROV_ALIAS = {"03": ["alicante"], "12": ["castellon"], "46": ["valencia"], "01": ["alava"], "07": ["baleares", "balears", "mallorca", "menorca", "ibiza", "formentera", "eivissa"],
              "15": ["coruna"], "35": ["palmas", "gran canaria", "lanzarote", "fuerteventura"], "38": ["tenerife", "la palma", "gomera", "hierro"], "26": ["rioja"],
              "17": ["gerona"], "25": ["lerida"], "32": ["orense"], "48": ["vizcaya"], "20": ["guipuzcoa"], "33": ["asturias"], "39": ["cantabria"], "31": ["navarra"]}
CCAA = [("andaluc", "41"), ("aragon", "50"), ("asturias", "33"), ("balear", "07"), ("canaria", "38"), ("cantabria", "39"), ("mancha", "45"), ("castilla y leon", "47"),
        ("catalu", "08"), ("extremadura", "06"), ("galicia", "15"), ("madrid", "28"), ("murcia", "30"), ("rioja", "26"), ("valenc", "46"), ("vasco", "01"), ("euskadi", "01"), ("navarra", "31")]
def prov_de(txt):
    t = norm(re.sub(r"\(.*?\)", " ", txt or ""))
    t = re.sub(r"^(electo|electa|designado|designada|designacion real)\s*:?\s*", "", t)
    if not t: return None
    for tok in [x.strip() for x in re.split(r"[/,;]", t) if x.strip()] + [t]:
        for c, n in IND.items():
            if norm(n) == tok or tok in PROV_ALIAS.get(c, []): return c
    for c, al in PROV_ALIAS.items():
        if any(re.search(r"\b" + re.escape(a) + r"\b", t) for a in al): return c
    for k, c in CCAA:
        if k in t: return c
    for c, n in IND.items():
        if norm(n) in t: return c
    return None

def cargar(nombre):
    p = OUT / nombre
    return json.loads(p.read_text(encoding="utf8")) if p.exists() else None

def fusionar(viejo, nuevo, clave_mand):
    """Nunca borra: lo previo que no aparece ahora se conserva con 'ausente'."""
    if not viejo: return nuevo
    pers = dict(viejo["personas"]); pers.update({k: {**pers.get(k, {}), **v} for k, v in nuevo["personas"].items()})
    mv = {clave_mand(m): m for m in viejo["mandatos"]}; mn = {clave_mand(m): m for m in nuevo["mandatos"]}
    out = []
    for k, m in mv.items():
        if k in mn: out.append({**m, **{a: b for a, b in mn[k].items() if b is not None}}); out[-1].pop("ausente", None)
        else: out.append({**m, "ausente": m.get("ausente") or HOY})
    out += [m for k, m in mn.items() if k not in mv]
    legs = {**viejo["legislaturas"], **nuevo["legislaturas"]}
    return {**nuevo, "legislaturas": legs, "personas": pers, "mandatos": out}

# ───────── Congreso ─────────
def congreso():
    pag = curl("https://www.congreso.es/es/opendata/diputados").decode("utf8", "replace")
    def url(pref):
        m = re.findall(r'href="(/webpublica/opendata/diputados/' + pref + r'__\d+\.json)"', pag); return "https://www.congreso.es" + m[0] if m else None
    def js(pref):
        u = url(pref); raw = curl(u).decode("utf-8-sig", "replace") if u else "[]"
        return json.loads(raw)
    act, baj, hist = js("DiputadosActivos"), js("DiputadosDeBaja"), js("Diput")
    legs, pers, mand = {}, {}, []
    for r in hist:
        r = {k: fixmoji(v) for k, v in r.items()}
        mm = re.match(r"Leg\. (.+)", r["LEGISLATURA"]); n = ROMAN.get(mm[1]) if mm else None
        if n is None: continue
        legs[str(n)] = {"nombre": NOMBRE_LEG.get(n) or f"{INV[n]} Legislatura", "inicio": iso(r["FECHAINICIOLEGISLATURA"]), "fin": iso(r.get("FECHAFINLEGISLATURA")),
                        "actual": r.get("LEGISLATURAACTUAL") == "S"}
        key = norm(f'{r["APELLIDOS"]} {r["NOMBRE"]}'); pers[key] = {"n": f'{r["NOMBRE"]} {r["APELLIDOS"]}'.strip()}
        mand.append({"p": key, "l": n, "e": "actual" if r.get("LEGISLATURAACTUAL") == "S" else "pasado"})
    idx = {(m["p"], m["l"]): m for m in mand}
    cur = max((int(k) for k, v in legs.items() if v["actual"]), default=15)
    for lst, estado in ((act, "activo"), (baj, "baja")):
        for r in lst:
            r = {k: fixmoji(v) for k, v in r.items()}
            ap, no = [x.strip() for x in r["NOMBRE"].split(",", 1)] if "," in r["NOMBRE"] else (r["NOMBRE"], "")
            key = norm(f"{ap} {no}"); pers.setdefault(key, {"n": f"{no} {ap}".strip()})
            m = idx.get((key, cur))
            if not m: m = {"p": key, "l": cur}; mand.append(m); idx[(key, cur)] = m
            circ = r.get("CIRCUNSCRIPCION")
            m.update({"e": estado, "cn": circ, "c": prov_de(circ), "g": r.get("GRUPOPARLAMENTARIO"), "pt": r.get("FORMACIONELECTORAL"),
                      "alta": iso(r.get("FECHAALTA")), "baja": iso(r.get("FECHABAJA")), "bio": r.get("BIOGRAFIA")})
    from collections import Counter
    bajas = Counter(m["baja"] for m in mand if m.get("baja") and m["l"] == cur)
    disol = next((d for d, n in bajas.most_common(1) if n >= 50), None)   # bajas masivas el día de la disolución de las Cortes
    for m in mand:
        if m["l"] == cur: m["vig"] = m.get("e") == "activo" or (disol is not None and m.get("baja") == disol)   # ocupaba escaño al disolverse
    return {"fuente": "https://www.congreso.es/es/opendata/diputados", "capturado": HOY, "legislatura_actual": cur, "disolucion": disol, "legislaturas": legs, "personas": pers, "mandatos": mand}

# ───────── Senado ─────────
LISTA = "https://www.senado.es/web/composicionorganizacion/senadores/composicionsenado/senadoresdesde1977/consultaorden/index.html"
RX = re.compile(r'fichasenador/index\.html[^"]*?\?legis=(\d+)&(?:amp;)?id1=(\d+)">([^<]+)</a></span><span class="col-5"><abbr title="([^"]*)">([^<]*)</abbr>.*?<span class="col-3">([^<]*)</span>', re.S)
def cdata(x, tag):
    m = re.search(rf"<{tag}>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</{tag}>", x, re.S); return unescape(re.sub(r"<[^>]+>", "", m[1])).strip() if m else ""

BLOQUEO = {"n": 0}   # peticiones seguidas sin respuesta: si el Senado nos limita (403), se para y se reanuda en la siguiente ejecución

def ficha(arg):
    """Ficha XML de un senador: datos personales y TODAS sus legislaturas (la lista oficial solo trae la última)."""
    import time
    id_, leg = arg
    if BLOQUEO["n"] >= 8: return id_, None
    for i in range(3):
        time.sleep(1.2)
        x = curl(f"https://www.senado.es/web/ficopendataservlet?tipoFich=1&cod={id_}&legis={leg}").decode("utf8", "replace")
        if "<fichaSenador>" in x and "<numLeg>" in x: BLOQUEO["n"] = 0; break
        BLOQUEO["n"] += 1; time.sleep(1 + i)
    else: return id_, None
    legs = []
    for b in re.findall(r"<legislatura>.*?</legislatura>", x, re.S):
        c = (re.findall(r"<credencial>.*?</credencial>", b, re.S) or [""])[-1]
        pr = cdata(c, "procedLiteral")
        legs.append({"l": int(cdata(b, "numLeg") or -1), "t": cdata(c, "procedTipo") or "E", "cn": re.sub(r"^(Electo|Electa|Designad[oa]|Designación real)\s*:\s*", "", pr).strip(),
                     "alta": iso(re.sub(r"^Fecha:\s*", "", cdata(c, "procedFecha"))), "baja_txt": cdata(c, "bajaLiteral") or None, "sust": cdata(c, "sustitucionLiteral") or None,
                     "pt": cdata(c, "partidoSiglas") or cdata(c, "formElecSiglas"), "pos": cdata(c, "posicionHemiciclo") or None})
    return id_, {"bio": cdata(x, "biografia"), "nac": iso(cdata(x, "fechaNacimiento")), "sexo": cdata(x, "sexo"), "legs": legs}

def senado():
    for _ in range(4):
        h = curl(LISTA).decode("utf8", "replace")
        if len(RX.findall(h)) > 2000: break
        import time; time.sleep(5)
    else: return {"mandatos": []}
    previo = cargar("senado.json") or {"personas": {}}
    legs, pers, mand, ultima = {}, {}, [], {}
    for leg, id_, nom, gname, gcod, proc in RX.findall(h):
        leg = int(leg); ultima[id_] = leg
        legs[str(leg)] = {"nombre": NOMBRE_LEG.get(leg) or f"{INV.get(leg, leg)} Legislatura", "inicio": None, "fin": None, "actual": leg == 15}
        proc = unescape(re.sub(r"\s+", " ", proc)).strip(); tipo = proc.split(":")[0]
        pers.setdefault(id_, {"n": titulo(unescape(nom))})
        mand.append({"p": id_, "l": leg, "g": gcod, "gn": unescape(gname).title(), "t": {"Electo": "E", "Electa": "E"}.get(tipo, "R" if "real" in tipo else "D"),
                     "cn": proc.split(":", 1)[-1].strip(), "c": prov_de(proc), "e": None if leg == 15 else "pasado"})   # None = no se toca el estado anterior
    # fichas pendientes: quien no tiene su historial completo y todos los de la legislatura actual (su estado cambia)
    import os
    pend = [(i, l) for i, l in ultima.items() if not previo["personas"].get(i, {}).get("completo") or (l == 15 and os.environ.get("SEMANAL") == "1")]
    pend.sort(key=lambda t: t[1] != 15)   # primero la legislatura actual
    total = len(pend); pend = pend[:int(os.environ.get("MAX_FICHAS", "300"))]   # tope por ejecución: se completa en varias pasadas
    print(f"   fichas del Senado pendientes: {total}; se leen {len(pend)} en esta pasada")
    with ThreadPoolExecutor(2) as ex: fichas = dict(ex.map(ficha, pend))
    ok = 0
    for id_, f in fichas.items():
        if f is None: continue
        ok += 1; pers[id_].update({k: v for k, v in (("nac", f["nac"]), ("sexo", f["sexo"]), ("completo", True)) if v})
        for g in f["legs"]:
            if g["l"] < 0: continue
            legs.setdefault(str(g["l"]), {"nombre": NOMBRE_LEG.get(g["l"]) or f"{INV.get(g['l'], g['l'])} Legislatura", "inicio": None, "fin": None, "actual": g["l"] == 15})
            m = next((x for x in mand if x["p"] == id_ and x["l"] == g["l"]), None)
            if m is None: m = {"p": id_, "l": g["l"]}; mand.append(m)
            m.update({"t": g["t"], "cn": g["cn"] or m.get("cn"), "c": prov_de(g["cn"]) or m.get("c"), "pt": g["pt"], "alta": g["alta"], "baja_txt": g["baja_txt"], "sust": g["sust"], "pos": g["pos"]})
            m["e"] = "pasado"
            if g["l"] == 15:
                m["e"] = "baja" if g["baja_txt"] else "activo"; m["vig"] = not g["baja_txt"]; m["bio"] = f["bio"]
    print(f"   fichas leídas: {ok}/{len(pend)}" + ("  (el Senado limitó el acceso: vuelve a ejecutar más tarde para completar)" if ok < len(pend) else ""))
    return {"fuente": "https://www.senado.es/web/composicionorganizacion/senadores/composicionsenado/senadoresdesde1977/", "capturado": HOY, "legislatura_actual": 15,
            "historico_completo": all(pers[i].get("completo") or previo["personas"].get(i, {}).get("completo") for i in ultima),
            "legislaturas": legs, "personas": pers, "mandatos": mand}

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for nombre, fn in (("congreso.json", congreso), ("senado.json", senado)):
        d = fn()
        if not d["mandatos"]: print(nombre, "SIN DATOS: no se sobrescribe", file=sys.stderr); continue
        d = fusionar(cargar(nombre), d, lambda m: (m["p"], m["l"]))
        (OUT / nombre).write_text(json.dumps(d, ensure_ascii=False, separators=(",", ":")), encoding="utf8")
        act = [m for m in d["mandatos"] if m["l"] == d["legislatura_actual"]]
        sin = [m for m in act if m.get("c") is None]
        print(f"{nombre}: {len(d['personas'])} personas, {len(d['mandatos'])} mandatos, legislatura actual: {len(act)} ({sum(m.get('e')=='activo' for m in act)} activos), sin provincia: {len(sin)}")
        for m in sin[:8]: print("   sin provincia:", m.get("cn"))

if __name__ == "__main__": main()
