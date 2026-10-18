#!/usr/bin/env python3
"""
AUDITOR DE CRONS — "¿estan sanos los crons del lab?" (SOLO LECTURA).

Carencia que resuelve (medida el 12-oct-2026, no supuesta):
  El lab ya tiene dos instrumentos de cron, y los dos tienen el MISMO punto
  ciego: `watchdog-informes-cron.py` (cron diario 12:00, skill hermes-cron-jobs)
  y `barrido-informes-fallidos.py` detectan fallo SOLO por la cabecera '(FAILED)'
  o la cola '## Error'. El formato de fallo ACTUAL de Hermes es otro:
  `**Status:** script failed`. Medido en esta sesion: el informe
  `~/.hermes/cron/output/da39a2148b34/2026-10-12_08-05-44.md` lleva
  `**Status:** script failed` + 'Script timed out after 300s' y el watchdog
  respondio `Status: silent (empty output)` ese mismo dia; el barrido solo
  encontro 9 fallos, todos de ago/sep, ninguno de octubre. Resultado: dos jobs
  llevan fallando en serie (uno de ellos 11 corridas seguidas desde el 30-sep)
  y NADIE lo avisa.
  Tercera capa, sin monitorizar por nadie: las ENTREGAS. `deliveries.db` tiene
  37 filas 'failed' (4 del propio 12-oct, 'Telegram send failed: Timed out'):
  el cron corre, produce y su salida no llega al usuario. Ni el watchdog ni
  `hermes cron doctor` miran esa tabla.

Que hace (no escribe, no dispara jobs, no toca servicios ni config):
  1. jobs.json -> failure_streak, last_status, last_error, next_run_at vencido
     (job 'atascado'), jobs habilitados que nunca han corrido.
  2. output/<job_id>/*.md -> fallo por criterio AMPLIADO (las 3 senales:
     '(FAILED)', '## Error', '**Status:** script failed'/'script timed out'),
     filtrando por fecha de modificacion dentro de la ventana.
  3. deliveries.db -> entregas 'failed' dentro de la ventana (la capa que nadie
     mira), con el error real de cada una.

Umbrales por flag, nunca a priori (RULE-015): la ventana y el retraso tolerado
se pasan por argumento.

Uso:
  python3 tools/auditar_crons.py                    # informe legible (48 h)
  python3 tools/auditar_crons.py --horas 168        # ventana de 7 dias
  python3 tools/auditar_crons.py --json             # JSON para crons
  python3 tools/auditar_crons.py --retraso-min 60   # tolerancia de 'atascado'
  AUDITOR_CRONS_DIR=/tmp/prueba python3 tools/auditar_crons.py   # pruebas

Codigo de salida: 0 = sin hallazgos; 1 = hay hallazgos (para encadenarlo a un
cron: stdout vacio o exit 0 = silencio).
"""

from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Senales de fallo en el informe de una corrida. La tercera es la que faltaba
# en los instrumentos previos (formato actual de Hermes).
SENALES_FALLO = (
    "(FAILED)",
    "## Error",
    "Status:** script failed",
    "Status: script failed",
    "script timed out",
)
CABECERA = 400
COLA = 900
ESTADOS_OK = {"ok", "success", "delivered", None, ""}


def _ahora() -> datetime:
    return datetime.now(timezone.utc)


def _parsear_iso(texto) -> datetime | None:
    """ISO con o sin offset -> datetime aware (UTC si no trae offset)."""
    if not texto or not isinstance(texto, str):
        return None
    try:
        d = datetime.fromisoformat(texto)
    except ValueError:
        return None
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)


