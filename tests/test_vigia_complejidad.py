#!/usr/bin/env python3
"""
Tests de tools/vigia_complejidad.py (auto-mejora 16-nov-2026).

Cubre las piezas puras del vigía (indexado, comparación de snapshots,
detección de deuda dura, lectura/escritura del histórico) y el entry point
`main()` sobre un directorio TEMPORAL de tools — nunca el lab real, salvo el
caso de integración que solo LEE el histórico y no guarda.

Ejecución:
  cd ~/joko-lab && TMPDIR=/tmp python3 -m unittest tests.test_vigia_complejidad -v
"""

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

TOOLS_DIR = str(Path(__file__).resolve().parent.parent / "tools")
sys.path.insert(0, TOOLS_DIR)

import vigia_complejidad as vc


def _func_simple(nombre: str, ramp: int, archivo: str = "/lab/tools/x.py") -> dict:
    """Registro con forma de complejidad_crap.analizar_archivo."""
    return {"archivo": archivo, "funcion": nombre, "complejidad": ramp, "linea": 1}


def _escribir_rampa(directorio: Path, nombre: str, rampas: list) -> None:
    """Crea un .py temporal con una función por cada rampa de complejidad indicada."""
    lineas = []
    for i, rampa in enumerate(rampas):
        lineas.append(f"def f{i}(x):")
        for j in range(rampa - 1):
            lineas.append(f"    if x == {j}: pass")
        lineas.append("    return 1")
        lineas.append("")
    (directorio / nombre).write_text("\n".join(lineas), encoding="utf-8")


class TestIndexar(unittest.TestCase):
    def test_clave_usa_nombre_de_archivo_y_funcion(self):
        self.assertEqual(vc._clave(_func_simple("evaluar", 30)), "x.py::evaluar")

    def test_solo_entran_las_del_radar(self):
        radar = vc._indexar([_func_simple("a", 5), _func_simple("b", 11), _func_simple("c", 21)])
        self.assertEqual(radar, {"x.py::b": 11, "x.py::c": 21})

    def test_umbral_exacto_no_entra(self):
        # complejidad 10 = mantenible (UMBRAL_COMPLEJO), no entra en el radar
        self.assertEqual(vc._indexar([_func_simple("a", 10)]), {})

    def test_registro_sin_complejidad_se_ignora(self):
        self.assertEqual(vc._indexar([{"archivo": "x.py", "funcion": "a"}]), {})


class TestResumen(unittest.TestCase):
    def test_cuenta_complejas_y_muy_complejas(self):
        self.assertEqual(
            vc._resumen({"a": 11, "b": 20, "c": 21, "d": 114}),
            {"en_radar": 4, "complejas": 2, "muy_complejas": 2},
        )

    def test_radar_vacio(self):
        self.assertEqual(vc._resumen({}), {"en_radar": 0, "complejas": 0, "muy_complejas": 0})


class TestComparar(unittest.TestCase):
    def test_previo_none_es_todo_nuevo(self):
        delta = vc._comparar(None, {"a.py::f": 12})
        self.assertEqual(delta["nuevas"], [("a.py::f", 0, 12)])
        self.assertEqual(delta["empeoradas"], [])

    def test_detecta_nueva_empeorada_mejorada_y_salida(self):
        previo = {"a.py::sube": 12, "a.py::baja": 18, "a.py::sale": 15}
        actual = {"a.py::sube": 25, "a.py::baja": 9, "a.py::nueva": 11}
        delta = vc._comparar(previo, actual)
        self.assertEqual(delta["empeoradas"], [("a.py::sube", 12, 25)])
        self.assertEqual(delta["mejoradas"], [("a.py::baja", 18, 9)])
        self.assertEqual(delta["salidas"], [("a.py::sale", 15, 0)])
        self.assertEqual(delta["nuevas"], [("a.py::nueva", 0, 11)])

    def test_sin_cambios_da_todo_vacio(self):
        delta = vc._comparar({"a.py::f": 12}, {"a.py::f": 12})
        self.assertFalse(any(delta.values()))

    def test_orden_por_magnitud(self):
        delta = vc._comparar({}, {"a.py::x": 12, "a.py::y": 40, "a.py::z": 21})
        self.assertEqual([x[0] for x in delta["nuevas"]], ["a.py::y", "a.py::z", "a.py::x"])


class TestDeudaDura(unittest.TestCase):
    def test_nueva_por_encima_del_umbral_es_dura(self):
        delta = vc._comparar(None, {"a.py::f": 21})
        self.assertEqual(len(vc._deuda_dura(delta)), 1)

    def test_nueva_11_20_no_es_dura(self):
        delta = vc._comparar(None, {"a.py::f": 20})
        self.assertEqual(vc._deuda_dura(delta), [])

    def test_cruce_del_umbral_es_dura(self):
        delta = vc._comparar({"a.py::f": 18}, {"a.py::f": 22})
        self.assertEqual(vc._deuda_dura(delta), [("a.py::f", 18, 22)])

    def test_muy_compleja_que_empeora_no_es_dura_nueva(self):
        # ya era >20: no es deuda NUEVA (el informe la lista como empeorada)
        delta = vc._comparar({"a.py::f": 30}, {"a.py::f": 34})
        self.assertEqual(vc._deuda_dura(delta), [])


