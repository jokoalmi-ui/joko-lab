#!/usr/bin/env python3
"""test_llm_as_judge.py — pruebas de consolidación de LLM-as-Judge (22-ago-2026).

Cubre: CONSENSO PASA, DISCREPANCIA (camino sin probar antes), REVISA,
UN_JUEZ, la regla determinista _forzar_falla (fidelidad/completitud <=1 -> FALLA)
y SIN_JUEZ. Sin red: consolida dicts directamente.

Uso: cd ~/joko-lab/tools && python3 -m unittest tests/test_llm_as_judge.py
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import llm_as_judge as j


def _juez(modelo, usado=True, fid=5, comp=5, rel=5, cla=5, util=5, ver="PASA"):
    return {"modelo": modelo, "usado": usado,
            "fidelidad": fid, "completitud": comp, "relevancia": rel,
            "claridad": cla, "utilidad": util, "veredicto": ver}


class TestConsolidar(unittest.TestCase):

    def test_consenso_pasa(self):
        j1 = _juez("glm-4.6v-flash")
        j2 = _juez("openai/gpt-oss-20b")
        r = j.consolidar(j1, j2)
        self.assertEqual(r["estado"], "CONSENSO")
        self.assertEqual(r["veredicto"], "PASA")

    def test_discrepancia(self):
        # j2 con fidelidad 1 -> forzado a FALLA; j1 PASA -> opuestos -> DISCREPANCIA
        j1 = _juez("glm-4.6v-flash", fid=5, ver="PASA")
        j2 = _juez("openai/gpt-oss-20b", fid=1, ver="PASA")
        r = j.consolidar(j1, j2)
        self.assertEqual(r["estado"], "DISCREPANCIA")
        self.assertEqual(r["veredicto"], "DISCREPANCIA")

    def test_discrepancia_por_promedio(self):
        # Divergencia de promedio >=1.5 sin veredictos opuestos -> DISCREPANCIA
        j1 = _juez("glm-4.6v-flash", fid=5, comp=5, rel=5, cla=5, util=5, ver="PASA")
        j2 = _juez("openai/gpt-oss-20b", fid=2, comp=2, rel=2, cla=2, util=2, ver="REVISA")
        r = j.consolidar(j1, j2)
        self.assertEqual(r["estado"], "DISCREPANCIA")

    def test_revisa(self):
        j1 = _juez("glm-4.6v-flash", fid=3, comp=2, ver="REVISA")
        j2 = _juez("openai/gpt-oss-20b", fid=4, comp=3, ver="REVISA")
        r = j.consolidar(j1, j2)
        self.assertEqual(r["estado"], "CONSENSO")
        self.assertEqual(r["veredicto"], "REVISA")

    def test_un_juez(self):
        j1 = _juez("glm-4.6v-flash")
        j2 = {"modelo": "openai/gpt-oss-20b", "usado": False, "error": "no cabe"}
        r = j.consolidar(j1, j2)
        self.assertEqual(r["estado"], "UN_JUEZ")
        self.assertEqual(r["veredicto"], "PASA")

    def test_forzar_falla_un_juez(self):
        # UN_JUEZ con fidelidad 1 -> FALLA (regla determinista critica)
        j1 = _juez("glm-4.6v-flash", fid=1, comp=5, ver="PASA")
        j2 = {"modelo": "openai/gpt-oss-20b", "usado": False}
        r = j.consolidar(j1, j2)
        self.assertEqual(r["veredicto"], "FALLA")

    def test_forzar_falla_doble(self):
        # Doble juez: uno con fidelidad 1 -> su veredicto se fuerza a FALLA
        j1 = _juez("glm-4.6v-flash", fid=1, comp=5, ver="REVISA")
        j2 = _juez("openai/gpt-oss-20b", fid=4, comp=4, ver="REVISA")
        r = j.consolidar(j1, j2)
        self.assertEqual(r["estado"], "CONSENSO")
        self.assertEqual(r["veredicto"], "REVISA")

    def test_sin_juez(self):
        j1 = {"modelo": "glm-4.6v-flash", "usado": False}
        j2 = {"modelo": "openai/gpt-oss-20b", "usado": False}
        r = j.consolidar(j1, j2)
        self.assertEqual(r["estado"], "SIN_JUEZ")


if __name__ == "__main__":
    unittest.main()
