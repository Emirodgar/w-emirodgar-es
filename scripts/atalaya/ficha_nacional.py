"""Atalaya: ficha nacional «¿Quién ganaría hoy las elecciones generales?» (la invoca build_fichas.py).

Solo usa datos reales del repositorio:
  - sondeos: elecciones-espana/data/2026-11-29/encuestas.json (sin CIS, como la media del resto de fichas)
  - votos y escaños por provincia en julio de 2023: atalaya/data/resultados/congreso-2023-07/circunscripciones.json (Interior)

Proyección de escaños = método de cambio proporcional uniforme: los votos de 2023 de cada provincia se multiplican por
(estimación actual / resultado nacional de 2023) para PP, PSOE, Vox y Sumar; el resto de listas conserva sus votos de 2023;
se aplica la barrera del 3 % provincial y el reparto D'Hondt real. Con la proporción 1 reproduce los 350 escaños de 2023.
Es un ejercicio orientativo (no hay encuestas provinciales), nunca una previsión. Se calcula con la media y con cada sondeo reciente
para mostrar el rango, que es la parte honesta del resultado.
"""
import math, re, statistics
from datetime import datetime

CUATRO = ["PP", "PSOE", "VOX", "SUMAR"]
NOM = {"PP": "PP", "PSOE": "PSOE", "VOX": "Vox", "SUMAR": "Sumar"}
COL = {"PP": "#1d77c9", "PSOE": "#d6332b", "VOX": "#5aa02c", "SUMAR": "#a3367f"}
# listas que apoyaron la investidura de 2023 además de PSOE y Sumar (dato histórico; no es una previsión de pactos)
SOCIOS = ["ERC", "JxCAT - JUNTS", "EH Bildu", "EAJ-PNV", "B.N.G.", "CCa"]


def dhondt(votos, n):
    sc = {k: 0 for k in votos}
    for _ in range(n):
        k = max(votos, key=lambda x: votos[x] / (sc[x] + 1)); sc[k] += 1
    return sc


def proyectar(prov, sondeo):
    """Escaños por lista con cambio proporcional uniforme. `sondeo` = {PP:%,PSOE:%,VOX:%,SUMAR:%,PODEMOS:%?}."""
    tot = sum(p["validos"] for p in prov.values())
    base = {k: sum(p["v"].get(k, [0])[0] for p in prov.values()) / tot * 100 for k in CUATRO}
    r = {k: sondeo[k] / base[k] for k in CUATRO}
    ro = 1.0  # el resto de listas conserva sus votos de 2023
    out = {}
    for pc, p in prov.items():
        nv = {n: v[0] * r.get(n, ro) for n, v in p["v"].items()}
        total_valido = sum(nv.values()) + p["blanco"]
        elegibles = {n: v for n, v in nv.items() if v >= 0.03 * total_valido and v > 0}
        escanos = sum(s for _, s in p["v"].values())
        for n, s in dhondt(elegibles, escanos).items(): out[n] = out.get(n, 0) + s
    return out


def media(sondeos, ref):
    """Misma media que el resto de fichas: sondeos de los 30 días previos al último, ponderados por raíz de la muestra."""
    sm, ct = {}, {}
    for x in sondeos:
        if (ref - datetime.fromisoformat(x["fecha"])).days > 30: continue
        w = math.sqrt(x.get("muestra") or 1000)
        for k, v in x["voto"].items():
            sm[k] = sm.get(k, 0) + v * w; ct[k] = ct.get(k, 0) + w
    return {k: sm[k] / ct[k] for k in sm}


