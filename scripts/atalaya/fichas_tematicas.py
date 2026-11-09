"""Atalaya: fichas de partido y de tema (estáticas, indexables). Las invoca build_fichas.py al final de su ejecución.

  /atalaya/fichas/partido/<siglas>/   encuestas, escaños 2023, posiciones por tema con cita, clima de prensa
  /atalaya/fichas/tema/<tema>/        qué posición tiene cada partido en ese tema (con cita y fuente) y cuánta prensa genera

Solo usa datos reales del repositorio (programas.json, escanos.json, noticias.json, sentimiento.json, encuestas medias).
Las posiciones proceden de programas anteriores, votaciones y declaraciones citadas: no son los programas de 2026.
"""
import json, re
from collections import Counter
from datetime import datetime

POS = {"favor": "A favor", "contra": "En contra", "matizada": "Matizada", "sin_posicion": "Sin posición"}
# Tema de programas.json -> tema del clasificador de prensa (solo los que coinciden con claridad)
TEMA_PRENSA = {"Vivienda": "vivienda", "Sanidad": "sanidad", "Empleo": "empleo", "Inmigración": "inmigración",
               "Modelo territorial": "modelo territorial", "Justicia": "corrupción y justicia"}
CSS_EXTRA = "<style>table.pos td,table.pos th{text-align:left;vertical-align:top}table.pos td:first-child{white-space:nowrap;font-weight:600}.chip{display:inline-block;padding:1px 8px;border-radius:10px;border:1px solid #d9e0ea;font-size:13px;white-space:nowrap}</style>"


