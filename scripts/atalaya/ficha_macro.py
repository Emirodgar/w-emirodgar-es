#!/usr/bin/env python3
"""Atalaya: fichas de histórico macroeconómico con los periodos de gobierno superpuestos
(estáticas, indexables, sin JavaScript).

  /atalaya/fichas/macro/<slug>/   serie histórica de un indicador, con una banda de color por
                                  periodo de gobierno (atalaya/data/gobiernos.json) de fondo.
                                  Las bandas señalan quién gobernaba, nunca implican causalidad.

Genérico: cada indicador es un fichero en INDICADORES, con una o dos series (principal y,
opcionalmente, secundaria). Para añadir uno nuevo (PIB, autónomos...): crear su JSON siguiendo
la forma de atalaya/data/presion_fiscal.json y añadir su nombre de fichero a INDICADORES.

Uso (raíz del repo): python3 scripts/atalaya/ficha_macro.py
"""
import json
from datetime import datetime, timezone
from html import escape as E
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
D = RAIZ / "atalaya/data"
OUT = RAIZ / "atalaya/fichas"
BASE = "https://emirodgar.es"
HOY = datetime.now(timezone.utc)
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

INDICADORES = ["presion_fiscal.json", "paro_epa.json", "pib.json", "autonomos.json", "pib_per_capita.json", "deficit.json", "deuda.json", "gasto_publico.json"]


def fecha_es(iso):
    d = datetime.fromisoformat(iso[:10])
    return f"{d.day} de {MESES[d.month - 1]} de {d.year}"


def J(p):
    return json.loads(Path(p).read_text(encoding="utf8"))


def nf(v, decimales=1):
    """Formatea en estilo español: punto de millar, coma decimal (p. ej. 34.240 o 2,6)."""
    s = f"{v:,.{decimales}f}"
    return s.replace(",", "§").replace(".", ",").replace("§", ".")


CSS = """body{font:16px/1.6 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;max-width:860px;margin:0 auto;padding:24px 16px 64px;color:#1b2330;background:#fff}
h1{font-size:28px;line-height:1.2;margin:.2em 0 .4em}h2{font-size:21px;margin:1.6em 0 .4em;border-top:1px solid #e3e8ef;padding-top:1em}
.ans{background:#eef6ff;border-left:4px solid #2563eb;padding:14px 16px;border-radius:6px;font-size:18px}
.meta,.src{color:#5b6778;font-size:14px}a{color:#1d4ed8}nav.bc{font-size:14px;color:#5b6778}
.warn{background:#fff8e6;border-left:4px solid #d99a00;padding:10px 14px;border-radius:6px;font-size:15px}
li{margin:.3em 0}main,h1{overflow-wrap:anywhere}
.chart-wrap{margin:1em 0}.chart-wrap svg{width:100%;height:auto;display:block}
.leyenda{display:flex;flex-wrap:wrap;gap:14px;font-size:13px;color:#5b6778;margin:.6em 0}
.leyenda span{display:inline-flex;align-items:center;gap:5px}
.leyenda i{width:14px;height:3px;border-radius:2px;display:inline-block}
.gband-label{font-size:11px;fill:#5b6778}
.axis-label{font-size:11px;fill:#5b6778}
.grid{stroke:#e3e8ef;stroke-width:1}.grid.cero{stroke:#b7c0cc;stroke-width:1.5}
table.datos{border-collapse:collapse;width:100%;font-size:14px;margin:.6em 0}
table.datos th,table.datos td{border:1px solid #d9e0ea;padding:5px 8px;text-align:right}
table.datos th:first-child,table.datos td:first-child{text-align:left}
table.datos th{background:#f4f7fb}
details summary{cursor:pointer;font-weight:600;color:#1d4ed8}
.ring{fill:#fff}
.ls-principal{stroke:#1b2330}.ls-secundaria{stroke:#94a3b8}
.leyenda i.ls-principal{background:#1b2330}.leyenda i.ls-secundaria{background:#94a3b8}
circle.ls-principal.dot{fill:#1b2330;stroke:none}circle.ls-secundaria.dot{fill:#94a3b8;stroke:none}
text.ls-principal.endlabel{fill:#1b2330}text.ls-secundaria.endlabel{fill:#5b6778}
@media (prefers-color-scheme:dark){body{background:#0e1219;color:#e5e9f0}h2{border-color:#243044}.ans{background:#0f2036}
.meta,.src,nav.bc,.leyenda{color:#98a5b8}a{color:#7cb0ff}.warn{background:#2a2310}
.grid{stroke:#243044}.grid.cero{stroke:#3b4b63}.gband-label,.axis-label{fill:#8b97a8}
table.datos th,table.datos td{border-color:#273449}table.datos th{background:#151d29}
details summary{color:#7cb0ff}.ring{fill:#0e1219}
.ls-principal{stroke:#e5e9f0}.ls-secundaria{stroke:#475569}
.leyenda i.ls-principal{background:#e5e9f0}.leyenda i.ls-secundaria{background:#475569}
circle.ls-principal.dot{fill:#e5e9f0}circle.ls-secundaria.dot{fill:#475569}
text.ls-principal.endlabel{fill:#e5e9f0}text.ls-secundaria.endlabel{fill:#98a5b8}}"""


