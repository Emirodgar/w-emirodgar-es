#!/usr/bin/env python3
"""Atalaya: archivo histórico acumulativo. Principio del proyecto: NUNCA se borra nada; solo se añade.

Lo que hacen los ficheros «vivos» (noticias.json, sentimiento.json…) es mostrar el estado actual, y ese estado se renueva y poda.
Este script copia a un archivo permanente, con fecha de primera captura, todo lo que va apareciendo:

  atalaya/data/archivo/noticias/AAAA-MM-DD.jsonl.gz      titulares vistos por primera vez ese día (uno por línea; sin duplicados)
  atalaya/data/archivo/sentimiento/AAAA-MM-DD.jsonl.gz   clasificaciones de Gemini hechas ese día (con el modelo)
  atalaya/data/archivo/snapshots/<nombre>/AAAA-MM-DD.json.gz   foto de politicos_prov / escanos / programas / padron SOLO cuando cambian
  atalaya/data/archivo/resumen.json                      contadores para el menú Fuentes

Los ficheros diarios son inmutables (se escriben una vez), así que el repositorio crece poco a poco y sin reescrituras.
Uso (raíz del repo): python3 scripts/atalaya/archivo.py
"""
import gzip, hashlib, json
from datetime import datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
D = RAIZ / "atalaya/data"
A = D / "archivo"
HOY = datetime.now(timezone.utc).strftime("%Y-%m-%d")
SNAPSHOTS = ["politicos_prov", "escanos", "programas", "padron"]

def leer_lineas(ruta):
    with gzip.open(ruta, "rt", encoding="utf8") as f:
        for l in f:
            if l.strip(): yield json.loads(l)

def escribir_lineas(ruta, filas):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    # mtime=0: el .gz es determinista (mismo contenido = mismos bytes) y git no ve cambios falsos
    with open(ruta, "wb") as raw, gzip.GzipFile(fileobj=raw, mode="wb", mtime=0, compresslevel=9) as f:
        for r in filas: f.write((json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf8"))

def ids_archivados(carpeta):
    vistos = set()
    for f in sorted(carpeta.glob("*.jsonl.gz")):
        for r in leer_lineas(f): vistos.add(r["i"])
    return vistos

def anadir_al_dia(carpeta, nuevas):
    """Añade filas al fichero de hoy sin tocar lo ya archivado (los ids se comparan antes con todo el archivo)."""
    destino = carpeta / f"{HOY}.jsonl.gz"
    previas = list(leer_lineas(destino)) if destino.exists() else []
    if nuevas: escribir_lineas(destino, previas + nuevas)

def archivar_noticias():
    carp = A / "noticias"
    vistos = ids_archivados(carp) if carp.exists() else set()
    actuales = json.loads((D / "noticias.json").read_text(encoding="utf8"))["noticias"]
    nuevas = [n for n in actuales if n.get("i") and n["i"] not in vistos]
    anadir_al_dia(carp, nuevas)
    return len(nuevas), len(vistos)

def archivar_sentimiento():
    f = D / "sentimiento.json"
    if not f.exists(): return 0
    sj = json.loads(f.read_text(encoding="utf8"))
    carp = A / "sentimiento"
    vistos = ids_archivados(carp) if carp.exists() else set()
    nuevas = [{"i": i, **v, "modelo": sj.get("modelo")} for i, v in sj["items"].items() if i not in vistos]
    anadir_al_dia(carp, nuevas)
    return len(nuevas)

def foto(nombre):
    f = D / f"{nombre}.json"
    if not f.exists(): return False
    texto = f.read_bytes()
    j = json.loads(texto)
    if isinstance(j, dict):                      # las marcas de fecha cambian en cada ejecución aunque los datos sean los mismos
        for k in ("actualizado", "generado"): j.pop(k, None)
    h = hashlib.sha1(json.dumps(j, sort_keys=True, ensure_ascii=False).encode("utf8")).hexdigest()
    carp = A / "snapshots" / nombre
    carp.mkdir(parents=True, exist_ok=True)
    marca = carp / "ultimo.sha1"
    if marca.exists() and marca.read_text().strip() == h: return False
    nombre = f"{HOY}.json.gz"
    if (carp / nombre).exists(): nombre = f"{HOY}-{datetime.now(timezone.utc).strftime('%H%M')}.json.gz"   # nunca se pisa una foto anterior
    with open(carp / nombre, "wb") as raw, gzip.GzipFile(fileobj=raw, mode="wb", mtime=0, compresslevel=9) as g: g.write(texto)
    marca.write_text(h)
    return True

def resumen():
    n = sum(1 for f in (A / "noticias").glob("*.jsonl.gz") for _ in leer_lineas(f)) if (A / "noticias").exists() else 0
    s = sum(1 for f in (A / "sentimiento").glob("*.jsonl.gz") for _ in leer_lineas(f)) if (A / "sentimiento").exists() else 0
    dias = sorted(f.name[:10] for f in (A / "noticias").glob("*.jsonl.gz")) if (A / "noticias").exists() else []
    snaps = {k: len(list((A / "snapshots" / k).glob("*.json.gz"))) for k in SNAPSHOTS if (A / "snapshots" / k).exists()}
    out = {"actualizado": HOY, "noticias": n, "clasificaciones": s, "desde": dias[0] if dias else None, "dias": len(dias), "fotos": snaps}
    (A / "resumen.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf8")
    return out

def main():
    A.mkdir(parents=True, exist_ok=True)
    nuevas_n, antes = archivar_noticias()
    nuevas_s = archivar_sentimiento()
    cambios = [k for k in SNAPSHOTS if foto(k)]
    r = resumen()
    print(f"Archivo: +{nuevas_n} titulares (ya había {antes}), {nuevas_s} clasificaciones del día, fotos nuevas: {cambios or 'ninguna'}. "
          f"Total: {r['noticias']} titulares en {r['dias']} días, {r['clasificaciones']} clasificaciones.")

if __name__ == "__main__":
    main()
    from manifest import marcar
    marcar("archivo")
