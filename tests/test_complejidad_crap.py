#!/usr/bin/env python3
"""Tests de tools/complejidad_crap.py — el INSTRUMENTO de la métrica del lab.

Motivo (RULE-015: validar el instrumento antes de confiar en su cifra): el
informe semanal de auto-mejora decide qué funciones refactorizar con la salida
de esta tool, y hasta hoy no tenía ninguna red. Detectado y fijado aquí el
defecto de medición real: `ast.walk` descendía a las funciones ANIDADAS y
atribuía sus decisiones al padre (21 funciones infladas en tools/, hasta +10).

Cubren: puntos de decisión McCabe (if/elif, bucles, except, assert, and/or,
ternario, comprehensions, match), NO inflación por anidamiento, forma de las
filas de `analizar_archivo`, umbrales, agregados y los modos de `main()`.
"""

import ast
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import complejidad_crap as cc  # noqa: E402


def _funcion(codigo: str):
    """Devuelve el nodo de la primera función de un fragmento de código."""
    arbol = ast.parse(codigo.strip())
    return arbol.body[0]


def _complejidad(codigo: str) -> int:
    return cc.complejidad_funcion(_funcion(codigo))


class TestPuntosDeDecision(unittest.TestCase):
    def test_funcion_sin_ramas_es_1(self):
        self.assertEqual(_complejidad("def f():\n    return 1"), 1)

    def test_if_suma_uno(self):
        self.assertEqual(_complejidad("def f(x):\n    if x:\n        return 1\n    return 0"), 2)

    def test_if_elif_else_suma_dos(self):
        codigo = """
def f(x):
    if x == 1:
        return "a"
    elif x == 2:
        return "b"
    else:
        return "c"
"""
        self.assertEqual(_complejidad(codigo), 3)

    def test_bucles_for_y_while(self):
        codigo = """
def f(xs):
    for x in xs:
        while x:
            x -= 1
    return xs
"""
        self.assertEqual(_complejidad(codigo), 3)

    def test_except_handler(self):
        codigo = """
def f():
    try:
        return 1
    except ValueError:
        return 2
"""
        self.assertEqual(_complejidad(codigo), 2)

    def test_boolop_and_anidado(self):
        # `a and b and c` = 3 valores -> 2 puntos de decisión
        self.assertEqual(_complejidad("def f(a, b, c):\n    return a and b and c"), 3)

    def test_ternario_ifexp(self):
        self.assertEqual(_complejidad("def f(x):\n    return 1 if x else 2"), 2)

    def test_assert(self):
        self.assertEqual(_complejidad("def f(x):\n    assert x\n    return x"), 2)

    def test_comprehension_con_dos_ifs(self):
        codigo = "def f(xs):\n    return [x for x in xs if x if x > 2]"
        self.assertEqual(_complejidad(codigo), 3)

    def test_no_cuenta_llamadas_ni_asignaciones(self):
        codigo = """
def f(x):
    y = x + 1
    z = sorted([y], reverse=True)
    return z
"""
        self.assertEqual(_complejidad(codigo), 1)


@unittest.skipUnless(sys.version_info >= (3, 10), "match requiere Python 3.10+")
class TestMatch(unittest.TestCase):
    def test_match_cuenta_por_caso(self):
        # Un `match` con 3 casos son 3 caminos, no 1 (radon cuenta los casos).
        codigo = """
def f(x):
    match x:
        case 1:
            return "uno"
        case 2:
            return "dos"
        case _:
            return "otros"
"""
        self.assertEqual(_complejidad(codigo), 4)

    def test_match_de_un_caso_suma_uno(self):
        codigo = "def f(x):\n    match x:\n        case 1:\n            return 'uno'\n    return 'otros'"
        self.assertEqual(_complejidad(codigo), 2)


class TestAnidamiento(unittest.TestCase):
    """El defecto medido: las decisiones de un def anidado NO son del padre."""

    def test_def_anidado_no_infla_al_padre(self):
        codigo = """
def outer(x):
    if x:
        x = 2

    def inner(y):
        if y:
            return 1
        for i in range(3):
            if i:
                return 2
        return 0

    return inner(x)
"""
        self.assertEqual(_complejidad(codigo), 2)

    def test_def_anidado_conserva_su_propia_complejidad(self):
        codigo = """
def outer():
    def inner(y):
        if y:
            return 1
        return 0

    return inner(1)
"""
        arbol = ast.parse(codigo.strip())
        anidadas = [n for n in ast.walk(arbol)
                    if isinstance(n, ast.FunctionDef) and n.name == "inner"]
        self.assertEqual(len(anidadas), 1)
        self.assertEqual(cc.complejidad_funcion(anidadas[0]), 2)

    def test_metodo_de_clase_no_infla_al_padre(self):
        codigo = """
def f(x):
    class Local:
        def metodo(self, y):
            if y:
                return 1
            return 0

    return Local()
"""
        self.assertEqual(_complejidad(codigo), 1)

    def test_lambda_con_ternario_suma_al_padre(self):
        # Un lambda no se reporta como función propia: sus decisiones quedan
        # atribuidas a quien lo contiene (comportamiento documentado).
        self.assertEqual(_complejidad("def f(xs):\n    return sorted(xs, key=lambda v: 0 if v else 1)"), 2)


