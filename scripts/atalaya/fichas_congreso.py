"""Atalaya: fichas del Congreso (estáticas, indexables). Las invoca build_fichas.py antes de generar las provincias.

  /atalaya/fichas/diputado/<nombre>/     una por cada diputado vigente de la legislatura actual (350)
  /atalaya/fichas/legislatura/xv/        composición, grupos y renovación de la legislatura actual
  /atalaya/fichas/legislatura/           las 16 legislaturas desde 1977: duración y renovación

El Senado queda fuera mientras su histórico esté incompleto (ver senado.json: historico_completo).
No se usa el campo «bio» de congreso.json: puede incluir datos personales (familia, etc.).
"""
import re
from collections import Counter
from datetime import datetime


def parlamento(c):
    """Devuelve (html para el índice de fichas, urls, {código de provincia: [(nombre, ruta, partido)]})."""
    E, BASE, FECHA, fecha_es, slug, pagina, J, D = (c[k] for k in ("E", "BASE", "FECHA", "fecha_es", "slug", "pagina", "J", "D"))
    prov_slug = c["prov_slug"]                                   # código INE -> (nombre, ruta de su ficha)
    cg = J(D / "parlamento" / "congreso.json")
    legs = cg["legislaturas"]; act = str(cg["legislatura_actual"]); disol = cg.get("disolucion")
    ident = lambda t: re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")
    nombre_leg = lambda l: legs[str(l)]["nombre"] if str(l) != "0" else "Legislatura Constituyente"
    rleg = lambda l: "legislatura/" + ("constituyente" if str(l) == "0" else ident(legs[str(l)]["nombre"].replace(" Legislatura", ""))) + "/"
    anios = lambda l: f"{legs[str(l)]['inicio'][:4]}–{(legs[str(l)]['fin'] or disol or '')[:4]}"
    nombres = {k: v["n"] for k, v in cg["personas"].items()}
    por_persona = {}
    for m in cg["mandatos"]: por_persona.setdefault(m["p"], []).append(m)
    vig = [m for m in cg["mandatos"] if str(m["l"]) == act and m.get("vig")]
    sigla = lambda pt: "pp" if pt == "PP" else "psoe" if "PSOE" in pt else "vox" if pt == "VOX" else "sumar" if pt == "SUMAR" else None
    grupo_de = lambda m: (m.get("g") or "").replace("Grupo Parlamentario ", "")
    usados, rutas = set(), {}
    for m in sorted(vig, key=lambda m: m["p"]):
        s = slug(nombres[m["p"]]); k = s; i = 2
        while k in usados: k = f"{s}-{i}"; i += 1
        usados.add(k); rutas[m["p"]] = f"diputado/{k}/"
    por_prov, urls = {}, []
    fuente = "<a href='https://www.congreso.es/es/opendata/diputados'>datos abiertos del Congreso de los Diputados</a>"

    def ld(titulo, desc, ruta, nivel):
        return [{"@context": "https://schema.org", "@type": "Article", "headline": titulo, "description": desc, "inLanguage": "es", "datePublished": FECHA, "dateModified": FECHA,
                 "author": {"@type": "Person", "name": "Emilio Rodríguez García", "url": f"{BASE}/sobre-mi"}, "mainEntityOfPage": f"{BASE}/atalaya/fichas/{ruta}"},
                {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Atalaya", "item": f"{BASE}/atalaya/"},
                    {"@type": "ListItem", "position": 2, "name": "Fichas", "item": f"{BASE}/atalaya/fichas/"},
                    {"@type": "ListItem", "position": 3, "name": nivel, "item": f"{BASE}/atalaya/fichas/{ruta}"}]}]

    bc = lambda t: f"<a href='/atalaya/'>Atalaya</a> › <a href='/atalaya/fichas/'>Fichas</a> › {E(t)}"
    f_disol = fecha_es(disol) if disol else None

    # ---- diputados ----
    for m in vig:
        nom = nombres[m["p"]]; ruta = rutas[m["p"]]; pv = prov_slug.get(m["c"])
        carrera = sorted({x["l"] for x in por_persona[m["p"]]}); n = len(carrera)
        sg = sigla(m["pt"] or "")
        ppt = f"<a href='/atalaya/fichas/partido/{sg}/'>{E(m['pt'])}</a>" if sg else E(m["pt"] or "")
        lugar = pv[0] if pv else (m.get("cn") or "")
        terr = f"<a href='/atalaya/fichas/{pv[1]}'>{E(pv[0])}</a>" if pv else E(lugar)
        grupo = grupo_de(m)
        resp = (f"{nom} es diputado/a del Congreso por {lugar} ({m['pt']}, Grupo Parlamentario {grupo}) en la {nombre_leg(act)}. "
                f"Es su {'primera' if n == 1 else f'{n}.ª'} legislatura en el Congreso.")
        filas = ""
        for l in carrera:
            nl = f"<a href='/atalaya/fichas/{rleg(l)}'>{E(nombre_leg(l))}</a>" if str(l) == act else E(nombre_leg(l))
            filas += f"<tr><td>{nl}</td><td>{anios(l)}</td></tr>"
        cuerpo = (f"<p class='meta'>Actualizado el {fecha_es(FECHA)}</p><p class='ans'>{E(resp)}</p>"
                  f"<h2>Datos del mandato</h2><ul><li>Partido: {ppt}</li><li>Grupo parlamentario: {E(grupo)}</li><li>Circunscripción: {terr}</li>"
                  f"<li>Alta en la {E(nombre_leg(act))}: {fecha_es(m['alta'])}</li>" + (f"<li>Las Cortes se disolvieron el {f_disol}.</li>" if f_disol else "") + "</ul>"
                  f"<h2>Legislaturas en el Congreso</h2><table><thead><tr><th>Legislatura</th><th>Años</th></tr></thead><tbody>{filas}</tbody></table>"
                  f"<p>Fuente: {fuente}. Solo se publican cargo, grupo y circunscripción: datos públicos del mandato, sin información personal.</p>"
                  f"<h2>Más fichas</h2><ul><li><a href='/atalaya/fichas/{rleg(act)}'>Todos los diputados de la {E(nombre_leg(act))}</a></li>"
                  + (f"<li><a href='/atalaya/fichas/{pv[1]}'>Elecciones en {E(pv[0])}</a></li>" if pv else "") + "</ul>")
        pagina(ruta, f"{nom}, diputado/a por {lugar} ({m['pt']}) | Atalaya", resp[:155], f"{nom}: diputado/a del Congreso", cuerpo, ld(nom, resp, ruta, nom), bc(nom))
        urls.append(f"{BASE}/atalaya/fichas/{ruta}")
        por_prov.setdefault(m["c"], []).append((nom, ruta, m["pt"]))

    # ---- legislatura actual ----
    ruta = rleg(act); gr = Counter(grupo_de(m) for m in vig)
    veter = Counter(len({x["l"] for x in por_persona[m["p"]]}) for m in vig)
    nuevos = veter[1]; med = sum(k * v for k, v in veter.items()) / len(vig)
    med_s = f"{med:.1f}".replace(".", ",")
    resp = (f"La {nombre_leg(act)} del Congreso comenzó el {fecha_es(legs[act]['inicio'])}" + (f" y las Cortes se disolvieron el {f_disol}" if f_disol else "")
            + f". Tiene {len(vig)} diputados vigentes; {nuevos} ({round(100 * nuevos / len(vig))} %) están en su primera legislatura y la media es de {med_s} legislaturas por diputado.")
    por_g = {}
    for m in sorted(vig, key=lambda m: nombres[m["p"]]): por_g.setdefault(grupo_de(m), []).append(m)
    det = "".join(
        f"<details><summary>{E(g)} ({len(ms)})</summary><ul>"
        + "".join(f"<li><a href='/atalaya/fichas/{rutas[x['p']]}'>{E(nombres[x['p']])}</a> <span class='meta'>({E(x['pt'])}, {E((prov_slug.get(x['c']) or (x.get('cn'), ''))[0])})</span></li>" for x in ms)
        + "</ul></details>" for g, ms in sorted(por_g.items(), key=lambda kv: -len(kv[1])))
    tg = "".join(f"<tr><td>{E(g)}</td><td>{n}</td></tr>" for g, n in gr.most_common())
    cuerpo = (f"<p class='meta'>Actualizado el {fecha_es(FECHA)}</p><p class='ans'>{E(resp)}</p>"
              f"<h2>Diputados por grupo parlamentario</h2><table><thead><tr><th>Grupo</th><th>Diputados</th></tr></thead><tbody>{tg}</tbody></table>"
              f"<h2>Todos los diputados</h2>{det}"
              f"<p>Fuente: {fuente}. <a href='/atalaya/fichas/legislatura/'>Ver todas las legislaturas</a>.</p>")
    pagina(ruta, f"{nombre_leg(act)} del Congreso: diputados y grupos | Atalaya", resp[:155], f"{nombre_leg(act)}: diputados y grupos", cuerpo,
           ld(nombre_leg(act), resp, ruta, nombre_leg(act)), bc(nombre_leg(act)))
    urls.append(f"{BASE}/atalaya/fichas/{ruta}")

    # ---- índice de legislaturas ----
    prev, filas = set(), ""
    for l in sorted(legs, key=int):
        ps = {m["p"] for m in cg["mandatos"] if str(m["l"]) == l}
        rep = f"{round(100 * len(ps & prev) / len(ps))} %" if prev and ps else "–"
        nom = f"<a href='/atalaya/fichas/{rleg(l)}'>{E(nombre_leg(l))}</a>" if l == act else E(nombre_leg(l))
        fin = legs[l]["fin"] or disol
        dur = f"{(datetime.fromisoformat(fin) - datetime.fromisoformat(legs[l]['inicio'])).days / 365.25:.1f}".replace(".", ",") if fin else "–"
        filas += f"<tr><td>{nom}</td><td>{anios(l)}</td><td>{dur}</td><td>{len(ps)}</td><td>{rep}</td></tr>"
        prev = ps
    resp = ("Desde 1977 ha habido 16 legislaturas del Congreso de los Diputados (la Constituyente y 15 más). La tabla muestra la duración de cada una, "
            "cuántas personas ocuparon escaño y qué parte ya había estado en la anterior.")
    cuerpo = (f"<p class='meta'>Actualizado el {fecha_es(FECHA)}</p><p class='ans'>{E(resp)}</p>"
              f"<table><thead><tr><th>Legislatura</th><th>Años</th><th>Duración (años)</th><th>Personas con escaño</th><th>Ya estaban en la anterior</th></tr></thead><tbody>{filas}</tbody></table>"
              "<p class='warn'>«Personas con escaño» incluye a quienes entraron por sustitución durante la legislatura, por eso supera los 350 escaños. "
              "La última legislatura se mide hasta la disolución de las Cortes.</p>"
              f"<p>Fuente: {fuente}.</p>")
    pagina("legislatura/", "Legislaturas del Congreso desde 1977: duración y renovación | Atalaya", resp[:155], "Legislaturas del Congreso de los Diputados desde 1977", cuerpo,
           ld("Legislaturas del Congreso", resp, "legislatura/", "Legislaturas"), bc("Legislaturas"))
    urls.append(f"{BASE}/atalaya/fichas/legislatura/")

    hub = (f"<h2>Congreso de los Diputados</h2><ul><li><a href='/atalaya/fichas/{rleg(act)}'>{E(nombre_leg(act))}: {len(vig)} diputados y grupos</a></li>"
           "<li><a href='/atalaya/fichas/legislatura/'>Legislaturas desde 1977</a></li><li>Cada ficha de provincia lista a sus diputados.</li></ul>")
    return hub, urls, por_prov
