#!/usr/bin/env python3
"""Atalaya: panel de tendencias. Cuenta cuántas veces aparece cada partido y político en los titulares recogidos por RSS.

Entrada : atalaya/data/archivo/noticias/*.jsonl.gz (histórico) + atalaya/data/noticias.json (vivo) + clasificación de tono (sentimiento).
Salida  : atalaya/data/tendencias_vivo.json  (eventos compactos de los últimos 30 días; la página agrega por periodo y territorio).
"picos" / "picos_ccaa": entidades cuya cuota reciente (en España / en cada comunidad) se dispara sobre su nivel habitual (ver picos()); se archivan en picos_historial.json.
Cada evento es [hora desde "base", [entidades], provincias (códigos INE de 2 cifras pegados: "3708"), tono (-1/0/1; 2 = sin clasificar), índice de titular o -1, nº de titulares].
Solo lee: no modifica el archivo histórico. Solo librería estándar.
Uso (raíz del repo): python3 scripts/atalaya/build_tendencias_vivo.py
"""
import gzip, json, re, unicodedata
from datetime import datetime, timedelta, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
D = RAIZ / "atalaya/data"
DIAS = 30
HORAS_TITULARES = 24   # titulares enlazables solo de las últimas 24 h (mantiene el fichero pequeño)

def norm(s): return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()

# (id, nombre, color, regex sobre el titular normalizado: sin tildes y en minúsculas). Partido = aparece su nombre o siglas.
PARTIDOS = [
    ("PP", "PP", "#3b82f6", r"\bpp\b|partido popular|populares"),
    ("PSOE", "PSOE", "#ef4444", r"\bpsoe\b|socialistas?\b|partido socialista"),
    ("Vox", "Vox", "#84cc16", r"\bvox\b"),
    ("Sumar", "Sumar", "#ec4899", r"\bsumar\b"),
    ("Podemos", "Podemos", "#a855f7", None),   # se trata aparte: «podemos» también es un verbo
    ("ERC", "ERC", "#f59e0b", r"\berc\b|esquerra republicana"),
    ("Junts", "Junts", "#14b8a6", r"\bjunts\b"),
    ("Bildu", "EH Bildu", "#a3e635", r"\bbildu\b"),
    ("PNV", "PNV", "#16a34a", r"\bpnv\b"),
    ("BNG", "BNG", "#38bdf8", r"\bbng\b"),
    ("CC", "Coalición Canaria", "#eab308", r"coalicion canaria"),
    ("UPN", "UPN", "#f87171", r"\bupn\b"),
    ("Compromis", "Compromís", "#fb923c", r"\bcompromis\b"),
    ("UPL", "UPL", "#c084fc", r"\bupl\b|union del pueblo leones"),
    ("SALF", "Se Acabó La Fiesta", "#facc15", r"\bsalf\b|se acabo la fiesta|\balvise\b"),
]
PODEMOS_RX = re.compile(r"\b(Podemos|PODEMOS)\b")

# (id, nombre, partido, regex del apellido solo, regex del nombre completo). El apellido solo se admite en prensa nacional
# cuando es ambiguo (Sánchez, Díaz, Montero): en prensa local podría ser un alcalde o un concejal.
POLITICOS = [
    ("sanchez", "Pedro Sánchez", "PSOE", r"\bsanchez\b", r"pedro sanchez", True),
    ("feijoo", "Alberto Núñez Feijóo", "PP", r"\bfeijoo\b", None, False),
    ("abascal", "Santiago Abascal", "Vox", r"\babascal\b", None, False),
    ("ayuso", "Isabel Díaz Ayuso", "PP", r"\bayuso\b", None, False),
    ("manueco", "Alfonso Fernández Mañueco", "PP", r"\bmanueco\b", None, False),
    ("zapatero", "José Luis Rodríguez Zapatero", "PSOE", r"\bzapatero\b", None, False),
    ("yolanda", "Yolanda Díaz", "Sumar", None, r"yolanda diaz", False),
    ("irene", "Irene Montero", "Podemos", None, r"irene montero", False),
    ("montero", "María Jesús Montero", "PSOE", r"\bmontero\b", r"maria jesus montero", True),
    ("puigdemont", "Carles Puigdemont", "Junts", r"\bpuigdemont\b", None, False),
    ("junqueras", "Oriol Junqueras", "ERC", r"\bjunqueras\b", None, False),
    ("rufian", "Gabriel Rufián", "ERC", r"\brufian\b", None, False),
    ("illa", "Salvador Illa", "PSOE", r"\bsalvador illa\b|\billa\b", None, True),
    ("colau", "Ada Colau", "Sumar", r"\bcolau\b", None, False),
    ("page", "Emiliano García-Page", "PSOE", r"\bgarcia-page\b|\bpage\b", None, True),
    ("moreno", "Juanma Moreno", "PP", None, r"juanma moreno|moreno bonilla", False),
]
COLORES = {p[0]: p[2] for p in PARTIDOS}

