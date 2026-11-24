#!/usr/bin/env python3
"""Atalaya: señales externas del panel de tendencias (v2): Google Noticias e interés de búsqueda de Google Trends.

Salida: atalaya/data/tendencias_google.json
  gnews  → por partido/político: titulares en Google Noticias en las últimas 24 h, ritmo (titulares/hora), nº de medios y 3 titulares.
           Google devuelve como mucho 100 por consulta: si se llena, el ritmo se calcula sobre el tramo que cubren esos 100 (lim=true).
  trends → índice de búsqueda en Google España (0-100, comparable entre entidades del mismo grupo) por hora los últimos 7 días,
           y reparto por comunidad autónoma. No hay API oficial: pytrends es frágil (429). Si falla, se conserva el último dato bueno
           y se marca con su fecha; el panel muestra de cuándo es.
Uso (raíz del repo): python3 scripts/atalaya/build_tendencias_google.py [--sin-trends] [--sin-gnews]
Requiere para Trends: pip install pytrends
"""
import json, re, subprocess, sys, time, unicodedata, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_tendencias_vivo import PARTIDOS, POLITICOS, CCAA   # noqa: E402  (mismas entidades que el panel)

RAIZ = Path(__file__).resolve().parents[2]
SALIDA = RAIZ / "atalaya/data/tendencias_google.json"
UA = "Mozilla/5.0 (compatible; EmirodgarBot/1.0; +https://emirodgar.es/atalaya)"
GN = "https://news.google.com/rss/search?hl=es&gl=ES&ceid=ES:es&q="

# Consulta de Google Noticias por entidad (las que no figuran usan su nombre entre comillas)
GN_Q = {
    "PP": '"Partido Popular" OR "PP"', "PSOE": 'PSOE OR "Partido Socialista"', "Vox": "Vox", "Sumar": "Sumar",
    "Podemos": 'Podemos (Belarra OR "Irene Montero" OR partido)', "ERC": 'ERC OR "Esquerra Republicana"', "Junts": "Junts",
    "Bildu": "Bildu", "PNV": "PNV", "BNG": "BNG", "CC": '"Coalición Canaria"', "UPN": "UPN", "Compromis": "Compromís",
    "UPL": '"Unión del Pueblo Leonés"', "SALF": '"Se Acabó La Fiesta" OR Alvise',
    "sanchez": '"Pedro Sánchez"', "feijoo": "Feijóo", "abascal": "Abascal", "ayuso": "Ayuso", "manueco": "Mañueco",
    "zapatero": "Zapatero", "yolanda": '"Yolanda Díaz"', "irene": '"Irene Montero"', "montero": '"María Jesús Montero"',
    "puigdemont": "Puigdemont", "junqueras": "Junqueras", "rufian": "Rufián", "illa": '"Salvador Illa"', "colau": '"Ada Colau"',
    "page": '"García-Page"', "moreno": '"Juanma Moreno"',
}
# Términos de Google Trends. El primero de cada grupo es el ancla: aparece en todas las tandas para poder compararlas entre sí.
TRENDS = {
    "partido": [("PSOE", "PSOE"), ("PP", "Partido Popular"), ("Vox", "Vox"), ("Sumar", "Sumar"), ("Podemos", "partido Podemos"),
                ("ERC", "ERC"), ("Junts", "Junts"), ("Bildu", "Bildu"), ("PNV", "PNV")],
    "politico": [("sanchez", "Pedro Sánchez"), ("feijoo", "Feijóo"), ("abascal", "Abascal"), ("ayuso", "Ayuso"), ("yolanda", "Yolanda Díaz"),
                 ("manueco", "Mañueco"), ("puigdemont", "Puigdemont"), ("zapatero", "Zapatero"), ("irene", "Irene Montero"), ("rufian", "Rufián")],
}

def norm(s): return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()

def get(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=25) as r: return r.read()
    except Exception:   # certificados en algunos Python de Windows: reintento con curl
        r = subprocess.run(["curl", "-s", "-L", "-m", "25", "-A", UA, url], capture_output=True)
        if not r.stdout: raise
        return r.stdout

# ---------------------------------------------------------------- Google Noticias
def gnews(eid, ahora):
    q = f"{GN_Q[eid]} when:1d"
    try: raiz = ET.fromstring(get(GN + quote(q)))
    except Exception as e: print("GNEWS FALLO", eid, repr(e)[:80]); return None
    its = []
    for it in raiz.iter("item"):
        try: dt = parsedate_to_datetime(it.findtext("pubDate")).astimezone(timezone.utc)
        except Exception: continue
        t = (it.findtext("title") or "").strip(); medio = (it.findtext("source") or "").strip()
        if medio and t.endswith(" - " + medio): t = t[: -len(medio) - 3]   # Google añade « - Medio» al titular
        its.append((dt, t, medio, (it.findtext("link") or "").strip()))
    its = [x for x in its if ahora - timedelta(hours=24) <= x[0] <= ahora + timedelta(minutes=5)]
    if not its: return {"n": 0, "ritmo": 0, "medios": 0, "lim": False, "top": []}
    its.sort(key=lambda x: x[0], reverse=True)
    lim = len(its) >= 95
    span = max(1.0, (ahora - its[-1][0]).total_seconds() / 3600) if lim else 24.0
    return {"n": len(its), "ritmo": round(len(its) / span, 1), "medios": len({x[2] for x in its if x[2]}), "lim": lim,
            "top": [{"t": x[1], "m": x[2], "u": x[3], "f": x[0].isoformat()} for x in its[:3]]}

