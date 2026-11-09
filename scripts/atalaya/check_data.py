#!/usr/bin/env python3
"""Atalaya: comprueba que los datos regenerados son razonables ANTES de hacer commit.

Si una fuente externa falla (Google Noticias bloquea la IP, Wikipedia cambia una tabla…), los scripts pueden escribir
ficheros casi vacíos; este control hace fallar el workflow para que no se publique nada roto.
Uso (raíz del repo): python3 scripts/atalaya/check_data.py [--semanal]
"""
import json, sys
from pathlib import Path

D = Path(__file__).resolve().parents[2] / "atalaya"
errores = []

def cargar(ruta):
    try: return json.loads((D / ruta).read_text(encoding="utf8"))
    except Exception as e: errores.append(f"{ruta}: no se puede leer ({e})"); return None

def exige(cond, msg):
    if not cond: errores.append(msg)

n = cargar("data/noticias.json")
if n:
    ls = n["noticias"]
    exige(len(ls) >= 300, f"noticias: solo {len(ls)} titulares (mínimo 300)")
    exige(sum(1 for x in ls if x["a"] == "local") >= 150, "noticias: pocos titulares locales (mínimo 150)")
    exige(len({p for x in ls for p in x["pv"]}) >= 35, "noticias: titulares en menos de 35 provincias")

if "--semanal" in sys.argv:
    e = cargar("data/escanos.json")
    if e:
        exige(len(e) >= 50, f"escaños: solo {len(e)} provincias (mínimo 50)")
        exige(all(any(v[-1] for v in x["partidos"].values()) for x in e.values()), "escaños: alguna provincia sin datos de 2023")
    p = cargar("data/politicos_prov.json")
    if p:
        pv = p["prov"]
        exige(sum(1 for x in pv.values() if x["candidatos"]) >= 48, "políticos: candidatos en menos de 48 provincias")
        exige(sum(1 for x in pv.values() if any(g["ambito"] == "municipal" for g in x["gobierno"])) >= 40, "políticos: alcaldes en menos de 40 provincias")
        exige(sum(1 for x in pv.values() if any(g["ambito"] == "autonómico" for g in x["gobierno"])) >= 45, "políticos: presidentes autonómicos en menos de 45 provincias")

res = D / "data/archivo/resumen.json"
if res.exists():
    r = json.loads(res.read_text(encoding="utf8"))
    exige(r["noticias"] >= 1000, f"archivo: solo {r['noticias']} titulares archivados (debe ir creciendo)")
else:
    errores.append("archivo: falta atalaya/data/archivo/resumen.json")

exige(len(list((D / "fichas").glob("*/index.html"))) >= 53, "fichas: faltan páginas (esperadas 53 más el índice)")

if errores:
    print("COMPROBACIÓN FALLIDA:"); [print(" -", x) for x in errores]; sys.exit(1)
print("Datos de Atalaya correctos.")
