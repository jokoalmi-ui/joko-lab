#!/usr/bin/env python3
"""
Tests de las funciones extraidas de format_synthesis() (refactor 07-ago-2026
con OpenCode): _limpiar_texto_item, _calcular_confianza, _detectar_boundaries,
_seccion_fuentes.

Red de seguridad: salida de format_synthesis comparada identica sobre una
Synthesis de ejemplo antes/despues + estos tests fijan cada pieza.

Ejecucion:
  cd ~/joko-lab && python3 -m unittest tests/test_knowledge_resolver.py -v
"""

import sys
import unittest
from pathlib import Path

TOOLS_DIR = str(Path(__file__).resolve().parent.parent / "tools")
sys.path.insert(0, TOOLS_DIR)

from knowledge_resolver import (KnowledgeItem, Synthesis,
                                _limpiar_texto_item, _calcular_confianza,
                                _detectar_boundaries, _seccion_fuentes,
                                _fuente_para_buffer, _crear_item,
                                _clasificar_y_anadir,
                                _cabecera_sintesis, _seccion_hechos,
                                _seccion_decisiones, _seccion_conflictos,
                                _seccion_hipotesis, _seccion_acciones,
                                _seccion_confianza)


def fact(content, stype="experimento", conf="ALTA"):
    return KnowledgeItem("hecho", content, f"{stype}.md", stype, conf)


class TestLimpiarTextoItem(unittest.TestCase):
    def test_limpia_contexto_rag(self):
        self.assertEqual(
            _limpiar_texto_item("[Contexto RAG] Gemma es bueno"),
            "Gemma es bueno")

    def test_limpia_marcadores_y_coseno(self):
        out = _limpiar_texto_item(
            "[Contexto RAG] texto (cos: 0.9 | rerank: 0.8) [/Contexto]  ")
        self.assertEqual(out, "texto")

    def test_strip(self):
        self.assertEqual(_limpiar_texto_item("  hola  "), "hola")


class TestCalcularConfianza(unittest.TestCase):
    def test_con_decisiones(self):
        s = Synthesis(
            facts=[fact("a", conf="ALTA"), fact("b", conf="ALTA"), fact("c", conf="MEDIA")],
            decisions=[KnowledgeItem("decision", "d", "x.md", "decision", "ALTA")],
        )
        high, total, pct = _calcular_confianza(s)
        self.assertEqual(high, 3)   # 2 facts ALTA + 1 decision
        self.assertEqual(total, 4)  # 3 facts + 1 decision
        self.assertEqual(pct, 75)

    def test_vacio(self):
        high, total, pct = _calcular_confianza(Synthesis())
        self.assertEqual((high, total, pct), (0, 0, 0))


class TestDetectarBoundaries(unittest.TestCase):
    def test_descartado(self):
        b = _detectar_boundaries(Synthesis(facts=[fact("Modelo descartado: Qwen")]))
        self.assertTrue(any("No usar modelos descartados" in x for x in b))

    def test_function_call(self):
        b = _detectar_boundaries(Synthesis(facts=[fact("responde con function call nativa")]))
        self.assertTrue(any("tool calls" in x for x in b))

    def test_sin_restricciones(self):
        b = _detectar_boundaries(Synthesis(facts=[fact("modelo normal")]))
        self.assertEqual(b, ["  ✓ Sin restricciones especiales detectadas"])


class TestSeccionFuentes(unittest.TestCase):
    def test_orden_por_peso(self):
        s = Synthesis(sources_consulted=["notas.md", "EXP-1.md"])
        lines = _seccion_fuentes(s)
        # una linea por fuente, ordenadas por peso desc: EXP-1 (experimento 10)
        # va primero que notas (documentacion 2)
        self.assertIn("EXP-1.md", lines[0])
        self.assertIn("notas.md", lines[1])
        # experimento: 10 // 3 = 3 estrellas
        self.assertIn("★★★", lines[0])

    def test_vacio(self):
        self.assertEqual(_seccion_fuentes(Synthesis()), [])


class TestFuenteParaBuffer(unittest.TestCase):
    def test_encuentra_fuente(self):
        self.assertEqual(
            _fuente_para_buffer("segun EXP-20260730-005.md se eligio",
                                ["EXP-20260730-005.md", "DEC-001.md"]),
            "EXP-20260730-005.md")

    def test_sin_fuente(self):
        self.assertEqual(_fuente_para_buffer("texto sin fuentes", ["a.md"]), "desconocido")

    def test_primera_fuente_match(self):
        self.assertEqual(
            _fuente_para_buffer("DEC-001.md mencionado", ["a.md", "DEC-001.md", "b.md"]),
            "DEC-001.md")


