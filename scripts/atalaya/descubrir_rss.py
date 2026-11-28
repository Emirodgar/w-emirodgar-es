#!/usr/bin/env python3
"""Atalaya: descubre y valida los feeds RSS de los medios locales de cada provincia.

Parte de una lista de portadas (CANDIDATOS), busca en cada una los <link rel="alternate" type="application/rss+xml">
(o rutas habituales), valida que el feed es XML con titulares recientes y escribe scripts/atalaya/medios_locales.json.
Solo hace peticiones públicas de lectura, a ritmo bajo y sin ocultar que es un script.
Uso (raíz del repo): python3 scripts/atalaya/descubrir_rss.py
"""
import json, re, subprocess, sys, xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import quote, urljoin, urlparse

RAIZ = Path(__file__).resolve().parents[2]
# (código de provincia, medio, portada). Una provincia puede tener varios medios.
CANDIDATOS = [
 ("37", "La Gaceta de Salamanca", "https://www.lagacetadesalamanca.es/"), ("37", "Salamanca24horas", "https://www.salamanca24horas.com/"), ("37", "Tribuna de Salamanca", "https://www.tribunasalamanca.com/"),
 ("37", "Salamancahoy", "https://www.salamancahoy.es/"), ("49", "La Opinión de Zamora", "https://www.laopiniondezamora.es/"), ("49", "Zamora News", "https://www.zamoranews.com/"),
 ("05", "El Diario de Ávila", "https://www.diariodeavila.es/"), ("09", "Diario de Burgos", "https://www.diariodeburgos.es/"), ("24", "Diario de León", "https://www.diariodeleon.es/"),
 ("34", "El Norte de Castilla Palencia", "https://www.elnortedecastilla.es/palencia/"), ("34", "Diario Palentino", "https://www.diariopalentino.es/"), ("40", "El Adelantado de Segovia", "https://www.eladelantado.com/"),
 ("42", "Heraldo-Diario de Soria", "https://www.heraldodiariodesoria.es/"), ("47", "El Norte de Castilla", "https://www.elnortedecastilla.es/"), ("47", "El Día de Valladolid", "https://www.eldiadevalladolid.com/"),
 ("28", "Telemadrid", "https://www.telemadrid.es/"), ("28", "Madridiario", "https://www.madridiario.es/"), ("08", "La Vanguardia", "https://www.lavanguardia.com/"), ("08", "El Periódico", "https://www.elperiodico.com/es/"),
 ("08", "Ara", "https://www.ara.cat/"), ("41", "Diario de Sevilla", "https://www.diariodesevilla.es/"), ("29", "Diario Sur", "https://www.diariosur.es/"), ("29", "La Opinión de Málaga", "https://www.laopiniondemalaga.es/"),
 ("18", "Ideal Granada", "https://www.ideal.es/granada/"), ("18", "Granada Hoy", "https://www.granadahoy.com/"), ("14", "Diario Córdoba", "https://www.diariocordoba.com/"), ("23", "Diario Jaén", "https://www.diariojaen.es/"),
 ("21", "Huelva Información", "https://www.huelvainformacion.es/"), ("11", "Diario de Cádiz", "https://www.diariodecadiz.es/"), ("04", "Diario de Almería", "https://www.diariodealmeria.es/"),
 ("46", "Levante-EMV", "https://www.levante-emv.com/"), ("46", "Las Provincias", "https://www.lasprovincias.es/"), ("03", "Información", "https://www.informacion.es/"), ("12", "El Periódico Mediterráneo", "https://www.elperiodicomediterraneo.com/"),
 ("50", "Heraldo de Aragón", "https://www.heraldo.es/"), ("50", "El Periódico de Aragón", "https://www.elperiodicodearagon.com/"), ("22", "Diario del AltoAragón", "https://www.diariodelaltoaragon.es/"), ("44", "Diario de Teruel", "https://www.diariodeteruel.es/"),
 ("15", "La Voz de Galicia", "https://www.lavozdegalicia.es/"), ("15", "La Opinión A Coruña", "https://www.laopinioncoruna.es/"), ("36", "Faro de Vigo", "https://www.farodevigo.es/"), ("36", "Diario de Pontevedra", "https://www.diariodepontevedra.es/"),
 ("32", "La Región", "https://www.laregion.es/"), ("27", "El Progreso", "https://www.elprogreso.es/"), ("33", "La Nueva España", "https://www.lne.es/"), ("33", "El Comercio", "https://www.elcomercio.es/"),
 ("39", "El Diario Montañés", "https://www.eldiariomontanes.es/"), ("48", "El Correo", "https://www.elcorreo.com/"), ("20", "Diario Vasco", "https://www.diariovasco.com/"), ("01", "El Correo Álava", "https://www.elcorreo.com/alava/"),
 ("31", "Diario de Navarra", "https://www.diariodenavarra.es/"), ("26", "La Rioja", "https://www.larioja.com/"), ("30", "La Verdad", "https://www.laverdad.es/"), ("30", "La Opinión de Murcia", "https://www.laopiniondemurcia.es/"),
 ("02", "La Tribuna de Albacete", "https://www.latribunadealbacete.es/"), ("13", "La Tribuna de Ciudad Real", "https://www.latribunadeciudadreal.es/"), ("16", "Las Noticias de Cuenca", "https://www.lasnoticiasdecuenca.es/"),
 ("19", "Nueva Alcarria", "https://www.nuevaalcarria.com/"), ("45", "La Tribuna de Toledo", "https://www.latribunadetoledo.es/"), ("06", "Diario Hoy", "https://www.hoy.es/"), ("10", "El Periódico Extremadura", "https://www.elperiodicoextremadura.com/"),
 ("07", "Diario de Mallorca", "https://www.diariodemallorca.es/"), ("07", "Ultima Hora", "https://www.ultimahora.es/"), ("35", "La Provincia", "https://www.laprovincia.es/"), ("38", "El Día", "https://www.eldia.es/"),
 ("17", "El Punt Avui", "https://www.elpuntavui.cat/"), ("25", "Segre", "https://www.segre.com/"), ("43", "Diari de Tarragona", "https://www.diaridetarragona.com/"), ("51", "El Faro de Ceuta", "https://elfarodeceuta.es/"), ("52", "El Faro de Melilla", "https://elfarodemelilla.es/"),
]
# Segunda tanda (nov 2026): refuerza las provincias con un solo medio y suma medios regionales. Se procesa con --nuevos y se FUSIONA
# con medios_locales.json (nunca borra los que ya estaban). Los que no den feed válido simplemente no se añaden.
CANDIDATOS_NUEVOS = [
 ("39", "Cantabria Liberal", "https://www.cantabrialiberal.com/"), ("39", "El Diario Cantabria", "https://www.eldiariocantabria.es/"), ("39", "Europa Press Cantabria", "https://www.europapress.es/cantabria/"),
 ("48", "Deia", "https://www.deia.eus/"), ("48", "Naiz", "https://www.naiz.eus/es"), ("20", "Noticias de Gipuzkoa", "https://www.noticiasdegipuzkoa.eus/"), ("20", "El Diario Vasco Política", "https://www.diariovasco.com/politica/"),
 ("01", "Noticias de Álava", "https://www.noticiasdealava.eus/"), ("01", "Gasteiz Hoy", "https://www.gasteizhoy.com/"),
 ("31", "Noticias de Navarra", "https://www.noticiasdenavarra.com/"), ("31", "Pamplona Actual", "https://www.pamplonaactual.com/"), ("31", "Navarra.com", "https://www.navarra.com/"),
 ("26", "Rioja2", "https://www.rioja2.com/"), ("26", "NueveCuatroUno", "https://www.nuevecuatrouno.com/"), ("26", "Diario La Rioja", "https://www.eldiariolarioja.es/"),
 ("13", "Lanza Digital", "https://www.lanzadigital.com/"), ("13", "Encastillalamancha Ciudad Real", "https://www.encastillalamancha.es/"),
 ("16", "Voces de Cuenca", "https://www.vocesdecuenca.com/"), ("16", "El Día de Cuenca", "https://www.eldiadecuenca.es/"),
 ("45", "El Día de Toledo", "https://www.eldiadetoledo.es/"), ("45", "Toledo Diario", "https://www.toledodiario.es/"), ("45", "eldiario.es Castilla-La Mancha", "https://www.eldiario.es/castilla-la-mancha/"),
 ("06", "Canal Extremadura", "https://www.canalextremadura.es/"), ("06", "Región Digital", "https://www.regiondigital.com/"), ("10", "Extremadura 7 días", "https://www.extremadura7dias.com/"), ("10", "eldiario.es Extremadura", "https://www.eldiario.es/extremadura/"),
 ("25", "La Mañana Lleida", "https://www.lamanyana.cat/"), ("25", "NacióDigital Lleida", "https://www.naciodigital.cat/lleida"), ("25", "Lleida Diari", "https://www.lleida.com/"),
 ("43", "Diari Més", "https://www.diarimes.com/"), ("43", "Reus Digital", "https://www.reusdigital.cat/"), ("17", "Diari de Girona", "https://www.diaridegirona.cat/"), ("17", "NacióDigital Girona", "https://www.naciodigital.cat/girona"),
 ("51", "Ceuta al Día", "https://ceutaaldia.com/"), ("51", "El Pueblo de Ceuta", "https://elpueblodeceuta.es/"), ("51", "Ceuta Actualidad", "https://www.ceutaactualidad.com/"),
 ("52", "Melilla Hoy", "https://www.melillahoy.es/"), ("52", "Melilla Actualidad", "https://www.melillaactualidad.es/"),
 ("15", "Praza", "https://praza.gal/"), ("36", "Galiciapress", "https://www.galiciapress.es/"), ("32", "Nós Diario", "https://www.nosdiario.gal/"), ("33", "Asturias24", "https://www.asturias24.es/"), ("33", "El Comercio Política", "https://www.elcomercio.es/politica/"),
 ("35", "Canarias7", "https://www.canarias7.es/"), ("35", "Canarias Ahora", "https://www.eldiario.es/canariasahora/"), ("38", "Diario de Avisos", "https://diariodeavisos.elespanol.com/"),
 ("07", "Periódico de Ibiza", "https://www.periodicodeibiza.es/"), ("07", "Menorca", "https://www.menorca.info/"), ("07", "Última Hora Política", "https://www.ultimahora.es/"),
 ("11", "Diario de Jerez", "https://www.diariodejerez.es/"), ("21", "Huelva24", "https://www.huelva24.com/"), ("41", "Andalucía Información", "https://andaluciainformacion.es/"), ("18", "Granada Digital", "https://www.granadadigital.es/"),
 ("46", "Valencia Plaza", "https://valenciaplaza.com/"), ("03", "Alicante Plaza", "https://alicanteplaza.es/"), ("30", "Murcia Plaza", "https://murciaplaza.com/"), ("50", "Aragón Digital", "https://www.aragondigital.es/"),
 ("42", "Soria Noticias", "https://sorianoticias.com/"), ("24", "ileon", "https://www.ileon.com/"), ("47", "Valladolid Plaza?", "https://www.valladolidplaza.com/"), ("40", "El Día de Segovia", "https://www.eldiasegovia.es/"),
 ("28", "Madridiario Política", "https://www.madridiario.es/"), ("28", "El Español Madrid", "https://www.elespanol.com/madrid/"), ("08", "NacióDigital", "https://www.naciodigital.cat/"), ("08", "El Nacional.cat", "https://www.elnacional.cat/es/"),
]
RUTAS = ["/rss", "/rss/", "/feed", "/feed/", "/rss.xml", "/rss/portada", "/rss/politica"]

