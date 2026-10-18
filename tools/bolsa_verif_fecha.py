#!/usr/bin/env python3
"""Verificacion SOLO LECTURA: fecha del ultimo punto de la serie diaria Nasdaq.
Objetivo: resolver la anomalia pendiente (4a vez anotada) - saber si el snapshot
de las 22:30 CEST corresponde al cierre de HOY o al del dia anterior.
"""
import json
import urllib.request
from datetime import datetime, timedelta

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
HEADERS = {
    "User-Agent": UA,
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://www.nasdaq.com",
    "Referer": "https://www.nasdaq.com/",
}

today = datetime.now()
fromdate = (today - timedelta(days=40)).strftime("%Y-%m-%d")
todate = today.strftime("%Y-%m-%d")

for t in ["FSLY", "MRVL", "WDC", "NVDA"]:
    url = (f"https://api.nasdaq.com/api/quote/{t}/historical?assetclass=stocks"
           f"&fromdate={fromdate}&todate={todate}&limit=9999")
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read().decode("utf-8"))
    rows = ((data.get("data") or {}).get("tradesTable") or {}).get("rows") or []
    pts = [(row.get("date"), row.get("close")) for row in rows[:6]]
    print(f"--- {t}: ultimos puntos publicados ---")
    for d, c in pts:
        print(f"    {d}  {c}")
print(f"\nHora local del chequeo: {today.isoformat(timespec='seconds')}")