def generar(c):
    E, BASE, FECHA, fecha_es, slug, nes, pagina, J, D = (c[k] for k in ("E", "BASE", "FECHA", "fecha_es", "slug", "nes", "pagina", "J", "D"))
    prog = J(D / "programas.json")
    partidos = prog["partidos"]; afs = prog["afirmaciones"]
    esc = J(D / "escanos.json")
    noticias = J(D / "noticias.json")["noticias"]
    sj = J(D / "sentimiento.json")["items"] if (D / "sentimiento.json").exists() else {}
    pinfo = {x["id"]: x for x in J(c["RAIZ"] / "elecciones-espana/data/2026-11-29/partidos.json")["partidos"]}
    cand = {x["partidoId"]: x for x in J(c["RAIZ"] / "elecciones-espana/data/2026-11-29/candidatos.json")["candidatos"]}
    nacional, nsond, fsond = c["nacional"], c["nsond"], c["fsond"]
    orden = sorted(nacional, key=lambda p: -nacional[p])
    urls, hub_p, hub_t = [], [], []
    seguro = lambda u: u if re.match(r"https?://", u or "") else "#"

    clas = []   # noticias con clasificación: (noticia, clasificación)
    for n in noticias:
        s = sj.get(n.get("i"))
        if s: clas.append((n, s))

    def prensa(filtro, n_min=15):
        """Resumen de prensa para las noticias clasificadas que cumplan el filtro; None si la muestra es demasiado corta."""
        sel = [(n, s) for n, s in clas if filtro(s)]
        if len(sel) < n_min: return None
        pos = sum(s["tono"] > 0 for _, s in sel); neg = sum(s["tono"] < 0 for _, s in sel); N = len(sel)
        return {"n": N, "pos": round(100 * pos / N), "neg": round(100 * neg / N), "neu": 100 - round(100 * pos / N) - round(100 * neg / N),
                "temas": [t for t, _ in Counter(s["tema"] for _, s in sel if s["tema"] != "otros").most_common(3)],
                "medios": Counter(n["m"] for n, _ in sel).most_common(5),
                "recientes": sorted(sel, key=lambda x: x[0]["f"], reverse=True)[:5]}

    def bloque_prensa(p, sujeto, con_temas=True):
        if not p: return f"<p>Todavía hay pocas noticias clasificadas sobre {E(sujeto)} para hacer una lectura fiable. Se actualizará cuando la muestra crezca.</p>"
        med = ", ".join(f"{E(m)} ({k})" for m, k in p["medios"])
        rec = "".join(f"<li><a href='{E(seguro(n['u']))}' rel='nofollow noopener'>{E(re.sub(chr(32)+'-'+chr(32)+'[^-]{3,60}$', '', n['t']))}</a> <span class='meta'>({E(n['m'])}, {fecha_es(n['f'])})</span></li>" for n, _ in p["recientes"])
        return (f"<p>De {p['n']} titulares recientes clasificados sobre {E(sujeto)}, un {p['neg']} % tiene tono negativo, un {p['neu']} % neutro y un {p['pos']} % positivo. "
                + (f"Temas más frecuentes: {E(', '.join(p['temas']) or 'sin un tema dominante')}. " if con_temas else "") + f"Medios que más lo recogen: {med}.</p>"
                f"<ul>{rec}</ul><p class='warn'>Clasificación automática hecha solo a partir del titular: es orientativa y mide el tono de la noticia, no la línea editorial del medio ni la opinión de la ciudadanía.</p>")

    def tabla_pos(a, columnas=None):
        filas = ""
        for pt in partidos:
            x = a["posiciones"].get(pt["id"]) or a["posiciones"].get(pt["siglas"])
            if not x: continue
            fu = f" <a href='{E(seguro(x['fuente']))}' rel='nofollow noopener'>fuente</a>" if x.get("fuente") else ""
            filas += f"<tr><td>{E(pt['siglas'])}</td><td><span class='chip'>{POS.get(x['posicion'], x['posicion'])}</span></td><td>{E(x.get('cita') or '')}{fu} <span class='meta'>{E(x.get('fecha') or '')}</span></td></tr>"
        return f"<table class='pos'><thead><tr><th>Partido</th><th>Posición</th><th>Cita y fuente</th></tr></thead><tbody>{filas}</tbody></table>"

    def ld_base(titulo, desc, ruta, nivel2, faqs):
        return [{"@context": "https://schema.org", "@type": "Article", "headline": titulo, "description": desc, "inLanguage": "es", "datePublished": FECHA, "dateModified": FECHA,
                 "author": {"@type": "Person", "name": "Emilio Rodríguez García", "url": f"{BASE}/sobre-mi"}, "publisher": {"@type": "Person", "name": "Emilio Rodríguez García"},
                 "mainEntityOfPage": f"{BASE}/atalaya/fichas/{ruta}"},
                {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": a, "acceptedAnswer": {"@type": "Answer", "text": b}} for a, b in faqs]},
                {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Atalaya", "item": f"{BASE}/atalaya/"},
                    {"@type": "ListItem", "position": 2, "name": "Fichas", "item": f"{BASE}/atalaya/fichas/"},
                    {"@type": "ListItem", "position": 3, "name": nivel2, "item": f"{BASE}/atalaya/fichas/{ruta}"}]}]

    aviso = ("<p class='warn'>Las posiciones proceden de programas anteriores, votaciones y declaraciones públicas recientes, cada una con su fuente. "
             "Los programas electorales de 2026 aún no se han publicado y pueden cambiarlas. Si no hay evidencia clara, figura «Sin posición».</p>")

    # ---------- partidos ----------
    for pt in partidos:
        sig = pt["siglas"]; ruta = f"partido/{slug(sig)}/"
        esc_act = (pinfo.get(pt["id"]) or {}).get("escanosActuales")
        prov_primero = sum(1 for v in esc.values() if v["partidos"].get(sig) and v["partidos"][sig][-1] == max(s[-1] for s in v["partidos"].values()) and v["partidos"][sig][-1] > 0)
        pos_enc = orden.index(sig) + 1 if sig in nacional else None
        enc = f"{nacional[sig]:.1f}".replace(".", ",") if sig in nacional else None
        cd = cand.get(pt["id"]) or {}
        pos_cnt = Counter((a["posiciones"].get(pt["id"]) or a["posiciones"].get(sig) or {}).get("posicion") for a in afs)
        # respuesta
        partes = []
        if enc: partes.append(f"la media de encuestas le da un {enc} % ({pos_enc}.º puesto)")
        if esc_act: partes.append(f"tiene {esc_act} escaños en el Congreso disuelto")
        resp = f"{pt['nombre']}: " + ("; ".join(partes) if partes else "sin datos de encuesta suficientes") + "."
        if cd.get("nombre"): resp += f" Su candidato anunciado es {cd['nombre']}."
        # posiciones agrupadas por tema
        pos_html = ""
        for t in sorted({a["tema"] for a in afs}):
            filas = ""
            for a in (x for x in afs if x["tema"] == t):
                x = a["posiciones"].get(pt["id"]) or a["posiciones"].get(sig)
                if not x: continue
                fu = f" <a href='{E(seguro(x['fuente']))}' rel='nofollow noopener'>fuente</a>" if x.get("fuente") else ""
                filas += f"<tr><td>{E(a['texto'])}</td><td><span class='chip'>{POS.get(x['posicion'], x['posicion'])}</span></td><td>{E(x.get('cita') or '')}{fu} <span class='meta'>{E(x.get('fecha') or '')}</span></td></tr>"
            if filas: pos_html += f"<h3><a href='/atalaya/fichas/tema/{slug(t)}/'>{E(t)}</a></h3><table class='pos'><thead><tr><th>Afirmación</th><th>Posición</th><th>Cita y fuente</th></tr></thead><tbody>{filas}</tbody></table>"
        pr = prensa(lambda s, sig=sig: s["partido"] == sig)
        cuerpo = (f"{CSS_EXTRA}<p class='meta'>Actualizado el {fecha_es(FECHA)} · Elecciones generales del 29 de noviembre de 2026</p><p class='ans'>{E(resp)}</p>"
                  f"<h2>1. Encuestas</h2><p>" + (f"Media ponderada de {nsond} sondeos de los 30 días previos al {fecha_es(fsond)} (sin CIS): {E(sig)} {enc} %. " if enc else "No hay media de encuestas disponible para este partido. ") +
                  "Detalle en <a href='/elecciones-espana/'>Elecciones en España</a>.</p>"
                  f"<h2>2. Escaños en el Congreso</h2><p>" + (f"{E(sig)} cuenta con {esc_act} escaños en el Congreso disuelto (Congreso de los Diputados). " if esc_act else "") +
                  (f"En las generales de 2023 fue el partido con más escaños en {prov_primero} provincias (datos por provincia de <a href='https://es.wikipedia.org/wiki/Elecciones_generales_de_Espa%C3%B1a_de_2023'>Wikipedia</a>; las coaliciones pueden no atribuirse al partido)." if prov_primero else "") + "</p>"
                  f"<h2>3. Qué posición tiene en cada tema</h2>{aviso}"
                  f"<p>De {len(afs)} afirmaciones analizadas: a favor en {pos_cnt.get('favor', 0)}, en contra en {pos_cnt.get('contra', 0)}, matizada en {pos_cnt.get('matizada', 0)} y sin posición clara en {pos_cnt.get('sin_posicion', 0)}.</p>{pos_html}"
                  f"<h2>4. Clima de prensa</h2>{bloque_prensa(pr, sig)}"
                  "<h2>Qué no incluye</h2><p class='warn'>No es un test de voto ni una recomendación. No usa todavía el programa electoral de 2026 ni encuestas provinciales.</p>")
        faqs = [(f"¿Qué dicen las encuestas sobre {sig}?", (f"La media de encuestas le da un {enc} %." if enc else "No hay media de encuestas disponible para este partido.")),
                (f"¿Quién es el candidato de {sig} en 2026?", (f"{cd['nombre']} ({cd.get('cargo') or 'cabeza de lista anunciado'})." if cd.get("nombre") else "Aún no hay un candidato anunciado con los datos disponibles.")),
                (f"¿Cuántos escaños tiene {sig} en el Congreso?", (f"{esc_act} escaños en el Congreso disuelto." if esc_act else "No tiene representación en el Congreso disuelto según los datos cargados."))]
        titulo = f"{sig}: encuestas, escaños y posiciones por tema (elecciones 2026)"
        pagina(ruta, titulo, resp[:155], f"{pt['nombre']} ({sig}): encuestas, posiciones y prensa", cuerpo, ld_base(f"{pt['nombre']} ({sig})", resp, ruta, sig, faqs),
               f"<a href='/atalaya/'>Atalaya</a> › <a href='/atalaya/fichas/'>Fichas</a> › {E(sig)}")
        urls.append(f"{BASE}/atalaya/fichas/{ruta}"); hub_p.append((pt["nombre"], sig, ruta))

    # ---------- temas ----------
    for t in sorted({a["tema"] for a in afs}):
        ruta = f"tema/{slug(t)}/"; sub = [a for a in afs if a["tema"] == t]
        cnt = {pt["siglas"]: (Counter((a["posiciones"].get(pt["id"]) or a["posiciones"].get(pt["siglas"]) or {}).get("posicion") for a in sub)) for pt in partidos}
        resumen = " ".join(f"{s}: {', '.join(f'{POS[k].lower()} en {v}' for k, v in cn.items() if k in POS and k != 'sin_posicion') or 'sin posición clara'}." for s, cn in cnt.items())
        resp = f"Posiciones de los partidos sobre {t.lower()} según {len(sub)} {'afirmaciones analizadas' if len(sub) != 1 else 'afirmación analizada'}. {resumen}"
        cuerpo = f"{CSS_EXTRA}<p class='meta'>Actualizado el {fecha_es(FECHA)} · Elecciones generales del 29 de noviembre de 2026</p><p class='ans'>{E(resp)}</p><h2>1. Posición de cada partido</h2>{aviso}"
        for a in sub: cuerpo += f"<h3>{E(a['texto'])}</h3>{tabla_pos(a)}"
        k = TEMA_PRENSA.get(t)
        if k:
            pr = prensa(lambda s, k=k: s["tema"] == k, n_min=10)
            cuerpo += f"<h2>2. Presencia en prensa</h2>{bloque_prensa(pr, t.lower(), False)}"
        cuerpo += ("<h2>Otros temas</h2><ul>" + "".join(f"<li><a href='/atalaya/fichas/tema/{slug(x)}/'>{E(x)}</a></li>" for x in sorted({a['tema'] for a in afs}) if x != t) + "</ul>"
                   "<h2>Partidos</h2><ul>" + "".join(f"<li><a href='/atalaya/fichas/partido/{slug(p['siglas'])}/'>{E(p['nombre'])}</a></li>" for p in partidos) + "</ul>"
                   "<h2>Qué no incluye</h2><p class='warn'>No es un test de voto ni una recomendación, y no sustituye a los programas electorales de 2026, que aún no se han publicado.</p>")
        faqs = [(f"¿Qué propone cada partido sobre {t.lower()}?", resp)]
        pagina(ruta, f"{t}: qué propone cada partido (elecciones 2026)", resp[:155], f"{t}: ¿qué posición tiene cada partido?", cuerpo, ld_base(f"{t}: posición de cada partido", resp, ruta, t, faqs),
               f"<a href='/atalaya/'>Atalaya</a> › <a href='/atalaya/fichas/'>Fichas</a> › {E(t)}")
        urls.append(f"{BASE}/atalaya/fichas/{ruta}"); hub_t.append((t, ruta))

    hub = ("<h2>Por partido</h2><ul>" + "".join(f"<li><a href='/atalaya/fichas/{r}'>{E(n)}</a></li>" for n, _, r in hub_p) + "</ul>"
           "<h2>Por tema</h2><ul>" + "".join(f"<li><a href='/atalaya/fichas/{r}'>{E(n)}: ¿qué propone cada partido?</a></li>" for n, r in hub_t) + "</ul>")
    return hub, urls
