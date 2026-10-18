#!/usr/bin/env python3
"""
Tests de verificar_research.py (post-procesador de veracidad, 16-ago-2026).

Verifica: inserción de la etiqueta tras Fuente, idempotencia (no duplica),
y que no corrompe el archivo.

Ejecucion:
  cd ~/joko-lab && python3 -m unittest tests/test_verificar_research.py -v
"""

import sys
import tempfile
import unittest
from pathlib import Path

TOOLS_DIR = str(Path(__file__).resolve().parent.parent / "tools")
sys.path.insert(0, TOOLS_DIR)

from verificar_research import ETIQUETA_RE, procesar_archivo


class TestProcesarArchivo(unittest.TestCase):
    def _crear_temp(self, contenido: str) -> Path:
        f = tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False,
                                        encoding="utf-8")
        f.write(contenido)
        f.close()
        return Path(f.name)

    def test_inserta_etiqueta_tras_fuente(self):
        contenido = ("# Análisis — Test (16-ago-2026)\n\n"
                     "**Fuente:** https://ejemplo.com\n\nCuerpo del análisis.")
        p = self._crear_temp(contenido)
        try:
            ok, _ = procesar_archivo(p)
            self.assertTrue(ok)
            texto = p.read_text(encoding="utf-8")
            self.assertIn("**VERACIDAD:**", texto)
            # La etiqueta va DESPUÉS del título y ANTES de Fuente
            self.assertLess(texto.index("**VERACIDAD:**"), texto.index("**Fuente:**"))
        finally:
            p.unlink(missing_ok=True)

    def test_idempotente_no_duplica(self):
        contenido = ("# Análisis — Test (16-ago-2026)\n\n"
                     "**Fuente:** https://ejemplo.com\n\nCuerpo.")
        p = self._crear_temp(contenido)
        try:
            procesar_archivo(p)
            procesar_archivo(p)  # segunda pasada
            texto = p.read_text(encoding="utf-8")
            self.assertEqual(len(ETIQUETA_RE.findall(texto)), 1)
        finally:
            p.unlink(missing_ok=True)

    def test_contenido_no_corrompido(self):
        contenido = ("# Análisis — Test (16-ago-2026)\n\n"
                     "**Fuente:** https://ejemplo.com\n\n"
                     "## Veredicto\nEl análisis concluye que el enfoque es válido.")
        p = self._crear_temp(contenido)
        try:
            procesar_archivo(p)
            texto = p.read_text(encoding="utf-8")
            self.assertIn("## Veredicto", texto)
            self.assertIn("El análisis concluye", texto)
        finally:
            p.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
