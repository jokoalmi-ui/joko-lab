#!/usr/bin/env python3
"""
Tests de las funciones extraidas de migrate_dec() (refactor 07-ago-2026 con
OpenCode): _inferir_tipo y _inferir_confianza.

Red de seguridad: dry-run del migrador identico antes/despues (sin --apply,
solo lectura) + estos tests fijan el comportamiento.

Ejecucion:
  cd ~/joko-lab && python3 -m unittest tests/test_migrate_to_ko.py -v
"""

import sys
import unittest
from datetime import datetime, timedelta
from pathlib import Path

TOOLS_DIR = str(Path(__file__).resolve().parent.parent / "tools")
sys.path.insert(0, TOOLS_DIR)

from migrate_to_ko import (
    _inferir_tipo, _inferir_confianza,
    _construir_ko_base, _preservar_legacy_fields,
)


class TestInferirTipo(unittest.TestCase):
    def test_rules_por_carpeta(self):
        self.assertEqual(_inferir_tipo(Path("/x/rules/dec.yaml"), {}), "RULE")

    def test_policies_por_carpeta(self):
        self.assertEqual(_inferir_tipo(Path("/x/policies/dec.yaml"), {}), "POLICY")

    def test_type_explicito(self):
        self.assertEqual(_inferir_tipo(Path("/x/decisions/dec.yaml"), {"type": "DEC"}), "DEC")

    def test_default_decisión(self):
        self.assertEqual(_inferir_tipo(Path("/x/decisions/dec.yaml"), {}), "DEC")


class TestInferirConfianza(unittest.TestCase):
    def test_alta(self):
        self.assertEqual(_inferir_confianza(0.9, None), (0.9, "ALTA"))

    def test_media(self):
        self.assertEqual(_inferir_confianza(0.6, None), (0.6, "MEDIA"))

    def test_baja(self):
        self.assertEqual(_inferir_confianza(0.3, None), (0.3, "BAJA"))

    def test_none(self):
        self.assertEqual(_inferir_confianza(None, None), (None, "NO_EVALUADA"))

    def test_validaciones_3_sin_confianza(self):
        self.assertEqual(_inferir_confianza(None, 3), (0.85, "ALTA"))

    def test_validaciones_1_sin_confianza(self):
        # >=1 sube confidence pero NO toca el label (solo >=3 lo hace)
        self.assertEqual(_inferir_confianza(None, 1), (0.70, "NO_EVALUADA"))

    def test_validaciones_3_con_confianza_baja(self):
        # el label se sobreescribe a ALTA; confidence no cambia (no es None)
        self.assertEqual(_inferir_confianza(0.3, 3), (0.3, "ALTA"))

    def test_validaciones_2_sin_confianza(self):
        self.assertEqual(_inferir_confianza(None, 2), (0.70, "NO_EVALUADA"))

    def test_validaciones_cero(self):
        self.assertEqual(_inferir_confianza(None, 0), (None, "NO_EVALUADA"))

    def test_validaciones_no_numericas(self):
        self.assertEqual(_inferir_confianza(None, "tres"), (None, "NO_EVALUADA"))


class TestConstruirKoBase(unittest.TestCase):
    """Tests de _construir_ko_base (extraida 08-ago-2026)."""

    def setUp(self):
        self.created = datetime(2026, 1, 15, 12, 0)

    def test_estructura_y_campos_calculados(self):
        ko = _construir_ko_base("DEC-999", "DEC", self.created, None,
                                0.9, "ALTA", ["EXP-001"], "Cuerpo")
        self.assertEqual(ko["id"], "DEC-999")
        self.assertEqual(ko["type"], "DEC")
        self.assertEqual(ko["status"], "activo")
        self.assertEqual(ko["version"], 1)
        self.assertEqual(ko["created"], "2026-01-15")
        self.assertIsNone(ko["last_validated"])
        # next_review = created + 3*30 dias; expires = created + 6*30 dias
        self.assertEqual(ko["next_review"], "2026-04-15")
        self.assertEqual(ko["expires"], "2026-07-14")
        self.assertEqual(ko["confidence"], 0.9)
        self.assertEqual(ko["confidence_label"], "ALTA")
        self.assertEqual(ko["evidence"], ["EXP-001"])
        self.assertEqual(ko["dependencies"], [])
        self.assertEqual(ko["contradicts"], [])
        self.assertIsNone(ko["superseded_by"])
        self.assertEqual(ko["domain"], "ai-architecture")
        self.assertEqual(ko["scope"], "todo_joko_lab")
        self.assertEqual(ko["body"], "Cuerpo")
        self.assertEqual(ko["legacy_fields"], {})
        self.assertEqual(ko["history"][0]["event"], "created")

    def test_last_validated_presente(self):
        lv = datetime(2026, 2, 1)
        ko = _construir_ko_base("R-1", "RULE", self.created, lv,
                                0.5, "MEDIA", [], "x")
        self.assertEqual(ko["last_validated"], "2026-02-01")

    def test_orden_de_claves(self):
        # El orden de claves es parte del contrato (se mantiene al serializar)
        ko = _construir_ko_base("P-1", "POLICY", self.created, None,
                                0.3, "BAJA", [], "")
        claves = list(ko.keys())
        self.assertEqual(claves[0], "id")
        self.assertEqual(claves[1], "type")
        self.assertEqual(claves[-1], "legacy_fields")
        self.assertLess(claves.index("history"), claves.index("legacy_fields"))


class TestPreservarLegacyFields(unittest.TestCase):
    """Tests de _preservar_legacy_fields (extraida 08-ago-2026)."""

    def _base(self):
        return {"dependencies": [], "legacy_fields": {}}

    def test_origen_a_dependencies(self):
        ko = self._base()
        _preservar_legacy_fields(ko, {"origen": "EXP-001"})
        self.assertEqual(ko["dependencies"], ["EXP-001"])

    def test_campos_legacy(self):
        ko = self._base()
        old = {
            "condicion": {"keywords": ["hola"]},
            "accion": {"modelo": "granite"},
            "prioridad": 80,
            "activa": True,
            "nota": "Nota",
            "alcance": "todo",
            "validaciones": 3,
        }
        _preservar_legacy_fields(ko, old)
        self.assertEqual(ko["legacy_fields"]["condicion"], {"keywords": ["hola"]})
        self.assertEqual(ko["legacy_fields"]["accion"], {"modelo": "granite"})
        self.assertEqual(ko["legacy_fields"]["prioridad"], 80)
        self.assertIs(ko["legacy_fields"]["activa"], True)
        self.assertEqual(ko["legacy_fields"]["nota"], "Nota")
        self.assertEqual(ko["legacy_fields"]["alcance"], "todo")
        self.assertEqual(ko["legacy_fields"]["validaciones"], 3)

    def test_prioridad_cero_se_preserva(self):
        # prioridad 0 es valor valido (is not None, no truthiness)
        ko = self._base()
        _preservar_legacy_fields(ko, {"prioridad": 0})
        self.assertEqual(ko["legacy_fields"]["prioridad"], 0)

    def test_activa_false_se_preserva(self):
        ko = self._base()
        _preservar_legacy_fields(ko, {"activa": False})
        self.assertIs(ko["legacy_fields"]["activa"], False)

    def test_vacio_no_muta(self):
        ko = self._base()
        _preservar_legacy_fields(ko, {})
        self.assertEqual(ko, {"dependencies": [], "legacy_fields": {}})


if __name__ == "__main__":
    unittest.main()
