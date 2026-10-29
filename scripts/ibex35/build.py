#!/usr/bin/env python3
"""Genera ibex35/data.json con el cierre diario del IBEX 35 y el cribado de
oportunidades (caída larga y profunda + primeras señales de giro).

Sin IA: precios de Yahoo Finance (yfinance) e indicadores calculados aquí.
Solo escribe si hay una sesión nueva respecto al data.json actual (o FORZAR=1).
Salidas para GitHub Actions (GITHUB_OUTPUT): ficheros, periodo.
"""
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd
import yfinance as yf

RAIZ = Path(__file__).resolve().parents[2]
DESTINO = RAIZ / "ibex35" / "data.json"
HISTORICO = RAIZ / "ibex35" / "historico.json"

# Composición del IBEX 35 (revisar cuando el comité de BME la cambie, en junio
# y diciembre). Si un ticker deja de devolver datos se avisa y se sigue sin él.
EMPRESAS = [
    ("ACS.MC", "ACS", "Construcción"),
    ("ACX.MC", "Acerinox", "Materiales"),
    ("AENA.MC", "Aena", "Infraestructuras"),
    ("AMS.MC", "Amadeus", "Tecnología"),
    ("ANA.MC", "Acciona", "Construcción"),
    ("ANE.MC", "Acciona Energía", "Energía"),
    ("BBVA.MC", "BBVA", "Banca"),
    ("BKT.MC", "Bankinter", "Banca"),
    ("CABK.MC", "CaixaBank", "Banca"),
    ("CLNX.MC", "Cellnex", "Telecomunicaciones"),
    ("COL.MC", "Colonial", "Inmobiliario"),
    ("ELE.MC", "Endesa", "Energía"),
    ("ENG.MC", "Enagás", "Energía"),
    ("FDR.MC", "Fluidra", "Industria"),
    ("FER.MC", "Ferrovial", "Infraestructuras"),
    ("GRF.MC", "Grifols", "Salud"),
    ("IAG.MC", "IAG", "Transporte"),
    ("IBE.MC", "Iberdrola", "Energía"),
    ("IDR.MC", "Indra", "Tecnología"),
    ("ITX.MC", "Inditex", "Consumo"),
    ("LOG.MC", "Logista", "Consumo"),
    ("MAP.MC", "Mapfre", "Seguros"),
    ("MRL.MC", "Merlin Properties", "Inmobiliario"),
    ("MTS.MC", "ArcelorMittal", "Materiales"),
    ("NTGY.MC", "Naturgy", "Energía"),
    ("PUIG.MC", "Puig", "Consumo"),
    ("RED.MC", "Redeia", "Energía"),
    ("REP.MC", "Repsol", "Energía"),
    ("ROVI.MC", "Rovi", "Salud"),
    ("SAB.MC", "Banco Sabadell", "Banca"),
    ("SAN.MC", "Banco Santander", "Banca"),
    ("SCYR.MC", "Sacyr", "Construcción"),
    ("SLR.MC", "Solaria", "Energía"),
    ("TEF.MC", "Telefónica", "Telecomunicaciones"),
    ("UNI.MC", "Unicaja", "Banca"),
]
INDICE = "^IBEX"

# Umbrales del cribado: aquí se ajusta el criterio sin tocar el resto.
CFG = {
    "caidaMinima": -25.0,        # % desde el máximo de 52 semanas
    "sesionesCaida": 125,        # el máximo debe ser de hace >= ~6 meses
    "minRecienteMin": 15,        # el mínimo no puede ser más reciente (sigue cayendo)
    "minRecienteMax": 90,        # ni más antiguo (el giro ya sería tardío)
    "reboteMinimo": 8.0,         # % de rebote desde el mínimo
    "rsiGiro": 45.0,             # RSI actual por encima de esto...
    "rsiSobreventa": 35.0,       # ...habiendo estado por debajo de esto en 60 sesiones
    "puntosOportunidad": 4,      # de 5 señales de giro
}
MADRID = ZoneInfo("Europe/Madrid")
SESIONES_GRAFICO = 252
PUNTOS_GRAFICO = 63


