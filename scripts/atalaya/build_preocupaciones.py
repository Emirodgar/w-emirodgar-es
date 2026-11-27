#!/usr/bin/env python3
"""Atalaya: serie histórica de preocupaciones ciudadanas (barómetros mensuales del CIS desde 2010).

Fuente: cis.es, PDF «Resultados» de cada barómetro. Dos preguntas: «principal problema que existe actualmente en España» (nacional) y
«problema que a Ud., personalmente, le afecta más» (personal; las «quejas» de cada hogar). Guarda, por barómetro, el % de menciones
(`total`: hasta tres respuestas; `primero`: solo el primer problema cuando el PDF lo da) en atalaya/data/preocupaciones.json.
Dos formatos de PDF: el moderno (desde 2014, tablas con cuatro columnas, lo lee build_cis.preguntas) y el antiguo (2010-2013,
una tabla por pregunta con «etiqueta % (N)»). Idempotente y reanudable: no vuelve a leer un barómetro ya guardado y nunca borra.
Los hitos y las acciones de gobierno van a mano en atalaya/data/hitos.json.
Requiere pdftotext. Uso (raíz del repo): python3 scripts/atalaya/build_preocupaciones.py [--desde 2010] [--hasta 2026]
"""
import argparse, json, re, sys, time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_cis as C          # noqa: E402
from manifest import marcar    # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
SALIDA = RAIZ / "atalaya/data/preocupaciones.json"
PREFIJO = re.compile(r"^(?:Primer problema|Segundo problema|Tercer problema|TOTAL|\s)+", re.I)
FILA_ANTIGUA = re.compile(r"^(.*?)\s*(\d+[.,]\d+)\s+\((\d[\d.]*)\)$")
FILA4 = re.compile(r"^(.*?)\s*((?:\d+\.\d+|\.)\s+(?:\d+\.\d+|\.)\s+(?:\d+\.\d+|\.)\s+\d+\.\d+)$")   # 2013: cuatro columnas, «.» = 0


def limpia(e):
    e = re.sub(r"^.*\?\s+", "", e)                                    # la pregunta pegada a la 1.ª etiqueta
    e = re.sub(r"^.*(?:\)\.|TOTAL|Total)\s+", "", e)                       # restos de la cabecera de la pregunta pegados a la 1.ª etiqueta
    e = re.sub(r"^.*\d,\d(?:\s+(?:\d+,\d|-))*\s+(?=[A-ZÁÉÍÓÚ])", "", e)           # cifras de una fila con guiones, que no se leyó
    return re.sub(r"\s+", " ", PREFIJO.sub("", e)).strip()


def bloques_antiguos(t):
    """Formato 2010-2013: «PREGUNTA 7» / «PREGUNTA 7a» + filas «etiqueta % (N)» hasta TOTAL; la etiqueta puede ocupar varias líneas."""
    partes = re.split(r"\nPREGUNTA (\d+a?)\n", "\n" + t)
    out = []
    for i in range(1, len(partes) - 1, 2):
        cuerpo, filas, buf = partes[i + 1], {}, ""
        cab = re.sub(r"\s+", " ", cuerpo[:300])
        for l in cuerpo.splitlines():
            l = l.strip()
            if not l or l.startswith(("___", "CIS", "Estudio n", "%", ".")) or re.fullmatch(r"\d+", l): continue
            m = FILA_ANTIGUA.match(l) or FILA4.match(l)
            if m:
                et = limpia(buf + " " + m.group(1)); buf = ""
                if et.upper() == "TOTAL": break
                v = [0.0 if x == "." else float(x.replace(",", ".")) for x in m.group(2).split()]
                if et: filas[et] = v
            elif not l.startswith("¿") and "MULTIRRESPUESTA" not in l and not cab.startswith(l): buf = (buf + " " + l).strip()
        out.append((partes[i], cab, filas))
    return out


