#!/usr/bin/env python3
"""Genera radar-porsche/index.html (HTML estático, sin JS para los datos).

Lee las copias de los datos de mejorimposible.es en radar-porsche/data/ y escribe
las tablas, los gráficos (CSS/SVG), el JSON-LD (Dataset + FAQPage) ya renderizados,
para que rastreadores que no ejecutan JavaScript vean todo el contenido.

Cabecera, pie y estilos de la web se toman de ibex35/index.html para no duplicarlos.
Solo librería estándar.   Uso:  python scripts/radar_porsche/build.py
"""
import html, json, os, re
from urllib.parse import urlparse

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATA = os.path.join(ROOT, "radar-porsche", "data")
OUT = os.path.join(ROOT, "radar-porsche", "index.html")
URL = "https://emirodgar.es/radar-porsche/"
FUENTE = "https://mejorimposible.es/porsche/"

MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
         "septiembre", "octubre", "noviembre", "diciembre"]

# Etiquetas de las series de precios (ids de scripts/actualizar-precios-anuncios/series.json de mejorimposible)
SERIES = {
    "911-g": ("911", "911 G / 930 (1974-89)"), "911-964": ("911", "911 964 (1989-94)"),
    "993": ("911", "911 993 (1994-98)"), "911-996": ("911", "911 996 (1998-2005)"),
    "911-997-1": ("911", "911 997.1 (2005-08)"), "911-997-2": ("911", "911 997.2 (2009-12)"),
    "911-991": ("911", "911 991.1 (2012-15)"), "911-991-2": ("911", "911 991.2 (2016-19)"),
    "911-992": ("911", "911 992 (2019-26)"),
    "boxster-986": ("718", "Boxster 986 (1996-2004)"), "boxster-987-1": ("718", "Boxster 987.1 (2005-08)"),
    "boxster-987-2": ("718", "Boxster 987.2 (2009-12)"), "boxster-981": ("718", "Boxster 981 (2012-16)"),
    "boxster-718": ("718", "718 Boxster (2017-26)"),
    "cayman-987-1": ("718", "Cayman 987.1 (2005-08)"), "cayman-987-2": ("718", "Cayman 987.2 (2009-12)"),
    "cayman-981": ("718", "Cayman 981 (2013-16)"), "cayman-718": ("718", "718 Cayman (2016-26)"),
    "cayenne-955": ("Cayenne", "Cayenne 955/957 (2003-10)"), "cayenne-958": ("Cayenne", "Cayenne 958 (2010-17)"),
    "cayenne-e3": ("Cayenne", "Cayenne E3 (2018-22)"), "cayenne-e3-2": ("Cayenne", "Cayenne E3.2 (2023-26)"),
    "macan-95b": ("Macan", "Macan 95B (2014-18)"), "macan-restyling": ("Macan", "Macan restyling (2019-23)"),
    "macan-ev": ("Macan", "Macan eléctrico (2024-26)"),
    "panamera-970": ("Panamera", "Panamera 970 (2010-16)"), "panamera-971": ("Panamera", "Panamera 971 (2017-23)"),
    "taycan-j1": ("Taycan", "Taycan (2020-26)"),
}
FAMILIAS = ["911", "718", "Cayenne", "Macan", "Panamera", "Taycan"]
CONF = {"alta": "Alta", "media": "Media", "baja": "Baja", "insuficiente": "Insuficiente"}


