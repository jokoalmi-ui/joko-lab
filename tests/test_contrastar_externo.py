#!/usr/bin/env python3
"""
Tests de contrastar_externo.py (gate externo de veracidad, fase 3, 16-ago-2026).

Verifica el flujo agente+script: sin fuente → BUSCAR; con fuentes aportadas →
VERIFICADO; estado interno → ALCANCE_INTERNO. También la extracción de keywords.

Ejecucion:
  cd ~/joko-lab && python3 -m unittest tests/test_contrastar_externo.py -v
"""

import sys
import unittest
from pathlib import Path

TOOLS_DIR = str(Path(__file__).resolve().parent.parent / "tools")
sys.path.insert(0, TOOLS_DIR)

from contrastar_externo import extraer_keywords
from verificador_alucinaciones import verificar


class TestExtraerKeywords(unittest.TestCase):
    def test_extrae_entidades_y_numeros(self):
        kws = extraer_keywords("La inflación en España fue del 3,6% en 2024.")
        # Entidades (España) + números (3,6 / 2024)
        self.assertIn("España", kws)
        self.assertIn("3,6", kws)

    def test_sin_entidades_devuelve_texto(self):
        kws = extraer_keywords("hay un dato curioso por aquí")
        self.assertTrue(len(kws) > 0)


class TestFlujoExterno(unittest.TestCase):
    def test_sin_fuente_bloquea(self):
        r = verificar("La inflación interanual en España fue del 2,6% en agosto de 2024.",
                      tema="inflación España")
        self.assertEqual(r["veredicto"], "BLOQUEADO_SIN_FUENTE")

    def test_con_fuentes_verificado(self):
        r = verificar(
            "La inflación interanual en España fue del 2,6% en agosto de 2024. [VERIFICADO] https://www.ine.es",
            tema="inflación España")
        self.assertEqual(r["veredicto"], "OK")
        self.assertEqual(r["etiqueta"], "[VERIFICADO]")

    def test_estado_interno_no_busca(self):
        r = verificar("El lab tiene 222 tests y 0 servicios caídos, GPU a 42°C.",
                      tema="estado Joko Lab")
        self.assertEqual(r["veredicto"], "OK_INTERNO")
        self.assertEqual(r["etiqueta"], "[ALCANCE INTERNO]")


if __name__ == "__main__":
    unittest.main()
