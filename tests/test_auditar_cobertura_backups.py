#!/usr/bin/env python3
"""
Tests de tools/auditar_cobertura_backups.py (herramienta creada 14-sep-2026
en la sesión semanal de auto-mejora).

Carencia cubierta: no existía NINGUNA comprobación automática de qué almacenes
de datos del lab viven FUERA de la cadena diaria de backups (el hueco de
perfume-ia/data/coleccion.db se detectó a mano el 05-sep y quedó anotado sin
implementar el 08-09).

Los tests usan SIEMPRE directorios temporales: nunca el lab real.

Ejecución:
  cd ~/joko-lab && python3 -m unittest tests/test_auditar_cobertura_backups.py -v
"""

import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

TOOLS_DIR = str(Path(__file__).resolve().parent.parent / "tools")
sys.path.insert(0, TOOLS_DIR)

import auditar_cobertura_backups as acb  # noqa: E402

# Base temporal NEUTRA: en las sesiones de Hermes TMPDIR apunta a
# ~/.hermes/cache/scratch, y la tool excluye esa rama como ruido ("/.hermes/")
# -> los tests de inventario daban FALSOS ROJOS según quién ejecutara la suite.
# Se fuerza una base fuera del hogar para que el test sea hermético al entorno.
BASE_TEMPORAL = "/tmp"


def _escribir(ruta: Path, contenido: str = "x" * 10) -> Path:
    """Crea un archivo real (y sus directorios) con contenido mínimo."""
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(contenido)
    return ruta


class TestExtraerFuentes(unittest.TestCase):
    def test_extrae_src_hermes_y_source_ignora_dest(self):
        texto = (
            "#!/bin/bash\n"
            "# SRC=\"/comentado/no\"\n"
            'SRC="/home/jokoalmi/joko-lab/"\n'
            'HERMES="$HOME/.hermes"\n'
            'DEST="/mnt/ssd_ia_datos/backups-hermes"\n'
            'SOURCE="/home/jokoalmi/otra"\n'
            "KEEP=7\n"
        )
        fuentes = acb.extraer_fuentes(texto, "script.sh")
        rutas = [str(r) for r, _ in fuentes]
        self.assertEqual(rutas, [
            "/home/jokoalmi/joko-lab",
            str(Path.home() / ".hermes"),
            "/home/jokoalmi/otra",
        ])
        self.assertEqual({o for _, o in fuentes}, {"script.sh"})

    def test_ignora_lineas_sin_comillas_de_asignacion(self):
        self.assertEqual(acb.extraer_fuentes("SRC=$VACIO\nno es asignacion\n"), [])


class TestEstaCubierto(unittest.TestCase):
    def test_dentro_y_fuera(self):
        raices = ["/tmp/labbase"]
        self.assertTrue(acb.esta_cubierto("/tmp/labbase/sub/x.db", raices))
        self.assertTrue(acb.esta_cubierto("/tmp/labbase", raices))
        self.assertFalse(acb.esta_cubierto("/tmp/otro/x.db", raices))

    def test_trampa_de_prefijo(self):
        # /tmp/cubierto2 NO está dentro de /tmp/cubierto (trampa clásica de startswith)
        self.assertFalse(acb.esta_cubierto("/tmp/cubierto2/x.db", ["/tmp/cubierto"]))


class TestRuidoYAlmacen(unittest.TestCase):
    def test_es_ruido(self):
        for ruta in ("/home/j/x/node_modules/a.db",
                     "/home/j/proy/.venv/lib/x.jsonl",
                     "/home/j/.cache/tracker/meta.db",
                     "/home/j/perfume-ia/data/coleccion.db.BACKUP.20260730_091538",
                     "/home/j/x/coleccion.db.bak-20260809",
                     "/home/j/x/cafes.sqlite-wal",
                     "/home/j/joko-lab.BACKUP.20260914/x.db"):
            self.assertTrue(acb.es_ruido(ruta), ruta)

    def test_no_es_ruido(self):
        self.assertFalse(acb.es_ruido("/home/jokoalmi/perfume-ia/data/coleccion.db"))

    def test_es_almacen(self):
        for nombre in ("coleccion.db", "cafes.sqlite3", "datos.sqlite", "ledger.jsonl"):
            self.assertTrue(acb.es_almacen(nombre), nombre)
        for nombre in ("script.py", "notas.txt", "backup.tar.gz"):
            self.assertFalse(acb.es_almacen(nombre), nombre)


class TestCategoria(unittest.TestCase):
    def test_datos_del_lab(self):
        for ruta in ("/home/j/perfume-ia/data/coleccion.db",
                     "/home/j/cafe-ia/data/cafes.db"):
            self.assertEqual(acb.categoria(ruta), "datos", ruta)

    def test_apps_y_config(self):
        for ruta in ("/home/j/.config/google-chrome/Default/CdmStorage.db",
                     "/home/j/.pki/nssdb/key4.db",
                     "/home/j/hermes-lab/recovery/2026-09-09_17-06/sessions.jsonl",
                     "/home/j/ComfyUI/user/comfyui.db",
                     # 29-sep-2026: estado de apps externas (reinstalables) pasa
                     # a PATRONES_APP -> 'app', no 'datos' (ver backlog 29-sep)
                     "/home/j/.local/share/opencode/opencode.db",
                     "/home/j/.local/share/tirith/log.jsonl"):
            self.assertEqual(acb.categoria(ruta), "app", ruta)


