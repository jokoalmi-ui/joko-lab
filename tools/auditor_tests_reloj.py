#!/usr/bin/env python3
"""AUDITOR DE TESTS QUE CADUCAN CON EL RELOJ — "¿algún test depende de 'hoy'?"

Carencia que resuelve (medida el 19-oct-2026, sesión semanal de auto-mejora):
  la suite del lab estaba ROJA (379 tests, 1 failure) y el rojo no era del
  código: `test_auditar_crons.test_main_exit_0_base_limpia` construía el
  fixture con `AHORA = datetime(2026, 10, 12, 12, 0)` y llamaba a
  `ac.main(["--json"])`, que usa el reloj REAL (`_ahora()`). El 12-oct el job
  sintético estaba "2 h en el futuro" y el test pasaba; el 19-oct ese mismo
  fixture llevaba 165 h vencido y el auditor —correctamente— devolvía exit 1.
  Resultado: un test que se rompe solo con el paso del tiempo, indistinguible
  de una regresión real si no se investiga el origen.

Qué hace (SOLO LECTURA; no ejecuta la suite, no modifica nada):
  Empareja cada `tests/test_<X>.py` con su(s) `tools/<X>.py` y busca la
  combinación que caduca, con AST (no con regex de texto, para no confundir
  un `main(` dentro de un docstring con una llamada real):
    (a) el test fija una FECHA ABSOLUTA (datetime(Y, M, D) o "YYYY-MM-DD"),
    (b) la tool emparejada lee el reloj real (`_ahora()`, datetime.now(),
        date.today(), time.time()),
    (c) el test LLAMA a `main(` y esa `def main` no acepta el reloj como
        parámetro (ni el test se lo pasa por keyword).
  (a)+(b)+(c) -> 🔴 CADUCABLE: el test cambiará de resultado sin que cambie
  el código. Sin fechas absolutas -> 🟡 (vigilar: el fixture puede ser
  relativo). Reloj inyectable o pasado por el test -> 🟢.

Uso:
  python3 tools/auditor_tests_reloj.py                  # informe legible
  python3 tools/auditor_tests_reloj.py --json           # JSON (crons)
  python3 tools/auditor_tests_reloj.py --dias 30        # umbral de antigüedad
  python3 tools/auditor_tests_reloj.py --hoy 2026-10-19 # reloj inyectado
  python3 tools/auditor_tests_reloj.py --tests <dir> --tools <dir>

Código de salida: 0 = ningún test caducable, 1 = hay 🔴, 2 = error de uso.

Relación con las otras herramientas del ciclo:
  - auditor_tests_entorno.py: hermeticidad frente al ENTORNO (TMPDIR).
  - auditor_tests_reloj.py:   hermeticidad frente al TIEMPO (reloj real).
  Misma familia de fallo: una red de test que cambia de resultado sin que
  cambie el código deja de ser red.
"""

import argparse
import ast
import json
import re
from datetime import date
from pathlib import Path

LAB = Path.home() / "joko-lab"
DIR_TESTS_DEFECTO = LAB / "tests"
DIR_TOOLS_DEFECTO = LAB / "tools"
DIAS_DEFECTO = 30

# Llamadas al reloj real dentro de una tool (texto: barato y suficiente).
RE_RELOJ = re.compile(r"\b(_ahora|datetime\.now|datetime\.utcnow|date\.today|time\.time)\s*\(")

# Fecha ISO suelta en un literal de cadena.
RE_FECHA_STR = re.compile(r"^(20\d{2})-(\d{2})-(\d{2})")

# Nombres de parámetro que hacen inyectable el reloj de un entry point.
PARAMS_RELOJ = ("ahora", "now", "hoy", "fecha_ref", "ref")

# Módulos/alias cuya llamada .now()/.today()/.time() es el RELOJ real
# (excluye falsos como datetime.min.time(), medido el 19-oct-2026).
BASES_RELOJ = ("datetime", "date", "time", "_dt", "dt", "_time", "_date")


def _leer(ruta: Path) -> str:
    """Lee un fichero de texto tolerantemente ('' si no se puede)."""
    try:
        return ruta.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def _arbol(texto: str):
    """AST del fuente, o None si no compila."""
    try:
        return ast.parse(texto)
    except SyntaxError:
        return None


def _candidatos_tool(stem: str, tools: list) -> list:
    """Empareja test_<stem> con tools cuyo nombre coincida, sea prefijo o lo contenga."""
    exactos = [t for t in tools if t.stem == stem]
    if exactos:
        return exactos
    return [t for t in tools if stem.startswith(t.stem) or t.stem.startswith(stem)]


def _pares(dir_tests: Path, dir_tools: Path) -> list:
    """Devuelve [(test, [tools emparejadas])] para cada test_*.py."""
    tools = sorted(p for p in dir_tools.glob("*.py") if not p.name.startswith("_"))
    return [(test, _candidatos_tool(test.stem[len("test_"):], tools))
            for test in sorted(dir_tests.glob("test_*.py"))]