def _cargar_jobs(ruta: Path) -> list:
    """jobs.json -> lista de jobs (tolera dict con 'jobs' o lista pelada)."""
    try:
        datos = json.loads(Path(ruta).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    if isinstance(datos, dict):
        return list(datos.get("jobs") or [])
    return list(datos or [])


def _nombre(job: dict) -> str:
    return str(job.get("name") or job.get("id") or "?")


def _evaluar_job(job: dict, ahora: datetime, retraso_min: int) -> list:
    """Hallazgos de ESTADO de un job (streak, ultimo fallo, atascado, nunca)."""
    h = []
    jid, nom = str(job.get("id") or "?"), _nombre(job)
    streak = job.get("failure_streak") or 0
    if streak > 0:
        h.append({"tipo": "estado", "job": nom, "id": jid,
                  "detalle": "fallo_repetido: %s corrida(s) seguidas con error"
                             % streak,
                  "cuando": job.get("last_run_at")})
    estado = job.get("last_status")
    if estado not in ESTADOS_OK:
        h.append({"tipo": "estado", "job": nom, "id": jid,
                  "detalle": "ultimo_estado=%s · %s" % (
                      estado, str(job.get("last_error") or "sin last_error")[:160]),
                  "cuando": job.get("last_run_at")})
    if job.get("last_delivery_error"):
        h.append({"tipo": "entrega", "job": nom, "id": jid,
                  "detalle": "last_delivery_error: %s"
                             % str(job.get("last_delivery_error"))[:160],
                  "cuando": job.get("last_run_at")})
    if job.get("enabled"):
        vencido = _vencido(job, ahora, retraso_min)
        if vencido is not None:
            h.append({"tipo": "estado", "job": nom, "id": jid,
                      "detalle": "atascado: next_run_at %s lleva %.1f h sin "
                                 "dispararse (ultima corrida: %s)"
                                 % (job.get("next_run_at"),
                                    vencido / 3600.0,
                                    job.get("last_run_at") or "nunca"),
                      "cuando": job.get("next_run_at")})
    return h


def _vencido(job: dict, ahora: datetime, retraso_min: int) -> float | None:
    """Segundos de retraso de next_run_at si supera la tolerancia; si no, None."""
    pendiente = _parsear_iso(job.get("next_run_at"))
    if pendiente is None:
        return None
    retraso = (ahora - pendiente).total_seconds()
    return retraso if retraso > retraso_min * 60 else None


def _fallo_de_informe(ruta: Path, desde: datetime) -> str | None:
    """Motivo del fallo si el informe lo registra y es de la ventana; si no, None."""
    try:
        if datetime.fromtimestamp(Path(ruta).stat().st_mtime,
                                  tz=timezone.utc) < desde:
            return None
        texto = Path(ruta).read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        return "ilegible: %s" % e
    cabecera, cola = texto[:CABECERA], texto[-COLA:]
    for senal in SENALES_FALLO:
        if senal in cabecera or senal in cola:
            return senal
    return None


def _fallos_de_informes(out_dir: Path, desde: datetime, idx: dict) -> list:
    """Barre output/<job_id>/*.md y AGRUPA los fallos de la ventana por job+senal."""
    if not Path(out_dir).is_dir():
        return []
    filas = []
    for job_dir in sorted(p for p in Path(out_dir).iterdir() if p.is_dir()):
        for f in sorted(job_dir.glob("*.md")):
            motivo = _fallo_de_informe(f, desde)
            if motivo:
                filas.append((job_dir.name, idx.get(job_dir.name, "(fuera de jobs.json)"),
                              f.name, motivo))
    return _agrupar_informes(filas)


def _agrupar_informes(filas: list) -> list:
    """filas (id, job, fichero, senal) -> un hallazgo por job+senal (sin ruido)."""
    grupos = {}
    for jid, nom, fichero, senal in filas:
        g = grupos.setdefault((jid, nom, senal), [])
        g.append(fichero)
    hallazgos = []
    for (jid, nom, senal), fichs in sorted(grupos.items()):
        detalle = "%d corrida(s) fallida(s) en la ventana (%s -> %s), senal '%s'" % (
            len(fichs), fichs[0], fichs[-1], senal)
        hallazgos.append({"tipo": "informe", "job": nom, "id": jid,
                          "detalle": detalle, "cuando": fichs[-1]})
    return hallazgos


def _entregas_fallidas(ruta_db: Path, desde: datetime) -> tuple:
    """(hallazgos, total_ventana, total_fallidas_historicas) de deliveries.db."""
    ruta = Path(ruta_db)
    if not ruta.exists():
        return [], 0, 0
    try:
        con = sqlite3.connect("file:%s?mode=ro" % ruta, uri=True)
    except sqlite3.Error as e:
        return [{"tipo": "entrega", "job": "(deliveries.db)", "id": "?",
                 "detalle": "no legible: %s" % e, "cuando": None}], 0, 0
    try:
        en_ventana, fallidas_hist = _contar_entregas(con, desde)
    finally:
        con.close()
    if not en_ventana:
        return [], len(en_ventana), fallidas_hist
    ejemplos = [(f[0][:19].replace("T", " "), str(f[1])[:110]) for f in en_ventana[-5:]]
    cab = "%d entrega(s) fallida(s) en la ventana (historico: %d):" % (
        len(en_ventana), fallidas_hist)
    detalle = "\n".join([cab] + ["      - %s -> %s" % (c, e) for c, e in ejemplos])
    return [{"tipo": "entrega", "job": "(todas las entregas)", "id": "-",
             "detalle": detalle, "cuando": ejemplos[-1][0] if ejemplos else None}], \
        len(en_ventana), fallidas_hist


def _contar_entregas(con: sqlite3.Connection, desde: datetime) -> tuple:
    """Filas (created_at, error) fallidas en la ventana + historico total."""
    fallidas, hist = [], 0
    for creado, estado, error in con.execute(
            "select created_at, status, error from deliveries"):
        if estado == "delivered":
            continue
        hist += 1
        fecha = _parsear_iso(creado)
        if fecha and fecha >= desde:
            fallidas.append((creado, error or estado))
    return fallidas, hist


def _recolectar(base: Path, horas: int, retraso_min: int, ahora: datetime) -> dict:
    """Todos los hallazgos de las 3 capas + metadatos del informe."""
    desde = ahora - timedelta(hours=horas)
    jobs = _cargar_jobs(base / "jobs.json")
    idx = {str(j.get("id")): _nombre(j) for j in jobs}
    hallazgos = []
    for job in jobs:
        hallazgos += _evaluar_job(job, ahora, retraso_min)
    hallazgos += _fallos_de_informes(base / "output", desde, idx)
    h_ent, ent_ventana, ent_hist = _entregas_fallidas(base / "deliveries.db", desde)
    hallazgos += h_ent
    return {"ahora": ahora, "horas": horas, "retraso_min": retraso_min, "base": base,
            "desde": desde, "jobs_total": len(jobs), "hallazgos": hallazgos,
            "entregas_ventana": ent_ventana, "entregas_hist": ent_hist}


def _formatear(datos: dict) -> str:
    """Informe legible: cabecera, conteo por tipo y detalle de cada hallazgo."""
    cab = ("=== AUDITOR DE CRONS — %s ===\n"
           "Fuentes: %s/{jobs.json, output/, deliveries.db}\n"
           "Ventana: %s  ·  retraso tolerado: %s min  ·  jobs: %s\n"
           % (datos["ahora"].strftime("%Y-%m-%d %H:%M:%S %Z"),
              datos["base"], datos["desde"].strftime("%Y-%m-%d %H:%M"), 
              datos["retraso_min"], datos["jobs_total"]))
    if not datos["hallazgos"]:
        return (cab + "\n✅ Sin hallazgos: ningun job en fallo repetido, ningun informe "
                     "fallido en la ventana y ninguna entrega fallida.\n")
    lineas = [cab, "🔴 %d hallazgo(s) en %d capa(s):\n"
              % (len(datos["hallazgos"]),
                 len({h["tipo"] for h in datos["hallazgos"]}))]
    for h in datos["hallazgos"]:
        lineas.append("[%s] %s (%s)\n    %s\n    cuando: %s"
                      % (h["tipo"], h["job"], h["id"], h["detalle"],
                         h.get("cuando") or "-"))
    lineas.append("Salida: exit 1 = hay hallazgos, exit 0 = silencio.")
    return "\n".join(lineas) + "\n"


def _json(datos: dict) -> str:
    """Resumen estructurado (nunca el dict completo: pitfall 16)."""
    por_tipo = {}
    for h in datos["hallazgos"]:
        por_tipo[h["tipo"]] = por_tipo.get(h["tipo"], 0) + 1
    return json.dumps({
        "fecha": datos["ahora"].isoformat(),
        "base": str(datos["base"]),
        "ventana_horas": datos["horas"],
        "retraso_min": datos["retraso_min"],
        "jobs_total": datos["jobs_total"],
        "hallazgos_total": len(datos["hallazgos"]),
        "por_tipo": por_tipo,
        "entregas_fallidas_ventana": datos["entregas_ventana"],
        "entregas_fallidas_historico": datos["entregas_hist"],
        "ok": not datos["hallazgos"],
        "hallazgos": datos["hallazgos"],
    }, ensure_ascii=False, indent=2)


def _base_por_defecto() -> Path:
    return Path(os.environ.get("AUDITOR_CRONS_DIR",
                               str(Path.home() / ".hermes" / "cron")))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Auditor de salud de los crons (solo lectura).")
    ap.add_argument("--horas", type=int, default=48,
                    help="ventana para informes y entregas (por defecto 48)")
    ap.add_argument("--retraso-min", type=int, default=15,
                    help="minutos de retraso de next_run_at tolerados (por defecto 15)")
    ap.add_argument("--json", action="store_true", help="salida JSON")
    ap.add_argument("--base", default=None, help="directorio de cron (pruebas)")
    args = ap.parse_args(argv)
    datos = _recolectar(Path(args.base) if args.base else _base_por_defecto(),
                        args.horas, args.retraso_min, _ahora())
    print(_json(datos) if args.json else _formatear(datos))
    return 1 if datos["hallazgos"] else 0


if __name__ == "__main__":
    sys.exit(main())
