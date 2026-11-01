#!/usr/bin/env python3
"""Tests de tools/captura_referencia.py (red de seguridad del ciclo de refactor).

Cubren: normalización de partes volátiles (pitfall 21), resolución segura de la
tool objetivo, huella, ejecución, diff (salida y exit), y la negativa a
sobrescribir una referencia existente (pitfall 33).
"""

import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import captura_referencia as cr  # noqa: E402


class TestNormalizar(unittest.TestCase):
    def test_timestamp_iso_completo(self):
        self.assertEqual(
            cr._normalizar("inicio 2026-10-26 13:00:50 fin"), "inicio <TS> fin"
        )

    def test_timestamp_con_t_y_milisegundos(self):
        self.assertEqual(cr._normalizar("ts=2026-10-26T13:00:50.123"), "ts=<TS>")

    def test_hora_suelta(self):
        self.assertEqual(cr._normalizar("corrida a las 09:41:07 ok"), "corrida a las <HORA> ok")

    def test_ruta_temporal(self):
        self.assertEqual(
            cr._normalizar("usando /tmp/ev_obs_ab12cd/x.json"), "usando /tmp/<TMP>/x.json"
        )

    def test_duracion(self):
        self.assertEqual(cr._normalizar("Ran 400 tests in 0.470s"), "Ran 400 tests in <DUR>")

    def test_pid(self):
        self.assertEqual(cr._normalizar("pid=12345 vivo"), "pid=<PID> vivo")

    def test_direccion_de_memoria(self):
        self.assertEqual(cr._normalizar("obj en 0x7f3ab12c"), "obj en <ADDR>")

    def test_no_toca_texto_estable(self):
        """Fechas sin hora, cifras y rutas del lab NO se normalizan."""
        estable = "2026-10-19 complejidad=114 total=980 ruta=/home/jokoalmi/joko-lab/tools"
        self.assertEqual(cr._normalizar(estable), estable)

    def test_normalizar_es_idempotente(self):
        una = cr._normalizar("2026-10-26 13:00:50 /tmp/x1 0.5s pid=9")
        self.assertEqual(cr._normalizar(una), una)


class TestResolverTool(unittest.TestCase):
    def test_tool_existente_sin_extension(self):
        ruta = cr._resolver_tool("complejidad_crap")
        self.assertIsNotNone(ruta)
        self.assertEqual(ruta.name, "complejidad_crap.py")

    def test_tool_existente_con_extension(self):
        self.assertIsNotNone(cr._resolver_tool("complejidad_crap.py"))

    def test_tool_inexistente(self):
        self.assertIsNone(cr._resolver_tool("no_existe_esta_tool_xyz"))

    def test_no_permite_salir_de_tools(self):
        self.assertIsNone(cr._resolver_tool("../../etc/passwd"))
        self.assertIsNone(cr._resolver_tool("../01-knowledge/RULE-012.yaml"))


class TestHuella(unittest.TestCase):
    def test_huella_estable(self):
        datos = {"exit": 0, "stdout": "hola", "stderr": ""}
        self.assertEqual(cr._huella(datos), cr._huella(dict(datos)))

    def test_huella_cambia_con_la_salida(self):
        a = {"exit": 0, "stdout": "hola", "stderr": ""}
        b = {"exit": 0, "stdout": "adios", "stderr": ""}
        self.assertNotEqual(cr._huella(a), cr._huella(b))

    def test_huella_cambia_con_el_exit(self):
        a = {"exit": 0, "stdout": "x", "stderr": ""}
        b = {"exit": 1, "stdout": "x", "stderr": ""}
        self.assertNotEqual(cr._huella(a), cr._huella(b))