# Código INE de provincia → comunidad autónoma
CCAA = {
    "Andalucía": ["04", "11", "14", "18", "21", "23", "29", "41"], "Aragón": ["22", "44", "50"], "Asturias": ["33"],
    "Illes Balears": ["07"], "Canarias": ["35", "38"], "Cantabria": ["39"], "Castilla y León": ["05", "09", "24", "34", "37", "40", "42", "47", "49"],
    "Castilla-La Mancha": ["02", "13", "16", "19", "45"], "Cataluña": ["08", "17", "25", "43"], "C. Valenciana": ["03", "12", "46"],
    "Extremadura": ["06", "10"], "Galicia": ["15", "27", "32", "36"], "Madrid": ["28"], "Murcia": ["30"], "Navarra": ["31"],
    "País Vasco": ["01", "20", "48"], "La Rioja": ["26"], "Ceuta": ["51"], "Melilla": ["52"],
}

def leer_gz(ruta):
    with gzip.open(ruta, "rt", encoding="utf8") as f:
        for l in f:
            if l.strip(): yield json.loads(l)

# Detección de picos: se compara la CUOTA de una entidad en la ventana reciente con su cuota habitual de los 7 días anteriores.
# Usar la cuota (y no el recuento) descuenta los cambios de volumen de la recogida; el esperado es cuota_habitual × titulares de la ventana,
# y el pico exige a la vez un mínimo de menciones, una razón sobre lo esperado y una desviación significativa. La desviación usa una varianza
# inflada (DISPERSION): un mismo hecho sale en muchos medios a la vez, así que los recuentos fluctúan mucho más que en un Poisson puro.
# Ajustado con una prueba sobre los últimos 10 días para que avise en una minoría de ventanas (si suena siempre, no avisa de nada).
# (ventana en horas, etiqueta, mínimo de menciones, razón mínima sobre lo esperado)
VENTANAS = [(6, "6 h", 15, 2.2), (24, "24 h", 40, 3.0)]
Z_MIN, BASE_MIN, DISPERSION = 3.0, 3000, 4.0
# Por comunidad hay mucho menos volumen y se hacen ~19 veces más pruebas (comunidad × entidad): umbrales de volumen más bajos pero z más exigente.
VENTANAS_CCAA = [(6, "6 h", 8, 2.5), (24, "24 h", 25, 3.0)]
Z_MIN_CCAA, BASE_MIN_CCAA, TW_MIN_CCAA = 4.0, 400, 20

