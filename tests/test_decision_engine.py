#!/usr/bin/env python3
"""
Tests unitarios para decision_engine.py
Cubre las 5 políticas + casos de error.

Modo de uso:
  python3 -m pytest tests/test_decision_engine.py -v
  python3 tests/test_decision_engine.py              # modo unittest directo
"""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

# Añadir el DE al path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "decision-engine"))
from decision_engine import (
    decide,
    evaluar_privacidad,
    evaluar_disponibilidad,
    evaluar_costes,
    evaluar_horario,
    evaluar_preferencias,
    load_state,
    load_ultima_decision,
)


class TestEvaluarPrivacidad(unittest.TestCase):
    """Política 1: datos sensibles → forzar local"""

    def test_datos_sensibles_activos(self):
        state = {}
        policies = {"privacidad": {"datos_sensibles": True, "niveles": []},
                     "modelos": {"por_proveedor": {"ollama": {"default": "llama31-8b-64k"}}}}
        r = evaluar_privacidad(state, policies)
        self.assertIsNotNone(r)
        self.assertEqual(r["provider"], "ollama")

    def test_datos_sensibles_inactivos(self):
        state = {}
        policies = {"privacidad": {"datos_sensibles": False, "niveles": []}}
        r = evaluar_privacidad(state, policies)
        self.assertIsNone(r)

    def test_sin_politica_privacidad(self):
        state = {}
        policies = {}
        r = evaluar_privacidad(state, policies)
        self.assertIsNone(r)


class TestEvaluarDisponibilidad(unittest.TestCase):
    """Política 2: disponibilidad de proveedores"""

    def test_todo_disponible(self):
        state = {
            "cloud": {"deepseek": {"disponible": True}, "gemini": {"disponible": True}},
            "services": {"ollama": {"activo": True}},
        }
        policies = {"modelos": {"por_proveedor": {}}}
        r = evaluar_disponibilidad(state, policies)
        self.assertIsNone(r)  # None = pasar a siguiente política

    def test_ds_caido_gemini_ok(self):
        state = {
            "cloud": {"deepseek": {"disponible": False}, "gemini": {"disponible": True}},
            "services": {"ollama": {"activo": False}},
        }
        policies = {"modelos": {"por_proveedor": {"gemini": {"default": "gemini-2.5-pro"}}}}
        r = evaluar_disponibilidad(state, policies)
        self.assertIsNotNone(r)
        self.assertEqual(r["provider"], "gemini")

    def test_gemini_caido_ds_ok(self):
        state = {
            "cloud": {"deepseek": {"disponible": True}, "gemini": {"disponible": False}},
            "services": {"ollama": {"activo": False}},
        }
        policies = {"modelos": {"por_proveedor": {"deepseek": {"default": "deepseek-v4-flash"}}}}
        r = evaluar_disponibilidad(state, policies)
        self.assertIsNotNone(r)
        self.assertEqual(r["provider"], "deepseek")

    def test_todo_cloud_caido_ollama_ok(self):
        state = {
            "cloud": {"deepseek": {"disponible": False}, "gemini": {"disponible": False}},
            "services": {"ollama": {"activo": True}},
        }
        policies = {"modelos": {"por_proveedor": {"ollama": {"default": "llama31-8b-64k"}}}}
        r = evaluar_disponibilidad(state, policies)
        self.assertIsNotNone(r)
        self.assertEqual(r["provider"], "ollama")

    def test_todo_caido(self):
        state = {
            "cloud": {"deepseek": {"disponible": False}, "gemini": {"disponible": False}},
            "services": {"ollama": {"activo": False}},
        }
        policies = {}
        r = evaluar_disponibilidad(state, policies)
        self.assertIsNotNone(r)
        self.assertEqual(r["provider"], "none")


