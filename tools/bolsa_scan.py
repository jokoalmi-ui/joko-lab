#!/usr/bin/env python3
"""
bolsa_scan.py — Escáner diario de patrones para el juego de bolsa autónomo
(Experimento 002, protocolo DECODE — método de Daniel Sánchez-Crespo).

Fuente: API pública de Nasdaq (sin API key; requiere headers de navegador).
Uso:
    python3 bolsa_scan.py            # escaneo normal, guarda snapshot
    python3 bolsa_scan.py --debug    # imprime la estructura cruda de un ticker
    python3 bolsa_scan.py --tickers NVDA,MRVL   # solo esos tickers

Salida: snapshot JSON en experiments/bolsa/snapshots/YYYY-MM-DD.json + tabla legible.
Fuentes (dos): /historical (serie diaria, publica la barra del dia con lag) y
/quote/{ticker}/info (cierre OFICIAL del dia, fix 18-sep-2026: lo que manda
para decidir). Regla: si la fuente falla, se registra el error — NUNCA se
inventan datos.
Creado: 06-ago-2026 (juego autónomo v2, autorizado por Joseba).
"""

import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timedelta

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
BASE = "https://api.nasdaq.com/api/quote/{ticker}/historical"
BASE_QUOTE = "https://api.nasdaq.com/api/quote/{ticker}/info?assetclass=stocks"
HEADERS = {
    "User-Agent": UA,
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://www.nasdaq.com",
    "Referer": "https://www.nasdaq.com/",
}

# Cartera vigilada (del curso DECODE + ejemplos de swing de Dani)
TICKERS = [
    "NVDA", "V", "GOOGL", "MSFT", "AAPL", "CCL", "WDC",      # clásicas "aburridas"
    "MRVL", "REGN", "PLTR", "FSLY", "MCHP", "UAA",            # ejemplos swing
    "NKE", "VSCO",                                             # evitar (contraejemplos)
]
EVITAR = {"NKE", "VSCO", "MSFT"}  # Dani: evitar para swing (contexto/negocio)

OUT_DIR = os.path.expanduser("~/joko-lab/lpa/experiments/bolsa/snapshots")


def fetch_historical(ticker, fromdate, todate):
    """Devuelve lista de dicts {date, close} o lanza excepción."""
    url = f"{BASE.format(ticker=ticker)}?assetclass=stocks&fromdate={fromdate}&todate={todate}&limit=9999"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read().decode("utf-8"))
    rows = ((data.get("data") or {}).get("tradesTable") or {}).get("rows") or []
    out = []
    for row in rows:
        fecha = row.get("date")
        close = row.get("close")
        if fecha and close:
            close = close.replace(",", "").replace("$", "").strip()
            try:
                out.append({"date": fecha, "close": float(close)})
            except ValueError:
                continue
    # La API devuelve la serie INVERTIDA (más reciente primero): darle la vuelta
    # para que el último elemento sea el cierre más actual (fix 06-ago-2026).
    out.reverse()
    return out


def fetch_live_quote(ticker):
    """Cierre OFICIAL del dia via /quote/{ticker}/info (fix 18-sep-2026).

    La serie historica publica la barra del dia con retraso (lag confirmado
    8 veces: 04, 08, 09, 14, 15, 16, 17 y 18-sep-2026), por lo que a las
    22:30 CEST el snapshot registra el cierre de AYER. Este endpoint, en
    cambio, ya devuelve el cierre oficial del dia en cuanto el mercado
    cierra (secondaryData: "Closed at ... 4:00 PM ET").
    Se usa SOLO secondaryData (cierre oficial) para no confundir el ultimo
    precio intradia con el cierre. Devuelve {"close", "date", "ts"} o None.
    """
    url = BASE_QUOTE.format(ticker=ticker)
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read().decode("utf-8"))
    sec = ((data.get("data") or {}).get("secondaryData")) or {}
    raw_price = sec.get("lastSalePrice")
    stamp = sec.get("lastTradeTimestamp") or ""
    if not raw_price or "Closed at" not in stamp:
        return None
    try:
        close = float(str(raw_price).replace(",", "").replace("$", "").strip())
    except ValueError:
        return None
    m = re.search(r"([A-Z][a-z]{2} \d{1,2}, \d{4})", stamp)
    fecha = None
    if m:
        try:
            fecha = datetime.strptime(m.group(1), "%b %d, %Y").strftime("%m/%d/%Y")
        except ValueError:
            fecha = None
    return {"close": close, "date": fecha or stamp, "ts": stamp}


