"""Atalaya: ficha «¿Quién es el rey de España y qué papel tiene en las elecciones?» (la invoca build_fichas.py).

Motivo: en el CSV de prompts, «rey de España», «reyes de España», «rey de las Españas», «quién es el actual rey y cuáles son sus
funciones» suman unas 8 variantes con volumen 4.000. Los hechos de la Corona y la lista histórica son públicos (Casa Real,
Constitución, Wikipedia); el vínculo con las elecciones del 29N sale de convocatoria.json.
"""
CE = "https://www.boe.es/buscar/act.php?id=BOE-A-1978-31229"
CASA = "https://www.casareal.es/"
# (monarca, casa, años)
REYES = [("Felipe V", "Borbón", "1700–1746 (con un breve reinado de Luis I en 1724)"), ("Fernando VI", "Borbón", "1746–1759"), ("Carlos III", "Borbón", "1759–1788"),
         ("Carlos IV", "Borbón", "1788–1808"), ("José I Bonaparte", "Bonaparte", "1808–1813"), ("Fernando VII", "Borbón", "1808 y 1813–1833"),
         ("Isabel II", "Borbón", "1833–1868"), ("Amadeo I", "Saboya", "1870–1873"), ("Alfonso XII", "Borbón", "1874–1885"),
         ("Alfonso XIII", "Borbón", "1886–1931"), ("Juan Carlos I", "Borbón", "1975–2014"), ("Felipe VI", "Borbón", "2014–actualidad")]


