"""Atalaya: ficha «¿Cuándo son las elecciones generales y cómo se vota?» (la invoca build_fichas.py).

Responde a prompts reales: «cuándo son las próximas elecciones», «calendario electoral», «tipos de elecciones y cuándo ocurren»,
«¿es legal votar nulo y qué consecuencias tiene?». Usa solo:
  - convocatoria.json de la elección vigente (hitos, voto por correo, veda de encuestas, cámaras)
  - resultados oficiales de 2023 (Interior) para participación, votos en blanco y nulos
  - normas electorales citadas como norma (LOREG); sin opiniones
"""
from datetime import datetime

LOREG = "https://www.boe.es/buscar/act.php?id=BOE-A-1985-11672"


def construir(c):
    E, FECHA, fecha_es, J, RAIZ, D = (c[k] for k in ("E", "FECHA", "fecha_es", "J", "RAIZ", "D"))
    cv = J(RAIZ / "elecciones-espana/data/2026-11-29/convocatoria.json")
    prov = J(D / "resultados/congreso-2023-07/circunscripciones.json")["prov"]
    f1 = lambda x: f"{x:.1f}".replace(".", ",")
    nes = lambda x: f"{x:,}".replace(",", ".")
    dia = lambda iso: datetime.fromisoformat(iso).strftime("%A")
    DIAS = {"Monday": "lunes", "Tuesday": "martes", "Wednesday": "miércoles", "Thursday": "jueves", "Friday": "viernes", "Saturday": "sábado", "Sunday": "domingo"}
    fe = lambda iso: f"{DIAS[dia(iso)]} {fecha_es(iso)}"
    dias_faltan = (datetime.fromisoformat(cv["fecha"]) - datetime.fromisoformat(FECHA)).days
    vc = cv["votoPorCorreo"]; ve = cv["vedaEncuestas"]
    hit = {h["titulo"]: h for h in cv["hitos"]}
    camp = hit["Campaña electoral"]; sen = next(x for x in cv["camaras"] if x["id"] == "senado")

    # participación, blancos y nulos de julio de 2023 (suma de las 52 circunscripciones, datos de Interior)
    censo = sum(p["censo"] for p in prov.values()); vot = sum(p["votantes"] for p in prov.values())
    bl = sum(p["blanco"] for p in prov.values()); nu = sum(p["nulos"] for p in prov.values()); va = sum(p["validos"] for p in prov.values())
    top_nulo = sorted(prov.values(), key=lambda p: -p["nulos"] / p["votantes"])[:3]

    resp = (f"Las elecciones generales de España son el domingo 29 de noviembre de 2026, con los colegios abiertos de 9:00 a 20:00. "
            + (f"Faltan {dias_faltan} días desde el {fecha_es(FECHA)}. " if dias_faltan > 0 else "")
            + f"La campaña va del {fecha_es(camp['fecha'])} al {fecha_es(camp['fechaFin'])}, el 28 de noviembre es jornada de reflexión y el plazo para pedir el voto por correo termina el {fecha_es(vc['solicitudHasta'])}.")

    filas = ""
    for h in cv["hitos"]:
        f = fecha_es(h["fecha"]) + (f" al {fecha_es(h['fechaFin'])}" if h.get("fechaFin") else "")
        filas += f"<tr><td>{f}</td><td><b>{E(h['titulo'])}</b></td><td>{E(h['detalle'])}</td></tr>"
    tabla = f"<table class='cal'><thead><tr><th>Fecha</th><th>Hito</th><th>Detalle</th></tr></thead><tbody>{filas}</tbody></table>"

    cuerpo = (
        f"<p class='meta'>Actualizado el {fecha_es(FECHA)} · Fuente principal: Junta Electoral Central y Ministerio del Interior</p><p class='ans'>{E(resp)}</p>"
        "<style>table.cal td,table.cal th{text-align:left;vertical-align:top}table.cal td:first-child{white-space:nowrap}</style>"
        f"<h2>1. Calendario electoral completo</h2><p>{E(cv['resumen'])}</p>{tabla}"
        "<p>Fuentes: " + ", ".join(f"<a href='{E(f['url'])}' rel='nofollow noopener'>{E(f['titulo'])}</a>" for f in cv["fuentes"][:3]) + ".</p>"
        "<h2>2. Cómo votar el 29 de noviembre</h2>"
        "<h3>En persona</h3>"
        f"<p>Acude a tu colegio electoral (el de tu sección, indicado en la tarjeta censal o en la web del Ministerio) el {fecha_es(cv['fecha'])} entre las {cv['horarioVotacion'].replace(' a ', ' y las ')}. Lleva un documento que acredite tu identidad con foto: DNI, pasaporte o carnet de conducir. "
        "Dentro verás dos papeletas, una del Congreso y otra del Senado, cada una con su sobre. El portal oficial es <a href='" + cv["portalOficial"]["url"] + "'>" + E(cv["portalOficial"]["nombre"]) + "</a>.</p>"
        "<h3>Por correo</h3>"
        f"<p>Se puede pedir desde el {fecha_es(vc['solicitudDesde'])} hasta el {fecha_es(vc['solicitudHasta'])}. Recibirás la documentación entre el {fecha_es(vc['envioDesde'])} y el {fecha_es(vc['envioHasta'])} y debes entregar el voto en Correos como máximo el {fecha_es(vc['remisionHasta'])}. "
        "Si pides el voto por correo ya no puedes votar en persona. Los pasos, uno a uno, están en la <a href='/como-votar-por-correo/'>guía de voto por correo</a>.</p>"
        "<h3>Residentes en el extranjero</h3>"
        "<p>Quien está inscrito en el censo de residentes ausentes (CERA) tiene un procedimiento propio a través de los consulados. Consulta el <a href='https://www.exteriores.gob.es/'>Ministerio de Asuntos Exteriores</a>.</p>"
        "<h2>3. Qué se elige: Congreso y Senado</h2>"
        "<ul><li><b>Congreso de los Diputados:</b> 350 escaños, repartidos por provincias con la regla D'Hondt; la mayoría absoluta son 176. Se vota una lista cerrada de partido. Consulta cómo se reparten en <a href='/atalaya/fichas/'>cada provincia</a>.</li>"
        "<li><b>Senado:</b> 209 senadores de elección directa (más 58 designados por los parlamentos autonómicos). "
        "En cada provincia se reparten cuatro escaños y cada elector marca hasta tres nombres.</li></ul>"
        "<h2>4. Reglas de campaña y encuestas</h2>"
        f"<ul><li>La campaña dura {E(cv['duracionCampana'])} (del {fecha_es(camp['fecha'])} al {fecha_es(camp['fechaFin'])}).</li>"
        f"<li>El 28 de noviembre es la <b>jornada de reflexión</b>: no se puede hacer campaña ni pedir el voto.</li>"
        f"<li><b>Veda de encuestas:</b> del {fecha_es(ve['desde'])} al {fecha_es(ve['hasta'])} no se pueden publicar sondeos. {E(ve['nota'])} Hasta entonces, la <a href='/atalaya/fichas/espana/'>media de encuestas y la proyección de escaños</a> se actualizan en Atalaya.</li></ul>"
        "<h2>5. Voto nulo y voto en blanco: qué son y qué efecto tienen</h2>"
        f"<p>Votar nulo es legal y no tiene sanción ni consecuencia jurídica; simplemente no cuenta para ningún partido. Son diferentes:</p>"
        f"<ul><li><b>Voto en blanco:</b> un sobre vacío (o sin papeleta válida). Es un voto <i>válido</i>: cuenta en el total de votos válidos y, por tanto, sube la cifra que un partido necesita para superar la barrera del 3 % por circunscripción (<a href='{LOREG}'>LOREG</a>).</li>"
        "<li><b>Voto nulo:</b> sobre con una papeleta tachada o modificada, con dos papeletas de partidos distintos, con objetos o con papeletas de otra elección. No cuenta como voto válido ni para la barrera. "
        "Si un sobre lleva dos papeletas idénticas del mismo partido, se cuenta como un solo voto válido.</li></ul>"
        f"<p>En las elecciones de julio de 2023 votaron {nes(vot)} personas ({f1(100 * vot / censo)} % del censo): {nes(bl)} votos en blanco ({f1(100 * bl / va)} % de los votos válidos) y {nes(nu)} nulos ({f1(100 * nu / vot)} % de los votantes). "
        f"Los nulos fueron más frecuentes en " + ", ".join(f"{E(p['n'])} ({f1(100 * p['nulos'] / p['votantes'])} %)" for p in top_nulo) + ". "
        "Fuente: resultados oficiales del <a href='https://infoelectoral.interior.gob.es/'>Ministerio del Interior</a>.</p>"
        "<h2>6. Tipos de elecciones en España y cada cuánto se celebran</h2>"
        "<table><thead><tr><th>Elección</th><th>Qué se elige</th><th>Cada cuánto</th><th>Última celebrada</th></tr></thead><tbody>"
        "<tr><td>Generales</td><td>Congreso y Senado</td><td>4 años (o antes, si se disuelven las Cortes)</td><td>23 de julio de 2023</td></tr>"
        "<tr><td>Europeas</td><td>Eurodiputados</td><td>5 años</td><td>9 de junio de 2024</td></tr>"
        "<tr><td>Municipales</td><td>Concejales (y alcalde, de forma indirecta)</td><td>4 años (cuarto domingo de mayo)</td><td>28 de mayo de 2023</td></tr>"
        "<tr><td>Autonómicas</td><td>Parlamentos de las comunidades</td><td>4 años; en algunas comunidades, fecha propia</td><td>Varía según la comunidad</td></tr>"
        "</tbody></table><p>Las generales son las únicas que deciden quién gobierna España: <a href='/atalaya/fichas/presidente/'>cómo se elige al presidente del Gobierno</a>.</p>"
    )
    faqs = [
        ("¿Cuándo son las próximas elecciones generales en España?", resp),
        ("¿A qué hora se vota el 29 de noviembre?", "Los colegios electorales abren de 9:00 a 20:00."),
        ("¿Hasta cuándo se puede pedir el voto por correo?", f"Hasta el {fecha_es(vc['solicitudHasta'])}. La entrega del voto en Correos termina el {fecha_es(vc['remisionHasta'])}."),
        ("¿Qué documento hay que llevar para votar?", "Un documento oficial con foto que acredite la identidad: DNI, pasaporte o carnet de conducir."),
        ("¿Es legal votar nulo en España?", "Sí. Votar nulo es legal y no tiene sanción. El voto nulo no cuenta para ningún partido ni para el cálculo de la barrera del 3 %."),
        ("¿Cuál es la diferencia entre voto nulo y voto en blanco?", "El voto en blanco es un voto válido (sobre vacío) y cuenta en el total de votos válidos; el voto nulo, por papeleta alterada o de otra elección, no es válido."),
        ("¿Cuándo no se pueden publicar encuestas?", f"Desde el {fecha_es(ve['desde'])} hasta la votación: la ley electoral prohíbe difundir sondeos en los cinco días previos."),
        ("¿Qué es la jornada de reflexión?", "El día anterior a la votación (28 de noviembre de 2026), en el que no se puede hacer campaña ni pedir el voto."),
        ("¿Cuándo se constituyen las nuevas Cortes?", f"El {fecha_es(hit['Constitución de las Cortes']['fecha'])}. La investidura del presidente del Gobierno no tiene fecha fijada."),
    ]
    faq_html = "<h2>Preguntas frecuentes</h2>" + "".join(f"<details><summary>{E(a)}</summary><p>{E(b)}</p></details>" for a, b in faqs)
    desc = "Las elecciones generales son el 29 de noviembre de 2026 (9:00 a 20:00). Calendario completo, cómo votar en persona o por correo, voto nulo y en blanco."
    evento = {"@context": "https://schema.org", "@type": "Event", "name": "Elecciones generales de España 2026", "startDate": "2026-11-29T09:00:00+01:00", "endDate": "2026-11-29T20:00:00+01:00",
              "eventStatus": "https://schema.org/EventScheduled", "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
              "location": {"@type": "Country", "name": "España"}, "url": cv["portalOficial"]["url"]}
    return cuerpo + faq_html, faqs, resp, desc, evento
