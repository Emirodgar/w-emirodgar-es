#!/usr/bin/env python3
"""Atalaya: datos del voto CERA (españoles residentes en el extranjero) para el panel atalaya/cera.

Solo cifras verificadas con fuente:
  1) INE, tabla 32091 (API oficial): electores CERA, participación CERA y solicitudes de voto por correo, por provincia,
     para Europeas 2014, municipales 2015 y 2019 y generales 2016.
  2) Cifras puntuales con enlace a su fuente (Ministerio de Inclusión, Maldita, El Orden Mundial, UNED), anotadas a mano abajo.
Lo que no tiene fuente comprobable no se incluye. Las discrepancias entre fuentes se marcan en el campo «nota».
Salida: atalaya/data/cera.json.   Uso (raíz del repo): python3 scripts/atalaya/build_cera.py
"""
import json, re, subprocess, unicodedata
from datetime import datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
INE = "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/32091?nult=40"
ELECS = {"Elecciones Parlamento Europeo 2014": "europeas-2014", "Elecciones Municipales y Autonómicas 2015": "municipales-2015",
         "Cortes Generales 2016": "generales-2016", "Elecciones Municipales y Autonómicas 2019": "municipales-2019"}
INDS = {"Electores del CERA (definitivos)": "cera", "Total de electores (CER y CERA)": "total", "Solicitudes de voto por correo presentadas": "sol",
        "Solicitudes de voto por correo tramitadas": "sol_ok", "Porcentaje de participación de los electores del CERA": "part"}

def norm(s): return re.sub(r"[^a-z0-9 ]", "", unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()).strip()

