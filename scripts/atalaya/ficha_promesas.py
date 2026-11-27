"""Atalaya: fichas «¿Qué propone <partido> sobre <tema>?» (las invoca build_fichas.py tras fichas_tematicas).

  /atalaya/fichas/partido/<siglas>/<tema>/

Fuente única: atalaya/data/promesas.json (propuestas extraídas de los programas electorales, con página y cita literal).
Reglas de honestidad:
  - No se mide cumplimiento: todas las propuestas están «sin evidencia» y así se dice.
  - La extracción es automática: se enlaza el documento original para contrastar cada cita.
  - Programa 2026 primero; el anterior (2023) solo como contexto, rotulado como tal.
  - Frente Amplio 2026 se publica bajo Sumar (partidos.json lo nombra «Sumar / Frente Amplio»).
  - Sin página si hay menos de 3 propuestas del partido en el tema (evita fichas vacías); Vox queda con pocas por su programa breve.
"""
import re
from collections import Counter, defaultdict

# código de promesas.json -> siglas de partidos.json
PARTIDO = {"PP": "PP", "PSOE": "PSOE", "VOX": "Vox", "SUMAR": "Sumar", "FA": "Sumar"}
NOMBRE = {"PP": "Partido Popular", "PSOE": "PSOE", "Vox": "Vox", "Sumar": "Sumar / Frente Amplio"}
DOC = {"PP-2026": "programa del PP de 2026", "PSOE-2026": "programa del PSOE de 2026", "VOX-2026": "programa de Vox de 2026",
       "FA-2026": "programa de Frente Amplio (Sumar) de 2026", "PP-2023": "programa del PP de 2023", "PSOE-2023": "programa del PSOE de 2023",
       "SUMAR-2023": "programa de Sumar de 2023"}
MIN = 3
MAX_ACTUAL, MAX_PREVIO = 15, 6
CITA_MAX = 240


def indice(J, D):
    """{(siglas, tema): [promesas]} para los pares con al menos MIN propuestas (sin el tema «Otros»)."""
    idx = defaultdict(list)
    for p in J(D / "promesas.json")["promesas"]:
        sig = PARTIDO.get(p["partido"])
        if sig and p["tema"] != "Otros":
            idx[(sig, p["tema"])].append(p)
    return {k: v for k, v in idx.items() if len(v) >= MIN}


def _limpia(p):
    """Cita sin el sufijo « - Pág. N» (si existe, esa es la página impresa). Devuelve (cita, página)."""
    t = re.sub(r"\s+", " ", p.get("cita") or "").strip()
    pag = p["pagina"]
    m = re.search(r"\s*[-–]\s*P[áa]g\.?\s*(\d+)\s*$", t)
    if m:
        pag = int(m.group(1)); t = t[:m.start()].rstrip()
    return t, pag


def _corta(t, n=CITA_MAX):
    t = re.sub(r"\s+", " ", t or "").strip()
    return t if len(t) <= n else t[:n].rsplit(" ", 1)[0].rstrip(",;:") + "…"


def _orden(ps):
    """Medibles primero, luego por página del documento."""
    return sorted(ps, key=lambda p: (not p["medible"], p["pagina"] or 0))


