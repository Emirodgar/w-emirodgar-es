#!/usr/bin/env python3
"""Atalaya: cruce de las promesas de los programas con los temas de preocupación del CIS.

Lee atalaya/data/promesas.json (4.000+ promesas extraídas de los programas) y cuenta, por partido, año del programa y tema de
preocupación, cuántas promesas hay y cuántas son medibles. Guarda solo los recuentos (unos pocos KB) en atalaya/data/promesas_por_tema.json,
para que la página Preocupaciones no tenga que descargar el fichero completo. Los temas de promesas sin equivalente en el CIS
(Justicia, Infraestructuras, Política exterior, Impuestos, Defensa, Derechos, Otros) no se cruzan.
Uso (raíz del repo): python3 scripts/atalaya/build_promesas_temas.py
"""
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from manifest import marcar   # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
# tema de la promesa -> temas de preocupación del CIS (claves de atalaya/preocupaciones). «Empleo» cuenta en paro y en calidad del empleo.
MAPA = {"Economía": ["economia"], "Empleo": ["paro", "empleo"], "Vivienda": ["vivienda"], "Inmigración": ["inmigracion"], "Sanidad": ["sanidad"],
        "Educación": ["educacion"], "Pensiones": ["pensiones"], "Medio ambiente": ["medioambiente"], "Energía": ["energia"],
        "Modelo territorial": ["cataluna"], "Modelo de Estado": ["politica"], "Igualdad": ["sociales"]}


def main():
    src = json.loads((RAIZ / "atalaya/data/promesas.json").read_text(encoding="utf8"))
    cont = defaultdict(lambda: defaultdict(lambda: {"n": 0, "medibles": 0}))
    docs = defaultdict(int)
    for p in src["promesas"]:
        k = f'{p["partido"]}-{p["anio"]}'
        docs[k] += 1
        for t in MAPA.get(p["tema"], []):
            c = cont[k][t]; c["n"] += 1; c["medibles"] += bool(p.get("medible"))
    out = {"actualizado": datetime.now(timezone.utc).replace(microsecond=0).isoformat(), "fuente": "atalaya/data/promesas.json",
           "aviso": "Recuento de promesas extraídas automáticamente de los programas electorales. No mide cumplimiento: el estado de todas está aún sin evidencia.",
           "mapa": MAPA, "total_por_programa": dict(sorted(docs.items())), "programas": {k: dict(sorted(v.items())) for k, v in sorted(cont.items())}}
    (RAIZ / "atalaya/data/promesas_por_tema.json").write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf8")
    marcar("promesas_por_tema")
    print({k: sum(v["n"] for v in t.values()) for k, t in out["programas"].items()})


if __name__ == "__main__":
    main()
