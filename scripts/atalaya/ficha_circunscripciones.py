"""Atalaya: ficha «¿Cuántas circunscripciones hay y cuántos escaños elige la mía?» (la invoca build_fichas.py).

Responde a prompts reales («circunscripción», «circunscripción electoral Madrid», «¿en qué circunscripción estoy registrado?»).
Usa: escaños y censo de las 52 circunscripciones en 2023 (Interior), padrón del INE y el ajuste de 2026 de convocatoria.json.
El ejemplo de reparto D'Hondt usa votos reales de Salamanca en 2023.
"""


def construir(c):
    E, FECHA, fecha_es, J, RAIZ, D, ps = (c[k] for k in ("E", "FECHA", "fecha_es", "J", "RAIZ", "D", "prov_slug"))
    prov = J(D / "resultados/congreso-2023-07/circunscripciones.json")["prov"]
    pad = J(D / "padron.json"); anio = pad["anios"][0]
    cv = J(RAIZ / "elecciones-espana/data/2026-11-29/convocatoria.json")
    nota = next(x for x in cv["camaras"] if x["id"] == "congreso")["nota"]
    nes = lambda x: f"{x:,}".replace(",", ".")
    f1 = lambda x: f"{x:.1f}".replace(".", ",")
    filas = []
    for pc, p in prov.items():
        esc = sum(s for _, s in p["v"].values()); hab = (pad["prov"].get(pc) or [None])[0]
        filas.append(dict(pc=pc, n=ps[pc][0], r=ps[pc][1], esc=esc, hab=hab, censo=p["censo"], cpe=p["censo"] / esc))
    por_cpe = sorted(filas, key=lambda f: f["cpe"])
    barato, caro = por_cpe[0], por_cpe[-1]
    ratio = caro["cpe"] / barato["cpe"]
    resp = (f"España tiene 52 circunscripciones electorales para elegir el Congreso: las 50 provincias más Ceuta y Melilla. Votas en la de tu provincia de residencia, según el censo, "
            f"y cada una reparte sus escaños con la regla D'Hondt. Cada provincia elige un mínimo de dos diputados y el resto se reparte según la población, "
            f"así que el voto no pesa igual en todas partes: en 2023, {barato['n']} necesitó {nes(round(barato['cpe']))} electores por escaño y {caro['n']}, {nes(round(caro['cpe']))}.")
    # ejemplo D'Hondt: Salamanca (código 37), votos reales de 2023
    sp = prov["37"]; sesc = sum(s for _, s in sp["v"].values())
    cand = [(k, v[0]) for k, v in sorted(sp["v"].items(), key=lambda kv: -kv[1][0])[:4]]
    cocientes = sorted(((v / d, k, d) for k, v in cand for d in range(1, sesc + 1)), reverse=True)[:sesc]
    ganados = {(k, d) for _, k, d in cocientes}
    th = "".join(f"<th>÷ {d}</th>" for d in range(1, sesc + 1))
    cuerpo_d = "".join(f"<tr><td>{E(k)}</td><td>{nes(v)}</td>" + "".join((f"<td><b>{nes(round(v / d))}</b> ✔</td>" if (k, d) in ganados else f"<td>{nes(round(v / d))}</td>") for d in range(1, sesc + 1)) + "</tr>" for k, v in cand)
    tabla_d = f"<table><thead><tr><th>Lista</th><th>Votos</th>{th}</tr></thead><tbody>{cuerpo_d}</tbody></table>"
    esc_d = {k: sum(1 for _, kk, _ in cocientes if kk == k) for k, _ in cand}
    ej = ", ".join(f"{E(k)} {n}" for k, n in esc_d.items() if n)
    tabla = "".join(f"<tr><td><a href='/atalaya/fichas/{f['r']}'>{E(f['n'])}</a></td><td>{f['esc']}</td><td>{nes(f['hab']) if f['hab'] else '–'}</td><td>{nes(f['censo'])}</td><td>{nes(round(f['cpe']))}</td></tr>" for f in sorted(filas, key=lambda f: f["r"]))
    cuerpo = (
        f"<p class='meta'>Actualizado el {fecha_es(FECHA)} · Escaños y censo de las elecciones de julio de 2023</p><p class='ans'>{E(resp)}</p>"
        "<h2>1. Qué es una circunscripción electoral</h2>"
        "<p>Es el territorio en el que se vota y se reparten los escaños. En las elecciones al Congreso coincide con la provincia (más Ceuta y Melilla); en las municipales es el municipio y en las europeas todo el país es una sola circunscripción. "
        "Se vota en la circunscripción en la que figuras en el censo electoral, que corresponde a tu domicilio. Los residentes en el extranjero (CERA) votan por la provincia de su última residencia.</p>"
        f"<p>Para el 29 de noviembre de 2026: {E(nota)}</p>"
        "<h2>2. Cómo se reparten los escaños: un ejemplo real</h2>"
        f"<p>En cada circunscripción se aplica la regla D'Hondt: se divide el voto de cada lista entre 1, 2, 3… y los escaños van a los cocientes más altos. Solo concurren las listas que superan el 3 % de los votos válidos de la circunscripción. "
        f"Ejemplo con los votos reales de Salamanca en 2023, que elige {sesc} diputados (las casillas con ✔ son los {sesc} cocientes más altos):</p>{tabla_d}"
        f"<p>Resultado: {ej}. Fuente: resultados oficiales del <a href='https://infoelectoral.interior.gob.es/'>Ministerio del Interior</a>.</p>"
        "<h2>3. Por qué un voto no pesa igual en todas las provincias</h2>"
        f"<p>Cada provincia elige un mínimo de dos diputados, así que las pequeñas tienen más escaños por habitante. En 2023, {E(barato['n'])} necesitó {nes(round(barato['cpe']))} electores por escaño y {E(caro['n'])}, {nes(round(caro['cpe']))}: "
        f"un escaño costó {f1(ratio)} veces más electores en {E(caro['n'])} que en {E(barato['n'])}. Además, en las provincias con pocos escaños (la mayoría) el reparto favorece a los partidos más votados y deja sin representación a los pequeños.</p>"
        f"<h2>4. Las 52 circunscripciones</h2><p>Escaños en 2023, habitantes del padrón de {anio} (INE), electores del censo de 2023 y electores por escaño. Pincha en una provincia para ver su ficha completa.</p>"
        f"<table><thead><tr><th>Circunscripción</th><th>Escaños</th><th>Habitantes</th><th>Censo</th><th>Electores por escaño</th></tr></thead><tbody>{tabla}</tbody></table>"
        "<p>Fuentes: <a href='https://infoelectoral.interior.gob.es/'>Ministerio del Interior</a> (escaños y censo) e <a href='https://www.ine.es/'>INE</a> (padrón).</p>"
        "<h2>Más información</h2><ul><li><a href='/atalaya/fichas/espana/'>¿Quién ganaría hoy las elecciones generales?</a></li><li><a href='/atalaya/fichas/calendario/'>Calendario y cómo votar</a></li></ul>"
    )
    faqs = [
        ("¿Cuántas circunscripciones electorales hay en España?", "52 para el Congreso de los Diputados: las 50 provincias, Ceuta y Melilla."),
        ("¿Qué es una circunscripción electoral?", "El territorio en el que se vota y en el que se reparten los escaños. En las elecciones generales coincide con la provincia."),
        ("¿En qué circunscripción voto?", "En la provincia en la que estás inscrito en el censo electoral, que corresponde a tu domicilio. Los residentes en el extranjero votan por su última provincia de residencia."),
        ("¿Cuántos escaños tiene cada provincia?", "Un mínimo de dos más los que corresponden por población; Ceuta y Melilla eligen uno cada una. La tabla de esta ficha muestra las 52 con sus escaños de 2023."),
        ("¿Cómo se reparten los escaños en cada circunscripción?", "Con la regla D'Hondt: se divide el voto de cada lista entre 1, 2, 3… y los escaños se asignan a los cocientes más altos. Antes se excluyen las listas con menos del 3 % de los votos válidos."),
        ("¿Por qué no pesa igual el voto en todas las provincias?", f"Porque cada provincia tiene un mínimo de dos escaños. En 2023, {barato['n']} necesitó {nes(round(barato['cpe']))} electores por escaño y {caro['n']}, {nes(round(caro['cpe']))}."),
    ]
    faq_html = "<h2>Preguntas frecuentes</h2>" + "".join(f"<details><summary>{E(a)}</summary><p>{E(b)}</p></details>" for a, b in faqs)
    desc = "España tiene 52 circunscripciones electorales (50 provincias, Ceuta y Melilla). Escaños de cada una, reparto D'Hondt con un ejemplo real y por qué el voto no pesa igual."
    return cuerpo + faq_html, faqs, resp, desc
