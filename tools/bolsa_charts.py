#!/usr/bin/env python3
"""
bolsa_charts.py — Genera charts de cierre diario con datos REALES de Nasdaq
para analizar patrones como Dani (ascendente / descendente / banda lateral /
L-swing). Sin pipes; salida PNG en experiments/bolsa/graficas/.

Uso: python3 bolsa_charts.py            # toda la cartera
     python3 bolsa_charts.py WDC,MRVL   # solo esos tickers
Creado: 06-ago-2026 (juego de bolsa autónomo, EXP-002).
"""

import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bolsa_scan import TICKERS, fetch_historical  # noqa: E402

try:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
except ImportError:
    sys.exit("matplotlib NO instalado — necesario para generar los charts")

OUT = os.path.expanduser("~/joko-lab/lpa/experiments/bolsa/graficas")


def main():
    os.makedirs(OUT, exist_ok=True)
    hoy = datetime.date.today()
    desde = hoy - datetime.timedelta(days=200)
    tickers = sys.argv[1].split(",") if len(sys.argv) > 1 else TICKERS

    for t in tickers:
        try:
            series = fetch_historical(t, desde.isoformat(), hoy.isoformat())
        except Exception as e:  # noqa: BLE001
            print(f"{t}: ERROR {type(e).__name__}: {e}")
            continue
        if len(series) < 30:
            print(f"{t}: serie insuficiente ({len(series)} puntos)")
            continue

        fechas = [datetime.datetime.strptime(p["date"], "%m/%d/%Y") for p in series]
        cierres = [p["close"] for p in series]
        ult = cierres[-1]
        high = max(cierres)
        low = min(cierres)

        fig, ax = plt.subplots(figsize=(10, 5), dpi=110)
        ax.plot(fechas, cierres, color="#2b6cb0", lw=1.8)
        ax.fill_between(fechas, cierres, low * 0.96, color="#2b6cb0", alpha=0.08)
        ax.set_title(f"{t} — cierre diario (Nasdaq, datos reales 06-ago-2026)", fontsize=12)
        ax.set_ylabel("USD")
        ax.grid(alpha=0.3)
        ax.axhline(ult, color="#c0563c", lw=0.8, ls="--")
        ax.annotate(
            f"ultimo {ult:.2f} USD",
            xy=(fechas[-1], ult),
            xytext=(-110, 14),
            textcoords="offset points",
            fontsize=9,
            color="#c0563c",
        )
        ax.annotate(
            f"max {high:.2f} / min {low:.2f}",
            xy=(fechas[0], high),
            xytext=(8, -16),
            textcoords="offset points",
            fontsize=8,
            color="#475569",
        )
        fig.tight_layout()
        path = os.path.join(OUT, f"{t}.png")
        fig.savefig(path)
        plt.close(fig)
        print(f"{t}: {len(series)} puntos -> {path} (ultimo {ult:.2f}, max {high:.2f}, min {low:.2f})")


if __name__ == "__main__":
    main()
