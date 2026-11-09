#!/usr/bin/env python3
"""Atalaya: políticos por provincia (REALES, con fuente) -> atalaya/data/politicos_prov.json

  gobierno   Presidente/a de la comunidad autónoma y alcalde/sa de la capital: Wikidata (cargo vigente, sin fecha de fin).
             Presidente/a de la Diputación: infobox de Wikipedia (cobertura parcial).
  candidatos Cabezas de lista al Congreso por circunscripción para el 29-N-2026: Wikipedia
             «Elecciones generales de España de 2026» (se actualiza al proclamarse las listas).

Todo son fuentes secundarias: cada ficha enlaza a su origen y se muestra «verificar» en el panel.
Uso (raíz del repo): python3 scripts/atalaya/build_politicos_prov.py
"""
import json, re, subprocess, unicodedata, urllib.parse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
D = RAIZ / "atalaya/data"
UA = "EmirodgarBot/1.0 (https://emirodgar.es/atalaya)"
NL = "\n"
ES = {"Araba": "Álava", "Alacant": "Alicante", "Castelló": "Castellón", "Illes Balears": "Baleares", "València": "Valencia",
      "Gipuzkoa": "Guipúzcoa", "Bizkaia": "Vizcaya"}
CCAA = {"Andalucía": "04 11 14 18 21 23 29 41", "Aragón": "22 44 50", "Asturias": "33", "Islas Baleares": "07", "Canarias": "35 38",
        "Cantabria": "39", "Castilla y León": "05 09 24 34 37 40 42 47 49", "Castilla-La Mancha": "02 13 16 19 45", "Cataluña": "08 17 25 43",
        "Comunidad Valenciana": "03 12 46", "Extremadura": "06 10", "Galicia": "15 27 32 36", "Comunidad de Madrid": "28",
        "Región de Murcia": "30", "País Vasco": "01 20 48", "La Rioja": "26", "Navarra": "31"}
P2C = {p: c for c, ps in CCAA.items() for p in ps.split()}
CAP = {"01": ["Vitoria-Gasteiz", "Vitoria"], "03": ["Alicante"], "07": ["Palma"], "12": ["Castelló de la Plana", "Castellón de la Plana"], "15": ["A Coruña", "La Coruña"],
       "20": ["San Sebastián", "Donostia"], "26": ["Logroño"], "30": ["Murcia"], "31": ["Pamplona"], "33": ["Oviedo"], "35": ["Las Palmas de Gran Canaria"],
       "38": ["Santa Cruz de Tenerife"], "39": ["Santander"], "46": ["Valencia", "València"], "48": ["Bilbao"], "51": ["Ceuta"], "52": ["Melilla"], "32": ["Ourense", "Orense"],
       "17": ["Girona", "Gerona"], "25": ["Lleida", "Lérida"], "21": ["Huelva"], "36": ["Pontevedra"]}
COLS = ["PP", "PSOE", "VOX", "FA", "PODEMOS", "ERC", "JUNTS", "EHB", "PNV", "BNG", "CC"]
SPECIAL = {"baleares, islas": "07", "coruña, a": "15", "coruña, la": "15", "palmas, las": "35", "rioja, la": "26", "alicante": "03", "castellón": "12", "valencia": "46",
           "guipúzcoa": "20", "vizcaya": "48", "álava": "01", "orense": "32", "gerona": "17", "lérida": "25", "asturias": "33", "cantabria": "39", "navarra": "31"}

def nrm(s): return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower().strip()
def curl(url, params=None, headers=None):
    cmd = ["curl", "-s", "-m", "60", "-A", UA]
    for h in headers or []: cmd += ["-H", h]
    if params: url += "?" + urllib.parse.urlencode(params)   # URL en ASCII: los argumentos no ASCII se corrompen en Windows
    r = subprocess.run(cmd + [url], capture_output=True)
    return r.stdout.decode("utf8", "replace")
def sparql(q):
    return json.loads(curl("https://query.wikidata.org/sparql", {"query": q}, ["Accept: application/sparql-results+json"]))["results"]["bindings"]