def construir(c):
    E, FECHA, fecha_es, J, RAIZ = (c[k] for k in ("E", "FECHA", "fecha_es", "J", "RAIZ"))
    cv = J(RAIZ / "elecciones-espana/data/2026-11-29/convocatoria.json")
    hit = {h["titulo"]: h for h in cv["hitos"]}
    resp = ("El rey de España es Felipe VI, jefe del Estado desde el 19 de junio de 2014, cuando su padre, Juan Carlos I, abdicó. España es una monarquía parlamentaria: "
            "el Rey representa al Estado y ejerce funciones simbólicas y formales, pero no gobierna; el poder ejecutivo lo ejerce el presidente del Gobierno, que elige el Congreso. "
            f"En las elecciones del 29 de noviembre de 2026 el Rey tiene un papel concreto: tras el voto, consulta a los partidos y propone un candidato a la investidura.")
    tab = "".join(f"<tr><td>{E(n)}</td><td>{E(ca)}</td><td>{E(a)}</td></tr>" for n, ca, a in REYES)
    cuerpo = (
        f"<p class='meta'>Actualizado el {fecha_es(FECHA)} · Datos de la Constitución, la Casa Real y fuentes públicas</p><p class='ans'>{E(resp)}</p>"
        "<h2>1. La Familia Real hoy</h2>"
        "<ul><li><b>Felipe VI:</b> rey de España desde 2014. Nació en 1968 y es el hijo de Juan Carlos I.</li>"
        "<li><b>Letizia Ortiz:</b> reina consorte, casada con Felipe VI desde 2004.</li>"
        "<li><b>Leonor:</b> princesa de Asturias, heredera de la Corona. Nació en 2005.</li>"
        "<li><b>Sofía:</b> infanta, hermana de Leonor. Nació en 2007.</li>"
        "<li><b>Juan Carlos I:</b> rey emérito desde su abdicación en 2014; ya no ejerce funciones institucionales.</li></ul>"
        f"<p>Fuente oficial: <a href='{CASA}'>Casa de S. M. el Rey</a>.</p>"
        "<h2>2. Qué funciones tiene el Rey</h2>"
        f"<p>Según el <a href='{CE}'>artículo 56 de la Constitución</a>, el Rey es el jefe del Estado, símbolo de su unidad y permanencia, arbitra y modera el funcionamiento regular de las instituciones y asume la más alta representación del Estado en las relaciones internacionales. "
        f"El <a href='{CE}'>artículo 62</a> enumera sus funciones formales, entre ellas:</p>"
        "<ul><li>sancionar y promulgar las leyes;</li><li>convocar y disolver las Cortes y convocar elecciones, en los términos de la Constitución;</li>"
        "<li>proponer al candidato a presidente del Gobierno y nombrarlo tras la investidura;</li><li>nombrar y separar a los ministros a propuesta del presidente;</li>"
        "<li>ostentar el mando supremo de las Fuerzas Armadas.</li></ul>"
        f"<p>Todos sus actos necesitan el <b>refrendo</b> del presidente del Gobierno o de los ministros competentes (<a href='{CE}'>art. 64</a>), que son los responsables políticos. "
        "La persona del Rey es inviolable y no está sujeta a responsabilidad (art. 56.3). Por eso se dice que «reina, pero no gobierna».</p>"
        "<h2>3. El papel del Rey en las elecciones del 29 de noviembre de 2026</h2>"
        f"<p>El Real Decreto 806/2026 de disolución de las Cortes y convocatoria de elecciones se publicó en el BOE el {fecha_es(hit['Publicación en el BOE']['fecha'])}. Después de la votación, el Rey interviene así:</p>"
        f"<ol><li>El {fecha_es(hit['Constitución de las Cortes']['fecha'])} se constituyen las nuevas Cortes.</li>"
        "<li>El Rey consulta a los representantes de los grupos políticos con representación parlamentaria, a través del presidente del Congreso.</li>"
        "<li>Propone un candidato a presidente del Gobierno. Si el Congreso lo inviste (176 votos en la primera votación o más síes que noes en la segunda), el Rey lo nombra.</li>"
        "<li>Si en dos meses nadie logra la confianza, el Rey disuelve las Cortes y convoca nuevas elecciones.</li></ol>"
        "<p>Más detalle en <a href='/atalaya/fichas/presidente/'>quién es el presidente de España y cómo se elige</a> y en el <a href='/atalaya/fichas/calendario/'>calendario electoral</a>.</p>"
        "<h2>4. Los reyes de España desde 1700</h2>"
        "<p>Monarcas desde el cambio de dinastía a los Borbones. Entre 1931 y 1975 no hubo rey en ejercicio: fue el periodo de la Segunda República y de la dictadura de Franco, que designó a Juan Carlos de Borbón como sucesor.</p>"
        f"<table><thead><tr><th>Monarca</th><th>Casa</th><th>Reinado</th></tr></thead><tbody>{tab}</tbody></table>"
        "<p>Fuentes: <a href='https://es.wikipedia.org/wiki/Anexo:Monarcas_de_Espa%C3%B1a'>Wikipedia, «Anexo:Monarcas de España»</a>, <a href='" + CASA + "'>Casa Real</a> y la <a href='" + CE + "'>Constitución Española</a>.</p>"
        "<p class='warn'>Los datos de la Familia Real y los años de reinado son hechos públicos de elaboración propia, contrastables en las fuentes citadas. Esta ficha no valora a la Corona.</p>"
    )
    faqs = [
        ("¿Quién es el rey de España?", resp),
        ("¿Cómo se llaman los reyes de España?", "Felipe VI y Letizia Ortiz, esta última como reina consorte. Su hija mayor, Leonor, es la princesa de Asturias y heredera de la Corona."),
        ("¿Cuáles son las funciones del Rey de España?", "Es el jefe del Estado: sanciona y promulga las leyes, convoca y disuelve las Cortes, propone al candidato a presidente del Gobierno, nombra a los ministros y tiene el mando supremo de las Fuerzas Armadas. Todos sus actos necesitan refrendo del Gobierno."),
        ("¿El Rey gobierna España?", "No. España es una monarquía parlamentaria: el Rey reina pero no gobierna. El poder ejecutivo lo ejerce el presidente del Gobierno, elegido por el Congreso."),
        ("¿Quién fue el rey anterior a Felipe VI?", "Juan Carlos I, rey desde 1975 hasta su abdicación el 19 de junio de 2014, fecha en la que Felipe VI fue proclamado."),
        ("¿Quién será el próximo rey o reina de España?", "La heredera es Leonor, princesa de Asturias, hija primogénita de Felipe VI."),
        ("¿Qué papel tiene el Rey en las elecciones generales?", "No vota por ninguna opción ni interviene en la campaña. Convoca las elecciones a propuesta del presidente del Gobierno y, después, propone un candidato a la investidura tras consultar a los partidos."),
    ]
    faq_html = "<h2>Preguntas frecuentes</h2>" + "".join(f"<details><summary>{E(a)}</summary><p>{E(b)}</p></details>" for a, b in faqs)
    desc = "Felipe VI es el rey de España desde 2014. Familia Real, funciones según la Constitución, su papel en las elecciones del 29N y los reyes de España desde 1700."
    return cuerpo + faq_html, faqs, resp, desc
