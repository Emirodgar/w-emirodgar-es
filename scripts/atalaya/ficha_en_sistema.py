"""Atalaya: English page «How does Spain's political system work? Main parties» (la invoca build_fichas.py).

Motivo: en el CSV de prompts, «what are the main political parties in Spain?» (5.386), «what are the main parties competing in the
upcoming Spain election?» (6.215), «how is the political system structured in Spain?» (5.386), «can you explain the political structure
of Spain?» (5.422). Usa partidos.json, candidatos.json, la media de encuestas de la ficha nacional y datos de la convocatoria.
"""
CE = "https://www.boe.es/buscar/act.php?id=BOE-A-1978-31229"
IDEO = {"Centroderecha": "Centre-right", "Centroizquierda": "Centre-left", "Derecha nacionalista": "Nationalist right", "Izquierda": "Left",
        "Independentista de izquierdas": "Left-wing, Catalan independence", "Independentista de centroderecha": "Centre-right, Catalan independence",
        "Izquierda independentista": "Left-wing, Basque independence", "Nacionalismo vasco de centro": "Centrist Basque nationalism",
        "Valencianismo de izquierdas": "Left-wing Valencian regionalism", "Nacionalismo gallego de izquierdas": "Left-wing Galician nationalism",
        "Nacionalismo canario de centro": "Centrist Canarian nationalism", "Regionalismo navarro de centroderecha": "Centre-right Navarrese regionalism",
        "Populismo antisistema": "Anti-establishment populism"}
NOMBRE = {"PP": "People's Party (Partido Popular)", "PSOE": "Spanish Socialist Workers' Party (PSOE)", "VOX": "Vox", "SUMAR": "Sumar / Frente Amplio",
          "ERC": "Republican Left of Catalonia (ERC)", "JUNTS": "Together for Catalonia (Junts)", "BILDU": "EH Bildu", "PNV": "Basque Nationalist Party (PNV)",
          "PODEMOS": "Podemos", "COMPROMIS": "Compromís", "BNG": "Galician Nationalist Bloc (BNG)", "CC": "Canarian Coalition (CC)", "UPN": "Navarrese People's Union (UPN)",
          "SALF": "Se Acabó La Fiesta (SALF)"}
