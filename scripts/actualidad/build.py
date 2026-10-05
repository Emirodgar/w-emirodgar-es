#!/usr/bin/env python3
"""Hemeroteca diaria: resume con Gemini la portada de El Mundo y The Objective.

Una ejecución al día = UNA llamada a Gemini (más una extra el primer día de
cada mes para cerrar el mes anterior). Todo lo demás es código determinista:
descarga de feeds, deduplicación, validación de URLs y fusión de ficheros.
Nunca se borra nada: cada día queda en su propio JSON.

Salida (todo bajo actualidad/datos/):
    latest.json            resumen del último día (lo lee la home)
    index.json             lista de días disponibles, del más reciente al más antiguo
    dias/AAAA-MM-DD.json   resumen completo del día + titulares recogidos
    meses/AAAA-MM.json     hitos del mes (alimenta /timeline) + resumen al cerrar
    meses/index.json       lista de meses disponibles

Uso (desde la raíz del repo):
    GEMINI_API_KEY=... python3 scripts/actualidad/build.py

Variables de entorno:
    GEMINI_API_KEY   obligatoria.
    GEMINI_MODEL     opcional (por defecto gemini-2.5-flash).
    FORZAR=1         regenera el día aunque ya exista.
    HOY              opcional, AAAA-MM-DD, para forzar la fecha (pruebas).

Solo usa la librería estándar de Python.
"""

import json
import os
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from html import unescape
from pathlib import Path
from urllib.parse import urlparse

RAIZ = Path(__file__).resolve().parents[2]
DATOS = RAIZ / "actualidad" / "datos"

MODELO = os.environ.get("GEMINI_MODEL") or "gemini-2.5-flash"
USER_AGENT = "Mozilla/5.0 (compatible; EmirodgarBot/1.0; +https://emirodgar.es/actualidad)"

# Los feeds. `paginado` = feed de WordPress que solo guarda unas horas y hay
# que recorrer con ?paged=N para cubrir 24 h.
MEDIOS = [
    {"nombre": "El Mundo", "id": "E", "url": "https://www.elmundo.es/rss/googlenews/portada.xml", "paginado": False},
    {"nombre": "The Objective", "id": "O", "url": "https://theobjective.com/feed/", "paginado": True},
]

CATEGORIAS = ["Política", "Economía", "Internacional", "Sociedad", "Sucesos", "Deportes", "Cultura", "Ciencia y Tecnología"]

VENTANA_HORAS = 25          # algo más de 24 h para no dejar huecos entre ejecuciones
DIAS_YA_VISTOS = 3          # días anteriores cuyas URLs no se vuelven a resumir
MAX_PAGINAS = 14
MAX_POR_MEDIO_EN_PROMPT = 50  # tope de titulares por medio que viajan a Gemini
MIN_NOTICIAS = 8            # por debajo de esto no se gasta una llamada a la API
MAX_TEMAS = 8
MAX_HITOS_DIA = 3

try:
    from zoneinfo import ZoneInfo
    MADRID = ZoneInfo("Europe/Madrid")
except Exception:  # noqa: BLE001 - Windows sin tzdata: aproximación para pruebas locales
    MADRID = timezone(timedelta(hours=2))

AHORA = datetime.now(timezone.utc).replace(microsecond=0)
HOY = date.fromisoformat(os.environ["HOY"]) if os.environ.get("HOY") else AHORA.astimezone(MADRID).date()
NOMBRES_MES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto",
               "Septiembre", "Octubre", "Noviembre", "Diciembre"]


def log(*a):
    print(*a, file=sys.stderr, flush=True)


# --------------------------------------------------------------------------
# Utilidades
# --------------------------------------------------------------------------
def leer_json(ruta, defecto):
    try:
        return json.loads(Path(ruta).read_text(encoding="utf-8"))
    except FileNotFoundError:
        return defecto


