"""Atalaya: fichas de las 17 comunidades autónomas «¿Quién ganará las elecciones generales en <comunidad>?» (las invoca build_fichas.py).

  /atalaya/fichas/comunidad/<slug>/

Agregan, sin datos nuevos, lo que ya hay por provincia: escaños de 2023 y proyección con la media de sondeos (volatilidad.py),
votos oficiales de 2023 (Interior), padrón y renta (INE), cargos vigentes (politicos_prov.json) y clima de prensa.
La proyección es el mismo cambio proporcional uniforme de la ficha nacional: no hay encuestas autonómicas.
Ceuta y Melilla son ciudades autónomas, no comunidades: siguen con su ficha provincial.
"""
import re

# nombre -> (slug, «en …», código de provincias)
CCAA = {
    "Andalucía": ("andalucia", "en Andalucía", "04 11 14 18 21 23 29 41"),
    "Aragón": ("aragon", "en Aragón", "22 44 50"),
    "Asturias": ("asturias", "en Asturias", "33"),
    "Baleares": ("baleares", "en las Islas Baleares", "07"),
    "Canarias": ("canarias", "en Canarias", "35 38"),
    "Cantabria": ("cantabria", "en Cantabria", "39"),
    "Castilla y León": ("castilla-y-leon", "en Castilla y León", "05 09 24 34 37 40 42 47 49"),
    "Castilla-La Mancha": ("castilla-la-mancha", "en Castilla-La Mancha", "02 13 16 19 45"),
    "Cataluña": ("cataluna", "en Cataluña", "08 17 25 43"),
    "Comunidad Valenciana": ("comunidad-valenciana", "en la Comunidad Valenciana", "03 12 46"),
    "Extremadura": ("extremadura", "en Extremadura", "06 10"),
    "Galicia": ("galicia", "en Galicia", "15 27 32 36"),
    "Madrid": ("madrid", "en la Comunidad de Madrid", "28"),
    "Murcia": ("murcia", "en la Región de Murcia", "30"),
    "Navarra": ("navarra", "en Navarra", "31"),
    "País Vasco": ("pais-vasco", "en el País Vasco", "01 20 48"),
    "La Rioja": ("la-rioja", "en La Rioja", "26"),
}
PROV2CCAA = {p: n for n, (_, _, ps) in CCAA.items() for p in ps.split()}
# presidentes autonómicos con ficha «Promesas vs. Hechos»
FICHA_PRESIDENTE = {"Castilla y León": ("politico/manueco/", "Alfonso Fernández Mañueco"), "Madrid": ("politico/ayuso/", "Isabel Díaz Ayuso")}


def ccaa_de(pc):
    """(nombre, ruta) de la comunidad de una provincia, o None (Ceuta y Melilla)."""
    n = PROV2CCAA.get(pc)
    return (n, f"comunidad/{CCAA[n][0]}/") if n else None


def _art(p, cap=False):
    s = ("el " + p) if p in ("PP", "PSOE") else p
    return s[:1].upper() + s[1:] if cap else s


def _c1(x):
    return f"{x:.1f}".replace(".", ",")


