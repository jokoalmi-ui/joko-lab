#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""revision_produccion_semanal.py — INSTRUMENTO de revision semanal (punto 3
del paquete de evaluacion de resultados, 2026-10-13).

Responde SOLO con numeros medidos a 4 preguntas:
  1. ¿Cuantas fichas salieron esta semana? (carpetas con mtime < 7 dias)
  2. ¿Cuantas llevan valoracion real? (filas de uso_diario con [VAL: justo|corto|excesivo])
  3. ¿Cuantos PRED vencidos sin revisar? (subprocess -> escanear_predicciones.py)
  4. ¿Que instrumentos llevan >7 dias sin escribir? (mtime de metrics/, solo stat)

No lee el contenido de los JSONL grandes (solo os.stat): no repite el kill del
2026-10-12. No escribe nada. Exit 0 siempre (es un informe, no un gate).
"""
import os
import re
import sqlite3
import subprocess
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

BASE = Path("/home/jokoalmi/joko-lab")
FICHAS = BASE / "research/infografias"
METRICS = BASE / "04-operations/metrics"
DB = Path("/home/jokoalmi/perfume-ia/data/coleccion.db")
SCAN = BASE / "tools/escanear_predicciones.py"
OBJ = BASE / "01-knowledge/objects"
DIAS = 7


def pregunta1(hoy: date):
    dirs = [d for d in FICHAS.glob("perfume-del-dia-*") if d.is_dir()]
    corte = datetime.now() - timedelta(days=DIAS)
    esta = sorted(d.name for d in dirs if datetime.fromtimestamp(d.stat().st_mtime) >= corte)
    return len(dirs), esta


def pregunta2(hoy: date):
    desde = (hoy - timedelta(days=DIAS)).isoformat()
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    try:
        filas = con.execute(
            "SELECT fecha, COALESCE(nota_personal,'') FROM uso_diario "
            "WHERE fecha >= ? ORDER BY fecha", (desde,)).fetchall()
    finally:
        con.close()
    real = re.compile(r"\[VAL: (justo|corto|excesivo)")
    pend = re.compile(r"\[VAL: sin respuesta")
    con_val = [f for f, n in filas if real.search(n)]
    con_pend = [f for f, n in filas if pend.search(n)]
    sin_marca = [f for f, n in filas if "[VAL:" not in n]
    return filas, con_val, con_pend, sin_marca


def pregunta3():
    try:
        r = subprocess.run(["/usr/bin/python3", str(SCAN), "--dir", str(OBJ)],
                           capture_output=True, text=True, timeout=120)
        salida = (r.stdout or "") + (r.stderr or "")
        ids = re.findall(r"(PRED-\d+) \((joseba|hermes|conjunta)\) — vencía (\d{4}-\d{2}-\d{2})",
                         salida)
        return r.returncode, ids, salida
    except Exception as e:  # noqa: BLE001
        return None, [], f"ERROR lanzando el escaner: {e}"


def pregunta4():
    """Solo os.stat (nunca se lee el contenido de los JSONL grandes).

    Regla de validacion del instrumento (RULE-015): un fichero con fecha en el
    nombre dentro de sesiones/ es un ARCHIVO diario, no un instrumento: se
    ignora en el listado de parados y se informa aparte. Y solo se marca como
    'parado' lo que estaba VIVO: escribio dentro de los ultimos 60 dias y
    lleva >7 dias sin escribir. Lo que dejo de escribirse hace >60 dias se
    considera cerrado, no averiado.
    """
    vivo = datetime.now() - timedelta(days=60)
    parados, frescos, ultimo_archivo = [], [], None
    for root, dirs, files in os.walk(METRICS):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
        if root.count(os.sep) - str(METRICS).count(os.sep) > 1:
            dirs[:] = []
            continue
        for f in files:
            if not f.endswith((".jsonl", ".log")):
                continue
            p = Path(root) / f
            try:
                st = p.stat()
            except OSError:
                continue
            mtime = datetime.fromtimestamp(st.st_mtime)
            edad = (datetime.now() - mtime).days
            rel = str(p.relative_to(BASE))
            if "sesiones" in p.parts:
                if ultimo_archivo is None or mtime > ultimo_archivo[0]:
                    ultimo_archivo = (mtime, rel, edad)
                continue
            if edad > DIAS and mtime >= vivo:
                parados.append((edad, st.st_size, rel))
            frescos.append((edad, st.st_size, rel))
    parados.sort(reverse=True)
    frescos.sort(key=lambda x: x[0])
    return parados, frescos[:3], ultimo_archivo


def main() -> int:
    hoy = date.today()
    print(f"REVISIÓN SEMANAL DE PRODUCCIÓN — {hoy.isoformat()}")
    print(f"(instrumento: revision_produccion_semanal.py · ventana: {DIAS} días)\n")

    total, esta = pregunta1(hoy)
    print(f"1) FICHAS — salieron {len(esta)} esta semana (de {total} en total)")
    print(f"   {' · '.join(esta) if esta else 'ninguna carpeta nueva'}")

    filas, con_val, con_pend, sin_marca = pregunta2(hoy)
    print(f"\n2) VALORACIÓN — {len(filas)} usos registrados; {len(con_val)} con valoración REAL")
    print(f"   con valoración: {', '.join(con_val) if con_val else 'ninguna'}")
    print(f"   con marca pendiente ([VAL: sin respuesta): {len(con_pend)}"
          + (f" -> {', '.join(con_pend)}" if con_pend else ""))
    print(f"   sin marca [VAL: en absoluto: {len(sin_marca)}")

    code, ids, salida = pregunta3()
    print(f"\n3) PRED — vencidos sin revisar: {len(ids)} (escaner exit={code})")
    for pid, kien, f in ids:
        print(f"   {pid} ({kien}) — vencía {f}")
    if not ids:
        print("   ninguno")

    parados, frescos, ultimo_archivo = pregunta4()
    print(f"\n4) INSTRUMENTOS — {len(parados)} vivos que llevan >{DIAS} días sin escribir")
    for edad, size, rel in parados:
        print(f"   {edad:>3} d  {size/1024:8.1f} KB  {rel}")
    if not parados:
        print("   ninguno")
    print("   más frescos:")
    for edad, size, rel in frescos:
        print(f"   {edad:>3} d  {size/1024:8.1f} KB  {rel}")
    if ultimo_archivo:
        mtime, rel, edad = ultimo_archivo
        print(f"   (archivo diario de sesiones/: el último es {rel}, hace {edad} d — dato, no juicio)")

    print("\nRecordatorio: este informe NO fija umbrales. Si algo te chirría, se cambia el instrumento.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
