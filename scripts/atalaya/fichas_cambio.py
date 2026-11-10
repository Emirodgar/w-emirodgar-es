"""Atalaya: fichas «¿qué provincias y ciudades pueden cambiar de partido?» (las invoca build_fichas.py).

  /atalaya/fichas/cambio/             hub: provincias que pueden cambiar de partido más votado (histórico + 2023 + sondeos)
  /atalaya/fichas/cambio/historico/   provincias que más han alternado de partido desde 1977
  /atalaya/fichas/cambio/escanos/     escaños más ajustados (votos que separaron el último escaño) y cuáles cambian de manos
  /atalaya/fichas/cambio/<partido>/   dónde puede ganar o perder escaños PP, PSOE, Vox y Sumar
  /atalaya/fichas/cambio/ciudades/    ciudades de más de 50.000 habitantes que pueden cambiar de partido más votado
  + un bloque «¿Puede cambiar de partido X?» en cada ficha de provincia

La formulación elegida es «cambiar de partido más votado», que se puede medir con un criterio único y reproducible. Las demás formas
habituales de preguntarlo («provincias decisivas», «provincias pendulares», «en juego») se recogen como preguntas relacionadas.
Todo sale de volatilidad.py: histórico de escaños (1977–2023), votos oficiales de 2023 y proyección con los sondeos recientes.
"""
from volatilidad import nom, UMBRAL_AIRE, UMBRAL_CORTA

ORD = ["cambio", "aire", "corta", "estable"]
ETQ = {"cambio": "Cambio proyectado", "aire": "En el aire", "corta": "Ventaja corta", "estable": "Estable"}
COL = {"PP": "#1d77c9", "PSOE": "#d6332b", "UCD": "#3d9a5b", "Vox": "#5aa02c", "Cs": "#e8892b", "Podemos": "#7b3fa0", "PNV": "#2a8a4a", "CiU": "#1b9bd1"}
CSS = ("<style>table.t td,table.t th{text-align:left;vertical-align:top}.chip{display:inline-block;padding:1px 8px;border-radius:10px;border:1px solid #9aa7ba;font-size:13px;white-space:nowrap}"
       ".k-cambio{background:#fde3e1;border-color:#d6332b;color:#7a1410}.k-aire{background:#fff0cc;border-color:#d99a00;color:#6b4a00}.k-corta{background:#e8f1ff;border-color:#2563eb;color:#143d91}.k-estable{background:#e9f6ec;border-color:#3d9a5b;color:#1e5a31}"
       ".dot{display:inline-block;width:11px;height:11px;border-radius:2px;margin-right:2px;border:1px solid #6b778a}"
       "@media (prefers-color-scheme:dark){.k-cambio{background:#3a1715;color:#ffb4ae}.k-aire{background:#3a2d0b;color:#ffd780}.k-corta{background:#12274d;color:#a9c8ff}.k-estable{background:#12301c;color:#9fe0b0}}</style>")