def picos(eventos, th, hn, ventanas=None, base_min=None, tw_min=50, z_min=None):
    ventanas = ventanas or VENTANAS; base_min = base_min or BASE_MIN; z_min = z_min or Z_MIN
    out = {}
    for hrs, etq, min_n, ratio_min in ventanas:
        w0, b1 = hn - hrs + 1, hn - hrs
        b0 = max(0, b1 - 168 + 1)
        tw, tb = sum(th[w0:hn + 1]), sum(th[b0:b1 + 1])
        if tb < base_min or tw < tw_min: continue
        ow, ob = {}, {}
        for h, es, _p, _t, _ti, n in eventos:
            if w0 <= h <= hn:
                for e in es: ow[e] = ow.get(e, 0) + n
            elif b0 <= h <= b1:
                for e in es: ob[e] = ob.get(e, 0) + n
        for e, obs in ow.items():
            esp = max(ob.get(e, 0) / tb * tw, 3.0)   # suelo de 3: una entidad casi nueva no dispara razones infinitas
            ratio, z = obs / esp, (obs - esp) / (DISPERSION * esp) ** 0.5
            if obs >= min_n and ratio >= ratio_min and z >= z_min and (e not in out or z > out[e]["z"]):
                out[e] = {"e": e, "v": etq, "n": obs, "esp": round(esp, 1), "ratio": round(ratio, 2), "z": round(z, 1)}
    return sorted(out.values(), key=lambda x: -x["z"])

def picos_ccaa(eventos, th_c, hn):
    """Mismo método, restringido a los titulares de cada comunidad (por sus provincias) y con su propia base de titulares."""
    out = []
    for c, provs in CCAA.items():
        ps = set(provs)
        ev_c = [e for e in eventos if any(e[2][i:i + 2] in ps for i in range(0, len(e[2]), 2))]
        for x in picos(ev_c, th_c[c], hn, VENTANAS_CCAA, BASE_MIN_CCAA, TW_MIN_CCAA, Z_MIN_CCAA): out.append({"c": c, **x})
    return sorted(out, key=lambda x: -x["z"])

def registrar_picos(pk, ahora):
    """Historial permanente (solo añade; nunca borra): un pico por entidad, ámbito y ventana de 6 h."""
    if not pk: return
    f = D / "picos_historial.json"
    h = json.loads(f.read_text(encoding="utf8")) if f.exists() else []
    cubo = ahora.strftime("%Y-%m-%d") + f"T{ahora.hour // 6 * 6:02d}"
    vistos = {(r["id"], r["v"], r["cubo"], r.get("c", "")) for r in h}
    nuevos = [{"cubo": cubo, "f": ahora.isoformat(timespec="minutes"), "id": ENT_IDS[x["e"]], **({"c": x["c"]} if x.get("c") else {}), "v": x["v"], "n": x["n"], "esp": x["esp"], "ratio": x["ratio"], "z": x["z"]}
              for x in pk if (ENT_IDS[x["e"]], x["v"], cubo, x.get("c", "")) not in vistos]
    if nuevos: f.write_text(json.dumps(h + nuevos, ensure_ascii=False, separators=(",", ":")), encoding="utf8")

ENT_IDS = [p[0] for p in PARTIDOS] + [x[0] for x in POLITICOS]   # índice de entidad → id (mismo orden que en main)

