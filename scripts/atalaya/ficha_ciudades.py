"""Atalaya: fichas de las 52 capitales de provincia «¿Qué vota <ciudad> y quién la gobierna?» (las invoca build_fichas.py).

  /atalaya/fichas/ciudad/<slug>/

Solo datos del repositorio: votos por municipio de las generales (julio 2023) y municipales (mayo 2023) de Interior, padrón y renta del INE,
alcalde vigente (politicos_prov.json, Wikidata/Wikipedia), proyección con la media de sondeos (mismo cambio proporcional que la ficha nacional)
y titulares que nombran la ciudad. «Más votado» no es «alcalde»: tras las municipales gobiernan los pactos.
"""
import re
import unicodedata

# provincia -> (código INE del municipio capital, nombre en español)
CAPITALES = {
    "01": ("01059", "Vitoria-Gasteiz"), "02": ("02003", "Albacete"), "03": ("03014", "Alicante"), "04": ("04013", "Almería"), "05": ("05019", "Ávila"),
    "06": ("06015", "Badajoz"), "07": ("07040", "Palma"), "08": ("08019", "Barcelona"), "09": ("09059", "Burgos"), "10": ("10037", "Cáceres"),
    "11": ("11012", "Cádiz"), "12": ("12040", "Castellón de la Plana"), "13": ("13034", "Ciudad Real"), "14": ("14021", "Córdoba"), "15": ("15030", "A Coruña"),
    "16": ("16078", "Cuenca"), "17": ("17079", "Girona"), "18": ("18087", "Granada"), "19": ("19130", "Guadalajara"), "20": ("20069", "San Sebastián"),
    "21": ("21041", "Huelva"), "22": ("22125", "Huesca"), "23": ("23050", "Jaén"), "24": ("24089", "León"), "25": ("25120", "Lleida"),
    "26": ("26089", "Logroño"), "27": ("27028", "Lugo"), "28": ("28079", "Madrid"), "29": ("29067", "Málaga"), "30": ("30030", "Murcia"),
    "31": ("31201", "Pamplona"), "32": ("32054", "Ourense"), "33": ("33044", "Oviedo"), "34": ("34120", "Palencia"), "35": ("35016", "Las Palmas de Gran Canaria"),
    "36": ("36038", "Pontevedra"), "37": ("37274", "Salamanca"), "38": ("38038", "Santa Cruz de Tenerife"), "39": ("39075", "Santander"), "40": ("40194", "Segovia"),
    "41": ("41091", "Sevilla"), "42": ("42173", "Soria"), "43": ("43148", "Tarragona"), "44": ("44216", "Teruel"), "45": ("45168", "Toledo"),
    "46": ("46250", "Valencia"), "47": ("47186", "Valladolid"), "48": ("48020", "Bilbao"), "49": ("49275", "Zamora"), "50": ("50297", "Zaragoza"),
    "51": ("51001", "Ceuta"), "52": ("52001", "Melilla"),
}
AGREGADOS = {"Total votos a candidatos", "Votos"}
# fichas de político que ya existen para un alcalde
FICHA_ALCALDE = {"37": ("politico/garcia-carbayo/", "Carlos García Carbayo")}


def _slug(s):
    return re.sub(r"[^a-z0-9]+", "-", unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()).strip("-")


def _nrm(t):
    return unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower()


def _c1(x):
    return f"{x:.1f}".replace(".", ",")


def ruta_capital(pc):
    """(nombre, ruta) de la capital de una provincia."""
    n = CAPITALES[pc][1]
    return n, f"ciudad/{_slug(n)}/"


def _art(p, cap=False):
    s = ("el " + p) if p in ("PP", "PSOE") else p
    return s[:1].upper() + s[1:] if cap else s