def descargar(tickers):
    """Cierres diarios ajustados de 2 años. Reintenta y devuelve DataFrame."""
    ultimo = None
    for intento in range(3):
        try:
            df = yf.download(tickers, period="2y", interval="1d", auto_adjust=True,
                             progress=False, group_by="column", threads=False)
            cierres = df["Close"].dropna(how="all")
            if not cierres.empty:
                return cierres
        except Exception as e:  # noqa: BLE001 - red/Yahoo: se reintenta
            ultimo = e
        time.sleep(5 * (intento + 1))
    raise SystemExit(f"No se pudieron descargar los precios: {ultimo}")


def rsi(serie, n=14):
    d = serie.diff()
    ganancia = d.clip(lower=0).ewm(alpha=1 / n, adjust=False).mean()
    perdida = (-d.clip(upper=0)).ewm(alpha=1 / n, adjust=False).mean()
    rs = ganancia / perdida.replace(0, float("nan"))
    return 100 - 100 / (1 + rs)


def variacion(serie, sesiones):
    if len(serie) <= sesiones:
        return None
    return round((serie.iloc[-1] / serie.iloc[-1 - sesiones] - 1) * 100, 2)


def analizar(serie):
    """Indicadores y estado de una serie de cierres (sin NaN)."""
    s = serie.dropna()
    if len(s) < 220:
        return None
    precio = float(s.iloc[-1])
    anio = s.iloc[-SESIONES_GRAFICO:]
    maximo = float(anio.max())
    sesiones_desde_max = len(anio) - 1 - int(anio.values.argmax())
    caida = (precio / maximo - 1) * 100

    sma20, sma50, sma200 = (s.rolling(n).mean() for n in (20, 50, 200))
    r = rsi(s)

    # Mínimo de las últimas 120 sesiones (el suelo candidato).
    ventana = s.iloc[-120:]
    minimo = float(ventana.min())
    sesiones_desde_min = len(ventana) - 1 - int(ventana.values.argmin())
    rebote = (precio / minimo - 1) * 100

    ytd_base = s[s.index.year < s.index[-1].year]
    ytd = round((precio / float(ytd_base.iloc[-1]) - 1) * 100, 2) if len(ytd_base) else None

    base = {
        "caida": caida <= CFG["caidaMinima"],
        "duracion": sesiones_desde_max >= CFG["sesionesCaida"],
        "bajoSma200": precio < float(sma200.iloc[-1]),
        "sma50BajoSma200": float(sma50.iloc[-1]) < float(sma200.iloc[-1]),
    }
    en_caida = all(base.values())

    senales = {
        "minimoReciente": CFG["minRecienteMin"] <= sesiones_desde_min <= CFG["minRecienteMax"],
        "rebote": rebote >= CFG["reboteMinimo"],
        "sobreSma20": precio > float(sma20.iloc[-1])
        and float(sma50.iloc[-1]) / float(sma50.iloc[-11]) - 1 >= -0.005,
        "rsi": float(r.iloc[-1]) >= CFG["rsiGiro"]
        and float(r.iloc[-60:].min()) <= CFG["rsiSobreventa"],
        "minimosCrecientes": float(s.iloc[-15:].min()) >= minimo * 1.02,
    }
    puntos = sum(senales.values())

    if en_caida and senales["minimoReciente"] and puntos >= CFG["puntosOportunidad"]:
        estado = "oportunidad"
    elif en_caida:
        estado = "vigilancia"
    else:
        estado = "normal"

    paso = max(1, len(anio) // PUNTOS_GRAFICO)
    spark = [round(float(v), 2) for v in anio.iloc[::-1].iloc[::paso].iloc[::-1]]
    if spark[-1] != round(precio, 2):
        spark.append(round(precio, 2))

    return {
        "precio": round(precio, 3),
        "d1": variacion(s, 1),
        "m1": variacion(s, 21),
        "m6": variacion(s, 126),
        "ytd": ytd,
        "a1": variacion(s, 252),
        "caida": round(caida, 1),
        "rebote": round(rebote, 1),
        "sesionesMin": sesiones_desde_min,
        "sesionesMax": sesiones_desde_max,
        "rsi": round(float(r.iloc[-1]), 1),
        "sma50": round(float(sma50.iloc[-1]), 3),
        "sma200": round(float(sma200.iloc[-1]), 3),
        "base": base,
        "senales": senales,
        "puntos": puntos,
        "estado": estado,
        "spark": spark,
    }


def main():
    cierres = descargar([t for t, _, _ in EMPRESAS] + [INDICE])

    # Una sesión sin cerrar (antes de las 17:45 de Madrid) no cuenta.
    ahora = datetime.now(MADRID)
    if cierres.index[-1].date() == ahora.date() and (ahora.hour, ahora.minute) < (17, 45):
        cierres = cierres.iloc[:-1]
    fecha = cierres.index[-1].date().isoformat()

    previo = json.loads(DESTINO.read_text(encoding="utf-8")) if DESTINO.exists() else {}
    if previo.get("fechaDatos") == fecha and not os.environ.get("FORZAR"):
        print(f"Ya existe la sesión {fecha}; nada que hacer.")
        return

    empresas, sin_datos = [], []
    for ticker, nombre, sector in EMPRESAS:
        if ticker not in cierres or cierres[ticker].dropna().empty:
            sin_datos.append(ticker)
            continue
        a = analizar(cierres[ticker])
        if a is None:
            sin_datos.append(ticker)
            continue
        empresas.append({"ticker": ticker.replace(".MC", ""), "nombre": nombre, "sector": sector, **a})

    if len(empresas) < 25:
        raise SystemExit(f"Solo {len(empresas)} empresas con datos (faltan {sin_datos}); no se publica.")
    if sin_datos:
        print("Sin datos:", ", ".join(sin_datos), file=sys.stderr)

    indice = analizar(cierres[INDICE]) if INDICE in cierres else None
    orden = {"oportunidad": 0, "vigilancia": 1, "normal": 2}
    empresas.sort(key=lambda e: (orden[e["estado"]], -e["puntos"], e["caida"]))

    meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
             "septiembre", "octubre", "noviembre", "diciembre"]
    d = datetime.fromisoformat(fecha)
    salida = {
        "fechaDatos": fecha,
        "lastUpdated": f"{d.day} de {meses[d.month - 1]}, {d.year}",
        "generado": ahora.isoformat(timespec="minutes"),
        "criterios": CFG,
        "indice": indice and {k: indice[k] for k in ("precio", "d1", "m1", "m6", "ytd", "a1", "caida", "spark")},
        "resumen": {k: sum(e["estado"] == k for e in empresas) for k in orden},
        "sinDatos": sin_datos,
        "empresas": empresas,
    }
    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    DESTINO.write_text(json.dumps(salida, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    hist = json.loads(HISTORICO.read_text(encoding="utf-8")) if HISTORICO.exists() else {}
    hist[fecha] = {k: [e["ticker"] for e in empresas if e["estado"] == k] for k in ("oportunidad", "vigilancia")}
    HISTORICO.write_text(json.dumps(dict(sorted(hist.items())), ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"{fecha}: {salida['resumen']}")
    salida_gh = os.environ.get("GITHUB_OUTPUT")
    if salida_gh:
        with open(salida_gh, "a", encoding="utf-8") as f:
            f.write("ficheros=ibex35/data.json ibex35/historico.json\n")
            f.write(f"periodo={fecha}\n")


if __name__ == "__main__":
    main()
