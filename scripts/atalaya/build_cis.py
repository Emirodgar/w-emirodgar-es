#!/usr/bin/env python3
"""Atalaya: barómetros del CIS (estimación de voto, indecisión, problemas principales, líder preferido y confianza en los líderes).

Fuente: cis.es, documentos públicos de cada barómetro (PDF «Resultados» y PDF «Estimación de voto»); no usa microdatos ni registro.
Para cada barómetro mensual del año lee la página del estudio (o, si aún solo hay avance de resultados, los PDF del avance), extrae las
tablas con pdftotext y guarda solo el resultado en atalaya/data/cis.json. Es idempotente: no vuelve a leer un barómetro ya guardado,
salvo que solo estuviera en avance y ya exista la página del estudio. Nunca borra barómetros.
Las preguntas se localizan por su texto, no por su número, porque la numeración cambia de un mes a otro.
La «estimación de voto» es la del CIS (modelo de escenarios), no una predicción nuestra ni equivale a la media de encuestas.
Requiere pdftotext (poppler). Uso (raíz del repo): python3 scripts/atalaya/build_cis.py [--anio 2026]
"""
import argparse, json, re, subprocess, sys, tempfile, time
from datetime import datetime, timezone
from html import unescape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from manifest import marcar   # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
SALIDA = RAIZ / "atalaya/data/cis.json"
UA = "Mozilla/5.0 (compatible; EmirodgarBot/1.0; +https://emirodgar.es/atalaya)"
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
BASE = "https://www.cis.es"
N = r"(\d+(?:,\d+)?)"


def curl(url, binario=False):
    r = subprocess.run(["curl", "-s", "-L", "-m", "90", "-A", UA, "-H", "Accept-Language: es-ES,es;q=0.9", "-w", "\n%{http_code}", url], capture_output=True)
    cuerpo, _, code = r.stdout.rpartition(b"\n")
    return int(code or 0), (cuerpo if binario else cuerpo.decode("utf8", "replace"))


def texto_pdf(url):
    code, data = curl(url, True)
    if code != 200 or not data.startswith(b"%PDF"): return None
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "d.pdf"; p.write_bytes(data)
        r = subprocess.run(["pdftotext", "-raw", "-enc", "UTF-8", str(p), "-"], capture_output=True)
        if r.returncode != 0: return None
        try: s = r.stdout.decode("utf8")
        except UnicodeDecodeError: s = r.stdout.decode("cp1252", "replace")   # pdftotext de Windows ignora -enc UTF-8
        return s.replace(chr(13) + chr(10), chr(10))


def num(s): return float(s.replace(",", "."))


def fecha(s):
    m = re.search(r"(\d{2})/(\d{2})/(\d{4})", s or "")
    return f"{m.group(3)}-{m.group(2)}-{m.group(1)}" if m else None


# ---------- localizar documentos ----------
def pagina_estudio(mes, anio):
    code, t = curl(f"{BASE}/es/estudios/barometro-de-{mes}-{anio}")
    if code != 200: return None
    cod = re.search(r"C[oó]digo\s*(\d{4})", re.sub(r"<[^>]+>", " ", t))
    if not cod: return None
    plano = re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", t)))
    docs = {x: unescape(h) for h, x in re.findall(r'href="(https://www\.cis\.es/documents/[^"]+)"[^>]*>\s*([^<]{3,60}?)\s*<', t)}
    res = next((h for x, h in docs.items() if x.startswith("Resultados PDF")), None)
    est = next((h for x, h in docs.items() if x.startswith("Estimaci")), None)
    return {"estudio": int(cod.group(1)), "url": f"{BASE}/es/estudios/barometro-de-{mes}-{anio}", "res": res, "est": est, "fuente": "estudio",
            "fecha_estudio": fecha((re.search(r"Fecha de estudio\s*(\S+)", plano) or [None, None])[1]),
            "fecha_avance": fecha((re.search(r"Fecha de avance\s*(\S+)", plano) or [None, None])[1]),
            "fecha_publicacion": fecha((re.search(r"Fecha de publicaci[oó]n\s*(\S+)", plano) or [None, None])[1])}


