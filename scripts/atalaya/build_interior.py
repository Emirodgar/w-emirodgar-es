#!/usr/bin/env python3
"""Atalaya: importa los resultados oficiales del Ministerio del Interior (infoelectoral) descargados a mano.

Entrada (carpeta privada, no se publica): data-private/interior/*.zip (cada .zip trae un .xlsx de «Resultados por municipio»
o «por circunscripción»). Se reconoce cada fichero por la primera fila de su hoja, p. ej. «Congreso | Julio 2023 | Resultados por municipio».
Salida (pública, compacta):
  atalaya/data/resultados/indice.json                      elecciones disponibles y partidos
  atalaya/data/resultados/<eleccion>/<NN>.json             un fichero por provincia con todos sus municipios
  atalaya/data/resultados/<eleccion>/circunscripciones.json  resultados por provincia, con votos y escaños (si el fichero existe)
Solo lee en flujo (xlsx = zip de XML); no necesita librerías externas. Nunca borra: si una elección ya está, se vuelve a escribir igual.
Uso (raíz del repo): python3 scripts/atalaya/build_interior.py
"""
import io, json, re, unicodedata, zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
ENTRADA = RAIZ / "data-private/interior"
SALIDA = RAIZ / "atalaya/data/resultados"
M = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
MESES = {"enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6, "julio": 7, "agosto": 8, "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12}
TIPOS = {"congreso": ("Congreso de los Diputados", "congreso"), "senado": ("Senado", "senado"), "municipales": ("Elecciones municipales", "municipales"),
         "cabildos insulares": ("Cabildos insulares", "cabildos"), "parlamento europeo": ("Parlamento Europeo", "europeas")}

def slug(s): return re.sub(r"[^a-z0-9]+", "-", unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()).strip("-")

def hojas(zpath):
    """Genera (nombre_hoja, filas) leyendo el .xlsx del interior del zip en flujo."""
    z = zipfile.ZipFile(zpath)
    x = zipfile.ZipFile(io.BytesIO(z.read(next(n for n in z.namelist() if n.endswith(".xlsx")))))
    ss = []
    if "xl/sharedStrings.xml" in x.namelist():
        for _, el in ET.iterparse(x.open("xl/sharedStrings.xml")):
            if el.tag == M + "si": ss.append("".join(t.text or "" for t in el.iter(M + "t"))); el.clear()
    wb = ET.fromstring(x.read("xl/workbook.xml"))
    nombres = [s.get("name") for s in wb.find(M + "sheets")]
    for i, nombre in enumerate(nombres, 1):
        def filas(i=i):
            for _, el in ET.iterparse(x.open(f"xl/worksheets/sheet{i}.xml")):
                if el.tag == M + "row":
                    fila = []
                    for c in el.findall(M + "c"):
                        v = c.find(M + "v"); t = c.get("t")
                        fila.append(ss[int(v.text)] if t == "s" and v is not None else (v.text if v is not None else ""))
                    yield fila; el.clear()
        yield nombre, filas()

def num(x):
    try: return int(float(x))
    except (ValueError, TypeError): return 0

def titulo(txt):
    """«Congreso | Julio 2023 | Resultados por municipio» -> (id, nombre, fecha ISO aprox., ámbito)."""
    t, mes, tipo = [p.strip() for p in txt.split("|")]
    nombre_t, corto = TIPOS.get(t.lower(), (t, slug(t)))
    m, a = mes.lower().split()
    eid = f"{corto}-{a}-{MESES[m]:02d}"
    return eid, f"{nombre_t} · {mes}", tipo.lower()

def leer(zpath):
    for nombre, filas in hojas(zpath):
        it = iter(filas)
        primera = next(it, None)
        while primera is not None and not any(primera): primera = next(it, None)    # el fichero del Senado trae filas vacías arriba
        if not primera or "|" not in (primera[0] or ""): continue
        eid, enombre, ambito = titulo(primera[0])
        nombres = abrevs = None; datos = []
        previa = None
        for f in it:
            if f and f[0] == "Nombre de Comunidad": nombres, abrevs = previa, f; continue
            if abrevs is None: previa = f; continue
            datos.append(f)
        if nombres is None: nombres = abrevs                                  # hojas sin fila de nombres completos
        yield eid, enombre, ambito, nombres, abrevs, datos

