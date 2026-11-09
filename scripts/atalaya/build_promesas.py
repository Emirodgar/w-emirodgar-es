#!/usr/bin/env python3
"""Atalaya: extrae promesas de los programas electorales completos, con cita literal y página, para el seguimiento de cumplimiento.

Entrada (carpeta privada, no se publica):  data-private/programas/<PARTIDO>-<AAAA>.txt
    Texto del programa. Las páginas se separan con un salto de página (\\f, lo que produce `pdftotext`) o con marcas «[[PAG 12]]».
    Metadatos opcionales en data-private/programas/documentos.json:
    {"PP-2023": {"titulo": "...", "url": "https://...", "fecha": "2023-07-04"}}
Salida (pública):  atalaya/data/promesas.json   -> solo promesas CON CITA CORTA y enlace al documento, nunca el texto íntegro.

Garantías:
  - La cita debe aparecer literalmente en la página indicada (se normaliza el espacio y las mayúsculas); si el modelo parafrasea o inventa, se descarta.
  - Nunca se borra nada: se fusiona por id y se conserva el estado y las evidencias que se hayan anotado a mano.
  - Cuota: como máximo MAX_LLAMADAS peticiones a Gemini por ejecución; lo que falte se procesa otro día (se recuerda por documento).
Uso: GEMINI_API_KEY=... python3 scripts/atalaya/build_promesas.py        Variables: PROGRAMAS_DIR, MAX_LLAMADAS (5), PAGINAS_LOTE (6), GEMINI_MODEL
"""
import hashlib, json, os, re, sys, time, unicodedata, urllib.error, urllib.request
from datetime import datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
CARPETA = Path(os.environ.get("PROGRAMAS_DIR") or RAIZ / "data-private/programas")
SALIDA = RAIZ / "atalaya/data/promesas.json"
MODELO = os.environ.get("GEMINI_MODEL") or "gemini-2.5-flash"
MAX_LLAMADAS = int(os.environ.get("MAX_LLAMADAS") or 5)
PAGINAS_LOTE = int(os.environ.get("PAGINAS_LOTE") or 6)
PAUSA = float(os.environ.get("PAUSA") or 7)
TEMAS = ["Vivienda", "Sanidad", "Educación", "Impuestos", "Empleo", "Pensiones", "Energía", "Inmigración", "Derechos", "Igualdad", "Justicia",
         "Defensa", "Política exterior", "Modelo territorial", "Modelo de Estado", "Medio ambiente", "Economía", "Infraestructuras", "Otros"]

def norm(s): return re.sub(r"\s+", " ", unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()).strip()
def S(t, **kw): return {"type": t, **kw}
ESQUEMA = S("ARRAY", items=S("OBJECT", properties={"pagina": S("INTEGER"), "tema": S("STRING", enum=TEMAS), "enunciado": S("STRING"),
            "cita": S("STRING"), "medible": S("BOOLEAN")}, required=["pagina", "tema", "enunciado", "cita", "medible"]))
SISTEMA = ("Extraes promesas y compromisos concretos de un programa electoral español para un seguimiento ciudadano. "
           "Solo incluyes compromisos de acción (leyes, medidas, objetivos con cifra o plazo); no eslóganes ni diagnósticos. "
           "Para cada uno: 'pagina' = número de página indicado antes del texto; 'enunciado' = la promesa en una frase neutra (máx. 200 caracteres); "
           "'cita' = un fragmento COPIADO LITERALMENTE del texto (máx. 40 palabras) que la respalda, sin cambiar ni una palabra; "
           "'medible' = true si hay una cifra, plazo o hecho comprobable. Si no hay promesas, devuelves una lista vacía. Solo JSON válido.")

def gemini(prompt):
    clave = os.environ["GEMINI_API_KEY"]
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODELO}:generateContent"
    cfg = {"responseMimeType": "application/json", "responseSchema": ESQUEMA, "temperature": 0.1}
    if "2.5" in MODELO: cfg["thinkingConfig"] = {"thinkingBudget": 0}
    cuerpo = json.dumps({"systemInstruction": {"parts": [{"text": SISTEMA}]}, "contents": [{"role": "user", "parts": [{"text": prompt}]}], "generationConfig": cfg}).encode("utf8")
    ultimo = None
    for i in range(4):
        req = urllib.request.Request(url, data=cuerpo, method="POST", headers={"Content-Type": "application/json", "x-goog-api-key": clave})
        try:
            with urllib.request.urlopen(req, timeout=180) as r: datos = json.loads(r.read().decode("utf8"))
            parts = ((datos.get("candidates") or [{}])[0].get("content") or {}).get("parts") or []
            texto = "".join(p.get("text", "") for p in parts)
            if not texto: raise ValueError("respuesta vacía")
            return json.loads(texto)
        except urllib.error.HTTPError as e:
            ultimo = f"HTTP {e.code}"
            if e.code not in (429, 500, 502, 503, 504): break
        except (urllib.error.URLError, TimeoutError, ValueError) as e: ultimo = str(e)
        time.sleep(5 * 2 ** i)
    raise RuntimeError(ultimo)