def avances():
    """Barómetros que solo tienen avance de resultados: enlaces desde la portada del CIS."""
    code, t = curl(f"{BASE}/es/")
    out = {}
    for h, n, mes, anio in re.findall(r'href="(https://www\.cis\.es/es/w/avance-de-resultados-del-estudio-(\d+)-bar%C3%B3metro-de-([a-z]+)-(\d{4})[^"]*)"', t):
        out[(mes, int(anio))] = {"estudio": int(n), "url": h, "res": f"{BASE}/documents/d/guest/es{n}mar_a-pdf", "est": f"{BASE}/documents/d/guest/{n}_estimacion-pdf",
                                 "fuente": "avance", "fecha_estudio": None, "fecha_avance": None, "fecha_publicacion": None}
    return out


# ---------- interpretar los PDF ----------
def estimacion(t):
    filas, otros, n = [], {}, None
    for l in t.splitlines():
        l = l.strip()
        m = re.match(rf"^(.+?)\s+{N}\s+±{N}\s+{N}(?:\s+{N}\s*[-–—]\s*{N})?$", l)
        if m and not re.match(r"^(En blanco|Voto Nulo|Abstenci)", m.group(1)):
            filas.append({"partido": m.group(1).replace("*", "").strip(), "directo": num(m.group(2)), "margen": num(m.group(3)), "estimacion": num(m.group(4)),
                          "intervalo": [num(m.group(5)), num(m.group(6))] if m.group(5) else None}); continue
        m = re.match(rf"^(En blanco|Voto Nulo|Abstenci[oó]n.*?|No sabe|No contesta)\s+{N}\s+±{N}", l)
        if m: otros[m.group(1).split(" (")[0].lower().replace("ó", "o").replace(" ", "_")] = num(m.group(2))
        m = re.match(r"^\(N\)\s+\(([\d.]+)\)$", l)
        if m and n is None: n = int(m.group(1).replace(".", ""))
    return filas, otros, n


def bloques(t):
    partes = re.split(r"[\n\x0c]Pregunta (\S+)\n", "\n" + t)   # el salto de página (\x0c) puede preceder a «Pregunta»
    return [(partes[i], partes[i + 1]) for i in range(1, len(partes) - 1, 2)]


def filas_tabla(b, cols):
    """Líneas «etiqueta n n …» con `cols` números al final; la etiqueta puede ocupar varias líneas."""
    rx = re.compile(rf"^(.*?)\s*((?:{N}\s+){{{cols - 1}}}{N})$")
    out, buf = [], ""
    for l in b.splitlines()[1:]:
        l = l.strip()
        if not l or l.startswith(("Estudio n", "Pág", "(RESPUESTA", "(MULTI", "(RECOD", "(SOBRE")) or l in ("Primer", "problema", "Segundo", "Tercer", "TOTAL"): continue
        if l.startswith("(N)") or l.startswith("Media") or l.startswith("Desviaci"): break
        m = rx.match(l)
        if m:
            etiqueta = (buf + " " + m.group(1)).strip(); buf = ""
            vals = [num(x) for x in m.group(2).split()]
            if etiqueta: out.append((etiqueta, vals))
        else: buf = (buf + " " + l).strip()
    return out