MES = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def construir(c, nacional, nsond):
    E, FECHA, J, RAIZ, D = (c[k] for k in ("E", "FECHA", "J", "RAIZ", "D"))
    from datetime import datetime
    fe = lambda iso: (lambda d: f"{MES[d.month - 1]} {d.day}, {d.year}")(datetime.fromisoformat(iso[:10]))
    f1 = lambda x: f"{x:.1f}"
    partidos = J(RAIZ / "elecciones-espana/data/2026-11-29/partidos.json")["partidos"]
    cands = {x["partidoId"]: x for x in J(RAIZ / "elecciones-espana/data/2026-11-29/candidatos.json")["candidatos"]}
    cv = J(RAIZ / "elecciones-espana/data/2026-11-29/convocatoria.json")
    filas = ""
    for p in partidos:
        i = p["id"]; cd = (cands.get(i) or {}).get("nombre") or "to be announced"
        k_ = {"VOX": "Vox", "SUMAR": "Sumar", "PODEMOS": "Podemos"}.get(i, i)
        enc = f"{f1(nacional[k_])} %" if k_ in nacional else "–"
        filas += f"<tr><td>{E(NOMBRE.get(i, p['nombre']))}</td><td>{E(IDEO.get(p['ideologia'], p['ideologia']))}</td><td>{'National' if p['ambito'] == 'estatal' else 'Regional'}</td><td>{p['escanosActuales']}</td><td>{enc}</td><td>{E(cd)}</td></tr>"
    top = sorted([i for i in nacional], key=lambda k: -nacional[k])
    lid, seg = top[0], top[1]
    resp = ("Spain is a parliamentary monarchy: King Felipe VI is the head of state, a two-chamber Parliament (the Cortes Generales) makes the laws, and a Government led by the Prime Minister runs the executive. "
            f"Four national parties dominate: the centre-right People's Party (PP), the centre-left Socialist Party (PSOE), the nationalist right Vox and the left-wing Sumar, "
            f"plus regional parties from Catalonia, the Basque Country, Galicia and other regions that matter in pacts. "
            f"For the general election on {fe(cv['fecha'])}, the poll average puts the {lid} first at {f1(nacional[lid])} %, ahead of the {seg} at {f1(nacional[seg])} %.")
    cuerpo = (
        f"<p class='meta'>Updated {fe(FECHA)} · General election: {fe(cv['fecha'])} · <a href='/atalaya/fichas/comparar/psoe-pp/'>Más en español</a></p><p class='ans'>{E(resp)}</p>"
        "<h2>1. How Spain's political system is structured</h2>"
        f"<ul><li><b>Form of State:</b> a parliamentary monarchy under the <a href='{CE}'>1978 Constitution</a>. The King is head of state but does not govern.</li>"
        "<li><b>Parliament (<i>Cortes Generales</i>):</b> the Congress of Deputies (350 members) and the Senate. The Congress elects the Prime Minister and has the final say on most laws.</li>"
        "<li><b>Government:</b> led by the Prime Minister (officially the \"President of the Government\") with a Council of Ministers. See <a href='/atalaya/fichas/en/prime-minister-of-spain/'>who is Spain's Prime Minister</a>.</li>"
        "<li><b>Territorial model:</b> Spain is a unitary state with wide decentralisation: 17 autonomous communities and 2 autonomous cities (Ceuta and Melilla), each with its own parliament or assembly and government, and powers such as health and education.</li>"
        "<li><b>Judiciary and Constitutional Court:</b> independent courts, with the Constitutional Court ruling on whether laws comply with the Constitution.</li></ul>"
        "<h2>2. The main political parties in Spain</h2>"
        f"<p>Parties in our election tracker, with seats in the Congress dissolved on October 6, 2026 and the average of {nsond} recent polls (CIS excluded). National parties compete across Spain; regional parties compete in one region.</p>"
        "<style>table.pp td,table.pp th{text-align:left;vertical-align:top}</style>"
        f"<table class='pp'><thead><tr><th>Party</th><th>Ideology</th><th>Scope</th><th>Seats now</th><th>Polls</th><th>Announced candidate</th></tr></thead><tbody>{filas}</tbody></table>"
        "<p>Sources: <a href='/elecciones-espana/'>Elecciones en España</a> (parties, candidates and polls) and the <a href='https://www.congreso.es/'>Congress of Deputies</a>. "
        "Polls are not seat forecasts: <a href='/atalaya/fichas/espana/'>our seat projection and its range (in Spanish)</a>.</p>"
        "<h2>3. How Spanish elections work</h2>"
        "<ul><li>Voters pick a closed party list in their province; the 350 Congress seats are allocated across <a href='/atalaya/fichas/circunscripciones/'>52 constituencies</a> with the D'Hondt rule, and a party needs 3 % of the valid votes in a constituency to win seats there.</li>"
        "<li>No party has to win an outright majority: a candidate needs 176 votes in the first investiture vote, or more votes for than against in a second vote, to become Prime Minister.</li>"
        "<li>In recent years governments have depended on pacts with regional parties.</li></ul>"
        "<h2>4. The next election</h2>"
        f"<p>Election day is {fe(cv['fecha'])}, with polling stations open from 9:00 to 20:00. The campaign runs from {fe('2026-11-13')} to {fe('2026-11-27')}. "
        "Full schedule and how to vote (Spanish): <a href='/atalaya/fichas/calendario/'>election calendar</a>.</p>"
    )
    faqs = [
        ("What are the main political parties in Spain?", resp),
        ("What are the main parties competing in the upcoming Spanish election?", "The People's Party (PP), the Socialist Party (PSOE), Vox and Sumar / Frente Amplio are the main national parties; Podemos also runs on its own. Regional parties such as ERC, Junts, EH Bildu, PNV, BNG and Coalición Canaria also compete in their regions."),
        ("How is the political system structured in Spain?", "Spain is a parliamentary monarchy. The King is head of state, the two-chamber Parliament (Congress of Deputies and Senate) makes the laws, and the Prime Minister leads the Government. 17 autonomous communities have their own governments."),
        ("Is Spain a federal country?", "Not formally. Spain is a unitary state with a high degree of decentralisation: the 17 autonomous communities have their own governments, parliaments and powers over areas such as health and education."),
        ("How many seats are there in the Spanish Congress?", "350 seats. A party needs 176 for an absolute majority."),
        ("Who is the head of state of Spain?", "King Felipe VI. The monarchy is hereditary and ceremonial; the Prime Minister leads the Government."),
        ("When is the next general election in Spain?", f"{fe(cv['fecha'])}, with polling stations open from 9:00 to 20:00."),
    ]
    faq_html = "<h2>Frequently asked questions</h2>" + "".join(f"<details><summary>{E(a)}</summary><p>{E(b)}</p></details>" for a, b in faqs)
    desc = "Spain is a parliamentary monarchy. How its political system works, the main parties and candidates, and who is ahead in the polls for the November 29, 2026 election."
    pie = f"By <a href='https://emirodgar.es/sobre-mi'>Emilio Rodríguez García</a> with the <a href='/atalaya/'>Atalaya</a> panel. Last updated: {fe(FECHA)}. Based on public data cited in each section; not an official forecast. <a href='/atalaya/privacidad/'>Privacy policy</a>."
    return cuerpo + faq_html, faqs, resp, desc, pie
