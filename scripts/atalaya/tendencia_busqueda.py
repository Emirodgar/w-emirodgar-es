"""Atalaya: bloque "Interés de búsqueda" (stat tile + sparkline de 12 meses), compartido entre
ficha_politico_autonomico.py y ficha_discurso_votos.py. Datos en atalaya/data/tendencias_busqueda.json
(volumen mensual y tendencia relativa, vía Semrush, base de datos España).
"""
from datetime import datetime
from html import escape as E

MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]


def fecha_es(iso):
    d = datetime.fromisoformat(iso[:10])
    return f"{d.day} de {MESES[d.month - 1]} de {d.year}"


CSS_TENDENCIA = """.tend{border:1px solid #e3e8ef;border-radius:8px;padding:14px 16px;margin:1em 0}
.tend b{font-size:20px}
.spark-line{stroke:#94a3b8;fill:none;stroke-width:2;stroke-linejoin:round;stroke-linecap:round}
.spark-ring{fill:#fff}.spark-dot{fill:#1d4ed8}
@media (prefers-color-scheme:dark){.tend{border-color:#273449}.spark-line{stroke:#475569}.spark-ring{fill:#0e1219}.spark-dot{fill:#7cb0ff}}"""


def nes(n):
    return f"{n:,}".replace(",", ".")


def spark_svg(trend, w=132, h=36):
    n = len(trend)
    xs = [2 + i * (w - 4) / (n - 1) for i in range(n)]
    ys = [h - 4 - v * (h - 10) for v in trend]
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))
    return (f"<svg viewBox='0 0 {w} {h}' width='{w}' height='{h}' aria-hidden='true'>"
            f"<polyline class='spark-line' points='{pts}'/>"
            f"<circle class='spark-ring' cx='{xs[-1]:.1f}' cy='{ys[-1]:.1f}' r='6'/>"
            f"<circle class='spark-dot' cx='{xs[-1]:.1f}' cy='{ys[-1]:.1f}' r='4'/>"
            "</svg>")


def bloque_tendencia(slug, data):
    """data: el dict completo cargado de tendencias_busqueda.json. Devuelve '' si no hay dato para ese slug."""
    p = data.get("personas", {}).get(slug)
    if not p:
        return ""
    svg = spark_svg(p["trend"])
    return (f"<h2>Interés de búsqueda</h2><div class='tend'>"
            f"<p><b>{nes(p['volumen'])}</b> búsquedas al mes en Google España por «{E(p['keyword'])}», "
            f"con esta tendencia en los últimos 12 meses:</p>{svg}"
            f"<p class='meta'>{E(data['aviso'])} Fuente: {E(data['fuente'])}, {fecha_es(data['actualizado'])}.</p>"
            "</div>")