def preguntas(t):
    r = {}
    for _, b in bloques(t):
        cab = re.sub(r"\s+", " ", b[:400])
        if "principal problema que existe actualmente en España" in cab and "problemas" not in r:
            r["problemas"] = [{"problema": e, "primero": v[0], "segundo": v[1], "tercero": v[2], "total": v[3]} for e, v in filas_tabla(b, 4)]
        elif "quién preferiría que fuese el/la presidente/a" in cab and "presidente_preferido" not in r:
            r["presidente_preferido"] = [{"nombre": e, "pct": v[0]} for e, v in filas_tabla(b, 1)]
        elif "probabilidad de que Ud. vaya a votar" in cab and "prob_voto" not in r:
            f = filas_tabla(b, 1); d = {e.split(" ")[0]: v[0] for e, v in f if re.match(r"^\d", e)}
            m = re.search(r"Media\s+(\d+,\d+)", b)
            r["prob_voto"] = {"pct_10": d.get("10"), "pct_0_a_4": round(sum(d.get(str(i), 0) for i in range(5)), 1), "media": num(m.group(1)) if m else None}
        elif "votan siempre por el mismo partido" in cab and "fidelidad" not in r:
            r["fidelidad"] = [{"respuesta": e.split("? ")[-1], "pct": v[0]} for e, v in filas_tabla(b, 1)]   # la pregunta se pega a la 1.ª etiqueta
        elif "Cuándo suele Ud. decidir" in cab and "cuando_decide" not in r:
            r["cuando_decide"] = [{"respuesta": e, "pct": v[0]} for e, v in filas_tabla(b, 1)]
        elif "le inspira" in cab and "confianza" in cab:
            quien = "sanchez" if "Sánchez" in cab else "feijoo" if "Feijóo" in cab else None
            if quien:
                canon = lambda e: (re.search(r"(?:Mucha|Bastante|Poca|Ninguna) confianza$|N\.S\.$|N\.C\.$", e) or [e])[0]   # la pregunta ocupa varias líneas y se pega a la 1.ª etiqueta
                r.setdefault("confianza", {})[quien] = {canon(e): v[0] for e, v in filas_tabla(b, 1)}
    return r


def procesar(meta, mes, anio):
    tr, te = texto_pdf(meta["res"]) if meta.get("res") else None, texto_pdf(meta["est"]) if meta.get("est") else None
    time.sleep(1)
    if not tr and not te: return None
    filas, otros, n = estimacion(te) if te else ([], {}, None)
    q = preguntas(tr) if tr else {}
    return {"estudio": meta["estudio"], "mes": f"{mes} {anio}", "anio": anio, "mes_n": MESES.index(mes) + 1, "n": n, "fuente": meta["fuente"], "url": meta["url"],
            "fecha_estudio": meta["fecha_estudio"], "fecha_avance": meta["fecha_avance"], "fecha_publicacion": meta["fecha_publicacion"],
            "estimacion": filas, "voto_directo_otros": otros, **q}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--anio", type=int, default=datetime.now(timezone.utc).year); a = ap.parse_args()
    prev = json.loads(SALIDA.read_text(encoding="utf8"))["barometros"] if SALIDA.exists() else []
    por = {(b["anio"], b["mes_n"]): b for b in prev}
    av = avances(); hoy = datetime.now(timezone.utc)
    for i, mes in enumerate(MESES, 1):
        if a.anio == hoy.year and i > hoy.month: break
        ya = por.get((a.anio, i))
        if ya and ya["fuente"] == "estudio" and ya.get("estimacion"): continue
        meta = pagina_estudio(mes, a.anio) or av.get((mes, a.anio))
        if not meta: print("sin datos", mes); continue
        if ya and ya["fuente"] == "avance" and meta["fuente"] == "avance" and ya.get("estimacion"): continue
        b = procesar(meta, mes, a.anio)
        if not b: print("sin documentos legibles", mes); continue
        por[(a.anio, i)] = b
        print(f"{mes} {a.anio} (estudio {b['estudio']}, {b['fuente']}): {len(b['estimacion'])} partidos, N={b['n']}, {len(b.get('problemas', []))} problemas")
    lista = [por[k] for k in sorted(por)]
    SALIDA.write_text(json.dumps({"actualizado": hoy.replace(microsecond=0).isoformat(), "fuente": "Centro de Investigaciones Sociológicas (cis.es)",
        "aviso": "La estimación de voto es la del CIS (modelo de escenarios), no una predicción propia ni la media de encuestas. «Voto directo» es sobre el censo; «estimación», sobre el voto válido. Los problemas son respuesta espontánea y multirrespuesta (hasta tres).",
        "barometros": lista}, ensure_ascii=False, separators=(",", ":")), encoding="utf8")
    marcar("cis")
    print(len(lista), "barómetros guardados")


if __name__ == "__main__":
    main()
