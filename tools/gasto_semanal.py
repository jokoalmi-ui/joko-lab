#!/usr/bin/python3
"""Resumen semanal de gasto por sesion (solo lectura).

Lee ~/.hermes/state.db con mode=ro: no escribe, no bloquea, no toca el scheduler.
Los costes son los que Hermes ya calculo (estimated_cost_usd); este script NO
recalcula precios: agrega y ordena lo registrado.

Uso:  gasto_semanal.py [--days 7] [--top 5]
Salida: texto plano para entregar por Telegram (cron no_agent).
"""
from __future__ import annotations

import argparse
import datetime as dt
import pathlib
import sqlite3
import sys

DB = pathlib.Path.home() / ".hermes" / "state.db"


def connect_ro(path: pathlib.Path) -> sqlite3.Connection:
    if not path.exists():
        print(f"gasto_semanal: no existe la BD {path}")
        sys.exit(0)
    con = sqlite3.connect(f"file:{path}?mode=ro", uri=True, timeout=5)
    con.row_factory = sqlite3.Row
    return con


def fmt(n: float) -> str:
    return f"{n:,.0f}".replace(",", ".")


def eur(n: float, d: int = 4) -> str:
    return f"{n:.{d}f}".replace(".", ",")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--top", type=int, default=5)
    a = ap.parse_args()

    con = connect_ro(DB)
    since = dt.datetime.now().timestamp() - a.days * 86400

    tot = con.execute(
        """
        SELECT COUNT(*) n,
               COALESCE(SUM(estimated_cost_usd), 0) coste,
               COALESCE(SUM(api_call_count), 0) calls,
               COALESCE(SUM(input_tokens), 0) inp,
               COALESCE(SUM(output_tokens), 0) outp,
               COALESCE(SUM(cache_read_tokens), 0) cache,
               COALESCE(SUM(reasoning_tokens), 0) reas,
               SUM(CASE WHEN COALESCE(estimated_cost_usd, 0) = 0 THEN 1 ELSE 0 END) sin_coste
        FROM sessions WHERE started_at >= ?
        """,
        (since,),
    ).fetchone()

    if not tot["n"]:
        print(f"Gasto {a.days} d: sin sesiones registradas.")
        return 0

    print(f"Gasto Hermes · ultimos {a.days} dias")
    print(f"Sesiones: {tot['n']} | llamadas API: {fmt(tot['calls'])}"
          f" ({tot['calls'] / tot['n']:.1f} por sesion)")
    print(f"Coste estimado: {eur(tot['coste'])} $"
          f" | por sesion {eur(tot['coste'] / tot['n'])} $"
          f" | por llamada {eur(tot['coste'] / tot['calls'] if tot['calls'] else 0, 5)} $")
    print(f"Tokens: entrada {fmt(tot['inp'])} · salida {fmt(tot['outp'])}"
          f" · cache_read {fmt(tot['cache'])}"
          f" ({tot['cache'] / (tot['inp'] + tot['cache']) * 100 if (tot['inp'] + tot['cache']) else 0:.0f}% del input)")
    if tot["reas"]:
        print(f"Razonamiento: {fmt(tot['reas'])} tok")
    if tot["sin_coste"]:
        print(f"Aviso: {tot['sin_coste']} sesion(es) sin coste calculado (cost_status distinto de 'estimated')")

    rows = con.execute(
        """
        SELECT id, source, model, started_at, api_call_count, message_count,
               COALESCE(estimated_cost_usd, 0) coste, input_tokens, cache_read_tokens
        FROM sessions WHERE started_at >= ?
        ORDER BY coste DESC LIMIT ?
        """,
        (since, a.top),
    ).fetchall()

    print()
    print(f"Top {len(rows)} sesiones por coste:")
    for r in rows:
        when = dt.datetime.fromtimestamp(r["started_at"]).strftime("%d-%b %H:%M")
        model = (r["model"] or "?").replace("deepseek-", "")
        print(f"· {when} {r['source']}/{model} · {eur(r['coste'])} $"
              f" · {r['api_call_count']} llamadas · {fmt(r['input_tokens'])} in"
              f" · {fmt(r['cache_read_tokens'])} cache")

    by_src = con.execute(
        """
        SELECT source, COUNT(*) n, COALESCE(SUM(estimated_cost_usd), 0) coste
        FROM sessions WHERE started_at >= ?
        GROUP BY source ORDER BY coste DESC
        """,
        (since,),
    ).fetchall()
    if len(by_src) > 1:
        print()
        print("Por origen:")
        for r in by_src:
            print(f"· {r['source']}: {r['n']} sesiones · {eur(r['coste'])} $"
                  f" ({r['coste'] / tot['coste'] * 100 if tot['coste'] else 0:.0f}%)")

    print()
    print("(solo lectura de state.db; coste = estimated_cost_usd de Hermes, no recalculado)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
