#!/usr/bin/env python3
"""Atalaya: normaliza las posiciones de los partidos (con cita, fuente y fecha) de /elecciones-espana
en atalaya/data/programas.json, base del módulo «Programas» y del seguimiento de promesas.

Fuente: elecciones-espana/data/2026-11-29/afinidad.json (mantenido con la skill actualizar-elecciones-espana).
Uso (raíz del repo): python3 scripts/atalaya/build_programas.py
"""
import json
from datetime import datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
ECON = {"Impuestos", "Empleo", "Vivienda", "Pensiones", "Energía"}   # clasificación del esquema: económica / política
ORDEN = ["PP", "PSOE", "VOX", "SUMAR", "PODEMOS"]

def main():
    src = json.loads((RAIZ / "elecciones-espana/data/2026-11-29/afinidad.json").read_text(encoding="utf8"))
    partidos = {p["id"]: p for p in json.loads((RAIZ / "elecciones-espana/data/2026-11-29/partidos.json").read_text(encoding="utf8"))["partidos"]}
    afs = []
    for a in src["afirmaciones"]:
        afs.append({"id": a["id"], "tema": a["tema"], "area": "economica" if a["tema"] in ECON else "politica", "texto": a["texto"],
                    "posiciones": {k: a["posiciones"][k] for k in ORDEN if k in a["posiciones"]}})
    out = {"actualizado": datetime.now(timezone.utc).strftime("%Y-%m-%d"), "aviso": src["aviso"],
           "fuente": "elecciones-espana/data/2026-11-29/afinidad.json",
           "partidos": [{"id": k, "siglas": partidos[k]["siglas"], "nombre": partidos[k]["nombre"], "color": partidos[k]["color"]} for k in ORDEN if k in partidos],
           "temas": sorted({a["tema"] for a in afs}), "afirmaciones": afs}
    (RAIZ / "atalaya/data/programas.json").write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf8")
    n = sum(len(a["posiciones"]) for a in afs)
    print(len(afs), "afirmaciones;", n, "posiciones;", sum(1 for a in afs for p in a["posiciones"].values() if p["posicion"] != "sin_posicion"), "con posición documentada")
main()