class TestCrearItem(unittest.TestCase):
    def test_construye_con_tipo_por_defecto(self):
        item = _crear_item(None, "BAJA", "texto de contenido", "src.md", "experimento")
        self.assertEqual(item.type, "hecho")
        self.assertEqual(item.content, "texto de contenido")
        self.assertEqual(item.source, "src.md")
        self.assertEqual(item.source_type, "experimento")
        self.assertEqual(item.confidence, "BAJA")

    def test_corta_a_300(self):
        item = _crear_item("decision", "ALTA", "x" * 500, "s", "decision")
        self.assertEqual(len(item.content), 300)


class TestClasificarYAnadir(unittest.TestCase):
    def test_dispatch_por_tipo(self):
        synth = Synthesis()
        for tipo, attr in [("conflicto", "conflicts"), ("conflict", "conflicts"),
                           ("hipotesis", "hypotheses"), ("decision", "decisions"),
                           ("accion", "actions"), ("hecho", "facts")]:
            item = _crear_item(tipo, "BAJA", f"texto {tipo}", "s", "doc")
            _clasificar_y_anadir(synth, item, tipo)
        self.assertEqual(len(synth.conflicts), 2)
        self.assertEqual(len(synth.hypotheses), 1)
        self.assertEqual(len(synth.decisions), 1)
        self.assertEqual(len(synth.actions), 1)
        self.assertEqual(len(synth.facts), 1)


class TestSeccionesFormatSynthesis(unittest.TestCase):
    """Tests de las 7 secciones extraidas de format_synthesis (08-ago-2026)."""

    def _synth(self, **kw):
        base = dict(facts=[], decisions=[], conflicts=[], hypotheses=[],
                    actions=[], sources_consulted=[])
        base.update(kw)
        return Synthesis(query="q", **base)

    def test_cabecera_incluye_confianza(self):
        s = self._synth()
        lines = _cabecera_sintesis(s, 80, 2, 5)
        self.assertIn("KNOWLEDGE RESOLVER — Sintesis", lines[1])
        self.assertIn("Confianza global: 80% (2/5 items con evidencia)", lines[4])

    def test_hechos_con_evidencia_y_sin(self):
        s = self._synth(facts=[
            KnowledgeItem("hecho", "texto hecho", "e.md", "experimento", "ALTA",
                          weight=6, evidence=["EXP-1"]),
            KnowledgeItem("hecho", "texto sin evi", "d.md", "documentacion", "MEDIA"),
        ])
        lines = _seccion_hechos(s)
        texto = "\n".join(lines)
        self.assertIn("── HECHOS CONFIRMADOS ──", texto)
        self.assertIn("[1] texto hecho", texto)
        self.assertIn("Evidencia: EXP-1", texto)
        self.assertNotIn("Evidencia:", texto.split("[2]")[1])

    def test_hechos_vacios_devuelven_lista_vacia(self):
        self.assertEqual(_seccion_hechos(self._synth()), [])

    def test_decisiones_limite_3(self):
        s = self._synth(decisions=[
            KnowledgeItem("decision", f"dec {i}", "s", "decision", "ALTA")
            for i in range(5)])
        lines = _seccion_decisiones(s)
        self.assertIn("── DECISIONES ACTIVAS ──", "\n".join(lines))
        self.assertEqual(len([l for l in lines if l.startswith("  [")]), 3)

    def test_conflictos_limite_3(self):
        s = self._synth(conflicts=[
            KnowledgeItem("conflicto", f"c {i}", "s", "doc", "MEDIA")
            for i in range(5)])
        lines = _seccion_conflictos(s)
        self.assertIn("── CONFLICTOS DETECTADOS ──", "\n".join(lines))
        self.assertEqual(len([l for l in lines if l.startswith("  ⚠")]), 3)

    def test_hipotesis_y_acciones(self):
        s = self._synth(hypotheses=[
            KnowledgeItem("hipotesis", "h1", "s", "doc", "MEDIA")],
            actions=[
            KnowledgeItem("accion", "a1", "s", "doc", "MEDIA")])
        hip = "\n".join(_seccion_hipotesis(s))
        acc = "\n".join(_seccion_acciones(s))
        self.assertIn("[?] h1", hip)
        self.assertIn("→ a1", acc)

    def test_confianza_con_decisiones_y_conflictos(self):
        s = self._synth(decisions=[
            KnowledgeItem("decision", "d1", "s", "decision", "ALTA")],
            conflicts=[
            KnowledgeItem("conflicto", "c1", "s", "doc", "MEDIA")])
        lines = _seccion_confianza(s, 75, 1, 4)
        texto = "\n".join(lines)
        self.assertIn("── CONFIANZA ──", texto)
        self.assertIn("Puntuacion: 75%", texto)
        self.assertIn("Decisiones activas aplicables: 1", texto)
        self.assertIn("Conflictos detectados: 1", texto)


if __name__ == "__main__":
    unittest.main()
