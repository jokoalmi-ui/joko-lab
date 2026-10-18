#!/usr/bin/env python3
"""
Tests de las funciones extraidas de main() (refactor 07-ago-2026 con
OpenCode): _contar_sesiones y _construir_resumen.

Red de seguridad: flujo main() identico en entorno aislado (mocks: sin
export real, sin eventos reales, dirs temporales) + estos tests fijan cada
pieza.

Ejecucion:
  cd ~/joko-lab && python3 -m unittest tests/test_consolidador_sesiones.py -v
"""

import io
import sys
import unittest
from datetime import datetime, timedelta
from pathlib import Path

TOOLS_DIR = str(Path(__file__).resolve().parent.parent / "tools")
sys.path.insert(0, TOOLS_DIR)

from consolidador_sesiones import _contar_sesiones, _construir_resumen

HOY = datetime(2026, 8, 7, 12, 0)
AYER = HOY - timedelta(days=1)


class TestContarSesiones(unittest.TestCase):
    def test_tipos_de_timestamp(self):
        ayer_iso = AYER.strftime("%Y-%m-%dT10:00:00")
        fh = io.StringIO(
            '{"timestamp": 1750000000, "id": "s1"}\n'
            f'{{"started_at": "{ayer_iso}", "id": "s2"}}\n'
            '{"created_at": 1750000001, "id": "s3"}\n'
            '{"timestamp": "no-ts", "id": "s4"}\n'
            'no-json\n'
            '\n'
        )
        por_fecha, con_ayer, con_total = _contar_sesiones(fh, AYER)
        self.assertEqual(con_total, 5)  # 4 validas + 1 no-json (no-json no cuenta)
        self.assertEqual(con_ayer, 1)   # solo s2 es de ayer
        # s1/s3 (epoch) caen en 2025; s2 en ayer; s4 sin fecha
        self.assertIn(AYER.strftime("%Y-%m-%d"), por_fecha)

    def test_vacio(self):
        por_fecha, con_ayer, con_total = _contar_sesiones(io.StringIO(""), AYER)
        self.assertEqual((por_fecha, con_ayer, con_total), ({}, 0, 0))


class TestConstruirResumen(unittest.TestCase):
    def test_estructura_y_textos(self):
        por_fecha = {"2026-08-06": 2, AYER.strftime("%Y-%m-%d"): 1}
        lineas = _construir_resumen(HOY, AYER, por_fecha, 3, 1)
        texto = "\n".join(lineas)
        self.assertIn(f"# Resumen de sesiones — {AYER.strftime('%Y-%m-%d')}", texto)
        self.assertIn("Total sesiones registradas: 3", texto)
        self.assertIn(f"Sesiones del día {AYER.strftime('%Y-%m-%d')}: 1", texto)
        self.assertIn("## Sesiones por día (últimos 7)", texto)
        self.assertIn("| Fecha | Sesiones |", texto)
        self.assertIn("## Nota para Hermes", texto)
        self.assertIn("cron 22:30", texto)

    def test_ultimos_7_dias(self):
        por_fecha = {f"2026-08-{i:02d}": i for i in range(1, 12)}
        lineas = _construir_resumen(HOY, AYER, por_fecha, 0, 0)
        # solo 7 filas de tabla + cabecera + separador
        filas = [l for l in lineas if l.startswith("| 2026-08-")]
        self.assertEqual(len(filas), 7)


if __name__ == "__main__":
    unittest.main()