def generar(c, V):
    E, FECHA, fecha_es, ps, publicar, slug = (c[k] for k in ("E", "FECHA", "fecha_es", "ps", "publicar", "slug"))
    P, C = V["P"], V["C"]
    f1 = lambda x: f"{x:.1f}".replace(".", ",")
    f2 = lambda x: (f"{x:.2f}" if x < 1 else f"{x:.1f}").replace(".", ",")
    nes = lambda x: f"{x:,}".replace(",", ".")
    art = lambda k: ("el " + nom(k)) if nom(k) in ("PP", "PSOE") else nom(k)
    Art = lambda k: art(k)[0].upper() + art(k)[1:]
    link = lambda pc: f"<a href='/atalaya/fichas/{ps[pc][1]}'>{E(ps[pc][0])}</a>"
    chip = lambda k: f"<span class='chip k-{k}'>{ETQ[k]}</span>"
    grupos = {k: sorted([p for p in P.values() if p["cat"] == k], key=lambda p: p["mm"]) for k in ORD}
    n_pol, n_son = V["ncomp"], V["nsond"]
    fs = fecha_es(V["fsond"])
    med, base = V["med"], V["base"]
    desp = ", ".join(f"{nom(k)} {f1(base[k])} % → {f1(med[k])} %" for k in ("PP", "PSOE", "VOX", "SUMAR"))
    nombres = lambda L, n=6: ", ".join(E(ps[p["pc"]][0]) for p in L[:n]) + (f" y {len(L) - n} más" if len(L) > n else "")

    def fila_prov(p):
        h = p["hist"]
        return (f"<tr><td>{link(p['pc'])}</td><td>{E(Art(p['l23']))} (+{f1(p['m23'])})</td><td>{E(Art(p['lm']))} (+{f1(p['mm'])})</td>"
                f"<td>{p['flips']} de {p['npol']}</td><td>{h['alt']} · {h['empates']}</td><td>{chip(p['cat'])}</td></tr>")
    cab_prov = ("<table class='t'><thead><tr><th>Provincia</th><th>Más votado en 2023 (margen, puntos)</th><th>Más votado con la media de sondeos</th>"
                "<th>Sondeos con vuelco</th><th>Alternancias · empates desde 1977</th><th>Situación</th></tr></thead><tbody>")

    def frase(p):
        s = f"En {ps[p['pc']][0]}, {art(p['l23'])} ganó en julio de 2023 por {f1(p['m23'])} puntos sobre {art(p['s23'])}. "
        if p["cat"] == "cambio":
            s += f"Con la media de los sondeos de los últimos 30 días, {art(p['lm'])} pasaría a ser el más votado ({f1(p['mm'])} puntos de ventaja) y lo sería en {p['flips']} de {p['npol']} sondeos recientes."
        elif p["cat"] == "aire":
            s += (f"Con la media de sondeos mantiene el primer puesto, pero con solo {f1(p['mm'])} puntos de margen"
                  + (f" y lo pierde en {p['flips']} de {p['npol']} sondeos recientes." if p["flips"] else "."))
        elif p["cat"] == "corta":
            s += f"Con la media de sondeos mantiene el primer puesto con {f1(p['mm'])} puntos de margen: una ventaja corta."
        else:
            s += f"Con la media de sondeos mantiene el primer puesto con {f1(p['mm'])} puntos de margen y no lo pierde en ningún sondeo reciente."
        h = p["hist"]
        s += (f" Desde 1977 el partido con más escaños ha cambiado {h['alt']} {'vez' if h['alt'] == 1 else 'veces'} ({h['alt8']} en las últimas 8 elecciones) "
              f"y hubo {h['empates']} {'empate' if h['empates'] == 1 else 'empates'} en cabeza.")
        return s

    # ---------------- 1. HUB ----------------
    ncam, nair, ncor = len(grupos["cambio"]), len(grupos["aire"]), len(grupos["corta"])
    cambios_txt = "; ".join(f"{E(ps[p['pc']][0])} ({art(p['l23'])} → {art(p['lm'])})" for p in grupos["cambio"])
    resp = (f"Con la media de los sondeos de los últimos 30 días, {ncam} provincias cambiarían de partido más votado respecto a las elecciones de julio de 2023: {cambios_txt}. "
            f"Otras {nair} están en el aire ({nombres(grupos['aire'])}) y {ncor} tienen una ventaja corta, de menos de {UMBRAL_CORTA:.0f} puntos ({nombres(grupos['corta'])}). "
            f"Las otras {len(grupos['estable'])} mantendrían al mismo partido en cabeza.")
    por_que = (f"<p>La media de sondeos mueve el voto nacional así respecto a 2023: {E(desp)}. Como el PSOE y Sumar bajan y Vox sube, cambian de partido las provincias donde el PSOE ganó por poco "
               f"y el PP está justo detrás.</p>")
    relevantes = grupos["cambio"] + grupos["aire"] + grupos["corta"]
    tabla = cab_prov + "".join(fila_prov(p) for p in relevantes) + "</tbody></table>"
    est = ", ".join(link(p["pc"]) for p in sorted(grupos["estable"], key=lambda p: ps[p["pc"]][0]))
    metodo = (f"<p>Una provincia «cambia de partido» cuando el partido más votado en ella es distinto al de julio de 2023. Para estimarlo se combinan tres señales con datos reales:</p>"
              "<ol><li><b>Resultado de 2023:</b> margen en puntos de voto válido entre el primero y el segundo, con los votos oficiales del <a href='https://infoelectoral.interior.gob.es/'>Ministerio del Interior</a>.</li>"
              f"<li><b>Sondeos recientes:</b> se aplica a los votos de 2023 de cada provincia el cambio que indica la media de {n_son} sondeos de los últimos 30 días hasta el {fs} (sin CIS), y se repite con cada uno de los {n_pol} sondeos que incluyen a los cuatro partidos principales para ver cuántos escenarios provocan un vuelco.</li>"
              "<li><b>Histórico:</b> cuántas veces ha cambiado el partido con más escaños desde 1977 y cuántas veces ha habido empate en cabeza (<a href='/atalaya/fichas/cambio/historico/'>detalle por provincia</a>).</li></ol>"
              f"<p>Clasificación: <b>cambio proyectado</b> (con la media de sondeos gana otro partido), <b>en el aire</b> (gana el mismo, pero con menos de {UMBRAL_AIRE:.0f} puntos de margen o pierde en algún sondeo), "
              f"<b>ventaja corta</b> (entre {UMBRAL_AIRE:.0f} y {UMBRAL_CORTA:.0f} puntos) y <b>estable</b> (más de {UMBRAL_CORTA:.0f}).</p>"
              "<p class='warn'>Limitaciones: no hay encuestas provinciales, así que el ejercicio supone que el voto cambia por igual en todas partes (no ocurre: en Cataluña, el País Vasco o Navarra los partidos regionales alteran el resultado). "
              "Los partidos regionales mantienen los votos de 2023. Es una estimación razonada con datos públicos, no una previsión oficial; el margen debe leerse como un orden de magnitud.</p>")
    rel = ("<h2>Otras formas de verlo</h2><ul><li><a href='/atalaya/fichas/cambio/historico/'>¿Qué provincias han cambiado más de partido desde 1977?</a></li>"
           "<li><a href='/atalaya/fichas/cambio/escanos/'>¿Qué escaños están más en el aire?</a></li>"
           "<li><a href='/atalaya/fichas/cambio/ciudades/'>¿Qué ciudades pueden cambiar de partido más votado?</a></li>"
           "<li>Escaños por partido: <a href='/atalaya/fichas/cambio/pp/'>PP</a>, <a href='/atalaya/fichas/cambio/psoe/'>PSOE</a>, <a href='/atalaya/fichas/cambio/vox/'>Vox</a> y <a href='/atalaya/fichas/cambio/sumar/'>Sumar</a>.</li>"
           "<li><a href='/atalaya/fichas/espana/'>¿Quién ganaría hoy las elecciones generales?</a></li></ul>")
    faqs = [
        ("¿Qué provincias pueden cambiar de partido ganador en las elecciones generales?", resp),
        ("¿Cuáles son las provincias clave o decisivas del 29N?", f"Las que más probabilidades tienen de cambiar de partido más votado o están en el aire: {nombres(grupos['cambio'] + grupos['aire'], 10)}."),
        ("¿Qué son las provincias pendulares o swing?", "Las que cambian de partido más votado con frecuencia o tienen un margen muy corto entre el primero y el segundo. Aquí se miden con el histórico de escaños desde 1977, el margen de 2023 y los sondeos recientes."),
        ("¿Cuántas provincias cambiarían de partido según las encuestas?", f"{ncam} con la media de sondeos de los últimos 30 días, y {nair} más están en el aire. Es una proyección orientativa que supone el mismo cambio de voto en toda España."),
        ("¿Cómo se calcula si una provincia puede cambiar de partido?", "Se compara el margen del primero sobre el segundo en 2023 con el cambio de voto que indican los sondeos, y se repite con cada sondeo reciente para ver en cuántos hay vuelco. Se añade el histórico de alternancias desde 1977."),
    ]
    cuerpo = (f"{CSS}<p class='meta'>Actualizado el {fecha_es(FECHA)} · Elecciones generales del 29 de noviembre de 2026</p><p class='ans'>{E(resp)}</p>"
              f"<h2>1. Por qué cambian</h2>{por_que}"
              f"<h2>2. Las provincias en juego</h2><p>Ordenadas de mayor a menor riesgo de cambio. «Sondeos con vuelco» indica en cuántos de los {n_pol} sondeos recientes el partido más votado sería otro distinto al de 2023.</p>{tabla}"
              f"<h2>3. Las {len(grupos['estable'])} provincias estables</h2><p>Con más de {UMBRAL_CORTA:.0f} puntos de margen proyectado y sin vuelco en ningún sondeo: {est}.</p>"
              f"<h2>4. Cómo se ha calculado</h2>{metodo}{rel}")
    publicar("cambio/", "¿Qué provincias pueden cambiar de partido en las elecciones generales del 29N?", "Provincias que pueden cambiar de partido más votado el 29N según el histórico desde 1977, el margen de 2023 y los últimos sondeos.",
             "¿Qué provincias pueden cambiar de partido ganador en las elecciones generales del 29N?", cuerpo + "<h2>Preguntas frecuentes</h2>" + "".join(f"<details><summary>{E(a)}</summary><p>{E(b)}</p></details>" for a, b in faqs), faqs, "Provincias que pueden cambiar de partido")

    # ---------------- 2. HISTÓRICO ----------------
    H = sorted(P.values(), key=lambda p: (-p["hist"]["alt"], -p["hist"]["empates"], ps[p["pc"]][0]))
    top = H[:5]
    nunca = [p for p in P.values() if p["hist"]["alt"] == 0 and len(p["hist"]["partidos"]) == 1]
    dot = lambda k: (f"<span class='dot' style='background:{COL.get(k, '#9aa7ba')}' title='{E(k or 'Empate')}'></span>" if k else "<span class='dot' style='background:transparent' title='Empate'></span>")
    filas = "".join(f"<tr><td>{link(p['pc'])}</td><td>{p['hist']['alt']}</td><td>{p['hist']['alt8']}</td><td>{p['hist']['empates']}</td><td>{E(', '.join(p['hist']['partidos']))}</td>"
                    f"<td style='white-space:nowrap'>{''.join(dot(k) for k in p['hist']['seq'])}</td></tr>" for p in H)
    top_txt = ", ".join("%s (%d)" % (E(ps[p["pc"]][0]), p["hist"]["alt"]) for p in top)
    resp2 = (f"Desde 1977, las provincias en las que más veces ha cambiado el partido con más escaños son {top_txt}. "
             f"{len(nunca)} provincias no han cambiado nunca de partido: {nombres(nunca, 8)}.")
    leyenda = "".join(f"<span class='dot' style='background:{col}'></span>{E(k)} &nbsp;" for k, col in COL.items() if k in ("PP", "PSOE", "UCD", "Vox", "Cs", "Podemos")) + "<span class='dot' style='background:transparent'></span>Empate en cabeza &nbsp;<span class='dot' style='background:#9aa7ba'></span>Otros"
    cuerpo2 = (f"{CSS}<p class='meta'>Actualizado el {fecha_es(FECHA)} · Escaños por provincia en las 16 elecciones generales entre 1977 y 2023</p><p class='ans'>{E(resp2)}</p>"
               "<h2>1. Qué se mide</h2><p>Para cada elección se toma el partido con más escaños en la provincia. Una <b>alternancia</b> es un cambio de ese partido entre dos elecciones con líder claro; un <b>empate en cabeza</b> es una elección en la que dos o más partidos quedaron igualados a escaños (frecuente en provincias pequeñas). "
               "Fuente: <a href='https://es.wikipedia.org/wiki/Elecciones_generales_de_Espa%C3%B1a'>Wikipedia</a>, que recoge los datos oficiales del Ministerio del Interior.</p>"
               f"<h2>2. Las 52 circunscripciones</h2><p>La tira de cuadros muestra el partido con más escaños en cada elección, de 1977 a 2023: {leyenda}.</p>"
               "<table class='t'><thead><tr><th>Provincia</th><th>Alternancias</th><th>En las últimas 8 elecciones</th><th>Empates en cabeza</th><th>Partidos que han liderado</th><th>1977 → 2023</th></tr></thead>"
               f"<tbody>{filas}</tbody></table>"
               "<h2>3. Cómo leerlo</h2><p>Una provincia con muchas alternancias y empates es más volátil: pequeños cambios de voto mueven al primero. Una provincia con cero alternancias es un feudo, pero eso no garantiza que lo siga siendo: "
               "<a href='/atalaya/fichas/cambio/'>cruzamos el histórico con los sondeos recientes</a> para estimar dónde puede haber un cambio el 29N.</p>")
    faqs2 = [("¿Qué provincias han cambiado más de partido ganador desde 1977?", resp2),
             ("¿Qué provincias nunca han cambiado de partido más votado?", f"{len(nunca)} provincias: {nombres(nunca, 12)}."),
             ("¿Qué es una alternancia electoral?", "Un cambio del partido con más escaños en una circunscripción entre dos elecciones consecutivas con líder claro."),
             ("¿Por qué hay empates en cabeza?", "En provincias con pocos escaños, dos partidos pueden obtener el mismo número de diputados, sobre todo cuando hay mucha competencia entre el primero y el segundo.")]
    publicar("cambio/historico/", "Provincias que más han cambiado de partido desde 1977: histórico de alternancias", "Alternancias y empates en cabeza por provincia en las 16 elecciones generales desde 1977, con la tira de líderes de cada una.",
             "¿Qué provincias han cambiado más de partido ganador desde 1977?", cuerpo2 + "<h2>Preguntas frecuentes</h2>" + "".join(f"<details><summary>{E(a)}</summary><p>{E(b)}</p></details>" for a, b in faqs2), faqs2, "Histórico de alternancias")

    # ---------------- 3. ESCAÑOS EN EL AIRE ----------------
    def fila_esc(p, u):
        return (f"<tr><td>{link(p['pc'])}</td><td>{p['escanos']}</td><td>{E(Art(u['gana']))}</td><td>{E(Art(u['pierde']))}</td><td>{nes(round(u['falta']))}</td><td>{f2(u['pct'])} %</td></tr>")
    cab_esc = "<table class='t'><thead><tr><th>Provincia</th><th>Escaños</th><th>Se lleva el último</th><th>Se queda a las puertas</th><th>Votos que le faltaron</th><th>% de votos válidos</th></tr></thead><tbody>"
    e23 = sorted(P.values(), key=lambda p: p["ult23"]["falta"])[:15]
    cambian = [p for p in P.values() if p["ult23"]["gana"] != p["ult_med"]["gana"]]
    em = sorted(P.values(), key=lambda p: p["ult_med"]["falta"])[:15]
    p0 = e23[0]
    resp3 = (f"En las elecciones de julio de 2023 el escaño más ajustado fue el de {E(ps[p0['pc']][0])}: {art(p0['ult23']['pierde'])} se quedó a {nes(round(p0['ult23']['falta']))} votos de quitárselo a {art(p0['ult23']['gana'])}. "
             f"Con la media de los sondeos, el último escaño cambiaría de manos en {len(cambian)} provincias: {nombres(cambian, 8)}.")
    cuerpo3 = (f"{CSS}<p class='meta'>Actualizado el {fecha_es(FECHA)} · Resultados oficiales de 2023 y proyección con los sondeos hasta el {fs}</p><p class='ans'>{resp3}</p>"
               "<h2>1. Qué es el último escaño</h2><p>En cada provincia se reparten los escaños con la regla D'Hondt: el último lo gana el partido con el mejor cociente que queda. La diferencia de votos con el siguiente aspirante mide lo ajustado que estuvo. "
               "Con pocos votos más, ese escaño habría cambiado de partido. <a href='/atalaya/fichas/circunscripciones/'>Cómo funciona el reparto</a>.</p>"
               f"<h2>2. Los 15 escaños más ajustados de 2023</h2>{cab_esc}{''.join(fila_esc(p, p['ult23']) for p in e23)}</tbody></table>"
               "<p>Cálculo propio con los votos oficiales del <a href='https://infoelectoral.interior.gob.es/'>Ministerio del Interior</a> y la barrera del 3 %.</p>"
               f"<h2>3. Con la media de los sondeos</h2><p>Aplicando el cambio de voto de los sondeos a los votos de 2023, estos serían los 15 últimos escaños más ajustados:</p>{cab_esc}{''.join(fila_esc(p, p['ult_med']) for p in em)}</tbody></table>"
               f"<h2>4. Provincias donde el último escaño cambia de manos</h2><p>Provincias en las que el partido que se lleva el último escaño con la media de sondeos es distinto al de 2023:</p><ul>"
               + "".join(f"<li>{link(p['pc'])}: {art(p['ult23']['gana'])} en 2023, {art(p['ult_med']['gana'])} con los sondeos.</li>" for p in cambian) + "</ul>"
               "<p class='warn'>Es una proyección orientativa que supone el mismo cambio de voto en todas las provincias. Un escaño ajustado en una proyección puede resolverse por unos pocos cientos de votos reales.</p>"
               "<p>Más: <a href='/atalaya/fichas/cambio/'>provincias que pueden cambiar de partido</a>.</p>")
    faqs3 = [("¿Qué escaños están más en el aire en las elecciones generales?", resp3),
             ("¿Qué es el último escaño de una provincia?", "El último de los escaños que reparte la regla D'Hondt en una circunscripción: lo gana el partido con el mejor cociente restante."),
             ("¿Cuántos votos pueden decidir un escaño?", f"En 2023, el escaño más ajustado se decidió por {nes(round(p0['ult23']['falta']))} votos en {ps[p0['pc']][0]}.")]
    publicar("cambio/escanos/", "Escaños más ajustados: qué escaños pueden cambiar de partido el 29N", "Los escaños que se decidieron por menos votos en 2023 y los que cambiarían de partido con los últimos sondeos.",
             "¿Qué escaños están más en el aire en las elecciones del 29N?", cuerpo3 + "<h2>Preguntas frecuentes</h2>" + "".join(f"<details><summary>{E(a)}</summary><p>{E(b)}</p></details>" for a, b in faqs3), faqs3, "Escaños en el aire")

    # ---------------- 4. FICHAS POR PARTIDO ----------------
    for k in ("PP", "PSOE", "VOX", "SUMAR"):
        n23, nmd, rg = V["t23"].get(k, 0), V["t_med"].get(k, 0), V["t_rango"][k]
        filas_p = []
        for p in P.values():
            a = p["seats23"].get(k, 0); b = p["seats_med"].get(k, 0); lo, hi = p["seats_rango"].get(k, (0, 0))
            if a or b or hi: filas_p.append((p, a, b, lo, hi))
        gan = sorted([x for x in filas_p if x[2] > x[1]], key=lambda x: -(x[2] - x[1]))
        per = sorted([x for x in filas_p if x[2] < x[1]], key=lambda x: x[2] - x[1])
        aire_ = [x for x in filas_p if x[2] == x[1] and (x[3] < x[1] or x[4] > x[1])]
        dlt = lambda n: f"{n:+d}".replace("-", "−")
        fila = lambda x: f"<tr><td>{link(x[0]['pc'])}</td><td>{x[1]}</td><td><b>{x[2]}</b></td><td>{x[3]}–{x[4]}</td><td>{dlt(x[2] - x[1])}</td></tr>"
        cab = "<table class='t'><thead><tr><th>Provincia</th><th>Escaños 2023</th><th>Con la media de sondeos</th><th>Rango entre sondeos</th><th>Cambio</th></tr></thead><tbody>"
        sub = lambda lista, tit, vacio: (f"<h2>{tit}</h2>" + (cab + "".join(fila(x) for x in lista) + "</tbody></table>" if lista else f"<p>{vacio}</p>"))
        d = nmd - n23
        if d > 0: tendencia = f"ganaría {d} escaños respecto a 2023"
        elif d < 0: tendencia = f"perdería {-d} escaños respecto a 2023"
        else: tendencia = "mantendría sus escaños de 2023"
        pg = ", ".join(f"{E(ps[x[0]['pc']][0])} ({dlt(x[2] - x[1])})" for x in gan[:5]) or "ninguna"
        pp_ = ", ".join(f"{E(ps[x[0]['pc']][0])} ({dlt(x[2] - x[1])})" for x in per[:5]) or "ninguna"
        resp4 = (f"Con la media de los sondeos de los últimos 30 días, {art(k)} {tendencia} ({n23} en 2023 → {nmd}, con un rango entre sondeos de {rg[0]} a {rg[1]}). "
                 f"Las provincias donde más ganaría son {pg}; donde más perdería, {pp_}.")
        q4 = f"¿En qué provincias puede ganar o perder escaños {art(k)} en las elecciones del 29N?"
        cuerpo4 = (f"{CSS}<p class='meta'>Actualizado el {fecha_es(FECHA)} · Proyección con {n_son} sondeos hasta el {fs}</p><p class='ans'>{E(resp4)}</p>"
                   "<p>La proyección aplica a los votos oficiales de 2023 de cada provincia el cambio nacional que indican los sondeos, con la barrera del 3 % y el reparto D'Hondt. El rango muestra el mínimo y el máximo entre los sondeos recientes: "
                   "si es amplio, el escaño está en el aire. <a href='/atalaya/fichas/espana/'>Método completo</a>.</p>"
                   + sub(gan, f"1. Provincias donde {E(art(k))} ganaría escaños", "Con la media de sondeos no gana escaños en ninguna provincia.")
                   + sub(per, f"2. Provincias donde {E(art(k))} perdería escaños", "Con la media de sondeos no pierde escaños en ninguna provincia.")
                   + sub(aire_, f"3. Escaños en el aire (la media no cambia, pero algún sondeo sí)", "No hay provincias con escaños en el aire para este partido.")
                   + "<p class='warn'>Es una proyección orientativa: supone el mismo cambio de voto en todas las provincias y no hay encuestas provinciales. No es una previsión oficial.</p>"
                   "<p>Más: <a href='/atalaya/fichas/cambio/'>provincias que pueden cambiar de partido</a> · <a href='/atalaya/fichas/cambio/escanos/'>escaños en el aire</a>.</p>")
        faqs4 = [(q4, resp4),
                 (f"¿Cuántos escaños tiene {art(k)} ahora?", f"{n23} escaños en el Congreso tras las elecciones de julio de 2023." if k != "SUMAR" else f"Sumar obtuvo {n23} escaños en 2023; después, su grupo parlamentario se redujo por salidas."),
                 (f"¿Cuántos escaños sacaría {art(k)} según las encuestas?", f"Unos {nmd} con la media de sondeos, con un rango de {rg[0]} a {rg[1]} según el sondeo.")]
        publicar(f"cambio/{slug(nom(k))}/", f"¿Dónde puede ganar o perder escaños {nom(k)} el 29N? Provincia a provincia", f"{Art(k)} {tendencia} con los últimos sondeos: provincias donde gana o pierde escaños, rango entre sondeos y escaños en el aire.",
                 q4, cuerpo4 + "<h2>Preguntas frecuentes</h2>" + "".join(f"<details><summary>{E(a)}</summary><p>{E(b)}</p></details>" for a, b in faqs4), faqs4, f"Escaños de {nom(k)} en juego")

    # ---------------- 5. CIUDADES ----------------
    CG = {k: sorted([x for x in C if x["cat"] == k], key=lambda x: x["mm"]) for k in ORD}
    def fila_c(x):
        return (f"<tr><td>{E(x['n'])} ({link(x['pc'])})</td><td>{nes(x['pob'])}</td><td>{E(Art(x['l23']))} (+{f1(x['m23'])})</td><td>{E(Art(x['lm']))} (+{f1(x['mm'])})</td><td>{x['flips']} de {x['npol']}</td><td>{chip(x['cat'])}</td></tr>")
    cab_c = ("<table class='t'><thead><tr><th>Ciudad (provincia)</th><th>Habitantes</th><th>Más votado en 2023 (margen)</th><th>Con la media de sondeos</th><th>Sondeos con vuelco</th><th>Situación</th></tr></thead><tbody>")
    pasan = {}
    for x in CG["cambio"]: pasan[(x["l23"], x["lm"])] = pasan.get((x["l23"], x["lm"]), 0) + 1
    de_ = lambda k: ("del " + nom(k)) if nom(k) in ("PP", "PSOE") else "de " + nom(k)
    al_ = lambda k: ("al " + nom(k)) if nom(k) in ("PP", "PSOE") else "a " + nom(k)
    desg = ", ".join(f"{n} {de_(a)} {al_(b)}" for (a, b), n in sorted(pasan.items(), key=lambda kv: -kv[1]))
    grandes = sorted(CG["cambio"] + CG["aire"], key=lambda x: -x["pob"])[:5]
    gr_txt = ", ".join("%s (%s)" % (E(x["n"]), nes(x["pob"])) for x in grandes)
    resp5 = (f"De las {len(C)} ciudades de más de 50.000 habitantes, {len(CG['cambio'])} cambiarían de partido más votado en unas generales con la media de los sondeos actuales ({desg}) y {len(CG['aire'])} están en el aire. "
             f"Entre las más pobladas en juego están {gr_txt}.")
    rel_c = "".join(f"<h2>{i}. {t}</h2>" + (f"<p>{d}</p>" if d else "") + cab_c + "".join(fila_c(x) for x in CG[k]) + "</tbody></table>"
                    for i, (k, t, d) in enumerate([("cambio", "Ciudades con cambio proyectado", "Con la media de sondeos gana un partido distinto al de 2023."),
                                                   ("aire", "Ciudades en el aire", f"Mantienen al mismo partido con la media, pero con menos de {UMBRAL_AIRE:.0f} puntos de margen o con vuelco en algún sondeo."),
                                                   ("corta", "Ciudades con ventaja corta", f"Entre {UMBRAL_AIRE:.0f} y {UMBRAL_CORTA:.0f} puntos de margen proyectado.")], 2))
    cuerpo5 = (f"{CSS}<p class='meta'>Actualizado el {fecha_es(FECHA)} · Resultados municipales de las elecciones generales de julio de 2023 (Interior)</p><p class='ans'>{E(resp5)}</p>"
               "<h2>1. Qué se mide</h2><p>Se usa el voto al <b>Congreso de los Diputados en julio de 2023</b> en cada municipio (no las elecciones municipales) y se le aplica el cambio nacional que indican los sondeos de los últimos 30 días. "
               f"Una ciudad «cambia de partido» cuando el partido más votado en ella sería distinto al de 2023. Se analizan las {len(C)} ciudades de más de 50.000 habitantes.</p>"
               + rel_c +
               "<p class='warn'>Es una estimación muy orientativa: supone el mismo cambio de voto en todas las ciudades, y el voto urbano puede moverse distinto del provincial. No hay encuestas municipales. "
               "No equivale a quién ganará la alcaldía: las <a href='/atalaya/fichas/'>fichas</a> se refieren a las elecciones generales.</p>"
               "<p>Más: <a href='/atalaya/fichas/cambio/'>provincias que pueden cambiar de partido</a> · <a href='/atalaya/fichas/cambio/historico/'>histórico por provincia</a>.</p>")
    faqs5 = [("¿Qué ciudades pueden cambiar de partido más votado en las elecciones generales?", resp5),
             ("¿Qué ciudades están más igualadas?", "Las que tienen menos de tres puntos de margen proyectado entre el primero y el segundo: " + ", ".join(E(x["n"]) for x in (CG["aire"][:8])) + "."),
             ("¿Esto sirve para saber quién ganará la alcaldía?", "No. Usa el voto a las elecciones generales de julio de 2023 en cada municipio, no el de las municipales.")]
    publicar("cambio/ciudades/", "¿Qué ciudades pueden cambiar de partido el 29N? Ciudades en juego", "Ciudades de más de 50.000 habitantes que pueden cambiar de partido más votado el 29N, con el voto de 2023 y los últimos sondeos.",
             "¿Qué ciudades pueden cambiar de partido más votado en las elecciones del 29N?", cuerpo5 + "<h2>Preguntas frecuentes</h2>" + "".join(f"<details><summary>{E(a)}</summary><p>{E(b)}</p></details>" for a, b in faqs5), faqs5, "Ciudades en juego")

    # ---------------- bloque para cada ficha de provincia ----------------
    def bloque(pc):
        p = P[pc]
        u = p["ult_med"]
        return (f"{CSS}<h2>¿Puede cambiar de partido {E(ps[pc][0])}?</h2><p>{chip(p['cat'])} {E(frase(p))}</p>"
                f"<p>El último escaño en 2023 lo ganó {art(p['ult23']['gana'])} y {art(p['ult23']['pierde'])} se quedó a {nes(round(p['ult23']['falta']))} votos de quitárselo. "
                f"<a href='/atalaya/fichas/cambio/'>Todas las provincias que pueden cambiar</a> · <a href='/atalaya/fichas/cambio/historico/'>histórico</a> · <a href='/atalaya/fichas/cambio/escanos/'>escaños en el aire</a>.</p>")
    return bloque, frase