def svg_tendencia(meses, serie):
    W, H, L, B, T, R = 720, 300, 44, 36, 14, 70
    ys = [v for s in serie.values() for v in s if v is not None]
    lo, hi = math.floor(min(ys) / 5) * 5, math.ceil(max(ys) / 5) * 5
    X = lambda i: L + (W - L - R) * (i / max(len(meses) - 1, 1))
    Y = lambda v: T + (H - T - B) * (1 - (v - lo) / (hi - lo))
    g = "".join(f"<line x1='{L}' x2='{W-R}' y1='{Y(v):.1f}' y2='{Y(v):.1f}' stroke='currentColor' stroke-opacity='.15'/><text x='{L-6}' y='{Y(v)+4:.1f}' text-anchor='end' font-size='11' fill='currentColor' opacity='.7'>{v} %</text>" for v in range(lo, hi + 1, 5))
    x = "".join(f"<text x='{X(i):.1f}' y='{H-12}' text-anchor='middle' font-size='11' fill='currentColor' opacity='.7'>{m}</text>" for i, m in enumerate(meses))
    ls = ""
    for k, s in serie.items():
        pts = [(X(i), Y(v), v) for i, v in enumerate(s) if v is not None]
        if not pts: continue
        ls += f"<polyline fill='none' stroke='{COL[k]}' stroke-width='2.5' points='{' '.join(f'{a:.1f},{b:.1f}' for a, b, _ in pts)}'/>"
        ls += "".join(f"<circle cx='{a:.1f}' cy='{b:.1f}' r='3' fill='{COL[k]}'/>" for a, b, _ in pts)
        a, b, v = pts[-1]
        ls += f"<text x='{a+8:.1f}' y='{b+4:.1f}' font-size='12' font-weight='600' fill='{COL[k]}'>{NOM[k]} {v:.1f}</text>".replace(f"{v:.1f}", f"{v:.1f}".replace(".", ","))
    return (f"<svg viewBox='0 0 {W} {H}' role='img' aria-label='Evolución mensual de la estimación de voto de PP, PSOE, Vox y Sumar' style='width:100%;height:auto;color:inherit'>{g}{x}{ls}</svg>")


def svg_escanos(filas, mayoria=176, tope=350):
    W, L, R, rh = 720, 90, 30, 34
    H = rh * len(filas) + 34
    X = lambda v: L + (W - L - R) * v / tope
    s = ""
    for i, (nom, col, lo, med, hi) in enumerate(filas):
        y = 20 + i * rh
        s += f"<text x='{L-8}' y='{y+16}' text-anchor='end' font-size='13' fill='currentColor'>{nom}</text>"
        s += f"<rect x='{X(lo):.1f}' y='{y+4}' width='{max(X(hi)-X(lo),3):.1f}' height='18' rx='3' fill='{col}' opacity='.30'/>"
        s += f"<rect x='{L}' y='{y+9}' width='{X(med)-L:.1f}' height='8' rx='2' fill='{col}'/>"
        s += f"<text x='{X(max(hi, med))+6:.1f}' y='{y+17}' font-size='12' fill='currentColor'>{med} <tspan opacity='.6'>({lo}–{hi})</tspan></text>"
    s += f"<line x1='{X(mayoria):.1f}' x2='{X(mayoria):.1f}' y1='8' y2='{H-20}' stroke='currentColor' stroke-dasharray='4 3' opacity='.7'/><text x='{X(mayoria):.1f}' y='{H-6}' text-anchor='middle' font-size='11' fill='currentColor'>mayoría absoluta: {mayoria}</text>"
    return f"<svg viewBox='0 0 {W} {H}' role='img' aria-label='Escaños proyectados con rango entre sondeos' style='width:100%;height:auto;color:inherit'>{s}</svg>"


