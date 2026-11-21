#!/usr/bin/env python3
"""Atalaya: ficha "Discurso vs. Votos" para líderes políticos sin cargo ejecutivo (estática, indexable).

  /atalaya/fichas/politico/<slug>/   posiciones públicas contrastadas con el voto real de su grupo
                                      parlamentario en el Congreso, cada una con su fuente.

Se usa cuando el político no tiene, o no ha tenido, cargo ejecutivo que permita contrastar
promesas de gobierno con hechos (a diferencia de ficha_politico_autonomico.py). Datos curados
a mano en atalaya/data/discurso_votos.json: nunca se borra nada, solo se amplía.

Uso (raíz del repo): python3 scripts/atalaya/ficha_discurso_votos.py
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


CSS = """body{font:16px/1.6 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;max-width:820px;margin:0 auto;padding:24px 16px 64px;color:#1b2330;background:#fff}
h1{font-size:28px;line-height:1.2;margin:.2em 0 .4em}h2{font-size:21px;margin:1.6em 0 .4em;border-top:1px solid #e3e8ef;padding-top:1em}
h3{font-size:16px;margin:1.2em 0 .3em}
.ans{background:#eef6ff;border-left:4px solid #2563eb;padding:14px 16px;border-radius:6px;font-size:18px}
.meta,.src{color:#5b6778;font-size:14px}a{color:#1d4ed8}nav.bc{font-size:14px;color:#5b6778}
.warn{background:#fff8e6;border-left:4px solid #d99a00;padding:10px 14px;border-radius:6px;font-size:15px}
li{margin:.3em 0}main,h1{overflow-wrap:anywhere}
.caso{border:1px solid #e3e8ef;border-radius:8px;padding:14px 16px;margin:1em 0}
.cita{border-left:3px solid #94a3b8;padding:2px 14px;margin:.5em 0;font-style:italic;color:#334155}
.chip{display:inline-block;padding:2px 10px;border-radius:10px;border:1px solid;font-size:13px;font-weight:600;white-space:nowrap}
.chip.ok{background:#e6f7ee;border-color:#34d399;color:#065f46}
.chip.bad{background:#fdecec;border-color:#f87171;color:#7f1d1d}
.chip.mid{background:#fff8e6;border-color:#d99a00;color:#7a4b00}
.tema{font-family:ui-monospace,monospace;font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:#5b6778}
.fu{font-size:13px;margin-top:.4em}
@media (prefers-color-scheme:dark){body{background:#0e1219;color:#e5e9f0}h2,h3{border-color:#243044}.ans{background:#0f2036}
.meta,.src,.tema,nav.bc{color:#98a5b8}a{color:#7cb0ff}.warn{background:#2a2310}.caso{border-color:#273449}.cita{border-color:#475569;color:#cbd5e1}
.chip.ok{background:#07271d;border-color:#34d399;color:#6ee7b7}.chip.bad{background:#2a1212;border-color:#f87171;color:#fca5a5}.chip.mid{background:#2a2310;border-color:#d99a00;color:#fbbf24}}"""


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


def bloque_fuentes(fs):
    return " · ".join(f"<a href='{E(f['url'])}' rel='nofollow noopener'>{E(f['titulo'])}</a>" for f in fs)


def bloque_caso(c):
    p, v = c["posicion"], c["voto"]
    return (f"<div class='caso'><div class='tema'>{E(c['tema'])}</div>"
            f"<h3>¿Qué dice?</h3><blockquote class='cita'>«{E(p['cita'])}»</blockquote>"
            f"<p class='meta'>{E(p['autor'])}, {fecha_es(p['fecha'])}. {E(p['contexto'])}</p>"
            f"<p class='fu'>Fuentes:{bloque_fuentes(p['fuentes'])}</p>"
            f"<h3>¿Cómo vota Vox? <span class='chip {E(c['color'])}'>{E(c['etiqueta'])}</span></h3>"
            f"<p>{E(v['resultado'])}</p><p class='fu'>Fuentes:{bloque_fuentes(v['fuentes'])}</p>"
            f"<p>{E(c['analisis'])}</p></div>")


def main():
    data = J(D / "discurso_votos.json")
    for pol in data["politicos"]:
        casos = pol["casos"]
        n_coherente = sum(1 for c in casos if c["veredicto"] == "coherente")
        n_incoherente = sum(1 for c in casos if c["veredicto"] == "incoherente")
        n_resto = len(casos) - n_coherente - n_incoherente
        v = lambda n, s, p: f"{n} {s}" if n == 1 else f"{n} {p}"
        resumen = (f"De {len(casos)} asuntos en los que {pol['nombre'].split()[-1]} ha fijado una posición pública, "
                   f"en {v(n_coherente, 'caso', 'casos')} el voto de {E(pol['partido'])} en el Congreso coincide con lo que dice, "
                   f"en {v(n_incoherente, 'caso', 'casos')} el voto contradice o complica el discurso, y "
                   f"en {v(n_resto, 'caso', 'casos')} la imagen es mixta o falta un argumento de fondo claro.")
        titulo = f"{pol['nombre']}: lo que dice y cómo vota {pol['partido']} en el Congreso"
        h1 = f"¿Es coherente {pol['nombre'].split()[-1]} con los votos de {pol['partido']} en el Congreso?"
        desc = resumen
        enlaces = "".join(f"<li><a href='{E(e['url'])}'>{E(e['titulo'])}</a>: {E(e['desc'])}</li>" for e in pol.get("enlaces", []))
        nota = f"<p class='warn'>{E(pol['nota_contexto'])}</p>" if pol.get("nota_contexto") else ""
        cuerpo = (f"<p class='meta'>Actualizado el {fecha_es(pol['actualizado'])} · {E(pol['cargo'])}</p>"
                  f"<p class='ans'>{E(resumen)}</p>"
                  + nota +
                  "<p class='warn'>Metodología: cada posición pública lleva cita literal, autor, fecha y fuente; cada voto es el resultado oficial "
                  "de una votación en el Congreso de los Diputados, con su propia fuente. No es un balance exhaustivo de su trayectoria: "
                  "es una muestra representativa por tema, que se ampliará con el tiempo.</p>"
                  "<h2>Caso por caso</h2>"
                  + "".join(bloque_caso(c) for c in casos)
                  + "<h2>Para seguir profundizando</h2><ul>"
                  + enlaces
                  + f"<li><a href='{E(pol['wiki'])}'>Ficha de Wikipedia</a> de {E(pol['nombre'])}.</li>"
                  "</ul>")
        faqs = [(f"¿Es coherente {pol['nombre']} con cómo vota {pol['partido']} en el Congreso?", resumen)]
        ld = [{"@context": "https://schema.org", "@type": "Article", "headline": titulo, "description": desc, "inLanguage": "es",
               "datePublished": pol["actualizado"], "dateModified": pol["actualizado"],
               "author": {"@type": "Person", "name": "Emilio Rodríguez García", "url": f"{BASE}/sobre-mi"},
               "publisher": {"@type": "Person", "name": "Emilio Rodríguez García"},
               "mainEntityOfPage": f"{BASE}/atalaya/fichas/politico/{pol['slug']}/"},
              {"@context": "https://schema.org", "@type": "FAQPage",
               "mainEntity": [{"@type": "Question", "name": a, "acceptedAnswer": {"@type": "Answer", "text": b}} for a, b in faqs]},
              {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                  {"@type": "ListItem", "position": 1, "name": "Atalaya", "item": f"{BASE}/atalaya/"},
                  {"@type": "ListItem", "position": 2, "name": "Fichas", "item": f"{BASE}/atalaya/fichas/"},
                  {"@type": "ListItem", "position": 3, "name": pol["nombre"], "item": f"{BASE}/atalaya/fichas/politico/{pol['slug']}/"}]}]
        bc = f"<a href='/atalaya/'>Atalaya</a> › <a href='/atalaya/fichas/'>Fichas</a> › {E(pol['nombre'])}"
        pie = (f"Elaborado por <a href=\"https://emirodgar.es/sobre-mi\">Emilio Rodríguez García</a> con el panel <a href=\"/atalaya/\">Atalaya</a>. "
               f"Última actualización: {fecha_es(pol['actualizado'])}. Contenido basado en fuentes públicas citadas en cada apartado; "
               "no es una opinión política ni una recomendación de voto. <a href=\"/atalaya/privacidad/\">Política de privacidad</a>.")
        url = pagina(f"politico/{pol['slug']}/", titulo, desc, h1, cuerpo, ld, bc, pie)
        print("Publicado:", url)


if __name__ == "__main__":
    main()
