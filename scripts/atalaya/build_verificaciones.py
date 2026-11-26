#!/usr/bin/env python3
"""Atalaya: verificaciones políticas de Maldita.es (Maldito Bulo), Newtral, EFE Verifica y Verificat, por RSS público.

Se queda con las piezas que nombran a un partido o candidato, o hablan de elecciones, y las etiqueta por partido. No juzga: guarda el
titular, el enlace y las categorías del propio verificador. No intenta adivinar el veredicto: los titulares («X no hizo Y», «el vídeo es un deepfake»)
no se dejan clasificar de forma fiable por palabras clave.
Nunca se borra nada: cada pieza se archiva una vez, con la fecha de primera captura:
  atalaya/data/archivo/verificaciones/AAAA-MM-DD.jsonl.gz
Salida viva: atalaya/data/verificaciones.json  (piezas de los últimos 60 días y recuento por partido y por verificador)
Una pieza que nombra a un partido no significa que lo desmienta: puede verificar algo que dijo un rival, un medio o una cuenta anónima.
Uso (raíz del repo): python3 scripts/atalaya/build_verificaciones.py
"""
import gzip, hashlib, json, re, subprocess, sys, unicodedata
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from html import unescape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import archivo                      # noqa: E402
from manifest import marcar         # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
D = RAIZ / "atalaya/data"
SALIDA = D / "verificaciones.json"
CARP = D / "archivo" / "verificaciones"
UA = "Mozilla/5.0 (compatible; EmirodgarBot/1.0; +https://emirodgar.es/atalaya)"
DIAS = 60
FEEDS = [("Maldita", "https://maldita.es/malditobulo/feed/"), ("Newtral", "https://newtral.es/zona-verificacion/feed/"),
         ("EFE Verifica", "https://verifica.efe.com/feed/"), ("Verificat", "https://www.verificat.cat/feed/")]
# Mismos criterios que build_news.py (nombre del partido y de sus portavoces más conocidos), más el Frente Amplio
PARTIDOS = {"PP": r"\bPP\b|Partido Popular|Feijóo|Mañueco|Ayuso", "PSOE": r"\bPSOE\b|socialist|Sánchez|Gobierno de España",
            "Vox": r"\bVox\b|Abascal", "Sumar": r"\bSumar\b|Yolanda Díaz", "Podemos": r"Podemos|Irene Montero",
            "Frente Amplio": r"Frente Amplio|Colau", "ERC": r"\bERC\b|Esquerra Republicana|Rufián|Junqueras",
            "Junts": r"\bJunts\b|Puigdemont|Nogueras", "PNV": r"\bPNV\b|\bEAJ\b|Nacionalista Vasco", "EH Bildu": r"Bildu|Otegi",
            "BNG": r"\bBNG\b|Bloque Nacionalista", "UPN": r"\bUPN\b|Unión del Pueblo Navarro"}
ELECTORAL = re.compile(r"elecciones|electoral|candidat|\bvoto\b|votar|urnas|campaña|debate|encuesta|\bCIS\b|Congreso|Senado|Junta Electoral|29-?N", re.I)


def get(url):
    r = subprocess.run(["curl", "-s", "-L", "-m", "40", "-A", UA, url], capture_output=True)
    if not r.stdout: raise RuntimeError("sin respuesta")
    return r.stdout


def piezas(medio, xml):
    for it in ET.fromstring(xml).iter("item"):
        t = unescape((it.findtext("title") or "").strip()); u = (it.findtext("link") or "").strip()
        if not t or not u: continue
        try: dt = parsedate_to_datetime(it.findtext("pubDate")).astimezone(timezone.utc)
        except Exception: continue
        cats = [unescape((c.text or "").strip()) for c in it.findall("category") if (c.text or "").strip()][:6]
        desc = re.sub(r"<[^>]+>", " ", unescape(it.findtext("description") or ""))
        yield {"i": hashlib.sha1(u.encode("utf8")).hexdigest()[:12], "t": t, "u": u, "f": dt.isoformat(), "m": medio, "c": cats, "txt": re.sub(r"\s+", " ", desc)[:400]}


def etiquetar(p):
    base = p["t"] + " " + p["txt"]
    ps = [k for k, rx in PARTIDOS.items() if re.search(rx, p["t"], re.I)] or [k for k, rx in PARTIDOS.items() if re.search(rx, base, re.I) and k not in ("PSOE",)]
    return ps, bool(ELECTORAL.search(base))


def main():
    arch = {}
    if CARP.exists():
        for f in sorted(CARP.glob("*.jsonl.gz")):
            for r in archivo.leer_lineas(f): arch[r["i"]] = r
    nuevas, vistas = [], 0
    for medio, url in FEEDS:
        try: lista = list(piezas(medio, get(url)))
        except Exception as e: print("FALLO", medio, repr(e)[:100]); continue
        vistas += len(lista)
        for p in lista:
            ps, elec = etiquetar(p)
            if not ps and not elec: continue                       # solo política y elecciones
            if p["i"] in arch: continue
            fila = {"i": p["i"], "t": p["t"], "u": p["u"], "f": p["f"], "m": p["m"], "c": p["c"], "p": ps, "e": elec, "cap": datetime.now(timezone.utc).strftime("%Y-%m-%d")}
            nuevas.append(fila); arch[fila["i"]] = fila
        print(f"{medio}: {len(lista)} piezas en el feed")
    if nuevas: archivo.anadir_al_dia(CARP, nuevas)
    corte = (datetime.now(timezone.utc) - timedelta(days=DIAS)).isoformat()
    vivas = sorted((r for r in arch.values() if r["f"] >= corte), key=lambda r: r["f"], reverse=True)
    por_partido = Counter(p for r in vivas for p in r["p"]); por_medio = Counter(r["m"] for r in vivas)
    SALIDA.write_text(json.dumps({"actualizado": datetime.now(timezone.utc).replace(microsecond=0).isoformat(), "dias": DIAS,
        "aviso": "Piezas de Maldita, Newtral, EFE Verifica y Verificat que nombran a un partido o candidato o hablan de elecciones. Que una pieza nombre a un partido no significa que lo desmienta: puede verificar algo que dijo un rival, un medio o una cuenta anónima.",
        "por_partido": dict(por_partido.most_common()), "por_medio": dict(por_medio.most_common()),
        "piezas": [{k: r[k] for k in ("t", "u", "f", "m", "c", "p", "e")} for r in vivas]}, ensure_ascii=False, separators=(",", ":")), encoding="utf8")
    marcar("verificaciones")
    print(len(nuevas), "nuevas;", len(vivas), "en los últimos", DIAS, "días;", len(arch), "archivadas")


if __name__ == "__main__":
    main()