def main():
    raw = subprocess.run(["curl", "-s", "-m", "60", INE], capture_output=True, check=True).stdout
    try: txt = raw.decode("utf8")
    except UnicodeDecodeError: txt = raw.decode("latin1")
    serie = json.loads(txt)
    ind = json.load(open(RAIZ / "atalaya/data/indice.json", encoding="utf8"))["prov"]
    por_nombre = {}
    for c, n in ind.items():
        for t in {n, {"Araba": "Álava", "Alacant": "Alicante", "Castelló": "Castellón", "València": "Valencia", "Illes Balears": "Balears",
                      "A Coruña": "Coruña", "Las Palmas": "Palmas", "La Rioja": "Rioja", "Bizkaia": "Vizcaya", "Gipuzkoa": "Guipúzcoa"}.get(n, n)}:
            por_nombre[norm(t)] = c
    nac, prov, sin = {}, {}, set()
    for s in serie:
        partes = s["Nombre"].split(", ")
        elec = next((ELECS[e] for e in ELECS if s["Nombre"].endswith(e)), None)
        ide = INDS.get(partes[0])
        if not elec or not ide or not s["Data"]: continue
        v = s["Data"][0]["Valor"]
        terr = s["Nombre"][len(partes[0]) + 2: -len(next(e for e in ELECS if s["Nombre"].endswith(e))) - 2]
        if terr == "TOTAL NACIONAL": nac.setdefault(elec, {})[ide] = v; continue
        toks = [norm(t) for t in re.split(r"\s*/\s*|,\s*", terr)]
        c = next((por_nombre[t] for t in toks if t in por_nombre), None)
        if not c: sin.add(terr); continue
        prov.setdefault(c, {}).setdefault(elec, {})[ide] = v
    if sin: print("Territorios sin código:", sorted(sin))
    cifras = [  # (año, elección, clave, valor, fuente, nota)
        {"id": "2008", "eleccion": "Generales 2008", "participacion_cera_pct": 31.74,
         "fuente": "https://revistas.uned.es/index.php/derechopolitico/article/download/41765/30110", "nota": "Artículo académico (UNED), previo al voto rogado."},
        {"id": "2011", "eleccion": "Generales 2011", "participacion_cera_pct": 4.9,
         "fuente": "https://elordenmundial.com/voto-exterior-espana-y-que-diferencias-europa/", "nota": "Primera elección con voto rogado."},
        {"id": "2016", "eleccion": "Generales 2016", "electores_cera": nac.get("generales-2016", {}).get("cera"),
         "participacion_cera_pct": nac.get("generales-2016", {}).get("part"),
         "fuente": "https://ine.es/jaxiPx/Tabla.htm?L=0&tpx=32091", "nota": "INE."},
        {"id": "2019a", "eleccion": "Generales abril 2019", "solicitudes": 181268, "no_votaron_pct_de_solicitantes": 35.2,
         "fuente": "https://maldita.es/malditodato/mas-de-80-000-espanoles-que-pidieron-su-voto-desde-el-extranjero-no-votaron-el-10-n-a-pesar-del-record-de-votos-cera/",
         "nota": "Maldita, con datos obtenidos por transparencia."},
        {"id": "2019n", "eleccion": "Generales noviembre 2019", "electores_cera": 2130754, "votos_cera": 145853, "participacion_cera_pct": 6.85, "solicitudes": 226050,
         "no_votaron_pct_de_solicitantes": 35.48,
         "fuente": "https://www.inclusion.gob.es/web/cartaespana/w/el-voto-cera-altera-en-un-escano-el-recuento-electoral-de-las-elecciones-generales",
         "nota": "Ministerio de Inclusión (censo, votos y 6,85 %). Otra fuente (El Orden Mundial) da 5,7 % para 2019: se usa la oficial."},
        {"id": "2023", "eleccion": "Generales julio 2023", "electores_cera": 2327388, "votos_cera": 233688, "participacion_cera_pct": 10.04,
         "fuente": "https://www.inclusion.gob.es/web/cartaespana/w/el-voto-cera-altera-en-un-escano-el-recuento-electoral-de-las-elecciones-generales",
         "nota": "Ministerio de Inclusión. Primera elección sin voto rogado (reforma de 2022)."},
    ]
    escanos = [
        {"eleccion": "Generales 1993", "provincia": "Cantabria", "de": "PP", "a": "PSOE", "fuente": "https://elordenmundial.com/voto-exterior-espana-y-que-diferencias-europa/"},
        {"eleccion": "Generales noviembre 2019", "provincia": "Bizkaia", "de": "PNV", "a": "PP", "fuente": "https://elordenmundial.com/voto-exterior-espana-y-que-diferencias-europa/",
         "nota": "Una sola fuente consultada."},
        {"eleccion": "Generales julio 2023", "provincia": "Madrid", "de": "PSOE", "a": "PP",
         "fuente": "https://www.inclusion.gob.es/web/cartaespana/w/el-voto-cera-altera-en-un-escano-el-recuento-electoral-de-las-elecciones-generales",
         "nota": "Confirmado también por El Orden Mundial. El recuento CERA empezó el viernes 28 de julio, cinco días después de la votación."},
    ]
    contexto = [
        {"dato": "El censo exterior ha crecido en 461.858 personas entre 2022 y 2026 (ley de nietos de 2022).",
         "fuente": "https://elordenmundial.com/voto-exterior-espana-y-que-diferencias-europa/",
         "nota": "Crecimientos anteriores de magnitud parecida: +404.003 entre 1996 y 2000 y +397.276 entre 2011 y 2015, según la misma fuente (Interior e INE)."},
    ]
    out = {"generado": datetime.now(timezone.utc).isoformat(), "aviso": "Solo cifras con fuente enlazada. CERA = españoles residentes en el extranjero.",
           "ine": {"fuente": "https://ine.es/jaxiPx/Tabla.htm?L=0&tpx=32091", "elecciones": {"europeas-2014": "Europeas 2014", "municipales-2015": "Municipales 2015",
                   "generales-2016": "Generales 2016", "municipales-2019": "Municipales 2019"}, "nacional": nac, "provincias": prov},
           "serie": cifras, "escanos": escanos, "contexto": contexto}
    (RAIZ / "atalaya/data/cera.json").write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf8")
    print("provincias:", len(prov), "| nacional:", {k: v.get("cera") for k, v in nac.items()})
main()