class TestTamanoLegible(unittest.TestCase):
    def test_unidades(self):
        self.assertEqual(acb.tamano_legible(0), "0B")
        self.assertEqual(acb.tamano_legible(1024), "1.0K")
        self.assertEqual(acb.tamano_legible(1024 ** 2), "1.0M")
        self.assertEqual(acb.tamano_legible(3 * 1024 ** 3), "3.0G")

    def test_total_bytes(self):
        items = [{"bytes": 10}, {"bytes": 32}]
        self.assertEqual(acb.total_bytes(items), 42)


class TestInventarioConTemporales(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(dir=BASE_TEMPORAL)
        self.base = Path(self._tmp.name)
        _escribir(self.base / "data/coleccion.db")
        _escribir(self.base / "data/notas.txt")
        _escribir(self.base / "data/logs/chat_20260914.jsonl")
        _escribir(self.base / "data/viejo.db.BACKUP.20260802")
        _escribir(self.base / "cubierto/cafes.db")
        _escribir(self.base / "proy/node_modules/dep.db")
        self.raices = [self.base / "cubierto"]

    def tearDown(self):
        self._tmp.cleanup()

    def test_clasifica_cubiertos_y_ruido(self):
        items = acb.inventariar(self.base, profundidad=5, raices=self.raices)
        rutas = {Path(i["ruta"]).name: i for i in items}
        # cafes.db vive DENTRO de la raíz cubierta -> se poda del escaneo
        self.assertEqual(set(rutas), {"coleccion.db", "chat_20260914.jsonl"})
        self.assertFalse(rutas["coleccion.db"]["cubierto"])
        self.assertFalse(rutas["chat_20260914.jsonl"]["cubierto"])
        self.assertEqual(rutas["coleccion.db"]["bytes"], 10)

    def test_almacen_en_raiz_cubierta_se_clasifica_cubierto(self):
        items = acb.inventariar(self.base / "cubierto", profundidad=2,
                                raices=self.raices)
        self.assertEqual(len(items), 1)
        self.assertTrue(items[0]["cubierto"])

    def test_profundidad_limita_el_escaneo(self):
        items = acb.inventariar(self.base, profundidad=1, raices=self.raices)
        self.assertEqual([Path(i["ruta"]).name for i in items], [])

    def test_no_cubiertos_primero(self):
        items = acb.inventariar(self.base, profundidad=5, raices=self.raices)
        self.assertFalse(items[0]["cubierto"])


class TestInforme(unittest.TestCase):
    def setUp(self):
        self.items = [
            {"ruta": "/home/j/perfume-ia/data/coleccion.db", "bytes": 348160,
             "mtime": "2026-09-14", "cubierto": False, "categoria": "datos"},
            {"ruta": "/home/j/.config/google-chrome/Default/CdmStorage.db",
             "bytes": 163840, "mtime": "2026-07-28", "cubierto": False,
             "categoria": "app"},
            {"ruta": "/home/j/joko-lab/x.db", "bytes": 2048,
             "mtime": "2026-09-14", "cubierto": True, "categoria": "datos"},
        ]
        self.raices = [(Path("/home/joko-lab"), "backup-joko-lab.sh")]

    def test_informe_contiene_secciones_y_accion(self):
        informe = acb.formatear_informe(self.items, self.raices)
        self.assertIn("Raíces cubiertas", informe)
        self.assertIn("Datos del lab NO cubiertos (1)", informe)
        self.assertIn("Apps/config fuera de la cadena: 1 ficheros", informe)
        self.assertIn("Almacenes cubiertos (1)", informe)
        self.assertIn("coleccion.db", informe)
        self.assertIn("340.0K", informe)
        self.assertIn("1 almacén(es) de datos fuera de la cadena", informe)

    def test_informe_todo_cubierto(self):
        informe = acb.formatear_informe([self.items[2]], self.raices)
        self.assertIn("Datos del lab NO cubiertos (0)", informe)
        self.assertIn("Todos los datos del lab detectados están dentro", informe)

    def test_huecos_lab_solo_datos_sin_cubrir(self):
        huecos = acb.huecos_lab(self.items)
        self.assertEqual([h["ruta"] for h in huecos],
                         ["/home/j/perfume-ia/data/coleccion.db"])

    def test_resumen_json_es_serializable(self):
        resumen = acb._resumen_json(self.items, self.raices)
        texto = json.dumps(resumen, ensure_ascii=False)
        self.assertIn("datos_no_cubiertos", texto)
        self.assertEqual(resumen["total"], 3)
        self.assertEqual(resumen["cubiertos"], 1)
        self.assertEqual(resumen["app_no_cubiertos"], 1)
        self.assertEqual(len(resumen["datos_no_cubiertos"]), 1)


class TestMain(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(dir=BASE_TEMPORAL)
        self.base = Path(self._tmp.name)
        _escribir(self.base / "data/coleccion.db")
        _escribir(self.base / ".config/chrome/x.db")

    def tearDown(self):
        self._tmp.cleanup()

    def test_main_devuelve_1_si_hay_datos_no_cubiertos(self):
        salida = io.StringIO()
        with redirect_stdout(salida):
            codigo = acb.main(["--base", str(self.base), "--json"])
        self.assertEqual(codigo, 1)
        datos = json.loads(salida.getvalue())
        self.assertEqual(datos["datos_no_cubiertos"][0]["ruta"],
                         str(self.base / "data/coleccion.db"))
        self.assertEqual(datos["app_no_cubiertos"], 1)

    def test_main_devuelve_0_si_la_raiz_lo_cubre(self):
        salida = io.StringIO()
        with redirect_stdout(salida):
            codigo = acb.main(["--base", str(self.base), "--raiz", str(self.base),
                               "--solo-no-cubiertos"])
        self.assertEqual(codigo, 0)
        self.assertEqual(salida.getvalue().strip(), "")


if __name__ == "__main__":
    unittest.main()
