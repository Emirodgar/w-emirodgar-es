"""Atalaya: bloques extra de la ficha de provincia (los invoca build_fichas.py).

Añade a cada ficha de provincia, solo con datos del repositorio:
  - quién gobierna (autonómico, capital, diputación) desde politicos_prov.json (Wikidata / Wikipedia);
  - cabezas de lista al Congreso por la circunscripción (politicos_prov.json);
  - elecciones municipales de mayo de 2023 en la provincia (resultados/municipales-2023-05/<cod>.json, Interior):
    votos agregados por partido, municipios donde ganó cada uno y los municipios más poblados.
Cuidado de redacción: «más votado» no es «alcalde»: tras las municipales gobiernan los pactos.
"""
import re

NOMBRE_LISTA = {"FA": "Frente Amplio (Sumar)", "VOX": "Vox", "PODEMOS": "Podemos", "SUMAR": "Sumar", "PP": "PP", "PSOE": "PSOE"}


# filas de totales que el CSV de Interior mezcla con las candidaturas
AGREGADOS = {"Total votos a candidatos", "Votos"}


def _c1(x):
    return f"{x:.1f}".replace(".", ",")


def _nota(n):
    """'[[Izquierda Unida|IU]]' -> 'IU'; '[[Más Madrid]]' -> 'Más Madrid'."""
    if not n:
        return ""
    return re.sub(r"\[\[(?:[^\]|]*\|)?([^\]]*)\]\]", r"\1", n).strip()


def bloques(c, pc, nombre):
    """Devuelve (html, faqs, fuentes_li). Cadenas vacías si no hay datos."""
    E, J, D, nes = c["E"], c["J"], c["D"], c["nes"]
    html, faqs, fuentes = "", [], []

    pol = (J(D / "politicos_prov.json")["prov"]).get(pc) or {}
    gob = pol.get("gobierno") or []
    if gob:
        li = ""
        for g in gob:
            ver = "" if str(g.get("fuente", "")).startswith("Wikidata") else " <span class='meta'>(Wikipedia; por verificar)</span>"
            pt = f" <span class='meta'>({E(g['partido'])})</span>" if g.get("partido") else ""
            li += f"<li><b>{E(g['rol'])}</b>: {E(g['nombre'])}{pt}{ver}</li>"
        html += f"<h2>Quién gobierna en {E(nombre)}</h2><ul>{li}</ul><p class='meta'>Cargos vigentes según Wikidata y, donde falta, el cuadro de Wikipedia. Los marcados «por verificar» no tienen aún confirmación independiente.</p>"
        faqs.append((f"¿Quién gobierna en {nombre}?", " ".join(f"{g['rol']}: {g['nombre']}" + (f" ({g['partido']})." if g.get('partido') else ".") for g in gob)))
        fuentes.append("Cargos: Wikidata y Wikipedia (<a href='https://www.wikidata.org/'>Wikidata</a>).")

    cands = pol.get("candidatos") or []
    if cands:
        li = ""
        for x in cands:
            nt = _nota(x.get("nota"))
            li += f"<li><b>{E(NOMBRE_LISTA.get(x['partido'], x['partido']))}</b>: {E(x['nombre'])}" + (f" <span class='meta'>({E(nt)})</span>" if nt else "") + "</li>"
        html += (f"<h2>Cabezas de lista al Congreso por {E(nombre)} (29N)</h2><ul>{li}</ul>"
                 "<p class='meta'>Según el cuadro de candidaturas de <a href='https://es.wikipedia.org/wiki/Elecciones_generales_de_Espa%C3%B1a_de_2026'>Wikipedia</a>; las candidaturas se confirman al proclamarse oficialmente.</p>")
        faqs.append((f"¿Quiénes encabezan las listas por {nombre} en las elecciones del 29N?",
                     "; ".join(f"{NOMBRE_LISTA.get(x['partido'], x['partido'])}: {x['nombre']}" for x in cands) + "."))
        fuentes.append("Candidaturas: <a href='https://es.wikipedia.org/wiki/Elecciones_generales_de_Espa%C3%B1a_de_2026'>Wikipedia</a>.")

    f = D / "resultados/municipales-2023-05" / f"{pc}.json"
    if f.exists():
        m = J(f)["mun"]
        tot, ganados, validos = {}, {}, 0
        grandes = []
        for cod, x in m.items():
            if not x.get("validos"):
                continue
            validos += x["validos"]
            for k, v in x["v"].items():
                if k in AGREGADOS:
                    continue
                tot[k] = tot.get(k, 0) + v
            top = max(((k, v) for k, v in x["v"].items() if k not in AGREGADOS), key=lambda kv: kv[1], default=None)
            if not top:
                continue
            ganados[top[0]] = ganados.get(top[0], 0) + 1
            grandes.append((x.get("pob") or 0, x["n"], top[0], 100 * top[1] / x["validos"]))
        if validos and tot:
            nmun = sum(1 for x in m.values() if x.get("validos"))
            orden = sorted(tot.items(), key=lambda kv: -kv[1])[:5]
            reparto = ", ".join(f"{E(k)} {_c1(100 * v / validos)} %" for k, v in orden)
            gan = ", ".join(f"{E(k)} en {n}" for k, n in sorted(ganados.items(), key=lambda kv: -kv[1])[:5])
            grandes.sort(reverse=True)
            filas = "".join(f"<tr><td>{E(n)}</td><td>{nes(p)}</td><td>{E(l)}</td><td>{_c1(pct)} %</td></tr>" for p, n, l, pct in grandes[:8] if p)
            html += (f"<h2>Municipales de 2023 en {E(nombre)}</h2>"
                     f"<p>En las elecciones municipales de mayo de 2023, sumando los {nes(nmun)} municipios con resultados, el reparto de votos válidos fue: {reparto}. "
                     f"Partido más votado por número de municipios: {gan}.</p>"
                     + (f"<table><thead><tr><th>Municipio</th><th>Habitantes</th><th>Más votado</th><th>% votos</th></tr></thead><tbody>{filas}</tbody></table>" if filas else "")
                     + "<p class='meta'>Fuente: <a href='https://infoelectoral.interior.gob.es/'>Ministerio del Interior</a>. «Más votado» no equivale a «alcalde»: tras las municipales gobiernan también los pactos entre listas, y las agrupaciones locales no se atribuyen a ningún partido nacional.</p>")
            lid = orden[0]
            faqs.append((f"¿Qué partido ganó las elecciones municipales de 2023 en {nombre}?",
                         f"Sumando todos los municipios de {nombre}, {lid[0]} fue la lista con más votos ({_c1(100 * lid[1] / validos)} % de los votos válidos). "
                         "Es un agregado de votos de todos los municipios; no indica quién gobierna cada ayuntamiento."))
            fuentes.append("Municipales 2023: <a href='https://infoelectoral.interior.gob.es/'>Ministerio del Interior</a>.")
    return html, faqs, fuentes