def _recalcular_con_cierre(m, precio):
    """Recalcula DD%/REC%/patron con el cierre OFICIAL del dia (fix 18-sep-2026).

    La serie historica trae la barra del dia con retraso, asi que las metricas
    de decision deben usar el cierre oficial (/quote/info) cuando exista.
    """
    high, low = m["high_3m"], m["low_30d"]
    dd = (precio - high) / high * 100 if high else 0.0
    rec = (precio - low) / low * 100 if low else 0.0
    if dd <= -15.0 and rec >= 8.0:
        patron = "L-swing"
    elif dd <= -15.0:
        patron = "descendente"
    elif rec >= 8.0:
        patron = "ascendente"
    else:
        patron = "lateral"
    return round(dd, 2), round(rec, 2), patron


def rec_rango_pct(precio, high, low):
    """Recorrido recuperado sobre el RANGO: (precio - valle) / (maximo - valle) * 100.

    Es la unidad del metodo ("entrar a mitad de subida" = 50% del recorrido de
    vuelta al maximo). NO es lo mismo que recovery_pct, que va sobre el valle:
    para WDC el 28-oct-2026, 50% de rango = 440,28 USD y 50% sobre valle = 498,00
    USD. Confundirlas convertia el umbral del 50% en una condicion mucho mas dura.
    """
    if not high or not low or high <= low:
        return None
    return round((precio - low) / (high - low) * 100, 2)


def compute_metrics(series):
    """Métricas del método de Dani sobre serie diaria de cierre."""
    if len(series) < 30:
        return None
    closes = [p["close"] for p in series]
    last = closes[-1]
    win = min(len(closes), 63)          # ~3 meses de trading
    high_3m = max(closes[-win:])
    low_30d = min(closes[-20:])         # mínimo reciente
    drawdown = (last - high_3m) / high_3m * 100
    recovery = (last - low_30d) / low_30d * 100 if low_30d else 0.0
    # Detección de patrón (heurística del curso, configurable):
    #   L (swing): cayó >=15% desde máx 3m y remonta >=8% desde mínimo 20d
    es_L = drawdown <= -15.0 and recovery >= 8.0
    if not es_L:
        if drawdown <= -15.0:
            patron = "descendente"
        elif recovery >= 8.0:
            patron = "ascendente"
        else:
            patron = "lateral"
    else:
        patron = "L-swing"
    return {
        "last": last,
        "last_date": series[-1]["date"],   # fecha del ultimo punto (fix 15-sep-2026:
                                          # la API publica con retraso el dia en curso)
        "high_3m": high_3m,
        "low_30d": low_30d,
        "drawdown_pct": round(drawdown, 2),
        "recovery_pct": round(recovery, 2),
        "recovery_rango_pct": rec_rango_pct(last, high_3m, low_30d),
        "patron": patron,
    }


def _parsear_args() -> tuple[bool, list | None]:
    """Parsea argumentos CLI: flag --debug y lista --tickers."""
    debug = "--debug" in sys.argv
    only = None
    if "--tickers" in sys.argv:
        i = sys.argv.index("--tickers")
        only = [t.upper() for t in sys.argv[i + 1].split(",")]
    return debug, only


def _escaneo_tickers(tickers, fromdate, todate, debug) -> tuple[dict, dict]:
    """Escanea cada ticker: métricas o error. Devuelve (resultados, errores)."""
    resultados = {}
    errores = {}

    for ticker in tickers:
        try:
            series = fetch_historical(ticker, fromdate, todate)
            if debug:
                print(f"[DEBUG {ticker}] filas={len(series)} primera={series[0] if series else None} ultima={series[-1] if series else None}")
            m = compute_metrics(series)
            if m is None:
                errores[ticker] = "serie insuficiente"
                continue
            m["ticker"] = ticker
            m["evitar"] = ticker in EVITAR
            # Cierre oficial del dia (complementa el lag de la serie historica)
            try:
                q = fetch_live_quote(ticker)
                if q:
                    m["live_close"] = q["close"]
                    m["live_date"] = q["date"]
                    m["recovery_rango_live_pct"] = rec_rango_pct(q["close"], m["high_3m"], m["low_30d"])
                    if q["close"] != m["last"]:
                        dd, rec, pat = _recalcular_con_cierre(m, q["close"])
                        m["drawdown_live_pct"] = dd
                        m["recovery_live_pct"] = rec
                        m["patron_live"] = pat
            except Exception as e:  # noqa: BLE001 — no debe tumbar el escaneo
                m["live_error"] = f"{type(e).__name__}: {e}"
            resultados[ticker] = m
        except Exception as e:  # noqa: BLE001 — el escáner nunca debe morir por un ticker
            errores[ticker] = f"{type(e).__name__}: {e}"
    return resultados, errores