class TestEvaluarCostes(unittest.TestCase):
    """Política 3: costes — saldo mínimo"""

    def test_saldo_suficiente(self):
        state = {
            "cloud": {"deepseek": {"saldo_usd": 10.0}, "gemini": {"saldo_usd": 10.0}}
        }
        policies = {"costes": {"limites": {"saldo_minimo_usd": 5.0}}}
        r = evaluar_costes(state, policies)
        self.assertIsNone(r)

    def test_saldo_insuficiente_ds(self):
        state = {
            "cloud": {"deepseek": {"saldo_usd": 1.0}, "gemini": {"saldo_usd": 10.0}}
        }
        policies = {"costes": {"limites": {"saldo_minimo_usd": 5.0}}}
        r = evaluar_costes(state, policies)
        self.assertIsNotNone(r)
        self.assertEqual(r["provider"], "ollama")

    def test_saldo_null(self):
        """Si el saldo es null (no se ha recolectado), la política no actúa."""
        state = {
            "cloud": {"deepseek": {"saldo_usd": None}, "gemini": {"saldo_usd": None}}
        }
        policies = {"costes": {"limites": {"saldo_minimo_usd": 5.0}}}
        r = evaluar_costes(state, policies)
        self.assertIsNone(r)

    def test_sin_limite_saldo(self):
        state = {
            "cloud": {"deepseek": {"saldo_usd": 0.5}, "gemini": {"saldo_usd": 0.5}}
        }
        policies = {"costes": {"limites": {"saldo_minimo_usd": 0}}}
        r = evaluar_costes(state, policies)
        self.assertIsNone(r)


class TestEvaluarHorario(unittest.TestCase):
    """Política 4: horario — elección según franja"""

    def test_franja_manana(self):
        """03:00-12:00 → gemini"""
        state = {"policies": {"hora": {"actual": "09:30", "franja_activa": "03:00-12:00"}}}
        policies = {
            "horario": {
                "reglas": [
                    {"horas": "03:00-12:00", "proveedor": "gemini"},
                    {"horas": "12:00-03:00", "proveedor": "deepseek"},
                ],
                "fallback": {"proveedor": "ollama"},
            },
            "modelos": {"por_proveedor": {"gemini": {"default": "gemini-2.5-pro"},
                                           "deepseek": {"default": "deepseek-v4-flash"}}},
        }
        r = evaluar_horario(state, policies)
        self.assertIsNotNone(r)
        self.assertEqual(r["provider"], "gemini")

    def test_franja_tarde(self):
        """12:00-03:00 (cruza medianoche) → deepseek"""
        state = {"policies": {"hora": {"actual": "15:00", "franja_activa": "12:00-03:00"}}}
        policies = {
            "horario": {
                "reglas": [
                    {"horas": "03:00-12:00", "proveedor": "gemini"},
                    {"horas": "12:00-03:00", "proveedor": "deepseek"},
                ],
                "fallback": {"proveedor": "ollama"},
            },
            "modelos": {"por_proveedor": {"deepseek": {"default": "deepseek-v4-flash"}}},
        }
        r = evaluar_horario(state, policies)
        self.assertIsNotNone(r)
        self.assertEqual(r["provider"], "deepseek")

    def test_franja_madrugada(self):
        """Después de medianoche pero antes de 03:00 → deepseek (sigue la regla 12:00-03:00)"""
        state = {"policies": {"hora": {"actual": "01:00", "franja_activa": "12:00-03:00"}}}
        policies = {
            "horario": {
                "reglas": [
                    {"horas": "03:00-12:00", "proveedor": "gemini"},
                    {"horas": "12:00-03:00", "proveedor": "deepseek"},
                ],
                "fallback": {"proveedor": "ollama"},
            },
            "modelos": {"por_proveedor": {"deepseek": {"default": "deepseek-v4-flash"}}},
        }
        r = evaluar_horario(state, policies)
        self.assertIsNotNone(r)
        self.assertEqual(r["provider"], "deepseek")

    def test_sin_hora_en_state(self):
        state = {"policies": {"hora": {}}}
        policies = {"horario": {"reglas": [], "fallback": {"proveedor": "ollama"}}}
        r = evaluar_horario(state, policies)
        self.assertIsNone(r)


