#!/usr/bin/env python3
"""Atalaya: genera fichas estáticas, rastreables e indexables, que responden a preguntas tipo
«¿Quién ganará las elecciones en Salamanca?» citando solo datos REALES del repositorio:
  - escaños por provincia desde 1977 (atalaya/data/escanos.json, Wikipedia/Interior)
  - media ponderada de encuestas (elecciones-espana/data/2026-11-29/encuestas.json)
  - titulares recientes con enlace (atalaya/data/noticias.json)
Nunca usa los datos simulados del panel.

Salida: atalaya/fichas/index.html, atalaya/fichas/espana/, atalaya/fichas/<provincia>/index.html, atalaya/fichas/sitemap.xml
Uso (raíz del repo): python3 scripts/atalaya/build_fichas.py
"""
import json, math, re, unicodedata
from datetime import datetime, timezone
from html import escape as E
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
D = RAIZ / "atalaya/data"; OUT = RAIZ / "atalaya/fichas"
BASE = "https://emirodgar.es"
ES = {"Araba": "Álava", "Alacant": "Alicante", "Castelló": "Castellón", "Illes Balears": "Baleares", "València": "Valencia",
      "Gipuzkoa": "Guipúzcoa", "Bizkaia": "Vizcaya"}
ID2P = {"PP": "PP", "PSOE": "PSOE", "VOX": "Vox", "SUMAR": "Sumar", "PODEMOS": "Podemos"}
CYL = {"05", "09", "24", "34", "37", "40", "42", "47", "49"}
HOY = datetime.now(timezone.utc)
FECHA = HOY.strftime("%Y-%m-%d")
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
def fecha_es(iso): d = datetime.fromisoformat(iso[:10]); return f"{d.day} de {MESES[d.month-1]} de {d.year}"

def slug(s): return re.sub(r"[^a-z0-9]+", "-", unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()).strip("-")
def J(p): return json.loads(Path(p).read_text(encoding="utf8"))

def poll_avg():
    enc = J(RAIZ / "elecciones-espana/data/2026-11-29/encuestas.json")
    s = [x for x in enc["sondeos"] if not re.search("cis", x["empresa"], re.I)]
    last = datetime.fromisoformat(s[0]["fecha"])
    rec = [x for x in s if (last - datetime.fromisoformat(x["fecha"])).days <= 30]
    sm, ct = {}, {}
    for x in rec:
        w = math.sqrt(x.get("muestra") or 1000)
        for k, v in x["voto"].items():
            p = ID2P.get(k)
            if p: sm[p] = sm.get(p, 0) + v * w; ct[p] = ct.get(p, 0) + w
    return {p: sm[p] / ct[p] for p in sm}, len(rec), s[0]["fecha"]

CSS = """body{font:16px/1.6 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;max-width:820px;margin:0 auto;padding:24px 16px 64px;color:#1b2330;background:#fff}
h1{font-size:30px;line-height:1.2;margin:.2em 0 .4em}h2{font-size:21px;margin:1.6em 0 .4em;border-top:1px solid #e3e8ef;padding-top:1em}
.ans{background:#eef6ff;border-left:4px solid #2563eb;padding:14px 16px;border-radius:6px;font-size:18px}
table{border-collapse:collapse;width:100%;font-size:14px;margin:.6em 0}th,td{border:1px solid #d9e0ea;padding:6px 8px;text-align:right}th:first-child,td:first-child{text-align:left}th{background:#f4f7fb}
.meta,.src{color:#5b6778;font-size:14px}a{color:#1d4ed8}nav.bc{font-size:14px;color:#5b6778}.warn{background:#fff8e6;border-left:4px solid #d99a00;padding:10px 14px;border-radius:6px;font-size:15px}
li{margin:.3em 0}details{margin:.5em 0}summary{cursor:pointer;font-weight:600}
@media (prefers-color-scheme:dark){body{background:#0e1219;color:#e5e9f0}h2{border-color:#243044}.ans{background:#0f2036}th{background:#151d29}th,td{border-color:#273449}.meta,.src,nav.bc{color:#98a5b8}a{color:#7cb0ff}.warn{background:#2a2310}}"""