def pagina(ruta, titulo, desc, h1, cuerpo, jsonld, bc, pie):
    url = f"{BASE}/atalaya/fichas/{ruta}"
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
<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>
<style>{CSS}</style>
</head>
<body>
<nav class="bc" aria-label="Migas de pan">{bc}</nav>
<main>
<h1>{E(h1)}</h1>
{cuerpo}
</main>
<footer class="src"><p>{pie}</p></footer>
</body>
</html>
"""
    d = OUT / ruta.rstrip("/")
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(html, encoding="utf8")
    return url


def grafico(ind, gobiernos, anio_min, anio_max):
    """SVG sin JS: línea principal (tinta) + línea secundaria opcional (gris), bandas de gobierno de fondo."""
    y_max, y_paso, unidad = ind["yMax"], ind["yPaso"], ind["unidad"]
    y_min = ind.get("yMin", 0)
    dec = ind.get("decimales", 1)
    dec_eje = 0 if float(y_paso).is_integer() else len(str(y_paso).split(".")[-1])
    W, H = 760, 320
    ML, MR, MT, MB = 42, 70, 14, 28
    PW, PH = W - ML - MR, H - MT - MB

    def x(anio):
        return ML + (anio - anio_min) / (anio_max - anio_min) * PW

    def y(val):
        return MT + PH - (val - y_min) / (y_max - y_min) * PH

    partes = []
    # bandas de gobierno
    for per in gobiernos["periodos"]:
        desde, hasta = per["desde"], per["hasta"] or anio_max + 1
        if hasta <= anio_min or desde >= anio_max + 1:
            continue
        x0, x1 = x(max(desde, anio_min)), x(min(hasta, anio_max + 1))
        color = gobiernos["colorPartido"].get(per["partido"], "#94a3b8")
        partes.append(f"<rect x='{x0:.1f}' y='{MT}' width='{(x1 - x0):.1f}' height='{PH}' fill='{color}' opacity='0.10'/>")
        if x1 - x0 > 26:
            partes.append(f"<text class='gband-label' x='{(x0 + x1) / 2:.1f}' y='{MT + 13}' text-anchor='middle'>{E(per['partido'])}</text>")
    # separadores verticales entre periodos
    for per in gobiernos["periodos"][1:]:
        if anio_min < per["desde"] < anio_max + 1:
            xi = x(per["desde"])
            partes.append(f"<line class='grid' x1='{xi:.1f}' y1='{MT}' x2='{xi:.1f}' y2='{MT + PH}'/>")
    # cuadrícula horizontal + etiquetas eje Y (empieza en el primer múltiplo de y_paso >= y_min)
    v = -(-y_min // y_paso) * y_paso if y_min < 0 else (y_min // y_paso) * y_paso
    while v <= y_max:
        yy = y(v)
        cls = "grid cero" if v == 0 and y_min < 0 else "grid"
        partes.append(f"<line class='{cls}' x1='{ML}' y1='{yy:.1f}' x2='{ML + PW}' y2='{yy:.1f}'/>")
        signo = "+" if (y_min < 0 and v > 0) else ""
        partes.append(f"<text class='axis-label' x='{ML - 6}' y='{yy + 4:.1f}' text-anchor='end'>{signo}{nf(v, dec_eje)}{unidad}</text>")
        v += y_paso
    # eje X: años cada 5 (cada 10 si la serie pasa de 40 años, para no amontonar etiquetas)
    paso_x = 10 if (anio_max - anio_min) > 40 else 5
    anio = anio_min
    while anio <= anio_max:
        partes.append(f"<text class='axis-label' x='{x(anio):.1f}' y='{H - 8}' text-anchor='middle'>{anio}</text>")
        anio += paso_x

    def linea(serie, cls, grosor):
        anios = sorted(int(a) for a in serie["datos"])
        pts = " ".join(f"{x(a):.1f},{y(serie['datos'][str(a)]):.1f}" for a in anios)
        ult = anios[-1]
        xu, yu = x(ult), y(serie["datos"][str(ult)])
        titulo = f"<title>{ult}: {nf(serie['datos'][str(ult)], dec)} {unidad}</title>"
        return (f"<polyline class='{cls}' fill='none' stroke-width='{grosor}' stroke-linejoin='round' stroke-linecap='round' points='{pts}'>{titulo}</polyline>"
                f"<circle cx='{xu:.1f}' cy='{yu:.1f}' r='6' class='ring'/>"
                f"<circle cx='{xu:.1f}' cy='{yu:.1f}' r='4' class='{cls} dot'/>"
                f"<text class='{cls} endlabel' x='{xu + 8:.1f}' y='{yu + 4:.1f}' font-size='13' font-weight='600'>{nf(serie['datos'][str(ult)], dec)} {unidad}</text>")

    if "secundaria" in ind["series"]:
        partes.append(linea(ind["series"]["secundaria"], "ls-secundaria", 2))
    partes.append(linea(ind["series"]["principal"], "ls-principal", 2.5))
    inner = "".join(partes)
    etiqueta_principal = ind["series"]["principal"]["etiqueta"]
    return f"<svg viewBox='0 0 {W} {H}' role='img' aria-label='Evolución de {E(etiqueta_principal)} en España, {anio_min}-{anio_max}'>{inner}</svg>"


def tabla_datos(ind, gobiernos):
    principal = ind["series"]["principal"]["datos"]
    secundaria = ind["series"].get("secundaria", {}).get("datos")
    anios = sorted(int(a) for a in principal)
    dec = ind.get("decimales", 1)

    def gobierno_de(a):
        for per in gobiernos["periodos"]:
            if per["desde"] <= a < (per["hasta"] or 9999):
                return per["presidente"]
        return "—"

    cab_sec = f"<th>{E(ind['series']['secundaria']['etiqueta'])}</th>" if secundaria else ""
    filas = "".join(
        f"<tr><td>{a}</td><td>{nf(principal[str(a)], dec)}</td>"
        + (f"<td>{nf(secundaria[str(a)], dec)}</td>" if secundaria else "")
        + f"<td>{E(gobierno_de(a))}</td></tr>"
        for a in anios)
    return (f"<details><summary>Ver los {len(anios)} años en tabla</summary>"
            f"<table class='datos'><thead><tr><th>Año</th><th>{E(ind['colTabla'])}</th>{cab_sec}<th>Presidente</th></tr></thead>"
            f"<tbody>{filas}</tbody></table></details>")


def construir(ind, gob):
    principal = ind["series"]["principal"]["datos"]
    anios = sorted(int(a) for a in principal)
    a0, a1 = anios[0], anios[-1]
    chart = grafico(ind, gob, a0, a1)
    partidos_visibles = {per["partido"] for per in gob["periodos"] if (per["hasta"] or a1 + 1) > a0 and per["desde"] < a1 + 1}
    leyenda_gob = " · ".join(f"<span><i style='background:{E(c)}'></i>{E(p)}</span>" for p, c in gob["colorPartido"].items() if p in partidos_visibles)
    leyenda_series = f"<span><i class='ls-principal'></i>{E(ind['series']['principal']['etiqueta'])}</span>"
    if "secundaria" in ind["series"]:
        leyenda_series += f"<span><i class='ls-secundaria'></i>{E(ind['series']['secundaria']['etiqueta'])}</span>"
    enlaces = "".join(f"<li><a href='{E(e['url'])}'>{E(e['titulo'])}</a>: {E(e['desc'])}</li>" for e in ind.get("enlaces", []))
    cuerpo = (f"<p class='meta'>Actualizado el {fecha_es(ind['actualizado'])}</p>"
              f"<p class='ans'>{E(ind['resumen'])}</p>"
              f"<p class='warn'>{E(ind['aviso'])}</p>"
              f"<h2>Evolución desde {a0}</h2>"
              "<div class='chart-wrap'>" + chart + "</div>"
              f"<p class='leyenda'>{leyenda_series}</p>"
              f"<p class='meta'>Bandas de color: quién gobernaba en cada periodo — {leyenda_gob}. "
              "No implica que este indicador dependa solo del partido en el Gobierno: el ciclo económico, las crisis y el contexto internacional pesan tanto o más.</p>"
              + tabla_datos(ind, gob)
              + f"<p class='fu src'>Fuente: <a href='{E(ind['fuenteUrl'])}' rel='nofollow noopener'>{E(ind['fuente'])}</a>.</p>"
              "<h2>Para seguir profundizando</h2><ul>" + enlaces + "</ul>")
    faqs = [(ind["pregunta_faq"], ind["resumen"])]
    ruta = f"macro/{ind['slug']}/"
    ld = [{"@context": "https://schema.org", "@type": "Article", "headline": ind["titulo_pagina"], "description": ind["resumen"], "inLanguage": "es",
           "datePublished": ind["actualizado"], "dateModified": ind["actualizado"],
           "author": {"@type": "Person", "name": "Emilio Rodríguez García", "url": f"{BASE}/sobre-mi"},
           "publisher": {"@type": "Person", "name": "Emilio Rodríguez García"},
           "mainEntityOfPage": f"{BASE}/atalaya/fichas/{ruta}"},
          {"@context": "https://schema.org", "@type": "FAQPage",
           "mainEntity": [{"@type": "Question", "name": a, "acceptedAnswer": {"@type": "Answer", "text": b}} for a, b in faqs]},
          {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
              {"@type": "ListItem", "position": 1, "name": "Atalaya", "item": f"{BASE}/atalaya/"},
              {"@type": "ListItem", "position": 2, "name": "Fichas", "item": f"{BASE}/atalaya/fichas/"},
              {"@type": "ListItem", "position": 3, "name": ind["titulo_pagina"].split(":")[0], "item": f"{BASE}/atalaya/fichas/{ruta}"}]}]
    bc = f"<a href='/atalaya/'>Atalaya</a> › <a href='/atalaya/fichas/'>Fichas</a> › {E(ind['titulo_pagina'].split(':')[0])}"
    pie = (f"Elaborado por <a href=\"https://emirodgar.es/sobre-mi\">Emilio Rodríguez García</a> con el panel <a href=\"/atalaya/\">Atalaya</a>. "
           f"Última actualización: {fecha_es(ind['actualizado'])}. Contenido basado en datos públicos citados en cada apartado; "
           "no es una opinión política. <a href=\"/atalaya/privacidad/\">Política de privacidad</a>.")
    return pagina(ruta, ind["titulo_pagina"], ind["resumen"], ind["h1"], cuerpo, ld, bc, pie)


def main():
    gob = J(D / "gobiernos.json")
    for nombre in INDICADORES:
        ruta_datos = D / nombre
        if not ruta_datos.exists():
            print(f"Omitido (no existe todavía): {nombre}")
            continue
        url = construir(J(ruta_datos), gob)
        print("Publicado:", url)


if __name__ == "__main__":
    main()