def wikitext(title):
    for _ in range(3):
        try: return json.loads(curl("https://es.wikipedia.org/w/api.php", {"action": "parse", "page": title, "prop": "wikitext", "format": "json", "formatversion": 2, "redirects": 1}))["parse"]["wikitext"]
        except Exception: continue
    return None
def art_title(url): return urllib.parse.unquote(url.rsplit("/wiki/", 1)[-1]) if url else None
def v(r, k): return r.get(k, {}).get("value")

def wd_persona(r, rol, ambito, fuente):
    return {"rol": rol, "ambito": ambito, "nombre": v(r, "presLabel"), "partido": v(r, "partyLabel"), "wiki": art_title(v(r, "art")), "fuente": fuente}

def gobierno():
    out = {}
    q_ccaa = """SELECT ?xLabel ?presLabel ?partyLabel ?art WHERE { ?x wdt:P31 wd:Q10742 . ?x p:P6 ?st . ?st ps:P6 ?pres . FILTER NOT EXISTS { ?st pq:P582 ?end }
      OPTIONAL { ?pres wdt:P102 ?party } OPTIONAL { ?art schema:about ?pres ; schema:isPartOf <https://es.wikipedia.org/> }
      SERVICE wikibase:label { bd:serviceParam wikibase:language "es,en". } }"""
    ccaa = {v(r, "xLabel"): r for r in sparql(q_ccaa)}
    q_nav = """SELECT ?xLabel ?presLabel ?partyLabel ?art WHERE { ?x rdfs:label "Comunidad Foral de Navarra"@es . ?x p:P6 ?st . ?st ps:P6 ?pres . FILTER NOT EXISTS { ?st pq:P582 ?end }
      OPTIONAL { ?pres wdt:P102 ?party } OPTIONAL { ?art schema:about ?pres ; schema:isPartOf <https://es.wikipedia.org/> }
      SERVICE wikibase:label { bd:serviceParam wikibase:language "es,en". } }"""
    for r in sparql(q_nav): ccaa["Navarra"] = r
    q_cap = """SELECT ?capLabel ?presLabel ?partyLabel ?art WHERE { ?prov wdt:P31 wd:Q162620 . ?prov wdt:P36 ?cap . ?cap p:P6 ?st . ?st ps:P6 ?pres . FILTER NOT EXISTS { ?st pq:P582 ?end }
      OPTIONAL { ?pres wdt:P102 ?party } OPTIONAL { ?art schema:about ?pres ; schema:isPartOf <https://es.wikipedia.org/> }
      SERVICE wikibase:label { bd:serviceParam wikibase:language "es,en". } }"""
    caps = {}
    for r in sparql(q_cap): caps.setdefault(nrm(v(r, "capLabel")), r)
    prov = json.loads((D / "indice.json").read_text(encoding="utf8"))["prov"]
    pend = {}
    for pc, nom in prov.items():
        g = []
        c = P2C.get(pc)
        if c and c in ccaa: g.append(wd_persona(ccaa[c], f"Presidente/a de {c}", "autonómico", "Wikidata"))
        hallado = False
        for n in CAP.get(pc, [ES.get(nom, nom)]):
            r = caps.get(nrm(n)) or next((x for k, x in caps.items() if k.startswith(nrm(n)) or nrm(n) in k.split(" de ")), None)
            if r:
                g.append(wd_persona(r, f"Alcalde/sa de {v(r, 'capLabel')}", "municipal", "Wikidata")); hallado = True; break
        if not hallado: pend[pc] = CAP.get(pc, [ES.get(nom, nom)])
        out[pc] = g
    if pend: alcaldes_por_municipio(pend, out)
    return out

