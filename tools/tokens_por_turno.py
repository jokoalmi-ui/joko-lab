#!/usr/bin/env python3
"""Contador de tokens por turno para sesiones de Hermes (SOLO LECTURA).

Origen del dato: ~/.hermes/state.db (WAL). Se abre con mode=ro; este script
no escribe, no bloquea y no toca el scheduler.

Que mide, y que no:
  - Mide caracteres reales de los mensajes guardados (user, assistant, tool)
    y los convierte a tokens con un ratio declarado (default 4.0 chars/token).
    NO es un tokenizer: es una estimacion, y se contrasta al final con el
    consumo real que registro la API en sessions/session_model_usage.
  - El coste de los esquemas de tools NO esta en la BD (viaja aparte en la
    peticion a la API). Se pasa como constante medida con --schemas-tokens.
    Medida 2026-10-24 en este host con model_tools.get_tool_definitions():
    32 esquemas inline = 49.834 B compactos ~= 12.500 tokens.
  - cache_read_tokens es lo que la API releyo de cache: es el coste dominante
    y no equivale a contexto nuevo.

Uso:
  tokens_por_turno.py                 # ultima sesion
  tokens_por_turno.py <session_id>
  tokens_por_turno.py <session_id> --schemas-tokens 12500 --ratio 4.0
"""
from __future__ import annotations

import argparse
import pathlib
import sqlite3
import sys

DB = pathlib.Path.home() / ".hermes" / "state.db"


def connect_ro(path: pathlib.Path) -> sqlite3.Connection:
    uri = f"file:{path}?mode=ro"
    con = sqlite3.connect(uri, uri=True, timeout=5.0)
    con.row_factory = sqlite3.Row
    return con


def pick_session(con: sqlite3.Connection, want: str | None) -> sqlite3.Row:
    if want and want not in ("last", ""):
        row = con.execute(
            "SELECT * FROM sessions WHERE id = ?", (want,)
        ).fetchone()
        if row is None:
            raise SystemExit(f"sesion no encontrada: {want}")
        return row
    row = con.execute(
        "SELECT * FROM sessions ORDER BY started_at DESC LIMIT 1"
    ).fetchone()
    if row is None:
        raise SystemExit("no hay sesiones en la BD")
    return row


def rows_msgs(con: sqlite3.Connection, sid: str, since: float | None):
    where = "session_id = ? AND COALESCE(active, 1) = 1"
    args: list = [sid]
    if since is not None:
        where += " AND timestamp >= ?"
        args.append(since)
    cur = con.execute(
        f"""
        SELECT id, role, tool_name, timestamp,
               COALESCE(length(content), 0) AS n_content,
               COALESCE(length(reasoning), 0) AS n_reasoning,
               CASE WHEN tool_calls IS NULL OR tool_calls = '' THEN 0 ELSE 1 END AS has_calls
        FROM messages
        WHERE {where}
        ORDER BY timestamp, id
        """,
        args,
    )
    return cur.fetchall()


def heredado(con: sqlite3.Connection, sid: str, since: float) -> tuple[int, int]:
    row = con.execute(
        "SELECT COUNT(*), COALESCE(SUM(COALESCE(length(content),0)),0) FROM messages "
        "WHERE session_id = ? AND COALESCE(active,1) = 1 AND timestamp < ?",
        (sid, since),
    ).fetchone()
    return int(row[0] or 0), int(row[1] or 0)


def anchor(ses: sqlite3.Row) -> dict:
    import json
    try:
        cfg = json.loads(ses["model_config"] or "{}")
    except Exception:
        return {}
    a = cfg.get("_usage_anchor") or {}
    return a if isinstance(a, dict) else {}



