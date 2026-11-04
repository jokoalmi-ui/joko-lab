#!/usr/bin/env python3
"""reconsolidar_rango.py — regenera ficheros delta de sesiones desde state.db.

Motivo (03-nov-2026): el consolidador no genero NINGUN fichero de sesiones entre
el 2026-10-01 y el 2026-10-15 (ni delta, ni .zst), mientras state.db conserva
771 sesiones de ese rango. Este script las extrae y escribe un
`sesiones-delta-YYYYMMDD.jsonl` por dia en un directorio de recuperacion
SEPARADO, para no contaminar el archivo del consolidador.

Solo lectura sobre state.db (mode=ro). No toca el acumulado ni los .zst.

Uso:
  python3 reconsolidar_rango.py --desde 2026-10-01 --hasta 2026-10-15
  (destino por defecto: <metrics>/sesiones/recovery-<AAAAMMDD de hoy>/)
"""
import argparse
import json
import os
import sqlite3
import sys
from collections import defaultdict
from datetime import datetime
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Europe/Madrid")
STATE = os.path.expanduser("~/.hermes/state.db")
BASE = "/home/jokoalmi/joko-lab/04-operations/metrics/sesiones"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--desde", required=True)
    ap.add_argument("--hasta", required=True)
    ap.add_argument("--destino", default=None)
    ap.add_argument("--todos-los-mensajes", action="store_true",
                    help="guarda todos los roles (por defecto solo user: es lo unico que lee el registro HEL)")
    a = ap.parse_args()

    t0 = datetime.strptime(a.desde + " 00:00", "%Y-%m-%d %H:%M").replace(tzinfo=TZ).timestamp()
    t1 = datetime.strptime(a.hasta + " 23:59", "%Y-%m-%d %H:%M").replace(tzinfo=TZ).timestamp()
    dest = a.destino or os.path.join(BASE, "recovery-" + datetime.now(TZ).strftime("%Y%m%d"))
    os.makedirs(dest, exist_ok=True)

    con = sqlite3.connect(f"file:{STATE}?mode=ro", uri=True)
    cur = con.cursor()
    ses = cur.execute(
        "SELECT id, source, started_at FROM sessions "
        "WHERE started_at >= ? AND started_at < ? ORDER BY started_at", (t0, t1)
    ).fetchall()

    filtro_rol = "" if a.todos_los_mensajes else " AND role = 'user' "
    por_dia = defaultdict(list)
    total_msg = 0
    for sid, source, started in ses:
        msgs = cur.execute(
            "SELECT role, content, timestamp FROM messages "
            "WHERE session_id = ?" + filtro_rol + "ORDER BY timestamp", (sid,)
        ).fetchall()
        dia = datetime.fromtimestamp(started, TZ).strftime("%Y%m%d")
        por_dia[dia].append({
            "id": sid,
            "source": source,
            "started_at": started,
            "messages": [{"role": r, "content": c, "timestamp": t} for r, c, t in msgs],
        })
        total_msg += len(msgs)
    con.close()

    total_escritas = 0
    for dia in sorted(por_dia):
        path = os.path.join(dest, f"sesiones-delta-{dia}.jsonl")
        with open(path, "w", encoding="utf-8") as f:
            for s in por_dia[dia]:
                f.write(json.dumps(s, ensure_ascii=False) + "\n")
        total_escritas += len(por_dia[dia])
        print(f"  {dia}: {len(por_dia[dia])} sesiones, {os.path.getsize(path)/1024:.0f} KB")
    print(f"\nTOTAL: {total_escritas} sesiones, {total_msg} mensajes en {len(por_dia)} dias")
    print(f"DESTINO: {dest}")
    if total_escritas == 0:
        print("AVISO: 0 sesiones en el rango; revisar fechas o state.db", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
