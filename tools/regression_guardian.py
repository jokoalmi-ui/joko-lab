#!/usr/bin/env python3
"""
REGRESSION GUARDIAN — "¿Este cambio rompe algo?"

Cuando se modifica una tool, genera y ejecuta verificación de regresión:
  1. Detecta archivos modificados recientemente (mtime < 24h) en tools/
  2. Comprueba sintaxis (py_compile) y tests existentes de cada archivo
  3. Mide la complejidad ciclomática (McCabe) de cada archivo verificado y
     avisa si alguna función supera el umbral (pitfall 41/24: los scripts
     nuevos deben nacer con main() <= 10; el drift silencioso de complejidad
     se acumula si nadie lo mide al tocar código)
  4. Ejecuta la suite completa y reporta impacto (✅ / ⚠️ / 🔴)

Uso:
  python3 tools/regression_guardian.py            # detecta cambios recientes
  python3 tools/regression_guardian.py --archivo tools/llm_as_judge.py
  python3 tools/regression_guardian.py --suite     # solo ejecuta la suite completa

Salida: informe de regresión con estado ✅/⚠️/🔴 y siguiente paso.
"""

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

LAB = Path(os.path.expanduser("~/joko-lab"))
TOOLS = LAB / "tools"
TESTS = LAB / "tests"
VENV_RAG = Path(os.path.expanduser("~/.venv/hermes-rag/bin/python"))
VENTANA_HORAS = 24

# Motor McCabe del lab (tools/complejidad_crap.py, solo ast, sin deps): se
# importa para medir la complejidad de los archivos verificados SIN duplicar
# la lógica de cálculo (mantener el mismo criterio en todo el lab).
sys.path.insert(0, str(TOOLS))
import complejidad_crap  # noqa: E402  (requiere TOOLS en sys.path)


def _archivos_recientes(ventana: float = VENTANA_HORAS) -> list:
    """Lista archivos de tools/ modificados en las últimas N horas."""
    ahora = time.time()
    resultado = []
    for f in sorted(TOOLS.glob("*.py")):
        if f.name.endswith(".bak") or "__pycache__" in str(f):
            continue
        try:
            mtime = f.stat().st_mtime
            if ahora - mtime < ventana * 3600:
                resultado.append(f)
        except Exception:
            continue
    return resultado


def _test_para(archivo: Path) -> list:
    """Busca tests existentes para un archivo (test_<nombre>.py)."""
    nombre = archivo.name.replace(".py", "")
    posibles = [
        TESTS / f"test_{nombre}.py",
        TESTS / f"test_{nombre}_audit.py",
        LAB / "tools" / "tests" / f"test_{nombre}.py",
    ]
    return [p for p in posibles if p.exists()]


def _py_compile(archivo: Path) -> tuple:
    """Verifica sintaxis. Devuelve (ok, mensaje)."""
    r = subprocess.run(
        [sys.executable, "-m", "py_compile", str(archivo)],
        capture_output=True, text=True, timeout=30,
    )
    if r.returncode == 0:
        return True, "sintaxis OK"
    return False, f"sintaxis ERROR: {r.stderr[:300]}"


def _funciones_complejas(archivo: Path) -> list:
    """Funciones del archivo con complejidad > umbral (motor complejidad_crap)."""
    try:
        return [
            r for r in complejidad_crap.analizar_archivo(archivo)
            if r["complejidad"] > complejidad_crap.UMBRAL_COMPLEJO
        ]
    except Exception:
        return []


def _bloque_complejidad(funciones: list) -> str:
    """Bloque de complejidad McCabe para el informe (✅ si limpio, 🟠/🔴 si no)."""
    if not funciones:
        return "- ✅ Complejidad OK (ninguna función >10)"
    lines = []
    for r in sorted(funciones, key=lambda x: x["complejidad"], reverse=True):
        marca = "🔴" if r["complejidad"] > complejidad_crap.UMBRAL_MUY_COMPLEJO else "🟠"
        lines.append(
            f"- {marca} `{r['funcion']}()` complejidad {r['complejidad']} "
            f"(línea {r['linea']}) — refactor pendiente (pitfall 41/24)"
        )
    return "\n".join(lines)


def _ejecutar_suite() -> tuple:
    """Ejecuta la suite unittest completa. Devuelve (ok, resumen)."""
    python = str(VENV_RAG) if VENV_RAG.exists() else sys.executable
    r = subprocess.run(
        [python, "-m", "unittest", "discover", "-s", "tests"],
        capture_output=True, text=True, timeout=300, cwd=str(LAB),
    )
    out = r.stdout + r.stderr
    # extraer resumen: "Ran N tests" / "OK" / "FAILED"
    resumen = out.strip().splitlines()[-5:]
    return r.returncode == 0, "\n".join(resumen)


