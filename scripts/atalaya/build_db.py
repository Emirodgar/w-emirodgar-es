#!/usr/bin/env python3
"""Atalaya: carga todos los datos disponibles en una base SQLite estructurada (esquema.sql).

Salida: data-private/atalaya.sqlite (fuera de git y fuera de la web publicada).
Orden: build_geo.py -> build_news.py -> build_politicos.py -> build_db.py
Uso (raíz del repo): python3 scripts/atalaya/build_db.py
"""
import json, sqlite3
from datetime import datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
D = RAIZ / "atalaya/data"; E = RAIZ / "elecciones-espana/data"
OUT = RAIZ / "data-private/atalaya.sqlite"
J = lambda p: json.loads(Path(p).read_text(encoding="utf8"))

def main():
    OUT.parent.mkdir(exist_ok=True)
    if OUT.exists(): OUT.unlink()
    db = sqlite3.connect(OUT); db.executescript((Path(__file__).parent / "esquema.sql").read_text(encoding="utf8"))
    ahora = datetime.now(timezone.utc).isoformat()

    # territorio
    ind = J(D / "indice.json"); provs = ind["prov"]
    db.execute("INSERT INTO territorio VALUES ('ES','pais','España',NULL,NULL,NULL)")
    db.executemany("INSERT INTO territorio(codigo,nivel,nombre,padre) VALUES (?, 'provincia', ?, 'ES')", provs.items())
    db.executemany("INSERT OR IGNORE INTO territorio(codigo,nivel,nombre,padre) VALUES (?, 'municipio', ?, ?)",
                   [(c, n, c[:2]) for c, n in ind["mun"] if c[:2] in provs])

    # fuentes, partidos, elecciones
    fuentes = {}
    def fuente(nombre, tipo):
        if nombre not in fuentes:
            fuentes[nombre] = db.execute("INSERT INTO fuente(nombre,tipo) VALUES (?,?)", (nombre, tipo)).lastrowid
        return fuentes[nombre]
    for p in J(E / "2026-11-29/partidos.json")["partidos"]:
        db.execute("INSERT OR IGNORE INTO partido VALUES (?,?,?,?,?,?)", (p["id"], p["nombre"], p.get("siglas"), p.get("color"), p.get("ambito"), p.get("ideologia")))
    for e in J(E / "elecciones.json")["elecciones"]:
        db.execute("INSERT OR IGNORE INTO eleccion VALUES (?,?,?,?)", (e["id"], e["tipo"], e["fecha"], "ES"))

    # encuestas
    f_enc = fuente("Sondeos publicados (elecciones-espana)", "encuesta")
    for s in J(E / "2026-11-29/encuestas.json")["sondeos"]:
        i = db.execute("INSERT INTO encuesta(fecha,empresa,medio,muestra,tipo,fuente_id) VALUES (?,?,?,?,?,?)",
                       (s["fecha"], s["empresa"], s.get("medio"), s.get("muestra"), s.get("tipo"), f_enc)).lastrowid
        db.executemany("INSERT INTO encuesta_voto VALUES (?,?,?)", [(i, k, v) for k, v in s["voto"].items()])

    # políticos
    pol = J(D / "politicos.json")["politicos"]
    db.executemany("INSERT INTO politico VALUES (?,?,?,?,?,?,?,?,?)",
                   [(p["id"], p["nombre"], p["partidoId"], p.get("cargo"), p["ambito"], p.get("prov"), p["estado"], p.get("wiki"), json.dumps(p["alias"], ensure_ascii=False)) for p in pol])
    import re, unicodedata
    n = lambda s: unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    rx = [(p["id"], [re.compile(r"(?<!\w)" + re.escape(n(a)) + r"(?!\w)") for a in p["alias"]]) for p in pol if p["alias"]]

    # artículos
    for a in J(D / "noticias.json")["noticias"]:
        aid = db.execute("INSERT OR IGNORE INTO articulo(url,titulo,medio,fuente_id,ambito,tipo,publicado,capturado) VALUES (?,?,?,?,?,?,?,?)",
                         (a["u"], a["t"], a["m"], fuente(a["m"], "prensa"), a["a"], "noticia", a["f"], ahora)).lastrowid
        if not aid: continue
        db.executemany("INSERT OR IGNORE INTO articulo_territorio VALUES (?,?,?,?)",
                       [(aid, c, "nombre", .6) for c in a["mun"]] + [(aid, c, "nombre", .7) for c in a["pv"] if c not in {m[:2] for m in a["mun"]} or True])
        db.executemany("INSERT OR IGNORE INTO articulo_partido VALUES (?,?)", [(aid, p.upper() if p != "Sumar" else "SUMAR") for p in a["p"]])
        t = n(a["t"])
        db.executemany("INSERT OR IGNORE INTO articulo_politico VALUES (?,?)", [(aid, pid) for pid, r in rx if any(x.search(t) for x in r)])
        db.execute("INSERT INTO analisis VALUES (?,?,?,?,?,?,?,?)", (aid, "palabras-clave", "0.1", ahora, None, None, int(a["r"]), None))
    db.commit()
    for t in ["territorio", "partido", "politico", "encuesta", "encuesta_voto", "articulo", "articulo_territorio", "articulo_politico", "analisis"]:
        print(f"{t:22}", db.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0])
    db.close()
main()
