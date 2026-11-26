#!/usr/bin/env python3
"""Atalaya: canales públicos de Telegram de los partidos (ritmo, formatos y visualizaciones).

Lee la vista web pública t.me/s/<canal> de los canales con lectura «automatica» del catálogo
atalaya/data/canales_mensajeria.json (los que enlaza la web oficial del partido o se han confirmado). No usa cuenta ni clave.
WhatsApp no tiene API ni RSS públicos: sus canales solo están en el catálogo (seguimiento manual).

Principio del proyecto: nunca se borra nada. Cada mensaje se archiva una vez, con su fecha de primera captura:
  atalaya/data/archivo/mensajeria/AAAA-MM-DD.jsonl.gz   mensajes vistos por primera vez ese día (texto recortado a 600 caracteres,
                                                        visualizaciones en el momento de la primera captura)
Salida viva:
  atalaya/data/mensajeria.json   por canal: seguidores (con su historial), mensajes por día, formatos, visualizaciones y últimos mensajes

Cortesía: una petición cada 2 s, identificada, pocas páginas por canal y parada ante cualquier 429/403.
Uso (raíz del repo): python3 scripts/atalaya/build_mensajeria.py [--paginas N] [--canal handle]
"""
import argparse, html, json, re, statistics, sys, time, urllib.error, urllib.request
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import archivo                       # noqa: E402  (helpers del archivo inmutable)
from manifest import marcar         # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
D = RAIZ / "atalaya/data"
CATALOGO = D / "canales_mensajeria.json"
SALIDA = D / "mensajeria.json"
CARP = D / "archivo" / "mensajeria"
UA = "Mozilla/5.0 (compatible; EmirodgarBot/1.0; +https://emirodgar.es/atalaya)"
PAUSA = 2.0
VENTANA_DIAS = 30


def pedir(handle, antes=None):
    url = f"https://t.me/s/{handle}" + (f"?before={antes}" if antes else "")
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "es"})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.read().decode("utf8", "replace")
    except urllib.error.HTTPError as e:
        if e.code in (403, 429): raise SystemExit(f"Telegram responde {e.code}: se detiene para no insistir")
        raise


def num(s):
    s = (s or "").strip().replace(",", ".")
    m = re.match(r"^([\d.]+)([KM]?)$", s)
    if not m: return None
    v = float(m.group(1)); return int(v * {"": 1, "K": 1e3, "M": 1e6}[m.group(2)])


def limpiar(t):
    t = re.sub(r"<br\s*/?>", " ", t); t = re.sub(r"<[^>]+>", "", t)
    return re.sub(r"\s+", " ", html.unescape(t)).strip()


def formato(bloque):
    f = []
    if "tgme_widget_message_photo_wrap" in bloque: f.append("imagen")
    if "tgme_widget_message_video_player" in bloque or "tgme_widget_message_roundvideo" in bloque: f.append("vídeo")
    if "tgme_widget_message_voice" in bloque: f.append("audio")
    if "tgme_widget_message_poll" in bloque: f.append("encuesta")
    if "tgme_widget_message_document" in bloque: f.append("documento")
    if "tgme_widget_message_link_preview" in bloque: f.append("enlace")
    return f or ["texto"]


def mensajes(pagina, handle):
    """Mensajes de una página de t.me/s: id, fecha, texto, formato, visualizaciones, reenviado."""
    out = []
    for b in re.split(r'<div class="tgme_widget_message_wrap', pagina)[1:]:
        p = re.search(r'data-post="([^"]+)"', b); d = re.search(r'<time datetime="([^"]+)"', b)
        if not p or not d: continue
        tx = re.search(r'<div class="tgme_widget_message_text[^"]*"[^>]*>(.*?)</div>', b, re.S)
        v = re.search(r'tgme_widget_message_views">([^<]+)<', b)
        out.append({"i": p.group(1), "n": int(p.group(1).split("/")[-1]), "f": d.group(1), "t": limpiar(tx.group(1))[:600] if tx else "",
                    "fmt": formato(b), "v": num(v.group(1)) if v else None, "fw": "tgme_widget_message_forwarded_from" in b})
    return out


def cabecera(pagina):
    og = re.search(r'<meta property="og:title" content="([^"]*)"', pagina)
    s = re.search(r'counter_value">([^<]+)</span> <span class="counter_type">subscribers', pagina)
    return (html.unescape(og.group(1)) if og else None), (num(s.group(1)) if s else None)


def leer_canal(handle, max_paginas, vistos):
    """Recorre hacia atrás hasta toparse con un mensaje ya archivado o agotar las páginas."""
    nuevos, titulo, subs, antes = [], None, None, None
    for k in range(max_paginas):
        pg = pedir(handle, antes)
        if k == 0: titulo, subs = cabecera(pg)
        ms = mensajes(pg, handle)
        if not ms: break
        nuevos += [m for m in ms if m["i"] not in vistos]
        if any(m["i"] in vistos for m in ms): break          # ya alcanzamos lo archivado
        antes = min(m["n"] for m in ms)
        time.sleep(PAUSA)
    return titulo, subs, nuevos


