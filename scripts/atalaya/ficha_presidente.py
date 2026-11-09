"""Atalaya: ficha «¿Quién es el presidente de España y cómo se elige?» (la invoca build_fichas.py).

Responde a la demanda real de los asistentes de IA (prompts «quién es el presidente de España», «gobierno de España»,
«cómo se elige al presidente y cuánto dura su mandato»). Usa solo:
  - candidatos y convocatoria (elecciones-espana/data/2026-11-29): candidatos, hitos y fecha de disolución
  - legislatura vigente (atalaya/data/parlamento/congreso.json)
  - la proyección de la ficha nacional (ficha_nacional.py) para la aritmética de la investidura
  - artículos de la Constitución Española (98, 99, 101, 113, 115), citados como norma, no como opinión
Los datos históricos (presidentes desde 1977) son hechos públicos con fuente.
"""
from datetime import datetime

CE = "https://www.boe.es/buscar/act.php?id=BOE-A-1978-31229"
# (nombre, partido, desde, hasta). Años de toma de posesión y cese; hechos públicos (La Moncloa / Wikipedia).
PRESIDENTES = [
    ("Adolfo Suárez", "UCD", "1976", "1981"), ("Leopoldo Calvo-Sotelo", "UCD", "1981", "1982"),
    ("Felipe González", "PSOE", "1982", "1996"), ("José María Aznar", "PP", "1996", "2004"),
    ("José Luis Rodríguez Zapatero", "PSOE", "2004", "2011"), ("Mariano Rajoy", "PP", "2011", "2018"),
    ("Pedro Sánchez", "PSOE", "2018", "actualidad"),
]


