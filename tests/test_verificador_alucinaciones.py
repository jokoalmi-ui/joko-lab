#!/usr/bin/env python3
"""
Tests de verificador_alucinaciones.py (gate de veracidad, 16-ago-2026).

Cubre los 4 tipos de alucinación + etiquetas de certeza + integración con
confidence.py. Red de seguridad: verifica que el gate bloquea lo no verificado
y aprueba lo verificado.

Ejecucion:
  cd ~/joko-lab && python3 -m unittest tests/test_verificador_alucinaciones.py -v
"""

import sys
import unittest
from pathlib import Path

TOOLS_DIR = str(Path(__file__).resolve().parent.parent / "tools")
sys.path.insert(0, TOOLS_DIR)

from verificador_alucinaciones import (
    detectar_contradiccion_interna,
    detectar_desviacion_prompt,
    detectar_fuentes,
    detectar_relevancia,
    verificar,
)


class TestDetectarContradiccionInterna(unittest.TestCase):
    def test_texto_normal_sin_contradiccion(self):
        r = detectar_contradiccion_interna(
            "El lab usa RAG local con LanceDB y alcanza un recall@5 del 100% en 70ms.")
        self.assertFalse(r["detectado"])

    def test_auto_contradiccion_detectada(self):
        r = detectar_contradiccion_interna(
            "El sistema está verificado y funciona. No obstante, no está verificado y no funciona.")
        self.assertTrue(r["detectado"])

    def test_conflicto_cercano_afirmacion_negacion(self):
        r = detectar_contradiccion_interna(
            "El sistema es estable pero no es estable en producción.")
        # El patrón "X es ... no es X" debe detectarse (conflicto cercano)
        self.assertTrue(r["detectado"])

    def test_condicional_si_no_no_es_contradiccion(self):
        # "si no está X" es una regla condicional, no una contradicción
        r = detectar_contradiccion_interna(
            "ya está remontando. si no está remontando, ni de broma, que se arriesga todo.")
        self.assertFalse(r["detectado"])

    def test_articulo_repetido_no_es_contradiccion(self):
        # "es una hazaña... no es una herramienta" — la palabra repetida es el
        # artículo "una", no un atributo → NO debe detectarse
        r = detectar_contradiccion_interna(
            "es una hazaña de ingeniería, pero no es una herramienta usable.")
        self.assertFalse(r["detectado"])

    def test_hablar_sobre_contradiccion_no_es_contradiccion(self):
        # Un análisis que DESCRIBE el concepto de contradicción (taxonomía de
        # alucinaciones) no se contradice a sí mismo
        r = detectar_contradiccion_interna(
            "el modelo se contradice dentro de la misma respuesta; según la taxonomía, "
            "se contradice cuando la salida va contra el prompt.")
        self.assertFalse(r["detectado"])


class TestDetectarDesviacionPrompt(unittest.TestCase):
    def test_sin_prompt_no_detecta(self):
        r = detectar_desviacion_prompt("cualquier texto", None)
        self.assertFalse(r["detectado"])

    def test_desobediencia_no_inventes(self):
        r = detectar_desviacion_prompt(
            "El modelo inventa datos que no existen en el corpus.",
            "Responde sin inventar datos.")
        self.assertTrue(r["detectado"])


class TestDetectarFuentes(unittest.TestCase):
    def test_factual_sin_fuente_bloquea(self):
        r = detectar_fuentes("La economía española creció un 4,5% en 2025.", "economía")
        self.assertTrue(r["detectado"])
        self.assertEqual(r["etiqueta"], "NO_VERIFICADO")

    def test_con_fuente_aprueba(self):
        r = detectar_fuentes(
            "Según el INE (https://www.ine.es), el PIB creció un 2,5% en 2024. [VERIFICADO]",
            "economía")
        self.assertFalse(r["detectado"])
        self.assertEqual(r["etiqueta"], "VERIFICADO")

    def test_alcance_interno_sin_datos_externos(self):
        r = detectar_fuentes("El lab tiene 205 tests en la suite.", None)
        self.assertEqual(r["etiqueta"], "ALCANCE_INTERNO")

    def test_estado_interno_lab_con_numeros(self):
        # Métricas internas del lab (tests, GPU, servicios) → ALCANCE_INTERNO, no hechos externos
        r = detectar_fuentes(
            "El lab tiene 220 tests, 0 servicios caídos, GPU a 42°C y 12 GB VRAM.", None)
        self.assertEqual(r["etiqueta"], "ALCANCE_INTERNO")

    def test_hechos_externos_no_lab_siguen_bloqueando(self):
        # Hechos externos (sin fuente) aunque mencionen "lab" en otra frase
        r = detectar_fuentes(
            "La economía española creció un 4,5% en 2025 según nadie en particular.", "economía")
        self.assertEqual(r["etiqueta"], "NO_VERIFICADO")


class TestDetectarRelevancia(unittest.TestCase):
    def test_tema_corto_no_juzga(self):
        r = detectar_relevancia("Hoy hace buen día para pasear.", "economía")
        self.assertFalse(r["detectado"])  # tema 1 palabra: no marcar

    def test_irrelevante_con_tema_largo(self):
        r = detectar_relevancia(
            "Hoy hace buen día para pasear por la playa y comer helado.",
            "arquitectura de agentes RAG con memoria persistente")
        self.assertTrue(r["detectado"])

    def test_relevante_al_tema(self):
        r = detectar_relevancia(
            "El pipeline RAG recupera documentos con BGE-M3 y los almacena en LanceDB.",
            "sistema de recuperación RAG con base de datos vectorial")
        self.assertFalse(r["detectado"])


class TestVerificar(unittest.TestCase):
    def test_factual_sin_fuente_bloquea(self):
        r = verificar("La economía española creció un 4,5% en 2025.", tema="economía")
        self.assertEqual(r["veredicto"], "BLOQUEADO_SIN_FUENTE")
        self.assertEqual(r["etiqueta"], "[NO VERIFICADO]")

    def test_con_fuente_ok(self):
        r = verificar(
            "Según el INE (https://www.ine.es), el PIB creció un 2,5% en 2024. [VERIFICADO]",
            tema="economía")
        self.assertEqual(r["veredicto"], "OK")
        self.assertEqual(r["etiqueta"], "[VERIFICADO]")

    def test_contradiccion_revisar(self):
        r = verificar(
            "El sistema está verificado y funciona. No obstante, no está verificado y no funciona.",
            tema="sistema")
        self.assertEqual(r["veredicto"], "REVISAR")
        self.assertEqual(r["etiqueta"], "[REVISAR]")

    def test_salida_json_serializable(self):
        import json
        r = verificar("Texto de prueba sin hechos externos.", tema="prueba")
        json.dumps(r, ensure_ascii=False)  # no debe lanzar


if __name__ == "__main__":
    unittest.main()
