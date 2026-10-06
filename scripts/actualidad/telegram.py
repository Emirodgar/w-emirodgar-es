#!/usr/bin/env python3
"""Envía por Telegram el resumen de un día de la hemeroteca.

Uso: TELEGRAM_BOT_TOKEN=... TELEGRAM_CHAT_ID=... python3 scripts/actualidad/telegram.py AAAA-MM-DD

Si faltan las variables, sale sin error (el envío es opcional). Solo usa la
librería estándar de Python.
"""

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from html import escape
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
LIMITE = 4000  # Telegram admite 4096 caracteres por mensaje


def main():
    token, chat = os.environ.get("TELEGRAM_BOT_TOKEN"), os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat:
        print("Sin TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID: no se envía nada.")
        return
    fecha = sys.argv[1]
    dia = json.loads((RAIZ / "actualidad" / "datos" / "dias" / f"{fecha}.json").read_text(encoding="utf-8"))

    pie = f'\n\n<a href="https://emirodgar.es/actualidad/">Leer el resumen completo</a>'
    cabecera = f"<b>{escape(dia['titular'])}</b>\n\n"
    cuerpo = escape(dia["resumen"])
    espacio = LIMITE - len(cabecera) - len(pie)
    if len(cuerpo) > espacio:
        cuerpo = cuerpo[:espacio].rsplit(" ", 1)[0] + "…"

    datos = urllib.parse.urlencode({
        "chat_id": chat, "text": cabecera + cuerpo + pie,
        "parse_mode": "HTML", "disable_web_page_preview": "true",
    }).encode()
    try:
        urllib.request.urlopen(f"https://api.telegram.org/bot{token}/sendMessage", datos, timeout=30)
        print("Resumen enviado por Telegram.")
    except urllib.error.HTTPError as e:
        # No se imprime la URL (lleva el token); solo el motivo que da Telegram.
        sys.exit(f"Telegram rechazó el mensaje: HTTP {e.code} {e.read().decode('utf-8', 'replace')[:300]}")


if __name__ == "__main__":
    main()
