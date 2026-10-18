#!/usr/bin/env python3
"""test_buscar_perfume.py — pruebas del pre-filter del RAG de perfume-ia
(limpiar_query, 22-ago-2026). Función pura, sin BD ni LanceDB.

Uso (venv RAG, donde está lancedb):
  ~/.venv/hermes-rag/bin/python3 -m unittest tests/test_buscar_perfume.py
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path.home() / "perfume-ia" / "modules" / "04-rag"))
try:
    import buscar_perfume as bp
    DISPONIBLE = True
except ImportError as e:  # buscar_perfume importa lancedb (solo en el venv RAG)
    DISPONIBLE = False
    _IMPORT_ERR = str(e)


@unittest.skipUnless(DISPONIBLE,
                     "buscar_perfume requiere lancedb: usar ~/.venv/hermes-rag/bin/python3")
class TestLimpiarQuery(unittest.TestCase):

    def test_quita_stopwords(self):
        self.assertEqual(
            bp.limpiar_query("hoy quiero un perfume fresco"),
            "fresco")

    def test_conserva_terminos_clave(self):
        self.assertEqual(
            bp.limpiar_query("quiero algo cítrico para el verano"),
            "cítrico verano")

    def test_solo_stopwords_vacio(self):
        self.assertEqual(bp.limpiar_query("hoy el perfume que"), "")

    def test_sin_stopwords_intacto(self):
        self.assertEqual(bp.limpiar_query("oud amaderado intenso"),
                         "oud amaderado intenso")

    def test_mayusculas_normalizadas(self):
        self.assertEqual(bp.limpiar_query("Hoy Recomiéndame Un Perfume Marino"),
                         "marino")

    def test_vacio(self):
        self.assertEqual(bp.limpiar_query(""), "")


if __name__ == "__main__":
    unittest.main()