def construir(c):
    E, BASE, FECHA, fecha_es, J, D, RAIZ = (c[k] for k in ("E", "BASE", "FECHA", "fecha_es", "J", "D", "RAIZ"))
    enc = J(RAIZ / "elecciones-espana/data/2026-11-29/encuestas.json")
    sond = [x for x in enc["sondeos"] if not re.search("cis", x["empresa"], re.I)]
    ref = datetime.fromisoformat(sond[0]["fecha"])
    rec = [x for x in sond if (ref - datetime.fromisoformat(x["fecha"])).days <= 30]
    med = media(sond, ref)
    prov = J(D / "resultados/congreso-2023-07/circunscripciones.json")["prov"]
    f1 = lambda x: f"{x:.1f}".replace(".", ",")

    # --- 1. media y rango por partido
    orden = sorted(CUATRO, key=lambda k: -med[k])
    rango = {k: (min(x["voto"][k] for x in rec if k in x["voto"]), max(x["voto"][k] for x in rec if k in x["voto"])) for k in CUATRO}
    # media del periodo anterior (30-60 días antes) para ver el cambio
    ant = [x for x in sond if 30 < (ref - datetime.fromisoformat(x["fecha"])).days <= 60]
    med_ant = {}
    if len(ant) >= 4:
        sm, ct = {}, {}
        for x in ant:
            w = math.sqrt(x.get("muestra") or 1000)
            for k, v in x["voto"].items(): sm[k] = sm.get(k, 0) + v * w; ct[k] = ct.get(k, 0) + w
        med_ant = {k: sm[k] / ct[k] for k in sm}
    base23 = {k: 100 * sum(p["v"].get(k, [0])[0] for p in prov.values()) / sum(p["validos"] for p in prov.values()) for k in CUATRO}
    filas = ""
    for k in orden:
        d = (f"{med[k]-med_ant[k]:+.1f}".replace(".", ",").replace("-", "−") + " pts") if k in med_ant else "–"
        filas += f"<tr><td>{NOM[k]}</td><td><b>{f1(med[k])} %</b></td><td>{f1(rango[k][0])}–{f1(rango[k][1])} %</td><td>{d}</td><td>{f1(base23[k])} %</td></tr>"
    tabla = ("<table><thead><tr><th>Partido</th><th>Media</th><th>Rango entre sondeos</th><th>Cambio vs. 30–60 días antes</th><th>Resultado 2023</th></tr></thead>"
             f"<tbody>{filas}</tbody></table>")
    lid, seg = orden[0], orden[1]
    ventaja = med[lid] - med[seg]
    solape = rango[lid][0] <= rango[seg][1]

    # --- 2. tendencia mensual (todos los sondeos sin CIS)
    cuenta = {}
    for x in sond: cuenta[x["fecha"][:7]] = cuenta.get(x["fecha"][:7], 0) + 1
    meses_n = [m for m in sorted(cuenta) if cuenta[m] >= 2][-9:]
    MES = {"01": "ene", "02": "feb", "03": "mar", "04": "abr", "05": "may", "06": "jun", "07": "jul", "08": "ago", "09": "sep", "10": "oct", "11": "nov", "12": "dic"}
    serie = {k: [] for k in CUATRO}
    for m in meses_n:
        sel = [x for x in sond if x["fecha"][:7] == m]
        for k in CUATRO:
            xs = [(x["voto"][k], math.sqrt(x.get("muestra") or 1000)) for x in sel if k in x["voto"]]
            serie[k].append(sum(v * w for v, w in xs) / sum(w for _, w in xs) if xs else None)
    grafico = svg_tendencia([MES[m[5:]] for m in meses_n], serie)

    # --- 3. proyección de escaños (media + cada sondeo reciente completo)
    p_media = proyectar(prov, med)
    completos = [x for x in rec if all(k in x["voto"] for k in CUATRO)]
    proy = [proyectar(prov, x["voto"]) for x in completos]
    def r(k): vs = [p.get(k, 0) for p in proy]; return min(vs), max(vs)
    socios = lambda p: p.get("PSOE", 0) + p.get("SUMAR", 0) + sum(p.get(s, 0) for s in SOCIOS)
    pv = lambda p: p.get("PP", 0) + p.get("VOX", 0)
    n_pv = sum(1 for p in proy if pv(p) >= 176); n_so = sum(1 for p in proy if socios(p) >= 176)
    blk_pv = (min(pv(p) for p in proy), max(pv(p) for p in proy)); blk_so = (min(socios(p) for p in proy), max(socios(p) for p in proy))
    chart_rows = [(NOM[k], COL[k], r(k)[0], p_media.get(k, 0), r(k)[1]) for k in orden]
    graf_esc = svg_escanos(chart_rows)
    esc_tab = "".join(f"<tr><td>{NOM[k]}</td><td><b>{p_media.get(k,0)}</b></td><td>{r(k)[0]}–{r(k)[1]}</td><td>{sum(p['v'].get(k,[0,0])[1] for p in prov.values())}</td></tr>" for k in orden)
    esc_tab += f"<tr><td>Resto de listas (regionales)</td><td><b>{350 - sum(p_media.get(k,0) for k in CUATRO)}</b></td><td>–</td><td>{350 - sum(sum(p['v'].get(k,[0,0])[1] for p in prov.values()) for k in CUATRO)}</td></tr>"
    mejor = max(orden, key=lambda k: p_media.get(k, 0))

    if n_pv == 0 and n_so == 0:
        mayoria_txt = (f"Con esta proyección, ni PP y Vox juntos ({blk_pv[0]}–{blk_pv[1]} escaños según el sondeo) ni el bloque de la investidura de 2023 ({blk_so[0]}–{blk_so[1]}) alcanzan los 176 en ningún sondeo reciente: "
                       f"el resultado depende de los partidos regionales y de pactos que ningún sondeo mide.")
    else:
        mayoria_txt = (f"PP y Vox juntos sumarían {blk_pv[0]}–{blk_pv[1]} escaños y alcanzarían los 176 en {n_pv} de {len(proy)} sondeos recientes; "
                       f"el bloque de la investidura de 2023 (PSOE, Sumar, ERC, Junts, Bildu, PNV, BNG y CC) sumaría {blk_so[0]}–{blk_so[1]} y llegaría en {n_so} de {len(proy)}.")

    resp = (f"Si las elecciones fueran hoy, el {NOM[lid]} sería el partido más votado: la media de encuestas le da un {f1(med[lid])} %, "
            f"{f1(ventaja)} puntos sobre {NOM[seg]} ({f1(med[seg])} %)" + (", aunque los rangos de ambos se solapan entre sondeos" if solape else ", y la ventaja se mantiene en todos los sondeos recientes") + ". "
            f"Ganar en votos no es gobernar: " + (f"proyectado sobre los votos de 2023, el {NOM[mejor]} lograría unos {p_media[mejor]} escaños, por debajo de los 176 de la mayoría absoluta. " if p_media[mejor] < 176 else f"el {NOM[mejor]} superaría los 176 escaños. ")
            + mayoria_txt)

    metodo = (f"<p>Para cada provincia se toman los votos oficiales de julio de 2023 (<a href='https://infoelectoral.interior.gob.es/'>Ministerio del Interior</a>) y se multiplican por el cociente entre la estimación actual y el resultado nacional de 2023 de cada partido. "
              f"Se aplica la barrera del 3 % por circunscripción y el reparto D'Hondt con los escaños reales de cada provincia. El ejercicio se repite con cada sondeo de los últimos 30 días que incluye a los cuatro partidos ({len(proy)} de {len(rec)}) para obtener el rango. "
              f"Con una proporción de 1 reproduce exactamente los 350 escaños de 2023, lo que valida la mecánica.</p>"
              "<ul><li>Supone que el cambio de voto es igual en todas las provincias; no lo es (hay territorios donde Vox o Sumar suben o bajan más).</li>"
              "<li>No proyecta Podemos, porque en 2023 no hay una base comparable (concurrió dentro de otras candidaturas), ni partidos nuevos.</li>"
              "<li>Los partidos regionales (ERC, Junts, Bildu, PNV, BNG, CC, UPN) conservan los votos de 2023, sin que los sondeos nacionales los midan; en una provincia pequeña, un par de puntos mueven el último escaño.</li>"
              "<li>Es una proyección orientativa a partir de datos públicos, no una encuesta ni una previsión oficial.</li></ul>")

    faqs = [
        ("¿Quién ganaría hoy las elecciones generales en España?", resp),
        ("¿Cuántos escaños necesita un partido para gobernar?", "La mayoría absoluta en el Congreso son 176 de 350 escaños. Sin ella hace falta sumar apoyos de otros grupos en la investidura."),
        ("¿Cuándo son las elecciones generales?", "El domingo 29 de noviembre de 2026, con horario de votación de 9:00 a 20:00."),
        ("¿Cómo se calcula esta media de encuestas?", f"Es una media ponderada por la raíz de la muestra de los sondeos publicados en los 30 días previos al {fecha_es(ref.strftime('%Y-%m-%d'))}, sin el CIS. Ahora incluye {len(rec)} sondeos."),
        ("¿Es una previsión de escaños?", "No. La proyección de escaños aplica el cambio de voto nacional de forma uniforme sobre los resultados provinciales de 2023, así que debe leerse como un ejercicio orientativo con un rango amplio."),
    ]
    faq_html = "<h2>Preguntas frecuentes</h2>" + "".join(f"<details><summary>{E(a)}</summary><p>{E(b)}</p></details>" for a, b in faqs)

    cuerpo = (f"<p class='meta'>Actualizado el {fecha_es(FECHA)} · último sondeo: {fecha_es(sond[0]['fecha'])} · Elecciones generales del 29 de noviembre de 2026</p><p class='ans'>{E(resp)}</p>"
              f"<h2>1. Qué dicen las encuestas</h2><p>Media ponderada de {len(rec)} sondeos de los 30 días previos al {fecha_es(sond[0]['fecha'])} (sin CIS). El rango muestra el sondeo más bajo y el más alto: si se solapan, la diferencia entre partidos es incierta.</p>{tabla}"
              f"<h2>2. Cómo ha evolucionado</h2><p>Media mensual de los sondeos publicados (sin CIS); solo se muestran los meses con al menos dos sondeos. Los meses con pocos sondeos son menos fiables.</p>{grafico}"
              f"<h2>3. Escaños: del voto al Congreso</h2><p>El sistema reparte 350 escaños por provincias con la regla D'Hondt, así que el porcentaje nacional no se traduce directamente en escaños. Proyección sobre los resultados oficiales de 2023, con la media y el rango entre sondeos:</p>{graf_esc}"
              f"<table><thead><tr><th>Lista</th><th>Con la media</th><th>Rango entre sondeos</th><th>Escaños 2023</th></tr></thead><tbody>{esc_tab}</tbody></table>"
              f"<h2>4. ¿Llegaría alguien a 176?</h2><p>{E(mayoria_txt)}</p><p class='meta'>El «bloque de la investidura de 2023» es un dato histórico (quiénes votaron a favor de la investidura entonces), no una previsión de pactos para 2026.</p>"
              f"<h2>5. Cómo se ha calculado la proyección</h2>{metodo}"
              "<h2>Qué podría cambiar el resultado</h2><ul><li>La participación y el reparto de los indecisos en las semanas finales de la campaña.</li>"
              "<li>El voto provincial: con 52 circunscripciones, pequeñas diferencias mueven escaños donde se reparten pocos diputados.</li>"
              "<li>Los partidos regionales y su peso en los pactos, que casi ningún sondeo nacional mide.</li></ul>"
              "<h2>Por provincias</h2><p>Consulta cómo ha votado cada provincia y quién va primero en las <a href='/atalaya/fichas/'>fichas por provincia</a>.</p>"
              "<h2>Fuentes</h2><ul><li>Sondeos: empresas y medios citados en <a href='/elecciones-espana/'>Elecciones en España</a>, que recopila las encuestas desde "
              "<a href='https://www.politicaelectoral.com/es/espana/generales-2026/nacional'>politicaelectoral.com</a> y <a href='https://es.wikipedia.org/wiki/Encuestas_de_opini%C3%B3n_para_las_elecciones_generales_de_Espa%C3%B1a_de_2026'>Wikipedia</a>.</li>"
              "<li>Resultados de 2023: <a href='https://infoelectoral.interior.gob.es/'>Ministerio del Interior</a>.</li></ul>" + faq_html)
    desc = f"Si las elecciones fueran hoy, el {NOM[lid]} ganaría con un {f1(med[lid])} % según la media de encuestas. Tendencia, escaños proyectados y mayoría de 176."
    return cuerpo, faqs, resp, desc, {"lid": NOM[lid], "pm": p_media, "rangos": {k: r(k) for k in CUATRO}, "n_pv": n_pv, "n_so": n_so, "n": len(proy)}
