#!/usr/bin/env python3
"""
Tests unitarios para state-manager.py
Cubre: get_gpu, get_system, check_ollama, check_lmstudio, check_n8n,
check_service, check_cloud, get_policies_state, collect_state, write_state.

Uso:
  python3 tests/test_state_manager.py
"""
import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock, PropertyMock

# Cargar state-manager.py como módulo (no es un paquete)
SM_PATH = Path(__file__).resolve().parent.parent / "state-manager" / "state-manager.py"
spec = importlib.util.spec_from_file_location("state_manager_mod", SM_PATH)
sm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sm)


class TestGetGPU(unittest.TestCase):
    def test_gpu_detectada(self):
        with patch.object(sm, "cmd", return_value="NVIDIA RTX A2000 12GB, 12282, 689, 11210, 6, 42"):
            r = sm.get_gpu()
            self.assertEqual(r["modelo"], "NVIDIA RTX A2000 12GB")
            self.assertEqual(r["vram_total_mb"], 12282)
            self.assertEqual(r["vram_usada_mb"], 689)
            self.assertEqual(r["vram_libre_mb"], 11210)
            self.assertEqual(r["utilizacion_pct"], 6)
            self.assertEqual(r["temp_c"], 42)

    def test_gpu_no_detectada(self):
        with patch.object(sm, "cmd", return_value=""):
            r = sm.get_gpu()
            self.assertEqual(r["modelo"], "no detectada")

    def test_gpu_error_parsing(self):
        with patch.object(sm, "cmd", return_value="solo un campo"):
            r = sm.get_gpu()
            # Si solo hay un campo, el parsing devuelve "solo un campo" como modelo
            self.assertEqual(r["modelo"], "solo un campo")


class TestGetSystem(unittest.TestCase):
    def test_system_normal(self):
        meminfo = "MemTotal:       32768 kB\nMemFree:        2048 kB\nMemAvailable:   20480 kB\n"
        loadavg = "1.41 0.80 0.60 2/345 12345\n"

        def fake_open(path, *a, **kw):
            p = str(path)
            if "loadavg" in p:
                return MagicMock(**{"__enter__.return_value": iter([loadavg])})
            return MagicMock(**{"__enter__.return_value": iter([meminfo])})

        with (
            patch("builtins.open", side_effect=fake_open),
            patch.object(sm, "cmd", return_value="Filesystem\n/\n/mnt/ssd_ia_datos\n"),
        ):
            r = sm.get_system()
            self.assertIn("ram_total_gb", r)
            self.assertIn("ram_libre_gb", r)
            self.assertIn("ram_disponible_gb", r)
            self.assertIn("cpu_load", r)
            self.assertIn("disco_root_libre_gb", r)
            self.assertIn("disco_ssd_libre_gb", r)


class TestCheckOllama(unittest.TestCase):
    def test_ollama_activo_con_modelos(self):
        def side_effect(*a, **kw):
            cmd = " ".join(a[0]) if isinstance(a[0], list) else str(a[0])
            if "api/tags" in cmd:
                return '{"models": [{"name": "llama31-8b-64k"}, {"name": "llama3.1:8b"}]}'
            if "api/ps" in cmd:
                return '{"models": [{"name": "llama31-8b-64k", "size": 4096}]}'
            return ""
        with patch.object(sm, "cmd", side_effect=side_effect):
            r = sm.check_ollama()
            self.assertTrue(r["activo"])
            self.assertEqual(len(r["modelos"]), 2)

    def test_ollama_inactivo(self):
        with patch.object(sm, "cmd", return_value=""):
            r = sm.check_ollama()
            self.assertFalse(r["activo"])
            self.assertEqual(r["modelos"], [])


class TestCheckLMStudio(unittest.TestCase):
    def test_lmstudio_activo(self):
        with patch.object(sm, "cmd", return_value='{"data": [{"id": "gemma-4-12b", "type": "llm"}]}'):
            r = sm.check_lmstudio()
            self.assertTrue(r["activo"])
            self.assertEqual(len(r["modelos"]), 1)

    def test_lmstudio_inactivo(self):
        with patch.object(sm, "cmd", return_value=""):
            r = sm.check_lmstudio()
            self.assertFalse(r["activo"])


class TestCheckN8n(unittest.TestCase):
    def test_n8n_activo(self):
        with patch.object(sm, "cmd", side_effect=["200", "2026-07-14 Version: 2.27.4\n..."]):
            r = sm.check_n8n()
            self.assertTrue(r["activo"])
            self.assertEqual(r["version"], "2.27.4")

    def test_n8n_inactivo(self):
        with patch.object(sm, "cmd", return_value="000"):
            r = sm.check_n8n()
            self.assertFalse(r["activo"])