def main():
    ahora = datetime.now(timezone.utc)
    base = (ahora - timedelta(days=DIAS)).replace(minute=0, second=0, microsecond=0)
    filas = {}
    for f in sorted((D / "archivo/noticias").glob("*.jsonl.gz")):
        for n in leer_gz(f): filas[n["i"]] = n
    for n in json.loads((D / "noticias.json").read_text(encoding="utf8"))["noticias"]: filas[n["i"]] = n

    tono = {}
    for f in sorted((D / "archivo/sentimiento").glob("*.jsonl.gz")):
        for r in leer_gz(f): tono[r["i"]] = r.get("tono")
    sj = D / "sentimiento.json"
    if sj.exists():
        for i, r in json.loads(sj.read_text(encoding="utf8")).get("items", {}).items(): tono[i] = r.get("tono")

    ents = [(p[0], p[1], "partido", p[2], None) for p in PARTIDOS] + [(x[0], x[1], "politico", COLORES.get(x[2], "#94a3b8"), x[2]) for x in POLITICOS]
    idx = {e[0]: k for k, e in enumerate(ents)}
    pat_p = [(idx[p[0]], re.compile(p[3])) for p in PARTIDOS if p[3]]
    pat_x = [(idx[x[0]], re.compile(x[3]) if x[3] else None, re.compile(x[4]) if x[4] else None, x[5]) for x in POLITICOS]

    eventos, titulares, totales, agrupados = [], [], {}, {}
    nh = DIAS * 24 + 2
    totales_h = [0] * nh   # todos los titulares por hora (con o sin mención): base para medir la cuota de cada entidad
    p2c = {p: c for c, ps in CCAA.items() for p in ps}
    th_c = {c: [0] * nh for c in CCAA}   # titulares por hora y comunidad (para la cuota local)
    limite_tit = ahora - timedelta(hours=HORAS_TITULARES)
    for n in sorted(filas.values(), key=lambda x: x["f"]):
        try: dt = datetime.fromisoformat(n["f"]).astimezone(timezone.utc)
        except Exception: continue
        if dt < base or dt > ahora + timedelta(hours=1): continue
        dia = dt.strftime("%Y-%m-%d"); totales[dia] = totales.get(dia, 0) + 1
        hh = int((dt - base).total_seconds() // 3600)
        if 0 <= hh < nh:
            totales_h[hh] += 1
            for c in {p2c[p] for p in n.get("pv", []) if p in p2c}: th_c[c][hh] += 1
        t = n["t"]; nt = norm(t); nacional = n.get("a") == "nacional"
        hit = {k for k, rx in pat_p if rx.search(nt)}
        if PODEMOS_RX.search(t): hit.add(idx["Podemos"])
        for k, solo, completo, ambiguo in pat_x:
            if (completo and completo.search(nt)) or (solo and (nacional or not ambiguo) and solo.search(nt)): hit.add(k)
        if not hit: continue
        h = int((dt - base).total_seconds() // 3600)
        ti = -1
        if dt >= limite_tit:
            ti = len(titulares); titulares.append({"t": t, "u": n["u"], "m": n.get("m", ""), "f": n["f"]})
        ev = [h, sorted(hit), "".join(sorted(p for p in n.get("pv", []) if len(p) == 2)), tono.get(n["i"]) if tono.get(n["i"]) in (-1, 0, 1) else 2, ti]
        if ti >= 0: eventos.append(ev + [1])
        else:   # sin titular enlazable: se agrupan los eventos idénticos (misma hora, entidades, provincias y tono) con un contador
            k = json.dumps(ev[:4])
            if k in agrupados: agrupados[k][5] += 1
            else: agrupados[k] = ev + [1]; eventos.append(agrupados[k])

    hn = int((ahora - base).total_seconds() // 3600)
    pk = picos(eventos, totales_h, hn)
    pkc = picos_ccaa(eventos, th_c, hn)
    registrar_picos(pk + pkc, ahora)
    ind = json.loads((D / "indice.json").read_text(encoding="utf8"))["prov"]
    salida = {
        "generado": ahora.isoformat(), "base": base.isoformat(), "dias": DIAS,
        "aviso": "Cuenta titulares de prensa recogidos por RSS donde aparece el nombre del partido o político. Mide presencia mediática, no apoyo ni intención de voto. "
                 "El tono es una clasificación automática del titular y solo existe para parte de ellos.",
        "entidades": [{"id": e[0], "n": e[1], "tipo": e[2], "c": e[3], **({"p": e[4]} if e[4] else {})} for e in ents],
        "provincias": ind, "ccaa": CCAA, "totales": totales, "totales_h": totales_h, "titulares": titulares, "eventos": eventos, "picos": pk, "picos_ccaa": pkc,
    }
    (D / "tendencias_vivo.json").write_text(json.dumps(salida, ensure_ascii=False, separators=(",", ":")), encoding="utf8")
    print(len(filas), "titulares leídos;", len(eventos), "con alguna mención;", len(titulares), "enlazables;", f"{(D / 'tendencias_vivo.json').stat().st_size // 1024} KB")

if __name__ == "__main__":
    main()
