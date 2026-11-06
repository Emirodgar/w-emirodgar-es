#!/usr/bin/env python3
"""Atalaya: construye atalaya/data/politicos.json (ficha estructurada de cada político).

Fuente de candidatos: elecciones-espana/data/2026-11-29/candidatos.json (ya mantenido por la skill
actualizar-elecciones-espana) + figuras de seguimiento añadidas a mano abajo. El estado (neutro / en foco /
bajo presión / crisis) NO se guarda aquí: se calcula a partir de titulares, ver atalaya/index.html.
Uso (raíz del repo): python3 scripts/atalaya/build_politicos.py
"""
import json, re
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
ALIAS = {  # variantes con las que se busca a la persona en los titulares (solo nombres no ambiguos)
    "Alberto Núñez Feijóo": ["Feijóo", "Núñez Feijóo"], "Pedro Sánchez": ["Pedro Sánchez"],
    "Santiago Abascal": ["Abascal"], "Gabriel Rufián": ["Rufián"], "Míriam Nogueras": ["Nogueras"],
    "Maribel Vaquero": ["Maribel Vaquero"], "Néstor Rego": ["Néstor Rego"], "Cristina Valido": ["Cristina Valido"],
    "Alberto Catalán": ["Alberto Catalán"],
}
EXTRAS = [  # figuras que interesa seguir aunque no sean cabeza de lista nacional
    {"nombre": "José Luis Rodríguez Zapatero", "partidoId": "PSOE", "cargo": "Expresidente del Gobierno", "alias": ["Zapatero"]},
    {"nombre": "Isabel Díaz Ayuso", "partidoId": "PP", "cargo": "Presidenta de la Comunidad de Madrid", "alias": ["Ayuso"]},
    {"nombre": "Alfonso Fernández Mañueco", "partidoId": "PP", "cargo": "Presidente de la Junta de Castilla y León", "alias": ["Mañueco"]},
    {"nombre": "Irene Montero", "partidoId": "PODEMOS", "cargo": "Aspira a encabezar la lista de Podemos", "alias": ["Irene Montero"]},
]

def slug(s): return re.sub(r"[^a-z0-9]+", "-", s.lower().encode("ascii", "ignore").decode()).strip("-")

def main():
    d = json.loads((RAIZ / "elecciones-espana/data/2026-11-29/candidatos.json").read_text(encoding="utf8"))
    out = []
    for c in d["candidatos"]:
        if not c.get("nombre"):
            out.append({"id": "slot-" + c["partidoId"].lower(), "nombre": None, "partidoId": c["partidoId"], "cargo": None,
                        "ambito": "nacional", "prov": None, "estado": "por_definir", "nota": c.get("nota", ""), "wiki": None, "alias": []})
            continue
        out.append({"id": slug(c["nombre"]), "nombre": c["nombre"], "partidoId": c["partidoId"], "cargo": c.get("cargo"),
                    "ambito": "nacional", "prov": None, "estado": "candidato", "wiki": c["nombre"].replace(" ", "_"),
                    "alias": ALIAS.get(c["nombre"], [c["nombre"]])})
    for e in EXTRAS:
        out.append({"id": slug(e["nombre"]), "nombre": e["nombre"], "partidoId": e["partidoId"], "cargo": e["cargo"], "ambito": "nacional",
                    "prov": None, "estado": "seguimiento", "wiki": e["nombre"].replace(" ", "_"), "alias": e["alias"]})
    (RAIZ / "atalaya/data/politicos.json").write_text(json.dumps({"fuente": "elecciones-espana/data/2026-11-29/candidatos.json",
        "politicos": out}, ensure_ascii=False, indent=1), encoding="utf8")
    print(len(out), "fichas")
main()