class TestCheckService(unittest.TestCase):
    def test_servicio_responde(self):
        with patch.object(sm, "cmd", return_value="200"):
            r = sm.check_service("test", 9999)
            self.assertTrue(r["activo"])

    def test_servicio_no_responde(self):
        with patch.object(sm, "cmd", return_value=""):
            r = sm.check_service("test", 9999)
            self.assertFalse(r["activo"])


class TestCheckCloud(unittest.TestCase):
    def test_cloud_disponible(self):
        with patch.object(sm, "cmd", return_value="200"):
            r = sm.check_cloud("deepseek", "https://api.deepseek.com")
            self.assertTrue(r["disponible"])

    def test_cloud_no_disponible(self):
        with patch.object(sm, "cmd", return_value=""):
            r = sm.check_cloud("deepseek", "https://api.deepseek.com")
            self.assertFalse(r["disponible"])


class TestGetPoliciesState(unittest.TestCase):
    def test_formato_hora(self):
        r = sm.get_policies_state()
        self.assertIn("hora", r)
        self.assertIn("actual", r["hora"])
        self.assertIn("franja_activa", r["hora"])
        self.assertRegex(r["hora"]["actual"], r"^\d{2}:\d{2}$")

    def test_ahorro_inactivo(self):
        r = sm.get_policies_state()
        self.assertIn("ahorro", r)
        self.assertFalse(r["ahorro"]["activo"])


class TestWriteState(unittest.TestCase):
    def test_escritura_atomica(self):
        original = sm.STATE_FILE
        tmp = Path(tempfile.mktemp(suffix=".json"))
        try:
            sm.STATE_FILE = tmp
            state = {"test": True, "timestamp": "2026-07-14T12:00:00"}
            sm.write_state(state)
            self.assertTrue(tmp.exists())
            loaded = json.loads(tmp.read_text())
            self.assertEqual(loaded["test"], True)
        finally:
            sm.STATE_FILE = original
            if tmp.exists():
                tmp.unlink()


class TestReadSecret(unittest.TestCase):
    def test_secret_existe(self):
        tmp = Path(tempfile.mktemp())
        tmp.write_text("mi-clave-secreta\n")
        try:
            original = sm.SECRETS_DIR
            sm.SECRETS_DIR = tmp.parent
            r = sm.read_secret(tmp.name)
            self.assertEqual(r, "mi-clave-secreta")
            sm.SECRETS_DIR = original
        finally:
            tmp.unlink()

    def test_secret_no_existe(self):
        r = sm.read_secret("archivo-inexistente.key")
        self.assertEqual(r, "")


class TestCollectState(unittest.TestCase):
    def test_tiene_todos_los_campos(self):
        with (
            patch.object(sm, "get_gpu", return_value={"modelo": "test", "vram_total_mb": 0, "vram_usada_mb": 0, "vram_libre_mb": 0, "temp_c": 0, "utilizacion_pct": 0}),
            patch.object(sm, "get_system", return_value={"ram_total_gb": 0, "ram_libre_gb": 0, "ram_disponible_gb": 0, "cpu_load": 0, "disco_root_libre_gb": 0, "disco_ssd_libre_gb": 0}),
            patch.object(sm, "check_ollama", return_value={"activo": False, "version": None, "modelos": [], "modelo_cargado": None}),
            patch.object(sm, "check_lmstudio", return_value={"activo": False, "version": None, "modelos": []}),
            patch.object(sm, "check_n8n", return_value={"activo": False, "version": None}),
            patch.object(sm, "check_service", return_value={"activo": False}),
            patch.object(sm, "read_secret", return_value=""),
            patch.object(sm, "check_cloud", return_value={"disponible": False, "saldo_usd": None, "latencia_ms": None}),
        ):
            state = sm.collect_state()
            self.assertIn("timestamp", state)
            self.assertIn("gpu", state)
            self.assertIn("system", state)
            self.assertIn("services", state)
            self.assertIn("cloud", state)
            self.assertIn("policies", state)
            self.assertEqual(len(state["services"]), 6)
            for s in ["ollama", "lmstudio", "n8n", "stirling_pdf", "pdf_cleaner", "monitor_flask"]:
                self.assertIn(s, state["services"])
            self.assertIn("deepseek", state["cloud"])
            self.assertIn("gemini", state["cloud"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
