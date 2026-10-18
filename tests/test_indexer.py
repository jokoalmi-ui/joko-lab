#!/usr/bin/env python3
"""
Tests de las funciones extraidas de load_notes_con_hash() (refactor 07-ago-2026
con OpenCode): _excluir_directorio, _parsear_archivo y _construir_documentos.

REQUIERE el venv del RAG (indexer importa lancedb/torch/langchain):
  ~/.venv/hermes-rag/bin/python3 -m unittest tests/test_indexer.py -v

Con python3 del sistema hace skip limpio (deps no disponibles).

Red de seguridad: conteos y hashes anclados comparados antes/despues (el
conteo total es inestable por el vault vivo: otra sesion escribe .md; los
hashes de rutas concretas SI son estables).
"""

import sys
import unittest
from pathlib import Path

TOOLS_DIR = str(Path(__file__).resolve().parent.parent / "tools")
sys.path.insert(0, TOOLS_DIR)

try:
    from indexer import (_excluir_directorio, _parsear_archivo,
                         _construir_documentos, _clasificar_cambios,
                         _recrear_indices, RecursiveCharacterTextSplitter)
    DISPONIBLE = True
except ImportError as e:
    DISPONIBLE = False
    _IMPORT_ERR = str(e)


@unittest.skipUnless(DISPONIBLE, f"deps del RAG no disponibles en este intérprete: {locals().get('_IMPORT_ERR','')}")
class TestExcluirDirectorio(unittest.TestCase):
    def test_ocultos(self):
        self.assertTrue(_excluir_directorio("/vault", ".git"))
        self.assertTrue(_excluir_directorio("/vault", ".BACKUP"))

    def test_node_modules(self):
        self.assertTrue(_excluir_directorio("/vault", "node_modules"))

    def test_decisions_bajo_04(self):
        self.assertTrue(_excluir_directorio("/vault/04-operations", "decisions"))
        self.assertFalse(_excluir_directorio("/vault/01-knowledge", "decisions"))

    def test_backups(self):
        self.assertTrue(_excluir_directorio("/vault", "carpeta.bak"))
        self.assertFalse(_excluir_directorio("/vault", "research"))


@unittest.skipUnless(DISPONIBLE, "deps del RAG no disponibles")
class TestParsearArchivo(unittest.TestCase):
    def test_yaml_con_type_status(self):
        # yaml_to_text(fpath) LEE del disco: archivo temporal real
        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as f:
            f.write("id: RULE-001\ntype: RULE\nstatus: activo\nlegacy_fields:\n  accion: ok\n")
            ruta = Path(f.name)
        try:
            meta, body, tipo, estado = _parsear_archivo("RULE-001.yaml", ruta, ruta.read_text())
            self.assertEqual(tipo, "RULE")
            self.assertEqual(estado, "activo")
            self.assertIsInstance(body, str)
            self.assertIn("accion", body)
        finally:
            ruta.unlink(missing_ok=True)

    def test_md_con_frontmatter(self):
        meta, body, tipo, estado = _parsear_archivo(
            "doc.md", Path("/v/doc.md"),
            "---\ntype: DEC\nstatus: activo\ntitle: T\n---\n# Cuerpo\n")
        self.assertEqual(tipo, "DEC")
        self.assertEqual(estado, "activo")
        self.assertEqual(meta.get("title"), "T")
        self.assertNotIn("---", body)

    def test_yaml_sin_type(self):
        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as f:
            f.write("id: X-1\n")
            ruta = Path(f.name)
        try:
            _, _, tipo, estado = _parsear_archivo("x.yaml", ruta, ruta.read_text())
            self.assertEqual((tipo, estado), ("", ""))
        finally:
            ruta.unlink(missing_ok=True)


@unittest.skipUnless(DISPONIBLE, "deps del RAG no disponibles")
class TestConstruirDocumentos(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from langchain_text_splitters import RecursiveCharacterTextSplitter as RC
        cls.splitter = RC(chunk_size=1000, chunk_overlap=150,
                          separators=["\n## ", "\n### ", "\n\n", "\n", " "])

    def test_chunks_con_id(self):
        body = "# T\n" + "\n".join(f"parrafo {i} de contenido largo para rellenar" for i in range(120))
        docs = _construir_documentos(self.splitter, "docs/largo.md",
                                     Path("/v/docs/largo.md"), {"title": "Mi Titulo"},
                                     body, "RULE", "activo")
        self.assertGreaterEqual(len(docs), 2)
        self.assertTrue(docs[0]["id"].startswith("docs/largo.md#0"))
        self.assertEqual(docs[0]["title"], "Mi Titulo")
        self.assertEqual(docs[0]["type"], "RULE")
        self.assertEqual(docs[0]["status"], "activo")

    def test_title_por_defecto(self):
        docs = _construir_documentos(self.splitter, "docs/sin-titulo.md",
                                     Path("/v/docs/sin-titulo.md"), {}, "texto corto",
                                     "", "")
        self.assertEqual(docs[0]["title"], "sin-titulo")


@unittest.skipUnless(DISPONIBLE, "deps del RAG no disponibles")
class TestClasificarCambios(unittest.TestCase):
    def test_caso_mixto(self):
        previo = {"a.md": "h1", "b.md": "h1", "c.md": "h1"}
        nuevo = {"a.md": "h1", "b.md": "h2", "d.md": "h1"}
        n, m, e, s = _clasificar_cambios(previo, nuevo)
        self.assertEqual(n, {"d.md"})
        self.assertEqual(m, {"b.md"})
        self.assertEqual(e, {"c.md"})
        self.assertEqual(s, {"a.md"})

    def test_todo_igual(self):
        previo = {"a.md": "h1"}
        n, m, e, s = _clasificar_cambios(previo, dict(previo))
        self.assertEqual((n, m, e), (set(), set(), set()))
        self.assertEqual(s, {"a.md"})

    def test_vacio(self):
        n, m, e, s = _clasificar_cambios({}, {})
        self.assertEqual((n, m, e, s), (set(), set(), set(), set()))


@unittest.skipUnless(DISPONIBLE, "deps del RAG no disponibles")
class TestRecrearIndices(unittest.TestCase):
    def test_llama_a_ambos_indices(self):
        class FakeTable:
            def __init__(self):
                self.llamadas = []
            def create_fts_index(self, *a, **k):
                self.llamadas.append("fts")
            def create_index(self, *a, **k):
                self.llamadas.append("vec")
        t = FakeTable()
        _recrear_indices(t)
        self.assertEqual(t.llamadas, ["fts", "vec"])

    def test_error_no_lanza(self):
        class TableQueFalla:
            def create_fts_index(self, *a, **k):
                raise RuntimeError("boom")
            def create_index(self, *a, **k):
                raise RuntimeError("boom")
        # no debe propagar excepcion
        _recrear_indices(TableQueFalla())


if __name__ == "__main__":
    unittest.main()