def _cadena(nodo) -> str:
    """Nombre punteado de un nodo (Name -> 'x', Attribute -> 'a.b.c')."""
    if isinstance(nodo, ast.Name):
        return nodo.id
    if isinstance(nodo, ast.Attribute):
        return _cadena(nodo.value) + "." + nodo.attr
    return ""


def _reloj(texto: str) -> list:
    """Llamadas al reloj real en la tool (AST: no cuenta docstrings/comentarios)."""
    arbol = _arbol(texto)
    if arbol is None:
        return sorted({m.group(1) for m in RE_RELOJ.finditer(texto)})
    hallados = set()
    for nodo in ast.walk(arbol):
        if not isinstance(nodo, ast.Call):
            continue
        f = nodo.func
        if isinstance(f, ast.Name) and f.id == "_ahora":
            hallados.add("_ahora")
        elif isinstance(f, ast.Attribute) and f.attr in ("now", "utcnow", "today", "time"):
            partes = _cadena(f).split(".")
            if len(partes) >= 2 and partes[-2] in BASES_RELOJ:
                hallados.add(".".join(partes[-2:]))
    return sorted(hallados)


def _def_main(arbol):
    """Nodo FunctionDef de main (el primero), o None."""
    if arbol is None:
        return None
    for nodo in ast.walk(arbol):
        if isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef)) and nodo.name == "main":
            return nodo
    return None


def _params(nodo) -> list:
    """Lista de nombres de parámetros de una FunctionDef."""
    a = nodo.args
    return [x.arg for x in list(a.posonlyargs) + list(a.args) + list(a.kwonlyargs)]


def _llamada_main(arbol):
    """Nodo Call que invoca el main de la tool dentro del test, o None.

    Se excluye `unittest.main()` (el runner del propio test) — sin este filtro
    TODO test con `if __name__ == "__main__"` parecía invocar a la tool
    (falso positivo medido en la primera pasada del 19-oct-2026).
    """
    if arbol is None:
        return None
    for nodo in ast.walk(arbol):
        if not isinstance(nodo, ast.Call):
            continue
        f = nodo.func
        if isinstance(f, ast.Attribute) and f.attr == "main":
            base = f.value
            if isinstance(base, ast.Name) and base.id == "unittest":
                continue
            return nodo
    return None


def _pasa_reloj(llamada) -> bool:
    """True si la llamada pasa el reloj por keyword (main(..., ahora=X))."""
    if llamada is None:
        return False
    return any(k.arg in PARAMS_RELOJ for k in llamada.keywords if k.arg)


def _es_constructor_datetime(nodo) -> bool:
    """True si el nodo es `datetime` suelto o `datetime.datetime` (import directo)."""
    if isinstance(nodo, ast.Name):
        return nodo.id == "datetime"
    return isinstance(nodo, ast.Attribute) and nodo.attr == "datetime"


def _iso_valida(y: int, mes: int, d: int):
    """Fecha ISO 'YYYY-MM-DD' si los tres enteros forman una fecha plausible."""
    if 2000 < y < 2100 and 1 <= mes <= 12 and 1 <= d <= 31:
        return "%04d-%02d-%02d" % (y, mes, d)
    return None


def _fecha_de_constructor(nodo):
    """Fecha de un Call datetime(Y, M, D) (import directo o datetime.datetime)."""
    if not isinstance(nodo, ast.Call) or not _es_constructor_datetime(nodo.func) \
            or len(nodo.args) < 3:
        return None
    consts = [a.value for a in nodo.args[:3]
              if isinstance(a, ast.Constant) and isinstance(a.value, int)
              and not isinstance(a.value, bool)]
    return _iso_valida(*consts) if len(consts) == 3 else None


def _fecha_de_literal(nodo):
    """Fecha de un literal ISO 'YYYY-MM-DD...' (nombres de informe, fixtures)."""
    if isinstance(nodo, ast.Constant) and isinstance(nodo.value, str):
        m = RE_FECHA_STR.match(nodo.value)
        return "-".join(m.groups()) if m else None
    return None


def _fechas_absolutas(arbol) -> list:
    """Fechas ISO absolutas fijadas en el test (constructor o literal)."""
    if arbol is None:
        return []
    fechas = {_fecha_de_constructor(n) for n in ast.walk(arbol)}
    fechas |= {_fecha_de_literal(n) for n in ast.walk(arbol)}
    fechas.discard(None)
    return sorted(f for f in fechas if f)


def _edad_dias(fechas: list, hoy: date) -> tuple:
    """(min, max) de días de antigüedad de las fechas; (None, None) si vacío."""
    edades = []
    for iso in fechas:
        try:
            edades.append((hoy - date.fromisoformat(iso)).days)
        except ValueError:
            continue
    return (min(edades), max(edades)) if edades else (None, None)


