#!/usr/bin/env python3
"""Atalaya: serie REAL de escaños al Congreso por provincia y elección (1977-2023) desde Wikipedia
(página «Circunscripción electoral de X», sección «Congreso de los Diputados»).

Salida: atalaya/data/escanos.json  ->  {prov: {"titulo", "url", "elecciones": [...], "partidos": {partido: [escaños...]}}}
Es una fuente secundaria (Wikipedia cita a Interior); la fuente primaria prevista es infoelectoral.interior.gob.es.
Uso (raíz del repo): python3 scripts/atalaya/build_resultados.py
"""
import json, re, subprocess, urllib.parse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
OUT = RAIZ / "atalaya/data/escanos.json"
NL = "\n"
ALT = {"Araba": ["Álava"], "Alacant": ["Alicante"], "Castelló": ["Castellón"], "Illes Balears": ["las Islas Baleares", "Baleares"],
       "València": ["Valencia"], "Gipuzkoa": ["Guipúzcoa"], "Bizkaia": ["Vizcaya"], "A Coruña": ["La Coruña", "A Coruña"],
       "Ourense": ["Orense", "Ourense"], "Lleida": ["Lérida", "Lleida"], "Girona": ["Gerona", "Girona"]}
PARTIDOS = {"Partido Popular": "PP", "PSOE": "PSOE", "Partido Socialista": "PSOE", "Vox": "Vox", "Ciudadanos": "Cs", "UCD": "UCD",
            "Alianza Popular": "AP/PP", "Podemos": "Podemos", "Unidas Podemos": "Podemos", "Sumar": "Sumar", "Izquierda Unida": "IU"}

def api(title):
    q = urllib.parse.urlencode({"action": "parse", "page": title, "prop": "wikitext", "format": "json", "formatversion": 2, "redirects": 1})
    try:  # curl: el almacén de certificados de algunos Python de Windows está caducado
        r = subprocess.run(["curl", "-s", "-m", "30", "-A", "EmirodgarBot/1.0 (https://emirodgar.es/atalaya)", "https://es.wikipedia.org/w/api.php?" + q],
                           capture_output=True, check=True)
        return json.loads(r.stdout.decode("utf8"))["parse"]["wikitext"]
    except Exception: return None

def seats(v):
    m = re.match(r"\s*(\d+)", re.sub(r"<[^>]+>|\{\{[^}]*\}\}", "", v)); return int(m.group(1)) if m else None

def parse(w):
    c = w.find("== Congreso de los Diputados ==")
    if c < 0: return None
    m0 = re.search(r"===[^=\n]*(?:Diputados|Escaños)[^=\n]*obtenidos por (?:partido|candidatura)[^=\n]*===", w[c:])
    if not m0: return None
    t0 = w.find("{|", c + m0.end()); t1 = w.find(NL + "|}", t0)
    filas = w[t0:t1].split(NL + "|-")
    cab = filas[1] if len(filas) > 1 else ""
    cab = re.sub(r"\[\[[^\]|]*\|([^\]]*)\]\]", r"\1", cab)      # [[destino|2023]] -> 2023
    labels = []
    for y, r in re.findall(r"(\d{4})(?:[^|!\]\d]*?\(([IV]+)\))?", cab[cab.find("Candidatura"):]):
        labels.append(y + (" " + r if r else ""))
    if not labels: return None
    out = {}
    for fila in filas[2:]:
        m = re.search(NL + r"\|\s*\[\[([^\]|]+)(?:\|([^\]]*))?\]\]", fila)
        if not m: continue
        nombre = next((v for k, v in PARTIDOS.items() if k.lower() in (m.group(1) + " " + (m.group(2) or "")).lower()), None)
        if not nombre: continue
        vals = [seats(x) for x in fila[m.end():].split("||")[1:]]
        vals = (vals + [None] * len(labels))[:len(labels)]
        acc = out.setdefault(nombre, [0] * len(labels))
        out[nombre] = [a + (b or 0) for a, b in zip(acc, vals)]
    tot = None
    mt = re.search(r"Total[^\n]*", w[t0:t1])
    if mt:
        tv = [seats(x) for x in mt.group(0).split("||")[1:]]
        tot = (tv + [None] * len(labels))[:len(labels)]
    if out and not any(v[-1] for v in out.values()):   # última columna = elección aún no celebrada
        labels = labels[:-1]; out = {k: v[:-1] for k, v in out.items()}; tot = tot[:-1] if tot else tot
    return {"elecciones": labels, "partidos": out, "total": tot} if out else None

def un(p):
    pc, nombre = p
    for alias in ALT.get(nombre, [nombre]):
        title = "Circunscripción electoral de " + alias
        w = api(title)
        if w:
            r = parse(w)
            if r:
                r.update({"titulo": title, "url": "https://es.wikipedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_"))}); return pc, r
    return pc, None

def main():
    prov = json.loads((RAIZ / "atalaya/data/indice.json").read_text(encoding="utf8"))["prov"]
    with ThreadPoolExecutor(6) as ex: res = dict(ex.map(un, prov.items()))
    ok = {k: v for k, v in res.items() if v and any(x[-1] for x in v["partidos"].values())}   # descarta tablas mal leídas
    OUT.write_text(json.dumps(ok, ensure_ascii=False, separators=(",", ":")), encoding="utf8")
    print(len(ok), "provincias con datos; sin datos:", [prov[k] for k in prov if k not in ok])
    s = ok.get("37")
    if s: print("Salamanca", s["elecciones"][-3:], {k: v[-3:] for k, v in s["partidos"].items()})
main()