class TestEvaluarPreferencias(unittest.TestCase):
    """Política 5: fallback por defecto"""

    def test_preferencias_devuelve_siempre(self):
        state = {}
        policies = {}
        r = evaluar_preferencias(state, policies)
        self.assertIsNotNone(r)
        self.assertEqual(r["provider"], "deepseek")
        self.assertEqual(r["model"], "deepseek-v4-flash")
        self.assertIn("Preferencia por defecto", r["reason"])


class TestDecide(unittest.TestCase):
    """Test completo de decide() con state.json simulado"""

    def setUp(self):
        # Guardar rutas originales
        self.original_state_file = Path("/mnt/ssd_ia_datos/lab-state/state.json")

    def _crear_state_temporal(self, data: dict):
        """Crea un state.json temporal y devuelve la ruta."""
        path = Path(tempfile.mktemp(suffix=".json"))
        path.write_text(json.dumps(data))
        return path

    def test_decide_con_state_valido(self):
        """Con state.json válido en horario diurno, debe elegir deepseek."""
        state = {
            "timestamp": "2026-07-14T15:00:00",
            "gpu": {"modelo": "RTX A2000", "vram_total_mb": 12282, "vram_usada_mb": 500,
                    "vram_libre_mb": 11000, "temp_c": 45, "utilizacion_pct": 10},
            "system": {"ram_total_gb": 30, "ram_libre_gb": 10, "ram_disponible_gb": 20,
                       "cpu_load": 1.0, "disco_root_libre_gb": 300, "disco_ssd_libre_gb": 130},
            "services": {"ollama": {"activo": True, "version": "0.30", "modelos": ["llama31-8b-64k"],
                                    "modelo_cargado": None},
                         "lmstudio": {"activo": False, "version": None, "modelos": []},
                         "n8n": {"activo": True, "version": "2.27.4"},
                         "stirling_pdf": {"activo": True},
                         "pdf_cleaner": {"activo": True},
                         "monitor_flask": {"activo": False}},
            "cloud": {"deepseek": {"disponible": True, "saldo_usd": None, "latencia_ms": None},
                      "gemini": {"disponible": True, "saldo_usd": None, "latencia_ms": None}},
            "policies": {"hora": {"actual": "15:00", "franja_activa": "12:00-03:00"},
                         "ahorro": {"activo": False}},
        }
        path = self._crear_state_temporal(state)

        # Monkey-patch la ruta del state_file
        import decision_engine as de
        original = de.STATE_FILE
        de.STATE_FILE = path

        try:
            r = decide()
            self.assertIn("provider", r)
            self.assertIn("model", r)
            self.assertIn("reason", r)
            # decide() añade timestamp (commit 205e683, 29-jul) -> 4 campos
            self.assertEqual(len(r), 4)
            # En franja 12:00-03:00 con todo disponible, debe ser deepseek
            self.assertEqual(r["provider"], "deepseek")
        finally:
            de.STATE_FILE = original
            os.unlink(path)

    def test_decide_state_no_existe_fallback(self):
        """Si no hay state.json, debe caer al fallback. No asume proveedor (depende de hora real)."""
        import decision_engine as de
        original = de.STATE_FILE
        de.STATE_FILE = Path(tempfile.mktemp(suffix=".inexistente"))

        try:
            r = decide()
            self.assertIn(r["provider"], ("deepseek", "gemini", "ollama"))
            self.assertIn("FALLBACK", r["reason"])
        finally:
            de.STATE_FILE = original

    def test_decide_privacidad_gana(self):
        """Si datos_sensibles=true, debe forzar ollama aunque el horario diga deepseek."""
        state = {
            "timestamp": "2026-07-14T15:00:00",
            "gpu": {}, "system": {},
            "services": {"ollama": {"activo": True, "version": None, "modelos": [], "modelo_cargado": None},
                         "lmstudio": {"activo": False, "version": None, "modelos": []},
                         "n8n": {"activo": True, "version": None},
                         "stirling_pdf": {"activo": True},
                         "pdf_cleaner": {"activo": True},
                         "monitor_flask": {"activo": False}},
            "cloud": {"deepseek": {"disponible": True, "saldo_usd": None, "latencia_ms": None},
                      "gemini": {"disponible": True, "saldo_usd": None, "latencia_ms": None}},
            "policies": {"hora": {"actual": "15:00", "franja_activa": "12:00-03:00"},
                         "ahorro": {"activo": False}},
        }
        path = self._crear_state_temporal(state)

        import decision_engine as de
        original_s = de.STATE_FILE
        de.STATE_FILE = path

        # Crear una política de privacidad con datos_sensibles=true
        tmp_policies = Path(tempfile.mktemp(suffix=".yaml"))
        tmp_policies.write_text("datos_sensibles: true\nniveles: []\n")
        original_policies = de.POLICIES_DIR
        de.POLICIES_DIR = tmp_policies.parent

        try:
            # Crear un archivo privacidad.yaml en el directorio temporal
            priv_yaml = tmp_policies.parent / "privacidad.yaml"
            priv_yaml.write_text("datos_sensibles: true\nniveles: []\n")
            # Necesitamos modelos.yaml para que el DE pueda resolver el modelo de ollama
            mod_yaml = tmp_policies.parent / "modelos.yaml"
            mod_yaml.write_text("por_proveedor:\n  ollama:\n    default: llama31-8b-64k\n")

            r = decide()
            self.assertEqual(r["provider"], "ollama")
        finally:
            de.STATE_FILE = original_s
            de.POLICIES_DIR = original_policies
            os.unlink(path)
            if priv_yaml.exists():
                os.unlink(priv_yaml)
            if mod_yaml.exists():
                os.unlink(mod_yaml)
            tmp_policies.unlink()