def bloque_gnews(ahora):
    out, fallos = {}, 0
    ids = [p[0] for p in PARTIDOS] + [x[0] for x in POLITICOS]
    for eid in ids:
        r = gnews(eid, ahora)
        if r is None:
            fallos += 1
            if fallos >= 6: break      # Google nos está limitando: no insistir
        else: out[eid] = r
        time.sleep(1.2)
    return out if len(out) >= len(ids) * 0.7 else None

# ---------------------------------------------------------------- Google Trends
def ccaa_de(nombre):
    n = norm(nombre)
    for k, rx in [("Madrid", r"madrid"), ("Cataluña", r"catalu|catalon"), ("Andalucía", r"andalu"), ("Castilla y León", r"castilla (y|and) leon"),
                  ("Castilla-La Mancha", r"castilla.la mancha"), ("C. Valenciana", r"valenc"), ("País Vasco", r"vasc|basque"),
                  ("Illes Balears", r"balear"), ("Canarias", r"canari|canary"), ("Murcia", r"murcia"), ("Navarra", r"navarr"),
                  ("Aragón", r"arag"), ("Asturias", r"asturi"), ("Cantabria", r"cantabri"), ("Galicia", r"galici"), ("La Rioja", r"rioja"),
                  ("Extremadura", r"extremadura"), ("Ceuta", r"ceuta"), ("Melilla", r"melilla")]:
        if re.search(rx, n): return k
    return None

def bloque_trends():
    from pytrends.request import TrendReq
    pt = TrendReq(hl="es-ES", tz=-60, timeout=(10, 30), retries=2, backoff_factor=3)
    res = {}
    for grupo, terminos in TRENDS.items():
        ancla = terminos[0]; resto = terminos[1:]
        tandas = [[ancla] + resto[i:i + 4] for i in range(0, len(resto), 4)]
        series, regiones, f_serie, f_reg = {}, {}, {}, {}
        horas = None
        for k, tanda in enumerate(tandas):
            kws = [t[1] for t in tanda]
            pt.build_payload(kws, timeframe="now 7-d", geo="ES")
            df = pt.interest_over_time(); time.sleep(3)
            rg = pt.interest_by_region(resolution="REGION", inc_low_vol=True); time.sleep(3)
            if horas is None: horas = [d.to_pydatetime().replace(tzinfo=timezone.utc).isoformat() for d in df.index]
            sa = float(df[ancla[1]].sum()); ra = float(rg[ancla[1]].sum())
            if k == 0: sa0, ra0 = sa, ra
            if sa <= 0 or ra <= 0: raise RuntimeError(f"ancla sin datos en {grupo}")
            fs, fr = sa0 / sa, ra0 / ra       # reescala la tanda para que el ancla valga lo mismo que en la primera
            for eid, kw in tanda:
                if eid in series: continue
                series[eid] = [float(v) * fs for v in df[kw].tolist()[:len(horas)]]
                reg = {}
                for nombre, v in rg[kw].items():
                    c = ccaa_de(nombre)
                    if c: reg[c] = float(v) * fr
                regiones[eid] = reg
        mx = max(max(s) for s in series.values()) or 1
        # serie: comparable entre entidades del grupo. region: normalizada por entidad (100 = donde más pesa para ella),
        # porque el reparto territorial describe dónde se busca relativamente más, no cuánto.
        res[grupo] = {eid: {"serie": [round(v / mx * 100, 1) for v in s],
                            "region": {c: round(v / (max(regiones[eid].values()) or 1) * 100, 1) for c, v in regiones[eid].items()}}
                      for eid, s in series.items()}
        res[grupo + "_horas"] = horas
    return res

def main():
    ahora = datetime.now(timezone.utc)
    prev = json.loads(SALIDA.read_text(encoding="utf8")) if SALIDA.exists() else {}
    sal = {"generado": ahora.isoformat(),
           "aviso": "Google Noticias: titulares de las últimas 24 h (Google devuelve un máximo de 100 por consulta). "
                    "Google Trends: índice relativo de búsqueda en España, no es un número de búsquedas."}
    if "--sin-gnews" in sys.argv: sal["gnews"] = prev.get("gnews")
    else:
        g = bloque_gnews(ahora)
        sal["gnews"] = {"fecha": ahora.isoformat(), "ok": True, "datos": g} if g else {**(prev.get("gnews") or {}), "ok": False}
        print("Google Noticias:", f"{len(g)} entidades" if g else "FALLÓ, se conserva el dato anterior")
    if "--sin-trends" in sys.argv: sal["trends"] = prev.get("trends")
    else:
        try:
            t = bloque_trends()
            sal["trends"] = {"fecha": ahora.isoformat(), "ok": True, **t}
            print("Google Trends: OK", {k: len(v) for k, v in t.items() if isinstance(v, dict)})
        except Exception as e:
            print("Google Trends FALLÓ:", type(e).__name__, str(e)[:150], "→ se conserva el dato anterior")
            sal["trends"] = {**(prev.get("trends") or {}), "ok": False}
    SALIDA.write_text(json.dumps(sal, ensure_ascii=False, separators=(",", ":")), encoding="utf8")
    print(f"{SALIDA.name}: {SALIDA.stat().st_size // 1024} KB")

if __name__ == "__main__":
    main()