class TestAnalizarArchivo(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def _escribir(self, nombre: str, contenido: str) -> Path:
        ruta = self.dir / nombre
        ruta.write_text(contenido, encoding="utf-8")
        return ruta

    def test_filas_con_claves_canonicas(self):
        ruta = self._escribir("a.py", "def f(x):\n    if x:\n        return 1\n    return 0\n")
        filas = cc.analizar_archivo(ruta)
        self.assertEqual(len(filas), 1)
        self.assertEqual(set(filas[0]), {"archivo", "funcion", "complejidad", "linea"})
        self.assertEqual(filas[0]["funcion"], "f")
        self.assertEqual(filas[0]["complejidad"], 2)
        self.assertEqual(filas[0]["linea"], 1)

    def test_padre_e_hija_se_reportan_por_separado(self):
        ruta = self._escribir("b.py", (
            "def outer():\n"
            "    def inner(y):\n"
            "        if y:\n"
            "            return 1\n"
            "        return 0\n"
            "    return inner(1)\n"
        ))
        por_nombre = {f["funcion"]: f["complejidad"] for f in cc.analizar_archivo(ruta)}
        self.assertEqual(por_nombre["outer"], 1)
        self.assertEqual(por_nombre["inner"], 2)

    def test_metodo_de_clase_es_fila_propia(self):
        ruta = self._escribir("c.py", "class A:\n    def m(self, x):\n        if x:\n            return 1\n        return 0\n")
        filas = cc.analizar_archivo(ruta)
        self.assertEqual([f["funcion"] for f in filas], ["m"])
        self.assertEqual(filas[0]["complejidad"], 2)

    def test_syntaxerror_devuelve_fila_negativa(self):
        ruta = self._escribir("roto.py", "def f(:\n    pass\n")
        filas = cc.analizar_archivo(ruta)
        self.assertEqual(len(filas), 1)
        self.assertEqual(filas[0]["complejidad"], -1)
        self.assertTrue(filas[0]["funcion"].startswith("<SyntaxError"))
        self.assertGreater(filas[0]["linea"], 0)

    def test_async_def_se_analiza(self):
        ruta = self._escribir("d.py", "async def f(x):\n    if x:\n        return 1\n    return 0\n")
        filas = cc.analizar_archivo(ruta)
        self.assertEqual(filas[0]["funcion"], "f")
        self.assertEqual(filas[0]["complejidad"], 2)


class TestAnalizarDir(unittest.TestCase):
    def test_solo_py_y_ordenado(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            (d / "b.py").write_text("def f():\n    return 1\n", encoding="utf-8")
            (d / "a.py").write_text("def g():\n    return 1\n", encoding="utf-8")
            (d / "notas.txt").write_text("def h():\n    pass\n", encoding="utf-8")
            (d / "sub").mkdir()
            (d / "sub" / "c.py").write_text("def i():\n    return 1\n", encoding="utf-8")
            nombres = [f["funcion"] for f in cc.analizar_dir(d)]
            self.assertEqual(nombres, ["g", "f"])  # orden por nombre de archivo


class TestUmbralesYFormato(unittest.TestCase):
    def test_marca_limites(self):
        self.assertEqual(cc._marca(1), "🟢")
        self.assertEqual(cc._marca(10), "🟢")
        self.assertEqual(cc._marca(11), "🟠")
        self.assertEqual(cc._marca(20), "🟠")
        self.assertEqual(cc._marca(21), "🔴")

    def test_contar_categorias(self):
        filas = [{"complejidad": c} for c in (1, 10, 11, 20, 21, 50)]
        self.assertEqual(cc._contar_categorias(filas), (2, 2))

    def test_formatear_funcion(self):
        fila = {"archivo": "/tmp/x/tool.py", "funcion": "f", "complejidad": 12, "linea": 7}
        self.assertEqual(cc._formatear_funcion(fila), "🟠  12  tool.py:7 f()")


class TestMain(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        (self.dir / "t.py").write_text(
            "def simple():\n    return 1\n"
            "def media(x):\n    if x:\n        return 1\n    return 0\n"
            "def grande(xs):\n"
            + "".join(f"    if xs == {i}:\n        return {i}\n" for i in range(12))
            + "    return -1\n",
            encoding="utf-8",
        )

    def tearDown(self):
        self.tmp.cleanup()

    def _main(self, *args):
        argv = sys.argv
        sys.argv = ["complejidad_crap.py", str(self.dir), *args]
        buf = io.StringIO()
        try:
            with redirect_stdout(buf):
                cc.main()
        finally:
            sys.argv = argv
        return buf.getvalue()

    def test_json_resumen_y_orden(self):
        datos = json.loads(self._main("--json"))
        self.assertEqual(datos["total_funciones"], 3)
        self.assertEqual(datos["muy_complejas"], 0)
        self.assertEqual(datos["complejas"], 1)  # `grande` = 1 + 12 ifs = 13
        self.assertEqual(datos["funciones"][0]["funcion"], "grande")
        self.assertEqual(datos["funciones"][0]["complejidad"], 13)

    def test_texto_min_filtra(self):
        salida = self._main("--min", "11")
        self.assertIn("grande()", salida)
        self.assertNotIn("media()", salida)

    def test_texto_top_limita(self):
        salida = self._main("--top", "1")
        self.assertIn("grande()", salida)
        self.assertNotIn("media()", salida)

    def test_texto_cabecera_con_totales(self):
        salida = self._main()
        self.assertIn("Total funciones: 3", salida)
        self.assertIn("complejas (11-20): 1", salida)
        self.assertIn("muy complejas (>20): 0", salida)

    def test_directorio_inexistente_exit_1(self):
        argv = sys.argv
        sys.argv = ["complejidad_crap.py", str(self.dir / "no_existe")]
        try:
            with redirect_stdout(io.StringIO()):
                with self.assertRaises(SystemExit) as ctx:
                    cc.main()
            self.assertEqual(ctx.exception.code, 1)
        finally:
            sys.argv = argv


if __name__ == "__main__":
    unittest.main()
