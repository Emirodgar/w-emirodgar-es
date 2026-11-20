#!/usr/bin/env python3
"""Atalaya: valida atalaya/data/debates.json (archivo de debates y entrevistas) y marca su frescura.

Los debates se redactan a mano (o con ayuda) en el JSON; este script NO sobrescribe nada: solo comprueba el esquema,
ordena por fecha y registra la fecha en el manifiesto. Un debate nunca se borra: si queda obsoleto, estado != "vigente".
Uso (raíz del repo): python3 scripts/atalaya/build_debates.py
"""
import json, re, sys
from pathlib import Path

RUTA = Path(__file__).resolve().parents[2] / "atalaya/data/debates.json"
VEREDICTOS = {"verdadero", "enganoso", "falso", "sin_veredicto"}
TIPOS = {"debate", "entrevista", "comparecencia", "mitin"}

def main():
    d = json.loads(RUTA.read_text(encoding="utf8"))
    err, ids = [], set()
    for x in d["debates"]:
        i = x.get("id", "?")
        if i in ids: err.append(f"{i}: id duplicado")
        ids.add(i)
        if not re.match(r"^\d{4}-\d{2}-\d{2}-", i): err.append(f"{i}: el id debe empezar por la fecha AAAA-MM-DD")
        if x.get("tipo") not in TIPOS: err.append(f"{i}: tipo desconocido")
        pid = {p["id"] for p in x.get("participantes", [])}
        if len(pid) < 1: err.append(f"{i}: sin participantes")
        for b in x.get("bloques", []):
            for r in b["resumen"]:
                if r["p"] not in pid: err.append(f"{i}: participante desconocido «{r['p']}» en bloque {b['tema']}")
        for a in x.get("afirmaciones", []):
            if a["p"] not in pid: err.append(f"{i}/{a['id']}: participante desconocido")
            for v in a["veredictos"]:
                if v["veredicto"] not in VEREDICTOS: err.append(f"{i}/{a['id']}: veredicto inválido «{v['veredicto']}»")
        for f in x.get("fuentes", []):
            if not f["url"].startswith("http"): err.append(f"{i}: fuente sin URL válida")
        if not x.get("fuentes"): err.append(f"{i}: sin fuentes")
    if err:
        print("\n".join(err)); sys.exit(1)
    d["debates"].sort(key=lambda x: x["fecha"], reverse=True)
    RUTA.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf8")
    sys.path.insert(0, str(Path(__file__).parent)); from manifest import marcar; marcar("debates")
    print(f"debates.json OK: {len(d['debates'])} debate(s)")

if __name__ == "__main__":
    main()
