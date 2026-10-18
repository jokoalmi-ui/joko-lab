#!/usr/bin/env python3
"""
Tests de las funciones puras de tools/auditor_deuda_tools.py (auto-mejora 21-sep-2026).

Cubre las piezas que deciden el ranking: detección de test por prefijo, fórmula
del score, conteo de referencias por categoría y filtro de críticas.
Todo con directorios temporales: NUNCA se toca el lab real.

Ejecución:
  cd ~/joko-lab && python3 -m unittest tests.test_auditor_deuda_tools -v
"""

import sys
import tempfile
import unittest
from pathlib import Path

TOOLS_DIR = str(Path(__file__).resolve().parent.parent / "tools")
sys.path.insert(0, TOOLS_DIR)

import auditor_deuda_tools as adt


class TestTieneTest(unittest.TestCase):
    def test_coincidencia_exacta(self):
        self.assertTrue(adt._tiene_test("search", {"search"}))

    def test_coincidencia_por_prefijo_de_test(self):
        # tests/test_verificar_fk.py cubre la tool verificar_fk_kos
        self.assertTrue(adt._tiene_test("verificar_fk_kos", {"verificar_fk"}))

    def test_coincidencia_por_prefijo_de_tool(self):
        self.assertTrue(adt._tiene_test("search", {"search_engine"}))

    def test_sin_coincidencia(self):
        self.assertFalse(adt._tiene_test("foo", {"bar", "baz"}))

    def test_set_vacio(self):
        self.assertFalse(adt._tiene_test("search", set()))


class TestScore(unittest.TestCase):
    CERO = {"cron": 0, "script": 0, "skill": 0, "codigo": 0}

    def test_tool_sin_uso_y_con_test(self):
        self.assertEqual(adt._score(self.CERO, True, 5), 0)

    def test_sin_test_suma_penalizacion(self):
        self.assertEqual(adt._score(self.CERO, False, 5), adt.PESO_SIN_TEST)

    def test_main_complejo_suma_penalizacion(self):
        # main() > 10 con test: solo la penalización de complejidad
        self.assertEqual(adt._score(self.CERO, True, 11), adt.PESO_MAIN_COMPLEJO)

    def test_main_en_el_umbral_no_penaliza(self):
        self.assertEqual(adt._score(self.CERO, True, adt.UMBRAL_MAIN), 0)

    def test_uso_real_pesa_por_categoria(self):
        refs = {"cron": 2, "script": 3, "skill": 4, "codigo": 99}
        esperado = (adt.PESO_CRON * 2 + adt.PESO_SCRIPT * 3 + adt.PESO_SKILL * 4
                    + adt.PESO_SIN_TEST + adt.PESO_MAIN_COMPLEJO)
        self.assertEqual(adt._score(refs, False, 20), esperado)


class TestFila(unittest.TestCase):
    def test_toma_complejidad_del_archivo(self):
        refs = {"cron": 1, "script": 0, "skill": 0, "codigo": 0}
        fila = adt._fila("search", refs, False, {"search.py": {"max": 14, "main": 0}})
        self.assertEqual(fila["main"], 0)
        self.assertEqual(fila["max"], 14)
        self.assertTrue(fila["en_automatizacion"])

    def test_archivo_desconocido_no_revienta(self):
        fila = adt._fila("x", {"cron": 0, "script": 0, "skill": 0, "codigo": 0}, True, {})
        self.assertEqual((fila["max"], fila["main"]), (0, 0))
        self.assertFalse(fila["en_automatizacion"])

    def test_sin_uso_solo_por_skill_no_es_automatizacion(self):
        refs = {"cron": 0, "script": 0, "skill": 9, "codigo": 1}
        fila = adt._fila("x", refs, False, {})
        self.assertFalse(fila["en_automatizacion"])