def curl(url, n=800000):
    r = subprocess.run(["curl", "-s", "-L", "-m", "20", "--max-filesize", str(n), url], capture_output=True)
    return r.stdout

def feed_valido(url):
    try:
        raiz = ET.fromstring(curl(url))
    except Exception: return 0
    return len(list(raiz.iter("item"))) + len(list(raiz.iter("{http://www.w3.org/2005/Atom}entry")))

def descubrir(c):
    pc, medio, portada = c
    html = curl(portada).decode("utf8", "replace")
    urls = [urljoin(portada, u) for u in re.findall(r'<link[^>]+type="application/(?:rss|atom)\+xml"[^>]*href="([^"]+)"', html)]
    urls += [urljoin(portada, r) for r in RUTAS]
    for u in dict.fromkeys(urls):
        n = feed_valido(u)
        if n >= 5: return {"prov": pc, "medio": medio, "url": u, "items": n}
    # Sin RSS propio: titulares de ese medio vía una búsqueda «site:» de Google Noticias (menos ruido que la búsqueda por provincia)
    dominio = urlparse(portada).netloc.replace("www.", "")
    gn = "https://news.google.com/rss/search?hl=es&gl=ES&ceid=ES:es&q=" + quote(f"site:{dominio} when:3d")
    n = feed_valido(gn)
    if n >= 5: return {"prov": pc, "medio": medio, "url": gn, "items": n, "via": "google-site"}
    return {"prov": pc, "medio": medio, "url": None, "items": 0}