def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("session", nargs="?", default="last")
    ap.add_argument("--db", default=str(DB))
    ap.add_argument("--schemas-tokens", type=float, default=12500.0)
    ap.add_argument("--ratio", type=float, default=4.0)
    ap.add_argument("--top", type=int, default=8, help="cuantos turnos listar")
    ap.add_argument("--all-msgs", action="store_true",
                    help="incluir mensajes anteriores a started_at (tail heredado)")
    a = ap.parse_args()

    path = pathlib.Path(a.db)
    if not path.exists():
        raise SystemExit(f"no existe la BD: {path}")
    con = connect_ro(path)
    ses = pick_session(con, a.session)
    sid = ses["id"]
    since = None if a.all_msgs else float(ses["started_at"] or 0)
    msgs = rows_msgs(con, sid, since)
    anc = anchor(ses)

    # Agrupar por turno: cada mensaje 'user' abre turno.
    turnos: list[dict] = []
    for m in msgs:
        if m["role"] == "user" or not turnos:
            turnos.append({
                "hora": m["timestamp"], "user": 0, "asst": 0, "tool": 0,
                "reason": 0, "calls": 0, "ntools": 0, "tools": {},
            })
        t = turnos[-1]
        if m["role"] == "user":
            t["user"] += m["n_content"]
        elif m["role"] == "assistant":
            t["asst"] += m["n_content"]
            t["reason"] += m["n_reasoning"]
            if m["has_calls"]:
                t["calls"] += 1
        elif m["role"] == "tool":
            t["tool"] += m["n_content"]
            t["ntools"] += 1
            name = m["tool_name"] or "?"
            t["tools"][name] = t["tools"].get(name, 0) + m["n_content"]

    r = a.ratio
    n_asst = sum(t["calls"] for t in turnos)
    calls_real = int(ses["api_call_count"] or 0)
    factor = (calls_real / n_asst) if n_asst else 1.0
    print(f"sesion    : {sid}  ({ses['source']}, {ses['model']})")
    print(f"BD        : {path}  (mode=ro)")
    print(f"ratio     : {r} chars/token (estimacion declarada)")
    print(f"esquemas  : {a.schemas_tokens:.0f} tok/llamada (constante medida, no BD)")
    print(f"turnos    : {len(turnos)} | assistant msgs: {n_asst} | api_call_count: {calls_real}"
          f" | factor: {factor:.2f}")
    if anc:
        print(f"anchor    : prompt_tokens={anc.get('prompt_tokens')} "
              f"completion={anc.get('completion_tokens')} base_msgs={anc.get('base_count')}"
              "  (medido por la API, no estimado)")
    if not a.all_msgs:
        h_n, h_c = heredado(con, sid, float(ses["started_at"] or 0))
        print(f"heredado  : {h_n} msgs / {h_c} chars ({h_c/r:.0f} tok) previos a started_at"
              " (fuera del recuento por turno)")
    if abs(factor - 1.0) > 0.2:
        print("AVISO     : el numero de assistant msgs no casa con api_call_count;"
              " los esquemas se reparten escalados (cota, no medida)")
    print()


    tot = {"user": 0, "asst": 0, "reason": 0, "tool": 0, "calls": 0, "ntools": 0}
    print(f"{'#':>2} {'hora':>8} {'api':>3} {'user':>7} {'asst':>7} {'reason':>7} "
          f"{'tools':>8} {'n':>3} {'esq':>8} {'total':>8} {'tool%':>6}")
    for i, t in enumerate(turnos, 1):
        for k in tot:
            tot[k] += t[k]
        esq = t["calls"] * factor * a.schemas_tokens
        total = esq + (t["user"] + t["asst"] + t["reason"] + t["tool"]) / r
        trool = (t["tool"] / r) / total * 100 if total else 0
        import datetime as _dt
        hora = _dt.datetime.fromtimestamp(t["hora"]).strftime("%H:%M:%S")
        print(f"{i:>2} {hora:>8} {t['calls']:>3} {t['user']/r:>7.0f} "
              f"{t['asst']/r:>7.0f} {t['reason']/r:>7.0f} {t['tool']/r:>8.0f} "
              f"{t['ntools']:>3} {esq:>8.0f} {total:>8.0f} {trool:>5.1f}%")

    esq_tot = calls_real * a.schemas_tokens
    msg_tok = (tot["user"] + tot["asst"] + tot["reason"] + tot["tool"]) / r
    print()
    print(f"llamadas API (assistant con/sin tool_calls): {tot['calls']}")
    print(f"tool results: {tot['ntools']}  ({tot['tool']/r:.0f} tok est.)")
    print(f"estimado de tokens de ENTRADA acumulados (prefijos repetidos): {msg_tok + esq_tot:.0f} tok")
    print(f"  de eso, esquemas: {esq_tot:.0f} tok ({esq_tot/(msg_tok+esq_tot)*100 if msg_tok+esq_tot else 0:.1f}%)")
    print(f"  de eso, tool results: {tot['tool']/r:.0f} tok ({tot['tool']/r/(msg_tok+esq_tot)*100 if msg_tok+esq_tot else 0:.1f}%)")
    print("  (ojo: no es el tamano del contexto, es la suma de lo que se reenvia en cada llamada)")

    # Top tools por volumen de salida
    agg: dict[str, int] = {}
    for t in turnos:
        for k, v in t["tools"].items():
            agg[k] = agg.get(k, 0) + v
    top = sorted(agg.items(), key=lambda kv: -kv[1])[:8]
    if top:
        print("\ntop tools por bytes devueltos:")
        for k, v in top:
            print(f"  {k:<22} {v:>9} B  ~{v/r:>7.0f} tok")

    # Contraste con el consumo real registrado por la API
    print("\n=== consumo REAL registrado (sessions) ===")
    real_in = ses["input_tokens"] or 0
    real_out = ses["output_tokens"] or 0
    cache = ses["cache_read_tokens"] or 0
    cw = ses["cache_write_tokens"] or 0
    calls = ses["api_call_count"] or 0
    print(f"api_call_count : {calls}")
    print(f"input_tokens   : {real_in}")
    print(f"output_tokens  : {real_out}")
    print(f"cache_read     : {cache}")
    print(f"cache_write    : {cw}")
    print(f"coste estimado : {ses['estimated_cost_usd'] or 0:.4f} USD")
    print(f"coste real     : {ses['actual_cost_usd'] or 0:.4f} USD  (status={ses['cost_status']})")
    if calls:
        print(f"\npor llamada: cache_read {cache/calls:.0f} tok  input {real_in/calls:.0f} tok  output {real_out/calls:.0f} tok")
        print(f"contexto medio por llamada ~ {cache/calls + real_in/calls:.0f} tok")
        if msg_tok + esq_tot:
            print(f"nuestra estimacion del contexto escrito / llamada ~ {(msg_tok+esq_tot)/calls:.0f} tok")
    con.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
