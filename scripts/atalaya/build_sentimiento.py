#!/usr/bin/env python3
"""Atalaya: clasifica los titulares recogidos con Gemini (tono, tema, partido afectado y riesgo).

Lee atalaya/data/noticias.json y escribe atalaya/data/sentimiento.json, con caché por titular: solo se envían a
Gemini los titulares que aún no están clasificados (máx. MAX_NUEVOS por ejecución). Solo se envía el TITULAR, el medio
y un identificador: son datos ya públicos y no se manda ningún dato personal ni del repositorio.

El modelo ve solo el titular, así que el resultado es una pista orientativa, no un juicio sobre el artículo completo.
Sin GEMINI_API_KEY el script termina sin error y sin tocar nada (el resto del workflow sigue).

Uso (raíz del repo): GEMINI_API_KEY=... python3 scripts/atalaya/build_sentimiento.py
Variables: GEMINI_MODEL (por defecto gemini-2.5-flash), MAX_NUEVOS (por defecto 400), LOTE (por defecto 100), PAUSA (s entre peticiones)
"""
import hashlib, json, os, sys, time, urllib.error, urllib.request
from datetime import datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
NOTICIAS = RAIZ / "atalaya/data/noticias.json"
SALIDA = RAIZ / "atalaya/data/sentimiento.json"
MODELO = os.environ.get("GEMINI_MODEL") or "gemini-2.5-flash"
MAX_NUEVOS = int(os.environ.get("MAX_NUEVOS") or 400)
LOTE = int(os.environ.get("LOTE") or 100)              # lotes grandes: la cuota gratuita de Gemini limita las PETICIONES, no los tokens
PAUSA = float(os.environ.get("PAUSA") or 7)            # segundos entre peticiones (≈ 8 por minuto)
MAX_LLAMADAS = int(os.environ.get("MAX_LLAMADAS") or 10)    # la cuota gratuita diaria es pequeña y se comparte con la hemeroteca: no gastarla toda
MAX_FALLOS_SEGUIDOS = 2                                # con cuota agotada (429) no tiene sentido seguir insistiendo
TEMAS = ["vivienda", "sanidad", "educación", "economía", "empleo", "corrupción y justicia", "seguridad", "inmigración", "infraestructuras",
         "medio ambiente", "cultura", "modelo territorial", "elecciones y partidos", "gestión municipal", "sucesos", "otros"]
PARTIDOS = ["PP", "PSOE", "Vox", "Sumar", "Podemos", "otro", "ninguno"]

def ident(url): return hashlib.sha1(url.encode("utf8")).hexdigest()[:12]
def log(*a): print(*a, flush=True)

def S(tipo, **kw): return {"type": tipo, **kw}
ESQUEMA = S("ARRAY", items=S("OBJECT", properties={
    "id": S("STRING"),
    "tono": S("INTEGER"),
    "tema": S("STRING", enum=TEMAS),
    "partido": S("STRING", enum=PARTIDOS),
    "riesgo": S("INTEGER"),
}, required=["id", "tono", "tema", "partido", "riesgo"]))

SISTEMA = (
    "Clasificas titulares de prensa política española para un panel de análisis electoral. Solo dispones del titular "
    "(y el medio): no inventes datos ni supongas lo que no dice. Para cada titular devuelves: "
    "tono = valoración de la noticia para la imagen pública del protagonista político (persona, partido o institución) "
    "de -2 (muy negativa: imputación, escándalo, dimisión forzada, fracaso grave) a +2 (muy positiva), 0 si es neutra o puramente informativa; "
    "tema = el tema principal; partido = el partido al que afecta principalmente la noticia, o 'ninguno' si no hay uno claro; "
    "riesgo = 0 si no hay un hecho que pueda afectar a una campaña, 1 si hay polémica menor, 2 si hay un hecho relevante "
    "(detención, imputación, accidente grave, dimisión, escándalo), 3 si es muy grave y de gran alcance. "
    "Ante la duda, 0. Devuelves únicamente JSON válido con un objeto por titular recibido."
)