class TestContarRefs(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="adt_test_"))
        (self.tmp / "usa_search.py").write_text('import search\nrun("search.py")\n', encoding="utf-8")
        (self.tmp / "script.sh").write_text("python3 tools/search.py -q hola\n", encoding="utf-8")
        (self.tmp / "otro.md").write_text("no menciona nada util\n", encoding="utf-8")
        self.fuentes = {"script": [self.tmp / "usa_search.py", self.tmp / "script.sh"],
                        "skill": [self.tmp / "otro.md"]}

    def test_cuenta_por_categoria(self):
        refs = adt._contar_refs(self.fuentes, {"search", "otro"})
        self.assertEqual(refs["search"]["script"], 2)
        self.assertEqual(refs["search"]["skill"], 0)
        self.assertEqual(refs["search"]["codigo"], 0)

    def test_no_confunde_subcadenas(self):
        # el token 'search' NO debe contar dentro de 'research' ni 'search_files'
        (self.tmp / "research.py").write_text("researcher = 1\nsearch_files = 2\n", encoding="utf-8")
        fuentes = {"codigo": [self.tmp / "research.py"]}
        refs = adt._contar_refs(fuentes, {"search"})
        self.assertEqual(refs["search"]["codigo"], 0)

    def test_nombre_ausente_cuenta_cero(self):
        refs = adt._contar_refs(self.fuentes, {"inexistente"})
        self.assertEqual(refs["inexistente"], {"cron": 0, "script": 0, "skill": 0, "codigo": 0})

    def test_fichero_ilegible_no_rompe(self):
        refs = adt._contar_refs({"codigo": [self.tmp / "no_existe.py"]}, {"search"})
        self.assertEqual(refs["search"]["codigo"], 0)


class TestDescubrimiento(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="adt_desc_"))
        (self.tmp / "alpha.py").write_text("x = 1\n", encoding="utf-8")
        (self.tmp / "beta.py").write_text("y = 2\n", encoding="utf-8")
        (self.tmp / f"{adt.PROPIA}.py").write_text("z = 3\n", encoding="utf-8")
        (self.tmp / "notas.md").write_text("nada\n", encoding="utf-8")

    def test_excluye_la_propia_auditora(self):
        self.assertEqual(adt._nombres_tools(self.tmp), ["alpha", "beta"])

    def test_stems_tests(self):
        tdir = Path(tempfile.mkdtemp(prefix="adt_tests_"))
        (tdir / "test_alpha.py").write_text("", encoding="utf-8")
        (tdir / "test_beta_audit.py").write_text("", encoding="utf-8")
        (tdir / "helper.py").write_text("", encoding="utf-8")
        self.assertEqual(adt._stems_tests(tdir), {"alpha", "beta_audit"})

    def test_stems_tests_sin_directorio(self):
        self.assertEqual(adt._stems_tests(Path("/tmp/adt_no_existe_xyz")), set())


class TestFiltroCriticas(unittest.TestCase):
    FILAS = [
        {"nombre": "a", "test": False, "en_automatizacion": True},
        {"nombre": "b", "test": False, "en_automatizacion": False},
        {"nombre": "c", "test": True, "en_automatizacion": True},
    ]

    def test_solo_automatizacion_sin_test(self):
        self.assertEqual([r["nombre"] for r in adt._sin_red(self.FILAS)], ["a"])

    def test_modo_completo_incluye_todas_las_sin_test(self):
        self.assertEqual([r["nombre"] for r in adt._sin_red(self.FILAS, solo_auto=False)], ["a", "b"])


class TestFormato(unittest.TestCase):
    def test_fila_marca_sin_test(self):
        fila = {"nombre": "search", "score": 70, "test": False, "main": 0, "max": 14,
                "refs": {"cron": 1, "script": 3, "skill": 57, "codigo": 34}}
        linea = adt._formatear_fila(fila)
        self.assertIn("search", linea)
        self.assertIn("test=NO", linea)
        self.assertIn("max= 14", linea)

    def test_fila_marca_con_test(self):
        fila = {"nombre": "evidence", "score": 24, "test": True, "main": 8, "max": 8,
                "refs": {"cron": 1, "script": 1, "skill": 19, "codigo": 13}}
        self.assertIn("test=OK", adt._formatear_fila(fila))


if __name__ == "__main__":
    unittest.main()
