#!/usr/bin/env python3
"""
Consolidador de sesiones — Joko Lab (nivel 2 de cross-session awareness)
Ejecutado por cron diario (22:30). Solo lectura de sesiones, escritura mínima
en el registro de sesiones consolidadas del lab.

Qué hace:
1. Exporta las sesiones NUEVAS de Hermes al registro del lab (metrics/sesiones/)
2. Fusiona el delta en un único acumulado deduplicado (sin copia completa diaria)
3. Escribe un resumen por día en metrics/sesiones/resumen-dia-YYYY-MM-DD.md
4. NO modifica memoria ni backlog (eso lo hace Hermes al leer el resumen)

ARREGLO 16-10-2026 (medido): antes hacía `hermes sessions export <fichero>` COMPLETO
(2238 sesiones -> 36,8 s, MAXRSS 11,3 GB, 1173 MB escritos) y escribía una copia
completa nueva cada día (93 ficheros = 15 GB). En un PC de 30 GB eso reventaba por
presión de memoria y el kernel mataba el worker (OOM): 15 fallos seguidos del
1 al 15 de octubre, 22:30. Ahora exporta solo el delta (`--newer-than 3d`:
2,4 s, MAXRSS 526 MB, 47 MB) y mantiene UN acumulado deduplicado por id.
La exportación completa solo se hace una vez, si el acumulado no existe.
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

HOME = Path.home()
LAB = Path(os.environ.get("JOKO_LAB_DIR", HOME / "joko-lab"))
SESIONES_DIR = LAB / "04-operations" / "metrics" / "sesiones"
TMP_DELTA = Path(os.environ.get("JOKO_TMP_DELTA", "/tmp/sesiones-consolidador.jsonl"))
ACUMULADO = SESIONES_DIR / "sesiones-acumulado.jsonl"
DIAS_DELTA = os.environ.get("JOKO_DIAS_DELTA", "3")
ID_KEYS = ("id", "session_id", "sessionId", "sid", "uuid")


def run(cmd):
    """Ejecuta un comando y devuelve (exit_code, stdout, stderr)."""
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    return p.returncode, p.stdout, p.stderr


def _extraer_fecha(ts) -> str:
    """Extrae fecha YYYY-MM-DD de un timestamp (epoch numérico o ISO string)."""
    if isinstance(ts, (int, float)) and ts > 1_000_000_000:
        return datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
    if isinstance(ts, str) and ts:
        return ts[:10]
    return ""


def _id_de(d):
    """Identificador de sesión, probando las claves conocidas."""
    for k in ID_KEYS:
        v = d.get(k)
        if v:
            return str(v)
    return None


def _contar_sesiones(objetivo, ayer):
    """Cuenta sesiones por fecha. Acepta una ruta (Path/str) o un fichero ya
    abierto (io.StringIO en los tests): memoria constante en ambos casos."""
    if hasattr(objetivo, "read"):
        return _contar_fh(objetivo, ayer)
    with Path(objetivo).open(errors="ignore") as fh:
        return _contar_fh(fh, ayer)


def _contar_fh(fh, ayer):
    por_fecha = {}
    con_ayer = 0
    con_total = 0
    for line in fh:
        line = line.strip()
        if not line:
            continue
        con_total += 1
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue
        ts = d.get("timestamp") or d.get("started_at") or d.get("created_at") or ""
        fecha = _extraer_fecha(ts)
        if fecha:
            por_fecha[fecha] = por_fecha.get(fecha, 0) + 1
        if fecha == ayer.strftime("%Y-%m-%d"):
            con_ayer += 1
    return por_fecha, con_ayer, con_total


def _fusionar_delta(delta: Path, acumulado: Path) -> int:
    """Añade al acumulado las líneas del delta cuyo id no esté ya.

    Devuelve cuántas líneas NUEVAS se añadieron. Lee el acumulado para los ids
    (solo ids en memoria) y luego anexa; no reescribe el fichero entero.
    """
    ids = set()
    if acumulado.exists():
        with acumulado.open(errors="ignore") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    sid = _id_de(json.loads(line))
                except json.JSONDecodeError:
                    continue
                if sid:
                    ids.add(sid)
    nuevas = 0
    with delta.open(errors="ignore") as src, acumulado.open("a", encoding="utf-8") as dst:
        for line in src:
            line = line.rstrip("\n")
            if not line.strip():
                continue
            try:
                sid = _id_de(json.loads(line))
            except json.JSONDecodeError:
                continue
            if sid and sid in ids:
                continue
            if sid:
                ids.add(sid)
            dst.write(line + "\n")
            nuevas += 1
    return nuevas


def _construir_resumen(hoy, ayer, por_fecha, con_total, con_ayer, origen=None, nuevas=None):
    """Construye las líneas del resumen del día.

    `origen` y `nuevas` son opcionales para no romper la firma antigua que fijan
    los tests; en producción el consolidador los pasa siempre.
    """
    lineas = [
        f"# Resumen de sesiones — {ayer.strftime('%Y-%m-%d')}",
        "",
        f"Generado: {hoy.isoformat(timespec='minutes')} por consolidador (cron 22:30)",
        "",
        f"- Total sesiones registradas: {con_total}",
        f"- Sesiones del día {ayer.strftime('%Y-%m-%d')}: {con_ayer}",
    ]
    if origen is not None:
        lineas.append(f"- Fuente de los conteos: {origen}")
    if nuevas is not None:
        lineas.append(f"- Sesiones nuevas incorporadas al acumulado: {nuevas}")
    lineas += [
        "",
        "## Sesiones por día (últimos 7)",
        "",
        "| Fecha | Sesiones |",
        "|-------|----------|",
    ]
    for fecha in sorted(por_fecha.keys())[-7:]:
        lineas.append(f"| {fecha} | {por_fecha[fecha]} |")
    lineas.append("")
    lineas.append("## Nota para Hermes")
    lineas.append("")
    lineas.append("Revisar las sesiones del día anterior con session_search si se necesita contexto.")
    lineas.append("")
    return lineas


def main():
    hoy = datetime.now()
    ayer = hoy - timedelta(days=1)

    SESIONES_DIR.mkdir(parents=True, exist_ok=True)
    hubo_acumulado = ACUMULADO.exists()

    # 1. Exportar SOLO el delta (si el acumulado no existe, exportación completa una vez)
    if hubo_acumulado:
        cmd = ["hermes", "sessions", "export", "--newer-than", f"{DIAS_DELTA}d", str(TMP_DELTA)]
    else:
        cmd = ["hermes", "sessions", "export", str(TMP_DELTA)]
    rc, out, err = run(cmd)
    if rc != 0 or not TMP_DELTA.exists():
        print(f"ERROR: hermes sessions export falló ({rc}): {err[:200]}")
        return 1

    # 2. Guardar el delta del día (ya NO una copia completa de todo el histórico)
    delta_dia = SESIONES_DIR / f"sesiones-delta-{hoy.strftime('%Y%m%d')}.jsonl"
    try:
        delta_dia.write_bytes(TMP_DELTA.read_bytes())
    except OSError as e:
        print(f"ERROR escribiendo {delta_dia}: {e}")
        return 1

    # 3. Fusionar en el acumulado deduplicado (append, sin reescribir el histórico)
    try:
        nuevas = _fusionar_delta(TMP_DELTA, ACUMULADO)
    except OSError as e:
        print(f"ERROR fusionando en {ACUMULADO}: {e}")
        return 1

    # 4. Contar sobre el acumulado (histórico completo) para no perder los totales
    origen = f"acumulado ({ACUMULADO.name}) + delta de {DIAS_DELTA} días"
    if ACUMULADO.exists():
        por_fecha, con_ayer, con_total = _contar_sesiones(ACUMULADO, ayer)
    else:
        origen = f"delta de {DIAS_DELTA} días (no hay acumulado)"
        por_fecha, con_ayer, con_total = _contar_sesiones(TMP_DELTA, ayer)

    # 5. Resumen del día
    resumen = SESIONES_DIR / f"resumen-dia-{ayer.strftime('%Y-%m-%d')}.md"
    lineas = _construir_resumen(hoy, ayer, por_fecha, con_total, con_ayer, origen, nuevas)

    try:
        resumen.write_text("\n".join(lineas), encoding="utf-8")
    except OSError as e:
        print(f"ERROR escribiendo resumen: {e}")
        return 1

    print(f"OK: {nuevas} sesiones nuevas ({delta_dia.name}, {delta_dia.stat().st_size // 1024} KB)")
    print(f"OK: {con_total} sesiones en el historico, {con_ayer} de {ayer.strftime('%Y-%m-%d')} — resumen en {resumen.name}")

    # Notificar al canal de eventos compartido (para que CLI/Telegram lo vean)
    subprocess.run(
        ["bash", str(HOME / ".hermes/scripts/shared-events.sh"), "write", "cron",
         "completado",
         f"Consolidador: {nuevas} sesiones nuevas, {con_total} en el historico, {con_ayer} del dia anterior",
         str(resumen)],
        capture_output=True, text=True, timeout=30,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
