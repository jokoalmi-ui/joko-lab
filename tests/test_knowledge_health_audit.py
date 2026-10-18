#!/usr/bin/env python3
"""
Tests de las funciones extraidas de audit() (refactor 07-ago-2026 con OpenCode):
_procesar_ko, _detectar_contradicciones, _calcular_health.

Red de seguridad del refactor: la salida completa del script se verifico
identica (diff JSON) y estos tests fijan el comportamiento de cada pieza.

Ejecucion:
  cd ~/joko-lab && python3 -m unittest tests/test_knowledge_health_audit.py -v
"""

import os
import sys
import tempfile
import unittest
from collections import defaultdict
from datetime import timedelta
from pathlib import Path

TOOLS_DIR = str(Path(__file__).resolve().parent.parent / "tools")
sys.path.insert(0, TOOLS_DIR)

import knowledge_health as kh


def stats_issues():
    # audit() usa defaultdict(int) en produccion; el contrato de _procesar_ko
    # y _detectar_contradicciones es ese mismo tipo.
    return defaultdict(int), []


def path_ko_ficticio(stem="RULE-TEST"):
    # Ruta bajo LAB_ROOT (no necesita existir: _procesar_ko solo usa stem y relative_to)
    return Path(str(kh.LAB_ROOT)) / "01-knowledge" / "objects" / f"{stem}.yaml"


class TestProcesarKo(unittest.TestCase):
    def test_sin_fecha_expiracion(self):
        stats, issues = stats_issues()
        item = kh._procesar_ko(
            path_ko_ficticio(), {"status": "activo"}, "RULE",
            None, kh.NOW, None, 0.9, "activo", ["fuente"], stats, issues)
        self.assertEqual(item["id"], "RULE-TEST")
        self.assertEqual(item["type"], "RULE")
        self.assertTrue(any("sin fecha de expiración" in i for i in issues))
        # Clave real con tilde (heredada del original; no se cambia para no
        # alterar la salida del JSON)
        self.assertEqual(stats["sin_expiración"], 1)

    def test_expirada(self):
        stats, issues = stats_issues()
        kh._procesar_ko(
            path_ko_ficticio("DEC-EXP"), {}, "DEC",
            None, kh.NOW, kh.NOW - timedelta(days=10), 0.9, "activo",
            ["fuente"], stats, issues)
        self.assertTrue(any("EXPIRADA" in i for i in issues))
        self.assertEqual(stats["expiradas"], 1)

    def test_confianza_baja(self):
        stats, issues = stats_issues()
        kh._procesar_ko(
            path_ko_ficticio(), {}, "RULE",
            None, kh.NOW, kh.NOW + timedelta(days=60), 0.4, "activo",
            ["fuente"], stats, issues)
        self.assertTrue(any("confianza baja" in i for i in issues))
        self.assertEqual(stats["confianza_baja"], 1)

    def test_sin_evidencia(self):
        stats, issues = stats_issues()
        kh._procesar_ko(
            path_ko_ficticio(), {"dependencies": []}, "RULE",
            None, kh.NOW, kh.NOW + timedelta(days=60), 0.9, "activo",
            [], stats, issues)
        self.assertTrue(any("sin evidencia" in i for i in issues))
        self.assertEqual(stats["sin_evidencia"], 1)

    def test_con_evidencia_directa_no_avisa(self):
        stats, issues = stats_issues()
        kh._procesar_ko(
            path_ko_ficticio(), {}, "RULE",
            None, kh.NOW, kh.NOW + timedelta(days=60), 0.9, "activo",
            ["EXP-2026-001"], stats, issues)
        self.assertFalse(any("sin evidencia" in i for i in issues))

    def test_retirado(self):
        stats, issues = stats_issues()
        kh._procesar_ko(
            path_ko_ficticio(), {}, "DEC",
            None, kh.NOW, kh.NOW + timedelta(days=60), 0.9, "retirado",
            ["fuente"], stats, issues)
        self.assertEqual(stats["decs_retired"], 1)


class TestDetectarContradicciones(unittest.TestCase):
    def test_detecta_conflicto(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            (base / "a.md").write_text(
                "qwen 3.5 es el modelo preferido para razonamiento "
                "y genera codigo estable y rapido y fiable", encoding="utf-8")
            (base / "b.md").write_text(
                "qwen 3.5 esta descartado como modelo para razonamiento "
                "y genera codigo inestable y lento y falla", encoding="utf-8")
            stats, _ = stats_issues()
            dec_items = [
                {"id": "DEC-A", "path": "a.md"},
                {"id": "DEC-B", "path": "b.md"},
            ]
            contradictions = kh._detectar_contradicciones(dec_items, stats, base_dir=base)
            self.assertEqual(len(contradictions), 1)
            self.assertEqual(stats["contradicciones"], 1)

    def test_sin_conflicto(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            (base / "a.md").write_text("el cielo es azul y el sol brilla", encoding="utf-8")
            (base / "b.md").write_text("la lluvia moja la calle y el asfalto", encoding="utf-8")
            stats, _ = stats_issues()
            dec_items = [
                {"id": "DEC-A", "path": "a.md"},
                {"id": "DEC-B", "path": "b.md"},
            ]
            contradictions = kh._detectar_contradicciones(dec_items, stats, base_dir=base)
            self.assertEqual(contradictions, [])


class TestCalcularHealth(unittest.TestCase):
    def test_vacio_cien(self):
        self.assertEqual(kh._calcular_health({}), 100)

    def test_una_expirada(self):
        self.assertEqual(kh._calcular_health({"expiradas": 1}), 95)

    def test_clamp_minimo_cero(self):
        self.assertEqual(kh._calcular_health({"expiradas": 30}), 0)

    def test_combinacion(self):
        stats = {"expiradas": 2, "sin_validar": 1}
        self.assertEqual(kh._calcular_health(stats), 87)


class TestChequearEstructuraMd(unittest.TestCase):
    def test_documento_completo(self):
        txt = ("---\ntitle: X\n---\n"
               "# H1\n## H2\n### H3\n"
               "texto con [[wikilink]]\n")
        flags = kh._chequear_estructura_md(txt)
        self.assertTrue(flags["has_fm"])
        self.assertTrue(flags["has_h1"])
        self.assertTrue(flags["has_h2"])
        self.assertTrue(flags["has_h3"])
        self.assertTrue(flags["has_enlaces"])

    def test_documento_vacio(self):
        flags = kh._chequear_estructura_md("solo texto sin estructura\n")
        self.assertFalse(flags["has_fm"])
        self.assertFalse(flags["has_h1"])
        self.assertFalse(flags["has_h2"])
        self.assertFalse(flags["has_h3"])
        self.assertFalse(flags["has_enlaces"])

    def test_enlace_markdown(self):
        flags = kh._chequear_estructura_md("ver [enlace](https://ejemplo.com)\n")
        self.assertTrue(flags["has_enlaces"])

    def test_frontmatter_incompleto(self):
        flags = kh._chequear_estructura_md("---\ntitle: sin cierre\n# H1\n")
        self.assertFalse(flags["has_fm"])

    def test_h1_sin_espacio_no_cuenta(self):
        # "#H1" (sin espacio) no debe contar como H1 (regex "^#\s")
        flags = kh._chequear_estructura_md("#H1 sin espacio\n")
        self.assertFalse(flags["has_h1"])


if __name__ == "__main__":
    unittest.main()
