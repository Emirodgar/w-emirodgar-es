"""Atalaya: English page «Who is the Prime Minister of Spain?» (la invoca build_fichas.py).

Motivo: en el CSV de prompts, las búsquedas en inglés sobre quién lidera España («who is the prime minister of Spain»,
«president of Spain», «does Spain have a president», «Spanish parliament») suman más de 21.000 de volumen por variante
y ninguna ficha de Atalaya estaba en inglés. Contenido equivalente a la ficha en español, con las mismas fuentes y datos.
"""
from datetime import datetime

CE = "https://www.boe.es/buscar/act.php?id=BOE-A-1978-31229"
MOY = "https://www.lamoncloa.gob.es/presidente/Paginas/index.aspx"
PM = [("Adolfo Suárez", "UCD", "1976–1981"), ("Leopoldo Calvo-Sotelo", "UCD", "1981–1982"), ("Felipe González", "PSOE", "1982–1996"),
      ("José María Aznar", "PP", "1996–2004"), ("José Luis Rodríguez Zapatero", "PSOE", "2004–2011"), ("Mariano Rajoy", "PP", "2011–2018"),
      ("Pedro Sánchez", "PSOE", "2018–present")]


def construir(c, nac):
    E, FECHA, J, RAIZ, D = (c[k] for k in ("E", "FECHA", "J", "RAIZ", "D"))
    cv = J(RAIZ / "elecciones-espana/data/2026-11-29/convocatoria.json")
    cands = J(RAIZ / "elecciones-espana/data/2026-11-29/candidatos.json")["candidatos"]
    parl = J(D / "parlamento/congreso.json")
    MES = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    fe = lambda iso: (lambda d: f"{MES[d.month - 1]} {d.day}, {d.year}")(datetime.fromisoformat(iso[:10]))
    hit = {h["titulo"]: h for h in cv["hitos"]}
    sen = next(x for x in cv["camaras"] if x["id"] == "senado")
    PN = {"PP": "PP (People's Party)", "PSOE": "PSOE (Socialist Party)", "VOX": "Vox", "SUMAR": "Sumar / Frente Amplio", "PODEMOS": "Podemos"}
    principales = [x for x in cands if x["partidoId"] in PN and x["nombre"]]
    tab_c = "".join(f"<tr><td>{E(x['nombre'])}</td><td>{PN[x['partidoId']]}</td></tr>" for x in principales)
    tab_pm = "".join(f"<tr><td>{E(n)}</td><td>{p}</td><td>{a}</td></tr>" for n, p, a in PM)
    pm, n, pv, so = nac["pm"], nac["n"], nac["n_pv"], nac["n_so"]
    disol = fe(parl["disolucion"])

    resp = (f"The Prime Minister of Spain is Pedro Sánchez, of the Socialist Party (PSOE), in office since June 2, 2018. Spain does not have a president in the usual sense: "
            f"the head of government is formally called the \"President of the Government\" (Presidente del Gobierno) and is commonly translated as Prime Minister, "
            f"while King Felipe VI is the head of state. Parliament was dissolved on {disol} and a general election is held on {fe(cv['fecha'])}, "
            f"so Sánchez stays in office until the new Congress elects a successor or reinstates him.")

    cuerpo = (
        f"<p class='meta'>Updated {fe(FECHA)} · General election: {fe(cv['fecha'])} · <a href='/atalaya/fichas/presidente/'>Versión en español</a></p><p class='ans'>{E(resp)}</p>"
        "<h2>1. Prime Minister, president and king: who is who</h2>"
        "<ul><li><b>Prime Minister (head of government):</b> Pedro Sánchez. Officially the \"President of the Government\"; he leads the executive from the Moncloa Palace in Madrid. This is who people usually mean by \"the president of Spain\".</li>"
        "<li><b>Head of state:</b> King Felipe VI. Spain is a parliamentary monarchy: the King represents the state but does not govern.</li>"
        "<li><b>President of the Congress of Deputies:</b> presides over the lower house and schedules the investiture debate. This is a different post.</li></ul>"
        "<h2>2. How the Prime Minister is chosen and how long the term lasts</h2>"
        f"<p>Voters do not elect the Prime Minister directly. After a general election, the King consults the parties and proposes a candidate, who must win an investiture vote in the Congress of Deputies (<a href='{CE}'>Article 99 of the Constitution</a>):</p>"
        "<ol><li>The candidate needs an <b>absolute majority (176 of 350 votes)</b> in the first vote.</li>"
        "<li>If that fails, a second vote is held 48 hours later and a <b>simple majority</b> (more votes in favour than against) is enough.</li>"
        "<li>If no candidate wins the Congress's confidence within two months of the first vote, the King dissolves Parliament and calls a new election.</li></ol>"
        f"<p>A legislature lasts at most four years and the Constitution sets no term limit, so a Prime Minister can serve as long as the Congress keeps its confidence. "
        f"It can be withdrawn through a constructive vote of no confidence, which needs an absolute majority and an alternative candidate (<a href='{CE}'>Article 113</a>).</p>"
        "<h2>3. What the Prime Minister does</h2>"
        f"<p>Under <a href='{CE}'>Article 98</a>, the Government directs domestic and foreign policy, the civil and military administration and the defence of the State. The Prime Minister leads and coordinates the Government, "
        f"proposes the appointment and dismissal of ministers to the King, and can propose the dissolution of Parliament (Article 115), as happened in October 2026. Official residence and workplace: <a href='{MOY}'>La Moncloa</a>.</p>"
        "<h2>4. What happens now: the general election of November 29, 2026</h2>"
        f"<p>The election was announced on {fe(hit['Anuncio de la convocatoria']['fecha'])} and Parliament was dissolved on {disol}. The Government remains in office; after the election it becomes a caretaker government until the new one takes office (<a href='{CE}'>Article 101</a>).</p>"
        "<table><thead><tr><th>Date</th><th>Milestone</th></tr></thead><tbody>"
        f"<tr><td>{fe('2026-11-13')} – {fe('2026-11-27')}</td><td>Election campaign</td></tr>"
        f"<tr><td>{fe(hit['Jornada de votación']['fecha'])}</td><td>Election day, polling stations open 9:00 to 20:00</td></tr>"
        f"<tr><td>{fe('2026-12-04')} – {fe('2026-12-07')}</td><td>Official count and proclamation of elected members</td></tr>"
        f"<tr><td>{fe(hit['Constitución de las Cortes']['fecha'])}</td><td>New Parliament convenes</td></tr>"
        "<tr><td>No fixed date</td><td>Investiture debate; the two-month clock starts at the first vote</td></tr></tbody></table>"
        "<h2>5. Who could be Prime Minister after the election</h2>"
        "<p>Candidates of the main parties, as announced in our data (voters choose party lists, not individuals):</p>"
        f"<table><thead><tr><th>Candidate</th><th>Party</th></tr></thead><tbody>{tab_c}</tbody></table>"
        f"<p>The decisive number is 176 seats. Projecting the current poll average onto the 2023 results, we estimate about {pm.get('PP', 0)} seats for the PP, {pm.get('PSOE', 0)} for the PSOE and {pm.get('VOX', 0)} for Vox; "
        f"the PP and Vox together would reach 176 in {pv} of {n} recent polls, and the bloc that backed the 2023 investiture in {so} of {n}. "
        "This is an indicative exercise, not a forecast: <a href='/atalaya/fichas/espana/'>method and range (in Spanish)</a>.</p>"
        "<h2>6. The Spanish Parliament</h2>"
        "<p>Parliament is called the <i>Cortes Generales</i> and has two chambers: the <b>Congress of Deputies</b> (350 members, who elect the Prime Minister) and the <b>Senate</b> "
        f"({sen['escanos']} directly elected senators plus 58 appointed by regional parliaments). Congress seats are allocated across <a href='/atalaya/fichas/circunscripciones/'>52 constituencies</a> using the D'Hondt rule.</p>"
        "<h2>7. Prime Ministers of Spain since 1977</h2>"
        f"<table><thead><tr><th>Prime Minister</th><th>Party</th><th>Years</th></tr></thead><tbody>{tab_pm}</tbody></table>"
        f"<p>Sources: <a href='{MOY}'>La Moncloa</a>, <a href='https://en.wikipedia.org/wiki/Prime_Minister_of_Spain'>Wikipedia</a>, <a href='{CE}'>Spanish Constitution</a>, <a href='https://29neleccionesgenerales.es'>29neleccionesgenerales.es</a> (Ministry of the Interior).</p>"
    )
    faqs = [
        ("Who is the Prime Minister of Spain?", resp),
        ("Does Spain have a president?", "Not in the usual sense. Spain is a parliamentary monarchy: the head of state is King Felipe VI and the head of government is officially called the President of the Government, usually translated as Prime Minister. That is Pedro Sánchez."),
        ("Who is the head of state of Spain?", "King Felipe VI. The monarchy is hereditary and ceremonial; the King does not govern."),
        ("Who is the leader of Spain?", "Pedro Sánchez leads the Government as Prime Minister. King Felipe VI is the head of state."),
        ("How is the Prime Minister of Spain chosen?", "The Congress of Deputies elects the Prime Minister in an investiture vote: 176 votes in the first round, or more votes for than against in a second round 48 hours later (Article 99 of the Constitution)."),
        ("How long is the Prime Minister's term?", "A legislature lasts up to four years. The Constitution sets no term limit, so a Prime Minister can be reinstated while keeping the Congress's confidence."),
        ("When is the next general election in Spain?", f"{fe(cv['fecha'])}, with polling stations open from 9:00 to 20:00."),
        ("What is La Moncloa?", "The Moncloa Palace in Madrid, the official residence and workplace of the Prime Minister. In the press, \"La Moncloa\" also means the Prime Minister's office."),
        ("What is the Spanish Parliament called?", "The Cortes Generales. It has two chambers: the Congress of Deputies (350 members) and the Senate."),
    ]
    faq_html = "<h2>Frequently asked questions</h2>" + "".join(f"<details><summary>{E(a)}</summary><p>{E(b)}</p></details>" for a, b in faqs)
    desc = "Pedro Sánchez (PSOE) is Spain's Prime Minister since 2018. How the PM is chosen, the term, the Spanish Parliament and what happens after the November 29, 2026 election."
    pie = f"By <a href='https://emirodgar.es/sobre-mi'>Emilio Rodríguez García</a> with the <a href='/atalaya/'>Atalaya</a> panel. Last updated: {fe(FECHA)}. Based on public data cited in each section; not an official forecast. <a href='/atalaya/privacidad/'>Privacy policy</a>."
    return cuerpo + faq_html, faqs, resp, desc, pie
