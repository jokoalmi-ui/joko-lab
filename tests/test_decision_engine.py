#!/usr/bin/env python3
"""
Tests de las funciones extraidas de evaluate() (refactor 07-ago-2026 con
OpenCode): _procesar_reglas_engine y _procesar_regla_hardcodeada.

Red de seguridad: salida de evaluate() identica para 2 casos + verificación
propia de OpenCode (140 combinaciones, 0 mismatches) + estos tests fijan
cada pieza.

Ejecucion:
  cd ~/joko-lab && python3 -m unittest tests/test_decision_engine.py -v
"""

import sys
import unittest
from pathlib import Path

TOOLS_DIR = str(Path(__file__).resolve().parent.parent / "tools")
sys.path.insert(0, TOOLS_DIR)

from decision_engine import (_procesar_reglas_engine, _procesar_regla_hardcodeada,
                             _cabecera_output, _seccion_checklist,
                             _seccion_bloqueos, _seccion_activaciones,
                             _seccion_inyecciones, _seccion_modelo,
                             _seccion_avisos)


class TestProcesarReglasEngine(unittest.TestCase):
    def test_block_y_modelo(self):
        reglas = [
            {"id": "R1", "origen": "KO", "prioridad": 90,
             "accion": {"modelo": "gemma", "params": {"temperature": 0.9}}},
            {"id": "R2", "origen": "KO", "prioridad": 80,
             "accion": {"accion": "block", "razon": "no"}},
        ]
        blocks, model = _procesar_reglas_engine(reglas)
        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0]["id"], "R2")
        self.assertEqual(model["model"], "gemma")
        self.assertEqual(model["prioridad"], 90)

    def test_modelo_por_prioridad(self):
        reglas = [
            {"id": "R1", "prioridad": 50, "accion": {"modelo": "a"}},
            {"id": "R2", "prioridad": 90, "accion": {"modelo": "b"}},
        ]
        blocks, model = _procesar_reglas_engine(reglas)
        self.assertEqual(model["model"], "b")

    def test_accion_no_dict_se_ignora(self):
        blocks, model = _procesar_reglas_engine([{"id": "R1", "accion": "otra"}])
        self.assertEqual(blocks, [])
        self.assertIsNone(model)

    def test_vacio(self):
        blocks, model = _procesar_reglas_engine([])
        self.assertEqual(blocks, [])
        self.assertIsNone(model)


class TestProcesarReglaHardcodeada(unittest.TestCase):
    def test_condicion_true_activa(self):
        regla = {"condition": lambda q: True, "knowledge_type": "activo",
                 "action": "block"}
        self.assertEqual(_procesar_regla_hardcodeada(regla, "x"), "block")

    def test_condicion_false(self):
        regla = {"condition": lambda q: False, "knowledge_type": "activo",
                 "action": "warn"}
        self.assertIsNone(_procesar_regla_hardcodeada(regla, "x"))

    def test_condicion_lanza(self):
        def boom(q):
            raise ValueError("x")
        regla = {"condition": boom, "knowledge_type": "activo", "action": "warn"}
        self.assertIsNone(_procesar_regla_hardcodeada(regla, "x"))

    def test_gate_pasivo_no_modifica(self):
        regla = {"condition": lambda q: True, "knowledge_type": "pasivo",
                 "action": "block"}
        self.assertIsNone(_procesar_regla_hardcodeada(regla, "x"))

    def test_tipos_de_accion(self):
        for accion in ("activate", "inject", "select_model", "warn"):
            regla = {"condition": lambda q: True, "knowledge_type": "activo",
                     "action": accion}
            self.assertEqual(_procesar_regla_hardcodeada(regla, "x"), accion)


class TestSeccionesFormatOutput(unittest.TestCase):
    """Tests de las secciones extraidas de format_output (08-ago-2026)."""

    def test_cabecera_output(self):
        lines = _cabecera_output({"task_type": "chat", "rules_triggered": 3})
        self.assertIn("ACTION LAYER v2 — Decision Engine", lines[1])
        self.assertIn("Tarea: CHAT", lines[3])
        self.assertIn("Reglas disparadas: 3", lines[4])

    def test_checklist_con_mandatory_y_recommended(self):
        cl = {"name": "CHK", "mandatory": [{"desc": "A"}],
              "recommended": [{"desc": "B"}]}
        lines = _seccion_checklist(cl)
        texto = "\n".join(lines)
        self.assertIn("── CHECKLIST OBLIGATORIA: CHK ──", texto)
        self.assertIn("□ A", texto)
        self.assertIn("○ B (recomendado)", texto)

    def test_bloqueos(self):
        lines = _seccion_bloqueos([{"id": "RULE-004", "gate": "block",
                                    "reason": "no", "origen": "x.yaml"}])
        texto = "\n".join(lines)
        self.assertIn("── 🚫 BLOQUEADO ──", texto)
        self.assertIn("❌ RULE-004 [block]", texto)
        self.assertIn("Origen: x.yaml", texto)

    def test_activaciones(self):
        lines = _seccion_activaciones([{"module": "m", "gate": "g",
                                        "reason": "r"}])
        texto = "\n".join(lines)
        self.assertIn("── ▶ MODULOS ACTIVADOS ──", texto)
        self.assertIn("→ m [g]", texto)

    def test_inyecciones(self):
        lines = _seccion_inyecciones([{"content": "c", "origen": "o", "gate": "g"}])
        texto = "\n".join(lines)
        self.assertIn("── 💉 RESTRICCIONES INYECTADAS ──", texto)
        self.assertIn("⚠ c", texto)

    def test_modelo(self):
        m = {"model": "granite", "gate": "model_selection",
             "params": {"temperature": 0.3, "max_tokens": 1024},
             "reason": "JSON", "origen": "o.yaml"}
        lines = _seccion_modelo(m)
        texto = "\n".join(lines)
        self.assertIn("── 🎯 MODELO SELECCIONADO ──", texto)
        self.assertIn("granite [model_selection]", texto)
        self.assertIn("temp=0.3, max_tokens=1024", texto)

    def test_avisos(self):
        lines = _seccion_avisos([{"reason": "baja confianza"}])
        texto = "\n".join(lines)
        self.assertIn("── ⚠ AVISOS ──", texto)
        self.assertIn("baja confianza", texto)

    def test_format_output_caso_vacio(self):
        result = {"task_type": "general", "rules_triggered": 0, "checklist": {},
                  "blocks": [], "activations": [], "injections": [],
                  "model_selection": None, "warnings": []}
        out = __import__("decision_engine").format_output(result)
        self.assertIn("Sin reglas activas para esta consulta.", out)


if __name__ == "__main__":
    unittest.main()
