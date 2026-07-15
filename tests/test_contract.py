#!/usr/bin/env python3
"""
Test de contrato: verifica que Runtime.resolve() cumple CONTRACT.md v1.0.

Evalúa:
- Los 9 campos obligatorios están presentes
- Tipos correctos
- Campos en estados de error
- decision_id único
- consistency provider/model
"""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from runtime.api import resolve, _generar_decision_id


class TestContratoCamposObligatorios(unittest.TestCase):
    """Sección 3 del CONTRACT.md: campos obligatorios"""

    def setUp(self):
        self.decision = resolve()

    def test_tiene_9_campos(self):
        """El contrato define 9 campos obligatorios."""
        required = ["provider", "model", "reason", "policy",
                    "privacy", "verification", "confidence",
                    "expires", "decision_id"]
        for field in required:
            self.assertIn(field, self.decision,
                          f"Campo obligatorio '{field}' falta en la decisión")

    def test_provider_no_vacio(self):
        self.assertIsInstance(self.decision["provider"], str)
        self.assertNotEqual(self.decision["provider"], "")

    def test_model_no_vacio(self):
        self.assertIsInstance(self.decision["model"], str)
        self.assertNotEqual(self.decision["model"], "")

    def test_reason_no_vacio(self):
        self.assertIsInstance(self.decision["reason"], str)
        self.assertNotEqual(self.decision["reason"], "")

    def test_policy_no_vacio(self):
        self.assertIsInstance(self.decision["policy"], str)
        self.assertNotEqual(self.decision["policy"], "")

    def test_privacy_valido(self):
        """privacy debe ser 'cloud', 'local' o 'unknown'."""
        self.assertIn(self.decision["privacy"], ("cloud", "local", "unknown"))

    def test_verification_valido(self):
        """verification debe ser LOW, MEDIUM, HIGH o NONE."""
        self.assertIn(self.decision["verification"], ("LOW", "MEDIUM", "HIGH", "NONE"))

    def test_confidence_en_rango(self):
        """confidence debe estar entre 0.0 y 1.0."""
        c = self.decision["confidence"]
        self.assertIsInstance(c, (int, float))
        self.assertGreaterEqual(c, 0.0)
        self.assertLessEqual(c, 1.0)

    def test_decision_id_formato(self):
        """decision_id debe tener formato YYYYMMDD-HHMMSS-xxxxxxxx."""
        did = self.decision["decision_id"]
        self.assertIsInstance(did, str)
        self.assertRegex(did, r"^\d{8}-\d{6}-[a-f0-9]{8}$")

    def test_expires_formato_iso(self):
        """expires debe ser ISO 8601 o None."""
        exp = self.decision["expires"]
        if exp is not None:
            self.assertIsInstance(exp, str)
            # Formato ISO básico: contiene T y zona horaria
            self.assertIn("T", exp)


class TestContratoConsistencia(unittest.TestCase):
    """Sección 3.2 del CONTRACT.md: estados válidos"""

    def test_provider_model_consistentes(self):
        """provider y model deben ser consistentes (ninguno 'none' con modelo válido)."""
        d = resolve()
        if d["provider"] == "none":
            self.assertEqual(d["model"], "none")
            self.assertEqual(d["confidence"], 0.0)
        else:
            self.assertNotEqual(d["model"], "none")
            self.assertGreater(d["confidence"], 0.0)

    def test_decision_id_unico(self):
        """Dos llamadas a resolve() deben generar decision_id distintos."""
        d1 = resolve()
        d2 = resolve()
        self.assertNotEqual(d1["decision_id"], d2["decision_id"])

    def test_decision_id_generador(self):
        """_generar_decision_id() debe producir IDs únicos."""
        ids = {_generar_decision_id() for _ in range(100)}
        self.assertEqual(len(ids), 100)


class TestContratoEstadosError(unittest.TestCase):
    """Sección 3.3 del CONTRACT.md: códigos de error"""

    def test_error_state_no_disponible(self):
        """Si no hay state.json, debe caer a fallback. Reason debe contener 'FALLBACK'."""
        import decision_engine as de
        original = de.STATE_FILE
        de.STATE_FILE = Path(tempfile.mktemp(suffix=".inexistente"))

        try:
            d = resolve()
            # El proveedor puede variar según la hora real, pero debe tener fallback
            self.assertIn("FALLBACK", d["reason"])
            self.assertIn(d["provider"], ("deepseek", "gemini", "ollama"))
            self.assertIn(d["privacy"], ("cloud", "local"))
        finally:
            de.STATE_FILE = original


class TestContratoTipos(unittest.TestCase):
    """Sección 3.1 del CONTRACT.md: tipos de cada campo"""

    def test_tipos_correctos(self):
        d = resolve()
        self.assertIsInstance(d["provider"], str)
        self.assertIsInstance(d["model"], str)
        self.assertIsInstance(d["reason"], str)
        self.assertIsInstance(d["policy"], str)
        self.assertIsInstance(d["privacy"], str)
        self.assertIsInstance(d["verification"], str)
        self.assertIsInstance(d["confidence"], (int, float))
        self.assertIsInstance(d["decision_id"], str)
        # expires puede ser string o None
        self.assertTrue(d["expires"] is None or isinstance(d["expires"], str))


class TestDecisionLedger(unittest.TestCase):
    """Verifica que resolve() escribe en decision-ledger.json"""

    def setUp(self):
        import runtime.api as api
        self.ledger_path = api.DECISION_LEDGER
        # Guardar ledger actual si existe
        self.old_content = None
        if self.ledger_path.exists():
            self.old_content = self.ledger_path.read_text()

    def tearDown(self):
        # Restaurar ledger original
        if self.old_content is not None:
            self.ledger_path.write_text(self.old_content)
        elif self.ledger_path.exists():
            self.ledger_path.unlink()

    def test_ledger_se_crea(self):
        """resolve() debe crear/actualizar el ledger."""
        from runtime.api import resolve
        # Forzar decisión para que se registre en el ledger
        d = resolve()
        self.assertTrue(self.ledger_path.exists(),
                        "decision-ledger.json debería existir tras resolve()")
        entries = json.loads(self.ledger_path.read_text())
        self.assertIsInstance(entries, list)
        self.assertGreater(len(entries), 0)
        ultima = entries[-1]
        self.assertEqual(ultima["decision_id"], d["decision_id"])
        self.assertIn("reason", ultima)
        self.assertIsInstance(ultima["reason"], list)
        self.assertIn("latency_ms", ultima)
        self.assertIn("fallback", ultima)
        self.assertIn("privacy", ultima)


if __name__ == "__main__":
    unittest.main(verbosity=2)