def load(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return json.load(f)


def e(s):
    return html.escape(str(s), quote=True)


def num(n, dec=0):
    s = f"{n:,.{dec}f}"
    return s.replace(",", "§").replace(".", ",").replace("§", ".")


def eur(n):
    return num(n) + " €"


def fecha(iso):
    y, m, d = iso[:10].split("-")
    return f"{int(d)} de {MESES[int(m) - 1]} de {y}"


def mes_txt(ym):
    y, m = ym.split("-")
    return f"{MESES[int(m) - 1]} de {y}"


# ---------------------------------------------------------------- datos
def preparar():
    an = load("analisis-reddit.json")
    pr = load("precios-anuncios.json")
    nt = load("noticias-historico.json")
    mn = load("menciones-historico.json")
    sm = load("tendencias-semanas.json")

    fams = {f["id"]: f for f in an["families"]}
    modelos = sorted([m for m in an["models"]], key=lambda m: -m["rank_score"])

    precios = []
    for sid, serie in pr["series"].items():
        if sid not in SERIES or not serie:
            continue
        ult = serie[-1]
        ant = serie[-2] if len(serie) > 1 else None
        var = None
        if ant and ant["n"] >= 5 and ult["n"] >= 5 and ant["precio"]:
            var = (ult["precio"] / ant["precio"] - 1) * 100
        precios.append({"id": sid, "familia": SERIES[sid][0], "label": SERIES[sid][1], "ult": ult, "var": var})
    noticias = sorted(nt, key=lambda x: x.get("published", ""), reverse=True)[:10]
    menciones = sorted(mn, key=lambda x: x.get("date", ""), reverse=True)[:6]
    sem_id = sorted(sm.keys())[-1]
    return an, pr, fams, modelos, precios, noticias, menciones, sem_id, sm[sem_id]


# ---------------------------------------------------------------- FAQ
def faqs(an, fams, modelos, precios, pr):
    st = an["stats"]
    ranking = sorted(fams.values(), key=lambda f: -f["rank_score"])
    top, last = ranking[0], ranking[-1]
    aspect = an["aspects_es"]

    def mejor_aspecto(f, clave):
        lst = f.get(clave) or []
        return aspect[lst[0]["aspect"]].lower() if lst else "—"

    sufic = [m for m in modelos if m["confidence"] in ("alta", "media")]
    mejor_modelo = sufic[0]
    peor_modelo = sorted(sufic, key=lambda m: m["wilson"])[0]
    med = [p for p in precios if p["ult"]["n"] >= 5]
    barato = min(med, key=lambda p: p["ult"]["precio"])
    caro = max(med, key=lambda p: p["ult"]["precio"])
    mes = mes_txt(pr["series"]["911-992"][-1]["mes"])

    return [
        ("¿Qué familia de Porsche tiene mejor valoración entre sus propietarios?",
         f"Según los comentarios de propietarios y conductores en Reddit analizados hasta el {fecha(an['generated'])}, "
         f"la familia mejor valorada es {top['label']}: {top['pct_positive']} % de opiniones positivas y puntuación Wilson de "
         f"{num(top['wilson'], 2)} sobre {top['users']} usuarios. La peor valorada es {last['label']} "
         f"({last['pct_positive']} % positivas sobre {last['users']} usuarios)."),
        ("¿Cuántas opiniones respaldan este análisis?",
         f"{num(st['users_counted'])} usuarios distintos, {num(st['comments_counted'])} comentarios contados y "
         f"{st['threads']} hilos de Reddit entre el {fecha(st['period_from'])} y el {fecha(st['period_to'])}. "
         "Cuenta un voto por usuario y modelo, y solo opiniones de quien tiene o ha tenido el coche, o lo ha conducido."),
        ("¿Qué generación de Porsche es la mejor valorada y cuál la peor?",
         f"Entre los modelos con muestra suficiente, el mejor valorado es {mejor_modelo['label']} "
         f"({mejor_modelo['pct_positive']} % positivas, {mejor_modelo['users']} usuarios) y el peor, {peor_modelo['label']} "
         f"({peor_modelo['pct_positive']} % positivas, {peor_modelo['users']} usuarios)."),
        ("¿Qué es lo que más gusta y lo que más molesta a los propietarios de un " + top["label"] + "?",
         f"En {top['label']}, el aspecto más elogiado es {mejor_aspecto(top, 'pros')} y la queja más repetida es "
         f"{mejor_aspecto(top, 'cons')}."),
        ("¿Cuánto cuesta un Porsche de segunda mano en España?",
         f"En los anuncios de AutoScout24.es de {mes}, la mediana más baja entre las series con al menos 5 anuncios corresponde a "
         f"{barato['label']} ({eur(barato['ult']['precio'])}) y la más alta a {caro['label']} ({eur(caro['ult']['precio'])}). "
         "Son precios de anuncio, no de venta."),
        ("¿Cada cuánto se actualizan los datos?",
         "Las noticias se actualizan varias veces al día, los precios de anuncios una vez al mes y el análisis de opiniones "
         "cuando se añaden nuevos hilos. Cada bloque muestra su fecha de actualización."),
        ("¿De dónde salen los datos?",
         "Opiniones: archivo público de Reddit (Arctic Shift), clasificadas con un modelo de IA y puntuadas por un script. "
         "Precios: anuncios de coches usados de AutoScout24.es. Noticias: feeds RSS de prensa. "
         f"La metodología completa está en {FUENTE}analisis."),
    ]


# ---------------------------------------------------------------- bloques HTML
def bloque_kpis(an, pr):
    st = an["stats"]
    items = [
        (num(st["users_counted"]), "usuarios contados"),
        (num(st["comments_counted"]), "comentarios válidos"),
        (str(st["threads"]), "hilos de Reddit"),
        (f"{mes_txt(st['period_from'][:7])} – {mes_txt(st['period_to'][:7])}", "periodo analizado"),
    ]
    return "".join(f'<div class="rp-kpi"><b>{e(v)}</b><span>{e(k)}</span></div>' for v, k in items)


def barra(f):
    tot = f["pos"] + f["neu"] + f["neg"] or 1
    p, n, g = (f["pos"] / tot * 100, f["neu"] / tot * 100, f["neg"] / tot * 100)
    return (f'<div class="rp-bar" role="img" aria-label="{num(p)} % positivas, {num(n)} % neutras, {num(g)} % negativas">'
            f'<i class="pos" style="width:{p:.1f}%"></i><i class="neu" style="width:{n:.1f}%"></i>'
            f'<i class="neg" style="width:{g:.1f}%"></i></div>')


def bloque_familias(fams, an):
    rows = []
    for i, f in enumerate(sorted(fams.values(), key=lambda f: -f["rank_score"]), 1):
        rows.append(
            f'<tr><td>{i}</td><th scope="row">{e(f["label"])}</th><td class="num">{f["users"]}</td>'
            f'<td class="bar">{barra(f)}</td><td class="num"><b>{f["pct_positive"]} %</b></td>'
            f'<td class="num">{num(f["wilson"], 2)}</td><td>{CONF.get(f["confidence"], f["confidence"])}</td></tr>')
    return ('<div class="rp-scroll"><table class="rp-t"><thead><tr><th>#</th><th>Familia</th><th class="num">Usuarios</th>'
            '<th>Reparto</th><th class="num">% positivo</th><th class="num">Wilson</th><th>Fiabilidad de la muestra</th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table></div>'
            '<p class="rp-leg"><i class="pos"></i> positivas <i class="neu"></i> neutras <i class="neg"></i> negativas</p>')


def bloque_modelos(modelos, an):
    asp = an["aspects_es"]
    rows = []
    for i, m in enumerate(modelos, 1):
        suf = m["confidence"] != "baja"
        pro = asp.get((m.get("pros") or [{}])[0].get("aspect", ""), "—")
        con = asp.get((m.get("cons") or [{}])[0].get("aspect", ""), "—")
        rows.append(
            f'<tr class="{"" if suf else "rp-low"}"><td>{i}</td><th scope="row">{e(m["label"])}</th>'
            f'<td class="num">{m["users"]}</td><td class="bar">{barra(m)}</td>'
            f'<td class="num"><b>{m["pct_positive"]} %</b></td><td class="num">{num(m["wilson"], 2)}</td>'
            f'<td>{e(pro)}</td><td>{e(con)}</td><td>{CONF.get(m["confidence"], m["confidence"])}</td></tr>')
    return ('<div class="rp-scroll"><table class="rp-t"><thead><tr><th>#</th><th>Modelo y generación</th><th class="num">Usuarios</th>'
            '<th>Reparto</th><th class="num">% positivo</th><th class="num">Wilson</th><th>Lo que más gusta</th>'
            '<th>Lo que más molesta</th><th>Muestra</th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table></div>'
            '<p class="rp-nota">Las filas atenuadas tienen menos de 5 votos efectivos: no son comparables.</p>')


def bloque_evolucion(an):
    h = an["history"]
    if len(h) < 2:
        return "<p>Todavía no hay histórico suficiente.</p>"
    a, b = h[-2], h[-1]
    rows = []
    for fid in FAMILIAS:
        fa, fb = a["families"].get(fid), b["families"].get(fid)
        if not fa or not fb:
            continue
        d = fb["pct_positive"] - fa["pct_positive"]
        cls = "up" if d > 0 else "down" if d < 0 else ""
        signo = "+" if d > 0 else ""
        rows.append(f'<tr><th scope="row">{e(fid)}</th><td class="num">{fa["pct_positive"]} %</td>'
                    f'<td class="num">{fb["pct_positive"]} %</td><td class="num {cls}"><b>{signo}{d} pts</b></td>'
                    f'<td class="num">{fa["users"]} → {fb["users"]}</td></tr>')
    return ('<div class="rp-scroll"><table class="rp-t"><thead><tr><th>Familia</th>'
            f'<th class="num">{e(fecha(a["date"]))}</th><th class="num">{e(fecha(b["date"]))}</th>'
            '<th class="num">Cambio</th><th class="num">Usuarios</th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table></div>'
            f'<p class="rp-nota">Entre ambas fechas la muestra pasó de {a["threads"]} a {b["threads"]} hilos: '
            'parte del cambio se debe a datos nuevos, no a que haya cambiado la opinión.</p>')


def spark(valores):
    """Mini gráfico SVG de mediana mensual (si hay 2+ puntos)."""
    if len(valores) < 2:
        return ""
    lo, hi = min(valores), max(valores)
    rng = (hi - lo) or 1
    w, h = 72, 22
    pts = " ".join(f"{i * w / (len(valores) - 1):.1f},{h - 2 - (v - lo) / rng * (h - 4):.1f}" for i, v in enumerate(valores))
    return f'<svg class="rp-spark" viewBox="0 0 {w} {h}" aria-hidden="true"><polyline fill="none" stroke="currentColor" stroke-width="1.6" points="{pts}"/></svg>'


def bloque_precios(precios, pr):
    out = []
    for fam in FAMILIAS:
        filas = [p for p in precios if p["familia"] == fam]
        if not filas:
            continue
        rows = []
        for p in filas:
            u = p["ult"]
            serie = [x["precio"] for x in pr["series"][p["id"]]]
            if p["var"] is None:
                var = '<td class="num">—</td>'
            else:
                cls = "up" if p["var"] > 0 else "down" if p["var"] < 0 else ""
                var = f'<td class="num {cls}">{"+" if p["var"] > 0 else ""}{num(p["var"], 1)} %</td>'
            low = "" if u["n"] >= 5 else ' class="rp-low"'
            rows.append(f'<tr{low}><th scope="row">{e(p["label"])}</th><td class="num"><b>{eur(u["precio"])}</b></td>'
                        f'<td class="num">{eur(u["p25"])} – {eur(u["p75"])}</td><td class="num">{u["n"]}</td>{var}'
                        f'<td>{spark(serie)}</td></tr>')
        out.append(f'<h3>{e(fam)}</h3><div class="rp-scroll"><table class="rp-t"><thead><tr><th>Generación</th>'
                   '<th class="num">Mediana</th><th class="num">Rango central (P25–P75)</th><th class="num">Anuncios</th>'
                   '<th class="num">vs. mes anterior</th><th></th></tr></thead>'
                   f'<tbody>{"".join(rows)}</tbody></table></div>')
    return "".join(out) + ('<p class="rp-nota">Precios de anuncio, no de venta, en AutoScout24.es. La mediana mezcla versiones y kilometrajes '
                           'de cada generación. Las filas atenuadas tienen menos de 5 anuncios y la variación solo se calcula con 5 o más '
                           'en los dos meses.</p>')


def dominio(u):
    try:
        return urlparse(u).netloc.removeprefix("www.")
    except Exception:
        return ""


def bloque_prensa(noticias, menciones, sem_id, sem):
    sem_txt = sem.get("summary", "")
    hl = "".join(f'<li><a href="{e(h["url"])}" rel="noopener" target="_blank">{e(h.get("shortTitle") or h.get("title", ""))}</a>'
                 f'{(" — " + e(h["note"])) if h.get("note") else ""}</li>' for h in sem.get("highlights", [])[:6])
    ns = "".join(f'<li><span class="d">{e(fecha(n["published"]))}</span> <a href="{e(n["url"])}" rel="noopener" target="_blank">'
                 f'{e(n["title"])}</a> <span class="s">{e(n.get("source") or dominio(n["url"]))}</span></li>' for n in noticias)
    ms = "".join(f'<li><span class="d">{e(fecha(m["date"]))}</span> <b>{e(m.get("source") or "")}</b> '
                 f'({ {"positive": "positiva", "negative": "negativa", "neutral": "neutra", "mixed": "mixta"}.get(m.get("sentiment"), m.get("sentiment", ""))}): '
                 f'{e(m["text"])} <a href="{e(m["url"])}" rel="noopener" target="_blank">Fuente</a></li>' for m in menciones)
    return (f'<h3>Resumen de la semana {e(sem_id.split("-W")[1])} de {e(sem_id.split("-W")[0])}</h3><p>{e(sem_txt)}</p>'
            f'<ul class="rp-list">{hl}</ul>'
            f'<h3>Últimas noticias</h3><ul class="rp-list">{ns}</ul>'
            f'<h3>Reseñas y opiniones recientes en medios</h3><ul class="rp-list">{ms}</ul>')


def bloque_faq(preguntas):
    return "".join(f'<details class="rp-faq"><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in preguntas)


def jsonld(an, pr, preguntas, ahora):
    dataset = {
        "@context": "https://schema.org", "@type": "Dataset",
        "name": "Radar Porsche: opinión de propietarios, precios y noticias",
        "description": ("Valoración de propietarios de Porsche por familia y generación (Reddit), mediana mensual de precios de anuncio "
                        "en España (AutoScout24.es) y noticias de la marca."),
        "url": URL, "inLanguage": "es", "dateModified": ahora,
        "creator": {"@type": "Person", "name": "Emilio Rodríguez García", "url": "https://emirodgar.es/emilio"},
        "temporalCoverage": f'{an["stats"]["period_from"]}/{an["stats"]["period_to"]}',
        "spatialCoverage": "España",
        "isBasedOn": [FUENTE + "analisis", "https://arctic-shift.photon-reddit.com", "https://www.autoscout24.es"],
        "variableMeasured": ["Porcentaje de opiniones positivas", "Puntuación Wilson (95 %)", "Mediana de precio de anuncio (EUR)"],
    }
    faq = {"@context": "https://schema.org", "@type": "FAQPage",
           "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in preguntas]}
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Inicio", "item": "https://emirodgar.es/"},
        {"@type": "ListItem", "position": 2, "name": "Dashboards", "item": "https://emirodgar.es/datos/"},
        {"@type": "ListItem", "position": 3, "name": "Radar Porsche", "item": URL}]}
    return "".join(f'<script type="application/ld+json">{json.dumps(o, ensure_ascii=False)}</script>\n' for o in (dataset, faq, crumbs))


CSS = """
.rp{--bg:#0f1418;--panel:#161d22;--line:#27333b;--txt:#e4eaee;--mut:#8a99a4;--acc:#5eead4;--up:#22c55e;--down:#ef4444;--amb:#f59e0b;
 background:var(--bg);color:var(--txt);font-family:"Inter","Helvetica Neue",Arial,system-ui,sans-serif;font-size:14px;line-height:1.55;padding:28px 0 12px}
.rp *{box-sizing:border-box}.rp a{color:var(--acc)}
.rp__wrap{width:calc(100% - 32px);max-width:1180px;margin:0 auto}
.rp-crumb{font-size:12px;color:var(--mut);margin-bottom:10px}.rp-crumb a{color:var(--mut)}
.rp h1{font-size:clamp(24px,4vw,34px);line-height:1.2;margin:0 0 8px}
.rp .lead{color:var(--mut);max-width:80ch;margin:0 0 6px}
.rp h2{font-size:20px;margin:0 0 4px}.rp h3{font-size:15px;margin:22px 0 8px;color:var(--acc)}
.rp-sec{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:20px;margin:18px 0}
.rp-sec>p.sub{color:var(--mut);margin:0 0 14px;max-width:80ch}
.rp-kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin:18px 0}
.rp-kpi{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:14px 16px}
.rp-kpi b{display:block;font-size:22px;line-height:1.2}.rp-kpi span{color:var(--mut);font-size:12px}
.rp-scroll{overflow-x:auto}
.rp-t{width:100%;border-collapse:collapse;font-size:13px}
.rp-t th,.rp-t td{padding:8px 10px;border-bottom:1px solid var(--line);text-align:left;vertical-align:middle;white-space:nowrap}
.rp-t thead th{color:var(--mut);font-weight:600;font-size:12px}
.rp-t th[scope=row]{font-weight:600}.rp-t .num{text-align:right}.rp-t td.bar{min-width:150px;width:200px}
.rp-t .up{color:var(--up)}.rp-t .down{color:var(--down)}
.rp-low{opacity:.5}
.rp-bar{display:flex;height:10px;border-radius:5px;overflow:hidden;background:var(--line)}
.rp-bar i,.rp-leg i{display:inline-block}.rp-bar .pos,.rp-leg .pos{background:var(--up)}
.rp-bar .neu,.rp-leg .neu{background:#64748b}.rp-bar .neg,.rp-leg .neg{background:var(--down)}
.rp-leg{font-size:12px;color:var(--mut);margin:10px 0 0}.rp-leg i{width:10px;height:10px;border-radius:2px;margin:0 4px 0 10px}
.rp-nota{font-size:12px;color:var(--mut);margin:10px 0 0;max-width:90ch}
.rp-spark{width:72px;height:22px;color:var(--acc);vertical-align:middle}
.rp-list{margin:0;padding-left:18px}.rp-list li{margin:6px 0}
.rp-list .d{color:var(--mut);font-size:12px;margin-right:6px}.rp-list .s{color:var(--mut);font-size:12px}
.rp-faq{border-top:1px solid var(--line);padding:10px 0}.rp-faq summary{cursor:pointer;font-weight:600}
.rp-faq p{margin:8px 0 0;color:var(--mut)}
.rp-meta{font-size:12px;color:var(--mut)}
@media(max-width:640px){.rp-sec{padding:14px}}
"""


def chrome():
    """Cabecera, pie y scripts de tema comunes: se copian de ibex35/index.html."""
    with open(os.path.join(ROOT, "ibex35", "index.html"), encoding="utf-8") as f:
        t = f.read()
    header = re.search(r"<header class=\"sg-header\".*?</header>", t, re.S).group(0)
    footer = re.search(r"<footer class=\"sg-footer\">.*?</footer>", t, re.S).group(0)
    ver = re.search(r"chrome\.css\?v=(\d+)", t).group(1)
    return header, footer, ver


def main():
    an, pr, fams, modelos, precios, noticias, menciones, sem_id, sem = preparar()
    preguntas = faqs(an, fams, modelos, precios, pr)
    header, footer, ver = chrome()
    # Fecha derivada de los datos (no del reloj): sin datos nuevos la página no cambia y no hay commit.
    hoy = max([an["generated"], pr["actualizado"][:10]] + [n["published"][:10] for n in noticias])
    titulo = "Radar Porsche | Opinión de propietarios, precios y noticias"
    desc = ("Panel con la valoración de propietarios de Porsche por modelo y generación, los precios de anuncio en España y las noticias "
            "de la marca, con metodología y fuentes.")
    ult_precio = mes_txt(pr["series"]["911-992"][-1]["mes"])

    pagina = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(titulo)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{URL}">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_ES">
<meta property="og:site_name" content="Emirodgar">
<meta property="og:title" content="{e(titulo)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{URL}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<script>try{{if(localStorage.getItem("theme")==="dark"){{document.documentElement.setAttribute("dark","");document.documentElement.classList.add("dark-mode")}}}}catch(e){{}}</script>
<link rel="stylesheet" href="/assets/css/chrome.css?v={ver}">
{jsonld(an, pr, preguntas, hoy)}<style>body{{margin:0;background:#0f1418}}{CSS}</style>
</head>
<body>
{header}
<main class="rp"><div class="rp__wrap">
<p class="rp-crumb"><a href="/">Inicio</a> › <a href="/datos/">Dashboards</a> › Radar Porsche</p>
<h1>Radar Porsche: qué opinan los propietarios, cuánto cuesta y qué se cuenta</h1>
<p class="lead">Tres fuentes en un solo panel: la opinión de propietarios y conductores en Reddit, los precios de anuncio en España y las noticias de la marca.</p>
<p class="rp-meta">Opiniones actualizadas el {e(fecha(an["generated"]))} · Precios de {e(ult_precio)} · Datos al {e(fecha(hoy))}</p>

<div class="rp-kpis">{bloque_kpis(an, pr)}</div>

<section class="rp-sec" id="familias"><h2>Valoración por familia</h2>
<p class="sub">Porcentaje de propietarios y conductores con opinión positiva, con un voto por usuario y modelo. La puntuación Wilson es el límite inferior al 95 % de confianza: premia la consistencia frente al volumen pequeño.</p>
{bloque_familias(fams, an)}</section>

<section class="rp-sec" id="modelos"><h2>Valoración por modelo y generación</h2>
<p class="sub">Ordenado por puntuación de ranking (Wilson × log₂ de votos netos). Incluye lo que más gusta y lo que más molesta en cada uno.</p>
{bloque_modelos(modelos, an)}</section>

<section class="rp-sec" id="evolucion"><h2>Evolución de la valoración</h2>
<p class="sub">Comparativa entre las dos últimas ediciones del análisis.</p>
{bloque_evolucion(an)}</section>

<section class="rp-sec" id="precios"><h2>Precios de segunda mano en España</h2>
<p class="sub">Mediana mensual de los anuncios de coches usados en AutoScout24.es, por generación. Último dato: {e(ult_precio)}.</p>
{bloque_precios(precios, pr)}</section>

<section class="rp-sec" id="prensa"><h2>Noticias y prensa</h2>
<p class="sub">Resumen semanal y últimas publicaciones sobre Porsche.</p>
{bloque_prensa(noticias, menciones, sem_id, sem)}</section>

<section class="rp-sec" id="faq"><h2>Preguntas frecuentes</h2>
<p class="sub">Respuestas generadas a partir de las cifras vigentes de este panel.</p>
{bloque_faq(preguntas)}</section>

<section class="rp-sec" id="metodologia"><h2>Metodología y límites</h2>
<ol class="rp-list">
<li>Se descargan hilos de Reddit sobre Porsche (subreddits generales y de cada modelo) desde el archivo público Arctic Shift.</li>
<li>Un modelo de IA clasifica cada comentario: solo cuentan propietarios actuales o anteriores y quienes han conducido el coche; se descartan bromas, spam y opiniones de oídas.</li>
<li>Un voto por usuario y modelo. Si el modelo es impreciso ("911"), el voto se reparte entre las generaciones posibles.</li>
<li>Ranking = límite inferior de Wilson al 95 % × log₂(1 + votos netos positivos).</li>
</ol>
<p class="rp-nota"><b>Límites:</b> la clasificación la hace una IA y puede equivocarse; los hilos del tipo «¿merece la pena?» atraen a propietarios satisfechos y los subreddits de modelo suelen ser más favorables; es una muestra, no un censo; y los precios son de anuncio, no de venta. Metodología completa y comentarios originales en <a href="{FUENTE}analisis" rel="noopener" target="_blank">mejorimposible.es/porsche/analisis</a>.</p>
</section>
</div></main>
{footer}
<script src="/assets/js/theme.js?v={ver}" defer></script>
</body>
</html>
"""
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(pagina)
    print(f"Escrito {OUT} ({len(pagina):,} bytes, {len(preguntas)} preguntas FAQ)")


if __name__ == "__main__":
    main()
