#!/usr/bin/env python3
"""Tests de tools/auditor_tests_entorno.py (herramienta creada 05-oct-2026 en
la sesión semanal de auto-mejora).

Carencia cubierta: la suite del lab llevaba >=6 días con 5 tests rojos sin que
nadie lo detectara, y 4 de ellos eran FALSOS rojos por acoplamiento al TMPDIR
de la sesión Hermes (tempfile respeta TMPDIR y la tool de cobertura de backups
excluye ~/.hermes como ruido).

Estos tests usan SIEMPRE directorios temporales fuera del hogar (/tmp), por la
misma lección que motivó la herramienta: la suite debe ser hermética al TMPDIR.

Ejecución:
  cd ~/joko-lab && python3 -m unittest tests.test_auditor_tests_entorno -v
"""

import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

TOOLS_DIR = str(Path(__file__).resolve().parent.parent / "tools")
sys.path.insert(0, TOOLS_DIR)

import auditor_tests_entorno as ate  # noqa: E402

BASE_TEMPORAL = "/tmp"

# Muestra realista de `unittest discover -v`, con un DeprecationWarning
# intercalado en la línea del resultado (el artefacto medido el 05-oct-2026).
SALIDA_VERBOSE = """\
test_uno (mod.Clase.test_uno) ... ok
test_dos (mod.Clase.test_dos) ... /ruta/search.py:234: DeprecationWarning: table_names() is deprecated
ok
test_tres (mod.Clase.test_tres) ... skipped 'sin deps'
test_cuatro (mod.Clase.test_cuatro) ... FAIL
test_cinco (mod.Clase.test_cinco) ... ERROR
test_seis (mod.Clase.test_seis) ... expected failure
test_siete (mod.Clase.test_siete) ... unexpected success
======================================================================
FAIL: test_cuatro (mod.Clase.test_cuatro)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/ruta/test_mod.py", line 10, in test_cuatro
    self.assertTrue(False)
AssertionError: False is not true

Ran 7 tests in 0.001s
"""

TEST_SINTETICO = '''\
import os
import unittest


class TestSintetico(unittest.TestCase):
    """Test de laboratorio: uno estable y otro que depende del entorno."""

    def test_estable(self):
        self.assertTrue(True)

    def test_dependiente(self):
        self.assertNotIn("hermes", os.environ.get("TMPDIR", ""))
'''


class TestParsearVerbose(unittest.TestCase):
    def setUp(self):
        self.estados = ate.parsear_verbose(SALIDA_VERBOSE)

    def test_reconoce_todos_los_estados(self):
        self.assertEqual(self.estados["mod.Clase.test_uno"], "ok")
        self.assertEqual(self.estados["mod.Clase.test_tres"], "skipped")
        self.assertEqual(self.estados["mod.Clase.test_cuatro"], "fail")
        self.assertEqual(self.estados["mod.Clase.test_cinco"], "error")
        self.assertEqual(self.estados["mod.Clase.test_seis"], "expected failure")
        self.assertEqual(self.estados["mod.Clase.test_siete"], "unexpected success")

    def test_aviso_intercalado_no_se_cuela_como_estado(self):
        estado = self.estados["mod.Clase.test_dos"]
        self.assertNotIn("Deprecation", estado)
        self.assertEqual(estado, ate.ESTADO_DESCONOCIDO)

    def test_traceback_no_crea_tests_fantasma(self):
        self.assertEqual(len(self.estados), 7)
        self.assertFalse(any("Traceback" in k for k in self.estados))

    def test_texto_vacio(self):
        self.assertEqual(ate.parsear_verbose(""), {})


class TestComparar(unittest.TestCase):
    def test_detecta_divergencias_y_ausencias(self):
        a = {"t1": "ok", "t2": "fail", "t3": "ok"}
        b = {"t1": "ok", "t2": "ok", "t4": "ok"}
        self.assertEqual(ate.comparar(a, b),
                         [("t2", "fail", "ok"), ("t3", "ok", "ausente"),
                          ("t4", "ausente", "ok")])

    def test_sin_divergencias(self):
        a = {"t1": "ok", "t2": "fail"}
        self.assertEqual(ate.comparar(a, dict(a)), [])


class TestResumir(unittest.TestCase):
    def test_cuenta_por_estado(self):
        resumen = ate.resumir_estados({"a": "ok", "b": "ok", "c": "fail"})
        self.assertEqual(resumen, {"ok": 2, "fail": 1})

    def test_vacio(self):
        self.assertEqual(ate.resumir_estados({}), {})


