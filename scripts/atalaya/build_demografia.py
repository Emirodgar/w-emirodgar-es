#!/usr/bin/env python3
"""Atalaya: perfil demográfico y renta por municipio (INE, Atlas de distribución de renta de los hogares, operación 353)
-> atalaya/data/demografia.json

  {"anio": 2024, "campos": ["edad_media", "pct_menor18", "pct_65", "renta_persona"],
   "mun": {"37274": [47.4, 13.2, 24.5, 17021.0]}, "prov": {"37": [...]}, "esp": [...]}

Se leen en flujo los CSV oficiales de las tablas «Indicadores demográficos» y «Indicadores de renta media y mediana» (una por provincia),
quedándose solo con las filas de municipio (sin distrito ni sección) y el último año. La media provincial y la de España se ponderan por población (padrón).
Uso (raíz del repo): python3 scripts/atalaya/build_demografia.py     (anual: el INE publica el Atlas cada año)
"""
import json, subprocess
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
D = RAIZ / "atalaya/data"
API = "https://servicios.ine.es/wstempus/js/ES/TABLAS_OPERACION/353"
CSV = "https://www.ine.es/jaxiT3/files/t/es/csv_bdsc/%s.csv"
CAMPOS = ["edad_media", "pct_menor18", "pct_65", "renta_persona"]
INDICADORES = {"Edad media de la población": 0, "Porcentaje de población menor de 18 años": 1, "Porcentaje de población de 65 y más años": 2,
               "Renta neta media por persona": 3}

def tablas():
    # Sin User-Agent propio: el WAF del INE rechaza los agentes que se declaran «bot».
    r = subprocess.run(["curl", "-s", "-m", "60", API], capture_output=True, check=True)
    t = json.loads(r.stdout.decode("utf-8-sig"))
    return [x["Id"] for x in t if x["Nombre"] in ("Indicadores demográficos", "Indicadores de renta media y mediana")]

def numero(x):
    x = x.strip().replace(".", "").replace(",", ".")
    try: return float(x)
    except ValueError: return None

def leer(id_):
    """Devuelve {municipio: {campo: (año, valor)}} de una tabla, o {} si no es de municipios."""
    out = {}
    p = subprocess.Popen(["curl", "-s", "-m", "900", CSV % id_], stdout=subprocess.PIPE)
    primera = True
    for raw in p.stdout:
        f = raw.decode("utf-8-sig", "replace").rstrip("\r\n").split(";")
        if primera: primera = False; continue
        if len(f) < 6 or f[1] or f[2]: continue                       # distritos y secciones fuera
        campo = INDICADORES.get(f[3])
        if campo is None: continue
        cod = f[0].split(" ", 1)[0]
        v, a = numero(f[5]), int(f[4])
        if v is None or len(cod) != 5: continue
        cur = out.setdefault(cod, {}).get(campo)
        if cur is None or a > cur[0]: out[cod][campo] = (a, v)
    p.wait()
    return out

def main():
    ids = tablas()
    print(len(ids), "tablas del Atlas (demográficos + renta)", flush=True)
    mun, anios = {}, []
    with ThreadPoolExecutor(4) as ex:
        for res in ex.map(leer, ids):
            for cod, campos in res.items():
                fila = mun.setdefault(cod, [None] * 4)
                for c, (a, v) in campos.items(): fila[c] = v; anios.append(a)
    pad = json.loads((D / "padron.json").read_text(encoding="utf8"))
    mun = {c: [round(x, 1) if x is not None else None for x in f] for c, f in mun.items() if c in pad["mun"]}
    def pond(codigos):
        out = []
        for i in range(4):
            num = den = 0
            for c in codigos:
                v, p = mun[c][i], (pad["mun"][c][0] or 0)
                if v is not None and p: num += v * p; den += p
            out.append(round(num / den, 1) if den else None)
        return out
    prov = {}
    for c in mun: prov.setdefault(c[:2], []).append(c)
    out = {"actualizado": datetime.now(timezone.utc).strftime("%Y-%m-%d"), "fuente": "INE · Atlas de distribución de renta de los hogares (operación 353)",
           "anio": max(anios) if anios else None, "campos": CAMPOS, "mun": mun, "prov": {p: pond(cs) for p, cs in prov.items()}, "esp": pond(list(mun))}
    (D / "demografia.json").write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf8")
    print(len(mun), "municipios;", sum(1 for f in mun.values() if f[3] is not None), "con renta;", sum(1 for f in mun.values() if f[0] is not None), "con edad. Año", out["anio"])
    print("España", out["esp"], "· Salamanca capital", mun.get("37274"), "· Madrid", mun.get("28079"))
main()
from manifest import marcar
marcar("demografia")
