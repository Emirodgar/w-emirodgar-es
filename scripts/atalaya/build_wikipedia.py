#!/usr/bin/env python3
"""Atalaya: visitas diarias a la Wikipedia en español de los partidos y los candidatos (señal de atención ciudadana).

Fuente: API pública de estadísticas de Wikimedia (wikimedia.org/api/rest_v1/metrics/pageviews, tráfico de usuarios, sin clave).
Salida: atalaya/data/wikipedia.json   por entidad, serie diaria acumulada (se conserva lo ya guardado, hasta 400 días), visitas de
        los últimos 7 días, variación frente a los 7 anteriores y día de pico.
Mide interés (se busca o se lee), no apoyo ni intención de voto, y un pico puede deberse a un hecho puntual (debate, escándalo).
Cortesía: una petición por entidad, pausa de 0,3 s, identificada. Se usa curl: el almacén de certificados de algunos Python de Windows está caducado.
Uso (raíz del repo): python3 scripts/atalaya/build_wikipedia.py [--dias 60]
"""
import argparse, json, subprocess, sys, time, urllib.parse
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from manifest import marcar   # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
D = RAIZ / "atalaya/data"
SALIDA = D / "wikipedia.json"
UA = "EmirodgarBot/1.0 (https://emirodgar.es/atalaya)"
API = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/es.wikipedia/all-access/user/{t}/daily/{a}/{b}"
MAX_DIAS = 400
# id -> (nombre, título canónico en es.wikipedia). Mismos nombres que usan los demás paneles.
PARTIDOS = {"PP": ("PP", "Partido_Popular"), "PSOE": ("PSOE", "Partido_Socialista_Obrero_Español"), "Vox": ("Vox", "Vox_(partido_político)"),
            "Sumar": ("Sumar", "Movimiento_Sumar"), "Podemos": ("Podemos", "Podemos"), "ERC": ("ERC", "Esquerra_Republicana_de_Catalunya"),
            "Junts": ("Junts", "Junts_per_Catalunya_(partido_político)"), "EH Bildu": ("EH Bildu", "Euskal_Herria_Bildu"),
            "PNV": ("PNV", "Partido_Nacionalista_Vasco"), "BNG": ("BNG", "Bloque_Nacionalista_Galego"), "UPN": ("UPN", "Unión_del_Pueblo_Navarro"),
            "CC": ("Coalición Canaria", "Coalición_Canaria"), "SALF": ("Se Acabó La Fiesta", "Se_Acabó_La_Fiesta")}


def pedir(titulo, a, b):
    url = API.format(t=urllib.parse.quote(titulo, safe=""), a=a, b=b)
    r = subprocess.run(["curl", "-s", "-m", "30", "-A", UA, url], capture_output=True)
    try: j = json.loads(r.stdout.decode("utf8"))
    except Exception: return None
    return {i["timestamp"][:8]: i["views"] for i in j.get("items", [])}


def entidades():
    out = [{"id": k, "nombre": n, "tipo": "partido", "partido": k, "titulo": t} for k, (n, t) in PARTIDOS.items()]
    pol = json.loads((D / "politicos.json").read_text(encoding="utf8"))["politicos"]
    for p in pol:
        if p.get("ambito") == "nacional" and p.get("estado") == "candidato" and p.get("wiki"):
            out.append({"id": p["id"], "nombre": p["nombre"], "tipo": "candidato", "partido": p.get("partidoId"), "titulo": p["wiki"]})
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--dias", type=int, default=60); a = ap.parse_args()
    hoy = datetime.now(timezone.utc).date()
    fin = hoy - timedelta(days=1)                       # el día en curso no está completo
    ini = fin - timedelta(days=a.dias - 1)
    previo = {}
    if SALIDA.exists():
        for e in json.loads(SALIDA.read_text(encoding="utf8"))["entidades"]: previo[e["id"]] = {f: v for f, v in e["serie"]}
    salida = []
    for e in entidades():
        nuevos = pedir(e["titulo"], ini.strftime("%Y%m%d"), fin.strftime("%Y%m%d"))
        if nuevos is None: print("SIN DATOS", e["titulo"]); nuevos = {}
        serie = dict(previo.get(e["id"], {}))
        for ts, v in nuevos.items(): serie[f"{ts[:4]}-{ts[4:6]}-{ts[6:]}"] = v
        fechas = sorted(serie)[-MAX_DIAS:]
        s = [[f, serie[f]] for f in fechas]
        v7 = sum(v for _, v in s[-7:]); p7 = sum(v for _, v in s[-14:-7])
        pico = max(s, key=lambda x: x[1]) if s else None
        salida.append({**e, "serie": s, "v7": v7, "v7_previo": p7, "cambio": round((v7 - p7) * 100 / p7, 1) if p7 else None,
                       "pico": {"f": pico[0], "v": pico[1]} if pico else None})
        time.sleep(0.3)
    SALIDA.write_text(json.dumps({"actualizado": datetime.now(timezone.utc).replace(microsecond=0).isoformat(), "hasta": fin.isoformat(),
        "fuente": "Estadísticas de visitas de Wikipedia en español (Wikimedia, tráfico de usuarios)",
        "aviso": "Mide interés (lecturas de la ficha en Wikipedia), no apoyo ni intención de voto. Un pico puede deberse a un hecho puntual.",
        "entidades": salida}, ensure_ascii=False, separators=(",", ":")), encoding="utf8")
    marcar("wikipedia")
    print(len(salida), "entidades; hasta", fin)


if __name__ == "__main__":
    main()