def pagina(ruta, titulo, desc, h1, cuerpo, jsonld, bc, shell=False):
    url = f"{BASE}/atalaya/fichas/{ruta}"
    css_extra = '<link rel="stylesheet" href="/atalaya/assets/shell.css">' if shell else ""
    js_extra = '<script src="/atalaya/assets/shell.js"></script>' if shell else ""
    pad = "body{max-width:none;padding-left:calc(var(--sbp) + 24px)}main{max-width:820px}" if shell else ""
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(titulo)}</title>
<meta name="description" content="{E(desc)}">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article"><meta property="og:locale" content="es_ES"><meta property="og:site_name" content="Emirodgar">
<meta property="og:title" content="{E(titulo)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{url}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
{css_extra}
<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>
<style>{CSS}{pad}</style>
</head>
<body>
{js_extra}
<nav class="bc" aria-label="Migas de pan">{bc}</nav>
<main>
<h1>{E(h1)}</h1>
{cuerpo}
</main>
<footer class="src"><p>Elaborado por <a href="https://emirodgar.es/sobre-mi">Emilio Rodríguez García</a> con el panel <a href="/atalaya/">Atalaya</a>. Última actualización: {fecha_es(FECHA)}. Contenido basado en datos públicos citados en cada apartado; no es una encuesta ni una predicción oficial.</p></footer>
</body>
</html>
"""
    d = OUT / ruta.rstrip("/"); d.mkdir(parents=True, exist_ok=True); (d / "index.html").write_text(html, encoding="utf8")

def tabla_escanos(v, n=6):
    labs = v["elecciones"][-n:]
    pts = [p for p in ["PP", "PSOE", "Vox", "Cs", "Podemos", "Sumar", "IU"] if p in v["partidos"] and any(v["partidos"][p][-n:])]
    th = "".join(f"<th>{E(l)}</th>" for l in labs)
    filas = "".join(f"<tr><td>{p}</td>" + "".join(f"<td>{x}</td>" for x in v["partidos"][p][-n:]) + "</tr>" for p in pts)
    tot = v.get("total")
    if tot: filas += "<tr><td><b>Total escaños</b></td>" + "".join(f"<td><b>{x if x is not None else '–'}</b></td>" for x in tot[-n:]) + "</tr>"
    return f"<table><thead><tr><th>Partido</th>{th}</tr></thead><tbody>{filas}</tbody></table>"

def analisis_provincia(v, nacional):
    """Devuelve (frase_respuesta, líder, victorias, N, detalle) usando solo escaños reales."""
    n = 6; labs = v["elecciones"][-n:]; part = {p: s[-n:] for p, s in v["partidos"].items()}
    last = {p: s[-1] for p, s in part.items()}
    top = sorted(last.items(), key=lambda x: -x[1]); L, ls = top[0]
    tot = (v.get("total") or [None])[-1]
    empate = len(top) > 1 and top[1][1] == ls
    otros = (tot - sum(last.values())) if tot else 0
    wins = sum(1 for i in range(len(labs)) if part[L][i] > max([part[p][i] for p in part if p != L] or [0]))
    lider_enc = max(nacional, key=nacional.get) if nacional else None
    return L, ls, tot, empate, otros, wins, len(labs), lider_enc

def nes(x):
    return f"{x:,}".replace(",", ".")

def de(ls, tot):
    return f"{ls} de {tot}" if tot else f"{ls} escaños"

def art(p, cap=False):
    t = ("el " + p) if p in ("PP", "PSOE") else {"Cs": "Ciudadanos"}.get(p, p)
    return t[0].upper() + t[1:] if cap else t

def respuesta(nombre, v, nacional):
    L, ls, tot, empate, otros, wins, N, enc = analisis_provincia(v, nacional)
    aL, aLc = art(L), art(L, True)
    anos = f"{v['elecciones'][-N].split()[0]}–{v['elecciones'][-1].split()[0]}"
    if empate or (tot and otros >= ls):
        return (f"En {nombre} el resultado está abierto: en 2023 hubo empate a escaños en la cabeza o el peso de otras fuerzas es comparable al del primer partido ({aL}, {de(ls, tot)}), "
                f"así que con los datos públicos disponibles no se puede señalar un favorito claro."), L, "abierto"
    base = f"{aLc} fue el partido con más escaños en {nombre} en 2023 ({de(ls, tot)}) y lo ha sido en {wins} de las últimas {N} convocatorias generales ({anos})."
    if wins >= N - 1 and (enc is None or L == enc or L not in ("PP", "PSOE")):
        return (f"Lo más probable es que {aL} vuelva a ser la fuerza con más escaños en {nombre}. {base} La media nacional de encuestas no apunta a un cambio de tendencia.", L, "probable")
    if wins >= N - 1:
        return (f"{aLc} parte como favorito en {nombre}, aunque con riesgo: {base} Sin embargo, la media nacional de encuestas favorece ahora a {art(enc)}, lo que podría reducir su ventaja.", L, "favorito con riesgo")
    if wins >= N // 2:
        return (f"El resultado en {nombre} está abierto, con ligera ventaja para {aL}. {base}", L, "abierto")
    return (f"Muy abierto: en {nombre} ningún partido domina de forma estable. {aLc} fue primero en 2023 ({de(ls, tot)}) pero solo en {wins} de las últimas {N} convocatorias.", L, "muy abierto")

def nrm(t): return unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower()

def titulares(pc, nombre, n=5):
    """Solo titulares cuyo texto o medio nombran la provincia: evita el ruido de la búsqueda de Google Noticias."""
    claves = {nrm(nombre), nrm(ES.get(nombre, nombre)), nrm(PROV[pc])}
    nw = [x for x in J(D / "noticias.json")["noticias"] if pc in x["pv"] and any(k in nrm(x["t"]) or k in nrm(x["m"]) for k in claves)]
    return nw[:n]

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    global PROV
    ind = J(D / "indice.json"); prov = ind["prov"]; PROV = prov; esc = J(D / "escanos.json")
    pad = J(D / "padron.json"); anio_pad = pad["anios"][0]
    nacional, nsond, fsond = poll_avg()
    orden = sorted(nacional.items(), key=lambda x: -x[1]); lider = orden[0][0]
    conv = J(RAIZ / "elecciones-espana/data/2026-11-29/convocatoria.json")
    urls = []
    items = []

    for pc, nom in prov.items():
        nombre = ES.get(nom, nom); sl = slug(nombre); ruta = f"{sl}/"
        v = esc.get(pc); tit = titulares(pc, nombre)
        pob = (pad["prov"].get(pc) or [None])[0]
        q = f"¿Quién ganará las elecciones generales en {nombre}?"
        if v:
            resp, L, nivel = respuesta(nombre, v, nacional)
            tot = (v.get("total") or [None])[-1]
            cab = f"<p class='ans'>{E(resp)}</p>"
            ev = (f"<h2>1. Qué ha votado {E(nombre)} en las últimas elecciones generales</h2><p>Escaños al Congreso por partido en las últimas convocatorias generales (fuente: <a href='{v['url']}'>Wikipedia, «{E(v['titulo'])}»</a>, que recoge datos oficiales; la serie completa llega hasta 1977):</p>{tabla_escanos(v)}"
                  f"<p>{E(nombre)} elige {tot} diputados al Congreso. Con pocos escaños en juego, unos pocos votos pueden mover el último escaño entre partidos." + (f" Tiene {nes(pob)} habitantes (INE, 1 de enero de {anio_pad}), unos {nes(round(pob / tot))} por diputado." if pob else "") + "</p>" if tot else "")
            faq_hist = f"En 2023, {art(L)} fue el partido con más escaños en {nombre}." if L else ""
            desc = resp.split(". ")[0].rstrip(".") + ". Escaños en el Congreso, encuestas y noticias recientes."
        else:
            resp = f"No hay todavía datos suficientes para señalar un favorito en {nombre}: no hemos podido cargar su histórico de escaños. Lo que sí se sabe es el contexto nacional: la media de encuestas sitúa a {art(lider)} en cabeza."
            cab = f"<p class='ans'>{E(resp)}</p>"; ev = f"<h2>1. Histórico de {E(nombre)}</h2><p>Pendiente de carga desde fuentes oficiales.</p>"
            faq_hist = ""; desc = resp.split(". ")[0].rstrip(".") + "."; nivel = "sin datos"
        nac = ", ".join(f"{p} {v_:.1f}%" for p, v_ in orden[:5])
        ev += (f"<h2>2. El clima nacional</h2><p>Media ponderada de {nsond} sondeos publicados en los 30 días previos al {fecha_es(fsond)} (sin CIS): {E(nac)}. "
               f"No hay una encuesta pública específica de {E(nombre)} cargada en este análisis, así que se aplica la tendencia general como contexto, no como previsión provincial. "
               f"Fuente: <a href='/elecciones-espana/'>Elecciones en España</a>.</p>")
        if tit:
            ev += f"<h2>3. Señales recientes en {E(nombre)}</h2><ul>" + "".join(f"<li><a href='{E(x['u'])}' rel='nofollow noopener'>{E(re.sub(chr(32)+'-'+chr(32)+'[^-]{3,60}$', '', x['t']))}</a> <span class='meta'>({E(x['m'])}, {fecha_es(x['f'])})</span></li>" for x in tit) + "</ul>"
        else:
            ev += f"<h2>3. Señales recientes en {E(nombre)}</h2><p>No se han detectado titulares recientes sobre política en {E(nombre)} en las fuentes monitorizadas.</p>"
        limites = ("<h2>Qué podría cambiar el resultado</h2><ul><li>Un cambio de tendencia nacional en las semanas finales de campaña.</li><li>Un hecho que afecte a la imagen de los candidatos locales o nacionales (imputaciones, dimisiones, crisis de gestión).</li>"
                   "<li>La participación y el reparto de los indecisos, que en provincias con pocos escaños pueden mover el último diputado.</li></ul>"
                   "<h2>Lo que este análisis no incluye</h2><p class='warn'>Todavía no usa encuestas provinciales, resultados municipales ni análisis de sentimiento en redes. Es una estimación razonada con datos públicos, no una encuesta ni una previsión oficial.</p>")
        fesc = ("<a href='" + v["url"] + "'>Wikipedia</a> (que recoge datos oficiales de resultados)") if v else "pendiente"
        fuentes = (f"<h2>Fuentes y método</h2><ul><li>Escaños por provincia: {fesc}.</li>"
                   f"<li>Encuestas: sondeos publicados por empresas y medios, ponderados por antigüedad y tamaño de muestra, en <a href='/elecciones-espana/'>Elecciones en España</a>.</li>"
                   "<li>Noticias: titulares por RSS de medios nacionales y de Google Noticias para prensa local, etiquetados por provincia.</li>"
                   "<li>Método: el partido con más escaños en 2023 y su regularidad en las últimas seis convocatorias, contrastados con la tendencia nacional de encuestas.</li></ul>"
                   f"<p>Explora el territorio en el <a href='/atalaya/#{pc}'>panel Atalaya</a>.</p>")
        faqs = [(q, resp)]
        if faq_hist: faqs.append((f"¿Quién ganó en {nombre} en las elecciones generales de 2023?", faq_hist + (f" Obtuvo {v['partidos'][L][-1]} de {tot} escaños." if tot else "")))
        faqs.append((f"¿Cuándo son las próximas elecciones generales?", f"Las elecciones generales se celebran el 29 de noviembre de 2026."))
        if tot: faqs.append((f"¿Cuántos diputados elige {nombre} al Congreso?", f"{nombre} elige {tot} diputados al Congreso de los Diputados."))
        if pob: faqs.append((f"¿Cuántos habitantes tiene {nombre}?", f"{nombre} tiene {nes(pob)} habitantes según el padrón del INE a 1 de enero de {anio_pad}."))
        faq_html = "<h2>Preguntas frecuentes</h2>" + "".join(f"<details><summary>{E(a)}</summary><p>{E(b)}</p></details>" for a, b in faqs)
        ld = [{"@context": "https://schema.org", "@type": "Article", "headline": q, "description": desc, "inLanguage": "es", "datePublished": FECHA, "dateModified": FECHA,
               "author": {"@type": "Person", "name": "Emilio Rodríguez García", "url": f"{BASE}/sobre-mi"},
               "publisher": {"@type": "Person", "name": "Emilio Rodríguez García"}, "mainEntityOfPage": f"{BASE}/atalaya/fichas/{ruta}", "about": nombre},
              {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": a, "acceptedAnswer": {"@type": "Answer", "text": b}} for a, b in faqs]},
              {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                  {"@type": "ListItem", "position": 1, "name": "Atalaya", "item": f"{BASE}/atalaya/"},
                  {"@type": "ListItem", "position": 2, "name": "Fichas", "item": f"{BASE}/atalaya/fichas/"},
                  {"@type": "ListItem", "position": 3, "name": nombre, "item": f"{BASE}/atalaya/fichas/{ruta}"}]}]
        bc = "<a href='/atalaya/'>Atalaya</a> › <a href='/atalaya/fichas/'>Fichas</a> › " + E(nombre)
        cuerpo = f"<p class='meta'>Actualizado el {fecha_es(FECHA)} · Elecciones generales del 29 de noviembre de 2026</p>{cab}{ev}{limites}{faq_html}{fuentes}"
        pagina(ruta, f"¿Quién ganará las elecciones en {nombre}? Análisis y datos (29N 2026)", desc, q, cuerpo, ld, bc)
        urls.append(f"{BASE}/atalaya/fichas/{ruta}"); items.append((nombre, ruta, nivel, resp))

    # España
    pp = orden[0]; sg = orden[1]
    resp = (f"Las encuestas sitúan a {art(pp[0])} en cabeza ({pp[1]:.1f}%), con {pp[1]-sg[1]:.1f} puntos sobre {art(sg[0])} ({sg[1]:.1f}%), pero el resultado no está decidido: "
            f"el reparto de escaños depende de lo que ocurra provincia a provincia.")
    nac = "".join(f"<tr><td>{p}</td><td>{v_:.1f}%</td></tr>" for p, v_ in orden)
    cuerpo = (f"<p class='meta'>Actualizado el {fecha_es(FECHA)}</p><p class='ans'>{E(resp)}</p>"
              f"<h2>Media de encuestas</h2><p>Media ponderada de {nsond} sondeos de los 30 días previos al {fecha_es(fsond)} (sin CIS).</p><table><thead><tr><th>Partido</th><th>Estimación de voto</th></tr></thead><tbody>{nac}</tbody></table>"
              "<p>Detalle y metodología en <a href='/elecciones-espana/'>Elecciones en España</a>.</p>"
              "<h2>Por provincias</h2><p>Consulta la ficha de cada provincia:</p><ul>" + "".join(f"<li><a href='/atalaya/fichas/{r}'>{E(n)}</a></li>" for n, r, _, _ in items) + "</ul>"
              "<h2>Límites</h2><p class='warn'>Una media de encuestas no es una previsión de escaños. No incluye todavía modelos territoriales ni análisis de redes.</p>")
    q = "¿Quién ganará las elecciones generales de 2026 en España?"
    ld = [{"@context": "https://schema.org", "@type": "Article", "headline": q, "description": resp, "inLanguage": "es", "datePublished": FECHA, "dateModified": FECHA,
           "author": {"@type": "Person", "name": "Emilio Rodríguez García", "url": f"{BASE}/sobre-mi"}, "mainEntityOfPage": f"{BASE}/atalaya/fichas/espana/"},
          {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": resp}}]}]
    pagina("espana/", "¿Quién ganará las elecciones generales de 2026? Encuestas y análisis", resp[:155], q, cuerpo, ld, "<a href='/atalaya/'>Atalaya</a> › <a href='/atalaya/fichas/'>Fichas</a> › España")
    urls.insert(0, f"{BASE}/atalaya/fichas/espana/")

    # hub
    filas = "".join(f"<li><a href='/atalaya/fichas/{r}'>¿Quién ganará en {E(n)}?</a> <span class='meta'>— {E(niv)}</span></li>" for n, r, niv, _ in items)
    cuerpo = (f"<p>Respuestas razonadas, con fuentes y fecha, sobre las elecciones generales del 29 de noviembre de 2026. Cada ficha usa solo datos públicos verificables (escaños desde 1977, encuestas y noticias) y explica qué incluye y qué no.</p>"
              f"<h2>España</h2><ul><li><a href='/atalaya/fichas/espana/'>¿Quién ganará las elecciones generales de 2026?</a></li></ul><h2>Por provincias</h2><ul>{filas}</ul>")
    ld = [{"@context": "https://schema.org", "@type": "CollectionPage", "name": "Fichas electorales por provincia", "url": f"{BASE}/atalaya/fichas/", "inLanguage": "es"}]
    pagina("", "Fichas electorales por provincia: ¿quién ganará? | Atalaya", "Quién ganará las elecciones generales de 2026 en cada provincia de España, con datos de escaños, encuestas y noticias.", "Fichas electorales por provincia", cuerpo, ld, "<a href='/atalaya/'>Atalaya</a> › Fichas", shell=True)
    urls.insert(0, f"{BASE}/atalaya/fichas/")
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"<url><loc>{u}</loc><lastmod>{FECHA}</lastmod></url>\n" for u in urls) + "</urlset>\n", encoding="utf8")
    print(len(urls), "páginas;", sum(1 for _, _, n, _ in items if n != "sin datos"), "provincias con histórico")
    for n, r, niv, rs in items:
        if n in ("Salamanca", "Barcelona", "Sevilla", "Madrid"): print(n, "|", niv, "|", rs[:200])
main()
from manifest import marcar
marcar("fichas")