def municipios(zpath):
    out = {}
    for eid, enombre, ambito, nombres, abrevs, datos in leer(zpath):
        if "municipio" not in ambito or eid.startswith("senado"): continue   # el Senado se vota por candidatos, no por partidos: otro formato
        e = out.setdefault(eid, {"nombre": enombre, "partidos": {}, "prov": {}})
        for j in range(13, len(abrevs)):
            if abrevs[j] and (nombres[j] if j < len(nombres) else ""): e["partidos"][abrevs[j]] = nombres[j]
        for f in datos:
            if len(f) < 13 or not f[1].strip().isdigit() or not f[3].strip().isdigit(): continue
            cod = f"{int(f[1]):02d}{int(f[3]):03d}"
            v = {abrevs[j]: num(f[j]) for j in range(13, min(len(f), len(abrevs))) if abrevs[j] and num(f[j]) > 0}
            e["prov"].setdefault(cod[:2], {})[cod] = {"n": f[4], "pob": num(f[5]), "mesas": num(f[6]), "censo": num(f[7]), "votantes": num(f[8]), "validos": num(f[9]),
                                                      "blanco": num(f[11]), "nulos": num(f[12]), "v": v}
    return out

def circunscripciones(zpath):
    out = {}
    for eid, enombre, ambito, nombres, abrevs, datos in leer(zpath):
        if "circunscri" not in ambito or eid.startswith("senado"): continue
        base = {h: i for i, h in enumerate(abrevs[:16])}
        res = {}
        for f in datos:
            if len(f) < 16 or not f[1].strip().isdigit(): continue
            r = {"n": f[2], "censo": num(f[base["Total censo electoral"]]), "votantes": num(f[base["Total votantes"]]), "validos": num(f[base["Votos válidos"]]),
                 "blanco": num(f[base["Votos en blanco"]]), "nulos": num(f[base["Votos nulos"]]), "v": {}}
            # pares «Votos / Diputados» bajo cada partido: la abreviatura está en la fila de nombres cortos, que es la de arriba
            for k in range(15, len(f) - 1, 2):
                sigla = nombres[k - 15] if 0 <= k - 15 < len(nombres) else ""
                if sigla and (num(f[k]) or num(f[k + 1])): r["v"][sigla] = [num(f[k]), num(f[k + 1])]
            res[f"{int(f[1]):02d}"] = r
        out[eid] = {"nombre": enombre, "prov": res}
    return out

def main():
    zips = sorted(ENTRADA.glob("*.zip"))
    if not zips: print(f"No hay ficheros en {ENTRADA}"); return
    SALIDA.mkdir(parents=True, exist_ok=True)
    indice = json.loads((SALIDA / "indice.json").read_text(encoding="utf8")) if (SALIDA / "indice.json").exists() else {"elecciones": {}}
    for z in zips:
        print("Leyendo", z.name, flush=True)
        for eid, e in municipios(z).items():
            carp = SALIDA / eid; carp.mkdir(exist_ok=True)
            tot = 0
            for pc, muns in e["prov"].items():
                usados = {p for m in muns.values() for p in m["v"]}
                (carp / f"{pc}.json").write_text(json.dumps({"eleccion": eid, "partidos": {p: e["partidos"].get(p, p) for p in sorted(usados)}, "mun": muns},
                                                            ensure_ascii=False, separators=(",", ":")), encoding="utf8"); tot += len(muns)
            ind = indice["elecciones"].setdefault(eid, {"id": eid})
            ind.update({"nombre": e["nombre"], "fuente": "Ministerio del Interior (infoelectoral.interior.gob.es)", "municipios": tot, "partidos": e["partidos"]})
            print(f"  {eid}: {tot} municipios en {len(e['prov'])} provincias")
        for eid, e in circunscripciones(z).items():
            carp = SALIDA / eid; carp.mkdir(exist_ok=True)
            (carp / "circunscripciones.json").write_text(json.dumps({"eleccion": eid, "prov": e["prov"]}, ensure_ascii=False, separators=(",", ":")), encoding="utf8")
            indice["elecciones"].setdefault(eid, {"id": eid})["circunscripciones"] = len(e["prov"])
            print(f"  {eid}: {len(e['prov'])} circunscripciones")
    (SALIDA / "indice.json").write_text(json.dumps(indice, ensure_ascii=False, indent=1), encoding="utf8")

if __name__ == "__main__":
    main()
    from manifest import marcar
    marcar("resultados")
