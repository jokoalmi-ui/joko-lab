#!/usr/bin/env python3
"""CAPTURA DE REFERENCIA — "¿la salida sigue idéntica?"

4ª pieza del ciclo de calidad del lab (junto a memory_detective,
pipeline_inspector y regression_guardian). Automatiza los pasos 3 y 6 de la
skill `refactor-seguro`: capturar la salida de una tool ANTES de tocar código
y compararla DESPUÉS, sin escribir un script de captura a mano en cada refactor.

Resuelve dos pitfalls documentados:
  - pitfall 21: las partes volátiles (rutas /tmp, timestamps, duraciones, pids,
    direcciones de memoria) se NORMALIZAN antes de guardar, así el diff no da
    falsos positivos.
  - pitfall 33: NUNCA sobrescribe una referencia existente con la misma
    etiqueta (era la causa del falso "SALIDA_IDENTICA_OK": se comparaba
    nuevo-vs-nuevo). Para rehacerla hay que pasar --forzar o cambiar etiqueta.

Uso:
  # 1) ANTES de tocar el código (guarda la referencia)
  python3 tools/captura_referencia.py --guardar --tool complejidad_crap -- --json

  # 2) DESPUÉS del refactor (compara; exit 0 = idéntica, 1 = distinta)
  python3 tools/captura_referencia.py --comparar --tool complejidad_crap -- --json

Opciones: --etiqueta (nombre de la captura), --dir (dónde se guardan, /tmp/joko-refs
por defecto), --timeout (120 s), --python (intérprete, p.ej. el venv RAG), --forzar.

Solo lectura sobre el lab: ejecuta la tool indicada con LOS ARGUMENTOS QUE TÚ PASES
(usa flags de solo lectura: --json, --dry-run, --help) y escribe únicamente en --dir.
⚠️ La tool objetivo debe ser DETERMINISTA: si lee BD viva, reloj o red (caso medido
`gasto_semanal`: 172→171 sesiones entre dos corridas), la identidad de salida no
significa nada → usa un fixture, `--dry-run` o argumentos que fijen los datos.
"""

import argparse
import difflib
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

LAB = Path(os.path.expanduser("~/joko-lab"))
TOOLS = LAB / "tools"
DIR_DEFECTO = Path("/tmp/joko-refs")
TIMEOUT_DEFECTO = 120

# Partes volátiles entre dos ejecuciones (pitfall 21). El orden importa:
# el timestamp completo va antes que la hora suelta.
PATRONES_VOLATILES = [
    (re.compile(r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:[.,]\d+)?"), "<TS>"),
    (re.compile(r"\b\d{2}:\d{2}:\d{2}\b"), "<HORA>"),
    (re.compile(r"/tmp/[A-Za-z0-9_.-]+"), "/tmp/<TMP>"),
    (re.compile(r"\b\d+\.\d+\s?(?:s|ms|seg|segundos)\b"), "<DUR>"),
    (re.compile(r"\b(pid|PID)\s*[=:]\s*\d+"), r"\1=<PID>"),
    (re.compile(r"0x[0-9a-fA-F]{6,}"), "<ADDR>"),
]


def _normalizar(texto: str) -> str:
    """Sustituye las partes volátiles por marcadores estables."""
    for patron, marca in PATRONES_VOLATILES:
        texto = patron.sub(marca, texto)
    return texto


def _resolver_tool(nombre: str):
    """Devuelve la ruta de tools/<nombre>.py o None si no existe o sale de tools/."""
    candidato = TOOLS / (nombre if nombre.endswith(".py") else f"{nombre}.py")
    try:
        ruta = candidato.resolve()
    except OSError:
        return None
    if ruta.is_file() and ruta.parent == TOOLS.resolve():
        return ruta
    return None


def _huella(datos: dict) -> str:
    """sha256 corto de la salida normalizada (exit + stdout + stderr)."""
    crudo = f"{datos.get('exit')}\n{datos.get('stdout', '')}\n{datos.get('stderr', '')}"
    return hashlib.sha256(crudo.encode("utf-8")).hexdigest()[:12]


def _ejecutar(tool: Path, argumentos: list, timeout: int, python: str) -> dict:
    """Ejecuta la tool capturando exit/stdout/stderr ya normalizados."""
    cmd = [python, str(tool), *argumentos]
    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout, cwd=str(LAB)
        )
    except subprocess.TimeoutExpired:
        return {"exit": None, "stdout": "", "stderr": f"TIMEOUT {timeout}s", "cmd": cmd}
    except OSError as exc:
        return {"exit": None, "stdout": "", "stderr": f"ERROR {exc}", "cmd": cmd}
    return {
        "exit": proc.returncode,
        "stdout": _normalizar(proc.stdout),
        "stderr": _normalizar(proc.stderr),
        "cmd": cmd,
    }


