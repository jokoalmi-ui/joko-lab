#!/usr/bin/env python3
"""test_local_cloud_orchestrator.py — pruebas del clasificador y verifier del
orquestador local-first (22-ago-2026). Sin red: solo funciones puras.

Uso: cd ~/joko-lab && python3 -m unittest tests/test_local_cloud_orchestrator.py
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import local_cloud_orchestrator as o


class TestClasificarTipo(unittest.TestCase):

    def test_batch_json(self):
        self.assertEqual(o.clasificar_tipo("extrae en json los datos"), "batch-json")

    def test_json_keyword(self):
        self.assertEqual(o.clasificar_tipo("dame solo json"), "batch-json")

    def test_vision(self):
        self.assertEqual(o.clasificar_tipo("describe la imagen"), "vision")

    def test_razonamiento(self):
        self.assertEqual(o.clasificar_tipo("razona quien es mayor si A>B"), "razonamiento")

    def test_batch_default(self):
        self.assertEqual(o.clasificar_tipo("resume este texto"), "batch")


class TestVerifier(unittest.TestCase):

    def test_json_valido(self):
        self.assertEqual(o._verificar_json('{"a": 1}'), (True, "json_valido"))

    def test_json_vacio(self):
        self.assertEqual(o._verificar_json("{}"), (False, "json_vacio"))

    def test_json_invalido(self):
        self.assertFalse(o._verificar_json("{a: 1}")[0])

    def test_json_fences(self):
        self.assertEqual(o._verificar_json('```json\n{"a": 1}\n```'), (True, "json_valido"))

    def test_batch_corto(self):
        self.assertFalse(o._verificar_batch("a")[0])

    def test_batch_error_motor(self):
        self.assertFalse(o._verificar_batch("ERROR: ningun modelo local cargado")[0])

    def test_batch_ok(self):
        self.assertEqual(o._verificar_batch("respuesta normal y completa"), (True, "contenido_ok"))

    def test_verifier_vacio(self):
        self.assertFalse(o.verifier("batch", "   ")[0])

    def test_razonamiento_no_verificable(self):
        self.assertFalse(o.verifier("razonamiento", "cualquier cosa")[0])

    def test_vision_asumida(self):
        self.assertTrue(o.verifier("vision", "descripción visual")[0])


if __name__ == "__main__":
    unittest.main()