def parsea_antiguo(t):
    r = {}
    for num, cab, filas in bloques_antiguos(t):
        if not filas: continue
        cuatro = {e: v for e, v in filas.items() if len(v) == 4}
        if cuatro and not num.endswith("a"):               # tabla de cuatro columnas: primero = 1.ª, total = última
            tot, pri = {e: v[3] for e, v in cuatro.items()}, {e: v[0] for e, v in cuatro.items()}
        else: tot = pri = {e: v[0] for e, v in filas.items()}
        nac = "principal problema que existe actualmente en espa" in cab.lower()
        per = "personalmente" in cab and "afecta" in cab
        k = "nacional" if nac else "personal" if per else None
        if not k: continue
        if num.endswith("a"):
            if k + "_primero" not in r: r[k + "_primero"] = tot
        elif k + "_total" not in r:
            r[k + "_total"] = tot
            if cuatro: r[k + "_primero"] = pri
    return r


def parsea_moderno(t):
    r = {}
    for _, b in C.bloques(t):
        cab = re.sub(r"\s+", " ", b[:400])
        nac = "principal problema que existe actualmente en España" in cab
        per = "personalmente, le afecta" in cab
        if (nac and "nacional_total" not in r) or (per and "personal_total" not in r):
            k = "nacional" if nac else "personal"
            f = C.filas_tabla(b, 4)
            if not f: continue
            r[k + "_total"] = {limpia(e): v[3] for e, v in f}
            r[k + "_primero"] = {limpia(e): v[0] for e, v in f}
    return r


def valido(b):
    """Algunos PDF (p. ej. mayo de 2023) maquetan las columnas por bloques y no se pueden leer: se descartan en vez de guardar basura."""
    n = b.get("nacional_total") or {}
    return "El paro" in n and len(n) >= 25 and max(n.values()) <= 100


def procesar(meta, mes, anio):
    t = C.texto_pdf(meta["res"]) if meta.get("res") else None
    time.sleep(0.6)
    if not t: return None
    r = parsea_moderno(t) or {}
    if "nacional_total" not in r: r = {**parsea_antiguo(t), **r}
    if "nacional_total" not in r or not valido(r): return None
    return {"fecha": f"{anio}-{C.MESES.index(mes) + 1:02d}", "estudio": meta["estudio"], "url": meta["url"], **r}


def main():
    ap = argparse.ArgumentParser(); hoy = datetime.now(timezone.utc)
    ap.add_argument("--desde", type=int, default=2010); ap.add_argument("--hasta", type=int, default=hoy.year); a = ap.parse_args()
    prev = json.loads(SALIDA.read_text(encoding="utf8")).get("barometros", []) if SALIDA.exists() else []
    for b in prev:                                      # normaliza etiquetas guardadas con versiones anteriores de limpia()
        for k in [k for k in b if k.endswith(("_total", "_primero"))]: b[k] = {limpia(e): v for e, v in b[k].items()}
    sin = [b["fecha"] for b in prev if not valido(b)]          # lecturas ilegibles de versiones anteriores: se descartan y se reintentan
    por = {b["fecha"]: b for b in prev if valido(b)}
    for anio in range(a.desde, a.hasta + 1):
        for i, mes in enumerate(C.MESES, 1):
            if anio == hoy.year and i > hoy.month: break
            f = f"{anio}-{i:02d}"
            if f in por: continue
            meta = C.pagina_estudio(mes, anio)
            if not meta: continue                       # meses sin barómetro (agosto)
            b = procesar(meta, mes, anio)
            if not b: sin.append(f); print("sin tabla legible", f); continue
            por[f] = b
            print(f, len(b["nacional_total"]), "problemas", "· personal" if "personal_total" in b else "")
            SALIDA.write_text(json.dumps({"barometros": [por[k] for k in sorted(por)]}, ensure_ascii=False, separators=(",", ":")), encoding="utf8")   # reanudable
    lista = [por[k] for k in sorted(por)]
    SALIDA.write_text(json.dumps({"actualizado": hoy.replace(microsecond=0).isoformat(), "fuente": "Centro de Investigaciones Sociológicas (cis.es), barómetros mensuales",
        "aviso": "Respuesta espontánea y multirrespuesta (hasta tres problemas): las columnas no suman 100. La redacción de las categorías cambia con los años; la página las agrupa en temas comparables.",
        "sin_leer": sorted(set(sin)), "barometros": lista}, ensure_ascii=False, separators=(",", ":")), encoding="utf8")
    marcar("preocupaciones")
    print(len(lista), "barómetros guardados; sin leer:", sin)


if __name__ == "__main__":
    main()