def _estado_par(test: Path, tools: list, hoy: date) -> dict:
    """Clasifica un par test<->tool en caducable / riesgo / inyectable."""
    texto_test = _leer(test)
    arbol_test = _arbol(texto_test)
    fechas = _fechas_absolutas(arbol_test)
    llamada = _llamada_main(arbol_test)
    pasa = _pasa_reloj(llamada)
    info = {"test": str(test), "tools": [t.name for t in tools], "llamada_main": llamada is not None,
            "pasa_reloj": pasa, "fechas": fechas, "reloj": [], "firma_main": "",
            "edad_min": None, "edad_max": None, "estado": "sin-reloj"}
    for tool in tools:
        reloj = _reloj(_leer(tool))
        if not reloj:
            continue
        nodo_main = _def_main(_arbol(_leer(tool)))
        params = _params(nodo_main) if nodo_main else []
        inyectable = not nodo_main or any(p in PARAMS_RELOJ for p in params)
        info["reloj"].extend(reloj)
        info["firma_main"] = ", ".join(params) if nodo_main else "sin def main"
        if inyectable or pasa:
            info["estado"] = "inyectable"
            break
        info["estado"] = "caducable" if (llamada is not None and fechas) else "riesgo"
    info["edad_min"], info["edad_max"] = _edad_dias(fechas, hoy)
    info["reloj"] = sorted(set(info["reloj"]))
    return info


def _analizar(pares: list, hoy: date) -> list:
    """Analiza los pares con reloj y los ordena por gravedad."""
    informes = []
    for test, tools in pares:
        if not tools:
            continue
        info = _estado_par(test, tools, hoy)
        if info["estado"] != "sin-reloj":
            informes.append(info)
    orden = {"caducable": 0, "riesgo": 1, "inyectable": 2}
    return sorted(informes, key=lambda i: (orden.get(i["estado"], 9), i["test"]))


def _detalle(info: dict) -> str:
    """Una línea de detalle por test: reloj, firma y antigüedad del fixture."""
    partes = ["reloj: " + ", ".join(info["reloj"]),
              "main(%s)" % info["firma_main"],
              "invoca main: %s" % ("sí" if info["llamada_main"] else "no")]
    if info["fechas"]:
        partes.append("fechas fijas: %d (antigüedad %s..%s d)"
                      % (len(info["fechas"]), info["edad_min"], info["edad_max"]))
    return " · ".join(partes)


def _formatear(informes: list, dias: int, hoy: date) -> str:
    """Informe legible agrupado por estado."""
    lineas = ["# ⏰ AUDITOR DE TESTS DEPENDIENTES DEL RELOJ", "",
              "Reloj de referencia: %s · umbral: %d días" % (hoy.isoformat(), dias),
              "Criterio 🔴: fecha absoluta en el test + tool que lee el reloj real + main() sin reloj inyectable.", ""]
    if not informes:
        return "\n".join(lineas + ["✅ Ningún test emparejado con una tool que lea el reloj."])
    for estado, titulo in (("caducable", "🔴 CADUCABLES (cambiarán de resultado sin cambiar el código)"),
                           ("riesgo", "🟡 EN RIESGO (reloj real sin fechas absolutas: vigilar)"),
                           ("inyectable", "🟢 SANOS (reloj inyectable o el test lo pasa)")):
        grupo = [i for i in informes if i["estado"] == estado]
        if not grupo:
            continue
        lineas += ["## %s" % titulo, ""]
        for info in grupo:
            lineas.append("- %s %s" % ("🔴" if estado == "caducable" else
                                       "🟡" if estado == "riesgo" else "🟢", Path(info["test"]).name))
            lineas.append("    tools: %s" % ", ".join(info["tools"]))
            lineas.append("    %s" % _detalle(info))
        lineas.append("")
    caducables = sum(1 for i in informes if i["estado"] == "caducable")
    lineas.append("Salida: exit 1 = hay %d test(s) caducable(s), exit 0 = silencio." % caducables)
    return "\n".join(lineas)


def _json(informes: list, dias: int, hoy: date) -> str:
    """Resumen JSON estable (sin volcados del fuente)."""
    return json.dumps({"fecha": hoy.isoformat(), "dias": dias, "total": len(informes),
                       "por_estado": {e: sum(1 for i in informes if i["estado"] == e)
                                      for e in ("caducable", "riesgo", "inyectable")},
                       "tests": informes}, ensure_ascii=False, indent=2)


def main(argv=None, hoy: date | None = None) -> int:
    ap = argparse.ArgumentParser(description="Auditor de tests que caducan con el reloj (solo lectura).")
    ap.add_argument("--tests", default=str(DIR_TESTS_DEFECTO), help="directorio de tests")
    ap.add_argument("--tools", default=str(DIR_TOOLS_DEFECTO), help="directorio de tools")
    ap.add_argument("--dias", type=int, default=DIAS_DEFECTO, help="umbral de antigüedad (informativo)")
    ap.add_argument("--hoy", default=None, help="fecha de referencia YYYY-MM-DD (pruebas)")
    ap.add_argument("--json", action="store_true", help="salida JSON")
    args = ap.parse_args(argv)
    hoy = hoy or (date.fromisoformat(args.hoy) if args.hoy else date.today())
    informes = _analizar(_pares(Path(args.tests), Path(args.tools)), hoy)
    print(_json(informes, args.dias, hoy) if args.json else _formatear(informes, args.dias, hoy))
    return 1 if any(i["estado"] == "caducable" for i in informes) else 0


if __name__ == "__main__":
    raise SystemExit(main())
