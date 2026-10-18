#!/usr/bin/env python3
"""
complejidad_crap.py — Complejidad ciclomática (McCabe) de los scripts del lab.

Herramienta DETERMINISTA: señala objetivamente qué código del lab es difícil
de cambiar o verificar. Es la base accionable del pendiente "Verificación de
código IA / CRAP" (06-ago): el CRAP completo (complejidad x (1 - cobertura))
NO es computable hoy porque el lab no tiene suite de tests unitarios de
tools/ (cobertura ≈ 0 -> CRAP se degradaría a complejidad pura). Esta
herramienta mide la complejidad, que es la señal util para el L2: qué scripts
merecen gate de revisión o refactor.

Método: AST estándar de Python (sin dependencias externas). Complejidad =
1 (base) + puntos de decisión: if/elif, for, while, except, assert, and/or,
if-expresion, if dentro de comprehensions. Mismo criterio que radon (mccabe).

Umbrales clasicos (McCabe):
  <= 10  mantenible
  11-20  complejo (revisar)
  > 20   muy complejo (candidato a refactor o gate)

Uso:
  python3 complejidad_crap.py [DIR] [--json] [--top N] [--min N]

Solo lectura: no modifica nada. Salida legible o JSON (para L2/ledger).
"""

import argparse
import ast
import json
import sys
from pathlib import Path

DEFAULT_DIR = Path.home() / "joko-lab" / "tools"
UMBRAL_COMPLEJO = 10
UMBRAL_MUY_COMPLEJO = 20


def _decision_points(nodo) -> int:
    """Cuenta puntos de decision (McCabe) en un subarbol AST."""
    puntos = 0
    for hijo in ast.walk(nodo):
        if isinstance(hijo, (ast.If, ast.While, ast.For, ast.ExceptHandler,
                             ast.Assert, ast.IfExp, ast.Match)):
            puntos += 1
        elif isinstance(hijo, ast.BoolOp):
            # and/or: cada operador anadido suma 1 (len(operadores)-1)
            puntos += max(0, len(hijo.values) - 1)
        elif isinstance(hijo, (ast.ListComp, ast.SetComp, ast.DictComp,
                               ast.GeneratorExp)):
            # cada clausula `if` dentro de la comprehension suma 1
            # (los ifs viven en cada nodo comprehension de .generators)
            puntos += sum(len(gen.ifs) for gen in hijo.generators)
    return puntos


def complejidad_funcion(nodo_func) -> int:
    """Complejidad ciclomatica de una funcion/metodo (1 + puntos de decision)."""
    return 1 + _decision_points(nodo_func)


def analizar_archivo(path: Path) -> list:
    """Devuelve [{archivo, funcion, complejidad, linea}] para un .py."""
    try:
        arbol = ast.parse(path.read_text(encoding="utf-8", errors="replace"))
    except SyntaxError as e:
        return [{
            "archivo": str(path),
            "funcion": f"<SyntaxError: {e.msg}>",
            "complejidad": -1,
            "linea": e.lineno or 0,
        }]
    resultados = []
    for nodo in ast.walk(arbol):
        if isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef)):
            resultados.append({
                "archivo": str(path),
                "funcion": nodo.name,
                "complejidad": complejidad_funcion(nodo),
                "linea": nodo.lineno,
            })
    return resultados


def analizar_dir(directorio: Path) -> list:
    todos = []
    for f in sorted(directorio.glob("*.py")):
        todos.extend(analizar_archivo(f))
    return todos


def _marca(complejidad: int) -> str:
    """Emoji de marca según umbrales."""
    if complejidad > UMBRAL_MUY_COMPLEJO:
        return "🔴"
    if complejidad > UMBRAL_COMPLEJO:
        return "🟠"
    return "🟢"


def _formatear_funcion(r: dict) -> str:
    """Formatea una función del reporte."""
    return (f"{_marca(r['complejidad'])} {r['complejidad']:>3}  "
            f"{Path(r['archivo']).name}:{r['linea']} {r['funcion']}()")


def _contar_categorias(resultados: list) -> tuple:
    """Devuelve (n_muy_complejas, n_complejas)."""
    n_muy = sum(1 for r in resultados if r["complejidad"] > UMBRAL_MUY_COMPLEJO)
    n_comp = sum(1 for r in resultados if UMBRAL_COMPLEJO < r["complejidad"] <= UMBRAL_MUY_COMPLEJO)
    return n_muy, n_comp


def imprimir_reporte(resultados: list, top: int, min_complejidad: int):
    if not resultados:
        print("No hay funciones que analizar.")
        return
    # Ordenar por complejidad desc
    orden = sorted(resultados, key=lambda r: r["complejidad"], reverse=True)
    if min_complejidad:
        orden = [r for r in orden if r["complejidad"] >= min_complejidad]
    print("=" * 72)
    print("COMPLEJIDAD CICLOMATICA (McCabe) — scripts del lab")
    print("Umbrales: <=10 mantenible | 11-20 complejo | >20 muy complejo")
    print("=" * 72)
    if top and top > 0:
        orden = orden[:top]
    n_muy, n_comp = _contar_categorias(resultados)
    print(f"\nTotal funciones: {len(resultados)} | complejas (11-20): {n_comp} | "
          f"muy complejas (>20): {n_muy}\n")
    for r in orden:
        print(_formatear_funcion(r))
    print("=" * 72)
    print("Solo lectura. Para CRAP completo (x cobertura) faltan tests "
          "unitarios de tools/.")


def main():
    parser = argparse.ArgumentParser(
        description="Complejidad ciclomatica (McCabe) de scripts del lab")
    parser.add_argument("directorio", nargs="?", default=str(DEFAULT_DIR),
                        help="Directorio con *.py (default: tools/)")
    parser.add_argument("--json", action="store_true", help="Salida JSON")
    parser.add_argument("--top", type=int, default=0,
                        help="Mostrar solo las N mas complejas (0 = todas)")
    parser.add_argument("--min", type=int, default=0,
                        help="Solo funciones con complejidad >= N")
    args = parser.parse_args()

    directorio = Path(args.directorio).expanduser()
    if not directorio.exists():
        print(f"ERROR: no existe {directorio}", file=sys.stderr)
        sys.exit(1)

    resultados = analizar_dir(directorio)
    if args.json:
        resumen = {
            "directorio": str(directorio),
            "total_funciones": len(resultados),
            "muy_complejas": sum(1 for r in resultados if r["complejidad"] > UMBRAL_MUY_COMPLEJO),
            "complejas": sum(1 for r in resultados if UMBRAL_COMPLEJO < r["complejidad"] <= UMBRAL_MUY_COMPLEJO),
            "funciones": sorted(resultados, key=lambda r: r["complejidad"], reverse=True),
        }
        print(json.dumps(resumen, ensure_ascii=False, indent=2, default=str))
    else:
        imprimir_reporte(resultados, args.top, args.min)


if __name__ == "__main__":
    main()