def alcaldes_por_municipio(pend, out):
    """Segunda pasada para capitales sin «cargo vigente» en la provincia: se acepta el mandato con fecha de inicio
    cuyo fin no ha llegado (o no existe) y se queda con el más reciente. Sin fecha de inicio no se usa (puede estar obsoleto)."""
    nombres = sorted({n for ns in pend.values() for n in ns})
    vals = " ".join('"%s"@es' % n for n in nombres)
    q = """SELECT ?l ?presLabel ?partyLabel ?art ?st ?en WHERE { VALUES ?l { %s } ?m rdfs:label ?l . ?m wdt:P31/wdt:P279* wd:Q2074737 .
      ?m p:P6 ?s . ?s ps:P6 ?pres . ?s pq:P580 ?st . OPTIONAL { ?s pq:P582 ?en }
      OPTIONAL { ?pres wdt:P102 ?party } OPTIONAL { ?art schema:about ?pres ; schema:isPartOf <https://es.wikipedia.org/> }
      SERVICE wikibase:label { bd:serviceParam wikibase:language "es,en". } }""" % vals
    hoy = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    mejor = {}
    for r in sparql(q):
        fin = (v(r, "en") or "9999")[:10]
        if fin <= hoy: continue
        k = nrm(v(r, "l"))
        if k not in mejor or v(r, "st") > v(mejor[k], "st"): mejor[k] = r
    for pc, ns in pend.items():
        for n in ns:
            r = mejor.get(nrm(n))
            if r:
                out[pc].append({"rol": f"Alcalde/sa de {n}", "ambito": "municipal", "nombre": v(r, "presLabel"), "partido": v(r, "partyLabel"),
                                "wiki": art_title(v(r, "art")), "fuente": "Wikidata (mandato con fechas)"}); break

SIN_DIPUTACION = {"07", "26", "28", "30", "31", "33", "35", "38", "39"}   # uniprovinciales e islas: no hay diputación provincial

def norm_partido(p):
    if not p: return None
    t = nrm(p)
    if "popular" in t or re.search(r"\bpp", t): return "Partido Popular"
    if "socialista" in t or "psoe" in t or "psc" in t: return "Partido Socialista Obrero Español"
    if "vox" in t: return "Vox"
    return re.sub(r"\[\[|\]\]", "", p).strip()

def persona_wiki(texto):
    """De «[[Enlace|Nombre]] <small>([[Partido|SIGLAS]])</small>» saca (nombre, página de Wikipedia, partido)."""
    base = re.split(r"<small|\s\(", texto)[0]
    m = re.search(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]", base)
    if m:
        wiki = m.group(1).strip().replace(" ", "_")
        nombre = re.sub(r"\s*\(.*\)$", "", m.group(1)).strip()
        if len(nombre.split()) < len((m.group(2) or "").split()): nombre = m.group(2).strip()
    else:
        nombre, wiki = re.sub(r"<[^>]+>|\{\{[^}]*\}\}|'{2,3}|\[\[|\]\]", "", base).strip(), None
    resto = texto[len(base):]
    mp = re.search(r"\(\s*\[\[(?:[^\]|]*\|)?([^\]]+)\]\]", resto) or re.search(r"\(([^)<\[]{2,30})\)", resto)
    return nombre, wiki, norm_partido(mp.group(1) if mp else None)

def campo(w, nombre):
    m = re.search(r"\|\s*" + nombre + r"\s*=\s*([^\n]*)", w, re.I)
    return re.split(r"\s\|\s*\w[\w ñáéíóú_]*=", m.group(1))[0].strip() if m else None

def diputaciones(prov):
    def uno(item):
        pc, nom = item
        if pc in SIN_DIPUTACION: return pc, None
        base = ES.get(nom, nom)
        for pref, rol in (("Diputación de ", "Presidente/a de la Diputación"), ("Diputación Provincial de ", "Presidente/a de la Diputación"), ("Diputación Foral de ", "Diputado/a General")):
            w = wikitext(pref + base)
            if not w or w.startswith("#REDIRECT"): continue
            t = campo(w, "titular_nom")
            if not t:
                m = re.search(r"(?:su\s+)?presidente(?:a)?\s+(?:actual\s+)?es\s+(?:el\s+|la\s+)?(\[\[[^\]]+\]\])", w, re.I)
                t = m.group(1) if m else None
            if t:
                nombre, wiki, partido = persona_wiki(t)
                if len(nombre.split()) >= 2:
                    if pc in {"01", "20", "48"}: rol = "Diputado/a General (Diputación Foral)"
                    return pc, {"rol": rol, "ambito": "provincial", "nombre": nombre, "partido": partido, "wiki": wiki, "fuente": "Wikipedia (infobox; verificar)"}
        return pc, None
    with ThreadPoolExecutor(6) as ex: return dict(x for x in ex.map(uno, prov.items()))

