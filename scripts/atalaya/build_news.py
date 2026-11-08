#!/usr/bin/env python3
"""Atalaya: recoge titulares por RSS y los etiqueta por provincia, municipio y partido.
Prototipo. Solo librería estándar. Salida: atalaya/data/noticias.json
Requiere haber ejecutado build_geo.py (usa atalaya/data/indice.json).
Uso (raíz del repo): python3 scripts/atalaya/build_news.py
"""
import hashlib, json, re, unicodedata, urllib.request, xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from html import unescape
from pathlib import Path
from urllib.parse import quote

RAIZ = Path(__file__).resolve().parents[2]
UA = "Mozilla/5.0 (compatible; EmirodgarBot/1.0; +https://emirodgar.es/atalaya)"
GN = "https://news.google.com/rss/search?hl=es&gl=ES&ceid=ES:es&q="
NACIONAL = [
    ("El País", "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/espana/portada"),
    ("El Mundo", "https://e00-elmundo.uecdn.es/elmundo/rss/espana.xml"),
    ("elDiario.es", "https://www.eldiario.es/rss/politica"),
    ("20minutos", "https://www.20minutos.es/rss/nacional/"),
    ("Europa Press", "https://www.europapress.es/rss/rss.aspx?ch=66"),
]
ALIAS = {"Araba": "Álava", "Alacant": "Alicante", "Castelló": "Castellón", "Illes Balears": "Baleares", "València": "Valencia",
         "Gipuzkoa": "Guipúzcoa", "Bizkaia": "Vizcaya", "Asturias": "Asturias"}
PARTIDOS = {"PP": r"\bPP\b|Partido Popular|Feijóo|Mañueco", "PSOE": r"\bPSOE\b|socialist|Sánchez",
            "Vox": r"\bVox\b|Abascal", "Sumar": r"\bSumar\b|Yolanda Díaz", "Podemos": r"Podemos",
            "UPL": r"\bUPL\b|Unión del Pueblo Leonés", "Cs": r"Ciudadanos"}
RIESGO = r"detenid|detención|imputad|investigad|corrupci|dimisi|accidente|incendio|fallec|muert|querella|escándalo|dana|inundaci|huelga|protesta"

def norm(s): return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
def get(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=25) as r: return r.read()
    except Exception:   # certificados caducados en el almacén de algunos Python de Windows: reintento con curl
        import subprocess
        r = subprocess.run(["curl", "-s", "-L", "-m", "25", "-A", UA, url], capture_output=True)
        if not r.stdout: raise
        return r.stdout
def items(xml):
    for it in ET.fromstring(xml).iter("item"):
        d = it.findtext("pubDate")
        try: dt = parsedate_to_datetime(d).astimezone(timezone.utc)
        except Exception: dt = datetime.now(timezone.utc)
        yield unescape((it.findtext("title") or "").strip()), (it.findtext("link") or "").strip(), dt, it.findtext("source")
POLITICA = re.compile(r"alcald|ayuntamient|diputaci|pleno|concejal|\bPP\b|PSOE|\bVox\b|Sumar|Podemos|elecciones|candidat|\bJunta\b|Gobierno|consejer|partido|municip|oposici|presupuest|subvenci|cortes|congreso|senado|socialist|popular", re.I)
LOCALES = RAIZ / "scripts/atalaya/medios_locales.json"

def items_cualquiera(xml):
    """RSS 2.0 o Atom: (titulo, enlace, fecha)."""
    raiz = ET.fromstring(xml)
    for it in raiz.iter("item"):
        d = it.findtext("pubDate")
        try: dt = parsedate_to_datetime(d).astimezone(timezone.utc)
        except Exception: dt = datetime.now(timezone.utc)
        yield unescape((it.findtext("title") or "").strip()), (it.findtext("link") or "").strip(), dt
    A = "{http://www.w3.org/2005/Atom}"
    for e in raiz.iter(A + "entry"):
        lk = next((l.get("href") for l in e.findall(A + "link") if l.get("rel") in (None, "alternate")), "")
        d = e.findtext(A + "updated") or e.findtext(A + "published") or ""
        try: dt = datetime.fromisoformat(d.replace("Z", "+00:00")).astimezone(timezone.utc)
        except Exception: dt = datetime.now(timezone.utc)
        yield unescape((e.findtext(A + "title") or "").strip()), lk, dt

