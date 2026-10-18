#!/usr/bin/env python3
"""AUDITOR DE TESTS DEPENDIENTES DEL ENTORNO — "¿algún test cambia según TMPDIR?"

Carencia que resuelve (medida el 05-oct-2026, sesión semanal de auto-mejora):
  la suite del lab llevaba >=6 días con 5 tests rojos y nadie lo detectó.
  4 de esos 5 rojos eran FALSOS: los tests crean directorios con `tempfile`,
  `tempfile` respeta TMPDIR, y en las sesiones de Hermes TMPDIR apunta a
  `~/.hermes/cache/scratch` — rama que `tools/auditar_cobertura_backups.py`
  excluye como ruido ("/.hermes/"). Dato medido el 05-oct: la MISMA suite daba
  5 fallos con el TMPDIR de Hermes y 1 con TMPDIR=/tmp. Consecuencia: quien
  miraba la suite desde un shell normal la veía casi verde y el problema
  (tests no herméticos) quedaba invisible.

Qué hace (SOLO LECTURA; no modifica tests, código ni configuración):
  1. Ejecuta la suite DOS veces en modo verbose, con dos TMPDIR distintos
     (neutro y el de Hermes por defecto).
  2. Compara el resultado test a test y lista las DIVERGENCIAS (test que pasa
     en un entorno y falla en el otro) — la huella de un test no hermético.
  3. Resume los estados de cada entorno para tener la foto completa.

Uso:
  python3 tools/auditor_tests_entorno.py                 # informe legible
  python3 tools/auditor_tests_entorno.py --json          # JSON (crons)
  python3 tools/auditor_tests_entorno.py --verbose       # lista todos los tests
  python3 tools/auditor_tests_entorno.py --python <py> --tests <dir> \
      --tmpdir-neutro /tmp --tmpdir-hermes ~/.hermes/cache/scratch

Código de salida: 0 = ningún test cambia de resultado según el entorno,
1 = hay divergencias (tests no herméticos), 2 = error de uso.

Nota de coste: la suite del lab tarda <1 s, así que ejecutarla dos veces es
barato; usar el python del venv RAG cuando haya deps pesadas (lancedb/yaml).
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

LAB = Path.home() / "joko-lab"
DIR_TESTS_DEFECTO = LAB / "tests"
VENV_RAG = Path.home() / ".venv" / "hermes-rag" / "bin" / "python3"
TMPDIR_NEUTRO_DEFECTO = "/tmp"
TMPDIR_HERMES_DEFECTO = Path.home() / ".hermes" / "cache" / "scratch"
TIMEOUT_DEFECTO = 900

# Línea de resultado de `unittest -v`: "test_x (mod.Clase.test_x) ... ok".
# Los tracebacks van indentados, así que el ancla ^ los descarta.
RE_RESULTADO = re.compile(r"^(\S+) \(([^)]+)\) \.\.\. (.+)$", re.M)

# Estados que imprime unittest. Se BUSCA uno de ellos dentro del resto de la
# línea porque hay avisos (p.ej. DeprecationWarning) que se intercalan en la
# MISMA línea del resultado y desplazan el "ok" -> sin este filtro el parser
# tomaba el texto del aviso como estado (artefacto medido el 05-oct-2026).
ESTADOS_VALIDOS = ("expected failure", "unexpected success", "skipped",
                   "fail", "error", "ok")
RE_ESTADO = re.compile(r"\b(?:" + "|".join(ESTADOS_VALIDOS) + r")\b", re.I)
ESTADO_DESCONOCIDO = "desconocido"


# --- Helpers puros (testeables sin ejecutar la suite) ------------------------

def parsear_verbose(texto: str) -> dict:
    """Extrae {id_de_test: estado} de la salida de `unittest discover -v`.

    El estado se reconoce por palabra clave ("ok", "fail", "error",
    "skipped"...) en el resto de la línea; si no aparece ninguno se marca
    "desconocido" (nunca se cuela texto de un aviso intercalado como estado)."""
    estados = {}
    for coincidencia in RE_RESULTADO.finditer(texto):
        encontrado = RE_ESTADO.search(coincidencia.group(3))
        estados[coincidencia.group(2)] = (encontrado.group(0).lower()
                                          if encontrado else ESTADO_DESCONOCIDO)
    return estados


def comparar(estados_a: dict, estados_b: dict) -> list:
    """Devuelve [(test_id, estado_a, estado_b)] de los tests que NO coinciden."""
    claves = set(estados_a) | set(estados_b)
    return sorted((c, estados_a.get(c, "ausente"), estados_b.get(c, "ausente"))
                  for c in claves if estados_a.get(c) != estados_b.get(c))


def resumir_estados(estados: dict) -> dict:
    """Cuenta cuántos tests hay en cada estado ({'ok': 340, 'fail': 1, ...})."""
    resumen = {}
    for estado in estados.values():
        resumen[estado] = resumen.get(estado, 0) + 1
    return resumen


def ejecutar_suite(python: str, dir_tests, tmpdir, timeout: int = TIMEOUT_DEFECTO):
    """Ejecuta la suite con `tmpdir` como TMPDIR. Devuelve (codigo, texto).

    No escribe en el árbol del lab (PYTHONDONTWRITEBYTECODE=1 evita
    __pycache__). Código -1 = no se pudo ejecutar (timeout o binario ausente)."""
    entorno = dict(os.environ)
    entorno["TMPDIR"] = str(tmpdir)
    entorno["PYTHONDONTWRITEBYTECODE"] = "1"
    # -W ignore va ANTES de -m: es flag del intérprete y evita que los avisos
    # (p.ej. DeprecationWarning) se intercalen en la línea del resultado.
    comando = [python, "-W", "ignore", "-m", "unittest", "discover",
               "-s", str(dir_tests), "-v"]
    try:
        proc = subprocess.run(comando, env=entorno, cwd=str(Path(dir_tests).parent),
                              capture_output=True, text=True, timeout=timeout)
    except (subprocess.TimeoutExpired, OSError) as exc:
        return -1, f"ERROR al ejecutar la suite: {exc}"
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def python_por_defecto() -> str:
    """Python del venv RAG (trae las deps del lab) si existe; si no, el actual."""
    return str(VENV_RAG) if VENV_RAG.is_file() else sys.executable


# --- Informe -----------------------------------------------------------------

def _lineas_estados(etiqueta: str, tmpdir, estados: dict) -> list:
    """Líneas del resumen de estados de un entorno."""
    resumen = resumir_estados(estados)
    detalle = ", ".join(f"{k}={v}" for k, v in sorted(resumen.items())) or "(sin tests)"
    return [f"- {etiqueta}: TMPDIR={tmpdir} -> {len(estados)} tests ({detalle})"]


def formatear_informe(python, tmpdir_neutro, tmpdir_hermes, est_neutro, est_hermes,
                      divergencias, verbose=False) -> str:
    """Construye el informe legible."""
    lineas = ["# 🌱 AUDITOR DE TESTS DEPENDIENTES DEL ENTORNO (solo lectura)", "",
              f"Intérprete: `{python}`", "## Ejecuciones"]
    lineas += _lineas_estados("Neutro", tmpdir_neutro, est_neutro)
    lineas += _lineas_estados("Hermes", tmpdir_hermes, est_hermes)
    lineas += ["", f"## 🔀 Divergencias ({len(divergencias)})"]
    if divergencias:
        for test_id, a, b in divergencias:
            lineas.append(f"- `{test_id}`: neutro={a} / hermes={b}")
        lineas += ["", "Estos tests NO son herméticos al entorno: fijar la base "
                       "temporal (p.ej. `tempfile.TemporaryDirectory(dir=\"/tmp\")`) "
                       "o neutralizar la variable que los afecta."]
    else:
        lineas.append("- (ninguna): ningún test cambia de resultado según TMPDIR ✅")
    if verbose:
        lineas += ["", "## 📋 Todos los tests (neutro vs hermes)"]
        for test_id in sorted(set(est_neutro) | set(est_hermes)):
            a = est_neutro.get(test_id, "ausente")
            b = est_hermes.get(test_id, "ausente")
            lineas.append(f"- {'≠' if a != b else '='} {a:>8} {b:<8} {test_id}")
    return "\n".join(lineas)


def resumen_json(python, tmpdir_neutro, tmpdir_hermes, est_neutro, est_hermes,
                 divergencias) -> dict:
    """Resumen estructurado serializable (sin lambdas ni Paths)."""
    return {
        "python": str(python),
        "entornos": [
            {"etiqueta": "neutro", "tmpdir": str(tmpdir_neutro),
             "estados": resumir_estados(est_neutro)},
            {"etiqueta": "hermes", "tmpdir": str(tmpdir_hermes),
             "estados": resumir_estados(est_hermes)},
        ],
        "divergencias": [{"test": t, "neutro": a, "hermes": b}
                         for t, a, b in divergencias],
        "n_divergencias": len(divergencias),
    }


# --- CLI ---------------------------------------------------------------------

def _parsear_args(argv=None):
    """Argumentos de CLI."""
    p = argparse.ArgumentParser(
        description="Detecta tests cuyo resultado depende del entorno (TMPDIR)")
    p.add_argument("--python", default="", help="intérprete (def: venv RAG si existe)")
    p.add_argument("--tests", default=str(DIR_TESTS_DEFECTO), help="directorio de tests")
    p.add_argument("--tmpdir-neutro", default=TMPDIR_NEUTRO_DEFECTO,
                   help=f"TMPDIR neutro (def: {TMPDIR_NEUTRO_DEFECTO})")
    p.add_argument("--tmpdir-hermes", default=str(TMPDIR_HERMES_DEFECTO),
                   help="TMPDIR de la sesión Hermes")
    p.add_argument("--timeout", type=int, default=TIMEOUT_DEFECTO,
                   help="segundos por ejecución de la suite")
    p.add_argument("--verbose", action="store_true", help="lista todos los tests")
    p.add_argument("--json", action="store_true", help="salida JSON")
    return p.parse_args(argv)


def main(argv=None) -> int:
    """Ejecuta la suite en dos entornos y reporta las divergencias."""
    args = _parsear_args(argv)
    python = args.python or python_por_defecto()
    if not Path(python).is_file():
        print(f"ERROR: no existe el intérprete {python}", file=sys.stderr)
        return 2
    _, texto_neutro = ejecutar_suite(python, args.tests, args.tmpdir_neutro, args.timeout)
    _, texto_hermes = ejecutar_suite(python, args.tests, args.tmpdir_hermes, args.timeout)
    est_neutro = parsear_verbose(texto_neutro)
    est_hermes = parsear_verbose(texto_hermes)
    divergencias = comparar(est_neutro, est_hermes)
    if args.json:
        print(json.dumps(resumen_json(python, args.tmpdir_neutro, args.tmpdir_hermes,
                                      est_neutro, est_hermes, divergencias),
                         ensure_ascii=False, indent=2))
    else:
        print(formatear_informe(python, args.tmpdir_neutro, args.tmpdir_hermes,
                                est_neutro, est_hermes, divergencias, args.verbose))
    return 1 if divergencias else 0


if __name__ == "__main__":
    raise SystemExit(main())
