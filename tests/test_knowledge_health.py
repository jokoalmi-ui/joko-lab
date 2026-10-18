#!/usr/bin/env python3
"""
Red de seguridad de knowledge_health.py — tests unitarios (unittest estándar).

Cubre las funciones puras: parse_frontmatter, classify_file, extract_date,
find_knowledge_files. Creado 07-ago-2026 como red previa al refactor de
audit() (complejidad 52). No toca el lab: usa archivos temporales salvo el
test de find_knowledge_files que lee el árbol real (solo lectura).

Ejecución:
  cd ~/joko-lab && python3 -m unittest tests/test_knowledge_health.py -v
"""

import os
import sys
import tempfile
import unittest
from datetime import date, datetime
from pathlib import Path

TOOLS_DIR = str(Path(__file__).resolve().parent.parent / "tools")
sys.path.insert(0, TOOLS_DIR)

import knowledge_health as kh


class TestParseFrontmatter(unittest.TestCase):
    def test_yaml_puro(self):
        with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as f:
            f.write("id: DEC-001\ntype: DEC\nstatus: activo\n")
            ruta = Path(f.name)
        try:
            fm = kh.parse_frontmatter(ruta)
            self.assertEqual(fm.get("id"), "DEC-001")
            self.assertEqual(fm.get("type"), "DEC")
        finally:
            ruta.unlink(missing_ok=True)

    def test_markdown_con_frontmatter(self):
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            f.write("---\ntitle: Prueba\ncreated: 2026-08-01\n---\n# H1\n")
            ruta = Path(f.name)
        try:
            fm = kh.parse_frontmatter(ruta)
            self.assertEqual(fm.get("title"), "Prueba")
            # yaml.safe_load convierte fechas ISO a datetime.date (no str)
            self.assertEqual(fm.get("created"), date(2026, 8, 1))
        finally:
            ruta.unlink(missing_ok=True)

    def test_sin_frontmatter(self):
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            f.write("# Solo titulo\nsin frontmatter\n")
            ruta = Path(f.name)
        try:
            self.assertEqual(kh.parse_frontmatter(ruta), {})
        finally:
            ruta.unlink(missing_ok=True)

    def test_frontmatter_roto(self):
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            f.write("---\n: no valido\n---\n")
            ruta = Path(f.name)
        try:
            self.assertEqual(kh.parse_frontmatter(ruta), {})
        finally:
            ruta.unlink(missing_ok=True)


class TestClassifyFile(unittest.TestCase):
    def test_type_explicito(self):
        fm = {"type": "RULE"}
        self.assertEqual(kh.classify_file(Path("cualquiera.md"), fm), "RULE")

    def test_type_explicito_preferido_sobre_nombre(self):
        fm = {"type": "DEC"}
        self.assertEqual(kh.classify_file(Path("rule-falsa.md"), fm), "DEC")

    def test_por_nombre_decision(self):
        self.assertEqual(kh.classify_file(Path("dec-001.md"), {}), "DEC")

    def test_por_nombre_experimento(self):
        self.assertEqual(kh.classify_file(Path("exp-20260728-002.md"), {}), "EXP")

    def test_por_nombre_observacion(self):
        self.assertEqual(kh.classify_file(Path("obs-005.md"), {}), "OBS")

    def test_por_nombre_rule(self):
        self.assertEqual(kh.classify_file(Path("rule-001.md"), {}), "RULE")

    def test_por_nombre_policy(self):
        self.assertEqual(kh.classify_file(Path("policy-002.md"), {}), "POLICY")

    def test_por_carpeta_decisions(self):
        ruta = Path("/tmp/joko-lab/01-knowledge/decisions/mi-decision.md")
        self.assertEqual(kh.classify_file(ruta, {}), "DEC")

    def test_por_carpeta_pattern_incubator(self):
        ruta = Path("/tmp/joko-lab/lpa/pattern-incubator/patron.md")
        self.assertEqual(kh.classify_file(ruta, {}), "PATTERN")

    def test_unknown(self):
        self.assertEqual(kh.classify_file(Path("notas-sueltas.md"), {}), "UNKNOWN")


class TestExtractDate(unittest.TestCase):
    def test_clave_datetime(self):
        fm = {"created": datetime(2026, 8, 1)}
        self.assertEqual(kh.extract_date(fm, ["created"]), datetime(2026, 8, 1))

    def test_clave_str_iso(self):
        fm = {"created": "2026-08-01"}
        self.assertEqual(kh.extract_date(fm, ["created"]), datetime(2026, 8, 1))

    def test_str_con_Z(self):
        fm = {"last_validated": "2026-08-01T10:00:00Z"}
        self.assertEqual(kh.extract_date(fm, ["last_validated"]), datetime(2026, 8, 1))

    def test_primera_clave_encontrada(self):
        fm = {"created": None, "date": "2026-07-15"}
        self.assertEqual(kh.extract_date(fm, ["created", "date"]), datetime(2026, 7, 15))

    def test_sin_claves(self):
        self.assertIsNone(kh.extract_date({}, ["created", "fecha"]))

    def test_valor_invalido(self):
        fm = {"created": "no-es-fecha"}
        self.assertIsNone(kh.extract_date(fm, ["created"]))


class TestFindKnowledgeFiles(unittest.TestCase):
    def test_excluye_backups_y_dotfiles(self):
        files = kh.find_knowledge_files()
        self.assertTrue(len(files) > 0, "debe encontrar al menos un archivo de conocimiento")
        for f in files:
            rel = str(f.relative_to(kh.LAB_ROOT)).lower()
            self.assertNotIn(".bak", rel)
            self.assertNotIn(".backup", rel)
            self.assertNotIn("/.", rel)

    def test_encuentra_objects_yaml(self):
        files = kh.find_knowledge_files()
        yamls = [f for f in files if f.suffix == ".yaml"]
        self.assertTrue(len(yamls) > 0, "debe encontrar al menos un .yaml en objects/")


if __name__ == "__main__":
    unittest.main()
