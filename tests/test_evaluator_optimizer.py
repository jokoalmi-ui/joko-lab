#!/usr/bin/env python3
"""
Tests de las funciones extraidas de improve_prompt (refactor 08-ago-2026 con
OpenCode): _build_critique, _run_optimization_loop y _apply_gate.

Red de seguridad: captura de referencia /tmp/improve_prompt_ref.json con
call_llm y _run_context_builder mockeados + estos tests fijan cada pieza.
Las llamadas a LLM (critic_llm, optimize_llm, evaluate_response) se
mockean: estas funciones solo se testean con su logica determinista.

Ejecucion:
  cd ~/joko-lab && python3 -m unittest tests/test_evaluator_optimizer.py -v
"""

import sys
import unittest
from unittest.mock import patch

from pathlib import Path

TOOLS_DIR = str(Path(__file__).resolve().parent.parent / "tools")
sys.path.insert(0, TOOLS_DIR)

import evaluator_optimizer as evo

# Prompt que cumple todas las reglas de la rubrica (10/10)
PROMPT_OK = (
    "Eres un asistente experto. Devuelve el resultado en formato json, "
    "sin inventar datos y unicamente con la informacion proporcionada "
    "en el contexto."
)
# Prompt con 2 fallos (contexto y restricciones)
PROMPT_2_FAIL = "Eres un experto en datos. Devuelve el resumen en formato lista."
# Prompt con 5 fallos
PROMPT_5_FAIL = "resume"


def eval_result(passed_flags, descriptions):
    """Construye un eval_result con los fallos indicados."""
    results = []
    for passed, desc in zip(passed_flags, descriptions):
        results.append({"id": "r", "desc": desc, "weight": 1, "passed": passed})
    return {"results": results, "score": 0, "max_score": len(results),
            "percentage": 0, "semantic_warnings": [], "passed": False}


class TestBuildCritique(unittest.TestCase):
    def test_automatica_1_fallo(self):
        res = eval_result([True, False], ["ok", "falla la restriccion"])
        crit = evo._build_critique("prompt", res)
        self.assertTrue(crit.startswith("Problemas:\n- "))
        self.assertIn("falla la restriccion", crit)

    def test_automatica_2_fallos(self):
        res = eval_result([False, False], ["falta A", "falta B"])
        crit = evo._build_critique("prompt", res)
        self.assertIn("falta A", crit)
        self.assertIn("falta B", crit)

    def test_llm_con_mas_de_2_fallos(self):
        res = eval_result([False, False, False], ["a", "b", "c"])
        with patch.object(evo, "critic_llm", return_value="CRITICA_MOCK") as mock:
            crit = evo._build_critique("prompt", res)
        mock.assert_called_once_with("prompt", res)
        self.assertEqual(crit, "CRITICA_MOCK")


class TestRunOptimizationLoop(unittest.TestCase):
    def test_aprueba_en_ronda_1(self):
        history, current = evo._run_optimization_loop(PROMPT_OK, 3)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["status"], "APROBADO")
        self.assertEqual(current, PROMPT_OK)

    def test_mejora_y_aprueba(self):
        # optimize_llm mock: devuelve el prompt con anadido (simula mejora)
        def fake_optimize(prompt, critique):
            return "[OPT] " + prompt + " mejorado mock"
        with patch.object(evo, "optimize_llm", side_effect=fake_optimize):
            history, current = evo._run_optimization_loop(PROMPT_2_FAIL, 3)
        self.assertGreaterEqual(len(history), 1)
        self.assertEqual(history[-1]["status"], "APROBADO")
        self.assertTrue(current.startswith("[OPT]"))

    def test_estancado_si_optimizacion_identica(self):
        # optimize_llm devuelve EXACTAMENTE el prompt actual -> ESTANCADO
        def fake_optimize(prompt, critique):
            return prompt
        with patch.object(evo, "optimize_llm", side_effect=fake_optimize):
            history, current = evo._run_optimization_loop(PROMPT_2_FAIL, 3)
        self.assertEqual(history[-1]["status"], "ESTANCADO")
        self.assertEqual(current, PROMPT_2_FAIL)

    def test_estancado_si_optimizacion_demasiado_corta(self):
        with patch.object(evo, "optimize_llm", return_value="corto"):
            history, current = evo._run_optimization_loop(PROMPT_2_FAIL, 3)
        self.assertEqual(history[-1]["status"], "ESTANCADO")
        self.assertEqual(current, PROMPT_2_FAIL)


class TestApplyGate(unittest.TestCase):
    def test_sin_modelo_rechaza(self):
        final, cosmetic, re_ = evo._apply_gate("orig", "mejorado", "")
        self.assertEqual(final, "orig")
        self.assertTrue(cosmetic)
        self.assertIsNone(re_)

    def test_respuesta_identica_rechaza_cosmetica(self):
        re_mock = {"same": True, "improvement": 0}
        with patch.object(evo, "evaluate_response", return_value=re_mock):
            final, cosmetic, re_ = evo._apply_gate("orig", "mejorado", "m")
        self.assertEqual(final, "orig")
        self.assertTrue(cosmetic)

    def test_empeoro_rechaza(self):
        re_mock = {"same": False, "improvement": -30}
        with patch.object(evo, "evaluate_response", return_value=re_mock):
            final, cosmetic, re_ = evo._apply_gate("orig", "mejorado", "m")
        self.assertEqual(final, "orig")
        self.assertTrue(cosmetic)

    def test_mejora_real_acepta(self):
        re_mock = {"same": False, "improvement": 15}
        with patch.object(evo, "evaluate_response", return_value=re_mock):
            final, cosmetic, re_ = evo._apply_gate("orig", "mejorado", "m")
        self.assertEqual(final, "mejorado")
        self.assertFalse(cosmetic)

    def test_error_llm_fail_closed(self):
        with patch.object(evo, "evaluate_response",
                          side_effect=Exception("timeout")):
            final, cosmetic, re_ = evo._apply_gate("orig", "mejorado", "m")
        self.assertEqual(final, "orig")
        self.assertTrue(cosmetic)
        self.assertIsNone(re_)

    def test_sin_cambio_no_llama_llm(self):
        # prompt == current: no debe llamar a evaluate_response
        with patch.object(evo, "evaluate_response") as mock:
            final, cosmetic, re_ = evo._apply_gate("orig", "orig", "m")
        mock.assert_not_called()
        self.assertEqual(final, "orig")