def gemini(prompt):
    clave = os.environ["GEMINI_API_KEY"]
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODELO}:generateContent"
    config = {"responseMimeType": "application/json", "responseSchema": ESQUEMA, "temperature": 0.1}
    if "2.5" in MODELO: config["thinkingConfig"] = {"thinkingBudget": 0}
    cuerpo = json.dumps({"systemInstruction": {"parts": [{"text": SISTEMA}]}, "contents": [{"role": "user", "parts": [{"text": prompt}]}],
                         "generationConfig": config}).encode("utf8")
    ultimo = None
    for intento in range(4):
        req = urllib.request.Request(url, data=cuerpo, method="POST", headers={"Content-Type": "application/json", "x-goog-api-key": clave})
        try:
            with urllib.request.urlopen(req, timeout=120) as r: datos = json.loads(r.read().decode("utf8"))
            cand = (datos.get("candidates") or [{}])[0]
            texto = "".join(p.get("text", "") for p in (cand.get("content") or {}).get("parts") or [])
            if not texto: raise ValueError(f"respuesta vacía ({cand.get('finishReason')})")
            return json.loads(texto)
        except urllib.error.HTTPError as e:
            ultimo = f"HTTP {e.code}: {e.read().decode('utf8', errors='replace')[:200]}"
            if e.code not in (429, 500, 502, 503, 504): break
        except (urllib.error.URLError, TimeoutError, ValueError) as e:
            ultimo = str(e)
        time.sleep(5 * 2 ** intento)
    raise RuntimeError(ultimo)

def valido(x):
    return (isinstance(x.get("tono"), int) and -2 <= x["tono"] <= 2 and isinstance(x.get("riesgo"), int) and 0 <= x["riesgo"] <= 3
            and x.get("tema") in TEMAS and x.get("partido") in PARTIDOS)

def main():
    if not os.environ.get("GEMINI_API_KEY"):
        log("Sin GEMINI_API_KEY: se omite la clasificación de sentimiento."); return False
    noticias = json.loads(NOTICIAS.read_text(encoding="utf8"))["noticias"]
    previo = json.loads(SALIDA.read_text(encoding="utf8")) if SALIDA.exists() else {"items": {}}
    items = previo.get("items", {})
    actuales = {ident(n["u"]): n for n in noticias if n.get("u")}
    pendientes = [(i, n) for i, n in actuales.items() if i not in items][:MAX_NUEVOS]
    log(f"{len(actuales)} titulares; {len(items)} ya clasificados; {len(pendientes)} nuevos a clasificar con {MODELO}")
    nuevos = fallos = seguidos = 0
    for k in range(0, len(pendientes), LOTE):
        if k // LOTE >= MAX_LLAMADAS: log(f"Límite de {MAX_LLAMADAS} peticiones diarias alcanzado: el resto se clasifica mañana."); break
        lote = pendientes[k:k + LOTE]
        prompt = "Clasifica estos titulares (formato id | medio | titular):\n" + "\n".join(f"{i} | {n['m']} | {n['t']}" for i, n in lote)
        try: res = gemini(prompt)
        except Exception as e:
            fallos += 1; seguidos += 1; log(f"Lote {k // LOTE + 1} fallido: {str(e)[:160]}")
            if seguidos >= MAX_FALLOS_SEGUIDOS: log("Demasiados fallos seguidos (¿cuota agotada?): se guarda lo clasificado y se sigue otro día."); break
            continue
        seguidos = 0
        ids = {i for i, _ in lote}
        for x in res:
            if x.get("id") in ids and valido(x):
                items[x["id"]] = {"tono": x["tono"], "tema": x["tema"], "partido": x["partido"], "riesgo": x["riesgo"]}; nuevos += 1
        time.sleep(PAUSA)
    items = {i: v for i, v in items.items() if i in actuales}           # la caché solo conserva lo que sigue en el feed
    if nuevos == 0 and not previo.get("items") and fallos:
        sys.exit("No se pudo clasificar ningún titular.")
    SALIDA.write_text(json.dumps({"modelo": MODELO, "actualizado": datetime.now(timezone.utc).isoformat(), "aviso": "Clasificación automática solo a partir del titular: orientativa.",
                                  "items": items}, ensure_ascii=False, separators=(",", ":")), encoding="utf8")
    tonos = [v["tono"] for v in items.values()]
    log(f"Clasificados {nuevos} nuevos ({fallos} lotes fallidos). Total {len(items)}. Tono medio {sum(tonos) / max(1, len(tonos)):+.2f}; negativos {sum(1 for t in tonos if t < 0)}; riesgo>=2: {sum(1 for v in items.values() if v['riesgo'] >= 2)}")
    return True
if main():   # solo se marca como actualizado si realmente se ha clasificado algo
    from manifest import marcar
    marcar("sentimiento")
