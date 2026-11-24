#!/usr/bin/env python3
"""Atalaya: ficha biográfica de un político (estática, indexable).

  /atalaya/fichas/politico/<slug>/   cargo, trayectoria fechada con fuente por hecho y qué no está verificado.

Datos curados a mano en atalaya/data/perfiles_politicos.json. Reutiliza la plantilla de
ficha_politico_autonomico.py. Nunca se borra nada: se amplía añadiendo hechos.

Uso (raíz del repo): python3 scripts/atalaya/ficha_perfil_politico.py
"""
import sys
from html import escape as E
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import ficha_politico_autonomico as F

BASE, D, J, fecha_es = F.BASE, F.D, F.J, F.fecha_es


def ext(u):
    return "" if u.startswith("/") else " rel='nofollow noopener'"


def fecha_hecho(f):
    return fecha_es(f) if len(f) >= 10 else f


def main():
    for p in J(D / "perfiles_politicos.json")["politicos"]:
        ruta = f"politico/{p['slug']}/"
        titulo = f"{p['nombre']}: quién es, cargo y trayectoria"
        h1 = f"¿Quién es {p['nombre']}?"
        hechos = "".join(
            f"<div class='prom'><div class='tema'>{E(fecha_hecho(h['fecha']))}</div><p>{E(h['texto'])}</p><p class='fu'>Fuentes: "
            + " · ".join(f"<a href='{E(u)}'{ext(u)}>{E(t)}</a>" for t, u in h["fuentes"])
            + "</p></div>" for h in sorted(p["hechos"], key=lambda h: h["fecha"], reverse=True))
        comp = ("<h2>Competencias</h2><ul>" + "".join(f"<li>{E(c)}</li>" for c in p["competencias"]) + "</ul>") if p["competencias"] else ""
        enl = "".join(f"<li><a href='{E(u)}'>{E(t)}</a>: {E(d)}</li>" for t, u, d in p["enlaces"])
        faq = "".join(f"<h3>{E(q)}</h3><p>{E(a)}</p>" for q, a in p["faq"])
        cuerpo = (f"<p class='meta'>Actualizado el {fecha_es(p['actualizado'])} · {E(p['cargo'])} ({E(p['partido'])})</p>"
                  f"<p class='ans'>{E(p['resumen'])}</p>"
                  "<h2>Trayectoria, de lo más reciente a lo más antiguo</h2>" + hechos + comp +
                  f"<h2>Qué no está verificado</h2><p class='warn'>{E(p['no_verificado'])}</p>"
                  "<h2>Preguntas frecuentes</h2>" + faq +
                  "<h2>Para seguir profundizando</h2><ul>" + enl + "</ul>")
        url = f"{BASE}/atalaya/fichas/{ruta}"
        ld = [{"@context": "https://schema.org", "@type": "ProfilePage", "headline": titulo, "description": p["resumen"], "inLanguage": "es",
               "dateModified": p["actualizado"],
               "author": {"@type": "Person", "name": "Emilio Rodríguez García", "url": f"{BASE}/sobre-mi"},
               "mainEntity": {"@type": "Person", "name": p["nombre"], "jobTitle": p["cargo"], "url": url}, "mainEntityOfPage": url},
              {"@context": "https://schema.org", "@type": "FAQPage",
               "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]]},
              {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                  {"@type": "ListItem", "position": 1, "name": "Atalaya", "item": f"{BASE}/atalaya/"},
                  {"@type": "ListItem", "position": 2, "name": "Fichas", "item": f"{BASE}/atalaya/fichas/"},
                  {"@type": "ListItem", "position": 3, "name": p["nombre"], "item": url}]}]
        bc = f"<a href='/atalaya/'>Atalaya</a> › <a href='/atalaya/fichas/'>Fichas</a> › {E(p['nombre'])}"
        pie = (f"Elaborado por <a href=\"https://emirodgar.es/sobre-mi\">Emilio Rodríguez García</a> con el panel <a href=\"/atalaya/\">Atalaya</a>. "
               f"Última actualización: {fecha_es(p['actualizado'])}. Contenido basado en fuentes públicas citadas en cada apartado; "
               "no es una opinión política ni una recomendación de voto. <a href=\"/atalaya/privacidad/\">Política de privacidad</a>.")
        print("Publicado:", F.pagina(ruta, titulo, p["resumen"], h1, cuerpo, ld, bc, pie))


if __name__ == "__main__":
    main()
