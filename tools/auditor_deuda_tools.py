#!/usr/bin/env python3
"""
AUDITOR DE DEUDA DE TOOLS — "¿qué tools del lab tienen deuda y cuánto riesgo hay?"

Responde a UNA pregunta que hasta hoy se contestaba a mano con bucles de shell:
¿qué tools se usan de verdad (cron / scripts / skills / código) y cuáles NO tienen
red (test, complejidad)?

Cruza 4 señales leídas del disco (SOLO LECTURA: no ejecuta ninguna tool):
  1. Uso real: referencias por token exacto en ~/.hermes/cron/jobs.json,
     ~/.hermes/scripts/, los SKILL.md de ~/.hermes/skills y las demás tools/tests.
  2. Red: ¿existe tests/test_<tool>.py (o un test que lo cubra por prefijo)?
  3. Complejidad: máxima y main() vía tools/complejidad_crap.py (analizar_dir).
  4. Resumen agregado: cuántas tools usadas por automatización están sin test.

Score de riesgo (fórmula transparente, no opinión):
  score = 3*refs_cron + 2*refs_scripts + 1*refs_skills + 4*(SIN test) + 2*(main() > 10)
Las 4 señales se imprimen por separado, así que el score se puede auditar.

Límite conocido: la referencia es por TOKEN exacto (no por ruta), así que una
palabra en prosa que coincida con el nombre de una tool cuenta como mención.

Uso:
  python3 tools/auditor_deuda_tools.py                 # informe completo
  python3 tools/auditor_deuda_tools.py --top 15        # solo el top 15
  python3 tools/auditor_deuda_tools.py --tool search   # detalle de una tool
  python3 tools/auditor_deuda_tools.py --json          # salida máquina
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

LAB = Path(os.path.expanduser("~/joko-lab"))
TOOLS = LAB / "tools"
TESTS = LAB / "tests"
HERMES = Path(os.path.expanduser("~/.hermes"))
CRON_JOBS = HERMES / "cron" / "jobs.json"
SCRIPTS = HERMES / "scripts"
SKILLS = HERMES / "skills"

sys.path.insert(0, str(TOOLS))

# Pesos del score (constantes para poder re-auditar la fórmula)
PESO_CRON = 3
PESO_SCRIPT = 2
PESO_SKILL = 1
PESO_SIN_TEST = 4
PESO_MAIN_COMPLEJO = 2
UMBRAL_MAIN = 10
MAX_BYTES = 3_000_000

_TOKEN = re.compile(r"[A-Za-z_][\w-]*")
PROPIA = "auditor_deuda_tools"


def _nombres_tools(tools_dir: Path = TOOLS) -> list:
    """Nombres (sin .py) de las tools del lab, sin la propia auditora."""
    return sorted(f.stem for f in tools_dir.glob("*.py") if f.stem != PROPIA)


def _stems_tests(tests_dir: Path = TESTS) -> set:
    """Stems de tests/test_*.py (sin el prefijo 'test_')."""
    if not tests_dir.exists():
        return set()
    return {t.stem[len("test_"):] for t in tests_dir.glob("test_*.py")}


def _tiene_test(nombre: str, stems: set) -> bool:
    """¿Hay test del nombre, o un test que lo cubra por prefijo en cualquier lado?"""
    return any(s == nombre or s.startswith(nombre) or nombre.startswith(s) for s in stems)


def _complejidades(tools_dir: Path = TOOLS) -> dict:
    """{archivo.py: {'max': N, 'main': N}} usando el analizador del lab."""
    import complejidad_crap as cc

    por_archivo = {}
    for r in cc.analizar_dir(tools_dir):
        d = por_archivo.setdefault(Path(r["archivo"]).name, {"max": 0, "main": 0})
        d["max"] = max(d["max"], r["complejidad"])
        if r["funcion"] == "main":
            d["main"] = max(d["main"], r["complejidad"])
    return por_archivo


def _fuentes() -> dict:
    """{categoría: [Path]} a escanear (una lectura por fichero)."""
    herramientas = [f for f in TOOLS.glob("*.py") if f.stem != PROPIA]

    def _propios(d):
        if not d.exists():
            return []
        return [f for f in sorted(d.glob("*.py")) + sorted(d.glob("*.sh"))
                if "archived" not in f.parts and "backups" not in f.parts]

    return {
        "cron": [CRON_JOBS] if CRON_JOBS.exists() else [],
        "script": _propios(SCRIPTS),
        "skill": sorted(SKILLS.rglob("SKILL.md")) if SKILLS.exists() else [],
        "codigo": herramientas + sorted(TESTS.glob("*.py")),
    }


def _contar_refs(fuentes: dict, nombres: set) -> dict:
    """{nombre: {categoria: nº de ficheros que lo mencionan}} (1 lectura por fichero)."""
    refs = {n: {"cron": 0, "script": 0, "skill": 0, "codigo": 0} for n in nombres}
    for categoria, ficheros in fuentes.items():
        for f in ficheros:
            try:
                if f.stat().st_size > MAX_BYTES:
                    continue
                tokens = set(_TOKEN.findall(f.read_text(errors="ignore")))
            except Exception:
                continue
            for n in nombres & tokens:
                refs[n][categoria] += 1
    return refs


def _score(refs: dict, tiene_test: bool, main: int) -> int:
    """Score de riesgo: uso real + falta de red. Ver docstring del módulo."""
    return (PESO_CRON * refs["cron"] + PESO_SCRIPT * refs["script"]
            + PESO_SKILL * refs["skill"]
            + (0 if tiene_test else PESO_SIN_TEST)
            + (PESO_MAIN_COMPLEJO if main > UMBRAL_MAIN else 0))


def _fila(nombre: str, refs: dict, tiene_test: bool, compl: dict) -> dict:
    """Ficha de una tool con sus 4 señales y el score."""
    c = compl.get(f"{nombre}.py", {"max": 0, "main": 0})
    en_auto = refs["cron"] + refs["script"]
    return {
        "nombre": nombre, "refs": refs, "test": tiene_test,
        "max": c["max"], "main": c["main"], "en_automatizacion": en_auto > 0,
        "score": _score(refs, tiene_test, c["main"]),
    }


def _filas(nombres: list, refs: dict, stems: set, compl: dict) -> list:
    """Todas las fichas, ordenadas por riesgo descendente."""
    filas = [_fila(n, refs[n], _tiene_test(n, stems), compl) for n in nombres]
    filas.sort(key=lambda r: (-r["score"], r["nombre"]))
    return filas


def _formatear_fila(r: dict) -> str:
    """Línea fija para el ranking."""
    red = "OK " if r["test"] else "NO "
    return (f"  {r['score']:>3}  {r['nombre']:<28} {r['refs']['cron']:>2}/{r['refs']['script']:>2}/"
            f"{r['refs']['skill']:>3}/{r['refs']['codigo']:>3}  test={red} "
            f"main={r['main']:>2} max={r['max']:>3}")


def _tabla(filas: list, top: int, titulo: str) -> list:
    """Bloque de tabla con cabecera."""
    lineas = [f"## {titulo}", "",
              "  score  tool                         c/s/S/C   test   complejidad", "-" * 74]
    lineas += [_formatear_fila(r) for r in filas[:top]]
    lineas.append("")
    return lineas


def _sin_red(filas: list, solo_auto: bool = True) -> list:
    """Tools sin test (por defecto, solo las usadas por automatización)."""
    return [r for r in filas if not r["test"] and (r["en_automatizacion"] or not solo_auto)]


def _resumen(filas: list) -> list:
    """Bloque de agregados + la lista crítica (automatización sin test)."""
    sin_test = [r for r in filas if not r["test"]]
    criticas = _sin_red(filas)
    complejas = [r for r in filas if r["max"] > UMBRAL_MAIN]
    lineas = ["## 📊 Agregados", "",
              f"- Tools medidas: {len(filas)}",
              f"- Sin test: {len(sin_test)} · con test: {len(filas) - len(sin_test)}",
              f"- Usadas por automatización (cron/scripts): "
              f"{len([r for r in filas if r['en_automatizacion']])}",
              f"- 🔴 Usadas por automatización y SIN test: {len(criticas)}",
              f"- Complejidad >10 (alguna función): {len(complejas)}", ""]
    if criticas:
        lineas += _tabla(criticas, len(criticas),
                         "🔴 Críticas: automatización SIN red de test")
    return lineas


def _detalle(fila: dict, stem_match: list) -> str:
    """Informe de una sola tool."""
    r = fila["refs"]
    return "\n".join([
        f"# 🔎 {fila['nombre']}",
        "",
        f"- Referencias cron: {r['cron']} · scripts: {r['script']} · skills: {r['skill']} · código: {r['codigo']}",
        f"- Test: {'sí' if fila['test'] else 'NO'} "
        f"{', '.join(stem_match) if stem_match else '(ningún test lo cubre)'}",
        f"- Complejidad main(): {fila['main']} · máxima: {fila['max']}",
        f"- Score: {fila['score']}",
        "",
        "Checklist antes de tocarla: backup (RULE-008) + `tools/pipeline_inspector.py "
        f"tools/{fila['nombre']}.py` + `tools/regression_guardian.py --archivo tools/{fila['nombre']}.py`.",
    ])


def _informe(filas: list, top: int) -> str:
    """Informe completo: ranking + agregados."""
    lineas = ["# 🧾 AUDITOR DE DEUDA DE TOOLS (lab)",
              "",
              f"Fórmula: score = {PESO_CRON}*cron + {PESO_SCRIPT}*scripts + {PESO_SKILL}*skills "
              f"+ {PESO_SIN_TEST}*(sin test) + {PESO_MAIN_COMPLEJO}*(main>{UMBRAL_MAIN})",
              "Columnas c/s/S/C = referencias en cron / scripts / skills / código.",
              ""]
    lineas += _tabla(filas, top, "🏆 Ranking de riesgo")
    lineas += _resumen(filas)
    return "\n".join(lineas)


def _args() -> argparse.Namespace:
    """Argumentos de línea de comandos."""
    p = argparse.ArgumentParser(description="Auditor de deuda de las tools del lab")
    p.add_argument("--top", type=int, default=20, help="Filas del ranking (default 20)")
    p.add_argument("--tool", default=None, help="Detalle de una tool concreta")
    p.add_argument("--json", action="store_true", help="Salida JSON")
    return p.parse_args()


def main() -> int:
    args = _args()
    nombres = _nombres_tools()
    stems = _stems_tests()
    refs = _contar_refs(_fuentes(), set(nombres))
    filas = _filas(nombres, refs, stems, _complejidades())

    if args.tool:
        objetivo = [f for f in filas if f["nombre"] == args.tool]
        if not objetivo:
            print(f"Tool no encontrada: {args.tool}", file=sys.stderr)
            return 2
        print(_detalle(objetivo[0], sorted(s for s in stems if _tiene_test(args.tool, {s}))))
        return 0
    if args.json:
        print(json.dumps(filas, ensure_ascii=False, indent=2))
        return 0
    print(_informe(filas, args.top))
    return 0


if __name__ == "__main__":
    sys.exit(main())