def paginas(texto):
    if "[[PAG" in texto:
        partes = re.split(r"\[\[PAG\s*(\d+)\]\]", texto)           # ['', '1', 'texto', '2', 'texto'...]
        return [(int(partes[i]), partes[i + 1]) for i in range(1, len(partes) - 1, 2)]
    return [(n + 1, p) for n, p in enumerate(texto.split("\f")) if p.strip()]

def main():
    if not CARPETA.exists(): print(f"No existe {CARPETA}: no hay programas que procesar."); return False
    docs = sorted(CARPETA.glob("*.txt"))
    if not docs: print("Sin ficheros .txt en", CARPETA); return False
    if not os.environ.get("GEMINI_API_KEY"): print("Sin GEMINI_API_KEY: se omite la extracción."); return False
    meta = json.loads((CARPETA / "documentos.json").read_text(encoding="utf8")) if (CARPETA / "documentos.json").exists() else {}
    prev = json.loads(SALIDA.read_text(encoding="utf8")) if SALIDA.exists() else {"promesas": [], "procesado": {}}
    por_id = {p["id"]: p for p in prev["promesas"]}; hecho = prev.get("procesado", {})
    llamadas = nuevas = descartadas = 0
    for f in docs:
        clave = f.stem; partido, _, anio = clave.partition("-")
        pags = paginas(f.read_text(encoding="utf8", errors="replace"))
        inicio = hecho.get(clave, 0)                                    # nº de lotes ya procesados de este documento
        for k in range(inicio, (len(pags) + PAGINAS_LOTE - 1) // PAGINAS_LOTE):
            if llamadas >= MAX_LLAMADAS: break
            lote = pags[k * PAGINAS_LOTE:(k + 1) * PAGINAS_LOTE]
            prompt = "Extrae las promesas de estas páginas del programa:\n\n" + "\n\n".join(f"=== PÁGINA {n} ===\n{t}" for n, t in lote)
            try: res = gemini(prompt)
            except Exception as e: print(f"{clave} lote {k + 1} fallido: {e}"); break
            llamadas += 1
            texto_pag = {n: norm(t) for n, t in lote}
            for x in res:
                if x.get("pagina") not in texto_pag or norm(x.get("cita", "")) not in texto_pag[x["pagina"]]:
                    descartadas += 1; continue                           # la cita no está en esa página: no se publica
                pid = hashlib.sha1(f"{clave}|{x['pagina']}|{norm(x['cita'])}".encode()).hexdigest()[:12]
                if pid in por_id: continue
                d = meta.get(clave, {})
                por_id[pid] = {"id": pid, "partido": partido.upper(), "anio": int(anio) if anio.isdigit() else anio, "documento": clave, "pagina": x["pagina"], "tema": x["tema"],
                               "enunciado": x["enunciado"][:240], "cita": x["cita"], "medible": bool(x["medible"]), "estado": "sin_evidencia", "evidencias": [],
                               "url_documento": d.get("url"), "extraido": datetime.now(timezone.utc).strftime("%Y-%m-%d"), "modelo": MODELO}
                nuevas += 1
            hecho[clave] = k + 1
            time.sleep(PAUSA)
    SALIDA.write_text(json.dumps({"actualizado": datetime.now(timezone.utc).strftime("%Y-%m-%d"), "aviso": "Extracción automática con cita literal verificada; el estado de cumplimiento lo anota una persona con evidencia enlazada.",
                                  "procesado": hecho, "promesas": sorted(por_id.values(), key=lambda p: (p["partido"], str(p["anio"]), p["pagina"]))}, ensure_ascii=False, indent=1), encoding="utf8")
    print(f"Promesas nuevas: {nuevas}; descartadas por cita no literal: {descartadas}; peticiones: {llamadas}. Total: {len(por_id)}.")
    return True

if __name__ == "__main__":
    if main():
        sys.path.insert(0, str(Path(__file__).parent)); from manifest import marcar; marcar("promesas")
