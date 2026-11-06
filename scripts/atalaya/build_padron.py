#!/usr/bin/env python3
"""Atalaya: población oficial por municipio (INE, Cifras oficiales del padrón, tabla 29005) -> atalaya/data/padron.json

  {"actualizado": "...", "anios": [2025, 2023, 2019, 2015, 2011], "mun": {"37274": [pob2025, pob2023, ...]}, "prov": {"37": [...]}}

El código de municipio es el código INE de 5 dígitos, el mismo que usa todo Atalaya. Se descarga el CSV oficial
(~27 MB) a un fichero temporal y solo se guardan los años que coinciden con elecciones generales y el último dato.
Uso (raíz del repo): python3 scripts/atalaya/build_padron.py   (se actualiza una vez al año, cuando el INE publica el padrón)
"""
import csv, json, subprocess, tempfile
from datetime import datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
URL = "https://www.ine.es/jaxiT3/files/t/es/csv_bdsc/29005.csv"
ANIOS_ELEC = [2023, 2019, 2015, 2011]

def main():
    prov = json.loads((RAIZ / "atalaya/data/indice.json").read_text(encoding="utf8"))["prov"]
    with tempfile.TemporaryDirectory() as td:
        f = Path(td) / "padron.csv"
        # Sin cabecera de User-Agent propia: el WAF del INE rechaza agentes que se declaran «bot».
        subprocess.run(["curl", "-s", "-m", "300", "-o", str(f), URL], check=True)
        datos, anios = {}, set()
        with open(f, encoding="utf-8-sig", newline="") as fh:
            for fila in csv.DictReader(fh, delimiter=";"):
                if fila["Sexo"] != "Total" or not fila["Total"].strip(): continue
                cod = fila["Municipios"].split(" ", 1)[0]
                if len(cod) != 5 or cod[:2] not in prov: continue
                a = int(fila["Periodo"]); anios.add(a)
                datos.setdefault(cod, {})[a] = int(fila["Total"].replace(".", ""))
    ultimo = max(anios)
    cols = [ultimo] + [a for a in ANIOS_ELEC if a != ultimo]
    mun = {c: [d.get(a) for a in cols] for c, d in datos.items()}
    provt = {}
    for c, v in mun.items():
        t = provt.setdefault(c[:2], [0] * len(cols))
        for i, x in enumerate(v): t[i] += x or 0
    out = {"actualizado": datetime.now(timezone.utc).strftime("%Y-%m-%d"), "fuente": "INE · Cifras oficiales del padrón por municipio (tabla 29005)",
           "anios": cols, "mun": mun, "prov": provt}
    (RAIZ / "atalaya/data/padron.json").write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf8")
    print(len(mun), "municipios;", len(provt), "provincias; población total", sum(v[0] for v in provt.values()), "en", ultimo)
    for c in ("37274", "28079", "08019"):
        print(c, mun.get(c))
main()
