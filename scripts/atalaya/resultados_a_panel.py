#!/usr/bin/env python3
"""Atalaya: puente entre los resultados de Interior ya importados y el panel «Elecciones en España».

Flujo de la noche electoral (los resultados de Interior se descargan a mano, como ya se hace con build_interior.py):
  1. Guardar el .zip de «Congreso | Noviembre 2026 | Resultados por municipio» (y «por circunscripción») en data-private/interior/
  2. python3 scripts/atalaya/build_interior.py                      -> atalaya/data/resultados/congreso-2026-11/…
  3. python3 scripts/atalaya/resultados_a_panel.py congreso-2026-11  -> elecciones-espana/data/2026-11-29/resultados.json
     (el panel pasa de «El Congreso hoy (disuelto)» a «Resultados: así quedó el Congreso»)

Suma los escaños y los votos de las 52 circunscripciones y asigna cada candidatura al id de partidos.json. La participación NO se calcula:
la suma provincial da un dato distinto del oficial (66,6 % frente al 70,4 % de 2023), así que se pasa a mano con --participacion.
Las candidaturas que no se reconocen (p. ej. una coalición nueva) se cuentan en la nota y se imprimen: añadirlas a MAPA si hay que mostrarlas.
Sin argumento de salida escribe solo si la elección es congreso-2026-11; con otra elección (p. ej. congreso-2023-07, para probar) imprime el resultado.
Uso: python3 scripts/atalaya/resultados_a_panel.py [eleccion] [--participacion 70.4] [--salida ruta.json]
"""
import argparse, json, re, sys, unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
RES = RAIZ / "atalaya/data/resultados"
PANEL = RAIZ / "elecciones-espana/data/2026-11-29"
ELECCION_29N = "congreso-2026-11"

# candidatura de Interior (clave o nombre, sin acentos y en minúsculas) -> id de partidos.json
MAPA = [(r"^pp$|partido popular", "PP"), (r"^psoe$|partido socialista obrero", "PSOE"), (r"^vox$", "VOX"), (r"^sumar$", "SUMAR"),
        (r"^erc|esquerra republicana", "ERC"), (r"junts", "JUNTS"), (r"bildu", "BILDU"), (r"eaj|pnv|nacionalista vasco", "PNV"),
        (r"^podemos$", "PODEMOS"), (r"compromis", "COMPROMIS"), (r"b\.n\.g|bloque nacionalista gal", "BNG"),
        (r"^cca$|coalicion canaria", "CC"), (r"u\.p\.n|union del pueblo navarro", "UPN"), (r"^salf$|acabo la fiesta", "SALF")]


def norm(s): return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower().strip()


def pid(clave, nombre):
    for rx, i in MAPA:
        if re.search(rx, norm(clave)) or re.search(rx, norm(nombre or "")): return i
    return None


def calcular(eleccion):
    d = json.loads((RES / eleccion / "circunscripciones.json").read_text(encoding="utf8"))["prov"]
    indice = json.loads((RES / "indice.json").read_text(encoding="utf8"))["elecciones"][eleccion]
    nombres = indice.get("partidos", {})
    esc, votos, desconocidas = {}, {}, {}
    censo = votantes = validos = 0
    for p in d.values():
        censo += p["censo"]; votantes += p["votantes"]; validos += p["validos"]
        for clave, (v, e) in p["v"].items():
            i = pid(clave, nombres.get(clave))
            if i: esc[i] = esc.get(i, 0) + e; votos[i] = votos.get(i, 0) + v
            elif e: desconocidas[clave] = desconocidas.get(clave, 0) + e
    total = sum(esc.values()) + sum(desconocidas.values())
    ord_ = sorted(votos, key=lambda k: -votos[k])
    nota = "Porcentajes de voto calculados sumando las 52 circunscripciones: pueden diferir en centésimas del dato oficial."
    if desconocidas:
        nota += " Otras candidaturas con escaños: " + ", ".join(f"{k} ({n})" for k, n in desconocidas.items()) + "."
    return {"disponible": True, "fechaEscrutinio": None, "participacion": None,
            "escanos": {k: esc[k] for k in sorted(esc, key=lambda k: -esc[k]) if esc[k]},
            "votoPct": {k: round(votos[k] / validos * 100, 2) for k in ord_}, "nota": nota}, total, desconocidas


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("eleccion", nargs="?", default=ELECCION_29N); ap.add_argument("--salida"); ap.add_argument("--participacion", type=float)
    a = ap.parse_args()
    res, total, desc = calcular(a.eleccion)
    if a.eleccion == ELECCION_29N:
        conv = json.loads((PANEL / "convocatoria.json").read_text(encoding="utf8"))
        res["fechaEscrutinio"] = conv.get("fecha")
    else:
        res.pop("fechaEscrutinio")
    if a.participacion is not None: res["participacion"] = a.participacion
    else: res.pop("participacion"); print("AVISO: sin --participacion, el panel no mostrará la participación", file=sys.stderr)
    if total != 350: print(f"AVISO: los escaños suman {total}, no 350: revisar el fichero de Interior y MAPA", file=sys.stderr)
    for k, n in desc.items(): print(f"AVISO: candidatura sin asignar a un partido: {k} ({n} escaños)", file=sys.stderr)
    salida = Path(a.salida) if a.salida else (PANEL / "resultados.json" if a.eleccion == ELECCION_29N else None)
    txt = json.dumps(res, ensure_ascii=False, indent=1)
    if salida: salida.write_text(txt, encoding="utf8"); print("Escrito", salida)
    else: sys.stdout.reconfigure(encoding="utf-8"); print(txt)


if __name__ == "__main__":
    main()