# Alcaldes de capital que Wikidata no trae: se leen del cuadro de la ciudad en Wikipedia. Se descarta si el mandato indicado es anterior a 2023.
PAGINAS_CIUDAD = {"02": "Albacete", "07": "Palma de Mallorca", "38": "Santa Cruz de Tenerife", "40": "Segovia"}
def alcaldes_infobox(faltan):
    out = {}
    for pc in faltan:
        t = PAGINAS_CIUDAD.get(pc)
        w = wikitext(t) if t else None
        if not w: continue
        al = campo(w, "alcalde") or campo(w, "alcaldesa")
        if not al: continue
        anio = re.match(r"\s*(\d{4})", campo(w, "alcalde_año") or "")
        if anio and int(anio.group(1)) < 2023: continue          # cuadro desactualizado (mandato anterior a las elecciones de 2023)
        nombre, wiki, partido = persona_wiki(al)
        if len(nombre.split()) >= 2:
            out[pc] = {"rol": f"Alcalde/sa de {t.split(' (')[0]}", "ambito": "municipal", "nombre": nombre, "partido": partido, "wiki": wiki, "fuente": "Wikipedia (cuadro de la ciudad; verificar)"}
    return out

# Presidentes que no salen de Wikidata: página «Presidente de …» de Wikipedia, campo «titular»
PAGINAS_TITULAR = {"31": ("Presidente del Gobierno de Navarra", "Presidente/a de Navarra", "autonómico"),
                   "51": ("Presidente de la Ciudad Autónoma de Ceuta", "Presidente/a de la Ciudad de Ceuta", "autonómico"),
                   "52": ("Presidente de la Ciudad Autónoma de Melilla", "Presidente/a de la Ciudad de Melilla", "autonómico")}
def titulares():
    out = {}
    for pc, (t, rol, amb) in PAGINAS_TITULAR.items():
        w = wikitext(t)
        if not w: continue
        ti = campo(w, "titular")
        if not ti: continue
        nombre, wiki, partido = persona_wiki(ti)
        partido = partido or norm_partido(re.sub(r"\[\[(?:[^\]|]*\|)?([^\]]+)\]\]", r"\1", campo(w, "partido") or ""))
        if len(nombre.split()) >= 2:
            out[pc] = {"rol": rol, "ambito": amb, "nombre": nombre, "partido": partido, "wiki": wiki, "fuente": "Wikipedia (cuadro del cargo; verificar)"}
    return out

def limpiar(t):
    t = re.sub(r"<ref[^>]*/>|<ref[^>]*>.*?</ref>", "", t, flags=re.S)
    return t