class TestLoadState(unittest.TestCase):
    """Test de carga de estado"""

    def test_load_state_no_existe(self):
        path = Path(tempfile.mktemp(suffix=".json"))
        try:
            import decision_engine as de
            original = de.STATE_FILE
            de.STATE_FILE = path
            r = load_state()
            self.assertEqual(r, {})
            de.STATE_FILE = original
        finally:
            path.unlink() if path.exists() else None

    def test_load_state_json_invalido(self):
        path = Path(tempfile.mktemp(suffix=".json"))
        path.write_text("{esto no es json}")
        try:
            import decision_engine as de
            original = de.STATE_FILE
            de.STATE_FILE = path
            r = load_state()
            self.assertEqual(r, {})
            de.STATE_FILE = original
        finally:
            path.unlink()


class TestLoadUltimaDecision(unittest.TestCase):
    """Test de carga de última decisión (fallback)"""

    def test_cuando_existe(self):
        path = Path(tempfile.mktemp(suffix=".json"))
        path.write_text('{"provider": "test", "model": "test-model", "reason": "test"}')
        try:
            import decision_engine as de
            original = de.ULTIMA_DECISION
            de.ULTIMA_DECISION = path
            r = load_ultima_decision()
            self.assertIsNotNone(r)
            self.assertEqual(r["provider"], "test")
            de.ULTIMA_DECISION = original
        finally:
            path.unlink()

    def test_cuando_no_existe(self):
        path = Path(tempfile.mktemp(suffix=".inexistente"))
        try:
            import decision_engine as de
            original = de.ULTIMA_DECISION
            de.ULTIMA_DECISION = path
            r = load_ultima_decision()
            self.assertIsNone(r)
            de.ULTIMA_DECISION = original
        finally:
            path.unlink() if path.exists() else None


if __name__ == "__main__":
    unittest.main(verbosity=2)