class TestInforme(unittest.TestCase):
    def setUp(self):
        self.a = {"mod.C.test_ok": "ok", "mod.C.test_x": "fail"}
        self.b = {"mod.C.test_ok": "ok", "mod.C.test_x": "ok"}

    def test_informe_lista_la_divergencia(self):
        informe = ate.formatear_informe("python3", "/tmp", "/tmp/hermes",
                                        self.a, self.b,
                                        ate.comparar(self.a, self.b))
        self.assertIn("Divergencias (1)", informe)
        self.assertIn("mod.C.test_x", informe)

    def test_informe_sin_divergencias(self):
        informe = ate.formatear_informe("python3", "/tmp", "/tmp/hermes",
                                        self.a, self.a, [])
        self.assertIn("Divergencias (0)", informe)

    def test_resumen_json_serializable(self):
        resumen = ate.resumen_json("python3", "/tmp", "/tmp/hermes",
                                   self.a, self.b, ate.comparar(self.a, self.b))
        texto = json.dumps(resumen, ensure_ascii=False)
        self.assertIn("divergencias", texto)
        self.assertEqual(resumen["n_divergencias"], 1)
        self.assertEqual(resumen["entornos"][0]["estados"]["ok"], 1)


class TestDeteccionEndToEnd(unittest.TestCase):
    """Caso real: la herramienta DEBE detectar un test no hermético al TMPDIR."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(dir=BASE_TEMPORAL)
        self.base = Path(self._tmp.name)
        self.tests = self.base / "tests"
        self.tests.mkdir()
        (self.tests / "test_sintetico.py").write_text(TEST_SINTETICO)
        self.neutro = self.base / "tmp_neutro"
        self.hermes = self.base / "tmp_hermes_like"
        self.neutro.mkdir()
        self.hermes.mkdir()

    def tearDown(self):
        self._tmp.cleanup()

    def _ejecutar(self):
        salida = io.StringIO()
        argv = ["--python", sys.executable, "--tests", str(self.tests),
                "--tmpdir-neutro", str(self.neutro),
                "--tmpdir-hermes", str(self.hermes), "--json"]
        with redirect_stdout(salida):
            codigo = ate.main(argv)
        return codigo, json.loads(salida.getvalue())

    def test_detecta_el_test_dependiente_del_entorno(self):
        codigo, resumen = self._ejecutar()
        self.assertEqual(codigo, 1)
        self.assertEqual(resumen["n_divergencias"], 1)
        self.assertEqual(resumen["divergencias"][0]["test"],
                         "test_sintetico.TestSintetico.test_dependiente")
        self.assertEqual(resumen["divergencias"][0]["neutro"], "ok")
        self.assertEqual(resumen["divergencias"][0]["hermes"], "fail")

    def test_sin_divergencias_cuando_ambos_entornos_coinciden(self):
        salida = io.StringIO()
        argv = ["--python", sys.executable, "--tests", str(self.tests),
                "--tmpdir-neutro", str(self.neutro),
                "--tmpdir-hermes", str(self.neutro), "--json"]
        with redirect_stdout(salida):
            codigo = ate.main(argv)
        self.assertEqual(codigo, 0)
        self.assertEqual(json.loads(salida.getvalue())["n_divergencias"], 0)

    def test_python_inexistente_devuelve_2(self):
        salida = io.StringIO()
        with redirect_stdout(salida), redirect_stderr(io.StringIO()):
            codigo = ate.main(["--python", "/no/existe/python", "--tests",
                               str(self.tests)])
        self.assertEqual(codigo, 2)


class TestNoDejaBasura(unittest.TestCase):
    """La herramienta es SOLO LECTURA: no debe escribir en el árbol de tests.

    Se comprueba sobre un directorio sintético en /tmp (nunca sobre la suite
    del lab: lanzarla desde dentro de sí misma se recursaría).
    """

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(dir=BASE_TEMPORAL)
        self.tests = Path(self._tmp.name) / "tests"
        self.tests.mkdir()
        (self.tests / "test_sintetico.py").write_text(TEST_SINTETICO)

    def tearDown(self):
        self._tmp.cleanup()

    def test_no_crea_ficheros_en_el_directorio_de_tests(self):
        antes = {p.name for p in self.tests.iterdir()}
        with redirect_stdout(io.StringIO()):
            ate.main(["--python", sys.executable, "--tests", str(self.tests),
                      "--tmpdir-neutro", BASE_TEMPORAL,
                      "--tmpdir-hermes", BASE_TEMPORAL])
        self.assertEqual({p.name for p in self.tests.iterdir()}, antes)


if __name__ == "__main__":
    unittest.main()
