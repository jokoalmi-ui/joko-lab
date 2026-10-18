#!/usr/bin/env python3
"""Tests unitarios de las funciones extraídas de medir_agentic.main() (09-ago-2026).

Cubren: _parsear_args, _clasificar_y_contar (4 ramas + contadores),
_construir_resultado, _guardar_history, _imprimir_json, _imprimir_texto.
Sin dependencias pesadas (import del módulo OK con python3 del sistema).
"""
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, "/home/jokoalmi/joko-lab/tools")
import medir_agentic as ma


def _cobertura(ok: bool) -> dict:
    return {
        "cobertura_ok": ok,
        "faltantes": [] if ok else ["x", "y"],
        "fuentes_esperadas": [],
        "fuentes_encontradas": [],
        "fuentes_completas": 0 if ok else 1,
    }


def _modo(ok: bool) -> dict:
    return {
        "max_iter": 1,
        "parada": "cobertura" if ok else "max_iter",
        "busquedas": 1,
        "duracion_s": 0.123,
        "cobertura_ok": ok,
        "faltantes": [] if ok else ["x", "y"],
        "fuentes_esperadas": [],
        "fuentes_encontradas": [],
        "fuentes_completas": 0 if ok else 1,
        "paths_ultima": ["/vault/a.md"],
        "ultima_cobertura": _cobertura(ok),
    }


def _resumen():
    return {
        "total": 1,
        "clasico_ok": 0,
        "agentic_ok": 0,
        "agentic_resuelve_adicional": 0,
        "sin_mejora": 0,
        "ambos_incompletos": 0,
    }


class TestParsearArgs(unittest.TestCase):
    def test_defaults(self):
        args = ma._parsear_args([])
        self.assertEqual(args.top_k, 5)
        self.assertEqual(args.max_iter, 3)
        self.assertFalse(args.json)
        self.assertFalse(args.no_history)
        self.assertEqual(args.bank, str(ma.BANCO_DEFAULT))

    def test_personalizados(self):
        args = ma._parsear_args(["--top-k", "7", "--max-iter", "4", "--json", "--no-history"])
        self.assertEqual(args.top_k, 7)
        self.assertEqual(args.max_iter, 4)
        self.assertTrue(args.json)
        self.assertTrue(args.no_history)


class TestClasificarYContar(unittest.TestCase):
    def test_agentic_resuelve(self):
        r = _resumen()
        marca = ma._clasificar_y_contar(_modo(False), _modo(True), r)
        self.assertEqual(marca, "AGENTIC_RESUELVE")
        self.assertEqual(r["agentic_resuelve_adicional"], 1)
        self.assertEqual(r["clasico_ok"], 0)
        self.assertEqual(r["agentic_ok"], 1)

    def test_sin_mejora(self):
        r = _resumen()
        marca = ma._clasificar_y_contar(_modo(True), _modo(True), r)
        self.assertEqual(marca, "SIN_MEJORA")
        self.assertEqual(r["sin_mejora"], 1)
        self.assertEqual(r["clasico_ok"], 1)
        self.assertEqual(r["agentic_ok"], 1)
        self.assertEqual(r["ambos_incompletos"], 0)

    def test_ambos_incompletos(self):
        r = _resumen()
        marca = ma._clasificar_y_contar(_modo(False), _modo(False), r)
        self.assertEqual(marca, "AMBOS_INCOMPLETOS")
        self.assertEqual(r["sin_mejora"], 1)
        self.assertEqual(r["ambos_incompletos"], 1)

    def test_clasico_mejor(self):
        r = _resumen()
        marca = ma._clasificar_y_contar(_modo(True), _modo(False), r)
        self.assertEqual(marca, "CLASICO_MEJOR")
        self.assertEqual(r["sin_mejora"], 0)
        self.assertEqual(r["agentic_resuelve_adicional"], 0)


class TestConstruirResultado(unittest.TestCase):
    def test_redondeo_y_campos(self):
        args = ma._parsear_args(["--bank", "/tmp/b.yaml", "--top-k", "5", "--max-iter", "3"])
        resumen = _resumen()
        res = ma._construir_resultado(args, [], resumen, [], 1.2345, 9.8765)
        self.assertEqual(res["resumen"]["tiempo_clasico_s"], 1.23)
        self.assertEqual(res["resumen"]["tiempo_agentic_s"], 9.88)
        self.assertEqual(res["top_k"], 5)
        self.assertEqual(res["banco"], "/tmp/b.yaml")
        self.assertIn("timestamp", res)
        self.assertEqual(res["detalle"], [])


class TestGuardarHistory(unittest.TestCase):
    def test_no_history_no_escribe(self):
        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d) / "history.jsonl"
            ma.HISTORY = tmp
            ma._guardar_history({"a": 1}, no_history=True)
            self.assertFalse(tmp.exists())

    def test_escribe_linea_jsonl(self):
        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d) / "history.jsonl"
            ma.HISTORY = tmp
            ma._guardar_history({"a": 1}, no_history=False)
            lineas = tmp.read_text(encoding="utf-8").strip().splitlines()
            self.assertEqual(len(lineas), 1)
            self.assertEqual(json.loads(lineas[0]), {"a": 1})

    def test_oserror_avisa_stderr(self):
        ma.HISTORY = Path("/proc/no_permitido/history.jsonl")
        err = io.StringIO()
        with redirect_stdout(io.StringIO()):
            old_stderr, sys.stderr = sys.stderr, err
            try:
                ma._guardar_history({"a": 1}, no_history=False)
            finally:
                sys.stderr = old_stderr
        self.assertIn("aviso", err.getvalue())


class TestImprimirJson(unittest.TestCase):
    def test_salida_json_valida(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            ma._imprimir_json({"clave": "valor", "n": 1})
        parsed = json.loads(buf.getvalue())
        self.assertEqual(parsed, {"clave": "valor", "n": 1})


class TestImprimirTexto(unittest.TestCase):
    def _resultado(self):
        r = _resumen()
        r["total"] = 6
        r.update({"clasico_ok": 2, "agentic_ok": 3,
                  "agentic_resuelve_adicional": 1, "sin_mejora": 2,
                  "ambos_incompletos": 1, "tiempo_clasico_s": 1.5,
                  "tiempo_agentic_s": 3.2})
        return {
            "timestamp": "2026-08-09T00:00:00",
            "top_k": 5,
            "max_iter_agentic": 3,
            "banco": "/tmp/b.yaml",
            "resumen": r,
            "detalle": [
                {"id": "B1", "pregunta": "pregunta b", "mejora": "AGENTIC_RESUELVE",
                 "clasico": _modo(False), "agentic": _modo(True)},
                {"id": "A1", "pregunta": "pregunta a", "mejora": "SIN_MEJORA",
                 "clasico": _modo(True), "agentic": _modo(True)},
            ],
        }

    def test_lineas_clave(self):
        lineas = ma._imprimir_texto(self._resultado())
        texto = "\n".join(lineas)
        self.assertIn("Cobertura clásica (1 búsqueda):  2/6", texto)
        self.assertIn("Cobertura agentic (loop):        3/6", texto)
        self.assertIn("▲ AGENTIC] B1: pregunta b", texto)
        self.assertIn("=  IGUAL] A1: pregunta a", texto)
        self.assertTrue(lineas[-1] == "")

    def test_termina_con_linea_vacia(self):
        lineas = ma._imprimir_texto(self._resultado())
        self.assertEqual(lineas[-1], "")


if __name__ == "__main__":
    unittest.main()