def generar(c, idx=None):
    E, BASE, FECHA, fecha_es, slug, pagina, J, D = (c[k] for k in ("E", "BASE", "FECHA", "fecha_es", "slug", "pagina", "J", "D"))
    idx = idx or indice(J, D)
    temas_ficha = {slug(a["tema"]) for a in J(D / "programas.json")["afirmaciones"]}
    seguro = lambda u: u if re.match(r"https?://", u or "") else "#"
    urls = []

    def lista(ps, maximo):
        out = ""
        for p in _orden(ps)[:maximo]:
            cita, pag = _limpia(p)
            doc = f" <a href='{E(seguro(p['url_documento']))}' rel='nofollow noopener'>programa, p. {pag}</a>" if p.get("url_documento") else f" <span class='meta'>p. {pag}</span>"
            out += (f"<li><b>{E(p['enunciado'])}</b><br><span class='meta'>«{E(_corta(cita))}»{doc}"
                    + (" · propuesta concreta y medible" if p["medible"] else "") + "</span></li>")
        return f"<ul>{out}</ul>"

    por_partido = defaultdict(list)   # sig -> [(tema, ruta)]
    por_tema = defaultdict(list)      # tema -> [(sig, ruta)]
    for (sig, tema) in sorted(idx):
        ps = idx[(sig, tema)]
        actual = [p for p in ps if p["anio"] == 2026]
        previo = [p for p in ps if p["anio"] != 2026]
        ruta = f"partido/{slug(sig)}/{slug(tema)}/"
        por_partido[sig].append((tema, ruta)); por_tema[tema].append((sig, ruta))
        t_l = tema.lower()
        nmed = sum(1 for p in ps if p["medible"])
        if actual:
            resp = (f"El programa de 2026 de {NOMBRE[sig]} recoge {len(actual)} propuesta{'s' if len(actual) != 1 else ''} sobre {t_l}"
                    f"{' (' + str(sum(1 for p in actual if p['medible'])) + ' concretas y medibles)' if any(p['medible'] for p in actual) else ''}.")
            if previo: resp += f" Su programa anterior añade {len(previo)} más, como contexto."
        else:
            resp = f"No hay propuestas sobre {t_l} extraídas del programa de 2026 de {NOMBRE[sig]}; su programa anterior recoge {len(previo)}."
        resp += " Cada propuesta se publica con su cita y la página del documento original."
        # comparación con los demás partidos en el mismo tema
        comp = ""
        for s2 in sorted(NOMBRE):
            ps2 = idx.get((s2, tema))
            n26 = sum(1 for p in ps2 if p["anio"] == 2026) if ps2 else 0
            enlace = f"<a href='/atalaya/fichas/partido/{slug(s2)}/{slug(tema)}/'>{E(NOMBRE[s2])}</a>" if ps2 else E(NOMBRE[s2])
            comp += f"<tr><td>{enlace}</td><td>{n26 if ps2 else '–'}</td></tr>"
        cuerpo = (f"<p class='meta'>Actualizado el {fecha_es(FECHA)} · Elecciones generales del 29 de noviembre de 2026</p><p class='ans'>{E(resp)}</p>")
        if actual:
            cuerpo += (f"<h2>1. Propuestas del programa de 2026</h2><p>Se muestran {min(len(actual), MAX_ACTUAL)} de {len(actual)}, empezando por las concretas y medibles.</p>{lista(actual, MAX_ACTUAL)}")
        if previo:
            cuerpo += (f"<h2>{2 if actual else 1}. Programa anterior (2023), solo como contexto</h2><p>Estas propuestas son de un programa anterior y pueden haber cambiado. Se muestran {min(len(previo), MAX_PREVIO)} de {len(previo)}.</p>{lista(previo, MAX_PREVIO)}")
        cuerpo += (f"<h2>Cuántas propuestas tiene cada partido sobre {E(t_l)}</h2><p>Propuestas extraídas del programa de 2026 (un número mayor no significa más ambición: depende de cómo esté redactado el documento).</p>"
                   f"<table><thead><tr><th>Partido</th><th>Propuestas 2026</th></tr></thead><tbody>{comp}</tbody></table>")
        enl = f"<li><a href='/atalaya/fichas/partido/{slug(sig)}/'>Ficha de {E(NOMBRE[sig])}: encuestas, escaños y posiciones</a></li>"
        if slug(tema) in temas_ficha:
            enl += f"<li><a href='/atalaya/fichas/tema/{slug(tema)}/'>{E(tema)}: posición de cada partido</a></li>"
        cuerpo += (f"<h2>Más fichas</h2><ul>{enl}</ul>"
                   "<h2>Qué no incluye</h2><p class='warn'>Las propuestas se han extraído de forma automática de los programas y pueden contener errores de resumen: la cita y el enlace al documento permiten contrastarlas. "
                   "Esto no mide cumplimiento (ninguna tiene aún evidencia de ejecución), no valora si las propuestas son buenas o viables y no es una recomendación de voto.</p>")
        faqs = [(f"¿Qué propone {NOMBRE[sig]} sobre {t_l}?", resp),
                (f"¿Cuántas propuestas sobre {t_l} tiene {NOMBRE[sig]}?", f"{len(ps)} en total ({len(actual)} en su programa de 2026 y {len(previo)} en el anterior), de las que {nmed} son concretas y medibles."),
                (f"¿Se sabe si {NOMBRE[sig]} cumple sus propuestas sobre {t_l}?", "No: Atalaya aún no mide el cumplimiento. Todas las propuestas figuran como «sin evidencia» hasta que haya datos públicos que las contrasten.")]
        cuerpo += "<h2>Preguntas frecuentes</h2>" + "".join(f"<details><summary>{E(a)}</summary><p>{E(b)}</p></details>" for a, b in faqs)
        titulo = f"{NOMBRE[sig]} sobre {t_l}: propuestas del programa electoral (2026)"
        ld = [{"@context": "https://schema.org", "@type": "Article", "headline": f"¿Qué propone {NOMBRE[sig]} sobre {t_l}?", "description": resp, "inLanguage": "es", "datePublished": FECHA, "dateModified": FECHA,
               "author": {"@type": "Person", "name": "Emilio Rodríguez García", "url": f"{BASE}/sobre-mi"}, "publisher": {"@type": "Person", "name": "Emilio Rodríguez García"},
               "mainEntityOfPage": f"{BASE}/atalaya/fichas/{ruta}"},
              {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": a, "acceptedAnswer": {"@type": "Answer", "text": b}} for a, b in faqs]},
              {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                  {"@type": "ListItem", "position": 1, "name": "Atalaya", "item": f"{BASE}/atalaya/"},
                  {"@type": "ListItem", "position": 2, "name": "Fichas", "item": f"{BASE}/atalaya/fichas/"},
                  {"@type": "ListItem", "position": 3, "name": NOMBRE[sig], "item": f"{BASE}/atalaya/fichas/partido/{slug(sig)}/"},
                  {"@type": "ListItem", "position": 4, "name": tema, "item": f"{BASE}/atalaya/fichas/{ruta}"}]}]
        bc = f"<a href='/atalaya/'>Atalaya</a> › <a href='/atalaya/fichas/'>Fichas</a> › <a href='/atalaya/fichas/partido/{slug(sig)}/'>{E(sig)}</a> › {E(tema)}"
        pagina(ruta, titulo, resp[:155], f"¿Qué propone {NOMBRE[sig]} sobre {t_l}?", cuerpo, ld, bc)
        urls.append(f"{BASE}/atalaya/fichas/{ruta}")
    return urls, dict(por_partido), dict(por_tema)
