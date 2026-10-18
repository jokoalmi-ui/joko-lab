#!/usr/bin/env python3
"""
Tests de las funciones extraidas de check_huerfano_rules() (refactor
08-ago-2026 con OpenCode): _nombres_origen, _origen_existe y
_origen_referenciado.

Red de seguridad: salida de check_huerfano_rules comparada identica sobre
un set de rules con directorios temporales antes/despues + estos tests
fijan cada pieza.

Ejecucion:
  cd ~/joko-lab && python3 -m unittest tests/test_debt_detector.py -v
"""

import sys
import tempfile
import unittest
from pathlib import Path

TOOLS_DIR = str(Path(__file__).resolve().parent.parent / "tools")
sys.path.insert(0, TOOLS_DIR)

import debt_detector as dd


class TestNombresOrigen(unittest.TestCase):
    def test_sin_extension(self):
        self.assertEqual(dd._nombres_origen("DEC-001"),
                         ("DEC-001.yaml", "DEC-001.md"))

    def test_con_extension_yaml(self):
        self.assertEqual(dd._nombres_origen("EXP-001.yaml"),
                         ("EXP-001.yaml", "EXP-001.yaml.md"))

    def test_con_extension_md(self):
        self.assertEqual(dd._nombres_origen("DEC-002.md"),
                         ("DEC-002.md.yaml", "DEC-002.md"))


class TestOrigenExiste(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="dd_test_"))
        (self.tmp / "DEC-001.yaml").write_text("id: DEC-001\n", encoding="utf-8")
        (self.tmp / "DEC-002.md").write_text("id: DEC-002\n", encoding="utf-8")
        dd.DECISIONS_DIR = str(self.tmp)
        dd.EXPERIMENTS_DIR = str(Path(tempfile.mkdtemp(prefix="dd_exp_")))

    def test_existe_yaml(self):
        self.assertTrue(dd._origen_existe("DEC-001.yaml", "DEC-001.md"))

    def test_existe_md(self):
        self.assertTrue(dd._origen_existe("DEC-002.yaml", "DEC-002.md"))

    def test_no_existe(self):
        self.assertFalse(dd._origen_existe("DEC-999.yaml", "DEC-999.md"))


class TestOrigenReferenciado(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="dd_ref_"))
        (self.tmp / "DEC-010.md").write_text(
            "menciona a EXP-777 aqui\n", encoding="utf-8")
        dd.DECISIONS_DIR = str(self.tmp)
        dd.EXPERIMENTS_DIR = str(Path(tempfile.mkdtemp(prefix="dd_exp2_")))

    def test_referenciado_en_archivo(self):
        self.assertTrue(dd._origen_referenciado("EXP-777"))

    def test_no_referenciado(self):
        self.assertFalse(dd._origen_referenciado("EXP-888"))

    def test_directorio_vacio_no_referencia(self):
        dd.DECISIONS_DIR = str(Path(tempfile.mkdtemp(prefix="dd_vacio1_")))
        dd.EXPERIMENTS_DIR = str(Path(tempfile.mkdtemp(prefix="dd_vacio2_")))
        self.assertFalse(dd._origen_referenciado("EXP-777"))


class TestCheckHuerfanoRules(unittest.TestCase):
    def setUp(self):
        dec = Path(tempfile.mkdtemp(prefix="dd_ch_dec_"))
        exp = Path(tempfile.mkdtemp(prefix="dd_ch_exp_"))
        (dec / "DEC-001.yaml").write_text("id: DEC-001\n", encoding="utf-8")
        (exp / "EXP-001.yaml").write_text("id: EXP-001\n", encoding="utf-8")
        dd.DECISIONS_DIR = str(dec)
        dd.EXPERIMENTS_DIR = str(exp)

    def test_huerfano_y_no(self):
        rules = {
            "RULE-A.yaml": {"id": "RULE-A", "origen": "DEC-001"},
            "RULE-B.yaml": {"id": "RULE-B", "origen": "DEC-999"},
            "RULE-C.yaml": {"id": "RULE-C"},
        }
        issues = dd.check_huerfano_rules(rules)
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0]["rule"], "RULE-B")
        self.assertEqual(issues[0]["origen"], "DEC-999")


if __name__ == "__main__":
    unittest.main()
