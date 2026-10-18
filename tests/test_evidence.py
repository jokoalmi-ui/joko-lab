#!/usr/bin/env python3
"""
Tests de las funciones extraidas de evidence.main() (refactor 08-ago-2026 con
OpenCode): _cuerpo_decisiones_por_politica, _cuerpo_fallback_rate,
_cuerpo_uso_rules, _cuerpo_uso_rag y _registrar_obs.

Red de seguridad: flujo main() identico en entorno aislado (dirs temporales,
sin tocar el lab) + estos tests fijan las piezas.

Ejecucion:
  cd ~/joko-lab && python3 -m unittest tests/test_evidence.py -v
"""

import sys
import unittest
from pathlib import Path

TOOLS_DIR = str(Path(__file__).resolve().parent.parent / "tools")
sys.path.insert(0, TOOLS_DIR)

from evidence import (
    _cuerpo_decisiones_por_politica,
    _cuerpo_fallback_rate,
    _cuerpo_uso_rules,
    _cuerpo_uso_rag,
    _registrar_obs,
)


class TestCuerpoDecisionesPorPolitica(unittest.TestCase):
    def test_completo(self):
        cuerpo = _cuerpo_decisiones_por_politica(
            {"horario": 60, "privacidad": 25, "costes": 15}, 100)
        self.assertIn("Distribucion de decisiones por politica:", cuerpo)
        self.assertIn("- horario: 60 (60.0%)", cuerpo)
        self.assertIn("- privacidad: 25 (25.0%)", cuerpo)
        self.assertIn("Total: 100 decisiones.", cuerpo)

    def test_top_3(self):
        cuerpo = _cuerpo_decisiones_por_politica(
            {"a": 1, "b": 2, "c": 3, "d": 4}, 10)
        # solo las 3 primeras entradas
        self.assertIn("- a:", cuerpo)
        self.assertIn("- c:", cuerpo)
        self.assertNotIn("- d:", cuerpo)

    def test_vacio_devuelve_none(self):
        self.assertIsNone(_cuerpo_decisiones_por_politica({}, 10))
        self.assertIsNone(_cuerpo_decisiones_por_politica({"a": 1}, 0))


class TestCuerpoFallbackRate(unittest.TestCase):
    def test_normal(self):
        cuerpo = _cuerpo_fallback_rate(0.05, 100, "2026-08-08")
        self.assertEqual(
            cuerpo,
            "Fallback rate (Disponibilidad) el 2026-08-08: 5.0% de 100 decisiones.")

    def test_total_cero_devuelve_none(self):
        self.assertIsNone(_cuerpo_fallback_rate(0.05, 0, "2026-08-08"))

    def test_fr_none_devuelve_none(self):
        self.assertIsNone(_cuerpo_fallback_rate(None, 100, "2026-08-08"))


class TestCuerpoUsoRules(unittest.TestCase):
    def test_con_nunca(self):
        cuerpo = _cuerpo_uso_rules(
            {"RULE-003": 22}, ["RULE-005", "RULE-007"])
        self.assertIn("RULE mas activada: RULE-003 (22 activaciones).", cuerpo)
        self.assertIn("Reglas nunca activadas: RULE-005, RULE-007.", cuerpo)

    def test_sin_nunca(self):
        cuerpo = _cuerpo_uso_rules({"RULE-003": 22}, [])
        self.assertIn("RULE mas activada: RULE-003 (22 activaciones).", cuerpo)
        self.assertNotIn("nunca activadas", cuerpo)

    def test_vacio_devuelve_none(self):
        self.assertIsNone(_cuerpo_uso_rules({}, []))


class TestCuerpoUsoRag(unittest.TestCase):
    def test_con_nunca(self):
        cuerpo = _cuerpo_uso_rag(
            {"research/x.md": 5}, ["PATTERN-001"])
        self.assertIn("Documento mas recuperado: research/x.md (5 veces).", cuerpo)
        self.assertIn("KOs nunca recuperados: PATTERN-001.", cuerpo)

    def test_sin_nunca(self):
        cuerpo = _cuerpo_uso_rag({"research/x.md": 5}, [])
        self.assertIn("Documento mas recuperado: research/x.md (5 veces).", cuerpo)
        self.assertNotIn("nunca recuperados", cuerpo)

    def test_vacio_devuelve_none(self):
        self.assertIsNone(_cuerpo_uso_rag({}, []))


class TestRegistrarObs(unittest.TestCase):
    def test_con_path(self):
        creadas = []
        nuevo = _registrar_obs(creadas, 5, "/tmp/OBS-005.md")
        self.assertEqual(nuevo, 6)
        self.assertEqual(creadas, ["/tmp/OBS-005.md"])

    def test_sin_path_no_incrementa(self):
        creadas = []
        nuevo = _registrar_obs(creadas, 5, None)
        self.assertEqual(nuevo, 5)
        self.assertEqual(creadas, [])


if __name__ == "__main__":
    unittest.main()