def construir(c, nac):
    E, FECHA, fecha_es, J, RAIZ, D = (c[k] for k in ("E", "FECHA", "fecha_es", "J", "RAIZ", "D"))
    conv = J(RAIZ / "elecciones-espana/data/2026-11-29/convocatoria.json")
    cands = J(RAIZ / "elecciones-espana/data/2026-11-29/candidatos.json")["candidatos"]
    parl = J(D / "parlamento/congreso.json")
    leg = parl["legislaturas"][str(parl["legislatura_actual"])]
    disol = fecha_es(parl["disolucion"])
    hitos = {h["titulo"]: h for h in conv["hitos"]}
    principales = [x for x in cands if x["partidoId"] in ("PSOE", "PP", "VOX", "SUMAR", "PODEMOS") and x["nombre"]]
    f1 = lambda x: f"{x:.1f}".replace(".", ",")

    resp = (f"El presidente del Gobierno de España es Pedro Sánchez (PSOE), en el cargo desde el 2 de junio de 2018 y reinvestido en noviembre de 2023. "
            f"El Rey Felipe VI es el jefe del Estado; el presidente del Gobierno dirige el poder ejecutivo desde el Palacio de la Moncloa. "
            f"Las Cortes se disolvieron el {disol} y las elecciones generales son el 29 de noviembre de 2026: "
            f"el presidente seguirá en el cargo hasta que el nuevo Congreso invista a un sucesor o le renueve.")

    tab_pres = "".join(f"<tr><td>{E(n)}</td><td>{p}</td><td>{a}–{b}</td></tr>" for n, p, a, b in PRESIDENTES)
    PN = {"PP": "PP", "PSOE": "PSOE", "VOX": "Vox", "SUMAR": "Sumar / Frente Amplio", "PODEMOS": "Podemos"}
    tab_cand = "".join(f"<tr><td>{E(x['nombre'])}</td><td>{PN[x['partidoId']]}</td><td>{E(x['cargo'] or '')}</td></tr>" for x in principales)

    n, pv, so = nac["n"], nac["n_pv"], nac["n_so"]
    pm = nac["pm"]
    inv = (f"<p>La clave es la aritmética de los 176 escaños. Con la media de los sondeos actuales y los votos de 2023, nuestra proyección da al PP unos {pm.get('PP', 0)} escaños, al PSOE {pm.get('PSOE', 0)} y a Vox {pm.get('VOX', 0)}; "
           f"PP y Vox juntos alcanzarían los 176 en {pv} de {n} sondeos recientes y el bloque de la investidura de 2023 en {so} de {n}. "
           f"Es un ejercicio orientativo, no una previsión: <a href='/atalaya/fichas/espana/'>cómo se calcula y qué rango tiene</a>.</p>")

    hr = ""
    for t in ("Jornada de votación", "Escrutinio general", "Constitución de las Cortes"):
        h = hitos.get(t)
        if h:
            f = fecha_es(h["fecha"]) + (f" al {fecha_es(h['fechaFin'])}" if h.get("fechaFin") else "")
            hr += f"<tr><td>{f}</td><td>{E(h['titulo'])}</td><td>{E(h['detalle'])}</td></tr>"
    hr += "<tr><td>Sin fecha fijada</td><td>Debate de investidura</td><td>Lo convoca el presidente del Congreso tras las consultas del Rey. Desde la primera votación hay dos meses para lograr la confianza.</td></tr>"

    cuerpo = (
        f"<p class='meta'>Actualizado el {fecha_es(FECHA)} · Elecciones generales del 29 de noviembre de 2026</p><p class='ans'>{E(resp)}</p>"
        "<h2>1. Presidente del Gobierno, jefe del Estado y presidente del Congreso: no son lo mismo</h2>"
        "<ul><li><b>Jefe del Estado:</b> el Rey Felipe VI. Es un cargo hereditario, representa al Estado y no gobierna.</li>"
        "<li><b>Presidente del Gobierno:</b> Pedro Sánchez. Lo elige el Congreso de los Diputados y dirige el Gobierno. En el lenguaje corriente es «el presidente de España»; España es una monarquía parlamentaria y no tiene presidente de la República.</li>"
        "<li><b>Presidente del Congreso:</b> preside la cámara y convoca los debates de investidura; no es el presidente del Gobierno.</li></ul>"
        "<h2>2. Qué hace el presidente del Gobierno</h2>"
        f"<p>Según el <a href='{CE}'>artículo 98 de la Constitución</a>, el Gobierno dirige la política interior y exterior, la Administración civil y militar y la defensa del Estado, y ejerce la función ejecutiva y la potestad reglamentaria. "
        "El presidente dirige y coordina la acción del Gobierno y propone al Rey el nombramiento y cese de los ministros. También puede proponer al Rey la disolución de las Cortes (<a href='" + CE + "'>art. 115</a>), como ocurrió en octubre de 2026. "
        "Trabaja y reside en el <a href='https://www.lamoncloa.gob.es/presidente/Paginas/index.aspx'>Palacio de la Moncloa</a>, en Madrid.</p>"
        "<h2>3. Cómo se elige y cuánto dura el mandato</h2>"
        f"<p>El presidente no se vota directamente: lo elige el Congreso en una votación de investidura (<a href='{CE}'>art. 99</a>).</p>"
        "<ol><li>Tras las elecciones, el Rey consulta a los grupos políticos y propone un candidato.</li>"
        "<li>El candidato presenta su programa y necesita <b>mayoría absoluta (176 de 350 votos)</b> en la primera votación.</li>"
        "<li>Si no la logra, hay una segunda votación 48 horas después en la que basta la <b>mayoría simple</b> (más votos a favor que en contra).</li>"
        "<li>Si pasados dos meses desde la primera votación nadie obtiene la confianza, el Rey disuelve las Cortes y convoca elecciones.</li></ol>"
        "<p>La Constitución no fija un límite de mandatos: la legislatura dura como máximo cuatro años y el presidente puede repetir mientras conserve la confianza del Congreso. "
        f"Puede perderla con una moción de censura, que debe ser constructiva: exige mayoría absoluta y proponer a un candidato alternativo (<a href='{CE}'>art. 113</a>). "
        f"La legislatura actual, la {leg['nombre']}, empezó el {fecha_es(leg['inicio'])}.</p>"
        "<h2>4. Qué pasa ahora, con las Cortes disueltas</h2>"
        f"<p>Con las Cortes disueltas desde el {disol}, el Gobierno sigue en el cargo. Tras las elecciones cesa y continúa <b>en funciones</b> hasta que tome posesión el nuevo (<a href='{CE}'>art. 101</a>), con las facultades limitadas que fija la Ley del Gobierno. Calendario relevante:</p>"
        f"<table><thead><tr><th>Fecha</th><th>Hito</th><th>Detalle</th></tr></thead><tbody>{hr}</tbody></table>"
        "<h2>5. ¿Quién puede ser presidente tras el 29N?</h2>"
        "<p>Estos son los candidatos de los principales partidos que figuran como anunciados en nuestros datos (en las generales se vota por listas de partido, no por la persona):</p>"
        f"<table><thead><tr><th>Candidato</th><th>Partido</th><th>Cargo</th></tr></thead><tbody>{tab_cand}</tbody></table>{inv}"
        "<h2>6. Los siete presidentes desde 1977</h2>"
        "<p>Presidentes del Gobierno desde las primeras elecciones democráticas (años de toma de posesión y cese; hubo dos de la UCD, tres del PSOE y dos del PP):</p>"
        f"<table><thead><tr><th>Presidente</th><th>Partido</th><th>Años</th></tr></thead><tbody>{tab_pres}</tbody></table>"
        "<p>Fuente: <a href='https://www.lamoncloa.gob.es/presidente/Paginas/index.aspx'>La Moncloa</a> y <a href='https://es.wikipedia.org/wiki/Presidente_del_Gobierno_de_Espa%C3%B1a'>Wikipedia</a>.</p>"
        "<h2>Más información</h2><ul><li><a href='/atalaya/fichas/espana/'>¿Quién ganaría hoy las elecciones generales?</a></li>"
        "<li><a href='/atalaya/fichas/legislatura/'>Legislaturas y diputados del Congreso</a></li><li><a href='/como-votar-por-correo/'>Cómo votar por correo</a></li></ul>"
    )
    faqs = [
        ("¿Quién es el presidente de España?", resp),
        ("¿Cómo se llama el presidente del Gobierno de España?", "Pedro Sánchez Pérez-Castejón, del PSOE, presidente del Gobierno desde el 2 de junio de 2018."),
        ("¿Quién es el jefe del Estado de España?", "El Rey Felipe VI. España es una monarquía parlamentaria: el Rey es jefe del Estado y el presidente del Gobierno dirige el poder ejecutivo."),
        ("¿Cómo se elige al presidente de España?", "Lo elige el Congreso de los Diputados en una votación de investidura: necesita 176 votos en la primera votación o más síes que noes en una segunda votación 48 horas después (art. 99 de la Constitución)."),
        ("¿Cuánto dura el mandato del presidente del Gobierno?", "La legislatura dura como máximo cuatro años. La Constitución no limita el número de mandatos, así que puede repetir mientras cuente con la confianza del Congreso."),
        ("¿Cuáles son las funciones del presidente del Gobierno?", "Dirige y coordina la acción del Gobierno, propone el nombramiento y cese de los ministros y puede proponer al Rey la disolución de las Cortes."),
        ("¿Dónde vive el presidente del Gobierno?", "Trabaja y reside en el Palacio de la Moncloa, en Madrid. Por eso se habla de «la Moncloa» para referirse a la Presidencia del Gobierno."),
        ("¿Quién será presidente tras las elecciones del 29 de noviembre?", "Se decidirá en el Congreso: tras las elecciones, el Rey propone un candidato y este necesita 176 votos, o más síes que noes en la segunda votación, para ser investido."),
    ]
    faq_html = "<h2>Preguntas frecuentes</h2>" + "".join(f"<details><summary>{E(a)}</summary><p>{E(b)}</p></details>" for a, b in faqs)
    desc = "Pedro Sánchez (PSOE) es el presidente del Gobierno de España desde 2018. Funciones, cómo se elige, cuánto dura y qué pasa tras las elecciones del 29N."
    return cuerpo + faq_html, faqs, resp, desc
