#!/usr/bin/env python3
"""
Tests de las funciones extraidas de extraer_resumen_estructurado() (refactor
07-ago-2026 con OpenCode): _resumen_markdown y _resumen_yaml.

Red de seguridad: salida de la funcion comparada identica sobre rutas reales
antes/despues + estos tests fijan el comportamiento de cada rama.

Ejecucion:
  cd ~/joko-lab && python3 -m unittest tests/test_context_builder_estructurado.py -v
"""

import sys
import unittest
from pathlib import Path

TOOLS_DIR = str(Path(__file__).resolve().parent.parent / "tools")
sys.path.insert(0, TOOLS_DIR)

from context_builder_estructurado import _resumen_markdown, _resumen_yaml


class TestResumenMarkdown(unittest.TestCase):
    def test_con_frontmatter(self):
        raw = ("---\nid: RULE-X\ntype: RULE\nstatus: activo\ntitle: Mi Regla\n---\n"
               "# Encabezado\nprimera linea util\nsegunda linea util\n")
        out = _resumen_markdown("docs/x.md", raw)
        self.assertIn("id: RULE-X", out)
        self.assertIn("type: RULE", out)
        self.assertIn("title: Mi Regla", out)
        self.assertIn("primera linea util", out)
        self.assertIn("segunda linea util", out)
        self.assertNotIn("# Encabezado", out)

    def test_sin_frontmatter(self):
        out = _resumen_markdown("docs/x.md", "solo texto\nmas texto\n")
        self.assertNotIn("id:", out)
        self.assertIn("solo texto", out)

    def test_ignora_lineas_vacias_y_encabezados(self):
        raw = "\n# H1\n\nprimera util\n# H2\nsegunda util\n"
        out = _resumen_markdown("docs/x.md", raw)
        self.assertIn("primera util", out)
        self.assertIn("segunda util", out)
        self.assertNotIn("H1", out.split(" | ")[-1])

    def test_linea_larga_cortada_a_160(self):
        out = _resumen_markdown("docs/x.md", "a" * 300 + "\n")
        self.assertIn("a" * 160, out)
        self.assertNotIn("a" * 161, out)


class TestResumenYaml(unittest.TestCase):
    def test_yaml_valido_con_campos(self):
        raw = ("id: RULE-1\ntype: RULE\nstatus: activo\ndomain: ai-architecture\n"
               "scope: todo\nbody: texto del cuerpo\n"
               "legacy_fields:\n  prioridad: 90\n  accion:\n    modelo: m\n"
               "    params:\n      temperature: 0.7\n")
        out = _resumen_yaml("objects/RULE-1.yaml", raw)
        self.assertIn("id: RULE-1", out)
        self.assertIn("domain: ai-architecture", out)
        self.assertIn("body: texto del cuerpo", out)
        self.assertIn("prioridad: 90", out)
        self.assertIn("param_temperature: 0.7", out)

    def test_yaml_invalido(self):
        # "a: [1, 2" (corchete sin cerrar) lanza ParserError en PyYAML
        out = _resumen_yaml("objects/bad.yaml", "a: [1, 2\n")
        self.assertIn("yaml no parseable", out)

    def test_yaml_no_dict_devuelve_ruta(self):
        # Un scalar/list no lanza: devuelve la ruta (comportamiento real)
        out = _resumen_yaml("objects/lista.yaml", "- uno\n- dos\n")
        self.assertEqual(out, "objects/lista.yaml")

    def test_params_none_no_se_incluyen(self):
        raw = ("id: RULE-1\nlegacy_fields:\n  accion:\n    params:\n"
               "      temperature: null\n      max_tokens: 500\n")
        out = _resumen_yaml("objects/RULE-1.yaml", raw)
        self.assertNotIn("param_temperature", out)
        self.assertIn("param_max_tokens: 500", out)

    def test_limite_8_partes(self):
        # 9 partes reales: rpath, campos(1), body, condicion, accion, prioridad,
        # nota, param_t, param_m -> partes[:8] descarta la ultima (param_max)
        raw = ("id: RULE-1\ntype: RULE\nstatus: activo\ndomain: a\nscope: b\n"
               "body: x\nlegacy_fields:\n  condicion: c\n  accion:\n"
               "    params:\n      temperature: 0.7\n      max_tokens: 500\n"
               "  prioridad: 9\n  nota: n\n")
        out = _resumen_yaml("objects/RULE-1.yaml", raw)
        # partes[:8]: param_temperature (8a) entra; param_max_tokens (9a) no
        self.assertIn("param_temperature: 0.7", out)
        self.assertNotIn("param_max_tokens", out)


if __name__ == "__main__":
    unittest.main()