def generar(c):
    E, BASE, FECHA, fecha_es, nes, pagina, J, D = (c[k] for k in ("E", "BASE", "FECHA", "fecha_es", "nes", "pagina", "J", "D"))
    VOL, ps_, nom, lider = c["VOL"], c["ps"], c["nom"], c["lider"]
    pad = J(D / "padron.json"); anios = pad["anios"]
    dem = J(D / "demografia.json")
    pol = J(D / "politicos_prov.json")["prov"]
    noticias = J(D / "noticias.json")["noticias"]
    cod_ccaa = c["ccaa_de"]
    urls, hub = [], []
    # voto CERA: el INE solo lo publica por provincia (generales 2016, atalaya/data/cera.json)
    try:
        cj = J(D / "cera.json"); cprov = cj["ine"]["provincias"]; cnac = cj["ine"]["nacional"].get("generales-2016", {})
        cera_orden = sorted((x["generales-2016"]["cera"] for x in cprov.values() if x.get("generales-2016")), reverse=True)
    except (OSError, KeyError, ValueError):
        cprov, cnac, cera_orden = {}, {}, []

    for pc, (code, nombre) in CAPITALES.items():
        ruta = f"ciudad/{_slug(nombre)}/"
        prov_n, prov_r = ps_[pc]
        gen = J(D / f"resultados/congreso-2023-07/{pc}.json")["mun"].get(code)
        mun = J(D / f"resultados/municipales-2023-05/{pc}.json")["mun"].get(code)
        if not gen or not mun:
            print("Sin resultados:", nombre); continue
        pob = gen["pob"]; serie = pad["mun"].get(code) or []
        gob = (pol.get(pc) or {}).get("gobierno", [])
        alc = next((g for g in gob if g["ambito"] == "municipal"), None)
        cc = cod_ccaa(pc)

        # generales 2023
        vg = {nom(k): v for k, v in gen["v"].items()}
        og = sorted(vg.items(), key=lambda kv: -kv[1])
        lg = og[0][0]; pg = 100 * og[0][1] / gen["validos"]
        # municipales 2023 (los totales que Interior mezcla con las candidaturas no cuentan)
        vm = {k: v for k, v in mun["v"].items() if k not in AGREGADOS}
        om = sorted(vm.items(), key=lambda kv: -kv[1])
        lm_ = nom(om[0][0]); pm = 100 * om[0][1] / mun["validos"]
        # proyección con sondeos
        l_proy, seg, marg = lider(gen["v"], gen["blanco"], VOL["r_med"])
        l_proy, seg = nom(l_proy), nom(seg)
        cambia = l_proy != lg

        frase_alc = (f"Al frente del ayuntamiento está {alc['nombre']}" + (f" ({alc['partido']})" if alc.get("partido") else "") + ". ") if alc else ""
        resp = (f"{nombre} tiene {nes(pob)} habitantes. {frase_alc}"
                f"En las municipales de mayo de 2023, {_art(lm_)} fue la lista más votada ({_c1(pm)} %); en las generales de julio de 2023, {_art(lg)} fue el partido más votado ({_c1(pg)} %). "
                + (f"Con la media de sondeos proyectada sobre los votos de 2023, {_art(l_proy)} pasaría a ser la fuerza más votada ({_c1(marg)} puntos de ventaja)." if cambia
                   else f"Con la media de sondeos proyectada sobre los votos de 2023, {_art(l_proy)} seguiría siendo la fuerza más votada, con {_c1(marg)} puntos sobre {_art(seg)}."))
        desc = f"Qué vota {nombre}: generales y municipales de 2023, población, renta, alcalde y proyección con sondeos para el 29N."

        # 1. generales
        part = f" (participación del {_c1(100 * gen['votantes'] / gen['censo'])} %)" if gen.get("censo") else ""
        prov_rc = ((c["RC"] or {}).get("prov") or {}).get(pc)
        comp = ""
        if prov_rc and prov_rc["validos"]:
            sp = prov_rc["v"].get([k for k in prov_rc["v"] if nom(k) == lg][0], [0])[0] if any(nom(k) == lg for k in prov_rc["v"]) else None
            if sp is not None:
                comp = f" En el conjunto de la provincia de {E(prov_n)}, {E(_art(lg))} obtuvo el {_c1(100 * sp / prov_rc['validos'])} %."
        s1 = (f"<h2>1. Elecciones generales de julio de 2023</h2><p>En {E(nombre)} votaron {nes(gen['votantes'])} personas{part}. Reparto de los votos válidos: "
              + ", ".join(f"{E(k)} {_c1(100 * v / gen['validos'])} %" for k, v in og[:6]) + f".{comp} Fuente: <a href='https://infoelectoral.interior.gob.es/'>Ministerio del Interior</a>.</p>")
        # 2. municipales
        s2 = (f"<h2>2. Elecciones municipales de mayo de 2023</h2><p>Reparto de los votos válidos en las municipales: "
              + ", ".join(f"{E(nom(k))} {_c1(100 * v / mun['validos'])} %" for k, v in om[:6])
              + ". «Más votado» no equivale a «alcalde»: tras las municipales gobiernan también los pactos entre listas. Fuente: <a href='https://infoelectoral.interior.gob.es/'>Ministerio del Interior</a>.</p>")
        # 3. proyección
        s3 = (f"<h2>3. ¿Cambiaría de partido el 29N?</h2><p>Si el cambio nacional de la media de sondeos se repitiera igual en {E(nombre)}, "
              + (f"{E(_art(l_proy))} superaría a {E(_art(lg))} y sería la fuerza más votada con {_c1(marg)} puntos de ventaja." if cambia
                 else f"{E(_art(l_proy))} seguiría en cabeza con {_c1(marg)} puntos de ventaja sobre {E(_art(seg))}.")
              + " Es una proyección orientativa, no una previsión: no hay encuestas municipales y el cambio real nunca es uniforme.</p>")
        # 4. población
        s4 = f"<h2>4. Población y renta</h2><p>{E(nombre)} tiene {nes(pob)} habitantes"
        if len(serie) == len(anios) and serie[-1]:
            ch = 100 * (serie[0] - serie[-1]) / serie[-1]
            s4 += f" (INE, 1 de enero de {anios[0]}; en {anios[-1]} eran {nes(serie[-1])}, un {_c1(abs(ch))} % {'más' if ch >= 0 else 'menos'})"
        prov_pob = (pad["prov"].get(pc) or [None])[0]
        if prov_pob: s4 += f", el {_c1(100 * pob / prov_pob)} % de la provincia"
        s4 += "."
        dm = dem["mun"].get(code); dp = dem["prov"].get(pc); es_ = dem["esp"]
        if dm and dm[0] is not None and dm[3] is not None:
            s4 += (f" La edad media es de {_c1(dm[0])} años (España, {_c1(es_[0])}); un {_c1(dm[2])} % tiene 65 años o más y un {_c1(dm[1])} % menos de 18. "
                   f"La renta neta media por persona es de {nes(round(dm[3]))} euros ({nes(round(es_[3]))} en España" + (f", {nes(round(dp[3]))} en la provincia" if dp and dp[3] else "") + f"), según el Atlas de renta de los hogares del INE de {dem['anio']}.")
        s4 += "</p>"
        # 5. gobierno
        li = "".join(f"<li><b>{E(g['rol'])}</b>: {E(g['nombre'])}" + (f" <span class='meta'>({E(g['partido'])})</span>" if g.get("partido") else "")
                     + ("" if str(g.get("fuente", "")).startswith("Wikidata") else " <span class='meta'>(Wikipedia; por verificar)</span>") + "</li>" for g in gob)
        fa = FICHA_ALCALDE.get(pc)
        s5 = (f"<h2>5. Quién gobierna</h2><ul>{li}</ul>" + (f"<p>Perfil: <a href='/atalaya/fichas/{fa[0]}'>{E(fa[1])}, alcalde de {E(nombre)}</a>.</p>" if fa else "")
              + "<p class='meta'>Cargos vigentes según Wikidata y, donde falta, Wikipedia.</p>") if gob else ""
        # 6. titulares
        k = _nrm(nombre)
        tit = [x for x in noticias if pc in x["pv"] and k in _nrm(x["t"])][:6]
        s6 = ("<h2>6. Señales recientes</h2><ul>" + "".join(
            f"<li><a href='{E(x['u'])}' rel='nofollow noopener'>{E(re.sub(chr(32)+'-'+chr(32)+'[^-]{3,60}$', '', x['t']))}</a> <span class='meta'>({E(x['m'])}, {fecha_es(x['f'])})</span></li>" for x in tit) + "</ul>") if tit else ""
        # 7. voto CERA (dato provincial)
        s7, cv = "", (cprov.get(pc) or {}).get("generales-2016")
        if cv and cv.get("cera") and cv.get("total"):
            pos = cera_orden.index(cv["cera"]) + 1; pct_c = 100 * cv["cera"] / cv["total"]
            media = f" (media nacional: {_c1(cnac['part'])} %)" if cnac.get("part") is not None else ""
            s7 = (f"<h2>7. Voto CERA</h2><p>El voto CERA es el de los españoles que viven en el extranjero y su recuento llega unos días después de la noche electoral. "
                  f"El INE lo publica por provincia, no por municipio. En la provincia de {E(prov_n)}, en las generales de 2016, había {nes(int(cv['cera']))} electores CERA, "
                  f"el {_c1(pct_c)} % de su censo (puesto {pos} de {len(cera_orden)} provincias), y votó el {_c1(cv['part'])} % de ellos{media}. "
                  f"Más cifras en la <a href='/atalaya/fichas/{prov_r}'>ficha de la provincia</a> y en el <a href='/atalaya/cera/'>panel del voto CERA</a>.</p>"
                  "<p class='meta'>Fuente: <a href='https://ine.es/jaxiPx/Tabla.htm?L=0&amp;tpx=32091'>INE, tabla 32091</a>.</p>")
        # enlaces
        enl = f"<li><a href='/atalaya/fichas/{prov_r}'>Provincia de {E(prov_n)}: ¿quién ganará las elecciones?</a></li>"
        if cc: enl += f"<li><a href='/atalaya/fichas/{cc[1]}'>{E(cc[0])}: ¿quién ganará las elecciones?</a></li>"
        enl += "<li><a href='/atalaya/fichas/cambio/ciudades/'>¿Qué ciudades pueden cambiar de partido más votado?</a></li>"
        faqs = [(f"¿Qué vota {nombre}?", resp),
                (f"¿Cuántos habitantes tiene {nombre}?", f"{nombre} tiene {nes(pob)} habitantes" + (f" según el padrón del INE a 1 de enero de {anios[0]}." if serie else ".")),
                (f"¿Qué partido ganó en {nombre} en las elecciones municipales de 2023?", f"{_art(lm_, True)} fue la lista más votada con el {_c1(pm)} % de los votos válidos. Más votado no significa alcalde: depende de los pactos."),
                (f"¿Qué partido ganó en {nombre} en las generales de 2023?", f"{_art(lg, True)} con el {_c1(pg)} % de los votos válidos."),
                (f"¿Puede cambiar de partido {nombre} en las elecciones del 29N?", (f"Con la proyección de los sondeos recientes, {_art(l_proy)} superaría a {_art(lg)}." if cambia else f"Con la proyección de los sondeos recientes, {_art(lg)} seguiría siendo el partido más votado. Es orientativo, no una previsión."))]
        if s7: faqs.append((f"¿Cuántos electores CERA hay en la provincia de {prov_n}?", f"En las elecciones generales de 2016, según el INE, la provincia de {prov_n} tenía {nes(int(cv['cera']))} electores CERA (españoles residentes en el extranjero), el {_c1(pct_c)} % de su censo. El INE no publica este dato por municipio."))
        if alc: faqs.insert(1, (f"¿Quién es el alcalde de {nombre}?", f"{alc['nombre']}" + (f" ({alc['partido']})" if alc.get("partido") else "") + ", según Wikidata y Wikipedia."))
        faq_html = "<h2>Preguntas frecuentes</h2>" + "".join(f"<details><summary>{E(a)}</summary><p>{E(b)}</p></details>" for a, b in faqs)
        q = f"¿Qué vota {nombre} y quién la gobierna?"
        cuerpo = (f"<p class='meta'>Actualizado el {fecha_es(FECHA)} · Elecciones generales del 29 de noviembre de 2026</p><p class='ans'>{E(resp)}</p>"
                  f"{s1}{s2}{s3}{s4}{s5}{s6}{s7}"
                  "<h2>Lo que este análisis no incluye</h2><p class='warn'>No hay encuestas municipales: la proyección supone que el cambio nacional se repite igual en la ciudad. Es un ejercicio orientativo, no una encuesta ni una previsión oficial.</p>"
                  f"<h2>Más fichas</h2><ul>{enl}</ul>{faq_html}"
                  "<h2>Fuentes y método</h2><ul><li>Votos de 2023: Ministerio del Interior.</li><li>Población, renta y voto CERA (por provincia): INE.</li><li>Cargos: Wikidata y Wikipedia.</li><li>Sondeos: media ponderada en <a href='/elecciones-espana/'>Elecciones en España</a>.</li><li>Titulares: RSS de medios que nombran la ciudad.</li></ul>"
                  "<p class='meta'><a href='/atalaya/fichas/metodologia/'>Metodología y fuentes de Atalaya</a></p>")
        ld = [{"@context": "https://schema.org", "@type": "Article", "headline": q, "description": desc, "inLanguage": "es", "datePublished": FECHA, "dateModified": FECHA,
               "author": {"@type": "Person", "name": "Emilio Rodríguez García", "url": f"{BASE}/sobre-mi"}, "publisher": {"@type": "Person", "name": "Emilio Rodríguez García"},
               "mainEntityOfPage": f"{BASE}/atalaya/fichas/{ruta}", "about": nombre},
              {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": a, "acceptedAnswer": {"@type": "Answer", "text": b}} for a, b in faqs]},
              {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                  {"@type": "ListItem", "position": 1, "name": "Atalaya", "item": f"{BASE}/atalaya/"},
                  {"@type": "ListItem", "position": 2, "name": "Fichas", "item": f"{BASE}/atalaya/fichas/"},
                  {"@type": "ListItem", "position": 3, "name": nombre, "item": f"{BASE}/atalaya/fichas/{ruta}"}]}]
        pagina(ruta, f"{nombre}: qué vota, quién gobierna y población (elecciones 2026)", desc, q, cuerpo, ld,
               f"<a href='/atalaya/'>Atalaya</a> › <a href='/atalaya/fichas/'>Fichas</a> › {E(nombre)} (ciudad)")
        urls.append(f"{BASE}/atalaya/fichas/{ruta}"); hub.append((nombre, ruta, pob))
    return urls, hub