def wb(n): return re.compile(r"(?<!\w)" + re.escape(norm(n)) + r"(?!\w)")

def main():
    ind = json.load(open(RAIZ / "atalaya/data/indice.json", encoding="utf8"))
    provs = ind["prov"]; muns_by_prov = {}
    for c, n in [m for m in ind["mun"] if m[0][:2] in provs]: muns_by_prov.setdefault(c[:2], []).append((c, n))
    nombres = {}
    for c, n in ind["mun"]: nombres.setdefault(norm(n), []).append(c)
    unico = {n: v[0] for n, v in nombres.items() if len(v) == 1 and len(n) > 6}   # municipios con nombre único en España
    pat_unico = [(c, wb(n)) for n, c in unico.items()]
    pat_prov = [(pc, [wb(x) for x in {n, ALIAS.get(n, n)}]) for pc, n in provs.items()]
    pat_mun = {pc: [(c, wb(n)) for c, n in ms if len(n) > 4] for pc, ms in muns_by_prov.items()}

    def local(pc):
        a = ALIAS.get(provs[pc], provs[pc])
        q = f'"{a}" (alcalde OR ayuntamiento OR elecciones OR PP OR PSOE OR Vox OR pleno) when:3d'
        try: xml = get(GN + quote(q))
        except Exception as e: print("FALLO", a, e); return []
        return [(pc, *x) for x in list(items(xml))[:22]]
    def nacional(f):
        try: return [(None, *x, f[0]) for x in items(get(f[1]))]
        except Exception as e: print("FALLO", f[0], e); return []

    def directo(m):
        try: xml = get(m["url"])
        except Exception as e: print("FALLO", m["medio"], e); return []
        try: lst = list(items_cualquiera(xml))
        except Exception as e: print("FEED ILEGIBLE", m["medio"], e); return []
        return [(m["prov"], t, l, dt, None, m["medio"]) for t, l, dt in lst if POLITICA.search(t)][:40]
    medios = json.load(open(LOCALES, encoding="utf8"))["medios"] if LOCALES.exists() else []

    with ThreadPoolExecutor(8) as ex:
        loc = list(ex.map(local, provs)); nac = list(ex.map(nacional, NACIONAL)); dire = list(ex.map(directo, medios))
    out, vistos = [], set()
    def add(pc, t, l, dt, src, medio, ambito, d=False):
        key = norm(t)[:80]
        if key in vistos or not l: return
        vistos.add(key); nt = norm(t)
        pv = {pc} if pc else set()
        for p, pats in pat_prov:
            if any(x.search(nt) for x in pats): pv.add(p)
        # con provincia conocida (prensa local) solo se buscan municipios de esa provincia: evita falsos positivos como «Montserrat»
        mun = set() if (pc and ambito == "local") else {c for c, rx in pat_unico if rx.search(nt)}
        for p in pv: mun |= {c for c, rx in pat_mun.get(p, []) if rx.search(nt)}
        pv |= {c[:2] for c in mun}
        out.append({"i": hashlib.sha1(l.encode("utf8")).hexdigest()[:12], "t": t, "u": l, "f": dt.isoformat(), "m": medio, "a": ambito, "pv": sorted(pv), "mun": sorted(mun), **({"d": 1} if d else {}),
                    "p": [k for k, rx in PARTIDOS.items() if re.search(rx, t, re.I)], "r": bool(re.search(RIESGO, nt))})
    for lst in dire:   # primero los feeds propios de cada medio: son los más fiables y ganan en los duplicados
        for pc, t, l, dt, src, medio in lst: add(pc, t, l, dt, src, medio, "local", True)
    for lst in nac:
        for pc, t, l, dt, src, medio in lst: add(pc, t, l, dt, src, medio, "nacional")
    for lst in loc:
        for pc, t, l, dt, src in lst: add(pc, t, l, dt, src, src or "Prensa local", "local")
    out.sort(key=lambda x: x["f"], reverse=True)
    (RAIZ / "atalaya/data/noticias.json").write_text(json.dumps({"generado": datetime.now(timezone.utc).isoformat(), "noticias": out},
        ensure_ascii=False, separators=(",", ":")), encoding="utf8")
    print(len(out), "titulares;", sum(1 for x in out if x["a"] == "local"), "locales;", sum(1 for x in out if x["mun"]), "con municipio;", sum(1 for x in out if x["r"]), "de riesgo")
main()
