#!/usr/bin/env python3
"""Tests de tools/auditor_tests_reloj.py (auto-mejora 19-oct-2026).

Cubren las funciones puras del auditor con directorios temporales: NUNCA se
leen los tests ni las tools reales del lab. El caso que motivó la herramienta
(test con fecha absoluta + main() sin reloj inyectable) está cubierto
explícitamente, junto con su versión sana (main con `ahora`).

Ejecucion:
  cd ~/joko-lab && python3 -m unittest tests.test_auditor_tests_reloj -v
"""

import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

TOOLS_DIR = str(Path(__file__).resolve().parent.parent / "tools")
sys.path.insert(0, TOOLS_DIR)

import auditor_tests_reloj as atr

HOY = date(2026, 10, 19)

TOOL_CON_RELOJ = '''
import datetime


def _ahora():
    return datetime.datetime.now()


def main(argv=None):
    return _ahora()
'''

TOOL_INYECTABLE = '''
import datetime


def main(argv=None, ahora=None):
    return ahora or datetime.datetime.now()
'''

TEST_CADUCABLE = '''
import unittest
from datetime import datetime, timezone

import mitool as mt

AHORA = datetime(2026, 10, 12, 12, 0, tzinfo=timezone.utc)


class T(unittest.TestCase):
    def test_x(self):
        self.assertEqual(mt.main(["--json"]), 0)


if __name__ == "__main__":
    unittest.main()
'''

TEST_SANTO = '''
import unittest

import mitool as mt


class T(unittest.TestCase):
    def test_x(self):
        self.assertEqual(mt.main(["--json"], ahora="2026-10-12"), 0)


if __name__ == "__main__":
    unittest.main()
'''


def _escribir(base: Path, nombre: str, texto: str) -> Path:
    ruta = base / nombre
    ruta.write_text(texto, encoding="utf-8")
    return ruta


class TestCandidatos(unittest.TestCase):
    def test_exacto_prioritario(self):
        with tempfile.TemporaryDirectory() as t:
            tools = [_escribir(Path(t), n, "") for n in ("x.py", "x_kos.py")]
            self.assertEqual([p.name for p in atr._candidatos_tool("x", tools)], ["x.py"])

    def test_prefijo_si_no_hay_exacto(self):
        with tempfile.TemporaryDirectory() as t:
            tools = [_escribir(Path(t), n, "") for n in ("verificar_fk_kos.py", "otra.py")]
            self.assertEqual([p.name for p in atr._candidatos_tool("verificar_fk", tools)],
                             ["verificar_fk_kos.py"])

    def test_sin_pareja(self):
        with tempfile.TemporaryDirectory() as t:
            tools = [_escribir(Path(t), "otra.py", "")]
            self.assertEqual(atr._candidatos_tool("nada", tools), [])


class TestRelojYFirmas(unittest.TestCase):
    def test_reloj_detectado(self):
        self.assertEqual(atr._reloj(TOOL_CON_RELOJ), ["_ahora", "datetime.now"])

    def test_sin_reloj(self):
        self.assertEqual(atr._reloj("def main():\n    return 1\n"), [])

    def test_params_de_main(self):
        nodo = atr._def_main(atr._arbol(TOOL_INYECTABLE))
        self.assertEqual(atr._params(nodo), ["argv", "ahora"])

    def test_sin_def_main(self):
        self.assertIsNone(atr._def_main(atr._arbol("X = 1\n")))


class TestLlamadaYFechas(unittest.TestCase):
    def test_llamada_a_la_tool(self):
        self.assertIsNotNone(atr._llamada_main(atr._arbol(TEST_CADUCABLE)))

    def test_unittest_main_no_cuenta(self):
        self.assertIsNone(atr._llamada_main(atr._arbol('import unittest\nunittest.main()\n')))

    def test_pasa_reloj_por_kwarg(self):
        llamada = atr._llamada_main(atr._arbol(TEST_SANTO))
        self.assertTrue(atr._pasa_reloj(llamada))

    def test_fechas_constructor_y_literal(self):
        arbol = atr._arbol('A = datetime(2026, 10, 12, 12, 0)\nB = "2026-09-01"\n')
        self.assertEqual(atr._fechas_absolutas(arbol), ["2026-09-01", "2026-10-12"])

    def test_fecha_invalida_descartada(self):
        self.assertEqual(atr._fechas_absolutas(atr._arbol("A = datetime(2026, 13, 40)\n")), [])

    def test_edad_dias(self):
        self.assertEqual(atr._edad_dias(["2026-10-12", "2026-10-19"], HOY), (0, 7))
        self.assertEqual(atr._edad_dias([], HOY), (None, None))


class TestEstadoPar(unittest.TestCase):
    def _par(self, texto_test, texto_tool):
        tmp = tempfile.mkdtemp()
        base = Path(tmp)
        test = _escribir(base, "test_mitool.py", texto_test)
        tool = _escribir(base, "mitool.py", texto_tool)
        return test, [tool]

    def test_caducable(self):
        test, tools = self._par(TEST_CADUCABLE, TOOL_CON_RELOJ)
        info = atr._estado_par(test, tools, HOY)
        self.assertEqual(info["estado"], "caducable")
        self.assertEqual(info["edad_max"], 7)

    def test_inyectable_por_firma(self):
        test, tools = self._par(TEST_CADUCABLE, TOOL_INYECTABLE)
        self.assertEqual(atr._estado_par(test, tools, HOY)["estado"], "inyectable")

    def test_inyectable_por_llamada(self):
        test, tools = self._par(TEST_SANTO, TOOL_CON_RELOJ)
        self.assertEqual(atr._estado_par(test, tools, HOY)["estado"], "inyectable")

    def test_riesgo_sin_fechas(self):
        test, tools = self._par(TEST_SANTO.replace(", ahora=\"2026-10-12\"", ""),
                                TOOL_CON_RELOJ)
        self.assertEqual(atr._estado_par(test, tools, HOY)["estado"], "riesgo")


class TestMain(unittest.TestCase):
    def _base(self):
        base = Path(tempfile.mkdtemp())
        (base / "tests").mkdir()
        (base / "tools").mkdir()
        _escribir(base / "tests", "test_mitool.py", TEST_CADUCABLE)
        _escribir(base / "tools", "mitool.py", TOOL_CON_RELOJ)
        return base

    def test_exit_1_con_caducable(self):
        base = self._base()
        self.assertEqual(atr.main(["--tests", str(base / "tests"),
                                   "--tools", str(base / "tools"),
                                   "--hoy", "2026-10-19", "--json"]), 1)

    def test_exit_0_si_la_tool_inyecta(self):
        base = self._base()
        _escribir(base / "tools", "mitool.py", TOOL_INYECTABLE)
        self.assertEqual(atr.main(["--tests", str(base / "tests"),
                                   "--tools", str(base / "tools"),
                                   "--hoy", "2026-10-19"]), 0)

    def test_hoy_inyectado_gana_al_reloj_real(self):
        base = self._base()
        self.assertEqual(atr.main(["--tests", str(base / "tests"),
                                   "--tools", str(base / "tools")], hoy=HOY), 1)


if __name__ == "__main__":
    unittest.main()