def candidatos(prov):
    w = wikitext("Elecciones generales de España de 2026") or ""
    i = w.find("Cabeza de listas por circunscripci")
    t0 = w.find("{|", i); t1 = w.find(NL + "|}", t0)
    tabla = limpiar(w[t0:t1])
    filas = tabla.split(NL + "|-")
    carry = {}; out = {}
    # mapa nombre -> código
    nom2pc = {nrm(ES.get(n, n)): pc for pc, n in prov.items()}; nom2pc.update({nrm(n): pc for pc, n in prov.items()})
    for fila in filas[2:]:
        cells = []
        for line in fila.split(NL):
            if line.startswith("|") and not line.startswith("|}") and not line.startswith("|-"):
                cells.append(line[1:])
        if not cells: continue
        first = cells[0]
        m = re.search(r"\[\[(?:[^\]|]*\|)?([^\]]+)\]\]", first)
        if not m: continue
        key = nrm(m.group(1))
        pc = {nrm(k): c for k, c in SPECIAL.items()}.get(key) or nom2pc.get(key)
        if not pc: continue
        occ = {c for c, n in carry.items() if n > 0}
        col = 0; lst = []
        for c in cells[1:]:
            attrs, content = "", c
            ma = re.match(r"^\s*((?:\w+\s*=\s*(?:\"[^\"]*\"|\S+)\s*)+)\|(?!\|)(.*)$", c)
            if ma and "[[" not in ma.group(1): attrs, content = ma.group(1), ma.group(2)
            while col in occ: col += 1
            cs = int((re.search(r"colspan\s*=\s*\"?(\d+)", attrs) or [0, 1])[1]); rs = int((re.search(r"rowspan\s*=\s*\"?(\d+)", attrs) or [0, 1])[1])
            lst.append((col, cs, rs, content.strip(), attrs)); col += cs
        for c0, cs, rs, content, attrs in lst:
            if rs > 1:
                for k in range(c0, c0 + cs): carry[k] = rs  # se decrementa al terminar la fila
        for k in list(carry):
            if k in occ: carry[k] -= 1
        # tras fijar los nuevos, restamos 1 a los recién creados (la fila actual cuenta)
        for c0, cs, rs, content, attrs in lst:
            if rs > 1:
                for k in range(c0, c0 + cs): carry[k] = rs - 1
        res = []
        for c0, cs, rs, content, attrs in lst:
            txt = content.strip()
            if not txt or "background:#818181" in attrs: continue
            nota = None
            mn = re.search(r"<br\s*/?>\s*\(?([^)<]+)\)?", txt)
            if mn: nota = mn.group(1).strip()
            principal = re.split(r"<br\s*/?>", txt)[0]
            principal = principal.replace("'''", "")
            ml = re.search(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]", principal)
            nombre = (ml.group(2) or ml.group(1)) if ml else re.sub(r"\[\[|\]\]|\{\{[^}]*\}\}|<[^>]+>", "", principal)
            nombre = re.sub(r"\s*\(([A-Za-z\-ÀÉ]+)\)\s*$", "", nombre).strip()
            wiki = ml.group(1).strip().replace(" ", "_") if ml else None
            for k in range(c0, min(c0 + cs, len(COLS))):
                res.append({"partido": COLS[k], "nombre": nombre, "wiki": wiki, "nota": nota})
        # FA y Podemos con colspan 2 -> una sola persona
        vistos = {}
        for r in res:
            kk = (r["nombre"], r["wiki"])
            if kk in vistos and {r["partido"], vistos[kk]["partido"]} == {"FA", "PODEMOS"}: vistos[kk]["partido"] = "FA/PODEMOS"
            elif kk not in vistos: vistos[kk] = r
        out[pc] = list(vistos.values())
    return out

def main():
    prov = json.loads((D / "indice.json").read_text(encoding="utf8"))["prov"]
    cand = candidatos(prov); gob = gobierno(); dip = diputaciones(prov); tit = titulares()
    # huecos de alcaldes: cuadro de la ciudad en Wikipedia
    faltan = [pc for pc in prov if not any(g["ambito"] == "municipal" for g in gob.get(pc, []))]
    alc = alcaldes_infobox(faltan)
    res = {}
    for pc in prov:
        g = list(gob.get(pc, []))
        if alc.get(pc): g.append(alc[pc])
        if tit.get(pc): g.append(tit[pc])
        if dip.get(pc): g.append(dip[pc])
        res[pc] = {"gobierno": g, "candidatos": cand.get(pc, [])}
    out = {"actualizado": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
           "fuentes": {"gobierno": "Wikidata (cargos vigentes) y, para los huecos, cuadros de Wikipedia (diputaciones, ciudades y presidencias): verificar", "candidatos": "https://es.wikipedia.org/wiki/Elecciones_generales_de_Espa%C3%B1a_de_2026"},
           "prov": res}
    (D / "politicos_prov.json").write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf8")
    print("gobierno:", sum(1 for p in res.values() if p["gobierno"]), "provincias;", 
          "candidatos:", sum(1 for p in res.values() if p["candidatos"]), "provincias,", sum(len(p["candidatos"]) for p in res.values()), "personas")
    s = res["37"]; print("Salamanca", [(x["rol"], x["nombre"]) for x in s["gobierno"]], [(x["partido"], x["nombre"]) for x in s["candidatos"]])
main()
from manifest import marcar
marcar("politicos_prov")