def escribir_json(ruta, datos):
    Path(ruta).parent.mkdir(parents=True, exist_ok=True)
    Path(ruta).write_text(json.dumps(datos, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def descargar(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def normalizar(texto):
    t = unicodedata.normalize("NFD", texto or "")
    t = "".join(c for c in t if unicodedata.category(c) != "Mn").lower()
    return re.sub(r"[^a-z0-9]+", " ", t).strip()


def limpiar_html(s):
    s = re.sub(r"<[^>]+>", " ", s or "")
    return re.sub(r"\s+", " ", unescape(s)).strip()


def rel(ruta):
    return str(Path(ruta).relative_to(RAIZ)).replace("\\", "/")


# --------------------------------------------------------------------------
# Feeds
# --------------------------------------------------------------------------
def parsear_feed(xml_bytes, medio):
    items = []
    for it in ET.fromstring(xml_bytes).iter("item"):
        enlace = (it.findtext("link") or "").strip()
        titulo = limpiar_html(it.findtext("title"))
        try:
            fecha = parsedate_to_datetime(it.findtext("pubDate")).astimezone(timezone.utc)
        except (TypeError, ValueError):
            continue
        if not enlace or not titulo:
            continue
        partes = [p for p in urlparse(enlace).path.split("/") if p]
        items.append({
            "medio": medio["nombre"],
            "titulo": titulo,
            "descripcion": limpiar_html(it.findtext("description"))[:220],
            "url": enlace,
            "fecha": fecha.isoformat(),
            "seccion": partes[0] if partes else "",
        })
    return items


def recoger(medio, desde):
    """Titulares del medio publicados desde `desde` (datetime UTC)."""
    recogidos, vistos = [], set()
    paginas = MAX_PAGINAS if medio["paginado"] else 1
    for n in range(1, paginas + 1):
        url = medio["url"] if n == 1 else f"{medio['url']}?paged={n}"
        try:
            items = parsear_feed(descargar(url), medio)
        except (urllib.error.URLError, TimeoutError, ET.ParseError) as e:
            log(f"[feed] {medio['nombre']} pág. {n}: {e}")
            break
        if not items:
            break
        for it in items:
            if it["url"] not in vistos:
                vistos.add(it["url"])
                recogidos.append(it)
        if min(i["fecha"] for i in items) < desde.isoformat():
            break
    nuevos = [i for i in recogidos if i["fecha"] >= desde.isoformat()]
    log(f"[feed] {medio['nombre']}: {len(recogidos)} leídos, {len(nuevos)} dentro de la ventana.")
    return nuevos


def urls_ya_vistas():
    vistas = set()
    for i in range(1, DIAS_YA_VISTOS + 1):
        dia = leer_json(DATOS / "dias" / f"{(HOY - timedelta(days=i)).isoformat()}.json", {})
        vistas.update(n["url"] for n in dia.get("noticias", []))
    return vistas


# --------------------------------------------------------------------------
# Gemini
# --------------------------------------------------------------------------
def gemini(prompt, esquema, sistema, temperatura=0.3):
    """Llama a generateContent forzando salida JSON con `esquema`."""
    clave = os.environ.get("GEMINI_API_KEY")
    if not clave:
        sys.exit("Falta GEMINI_API_KEY en el entorno.")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODELO}:generateContent"
    config = {"responseMimeType": "application/json", "responseSchema": esquema, "temperature": temperatura}
    if "2.5" in MODELO:
        config["thinkingConfig"] = {"thinkingBudget": 0}  # resumir no necesita razonar: ahorra tokens
    cuerpo = json.dumps({
        "systemInstruction": {"parts": [{"text": sistema}]},
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": config,
    }).encode("utf-8")
    ultimo_error = None
    for intento in range(5):
        req = urllib.request.Request(
            url, data=cuerpo, method="POST",
            headers={"Content-Type": "application/json", "x-goog-api-key": clave},
        )
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                datos = json.loads(resp.read().decode("utf-8"))
            cand = (datos.get("candidates") or [{}])[0]
            texto = "".join(p.get("text", "") for p in (cand.get("content") or {}).get("parts") or [])
            if not texto:
                raise ValueError(f"Respuesta vacía (finishReason={cand.get('finishReason')})")
            uso = datos.get("usageMetadata") or {}
            log(f"[gemini] tokens: {uso.get('promptTokenCount')} entrada, {uso.get('candidatesTokenCount')} salida")
            return json.loads(texto)
        except urllib.error.HTTPError as e:
            ultimo_error = f"HTTP {e.code}: {e.read().decode('utf-8', errors='replace')[:400]}"
            if e.code not in (429, 500, 502, 503, 504):
                break  # 400/401/403/404: reintentar no arregla nada
        except (urllib.error.URLError, TimeoutError, ValueError) as e:
            ultimo_error = str(e)
        espera = 5 * (2 ** intento)
        log(f"[gemini] intento {intento + 1} fallido ({ultimo_error}); reintento en {espera}s")
        time.sleep(espera)
    raise RuntimeError(f"Gemini no respondió correctamente: {ultimo_error}")


def S(tipo, **kw):
    return {"type": tipo, **kw}


def lista(items):
    return S("ARRAY", items=items)


def obj(props):
    return S("OBJECT", properties=props, required=list(props))


SISTEMA = (
    "Eres el redactor de la hemeroteca de emirodgar.es. Resumes en español de España, con tono "
    "periodístico neutral y sobrio, lo que han destacado dos diarios digitales (El Mundo y The "
    "Objective) a partir de sus titulares y entradillas. Solo cuentas lo que está en el material: "
    "no inventas hechos, cifras, nombres ni fechas, y no tomas partido. Cuando un dato sea una "
    "afirmación de un medio o de una fuente concreta, atribúyelo (\"según El Mundo\"). Hablas de "
    "lo ocurrido, nunca de los feeds, los titulares ni del análisis. Devuelves únicamente JSON válido."
)

ESQ_DIA = obj({
    "titular": S("STRING"),
    "resumen": S("STRING"),
    "temas": lista(obj({
        "tema": S("STRING"),
        "categoria": S("STRING", enum=CATEGORIAS),
        "descripcion": S("STRING"),
        "ids": lista(S("STRING")),
    })),
    "enfoques": S("STRING"),
    "hitos": lista(obj({
        "titulo": S("STRING"),
        "categoria": S("STRING", enum=CATEGORIAS),
        "descripcion": S("STRING"),
        "relevancia": S("INTEGER"),
        "id": S("STRING"),
    })),
})

ESQ_MES = obj({"resumen_mes": S("STRING")})


def seleccionar_para_prompt(noticias):
    """Hasta MAX_POR_MEDIO_EN_PROMPT por medio (las más recientes) y un id corto por noticia."""
    elegidas = []
    for medio in MEDIOS:
        propias = sorted((n for n in noticias if n["medio"] == medio["nombre"]), key=lambda n: n["fecha"], reverse=True)
        for i, n in enumerate(propias[:MAX_POR_MEDIO_EN_PROMPT], 1):
            elegidas.append({**n, "id": f"{medio['id']}{i}"})
    return elegidas


def redactar_dia(elegidas):
    lineas = []
    for n in elegidas:
        desc = n["descripcion"]
        if normalizar(desc).startswith(normalizar(n["titulo"])[:40]):
            desc = ""  # entradilla que repite el titular: no gastar tokens
        lineas.append(f"{n['id']} | {n['seccion']} | {n['titulo']}" + (f" — {desc}" if desc else ""))
    prompt = f"""FECHA: {HOY.isoformat()}

TITULARES DE LAS ÚLTIMAS 24 HORAS (id | sección | titular — entradilla). Prefijo E = El Mundo, O = The Objective:
{chr(10).join(lineas)}

TAREA
1. "titular": una sola frase (máx. 110 caracteres) que capture lo más importante de la jornada.
2. "resumen": 2-3 párrafos separados por una línea en blanco, agrupados por bloques temáticos con transiciones \
naturales, empezando por lo de mayor peso.
3. "temas": entre 4 y {MAX_TEMAS} temas o historias distintas, ordenados por importancia. "tema" es un titular breve \
y propio (no copies el de un medio); "descripcion" 1-2 frases; "ids" son los ids de los titulares de la lista que \
tratan ese tema (copiados tal cual, 1 a 4).
4. "enfoques": un párrafo breve sobre qué temas coinciden en ambos medios y en cuáles cada uno pone el foco de forma \
distinta. Descríbelo con neutralidad. Cadena vacía si el material no permite comparar.
5. "hitos": entre 0 y {MAX_HITOS_DIA} hechos de la jornada con entidad suficiente para figurar en una cronología \
histórica (decisiones políticas, hechos de gran impacto, cifras o resultados relevantes). No incluyas tertulia ni \
contenido de servicio. "relevancia" de 1 (menor) a 5 (muy alta); "id" el id del titular que mejor lo respalda. \
Lista vacía si no hay ninguno."""
    return gemini(prompt, ESQ_DIA, SISTEMA)


def cerrar_meses():
    """Redacta (una vez) el resumen de los meses ya terminados que aún no lo tienen."""
    tocados = []
    mes_actual = HOY.strftime("%Y-%m")
    for ruta in sorted((DATOS / "meses").glob("2???-??.json")):
        datos = leer_json(ruta, {})
        if datos.get("mes", "") >= mes_actual or datos.get("resumen_mes") or not datos.get("hitos"):
            continue
        hitos = "\n".join(f"{h['fecha']} | {h['categoria']} | {h['titulo']}: {h['descripcion']}" for h in datos["hitos"])
        prompt = f"""Estos son los hitos registrados en {datos['titulo_mes']}:
{hitos}

Escribe "resumen_mes": 2-3 frases que describan el mes completo en conjunto, sin listar fecha por fecha y sin añadir nada que no esté en los hitos."""
        datos["resumen_mes"] = gemini(prompt, ESQ_MES, SISTEMA)["resumen_mes"].strip()
        escribir_json(ruta, datos)
        tocados.append(rel(ruta))
    return tocados


# --------------------------------------------------------------------------
# Escritura (validación determinista de lo que devuelve el modelo)
# --------------------------------------------------------------------------
def ref(n):
    return {"medio": n["medio"], "titulo": n["titulo"], "url": n["url"]}


def construir_dia(r, elegidas, todas):
    por_id = {n["id"]: n for n in elegidas}

    temas = []
    for t in r.get("temas", [])[:MAX_TEMAS]:
        fuentes = [ref(por_id[i]) for i in dict.fromkeys(t.get("ids", [])) if i in por_id]
        if t.get("tema", "").strip() and t.get("descripcion", "").strip() and t.get("categoria") in CATEGORIAS and fuentes:
            temas.append({
                "tema": t["tema"].strip(),
                "categoria": t["categoria"],
                "descripcion": t["descripcion"].strip(),
                "medios": sorted({f["medio"] for f in fuentes}),
                "fuentes": fuentes,
            })
    resumen, titular = (r.get("resumen") or "").strip(), (r.get("titular") or "").strip()[:140]
    if not temas or not resumen or not titular:
        raise RuntimeError("Gemini no devolvió titular/resumen/temas utilizables; se aborta sin tocar nada.")

    hitos = []
    for h in r.get("hitos", [])[:MAX_HITOS_DIA]:
        n = por_id.get(h.get("id"))
        if n and h.get("categoria") in CATEGORIAS and h.get("titulo", "").strip() and h.get("descripcion", "").strip():
            hitos.append({
                # fecha de la noticia (no de la ejecución): a las 7:00 se resume lo de ayer
                "fecha": datetime.fromisoformat(n["fecha"]).astimezone(MADRID).date().isoformat(),
                "edicion": HOY.isoformat(),
                "titulo": h["titulo"].strip()[:100],
                "categoria": h["categoria"],
                "descripcion": h["descripcion"].strip(),
                "relevancia": max(1, min(5, int(h.get("relevancia") or 1))),
                "fuente": ref(n),
            })

    por_medio = {m["nombre"]: sum(1 for n in todas if n["medio"] == m["nombre"]) for m in MEDIOS}
    return {
        "fecha": HOY.isoformat(),
        "generado_en": AHORA.isoformat(),
        "modelo": MODELO,
        "titular": titular,
        "resumen": resumen,
        "temas": temas,
        "enfoques": (r.get("enfoques") or "").strip(),
        "por_medio": por_medio,
        "por_categoria": dict(sorted(
            ((c, sum(1 for t in temas if t["categoria"] == c)) for c in CATEGORIAS if any(t["categoria"] == c for t in temas)),
            key=lambda kv: -kv[1])),
        "hitos": hitos,
        "noticias": [{"medio": n["medio"], "seccion": n["seccion"], "titulo": n["titulo"], "url": n["url"],
                      "fecha": n["fecha"]} for n in sorted(todas, key=lambda n: n["fecha"], reverse=True)],
    }


def escribir_dia(dia):
    tocados = []
    ruta = DATOS / "dias" / f"{dia['fecha']}.json"
    escribir_json(ruta, dia)
    tocados.append(rel(ruta))

    # índice de días (nunca se elimina ninguno)
    ruta_i = DATOS / "index.json"
    indice = {d["fecha"]: d for d in leer_json(ruta_i, {}).get("dias", [])}
    indice[dia["fecha"]] = {"fecha": dia["fecha"], "titular": dia["titular"], "noticias": len(dia["noticias"]),
                            "temas": [t["tema"] for t in dia["temas"][:3]]}
    escribir_json(ruta_i, {"dias": [indice[k] for k in sorted(indice, reverse=True)]})
    tocados.append(rel(ruta_i))

    # versión ligera para la home
    ruta_l = DATOS / "latest.json"
    escribir_json(ruta_l, {k: dia[k] for k in ("fecha", "generado_en", "titular", "por_medio")}
                  | {"temas": [{k: t[k] for k in ("tema", "categoria", "descripcion")} for t in dia["temas"][:4]]})
    tocados.append(rel(ruta_l))

    # hitos por mes (timeline): cada hito va al mes de su noticia
    por_mes = {}
    for h in dia["hitos"]:
        por_mes.setdefault(h["fecha"][:7], []).append(h)
    for mes, nuevos in por_mes.items():
        ruta_m = DATOS / "meses" / f"{mes}.json"
        m = leer_json(ruta_m, {})
        hitos = [h for h in m.get("hitos", []) if h.get("edicion") != dia["fecha"]]  # re-ejecutar una edición la sustituye
        hitos = sorted(hitos + nuevos, key=lambda h: h["fecha"])
        mejor = max(reversed(hitos), key=lambda h: h["relevancia"])  # en empate, el más antiguo
        for h in hitos:
            h["destacado"] = h is mejor
        a, mm = int(mes[:4]), int(mes[5:])
        escribir_json(ruta_m, {"mes": mes, "titulo_mes": f"{NOMBRES_MES[mm - 1]} {a}",
                               "resumen_mes": m.get("resumen_mes", ""), "hitos": hitos})
        tocados.append(rel(ruta_m))
    return tocados


def reindexar_meses():
    meses = sorted(p.stem for p in (DATOS / "meses").glob("2???-??.json"))
    escribir_json(DATOS / "meses" / "index.json", {"meses": meses})
    return [rel(DATOS / "meses" / "index.json")]


# --------------------------------------------------------------------------
def main():
    destino = DATOS / "dias" / f"{HOY.isoformat()}.json"
    if destino.exists() and not os.environ.get("FORZAR"):
        print(f"{destino.name} ya existe: nada que hacer.")
        salida({"ficheros": "", "periodo": HOY.isoformat()})
        return

    desde = AHORA - timedelta(hours=VENTANA_HORAS)
    vistas = urls_ya_vistas()
    todas = []
    for medio in MEDIOS:
        todas += [n for n in recoger(medio, desde) if n["url"] not in vistas]
    log(f"[recogida] {len(todas)} titulares nuevos en total.")

    if len(todas) < MIN_NOTICIAS:
        print(f"Solo {len(todas)} titulares nuevos (mínimo {MIN_NOTICIAS}): no se llama a Gemini.")
        salida({"ficheros": "", "periodo": HOY.isoformat()})
        return

    elegidas = seleccionar_para_prompt(todas)
    dia = construir_dia(redactar_dia(elegidas), elegidas, todas)
    tocados = escribir_dia(dia)
    tocados += cerrar_meses()
    tocados += reindexar_meses()
    print("Ficheros tocados:", " ".join(tocados))
    salida({"ficheros": " ".join(dict.fromkeys(tocados)), "periodo": HOY.isoformat()})


def salida(valores):
    ruta = os.environ.get("GITHUB_OUTPUT")
    if ruta:
        with open(ruta, "a", encoding="utf-8") as fh:
            for k, v in valores.items():
                fh.write(f"{k}={v}\n")


if __name__ == "__main__":
    main()
