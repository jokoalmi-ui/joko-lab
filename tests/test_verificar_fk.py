#!/usr/bin/env python3
"""
Tests de las funciones extraidas de escanear_ko() (refactor 07-ago-2026 con
OpenCode): _escanear_estructurados y _revisar_texto.

Red de seguridad: salida JSON del detector verificada identica antes/despues
y estos tests fijan el comportamiento de cada pieza.

Ejecucion:
  cd ~/joko-lab && python3 -m unittest tests/test_verificar_fk.py -v
"""

import sys
import unittest
from pathlib import Path

TOOLS_DIR = str(Path(__file__).resolve().parent.parent / "tools")
sys.path.insert(0, TOOLS_DIR)

from verificar_fk_kos import _escanear_estructurados, _revisar_texto

IDS_VALIDOS = {"RULE-001", "DEC-001", "POLICY-002"}
RUTA = Path("/tmp/ficticio.yaml")


class TestEscanearEstructurados(unittest.TestCase):
    def test_dependencies_rota(self):
        data = {"dependencies": ["RULE-999"]}
        rotas = []
        _escanear_estructurados(data, RUTA, "KO-1", IDS_VALIDOS, rotas)
        self.assertEqual(len(rotas), 1)
        self.assertEqual(rotas[0][2], "dependencies")
        self.assertEqual(rotas[0][3], "RULE-999")
        self.assertEqual(rotas[0][4], "structured")

    def test_dependencies_validas_no_avisan(self):
        data = {"dependencies": ["RULE-001", "DEC-001"]}
        rotas = []
        _escanear_estructurados(data, RUTA, "KO-1", IDS_VALIDOS, rotas)
        self.assertEqual(rotas, [])

    def test_dependencies_como_string(self):
        data = {"dependencies": "RULE-999"}
        rotas = []
        _escanear_estructurados(data, RUTA, "KO-1", IDS_VALIDOS, rotas)
        self.assertEqual(len(rotas), 1)
        self.assertEqual(rotas[0][3], "RULE-999")

    def test_superseded_by_roto(self):
        data = {"superseded_by": "DEC-777"}
        rotas = []
        _escanear_estructurados(data, RUTA, "KO-1", IDS_VALIDOS, rotas)
        self.assertEqual(len(rotas), 1)
        self.assertEqual(rotas[0][2], "superseded_by")
        self.assertEqual(rotas[0][4], "structured")

    def test_prefijo_no_ko_se_ignora(self):
        # EXP-, JL-, CP- no son FK de KO: no deben aparecer como rotas
        data = {"dependencies": ["EXP-20260807-001", "JL-014"]}
        rotas = []
        _escanear_estructurados(data, RUTA, "KO-1", IDS_VALIDOS, rotas)
        self.assertEqual(rotas, [])


class TestRevisarTexto(unittest.TestCase):
    def test_mencion_inexistente(self):
        rotas = []
        _revisar_texto("menciona RULE-CONF-001 en el texto", "body",
                       RUTA, "KO-1", IDS_VALIDOS, rotas)
        self.assertEqual(len(rotas), 1)
        self.assertEqual(rotas[0][3], "RULE-CONF-001")
        self.assertEqual(rotas[0][4], "prosa")

    def test_menciones_validas_no_avisan(self):
        rotas = []
        _revisar_texto("usa RULE-001 y DEC-001", "body",
                       RUTA, "KO-1", IDS_VALIDOS, rotas)
        self.assertEqual(rotas, [])

    def test_no_str_no_rompe(self):
        rotas = []
        _revisar_texto(None, "body", RUTA, "KO-1", IDS_VALIDOS, rotas)
        _revisar_texto(123, "body", RUTA, "KO-1", IDS_VALIDOS, rotas)
        self.assertEqual(rotas, [])


if __name__ == "__main__":
    unittest.main()