def main():
    solo_nuevos = "--nuevos" in sys.argv
    with ThreadPoolExecutor(8) as ex: res = list(ex.map(descubrir, CANDIDATOS_NUEVOS if solo_nuevos else CANDIDATOS))
    ok = [r for r in res if r["url"]]
    f = RAIZ / "scripts/atalaya/medios_locales.json"
    previos = json.loads(f.read_text(encoding="utf8"))["medios"] if f.exists() else []
    fus = {(m["prov"], m["medio"]): m for m in previos}          # fusionar: lo ya validado se conserva siempre
    for r in ok: fus[(r["prov"], r["medio"])] = r
    f.write_text(json.dumps({"medios": list(fus.values())}, ensure_ascii=False, indent=1), encoding="utf8")
    print(len(ok), "feeds válidos de", len(res), "medios;", len(fus), "en total")
    print("nuevos con feed propio:", [r["medio"] for r in ok if r["medio"] not in {m["medio"] for m in previos} and "via" not in r])
    print("nuevos vía Google site:", [r["medio"] for r in ok if r["medio"] not in {m["medio"] for m in previos} and "via" in r])
    print("sin feed:", [r["medio"] for r in res if not r["url"]])
    print("provincias cubiertas:", len({r["prov"] for r in fus.values()}))
if __name__ == "__main__": main()
