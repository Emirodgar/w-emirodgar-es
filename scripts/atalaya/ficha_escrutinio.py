"""Atalaya: ficha «¿Cuándo se conocen los resultados y cómo funciona el escrutinio?» (la invoca build_fichas.py).

Motivo: en el CSV de prompts, «escrutinio» (860), «¿cuándo se publicarán los resultados oficiales de las elecciones?» (718),
«resultados electorales y escrutinio en tiempo real» (8.005) y «cómo seguir los resultados en vivo». Usa los hitos de
convocatoria.json y los resultados oficiales de 2023 (Interior) para dar un ejemplo real de qué cambia entre noches.
"""
CE_LOREG = "https://www.boe.es/buscar/act.php?id=BOE-A-1985-11672"


def construir(c):
    E, FECHA, fecha_es, J, RAIZ, D = (c[k] for k in ("E", "FECHA", "fecha_es", "J", "RAIZ", "D"))
    cv = J(RAIZ / "elecciones-espana/data/2026-11-29/convocatoria.json")
    hit = {h["titulo"]: h for h in cv["hitos"]}
    esc = hit["Escrutinio general"]; vot = hit["Jornada de votación"]; cor = hit["Constitución de las Cortes"]
    ve = cv["vedaEncuestas"]
    prov = J(D / "resultados/congreso-2023-07/circunscripciones.json")["prov"]
    nes = lambda x: f"{x:,}".replace(",", ".")
    f1 = lambda x: f"{x:.1f}".replace(".", ",")
    censo = sum(p["censo"] for p in prov.values()); vots = sum(p["votantes"] for p in prov.values())
    top = {}
    for p in prov.values():
        for k, v in p["v"].items(): top[k] = top.get(k, 0) + v[0]
    val = sum(p["validos"] for p in prov.values())
    cuatro = ", ".join(f"{k} {f1(100 * top[k] / val)} %" for k in ("PP", "PSOE", "VOX", "SUMAR"))
    resp = (f"Los primeros datos se conocen la noche del domingo 29 de noviembre de 2026, nada más cerrar los colegios a las 20:00, y son provisionales. "
            f"Los resultados oficiales llegan con el escrutinio general que hacen las Juntas Electorales Provinciales, del {fecha_es(esc['fecha'])} al {fecha_es(esc['fechaFin'])}, "
            f"y la composición definitiva del Congreso se conoce cuando se proclaman los electos y se constituyen las Cortes el {fecha_es(cor['fecha'])}.")
    filas = (
        f"<tr><td>Domingo {fecha_es(vot['fecha'])}, 20:00</td><td>Cierre de los colegios y escrutinio en cada mesa</td><td>Cada mesa abre las urnas, cuenta las papeletas en voz alta y levanta el acta. Es un recuento público.</td></tr>"
        "<tr><td>Noche electoral</td><td>Avance de resultados provisionales</td><td>El Ministerio del Interior consolida las actas de las mesas y publica el avance. No es el resultado oficial: faltan, por ejemplo, el voto por correo y desde el extranjero.</td></tr>"
        f"<tr><td>{fecha_es(esc['fecha'])} al {fecha_es(esc['fechaFin'])}</td><td>Escrutinio general</td><td>{E(esc['detalle'])} Aquí se suman los votos por correo y los de los residentes en el extranjero (CERA).</td></tr>"
        "<tr><td>Después del escrutinio</td><td>Proclamación de electos</td><td>Las Juntas Electorales proclaman a los diputados y senadores electos, y la Junta Electoral Central lo publica en el BOE. Cabe recurso ante los tribunales.</td></tr>"
        f"<tr><td>{fecha_es(cor['fecha'])}</td><td>Constitución de las Cortes</td><td>{E(cor['detalle'])}</td></tr>"
    )
    cuerpo = (
        f"<p class='meta'>Actualizado el {fecha_es(FECHA)} · Fuente: calendario de la Junta Electoral Central y Ministerio del Interior</p><p class='ans'>{E(resp)}</p>"
        "<style>table.cal td,table.cal th{text-align:left;vertical-align:top}</style>"
        "<h2>1. Del cierre de los colegios a los resultados oficiales</h2>"
        f"<table class='cal'><thead><tr><th>Cuándo</th><th>Qué ocurre</th><th>Detalle</th></tr></thead><tbody>{filas}</tbody></table>"
        "<h2>2. Qué es el escrutinio</h2>"
        "<p>Es el recuento de los votos. Hay dos fases:</p>"
        "<ul><li><b>Escrutinio en la mesa electoral:</b> se hace el mismo domingo, en cada colegio, delante de interventores y público. De aquí sale el avance provisional.</li>"
        f"<li><b>Escrutinio general:</b> lo hace cada Junta Electoral Provincial a partir de las actas, resuelve las reclamaciones y suma el voto por correo y el voto exterior. Es el que da el resultado oficial (<a href='{CE_LOREG}'>LOREG</a>).</li></ul>"
        "<h2>3. Cómo seguir los resultados el 29N</h2>"
        f"<p>El Ministerio del Interior publica los resultados en su portal oficial, <a href='{cv['portalOficial']['url']}'>{E(cv['portalOficial']['nombre'])}</a>, con el avance provisional la noche electoral. "
        f"Los resultados oficiales se archivan en <a href='https://infoelectoral.interior.gob.es/'>Infoelectoral</a>. Atalaya incorporará los resultados de 2026 a las <a href='/atalaya/fichas/'>fichas por provincia</a> cuando sean oficiales.</p>"
        f"<p>Recuerda que los sondeos no pueden publicarse del {fecha_es(ve['desde'])} hasta el cierre de los colegios. Hasta entonces, la <a href='/atalaya/fichas/espana/'>media de encuestas y la proyección de escaños</a> sigue disponible.</p>"
        "<h2>4. Por qué el dato provisional puede cambiar</h2>"
        "<p>El avance de la noche electoral cuenta las actas de las mesas, pero no incluye todavía el voto por correo ni los votos del extranjero, y puede haber reclamaciones. "
        "Esos votos pueden mover votos y, en circunscripciones con escaños muy ajustados, incluso el último escaño: es la razón por la que se habla de resultado provisional hasta el escrutinio general.</p>"
        f"<h2>5. Un ejemplo: las elecciones de julio de 2023</h2><p>En 2023 votaron {nes(vots)} personas de un censo de {nes(censo)} ({f1(100 * vots / censo)} %). Reparto final de los votos válidos: {cuatro}. "
        "Fuente: resultados oficiales del <a href='https://infoelectoral.interior.gob.es/'>Ministerio del Interior</a>. Cómo se convierten esos votos en escaños: <a href='/atalaya/fichas/circunscripciones/'>circunscripciones y reparto D'Hondt</a>.</p>"
    )
    faqs = [
        ("¿Cuándo se conocen los resultados de las elecciones generales?", resp),
        ("¿A qué hora empieza el recuento de votos?", "Al cerrar los colegios electorales, a las 20:00 del domingo 29 de noviembre de 2026. Cada mesa cuenta sus papeletas en público."),
        ("¿Qué es el escrutinio?", "El recuento de los votos. Primero se hace en cada mesa electoral y después, de forma oficial, en el escrutinio general de las Juntas Electorales Provinciales."),
        ("¿Cuándo es el escrutinio general?", f"Del {fecha_es(esc['fecha'])} al {fecha_es(esc['fechaFin'])}, según el calendario de la Junta Electoral Central."),
        ("¿Son definitivos los resultados de la noche electoral?", "No. Son un avance provisional. Los oficiales llegan con el escrutinio general, que incorpora el voto por correo y el voto exterior."),
        ("¿Cuándo se constituyen las nuevas Cortes?", f"El {fecha_es(cor['fecha'])}. La investidura del presidente no tiene fecha fijada."),
    ]
    faq_html = "<h2>Preguntas frecuentes</h2>" + "".join(f"<details><summary>{E(a)}</summary><p>{E(b)}</p></details>" for a, b in faqs)
    desc = "Los primeros resultados llegan la noche del 29N y son provisionales; el escrutinio general oficial es del 4 al 7 de diciembre. Calendario y cómo seguir el recuento."
    return cuerpo + faq_html, faqs, resp, desc