def archivados():
    todos = {}
    if CARP.exists():
        for f in sorted(CARP.glob("*.jsonl.gz")):
            for r in archivo.leer_lineas(f): todos[r["i"]] = r
    return todos


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--paginas", type=int, default=None); ap.add_argument("--canal")
    a = ap.parse_args()
    cat = json.loads(CATALOGO.read_text(encoding="utf8"))
    canales = [c for c in cat["canales"] if c["plataforma"] == "telegram" and c.get("lectura") == "automatica" and (not a.canal or c["handle"] == a.canal)]
    arch = archivados(); vistos = set(arch)
    previo = json.loads(SALIDA.read_text(encoding="utf8")) if SALIDA.exists() else {"canales": []}
    hist_prev = {c["handle"]: c.get("historial_seguidores", []) for c in previo["canales"]}
    ahora = datetime.now(timezone.utc); hoy = ahora.strftime("%Y-%m-%d")
    nuevos_total = []; info = {}
    for c in canales:
        h = c["handle"]
        primera = not any(k.lower().startswith(h.lower() + "/") for k in vistos)   # Telegram devuelve el id con su mayúscula canónica
        titulo, subs, nuevos = leer_canal(h, a.paginas or (8 if primera else 3), vistos)
        for m in nuevos: m["cap"] = hoy
        nuevos_total += nuevos; info[h] = (titulo, subs)
        print(f"{c['partido']:9s} @{h}: {len(nuevos)} nuevos, {subs} seguidores")
        time.sleep(PAUSA)
    # archivo inmutable: solo se añade
    if nuevos_total:
        fila = lambda m: {"i": m["i"], "f": m["f"], "t": m["t"], "fmt": m["fmt"], "v": m["v"], "fw": m["fw"], "cap": m["cap"]}
        archivo.anadir_al_dia(CARP, [fila(m) for m in nuevos_total])
    arch = archivados()
    salida = []
    corte = (ahora - timedelta(days=VENTANA_DIAS)).strftime("%Y-%m-%dT")
    for c in cat["canales"]:
        if c["plataforma"] != "telegram" or c.get("lectura") != "automatica": continue
        h = c["handle"]; ms = sorted((r for r in arch.values() if r["i"].lower().startswith(h.lower() + "/")), key=lambda r: r["f"])
        titulo, subs = info.get(h, (None, None))
        hist = hist_prev.get(h, [])
        if subs and not any(x["f"] == hoy for x in hist): hist = hist + [{"f": hoy, "n": subs}]
        rec = [m for m in ms if m["f"] >= corte]
        pd = Counter(m["f"][:10] for m in rec)
        dias = max(1, (ahora.date() - datetime.fromisoformat(rec[0]["f"]).date()).days + 1) if rec else 1
        dias = min(dias, VENTANA_DIAS)
        vs = [m["v"] for m in rec if m["v"]]
        fm = Counter(f for m in rec for f in m["fmt"])
        salida.append({"partido": c["partido"], "handle": h, "url": c["url"], "nombre": titulo or c.get("nombre"), "origen": c["origen"],
                       "seguidores": subs or (hist[-1]["n"] if hist else c.get("seguidores")), "historial_seguidores": hist,
                       "mensajes_archivados": len(ms), "primero": ms[0]["f"][:10] if ms else None, "ultimo": ms[-1]["f"][:10] if ms else None,
                       "ventana": {"dias": dias, "mensajes": len(rec), "por_dia": round(len(rec) / dias, 1), "vistas_total": sum(vs),
                                   "vistas_mediana": int(statistics.median(vs)) if vs else None,
                                   "vistas_por_seguidor": round(statistics.median(vs) / (subs or c.get("seguidores") or 1), 2) if vs else None,
                                   "formatos": dict(fm.most_common()), "reenviados": sum(1 for m in rec if m["fw"]),
                                   "serie": [{"f": d, "n": pd[d]} for d in sorted(pd)]},
                       "ultimos": [{"f": m["f"], "t": m["t"][:220], "u": "https://t.me/" + m["i"], "v": m["v"], "fmt": m["fmt"]} for m in ms[-5:][::-1]]})
    SALIDA.write_text(json.dumps({"actualizado": ahora.replace(microsecond=0).isoformat(), "ventana_dias": VENTANA_DIAS,
        "aviso": "Solo canales públicos de Telegram enlazados por la web de cada partido (o confirmados). Las visualizaciones son las de la primera captura de cada mensaje; los mensajes recientes pueden estar infravalorados. No es una medida de apoyo ni de alcance total. Los partidos sin canal confirmado no aparecen.",
        "canales": salida}, ensure_ascii=False, indent=1), encoding="utf8")
    marcar("mensajeria")
    print(len(nuevos_total), "mensajes nuevos;", len(arch), "archivados en total")


if __name__ == "__main__":
    main()
