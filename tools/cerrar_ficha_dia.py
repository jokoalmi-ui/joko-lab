#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cerrar_ficha_dia.py — INSTRUMENTO de cierre diario de la ficha (punto 1
del paquete de evaluacion de resultados, 2026-10-13).

Que hace (y que NO hace):
  - Cierra la marca de valoracion PENDIENTE de la fila de uso_diario del dia
    ([VAL: sin respuesta aun | ventana H-H] -> [VAL: <veredicto> | ventana H-H])
    y AÑADE al final de nota_personal la linea de cierre. Nunca reescribe ni
    borra el texto ya escrito (regla edicion-aditiva-registros §3).
  - Apunta una linea al ledger JSONL para poder agregar despues.
  - NO inventa valores: si no hay fila para la fecha, sale con error y no
    escribe nada.

Uso:
  /usr/bin/python3 cerrar_ficha_dia.py --llevada si --veredicto justo \
      --nota "texto libre" [--fecha 2026-10-13] [--ventana 10-20] [--dry-run]
"""
import argparse
import json
import re
import shutil
import sqlite3
import sys
from datetime import date, datetime
from pathlib import Path

DB = Path("/home/jokoalmi/perfume-ia/data/coleccion.db")
LEDGER = Path("/home/jokoalmi/joko-lab/04-operations/metrics/resultado_fichas.jsonl")
PEND = re.compile(r"\[VAL: sin respuesta aun(?:\s*\|\s*ventana ([^\]]+))?\]")


def cerrar(fecha: str, llevada: str, veredicto: str, nota: str, ventana: str,
           dry_run: bool) -> int:
    if not DB.exists():
        print(f"ERROR: no existe la BD {DB}", file=sys.stderr)
        return 2
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    try:
        fila = con.execute(
            "SELECT id, perfume_id, nota_personal FROM uso_diario "
            "WHERE fecha = ? ORDER BY id DESC LIMIT 1", (fecha,)).fetchone()
        if not fila:
            print(f"ERROR: no hay fila en uso_diario con fecha={fecha}. "
                  f"No se escribe nada (no se inventan datos).", file=sys.stderr)
            return 2
        uso_id, perfume_id, nota_actual = fila
        nota_actual = nota_actual or ""
        m = PEND.search(nota_actual)
        if m and not ventana:
            ventana = (m.group(1) or "").strip()

        if veredicto:
            marca = f"[VAL: {veredicto}" + (f" | ventana {ventana}" if ventana else "") + "]"
        elif llevada == "no":
            marca = "[VAL: no llevada" + (f" | ventana {ventana}" if ventana else "") + "]"
        else:
            marca = "[VAL: llevada, veredicto pendiente" + \
                    (f" | ventana {ventana}" if ventana else "") + "]"

        if m:
            nueva = PEND.sub(marca, nota_actual, count=1)
        else:
            nueva = f"{marca} {nota_actual}"
        cierre = f" · cierre {date.today().isoformat()}: llevada={llevada}"
        if veredicto:
            cierre += f" · veredicto={veredicto}"
        if nota:
            cierre += f" · {nota}"
        nueva = nueva.rstrip() + cierre

        print(f"uso_diario id={uso_id}  perfume_id={perfume_id}  fecha={fecha}")
        print(f"marca pendiente encontrada: {'SI' if m else 'NO (se antepone marca nueva)'}")
        print("--- nota_personal NUEVA (previa + cierre) ---")
        print(nueva)
        print("---------------------------------------------")

        if dry_run:
            print("[dry-run] no se escribe ni en la BD ni en el ledger.")
            return 0

        bak = DB.with_name(DB.name + f".BACKUP.{datetime.now():%Y%m%d}_cierre")
        if not bak.exists():
            shutil.copy2(DB, bak)
        con.close()
        con = sqlite3.connect(DB)
        cur = con.execute("UPDATE uso_diario SET nota_personal = ? WHERE id = ?",
                          (nueva, uso_id))
        if cur.rowcount != 1:
            print("ERROR: el UPDATE no afecto a 1 fila; se aborta sin tocar el ledger",
                  file=sys.stderr)
            return 3
        con.commit()
        verif = con.execute("SELECT nota_personal FROM uso_diario WHERE id = ?",
                            (uso_id,)).fetchone()[0]
        print(f"UPDATE ok (1 fila). Verificacion de lectura: {'COINCIDE' if verif == nueva else 'DIVERGE'}")
        print(f"backup: {bak if bak.exists() else '(ya existia)'}")
        con.close()
    finally:
        try:
            con.close()
        except Exception:
            pass

    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    linea = {
        "fecha_ficha": fecha,
        "uso_diario_id": uso_id,
        "perfume_id": perfume_id,
        "llevada": llevada,
        "veredicto": veredicto or None,
        "ventana": ventana or None,
        "nota": nota or None,
        "cerrado_ts": datetime.now().isoformat(timespec="seconds"),
    }
    with LEDGER.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(linea, ensure_ascii=False) + "\n")
    print(f"ledger += 1 linea -> {LEDGER}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fecha", default=date.today().isoformat())
    ap.add_argument("--llevada", required=True, choices=["si", "no"])
    ap.add_argument("--veredicto", default="", choices=["", "justo", "corto", "excesivo"])
    ap.add_argument("--nota", default="")
    ap.add_argument("--ventana", default="")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    return cerrar(a.fecha, a.llevada, a.veredicto, a.nota, a.ventana, a.dry_run)


if __name__ == "__main__":
    sys.exit(main())
