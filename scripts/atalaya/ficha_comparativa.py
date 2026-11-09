"""Atalaya: ficha «¿Qué diferencias hay entre el PSOE y el PP?» (la invoca build_fichas.py).

Responde a prompts reales («qué diferencias hay entre el PSOE y el Partido Popular», «principales políticas de los partidos»).
Solo usa datos del repositorio: posiciones citadas con fuente (programas.json), encuestas y escaños (ficha nacional / partidos.json)
y resultados oficiales de 2023. No valora ni recomienda: muestra dónde coinciden y dónde discrepan, con la cita y su fuente.
"""
import math, re
from collections import Counter

POS = {"favor": "A favor", "contra": "En contra", "matizada": "Matizada", "sin_posicion": "Sin posición"}


def construir(c):
    E, FECHA, fecha_es, J, RAIZ, D, slug = (c[k] for k in ("E", "FECHA", "fecha_es", "J", "RAIZ", "D", "slug"))
    nacional, nsond, fsond = c["nacional"], c["nsond"], c["fsond"]
    prog = J(D / "programas.json"); afs = prog["afirmaciones"]
    pinfo = {x["id"]: x for x in J(RAIZ / "elecciones-espana/data/2026-11-29/partidos.json")["partidos"]}
    cand = {x["partidoId"]: x for x in J(RAIZ / "elecciones-espana/data/2026-11-29/candidatos.json")["candidatos"]}
    prov = J(D / "resultados/congreso-2023-07/circunscripciones.json")["prov"]
    seguro = lambda u: u if re.match(r"https?://", u or "") else "#"
    f1 = lambda x: f"{x:.1f}".replace(".", ",")
    A, B = "PSOE", "PP"

    def pos(a, k): return (a["posiciones"].get(k) or {})

    # clasificación de las afirmaciones
    grupos = {"opuestas": [], "coinciden": [], "matices": [], "sin": []}
    for a in afs:
        x, y = pos(a, A).get("posicion"), pos(a, B).get("posicion")
        if "sin_posicion" in (x, y) or not x or not y: grupos["sin"].append(a)
        elif x == y and x in ("favor", "contra"): grupos["coinciden"].append(a)
        elif x in ("favor", "contra") and y in ("favor", "contra"): grupos["opuestas"].append(a)
        else: grupos["matices"].append(a)
    N = len(afs)

    # resultados de 2023 por votos y provincias ganadas
    tot = sum(p["validos"] for p in prov.values())
    vp = {k: sum(p["v"].get(k, [0])[0] for p in prov.values()) for k in (A, B)}
    ep = {k: sum(p["v"].get(k, [0, 0])[1] for p in prov.values()) for k in (A, B)}
    gana = Counter()
    for p in prov.values():
        top = max(p["v"].items(), key=lambda kv: (kv[1][1], kv[1][0]))[0]
        gana[top] += 1

    nA, nB = pinfo[A]["nombre"], pinfo[B]["nombre"]
    temas = lambda g, n=4: ", ".join(list(dict.fromkeys(a["tema"].lower() for a in grupos[g]))[:n])
    t_op, t_co = temas("opuestas"), temas("coinciden", 3)
    resp = (f"El PSOE (centroizquierda) y el PP (centroderecha) son los dos grandes partidos de España y discrepan con claridad en {len(grupos['opuestas'])} de las {N} cuestiones analizadas "
            f"(temas como {t_op}), coinciden en {len(grupos['coinciden'])} ({t_co}) y en el resto sus posturas tienen matices o faltan datos. "
            f"En las encuestas, el PP lidera con un {f1(nacional[B])} % frente al {f1(nacional[A])} % del PSOE.")

    def celda(a, k):
        x = pos(a, k)
        if not x: return "<td>–</td>"
        fu = f" <a href='{E(seguro(x['fuente']))}' rel='nofollow noopener'>fuente</a>" if x.get("fuente") else ""
        return f"<td><span class='chip'>{POS.get(x['posicion'], x['posicion'])}</span><br><span class='meta'>{E(x.get('cita') or '')}{fu} {E(x.get('fecha') or '')}</span></td>"

    def tabla(lista):
        filas = "".join(f"<tr><td><a href='/atalaya/fichas/tema/{slug(a['tema'])}/'>{E(a['tema'])}</a>: {E(a['texto'])}</td>{celda(a, A)}{celda(a, B)}</tr>" for a in lista)
        return f"<table class='pos'><thead><tr><th>Cuestión</th><th>PSOE</th><th>PP</th></tr></thead><tbody>{filas}</tbody></table>"

    resumen = (f"<table><thead><tr><th></th><th>PSOE</th><th>PP</th></tr></thead><tbody>"
               f"<tr><td>Ideología (en nuestros datos)</td><td>{E(pinfo[A]['ideologia'])}</td><td>{E(pinfo[B]['ideologia'])}</td></tr>"
               f"<tr><td>Candidato anunciado 2026</td><td>{E(cand[A]['nombre'])}</td><td>{E(cand[B]['nombre'])}</td></tr>"
               f"<tr><td>Escaños en el Congreso disuelto</td><td>{pinfo[A]['escanosActuales']}</td><td>{pinfo[B]['escanosActuales']}</td></tr>"
               f"<tr><td>Media de encuestas (30 días)</td><td><b>{f1(nacional[A])} %</b></td><td><b>{f1(nacional[B])} %</b></td></tr>"
               f"<tr><td>Votos en julio de 2023</td><td>{f1(100 * vp[A] / tot)} %</td><td>{f1(100 * vp[B] / tot)} %</td></tr>"
               f"<tr><td>Escaños en 2023</td><td>{ep[A]}</td><td>{ep[B]}</td></tr>"
               f"<tr><td>Provincias en las que fue primero en escaños (2023)</td><td>{gana[A]}</td><td>{gana[B]}</td></tr>"
               f"<tr><td>Presidentes del Gobierno desde 1977</td><td>Felipe González (1982–96), José Luis Rodríguez Zapatero (2004–11), Pedro Sánchez (2018–)</td><td>José María Aznar (1996–2004), Mariano Rajoy (2011–18)</td></tr>"
               "</tbody></table>")

    cuerpo = (
        "<style>table.pos td,table.pos th{text-align:left;vertical-align:top}.chip{display:inline-block;padding:1px 8px;border-radius:10px;border:1px solid #d9e0ea;font-size:13px;white-space:nowrap}</style>"
        f"<p class='meta'>Actualizado el {fecha_es(FECHA)} · Elecciones generales del 29 de noviembre de 2026</p><p class='ans'>{E(resp)}</p>"
        f"<h2>1. Los dos partidos en cifras</h2><p>{E(nA)} y {E(nB)} se han alternado en el Gobierno desde 1982. Datos de encuestas ({nsond} sondeos hasta el {fecha_es(fsond)}, sin CIS), escaños y resultados oficiales.</p>{resumen}"
        "<p>Fuentes: <a href='/elecciones-espana/'>Elecciones en España</a>, <a href='https://infoelectoral.interior.gob.es/'>Ministerio del Interior</a> y <a href='https://www.lamoncloa.gob.es/presidente/Paginas/index.aspx'>La Moncloa</a>. "
        "Más sobre cada uno: <a href='/atalaya/fichas/partido/psoe/'>ficha del PSOE</a> y <a href='/atalaya/fichas/partido/pp/'>ficha del PP</a>.</p>"
        "<p class='warn'>Las posiciones proceden de programas anteriores, votaciones y declaraciones públicas recientes, cada una con su fuente. Los programas de 2026 aún no se han publicado y pueden cambiarlas. Atalaya no recomienda voto: solo muestra lo que cada partido ha dicho o votado.</p>"
        f"<h2>2. Dónde discrepan ({len(grupos['opuestas'])})</h2><p>Un partido a favor y el otro en contra:</p>{tabla(grupos['opuestas'])}"
        f"<h2>3. Dónde coinciden ({len(grupos['coinciden'])})</h2>{tabla(grupos['coinciden'])}"
        f"<h2>4. Posturas con matices ({len(grupos['matices'])})</h2><p>Al menos uno de los dos partidos tiene una posición matizada (apoya una parte, condiciona su apoyo o propone otra fórmula):</p>{tabla(grupos['matices'])}"
        + (f"<h2>5. Sin posición clara ({len(grupos['sin'])})</h2><p>Cuestiones en las que no hay evidencia suficiente para uno o ambos partidos: " + "; ".join(E(a["texto"]) for a in grupos["sin"]) + ".</p>" if grupos["sin"] else "")
        + "<h2>Por tema</h2><ul>" + "".join(f"<li><a href='/atalaya/fichas/tema/{slug(t)}/'>{E(t)}</a></li>" for t in sorted({a['tema'] for a in afs})) + "</ul>"
        "<h2>Qué no incluye</h2><p class='warn'>No es un test de voto ni una recomendación. Cada cuestión resume una sola pregunta y no equivale al programa completo de un partido. Si quieres comparar con tus propias ideas, usa el test <a href='/a-quien-votar/'>¿A quién votar?</a>.</p>"
    )
    faqs = [
        ("¿Qué diferencias hay entre el PSOE y el Partido Popular?", resp),
        ("¿El PSOE es de izquierdas y el PP de derechas?", "El PSOE se sitúa en el centroizquierda y el PP en el centroderecha según la clasificación usada en Atalaya. La ubicación exacta de cada cuestión depende del tema."),
        ("¿En qué temas están de acuerdo el PSOE y el PP?", "En los datos analizados coinciden en: " + "; ".join(a["texto"].rstrip(".").lower() for a in grupos["coinciden"]) + "."),
        ("¿En qué temas discrepan el PSOE y el PP?", "Discrepan en temas como " + t_op + ", por ejemplo: " + "; ".join(a["texto"].rstrip(".").lower() for a in grupos["opuestas"][:4]) + "."),
        ("¿Quién va ganando en las encuestas, el PSOE o el PP?", f"El PP, con una media del {f1(nacional[B])} % frente al {f1(nacional[A])} % del PSOE, sobre {nsond} sondeos de los últimos 30 días."),
        ("¿Cuántos escaños tiene cada uno?", f"En el Congreso disuelto el PP tiene {pinfo[B]['escanosActuales']} escaños y el PSOE {pinfo[A]['escanosActuales']}, resultado de las elecciones de julio de 2023."),
    ]
    faq_html = "<h2>Preguntas frecuentes</h2>" + "".join(f"<details><summary>{E(a)}</summary><p>{E(b)}</p></details>" for a, b in faqs)
    desc = f"PSOE y PP discrepan en {len(grupos['opuestas'])} de {N} cuestiones y coinciden en {len(grupos['coinciden'])}. Posiciones citadas con fuente, encuestas, escaños y resultados de 2023."
    return cuerpo + faq_html, faqs, resp, desc
