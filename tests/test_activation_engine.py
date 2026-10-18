#!/usr/bin/env python3
"""
Tests de las funciones extraidas de activate() (refactor 07-ago-2026 con
OpenCode): _match_rule, _es_block, _es_modelo, _mejor_modelo,
_aplicar_politicas, _trace_modelo.

Red de seguridad: salida de activate() identica para 5 casos (con
_log_activation neutralizado para no tocar el ledger) + estos tests fijan
cada pieza, incluido el caso del bug condicion:null del 04-ago.

Ejecucion:
  cd ~/joko-lab && python3 -m unittest tests/test_activation_engine.py -v
"""

import sys
import unittest
from pathlib import Path

TOOLS_DIR = str(Path(__file__).resolve().parent.parent / "tools")
sys.path.insert(0, TOOLS_DIR)

from activation_engine import (_match_rule, _es_block, _es_modelo,
                               _mejor_modelo, _aplicar_politicas,
                               _trace_modelo)


class TestMatchRule(unittest.TestCase):
    def test_match_por_tipo(self):
        rule = {"condicion": {"tipo_tarea": ["creatividad"]}}
        self.assertTrue(_match_rule("creatividad", "", rule))

    def test_no_match_otro_tipo(self):
        rule = {"condicion": {"tipo_tarea": ["creatividad"]}}
        self.assertFalse(_match_rule("json", "", rule))

    def test_cualquiera(self):
        rule = {"condicion": {"tipo_tarea": ["cualquiera"]}}
        self.assertTrue(_match_rule("general", "", rule))

    def test_keywords_necesarias(self):
        rule = {"condicion": {"tipo_tarea": ["general"], "keywords": ["relato"]}}
        self.assertTrue(_match_rule("general", "escribe un relato", rule))
        self.assertFalse(_match_rule("general", "hola que tal", rule))

    def test_condicion_none_no_matchea(self):
        # Bug 04-ago: condicion null hacia que la RULE nunca se activara
        rule = {"condicion": None}
        self.assertFalse(_match_rule("creatividad", "", rule))

    def test_prompt_vacio_con_keywords(self):
        # kw_match = not keywords cuando prompt_lower vacio
        rule = {"condicion": {"tipo_tarea": ["general"]}}
        self.assertTrue(_match_rule("general", "", rule))


class TestClasificacion(unittest.TestCase):
    def test_es_block(self):
        self.assertTrue(_es_block({"accion": {"accion": "block"}}))
        self.assertFalse(_es_block({"accion": {"modelo": "x"}}))
        self.assertFalse(_es_block({"accion": "otra"}))

    def test_es_modelo(self):
        self.assertTrue(_es_modelo({"accion": {"modelo": "gemma"}}))
        self.assertFalse(_es_modelo({"accion": {"accion": "block"}}))

    def test_mejor_modelo(self):
        self.assertTrue(_mejor_modelo({"prioridad": 90}, None))
        self.assertTrue(_mejor_modelo({"prioridad": 90}, {"prioridad": 50}))
        self.assertFalse(_mejor_modelo({"prioridad": 30}, {"prioridad": 50}))


class TestAplicarPoliticas(unittest.TestCase):
    def test_solo_block_y_force_local(self):
        policies = [
            {"id": "POL-1", "activa": True, "accion": "block"},
            {"id": "POL-2", "activa": True, "accion": "force_local"},
            {"id": "POL-3", "activa": True, "accion": "avisar"},
            {"id": "POL-4", "activa": False, "accion": "block"},
        ]
        out = _aplicar_politicas(policies)
        ids = [p["id"] for p in out]
        self.assertEqual(ids, ["POL-1", "POL-2"])


class TestTraceModelo(unittest.TestCase):
    def test_trace_con_claves(self):
        rule = {
            "desc": "Usar gemma para creatividad",
            "origen": "DEC-003",
            "accion": {"modelo": "gemma"},
            "validaciones": 3,
            "confianza": 0.85,
        }
        t = _trace_modelo(rule)
        # Devuelve el dict interno; activate() lo asigna a model_selection["_trace"]
        self.assertEqual(t["decision"], "Seleccionar gemma")
        self.assertIn("3 validaciones", t["proof"])
        self.assertIn("timestamp", t)


if __name__ == "__main__":
    unittest.main()
