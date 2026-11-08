"""Atalaya: manifiesto de frescura. Cada script de datos llama a marcar("nombre") al terminar bien;
el menú Fuentes lo lee para avisar de qué datos están desactualizados.

atalaya/data/manifest.json  ->  {"noticias": "2026-11-08T09:25:11+00:00", "escanos": "...", ...}
"""
import json
from datetime import datetime, timezone
from pathlib import Path

RUTA = Path(__file__).resolve().parents[2] / "atalaya/data/manifest.json"

def marcar(nombre):
    try: d = json.loads(RUTA.read_text(encoding="utf8"))
    except Exception: d = {}
    d[nombre] = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    RUTA.write_text(json.dumps(dict(sorted(d.items())), ensure_ascii=False, indent=1), encoding="utf8")
