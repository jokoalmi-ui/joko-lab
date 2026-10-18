#!/usr/bin/env python3
"""test_escaneo_secretos_cron.py — pruebas del escáner de secretos en outputs
de crons (22-ago-2026). Usa directorios temporales, sin red.

Uso: cd ~/joko-lab && python3 -m unittest tests/test_escaneo_secretos_cron.py
"""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import escaneo_secretos_cron as esc


class TestEscaneo(unittest.TestCase):

    def _tmp(self, contenido):
        d = Path(tempfile.mkdtemp())
        (d / "job1").mkdir()
        (d / "job1" / "2026-08-22_10-00.md").write_text(contenido, encoding="utf-8")
        return d

    def test_limpio_silencioso(self):
        d = self._tmp("Todo normal, sin secretos.\n")
        self.assertEqual(esc.escanear(d), [])

    def test_detecta_sk(self):
        d = self._tmp("clave: sk-abcdefghijklmnopqrstuvwxyz123456\n")
        h = esc.escanear(d)
        self.assertEqual(len(h), 1)
        self.assertIn("OPENAI/DEEPSEEK", h[0][2])

    def test_detecta_ghp(self):
        d = self._tmp("token ghp_1234567890abcdefghijklmnopqrstuvwxyz\n")
        h = esc.escanear(d)
        self.assertEqual(len(h), 1)
        self.assertIn("GITHUB_PAT", h[0][2])

    def test_redacta_valor(self):
        d = self._tmp("clave: sk-abcdefghijklmnopqrstuvwxyz123456\n")
        h = esc.escanear(d)
        self.assertNotIn("abcdefghijklmnopqrstuvwxyz123456", h[0][3])

    def test_sin_directorio(self):
        self.assertEqual(esc.escanear(Path("/tmp/no-existe-xyz-12345")), [])


if __name__ == "__main__":
    unittest.main()