class TestEjecutar(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.script = Path(self.tmp.name) / "eco.py"
        self.script.write_text(
            "import sys\nprint('salida', sys.argv[1])\nprint('aviso', file=sys.stderr)\n"
            "sys.exit(3)\n",
            encoding="utf-8",
        )

    def test_captura_salida_exit_y_stderr(self):
        datos = cr._ejecutar(self.script, ["hola"], 30, sys.executable)
        self.assertEqual(datos["exit"], 3)
        self.assertIn("salida hola", datos["stdout"])
        self.assertIn("aviso", datos["stderr"])

    def test_timeout_no_lanza_excepcion(self):
        lento = Path(self.tmp.name) / "lento.py"
        lento.write_text("import time\ntime.sleep(5)\n", encoding="utf-8")
        datos = cr._ejecutar(lento, [], 1, sys.executable)
        self.assertIsNone(datos["exit"])
        self.assertIn("TIMEOUT", datos["stderr"])


class TestDiff(unittest.TestCase):
    def _datos(self, salida="x", exit_code=0, err=""):
        return {"exit": exit_code, "stdout": salida, "stderr": err}

    def test_identico_sin_diferencias(self):
        self.assertEqual(cr._diff(self._datos(), self._datos()), [])

    def test_cambio_de_salida_detectado(self):
        diffs = cr._diff(self._datos("uno\ndos"), self._datos("uno\ntres"))
        texto = "\n".join(diffs)
        self.assertIn("--- antes/stdout", texto)
        self.assertIn("+++ ahora/stdout", texto)
        self.assertIn("-dos", texto)
        self.assertIn("+tres", texto)

    def test_cambio_solo_de_exit_detectado(self):
        diffs = cr._diff(self._datos(exit_code=0), self._datos(exit_code=1))
        self.assertEqual(len(diffs), 1)
        self.assertIn("exit: antes=0 ahora=1", diffs[0])

    def test_cambio_solo_de_stderr_detectado(self):
        diffs = cr._diff(self._datos(err=""), self._datos(err="boom"))
        self.assertIn("+boom", "\n".join(diffs))


class TestRutaRef(unittest.TestCase):
    def test_sanea_etiqueta(self):
        destino = cr._ruta_ref(Path("/tmp/x"), Path("/l/tools/foo.py"), "antes/../raro ")
        self.assertEqual(destino.name, "foo__antes_.._raro_.json")

    def test_etiqueta_vacia_no_rompe(self):
        destino = cr._ruta_ref(Path("/tmp/x"), Path("/l/tools/foo.py"), "")
        self.assertEqual(destino.name, "foo__ref.json")


class TestModoGuardarYComparar(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.dir = Path(self.tmp.name)
        self.destino = self.dir / "complejidad_crap__antes.json"
        self.nuevo = {"exit": 0, "stdout": "total 980\n", "stderr": "", "cmd": ["py", "x"]}

    def _silencioso(self, fn, *a):
        buf = io.StringIO()
        with redirect_stdout(buf):
            codigo = fn(*a)
        return codigo, buf.getvalue()

    def test_guardar_escribe_la_referencia(self):
        codigo, salida = self._silencioso(cr._accion_guardar, self.nuevo, self.destino, False)
        self.assertEqual(codigo, 0)
        self.assertTrue(self.destino.exists())
        self.assertIn("Referencia guardada", salida)
        guardado = json.loads(self.destino.read_text(encoding="utf-8"))
        self.assertEqual(guardado["stdout"], "total 980\n")
        self.assertIn("huella", guardado)

    def test_guardar_no_sobrescribe_sin_forzar(self):
        """Pitfall 33: una referencia previa NUNCA se pisa en silencio."""
        self.destino.write_text(json.dumps({"exit": 0, "stdout": "ORIGINAL"}), encoding="utf-8")
        codigo, salida = self._silencioso(cr._accion_guardar, self.nuevo, self.destino, False)
        self.assertEqual(codigo, 2)
        self.assertIn("Ya existe una referencia", salida)
        self.assertEqual(json.loads(self.destino.read_text(encoding="utf-8"))["stdout"], "ORIGINAL")

    def test_guardar_con_forzar_si_sobrescribe(self):
        self.destino.write_text(json.dumps({"exit": 0, "stdout": "ORIGINAL"}), encoding="utf-8")
        codigo, _ = self._silencioso(cr._accion_guardar, self.nuevo, self.destino, True)
        self.assertEqual(codigo, 0)
        self.assertEqual(json.loads(self.destino.read_text(encoding="utf-8"))["stdout"], "total 980\n")

    def test_comparar_sin_referencia(self):
        codigo, salida = self._silencioso(cr._accion_comparar, self.nuevo, self.destino)
        self.assertEqual(codigo, 2)
        self.assertIn("No hay referencia", salida)

    def test_comparar_identica(self):
        cr._guardar_json(self.destino, dict(self.nuevo, huella="abc"))
        codigo, salida = self._silencioso(cr._accion_comparar, self.nuevo, self.destino)
        self.assertEqual(codigo, 0)
        self.assertIn("SALIDA IDÉNTICA", salida)

    def test_comparar_distinta(self):
        cr._guardar_json(self.destino, {"exit": 0, "stdout": "total 423\n", "stderr": ""})
        codigo, salida = self._silencioso(cr._accion_comparar, self.nuevo, self.destino)
        self.assertEqual(codigo, 1)
        self.assertIn("SALIDA DISTINTA", salida)
        self.assertIn("+total 980", salida)


class TestMainCasoReal(unittest.TestCase):
    """Caso real: captura y comparación de una tool del lab (determinista)."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.dir = self.tmp.name

    def _main(self, argv):
        buf = io.StringIO()
        with redirect_stdout(buf):
            codigo = cr.main(argv)
        return codigo, buf.getvalue()

    def test_guardar_y_comparar_da_identica(self):
        comun = ["--tool", "complejidad_crap", "--dir", self.dir, "--", "--json"]
        codigo, salida = self._main(["--guardar", *comun])
        self.assertEqual(codigo, 0)
        self.assertIn("Referencia guardada", salida)
        codigo, salida = self._main(["--comparar", *comun])
        self.assertEqual(codigo, 0)
        self.assertIn("SALIDA IDÉNTICA", salida)

    def test_tool_inexistente_devuelve_2(self):
        codigo, salida = self._main(["--guardar", "--tool", "no_existe_xyz", "--dir", self.dir])
        self.assertEqual(codigo, 2)
        self.assertIn("No existe tools/no_existe_xyz.py", salida)

    def test_comparar_detecta_cambio_de_salida_real(self):
        comun = ["--tool", "complejidad_crap", "--dir", self.dir, "--", "--json"]
        self.assertEqual(self._main(["--guardar", *comun])[0], 0)
        # Se manipula la referencia (simula el "antes" con otro contenido).
        ref = Path(self.dir) / "complejidad_crap__antes.json"
        datos = json.loads(ref.read_text(encoding="utf-8"))
        datos["stdout"] = datos["stdout"].replace('"total_funciones"', '"total_funciones_X"', 1)
        ref.write_text(json.dumps(datos), encoding="utf-8")
        codigo, salida = self._main(["--comparar", *comun])
        self.assertEqual(codigo, 1)
        self.assertIn("SALIDA DISTINTA", salida)


if __name__ == "__main__":
    unittest.main()