def generar(c):
    E, BASE, FECHA, fecha_es, nes, pagina, J, D = (c[k] for k in ("E", "BASE", "FECHA", "fecha_es", "nes", "pagina", "J", "D"))
    VOL, ps_, clima, nom, titulares, nacional, RC = c["VOL"], c["ps"], c["clima"], c["nom"], c["titulares"], c["nacional"], c["RC"]
    pad = J(D / "padron.json"); anio_pad = pad["anios"][0]
    dem = J(D / "demografia.json")
    pol = J(D / "politicos_prov.json")["prov"]
    orden_n = sorted(nacional.items(), key=lambda x: -x[1]); lider_n = orden_n[0][0]
    urls, hub = [], []
    # voto CERA por comunidad: suma de las provincias, generales 2016 (INE, atalaya/data/cera.json)
    CERA = {}
    try:
        cj = J(D / "cera.json"); cprov = cj["ine"]["provincias"]; cnac = cj["ine"]["nacional"].get("generales-2016", {})
        for n_, (_, _, cd_) in CCAA.items():
            vs = [cprov[x]["generales-2016"] for x in cd_.split() if cprov.get(x, {}).get("generales-2016")]
            if vs and len(vs) == len(cd_.split()):
                ce = sum(v["cera"] for v in vs); tot = sum(v["total"] for v in vs)
                CERA[n_] = {"cera": ce, "pct": 100 * ce / tot, "part": sum(v["cera"] * v["part"] for v in vs) / ce}
        CERA_ORDEN = sorted(CERA, key=lambda k: -CERA[k]["cera"])
    except (OSError, KeyError, ValueError):
        CERA, CERA_ORDEN, cnac = {}, [], {}

    for nombre, (sl, en_, cods) in CCAA.items():
        pcs = cods.split(); ruta = f"comunidad/{sl}/"
        P = [VOL["P"][pc] for pc in pcs]
        N = sum(p["escanos"] for p in P)
        # escaños 2023 y proyección con la media de sondeos
        s23, smed = {}, {}
        for p in P:
            for k, v in p["seats23"].items(): s23[nom(k)] = s23.get(nom(k), 0) + v
            for k, v in p["seats_med"].items(): smed[nom(k)] = smed.get(nom(k), 0) + v
        o23 = sorted(s23.items(), key=lambda kv: -kv[1]); omed = sorted(smed.items(), key=lambda kv: -kv[1])
        L23 = o23[0][0]; empate = len(o23) > 1 and o23[1][1] == o23[0][1]
        cambian = [p for p in P if p["cat"] == "cambio"]
        txt23 = ", ".join(f"{k} {v}" for k, v in o23[:5])
        txtm = ", ".join(f"{k} {v}" for k, v in omed[:5])
        resp = (f"En 2023, {nombre} eligió {N} diputados al Congreso: {txt23}. "
                + ("Hubo empate en cabeza. " if empate else f"{_art(L23, True)} fue la fuerza con más escaños. ")
                + f"Trasladando a los votos de 2023 la media de sondeos recientes (proyección orientativa, sin encuestas autonómicas), el reparto sería {txtm}."
                + (f" El partido más votado cambiaría en {len(cambian)} de {len(P)} provincias: {', '.join(ps_[p['pc']][0] for p in cambian)}." if cambian
                   else " Ninguna de sus provincias cambiaría de partido más votado con esa proyección."))
        desc = f"Escaños, resultados de 2023, proyección con sondeos y datos de {nombre}: {N} diputados en juego el 29N."

        # tabla por provincia
        filas = ""
        for p in P:
            nm, rt = ps_[p["pc"]]
            lm = f"{E(nom(p['lm']))}" + (" (cambio)" if p["cat"] == "cambio" else "")
            filas += (f"<tr><td><a href='/atalaya/fichas/{rt}'>{E(nm)}</a></td><td>{p['escanos']}</td><td>{E(nom(p['l23']))}</td><td>{lm}</td><td>{_c1(p['mm'])}</td></tr>")
        tabla = ("<table><thead><tr><th>Provincia</th><th>Diputados</th><th>Más votado 2023</th><th>Más votado con sondeos</th><th>Ventaja proyectada (pts)</th></tr></thead>"
                 f"<tbody>{filas}</tbody></table>")
        uni = (f"<p>{E(nombre)} es una comunidad uniprovincial: su circunscripción electoral coincide con la comunidad. Detalle en la <a href='/atalaya/fichas/{ps_[pcs[0]][1]}'>ficha de {E(ps_[pcs[0]][0])}</a>.</p>" if len(pcs) == 1 else "")

        # votos oficiales 2023 agregados
        tot, validos, votantes, censo = {}, 0, 0, 0
        for pc in pcs:
            rc = ((RC or {}).get("prov") or {}).get(pc)
            if rc and rc["validos"]:
                validos += rc["validos"]; votantes += rc["votantes"]; censo += rc["censo"]
                for k, v in rc["v"].items():
                    a = tot.setdefault(nom(k), [0, 0]); a[0] += v[0]; a[1] += v[1]
        votos = ""
        if validos:
            top = sorted(tot.items(), key=lambda kv: -kv[1][0])[:6]
            votos = (f"<h2>Votos en las generales de julio de 2023 (datos oficiales)</h2><p>Votaron {nes(votantes)} personas" + (f" (participación del {_c1(100 * votantes / censo)} %)" if censo else "")
                     + ". Reparto de los votos válidos: " + ", ".join(f"{E(k)} {_c1(100 * v[0] / validos)} % ({v[1]} escaño{'s' if v[1] != 1 else ''})" for k, v in top)
                     + ". Fuente: <a href='https://infoelectoral.interior.gob.es/'>Ministerio del Interior</a>.</p>")

        # gobierno autonómico y capitales
        pres = next((g for pc in pcs for g in (pol.get(pc) or {}).get("gobierno", []) if g["ambito"] == "autonómico"), None)
        alc = [g for pc in pcs for g in (pol.get(pc) or {}).get("gobierno", []) if g["ambito"] == "municipal"]
        gob = ""
        if pres or alc:
            li = ""
            for g in ([pres] if pres else []) + alc:
                ver = "" if str(g.get("fuente", "")).startswith("Wikidata") else " <span class='meta'>(Wikipedia; por verificar)</span>"
                pt = f" <span class='meta'>({E(g['partido'])})</span>" if g.get("partido") else ""
                li += f"<li><b>{E(g['rol'])}</b>: {E(g['nombre'])}{pt}{ver}</li>"
            fp = FICHA_PRESIDENTE.get(nombre)
            gob = (f"<h2>Quién gobierna {E(en_)}</h2><ul>{li}</ul>"
                   + (f"<p>Su gestión, contrastada con su investidura: <a href='/atalaya/fichas/{fp[0]}'>{E(fp[1])}: promesas y datos</a>.</p>" if fp else "")
                   + "<p class='meta'>Cargos vigentes según Wikidata y, donde falta, Wikipedia. Capitales de provincia con alcalde disponible.</p>")

        # demografía ponderada por población
        pob = {pc: (pad["prov"].get(pc) or [None])[0] for pc in pcs}
        pt_ = sum(v for v in pob.values() if v)
        dtxt = ""
        pw = [(pob[pc], dem["prov"].get(pc)) for pc in pcs if pob[pc] and dem["prov"].get(pc) and dem["prov"][pc][0] is not None and dem["prov"][pc][3] is not None]
        if pt_ and len(pw) == len(pcs):
            w = lambda i: sum(a * d[i] for a, d in pw) / sum(a for a, _ in pw)
            es_ = dem["esp"]
            dtxt = (f"<h2>Población y renta</h2><p>{E(nombre)} tiene {nes(pt_)} habitantes (INE, 1 de enero de {anio_pad}), unos {nes(round(pt_ / N))} por diputado. "
                    f"La edad media es de {_c1(w(0))} años (España, {_c1(es_[0])}); un {_c1(w(2))} % tiene 65 años o más. La renta neta media por persona es de {nes(round(w(3)))} euros ({nes(round(es_[3]))} en España), "
                    f"según el Atlas de renta de los hogares del INE de {dem['anio']}. Medias de sus provincias ponderadas por población.</p>")

        # voto CERA
        cera_h = ""
        if nombre in CERA:
            cc = CERA[nombre]; pos = CERA_ORDEN.index(nombre) + 1
            media = f" (media nacional: {_c1(cnac['part'])} %)" if cnac.get("part") is not None else ""
            cera_h = (f"<h2>Voto CERA {E(en_)}</h2>"
                      "<p>El voto CERA es el de los españoles que viven en el extranjero. Su recuento llega unos días después de la noche electoral y ha cambiado escaños en 1993, 2019 y 2023. "
                      f"En las elecciones generales de 2016, según el INE, {E(nombre)} sumaba {nes(int(cc['cera']))} electores CERA, el {_c1(cc['pct'])} % de su censo, y es la {pos}.ª comunidad de {len(CERA)} por número de electores CERA. "
                      f"Votó el {_c1(cc['part'])} % de ellos{media}.</p>"
                      "<p class='meta'>Fuente: <a href='https://ine.es/jaxiPx/Tabla.htm?L=0&amp;tpx=32091'>INE, tabla 32091</a>; suma de las provincias, con la participación ponderada por electores. "
                      "Más cifras y la evolución desde 2008 en el <a href='/atalaya/cera/'>panel del voto CERA</a>.</p>")

        # prensa: agregado y titulares recientes
        cl = {"n": 0, "neg": 0, "pos": 0, "riesgo": 0, "temas": {}}
        for pc in pcs:
            x = clima.get(pc)
            if x:
                for k in ("n", "neg", "pos", "riesgo"): cl[k] += x[k]
                for t_, n_ in x["temas"].items(): cl["temas"][t_] = cl["temas"].get(t_, 0) + n_
        prensa = ""
        if cl["n"] >= 15:
            pct = lambda k: round(100 * cl[k] / cl["n"])
            temas = ", ".join(t for t, _ in sorted(((t, n) for t, n in cl["temas"].items() if t != "otros"), key=lambda kv: -kv[1])[:3])
            prensa = (f"<h2>El clima de prensa</h2><p>De {cl['n']} titulares recientes sobre las provincias de {E(nombre)} clasificados de forma automática, un {pct('neg')} % tiene tono negativo, "
                      f"un {100 - pct('neg') - pct('pos')} % neutro y un {pct('pos')} % positivo. Temas más frecuentes: {E(temas)}. Estimación orientativa hecha solo con el titular; no equivale a una encuesta.</p>")
        tit = {}
        for pc in pcs:
            for x in titulares(pc, ps_[pc][0], 5): tit[x["u"]] = x
        tit = sorted(tit.values(), key=lambda x: x["f"], reverse=True)[:6]
        senal = ("<h2>Señales recientes</h2><ul>" + "".join(
            f"<li><a href='{E(x['u'])}' rel='nofollow noopener'>{E(re.sub(chr(32)+'-'+chr(32)+'[^-]{3,60}$', '', x['t']))}</a> <span class='meta'>({E(x['m'])}, {fecha_es(x['f'])})</span></li>" for x in tit) + "</ul>") if tit else ""

        # cabezas de lista
        cab = ""
        if len(pcs) > 1:
            li = ""
            for pc in pcs:
                cs = (pol.get(pc) or {}).get("candidatos") or []
                if cs:
                    li += f"<li><a href='/atalaya/fichas/{ps_[pc][1]}'>{E(ps_[pc][0])}</a>: " + "; ".join(f"{E(x['partido'])} {E(x['nombre'])}" for x in cs if x["partido"] in ("PP", "PSOE", "VOX")) + "</li>"
            if li: cab = f"<h2>Cabezas de lista de PP, PSOE y Vox por provincia</h2><ul>{li}</ul><p class='meta'>Según el cuadro de candidaturas de <a href='https://es.wikipedia.org/wiki/Elecciones_generales_de_Espa%C3%B1a_de_2026'>Wikipedia</a>; se confirman al proclamarse oficialmente.</p>"

        otras = "".join(f"<li><a href='/atalaya/fichas/{r}'>{E(n)}</a></li>" for n, (s_, _, _) in CCAA.items() if n != nombre for r in [f"comunidad/{s_}/"])
        faqs = [(f"¿Quién ganará las elecciones generales {en_}?", resp),
                (f"¿Cuántos diputados elige {nombre} al Congreso?", f"{nombre} elige {N} diputados al Congreso de los Diputados, repartidos en {len(pcs)} circunscripción{'es' if len(pcs) != 1 else ''}."),
                (f"¿Qué partido ganó en {nombre} en las generales de 2023?", (f"Hubo empate en cabeza en escaños: {txt23}." if empate else f"{_art(L23, True)} fue el partido con más escaños en {nombre} en 2023 ({txt23}).")),
                (f"¿Puede cambiar de partido {nombre} en las elecciones del 29N?", (f"Con la proyección de sondeos recientes, el partido más votado cambiaría en {len(cambian)} de {len(P)} provincias." if cambian else "Con la proyección de sondeos recientes, ninguna provincia cambiaría de partido más votado. Es una proyección orientativa, no una previsión.")),
                ("¿Cuándo son las próximas elecciones generales?", "Las elecciones generales se celebran el 29 de noviembre de 2026.")]
        if pres: faqs.insert(2, (f"¿Quién preside {nombre}?", f"{pres['nombre']}" + (f" ({pres['partido']})" if pres.get("partido") else "") + ", según Wikidata y Wikipedia."))
        if nombre in CERA: faqs.append((f"¿Cuántos electores CERA hay {en_}?", f"En las elecciones generales de 2016, según el INE, {nombre} sumaba {nes(int(CERA[nombre]['cera']))} electores CERA (españoles residentes en el extranjero), el {_c1(CERA[nombre]['pct'])} % de su censo electoral."))
        if pt_: faqs.append((f"¿Cuántos habitantes tiene {nombre}?", f"{nombre} tiene {nes(pt_)} habitantes según el padrón del INE a 1 de enero de {anio_pad}."))
        faq_html = "<h2>Preguntas frecuentes</h2>" + "".join(f"<details><summary>{E(a)}</summary><p>{E(b)}</p></details>" for a, b in faqs)
        q = f"¿Quién ganará las elecciones generales {en_}?"
        cuerpo = (f"<p class='meta'>Actualizado el {fecha_es(FECHA)} · Elecciones generales del 29 de noviembre de 2026</p><p class='ans'>{E(resp)}</p>"
                  f"<h2>1. Provincias y diputados</h2>{uni}{tabla}"
                  f"<p class='meta'>«Más votado con sondeos»: se aplica a los votos de 2023 de cada provincia el cambio proporcional de la media de sondeos nacionales y se reparten los escaños con D'Hondt y barrera del 3 %. Ventaja = puntos entre el primero y el segundo.</p>"
                  f"{votos}{gob}{cab}{dtxt}{cera_h}{prensa}{senal}"
                  "<h2>Lo que este análisis no incluye</h2><p class='warn'>No hay encuestas autonómicas: la proyección supone que el cambio nacional se repite igual en todas las provincias. Es un ejercicio orientativo, no una encuesta ni una previsión oficial.</p>"
                  f"{faq_html}<h2>Otras comunidades</h2><ul>{otras}</ul>"
                  "<h2>Fuentes y método</h2><ul><li>Escaños y votos de 2023: Ministerio del Interior y Wikipedia.</li><li>Sondeos: media ponderada en <a href='/elecciones-espana/'>Elecciones en España</a>.</li>"
                  "<li>Población, renta y voto CERA: INE.</li><li>Cargos y candidaturas: Wikidata y Wikipedia.</li><li>Prensa: titulares por RSS clasificados automáticamente.</li></ul>"
                  "<p class='meta'><a href='/atalaya/fichas/metodologia/'>Metodología y fuentes de Atalaya</a></p>")
        ld = [{"@context": "https://schema.org", "@type": "Article", "headline": q, "description": desc, "inLanguage": "es", "datePublished": FECHA, "dateModified": FECHA,
               "author": {"@type": "Person", "name": "Emilio Rodríguez García", "url": f"{BASE}/sobre-mi"}, "publisher": {"@type": "Person", "name": "Emilio Rodríguez García"},
               "mainEntityOfPage": f"{BASE}/atalaya/fichas/{ruta}", "about": nombre},
              {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": a, "acceptedAnswer": {"@type": "Answer", "text": b}} for a, b in faqs]},
              {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                  {"@type": "ListItem", "position": 1, "name": "Atalaya", "item": f"{BASE}/atalaya/"},
                  {"@type": "ListItem", "position": 2, "name": "Fichas", "item": f"{BASE}/atalaya/fichas/"},
                  {"@type": "ListItem", "position": 3, "name": nombre, "item": f"{BASE}/atalaya/fichas/{ruta}"}]}]
        pagina(ruta, f"¿Quién ganará las elecciones {en_}? Escaños y datos (29N 2026)", desc, q, cuerpo, ld,
               f"<a href='/atalaya/'>Atalaya</a> › <a href='/atalaya/fichas/'>Fichas</a> › {E(nombre)}")
        urls.append(f"{BASE}/atalaya/fichas/{ruta}"); hub.append((nombre, ruta, N))
    return urls, hub
