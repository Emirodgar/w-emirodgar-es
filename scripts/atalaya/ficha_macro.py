#!/usr/bin/env python3
"""Atalaya: fichas de histórico macroeconómico con los periodos de gobierno superpuestos
(estáticas, indexables, sin JavaScript).

  /atalaya/fichas/macro/<slug>/   serie histórica de un indicador, con una banda de color por
                                  periodo de gobierno (atalaya/data/gobiernos.json) de fondo.
                                  Las bandas señalan quién gobernaba, nunca implican causalidad.

Primera serie: presión fiscal (atalaya/data/presion_fiscal.json). Pensado para añadir más
indicadores (PIB, paro, autónomos...) como nuevas entradas en MACROS, reutilizando el mismo
renderizador de gráfico y de bandas de gobierno.

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


def fecha_es(iso):
    d = datetime.fromisoformat(iso[:10])
    return f"{d.day} de {MESES[d.month - 1]} de {d.year}"


def J(p):
    return json.loads(Path(p).read_text(encoding="utf8"))


def nf(v):
    return f"{v:.1f}".replace(".", ",")


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
.grid{stroke:#e3e8ef;stroke-width:1}
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
.grid{stroke:#243044}.gband-label,.axis-label{fill:#8b97a8}
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


def grafico(serie_principal, serie_secundaria, gobiernos, anio_min, anio_max, y_max=40, y_paso=10):
    """SVG sin JS: línea principal (tinta) + línea secundaria (gris), bandas de gobierno de fondo."""
    W, H = 760, 320
    ML, MR, MT, MB = 42, 70, 14, 28
    PW, PH = W - ML - MR, H - MT - MB

    def x(anio):
        return ML + (anio - anio_min) / (anio_max - anio_min) * PW

    def y(val):
        return MT + PH - (val / y_max) * PH

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
    # cuadrícula horizontal + etiquetas eje Y
    v = 0
    while v <= y_max:
        yy = y(v)
        partes.append(f"<line class='grid' x1='{ML}' y1='{yy:.1f}' x2='{ML + PW}' y2='{yy:.1f}'/>")
        partes.append(f"<text class='axis-label' x='{ML - 6}' y='{yy + 4:.1f}' text-anchor='end'>{v}%</text>")
        v += y_paso
    # eje X: años cada 5
    anio = anio_min
    while anio <= anio_max:
        partes.append(f"<text class='axis-label' x='{x(anio):.1f}' y='{H - 8}' text-anchor='middle'>{anio}</text>")
        anio += 5

    def linea(serie, cls, grosor):
        anios = sorted(int(a) for a in serie["datos"])
        pts = " ".join(f"{x(a):.1f},{y(serie['datos'][str(a)]):.1f}" for a in anios)
        ult = anios[-1]
        xu, yu = x(ult), y(serie["datos"][str(ult)])
        titulo = f"<title>{ult}: {nf(serie['datos'][str(ult)])} % del PIB</title>"
        return (f"<polyline class='{cls}' fill='none' stroke-width='{grosor}' stroke-linejoin='round' stroke-linecap='round' points='{pts}'>{titulo}</polyline>"
                f"<circle cx='{xu:.1f}' cy='{yu:.1f}' r='6' class='ring'/>"
                f"<circle cx='{xu:.1f}' cy='{yu:.1f}' r='4' class='{cls} dot'/>"
                f"<text class='{cls} endlabel' x='{xu + 8:.1f}' y='{yu + 4:.1f}' font-size='13' font-weight='600'>{nf(serie['datos'][str(ult)])} %</text>")

    partes.append(linea(serie_secundaria, "ls-secundaria", 2))
    partes.append(linea(serie_principal, "ls-principal", 2.5))
    inner = "".join(partes)
    return f"<svg viewBox='0 0 {W} {H}' role='img' aria-label='Evolución de la presión fiscal en España, {anio_min}-{anio_max}'>{inner}</svg>"


def tabla_datos(datos_json, gobiernos):
    total, solo = datos_json["series"]["total"]["datos"], datos_json["series"]["soloImpuestos"]["datos"]
    anios = sorted(int(a) for a in total)

    def gobierno_de(a):
        for per in gobiernos["periodos"]:
            if per["desde"] <= a < (per["hasta"] or 9999):
                return per["presidente"]
        return "—"
    filas = "".join(
        f"<tr><td>{a}</td><td>{nf(total[str(a)])}</td><td>{nf(solo[str(a)])}</td><td>{E(gobierno_de(a))}</td></tr>"
        for a in anios)
    return (f"<details><summary>Ver los {len(anios)} años en tabla</summary>"
            "<table class='datos'><thead><tr><th>Año</th><th>Total (% PIB)</th><th>Solo impuestos (% PIB)</th><th>Presidente</th></tr></thead>"
            f"<tbody>{filas}</tbody></table></details>")


def main():
    pf = J(D / "presion_fiscal.json")
    gob = J(D / "gobiernos.json")
    total, solo = pf["series"]["total"]["datos"], pf["series"]["soloImpuestos"]["datos"]
    anios = sorted(int(a) for a in total)
    a0, a1 = anios[0], anios[-1]
    v0, v1 = total[str(a0)], total[str(a1)]
    minimo_anio = min(anios, key=lambda a: total[str(a)])
    resumen = (f"La presión fiscal total en España (impuestos y cotizaciones sociales, sobre el PIB) pasó del {nf(v0)} % en {a0} "
               f"al {nf(v1)} % en {a1}, con un mínimo del {nf(total[str(minimo_anio)])} % en {minimo_anio}, durante la crisis financiera.")
    titulo = "Presión fiscal en España: evolución desde 1995, con los gobiernos de cada periodo"
    h1 = f"¿Cómo ha evolucionado la presión fiscal en España desde {a0}?"
    desc = resumen
    chart = grafico(pf["series"]["total"], pf["series"]["soloImpuestos"], gob, a0, a1)
    leyenda_gob = " · ".join(f"<span><i style='background:{E(c)}'></i>{E(p)}</span>" for p, c in gob["colorPartido"].items())
    cuerpo = (f"<p class='meta'>Actualizado el {fecha_es(pf['actualizado'])}</p>"
              f"<p class='ans'>{E(resumen)}</p>"
              f"<p class='warn'>{E(pf['aviso'])}</p>"
              "<h2>Evolución desde 1995</h2>"
              "<div class='chart-wrap'>" + chart + "</div>"
              "<p class='leyenda'><span><i class='ls-principal'></i>Presión fiscal total (impuestos + cotizaciones sociales)</span>"
              "<span><i class='ls-secundaria'></i>Solo impuestos (sin cotizaciones sociales)</span></p>"
              f"<p class='meta'>Bandas de color: quién gobernaba en cada periodo — {leyenda_gob}. "
              "No implica que la presión fiscal dependa solo del partido en el Gobierno: el ciclo económico, las crisis y los pactos presupuestarios pesan tanto o más.</p>"
              + tabla_datos(pf, gob)
              + f"<p class='fu src'>Fuente: <a href='{E(pf['fuenteUrl'])}' rel='nofollow noopener'>{E(pf['fuente'])}</a>.</p>"
              "<h2>Para seguir profundizando</h2><ul>"
              "<li><a href='/macrodata-espana/'>MacroData España</a>: IPC, PIB, paro y otros indicadores económicos, actualizados cada mes.</li>"
              "<li><a href='/atalaya/fichas/politico/manueco/'>¿Qué prometió Mañueco en su investidura de 2022?</a>: promesas de bajadas de impuestos, contrastadas con hechos.</li>"
              "<li><a href='/atalaya/fichas/politico/ayuso/'>¿Qué prometió Ayuso en su investidura de 2023?</a>: lo mismo, en Madrid.</li>"
              "</ul>")
    faqs = [(f"¿Ha subido o bajado la presión fiscal en España desde {a0}?", resumen)]
    ld = [{"@context": "https://schema.org", "@type": "Article", "headline": titulo, "description": desc, "inLanguage": "es",
           "datePublished": pf["actualizado"], "dateModified": pf["actualizado"],
           "author": {"@type": "Person", "name": "Emilio Rodríguez García", "url": f"{BASE}/sobre-mi"},
           "publisher": {"@type": "Person", "name": "Emilio Rodríguez García"},
           "mainEntityOfPage": f"{BASE}/atalaya/fichas/macro/presion-fiscal/"},
          {"@context": "https://schema.org", "@type": "FAQPage",
           "mainEntity": [{"@type": "Question", "name": a, "acceptedAnswer": {"@type": "Answer", "text": b}} for a, b in faqs]},
          {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
              {"@type": "ListItem", "position": 1, "name": "Atalaya", "item": f"{BASE}/atalaya/"},
              {"@type": "ListItem", "position": 2, "name": "Fichas", "item": f"{BASE}/atalaya/fichas/"},
              {"@type": "ListItem", "position": 3, "name": "Presión fiscal", "item": f"{BASE}/atalaya/fichas/macro/presion-fiscal/"}]}]
    bc = "<a href='/atalaya/'>Atalaya</a> › <a href='/atalaya/fichas/'>Fichas</a> › Presión fiscal"
    pie = (f"Elaborado por <a href=\"https://emirodgar.es/sobre-mi\">Emilio Rodríguez García</a> con el panel <a href=\"/atalaya/\">Atalaya</a>. "
           f"Última actualización: {fecha_es(pf['actualizado'])}. Contenido basado en datos públicos citados en cada apartado; "
           "no es una opinión política. <a href=\"/atalaya/privacidad/\">Política de privacidad</a>.")
    url = pagina("macro/presion-fiscal/", titulo, desc, h1, cuerpo, ld, bc, pie)
    print("Publicado:", url)


if __name__ == "__main__":
    main()