class TestDeltaYDuras(unittest.TestCase):
    def test_sin_previo_no_hay_delta_ni_deuda(self):
        delta, duras = vc._delta_y_duras(None, {"a.py::f": 114})
        self.assertEqual(duras, [])
        self.assertFalse(any(delta.values()))

    def test_con_previo_calcula_deuda_dura(self):
        previo = {"funciones": {"a.py::f": 12}}
        delta, duras = vc._delta_y_duras(previo, {"a.py::f": 12, "a.py::n": 30})
        self.assertEqual([x[0] for x in duras], ["a.py::n"])

    def test_previo_sin_clave_funciones_no_revienta(self):
        delta, duras = vc._delta_y_duras({"ts": "x"}, {"a.py::n": 30})
        self.assertEqual([x[0] for x in duras], ["a.py::n"])


class TestHistorico(unittest.TestCase):
    def test_sin_fichero_devuelve_none(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertIsNone(vc._leer_ultimo(Path(tmp) / "no_existe.jsonl"))

    def test_lee_la_ultima_linea_y_salta_corruptas(self):
        with tempfile.TemporaryDirectory() as tmp:
            ruta = Path(tmp) / "h.jsonl"
            ruta.write_text(
                json.dumps({"ts": "uno", "en_radar": 1}) + "\n"
                + "{esto no es json\n"
                + json.dumps({"ts": "dos", "en_radar": 2}) + "\n",
                encoding="utf-8",
            )
            self.assertEqual(vc._leer_ultimo(ruta)["ts"], "dos")

    def test_guardar_crea_directorio_y_hace_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            ruta = Path(tmp) / "sub" / "h.jsonl"
            vc._guardar(ruta, {"a.py::f": 12, "a.py::g": 30})
            ultimo = vc._leer_ultimo(ruta)
            self.assertEqual(ultimo["en_radar"], 2)
            self.assertEqual(ultimo["complejas"], 1)
            self.assertEqual(ultimo["muy_complejas"], 1)
            self.assertEqual(ultimo["funciones"], {"a.py::g": 30, "a.py::f": 12})
            self.assertIn("ts", ultimo)


class TestMainEntryPoint(unittest.TestCase):
    def _lab(self, tmp: str, rampas: list) -> tuple:
        directorio = Path(tmp) / "tools"
        directorio.mkdir()
        _escribir_rampa(directorio, "tool.py", rampas)
        return directorio, Path(tmp) / "hist.jsonl"

    def _run(self, *argv) -> tuple:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            codigo = vc.main(list(argv))
        return codigo, buf.getvalue()

    def test_primera_ejecucion_crea_linea_base_y_exit_0(self):
        with tempfile.TemporaryDirectory() as tmp:
            directorio, historial = self._lab(tmp, [3])
            codigo, salida = self._run("--directorio", str(directorio), "--historial", str(historial))
            self.assertEqual(codigo, 0)
            self.assertIn("Línea base", salida)
            self.assertEqual(len(historial.read_text().splitlines()), 1)

    def test_segunda_ejecucion_sin_cambios(self):
        with tempfile.TemporaryDirectory() as tmp:
            directorio, historial = self._lab(tmp, [3])
            self._run("--directorio", str(directorio), "--historial", str(historial))
            codigo, salida = self._run("--directorio", str(directorio), "--historial", str(historial))
            self.assertEqual(codigo, 0)
            self.assertIn("Sin cambios", salida)

    def test_funcion_nueva_muy_compleja_rompe_exit(self):
        with tempfile.TemporaryDirectory() as tmp:
            directorio, historial = self._lab(tmp, [3])
            self._run("--directorio", str(directorio), "--historial", str(historial))
            _escribir_rampa(directorio, "tool.py", [3, 25])
            codigo, salida = self._run("--directorio", str(directorio), "--historial", str(historial))
            self.assertEqual(codigo, 1)
            self.assertIn("Deuda DURA", salida)
            self.assertIn("tool.py::f1", salida)

    def test_funcion_nueva_blanda_no_rompe_exit(self):
        with tempfile.TemporaryDirectory() as tmp:
            directorio, historial = self._lab(tmp, [3])
            self._run("--directorio", str(directorio), "--historial", str(historial))
            _escribir_rampa(directorio, "tool.py", [3, 14])
            codigo, salida = self._run("--directorio", str(directorio), "--historial", str(historial))
            self.assertEqual(codigo, 0)
            self.assertIn("Nuevas en el radar", salida)

    def test_sin_guardar_no_escribe(self):
        with tempfile.TemporaryDirectory() as tmp:
            directorio, historial = self._lab(tmp, [25])
            codigo, _ = self._run(
                "--directorio", str(directorio), "--historial", str(historial), "--sin-guardar"
            )
            self.assertEqual(codigo, 0)  # sin histórico no hay delta → no hay deuda nueva
            self.assertFalse(historial.exists())

    def test_json_es_parseable_y_trae_el_delta(self):
        with tempfile.TemporaryDirectory() as tmp:
            directorio, historial = self._lab(tmp, [3])
            self._run("--directorio", str(directorio), "--historial", str(historial))
            _escribir_rampa(directorio, "tool.py", [3, 30])
            _, salida = self._run(
                "--directorio", str(directorio), "--historial", str(historial), "--json"
            )
            datos = json.loads(salida)
            self.assertEqual(datos["actual"]["en_radar"], 1)
            self.assertEqual(len(datos["deuda_dura"]), 1)
            self.assertEqual(datos["deuda_dura"][0][0], "tool.py::f1")


if __name__ == "__main__":
    unittest.main()