class TestFormatReportHelpers(unittest.TestCase):
    """Tests de las funciones extraidas de format_report (refactor 08-ago).

    La red principal es la referencia de salida byte-identica
    (/tmp/format_report_ref.txt, 4 casos); estos tests fijan las piezas.
    """

    def _result(self, history, passed, re=None, accepted=False, cosmetic=True):
        return {
            "original": "prompt original",
            "final": "prompt final",
            "accepted": accepted,
            "cosmetic_rejected": cosmetic,
            "total_rounds": len(history),
            "initial_score": history[0]["score"] if history else 0,
            "final_score": history[-1]["score"] if history else 0,
            "passed": passed,
            "history": history,
            "response_eval": re,
        }

    def test_cabecera_informe(self):
        r = self._result([], True)
        lines = evo._cabecera_informe(r)
        self.assertEqual(lines[0], "═" * 43)
        self.assertIn("EVALUATOR-OPTIMIZER v2", lines[1])
        self.assertTrue(any("Estado: ✅ APROBADO" in l for l in lines))
        self.assertEqual(lines[-1], "")  # linea vacia final

    def test_cabecera_no_paso_umbral(self):
        r = self._result([], False)
        lines = evo._cabecera_informe(r)
        self.assertTrue(any("Estado: ❌ NO PASO EL UMBRAL" in l for l in lines))

    def test_seccion_historia_con_warnings(self):
        r = self._result([
            {"round": 1, "status": "MEJORADO", "score": 70,
             "eval": {"semantic_warnings": ["Posible contradiccion: 'a' vs 'b'"],
                      "passed": False},
             "critique": "Problemas:\n- Falta contexto",
             "optimized": "[OPT] prompt"},
        ], False)
        lines = evo._seccion_historia(r)
        texto = "\n".join(lines)
        self.assertIn("Ronda 1 [🔄] Score: 70%", texto)
        self.assertIn("⚠ Posible contradiccion: 'a' vs 'b'", texto)
        self.assertIn("├ Problemas:", texto)
        self.assertIn("└ Prompt: [OPT] prompt", texto)
        self.assertEqual(lines[-1], "")  # linea vacia tras cada ronda

    def test_seccion_historia_estancado(self):
        r = self._result([
            {"round": 1, "status": "ESTANCADO", "score": 60,
             "eval": {"semantic_warnings": [], "passed": False},
             "critique": "Critica", "optimized": ""},
        ], False)
        lines = evo._seccion_historia(r)
        self.assertIn("Ronda 1 [⏹] Score: 60%", "\n".join(lines))

    def test_seccion_gate_cosmetica(self):
        re_ = {"same": True, "improvement": 0, "len1": 40, "len2": 42,
               "structure1": False, "structure2": False}
        r = self._result([], False, re=re_)
        lines = evo._seccion_gate(r)
        texto = "\n".join(lines)
        self.assertIn("── GATE: RESPUESTA CONTRA MODELO DESTINO ──", texto)
        self.assertIn("❌ OPTIMIZACION RECHAZADA (cosmetica)", texto)

    def test_seccion_gate_aceptada(self):
        re_ = {"same": False, "improvement": 25, "len1": 40, "len2": 60,
               "structure1": False, "structure2": True}
        r = self._result([], False, re=re_, accepted=True, cosmetic=False)
        lines = evo._seccion_gate(r)
        texto = "\n".join(lines)
        self.assertIn("✅ OPTIMIZACION ACEPTADA (mejora real)", texto)
        self.assertIn("Mejora: 25%", texto)
        self.assertIn("[estructurado]", texto)

    def test_seccion_gate_sin_response_eval(self):
        r = self._result([], True, re=None)
        self.assertEqual(evo._seccion_gate(r), [])

    def test_format_report_ensambla_en_orden(self):
        r = self._result([
            {"round": 1, "status": "MEJORADO", "score": 50,
             "eval": {"semantic_warnings": [], "passed": False},
             "critique": "C", "optimized": "[OPT] v1"},
        ], True, re={"same": False, "improvement": 10, "len1": 10, "len2": 20,
                     "structure1": False, "structure2": False})
        out = evo.format_report(r)
        # el bloque 'Prompt final optimizado' va entre historia y GATE
        self.assertLess(out.index("Ronda 1"), out.index("Prompt final optimizado"))
        self.assertLess(out.index("Prompt final optimizado"),
                        out.index("GATE: RESPUESTA CONTRA MODELO DESTINO"))
        self.assertTrue(out.endswith("═" * 43))


if __name__ == "__main__":
    unittest.main()
