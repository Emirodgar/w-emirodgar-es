#!/usr/bin/env python3
"""Atalaya: prepara los textos de los programas electorales para build_promesas.py.

Para cada documento de scripts/atalaya/programas_fuentes.json:
  1. si ya existe data-private/programas/<clave>.txt, no hace nada;
  2. si hay un PDF (descargado a mano) en data-private/programas/ o en programas-fuente/, lo convierte a texto;
  3. si no, intenta descargarlo de la web oficial del partido. Si el sitio lo bloquea (error o página de comprobación antibots),
     NO se intenta saltar el bloqueo: se avisa de dónde bajarlo a mano.
El texto íntegro nunca se publica; solo se usa para extraer citas cortas con su página.
Requiere `pdftotext` (poppler). Uso (raíz del repo): python3 scripts/atalaya/descargar_programas.py
"""
import json, os, shutil, subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
CARPETA = Path(os.environ.get("PROGRAMAS_DIR") or RAIZ / "data-private/programas")
ALTERNATIVA = RAIZ / "programas-fuente"
DOCS = json.loads((Path(__file__).parent / "programas_fuentes.json").read_text(encoding="utf8"))["documentos"]

def es_pdf(f):
    try: return f.read_bytes()[:5] == b"%PDF-"
    except OSError: return False

def a_texto(pdf, txt):
    if not shutil.which("pdftotext"): print("  falta pdftotext (poppler-utils)"); return False
    r = subprocess.run(["pdftotext", "-enc", "UTF-8", str(pdf), str(txt)], capture_output=True)
    return r.returncode == 0 and txt.exists() and txt.stat().st_size > 5000

def main():
    CARPETA.mkdir(parents=True, exist_ok=True)
    listos = 0
    for clave, d in DOCS.items():
        txt, pdf = CARPETA / f"{clave}.txt", CARPETA / f"{clave}.pdf"
        if txt.exists(): print(f"{clave}: ya hay texto"); listos += 1; continue
        if not es_pdf(pdf) and es_pdf(ALTERNATIVA / f"{clave}.pdf"): pdf = ALTERNATIVA / f"{clave}.pdf"
        if not es_pdf(pdf):
            # curl sin cabeceras propias; se comprueba que lo recibido es realmente un PDF
            subprocess.run(["curl", "-s", "-L", "-m", "180", "-o", str(CARPETA / f"{clave}.pdf"), d["url"]], capture_output=True)
            pdf = CARPETA / f"{clave}.pdf"
            if not es_pdf(pdf):
                pdf.unlink(missing_ok=True)
                print(f"{clave}: la web no entrega el PDF (bloqueo o cambio de enlace). Bájalo a mano de {d['pagina']} y guárdalo como "
                      f"data-private/programas/{clave}.pdf o programas-fuente/{clave}.pdf"); continue
        if a_texto(pdf, txt): print(f"{clave}: texto listo ({txt.stat().st_size // 1000} KB)"); listos += 1
        else: print(f"{clave}: no se pudo convertir a texto")
    meta = {k: {"titulo": v["titulo"], "url": v["url"], "fecha": v["fecha"]} for k, v in DOCS.items()}
    (CARPETA / "documentos.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf8")
    print(f"{listos} de {len(DOCS)} programas con texto")

if __name__ == "__main__":
    main()