def _ruta_ref(directorio: Path, tool: Path, etiqueta: str) -> Path:
    """Ruta del JSON de referencia: <dir>/<tool>__<etiqueta>.json."""
    seguro = re.sub(r"[^A-Za-z0-9_.-]+", "_", etiqueta) or "ref"
    return directorio / f"{tool.stem}__{seguro}.json"


def _guardar_json(destino: Path, datos: dict) -> None:
    """Escribe la referencia en disco creando el directorio si hace falta."""
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8")


def _cargar_json(destino: Path):
    """Lee la referencia; None si no existe o está corrupta."""
    try:
        return json.loads(destino.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _diff(ref: dict, nuevo: dict) -> list:
    """Lista de diferencias (exit + diff unificado por canal); vacía si idéntica."""
    diffs = []
    if ref.get("exit") != nuevo.get("exit"):
        diffs.append(f"  exit: antes={ref.get('exit')} ahora={nuevo.get('exit')}")
    for canal in ("stdout", "stderr"):
        antes = ref.get(canal, "").splitlines()
        ahora = nuevo.get(canal, "").splitlines()
        if antes != ahora:
            diffs.extend(
                difflib.unified_diff(
                    antes, ahora, fromfile=f"antes/{canal}", tofile=f"ahora/{canal}",
                    lineterm="", n=2,
                )
            )
    return diffs


def _accion_guardar(nuevo: dict, destino: Path, forzar: bool) -> int:
    """Modo --guardar: persiste la referencia sin pisar una anterior (pitfall 33)."""
    if destino.exists() and not forzar:
        print(f"🔴 Ya existe una referencia: {destino}")
        print("   No la sobrescribo (pitfall 33: compararías nuevo-vs-nuevo).")
        print("   Usa otra --etiqueta, o --forzar si de verdad quieres rehacerla.")
        return 2
    nuevo["huella"] = _huella(nuevo)
    _guardar_json(destino, nuevo)
    print(f"✅ Referencia guardada: {destino}")
    print(f"   exit={nuevo['exit']} · huella={nuevo['huella']} · cmd={' '.join(nuevo['cmd'])}")
    return 0


def _accion_comparar(nuevo: dict, destino: Path) -> int:
    """Modo --comparar: diff contra la referencia (0 idéntica, 1 distinta, 2 sin ref)."""
    ref = _cargar_json(destino)
    if ref is None:
        print(f"🔴 No hay referencia legible en {destino}")
        print("   Ejecuta primero con --guardar ANTES de tocar el código.")
        return 2
    diffs = _diff(ref, nuevo)
    if not diffs:
        print("✅ SALIDA IDÉNTICA a la referencia")
        print(f"   {destino} · huella={_huella(nuevo)} · exit={nuevo['exit']}")
        return 0
    print(f"🔴 SALIDA DISTINTA ({len(diffs)} línea(s) de diff)")
    print(f"   referencia: {destino}")
    print(f"   exit: antes={ref.get('exit')} ahora={nuevo.get('exit')}")
    for linea in diffs:
        print(linea if linea.startswith((" ", "+", "-", "@")) else f"  {linea}")
    return 1


def _parsear(argv):
    """Argumentos de la CLI (los de la tool van tras `--`)."""
    p = argparse.ArgumentParser(
        description="Captura y compara la salida de una tool del lab (red de seguridad).",
        epilog="Ejemplo: --guardar --tool complejidad_crap -- --json",
    )
    modo = p.add_mutually_exclusive_group(required=True)
    modo.add_argument("--guardar", action="store_true", help="guarda la referencia")
    modo.add_argument("--comparar", action="store_true", help="compara con la referencia")
    p.add_argument("--tool", required=True, help="nombre de la tool (sin .py)")
    p.add_argument("--etiqueta", default="antes", help="nombre de la captura (def. 'antes')")
    p.add_argument("--dir", default=str(DIR_DEFECTO), help="directorio de referencias")
    p.add_argument("--timeout", type=int, default=TIMEOUT_DEFECTO, help="segundos (def. 120)")
    p.add_argument("--python", default=sys.executable, help="intérprete (def. el actual)")
    p.add_argument("--forzar", action="store_true", help="permite pisar una referencia")
    args, extra = p.parse_known_args(argv)
    args.argumentos = extra[1:] if extra and extra[0] == "--" else extra
    return args


def main(argv=None) -> int:
    """Punto de entrada: resuelve la tool, la ejecuta y guarda o compara."""
    args = _parsear(argv)
    tool = _resolver_tool(args.tool)
    if tool is None:
        print(f"🔴 No existe tools/{args.tool}.py (o está fuera de tools/)")
        return 2
    destino = _ruta_ref(Path(args.dir).expanduser(), tool, args.etiqueta)
    nuevo = _ejecutar(tool, args.argumentos, args.timeout, args.python)
    if args.guardar:
        return _accion_guardar(nuevo, destino, args.forzar)
    return _accion_comparar(nuevo, destino)


if __name__ == "__main__":
    sys.exit(main())