def _informe(archivo: Path) -> str:
    """Informe de regresión para un archivo concreto."""
    lines = []
    lines.append(f"## 🔄 {archivo.name}")
    ok_sint, msg_sint = _py_compile(archivo)
    lines.append(f"- {'✅' if ok_sint else '🔴'} {msg_sint}")
    lines.append(_bloque_complejidad(_funciones_complejas(archivo)))

    tests = _test_para(archivo)
    if tests:
        lines.append(f"- 🧪 Tests existentes: {', '.join(str(t.name) for t in tests)}")
        for t in tests:
            r = subprocess.run(
                [str(VENV_RAG) if VENV_RAG.exists() else sys.executable, "-m", "unittest", str(t)],
                capture_output=True, text=True, timeout=120, cwd=str(LAB),
            )
            ok = r.returncode == 0
            ultima = (r.stdout + r.stderr).strip().splitlines()[-3:]
            lines.append(f"  - {'✅' if ok else '🔴'} {t.name}: {' | '.join(ultima)}")
    else:
        lines.append("- ⚠️ Sin test específico para este archivo (la suite general cubrirá)")

    return "\n".join(lines)


def _informe_suite(ok: bool, resumen: str) -> str:
    """Formatea el resultado de la suite."""
    estado = "✅" if ok else "🔴"
    lines = [f"## {estado} Suite completa"]
    for l in resumen[-3:]:
        lines.append(f"  {l}")
    return "\n".join(lines)


def _siguiente_paso(ok: bool, hay_complejas: bool = False) -> str:
    """Genera el siguiente paso según el estado (suite + complejidad)."""
    lines = ["## 🎯 Siguiente paso"]
    if not ok:
        lines.append("- 🔴 La suite falla. Revisar el informe y corregir antes de continuar.")
    elif hay_complejas:
        lines.append("- ⚠️ Hay funciones >10 en el cambio: refactorizar antes de cerrar "
                     "(pitfall 41/24). La suite pasa, pero la complejidad nueva es deuda.")
    else:
        lines.append("- ✅ Sin regresiones ni complejidad nueva. Cambio seguro (con backup RULE-008).")
    return "\n".join(lines)


def _modo_suite() -> int:
    """Modo --suite: ejecuta la suite completa y reporta."""
    ok, resumen = _ejecutar_suite()
    print(f"## {'✅ SUITE OK' if ok else '🔴 SUITE CON FALLOS'}")
    print()
    for l in resumen:
        print(f"  {l}")
    return 0 if ok else 1


def _modo_archivo(archivo: Path) -> int:
    """Modo --archivo: verifica un archivo concreto."""
    if not archivo.exists():
        print(f"❌ No existe: {archivo}")
        return 1
    print(_informe(archivo))
    print()
    ok, resumen = _ejecutar_suite()
    hay_complejas = bool(_funciones_complejas(archivo))
    print(_informe_suite(ok, resumen))
    print()
    print(_siguiente_paso(ok, hay_complejas))
    return 0 if ok else 1


def _modo_deteccion() -> int:
    """Modo automático: detecta cambios recientes y verifica."""
    recientes = _archivos_recientes()
    if not recientes:
        print("## 🔍 Sin archivos modificados en las últimas 24h en tools/")
        print()
        print("Si acabas de cambiar algo, pasa el --archivo explícito.")
        return 0

    print(f"## 🔍 Archivos modificados en las últimas 24h ({len(recientes)})")
    for f in recientes:
        print(f"- `{f.name}` ({time.strftime('%H:%M', time.localtime(f.stat().st_mtime))})")
    print()
    print("## 🔄 Verificación individual")
    total_complejas = 0
    for f in recientes:
        print(_informe(f))
        print()
        total_complejas += len(_funciones_complejas(f))

    print("## 🧪 Suite completa")
    ok, resumen = _ejecutar_suite()
    print(f"- {'✅ SUITE OK' if ok else '🔴 SUITE CON FALLOS'}")
    for l in resumen[-3:]:
        print(f"  {l}")
    print()
    print(_siguiente_paso(ok, total_complejas > 0))
    return 0 if ok else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Regression Guardian: ¿este cambio rompe algo?")
    parser.add_argument("--archivo", default=None, help="Archivo concreto a verificar")
    parser.add_argument("--suite", action="store_true", help="Solo ejecutar la suite completa")
    args = parser.parse_args()

    print("# 🧪 REGRESSION GUARDIAN — verificación de regresión")
    print()

    if args.suite:
        return _modo_suite()

    if args.archivo:
        return _modo_archivo(Path(args.archivo))

    return _modo_deteccion()


if __name__ == "__main__":
    sys.exit(main())
