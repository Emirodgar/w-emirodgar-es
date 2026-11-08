#!/usr/bin/env python3
"""Atalaya: archivo permanente de encuestas.

Recoge los sondeos de cada convocatoria de /elecciones-espana (elecciones-espana/data/<fecha>/encuestas.json) y los
exportados a mano desde el panel (atalaya/data/encuestas-manuales.json) y los fusiona en atalaya/data/encuestas.json.

Principio del proyecto: NUNCA se borra nada. Una encuesta que deja de aparecer en la fuente se conserva con "ausente";
las que se archivan desde el panel quedan con "archivada": true y siguen en el fichero.
Clave de cada encuesta: fecha | empresa | ámbito | convocatoria.
Uso (raíz del repo): python3 scripts/atalaya/build_encuestas.py
"""
import json, re, unicodedata
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
OUT = RAIZ / "atalaya/data/encuestas.json"
MANUAL = RAIZ / "atalaya/data/encuestas-manuales.json"
HOY = date.today().isoformat()
slug = lambda s: re.sub(r"[^a-z0-9]+", "-", unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()).strip("-")

def clave(e): return f'{e["fecha"]}|{slug(e["empresa"])}|{e.get("ambito","ES")}|{e.get("convocatoria","")}'

def leer_fuentes():
    for d in sorted((RAIZ / "elecciones-espana/data").iterdir()):
        f = d / "encuestas.json"
        if not (d.is_dir() and f.exists()): continue
        j = json.loads(f.read_text(encoding="utf8"))
        for s in j.get("sondeos", []):
            yield {"fecha": s["fecha"], "empresa": s["empresa"], "medio": s.get("medio"), "muestra": s.get("muestra"), "tipo": s.get("tipo"),
                   "ambito": "ES", "convocatoria": d.name, "voto": s["voto"], "fuente": f"elecciones-espana/data/{d.name}/encuestas.json"}
    if MANUAL.exists():
        for s in json.loads(MANUAL.read_text(encoding="utf8")):
            yield {"fecha": s["fecha"], "empresa": s["empresa"], "medio": s.get("medio"), "muestra": s.get("muestra") or s.get("n"), "tipo": s.get("tipo", "manual"),
                   "ambito": s.get("ambito", "ES"), "convocatoria": s.get("convocatoria", ""), "voto": s["voto"], "fuente": "manual"}

def main():
    viejo = json.loads(OUT.read_text(encoding="utf8")) if OUT.exists() else {"encuestas": []}
    act = {clave(e): e for e in viejo["encuestas"]}
    vistas = set()
    for e in leer_fuentes():
        k = clave(e); vistas.add(k)
        if k in act:   # se actualizan los datos de la fuente; la marca "archivada" y la fecha de captura se conservan
            a = act[k]; a.update({x: y for x, y in e.items() if y is not None}); a.pop("ausente", None)
        else:
            act[k] = {**e, "capturada": HOY, "archivada": False}
    for k, a in act.items():
        if k not in vistas and not a.get("ausente"): a["ausente"] = HOY
    lista = sorted(act.values(), key=lambda a: (a["fecha"], a["empresa"]), reverse=True)
    out = {"descripcion": "Archivo permanente de encuestas. No se borra nada: se archiva.", "actualizado": HOY, "encuestas": lista}
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf8")
    print(f"{len(lista)} encuestas archivadas ({len(vistas)} vistas hoy)")

if __name__ == "__main__": main()