def _guardar_snapshot(resultados, errores, today) -> str:
    """Persiste el snapshot JSON; devuelve la ruta del archivo escrito."""
    # Snapshot persistente
    os.makedirs(OUT_DIR, exist_ok=True)
    snapshot = {
        "fecha": today.isoformat(timespec="seconds"),
        "fuente": "nasdaq.com/api (sin key)",
        "resultados": resultados,
        "errores": errores,
    }
    path = os.path.join(OUT_DIR, f"{today.strftime('%Y-%m-%d')}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, ensure_ascii=False, indent=2)
    return path


def _formatear_tabla(resultados, errores) -> list[str]:
    """Devuelve la tabla legible para el agente/cron como lista de líneas."""
    # Tabla legible para el agente/cron
    path = os.path.join(OUT_DIR, f"{datetime.now().strftime('%Y-%m-%d')}.json")
    lines = [f"SNAPSHOT: {path}  ({datetime.now().strftime('%H:%M:%S')})"]
    fechas = sorted({m["last_date"] for m in resultados.values() if m.get("last_date")})
    if fechas:
        lines.append("CIERRE REGISTRADO = ultimo punto publicado por Nasdaq: " + ", ".join(fechas))
    live = [(t, m) for t, m in resultados.items() if m.get("live_close")]
    if live:
        partes = [f"{t} {m['live_close']:.2f} ({m.get('live_date', '?')})" for t, m in live]
        lines.append("CIERRE OFICIAL DEL DIA (quote/info, mismo dia): " + "; ".join(partes))
    faltan = [t for t, m in resultados.items() if not m.get("live_close")]
    if faltan:
        lines.append("SIN CIERRE EN VIVO (revisar): " + ", ".join(faltan))
    vivos = [(t, m) for t, m in resultados.items() if m.get("patron_live")]
    if vivos:
        partes = [
            f"{t} {m['live_close']:.2f} -> DD {m['drawdown_live_pct']:.2f}% REC {m['recovery_live_pct']:.2f}% (RANGO {m.get('recovery_rango_live_pct')}%) {m['patron_live']}"
            for t, m in vivos
        ]
        lines.append("METRICAS CON EL CIERRE DEL DIA (sustituyen a la serie, que va con lag): " + "; ".join(partes))
    lines.append(f"{'TICKER':7} {'CIERRE':>10} {'MAX3M':>10} {'DD%':>7} {'REC%':>7}  PATRON")
    for t, m in resultados.items():
        flag = " [EVITAR]" if m["evitar"] else ""
        lines.append(f"{t:7} {m['last']:>10.2f} {m['high_3m']:>10.2f} {m['drawdown_pct']:>7.2f} {m['recovery_pct']:>7.2f}  {m['patron']}{flag}")
    if errores:
        lines.append("ERRORES:")
        for t, e in errores.items():
            lines.append(f"  {t}: {e}")
    # Candidatas L para el cron (patron con el cierre oficial del dia si existe)
    cands = [
        t + ("*" if m.get("patron_live") else "")
        for t, m in resultados.items()
        if (m.get("patron_live") or m["patron"]) == "L-swing"
    ]
    lines.append("CANDIDATAS_L: " + (", ".join(cands) if cands else "(ninguna)"))
    rl = [
        f"{t} {m.get('recovery_rango_live_pct', m.get('recovery_rango_pct'))}%"
        for t, m in resultados.items()
        if (m.get("patron_live") or m["patron"]) == "L-swing"
    ]
    if rl:
        lines.append("REC_RANGO_L (0%=valle, 100%=max 3m; umbral de entrada >=35%): " + "; ".join(rl))
    if any(m.get("patron_live") for m in resultados.values()):
        lines.append("* patron calculado con el CIERRE OFICIAL DEL DIA (quote/info), no con la serie con lag")
    return lines


def main():
    debug, only = _parsear_args()

    today = datetime.now()
    todate = today.strftime("%Y-%m-%d")
    fromdate = (today - timedelta(days=200)).strftime("%Y-%m-%d")

    tickers = only if only else TICKERS
    resultados, errores = _escaneo_tickers(tickers, fromdate, todate, debug)

    path = _guardar_snapshot(resultados, errores, today)

    for line in _formatear_tabla(resultados, errores):
        print(line)


if __name__ == "__main__":
    main()
