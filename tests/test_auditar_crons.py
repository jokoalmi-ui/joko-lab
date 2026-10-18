#!/usr/bin/env python3
"""
Tests de las funciones puras de tools/auditar_crons.py (auto-mejora 12-oct-2026).

Cubre las 3 capas del auditor: estado de los jobs (streak/atascado/entrega),
criterio AMPLIADO de fallo de los informes ('**Status:** script failed', la
senal que los instrumentos previos no veian), agrupacion sin ruido y entregas
fallidas desde una deliveries.db temporal. Todo con directorios temporales:
NUNCA se leen los datos reales del lab.

Ejecucion:
  cd ~/joko-lab && python3 -m unittest tests.test_auditar_crons -v
"""

import json
import os
import sqlite3
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

TOOLS_DIR = str(Path(__file__).resolve().parent.parent / "tools")
sys.path.insert(0, TOOLS_DIR)

import auditar_crons as ac

AHORA = datetime(2026, 10, 12, 12, 0, tzinfo=timezone.utc)
HACE = timedelta(hours=48)


def _informe(directorio, job_id, nombre, texto):
    """Escribe un informe falso en <directorio>/output/<job_id>/<nombre>."""
    d = Path(directorio) / "output" / job_id
    d.mkdir(parents=True, exist_ok=True)
    f = d / nombre
    f.write_text(texto, encoding="utf-8")
    return f


class TestParsearIso(unittest.TestCase):
    def test_con_offset(self):
        d = ac._parsear_iso("2026-10-12T08:05:45.196395+02:00")
        self.assertEqual(d.astimezone(timezone.utc).hour, 6)

    def test_sin_offset_es_utc(self):
        self.assertEqual(ac._parsear_iso("2026-10-12T08:05:45").tzinfo, timezone.utc)

    def test_invalido_y_vacio(self):
        self.assertIsNone(ac._parsear_iso("nunca"))
        self.assertIsNone(ac._parsear_iso(None))
        self.assertIsNone(ac._parsear_iso(3))


class TestCargarJobs(unittest.TestCase):
    def test_dict_con_clave_jobs(self):
        with tempfile.TemporaryDirectory() as t:
            p = Path(t) / "jobs.json"
            p.write_text(json.dumps({"jobs": [{"id": "a"}]}), encoding="utf-8")
            self.assertEqual(len(ac._cargar_jobs(p)), 1)

    def test_lista_pelada(self):
        with tempfile.TemporaryDirectory() as t:
            p = Path(t) / "jobs.json"
            p.write_text(json.dumps([{"id": "a"}, {"id": "b"}]), encoding="utf-8")
            self.assertEqual(len(ac._cargar_jobs(p)), 2)

    def test_archivo_inexistente_o_corrupto(self):
        self.assertEqual(ac._cargar_jobs(Path("/tmp/no_existe_jobs.json")), [])


class TestFalloDeInforme(unittest.TestCase):
    """La senal que faltaba en el watchdog: '**Status:** script failed'."""

    def test_status_script_failed(self):
        with tempfile.TemporaryDirectory() as t:
            f = _informe(t, "abc", "2026-10-12_08-05-44.md",
                         "# Cron Job: rag-reindex-daily\n\n**Status:** script failed\n\n"
                         "Script timed out after 300s: /home/x/rag-reindex.sh\n")
            self.assertTrue(ac._fallo_de_informe(f, AHORA - HACE))

    def test_failed_en_cabecera(self):
        with tempfile.TemporaryDirectory() as t:
            f = _informe(t, "abc", "x.md", "# Cron Job: x (FAILED)\n\nok\n")
            self.assertEqual(ac._fallo_de_informe(f, AHORA - HACE), "(FAILED)")

    def test_error_en_cola(self):
        with tempfile.TemporaryDirectory() as t:
            f = _informe(t, "abc", "x.md", "# Cron Job: x\n\n" + "ruido\n" * 300
                         + "\n## Error\nTraceback: boom\n")
            self.assertEqual(ac._fallo_de_informe(f, AHORA - HACE), "## Error")

    def test_informe_correcto_no_es_fallo(self):
        with tempfile.TemporaryDirectory() as t:
            f = _informe(t, "abc", "x.md",
                         "# Cron Job: x\n\n**Status:** ok\n\n[✓] Todo bien: 45677 "
                         "fragmentos ya indexados.\n")
            self.assertIsNone(ac._fallo_de_informe(f, AHORA - HACE))

    def test_fuera_de_ventana_por_mtime(self):
        with tempfile.TemporaryDirectory() as t:
            f = _informe(t, "abc", "x.md", "# Cron Job: x\n\n**Status:** script failed\n")
            viejo = (AHORA - timedelta(days=30)).timestamp()
            os.utime(f, (viejo, viejo))
            self.assertIsNone(ac._fallo_de_informe(f, AHORA - HACE))


class TestFallosDeInformes(unittest.TestCase):
    def test_agrupa_por_job_y_senal(self):
        with tempfile.TemporaryDirectory() as t:
            for h in ("00-13-26", "00-32-38", "00-51-50"):
                _informe(t, "teler", "2026-10-12_%s.md" % h,
                         "# Cron Job: telegram-watchdog\n\n**Status:** script failed\n")
            _informe(t, "otro", "2026-10-12_08-05-44.md",
                     "# Cron Job: rag-reindex\n\n**Status:** script failed\n")
            h = ac._fallos_de_informes(Path(t) / "output", AHORA - HACE,
                                       {"teler": "telegram-watchdog", "otro": "rag-reindex"})
            self.assertEqual(len(h), 2)
            por_job = {x["job"]: x for x in h}
            self.assertIn("3 corrida(s) fallida(s)", por_job["telegram-watchdog"]["detalle"])
            self.assertEqual(por_job["rag-reindex"]["id"], "otro")

    def test_sin_directorio_output(self):
        with tempfile.TemporaryDirectory() as t:
            self.assertEqual(ac._fallos_de_informes(Path(t) / "output", AHORA - HACE, {}), [])


class TestEvaluarJob(unittest.TestCase):
    def test_job_sano_no_da_hallazgos(self):
        job = {"id": "a", "name": "sano", "enabled": True, "last_status": "ok",
               "failure_streak": 0, "next_run_at": (AHORA + timedelta(hours=1)).isoformat()}
        self.assertEqual(ac._evaluar_job(job, AHORA, 15), [])

    def test_fallo_repetido_y_ultimo_error(self):
        job = {"id": "b", "name": "consolidador", "enabled": True,
               "last_status": "error", "failure_streak": 11,
               "last_error": "cron worker exited with status -15", "next_run_at": None,
               "last_run_at": "2026-10-11T22:31:20+02:00"}
        h = ac._evaluar_job(job, AHORA, 15)
        self.assertEqual(len(h), 2)
        self.assertIn("11 corrida", h[0]["detalle"])
        self.assertIn("ultimo_estado=error", h[1]["detalle"])

    def test_atascado_cuando_next_run_vencido(self):
        job = {"id": "c", "name": "recordatorio", "enabled": True, "last_status": "ok",
               "failure_streak": 0, "last_run_at": None,
               "next_run_at": (AHORA - timedelta(days=11)).isoformat()}
        h = ac._evaluar_job(job, AHORA, 15)
        self.assertEqual(len(h), 1)
        self.assertIn("atascado", h[0]["detalle"])

    def test_atascado_no_se_reporta_dentro_de_la_tolerancia(self):
        job = {"id": "d", "name": "reciente", "enabled": True, "last_status": "ok",
               "failure_streak": 0, "next_run_at": (AHORA - timedelta(minutes=5)).isoformat()}
        self.assertEqual(ac._evaluar_job(job, AHORA, 15), [])

    def test_job_pausado_atascado_no_cuenta(self):
        job = {"id": "e", "name": "pausado", "enabled": False, "last_status": "ok",
               "failure_streak": 0, "next_run_at": (AHORA - timedelta(days=9)).isoformat()}
        self.assertEqual(ac._evaluar_job(job, AHORA, 15), [])

    def test_entrega_del_ultimo_run(self):
        job = {"id": "f", "name": "rag", "enabled": True, "last_status": "ok",
               "failure_streak": 0, "next_run_at": None,
               "last_delivery_error": "Telegram send failed: Timed out"}
        h = ac._evaluar_job(job, AHORA, 15)
        self.assertEqual(h[0]["tipo"], "entrega")


def _db_entregas(ruta, filas):
    con = sqlite3.connect(str(ruta))
    con.execute("create table deliveries (created_at text, status text, error text)")
    con.executemany("insert into deliveries values (?,?,?)", filas)
    con.commit()
    con.close()


class TestEntregasFallidas(unittest.TestCase):
    def _db(self, t):
        ruta = Path(t) / "deliveries.db"
        _db_entregas(ruta, [
            ("2026-10-12T00:03:55.999648+02:00", "failed",
             "delivery error: Telegram send failed: Timed out"),
            ("2026-09-30T22:00:00+02:00", "failed", "live adapter send failed"),
            ("2026-10-12T09:00:00+02:00", "delivered", None),
        ])
        return ruta

    def test_solo_falla_la_de_la_ventana_y_cuenta_historico(self):
        with tempfile.TemporaryDirectory() as t:
            h, en_ventana, hist = ac._entregas_fallidas(self._db(t), AHORA - HACE)
            self.assertEqual((en_ventana, hist), (1, 2))
            self.assertEqual(len(h), 1)
            self.assertIn("1 entrega(s) fallida(s)", h[0]["detalle"])
            self.assertIn("Timed out", h[0]["detalle"])
            self.assertEqual(h[0]["tipo"], "entrega")

    def test_db_ausente_no_revienta(self):
        h, en_ventana, hist = ac._entregas_fallidas(Path("/tmp/no_deliveries.db"), AHORA)
        self.assertEqual((h, en_ventana, hist), ([], 0, 0))


class TestRecolectarYMain(unittest.TestCase):
    def _base_limpia(self, t):
        base = Path(t) / "cron"
        (base / "output" / "ok1").mkdir(parents=True)
        (base / "jobs.json").write_text(json.dumps({"jobs": [
            {"id": "ok1", "name": "sano", "enabled": True, "last_status": "ok",
             "failure_streak": 0, "next_run_at": (AHORA + timedelta(hours=2)).isoformat()},
        ]}), encoding="utf-8")
        return base

    def _base_con_fallos(self, t):
        base = self._base_limpia(t)
        _informe(base, "ok1", "2026-10-12_08-05-44.md",
                 "# Cron Job: sano\n\n**Status:** script failed\n")
        _db_entregas(base / "deliveries.db", [
            ("2026-10-12T00:03:55.999648+02:00", "failed", "Timed out"),
        ])
        return base

    def test_base_limpia_da_ok(self):
        with tempfile.TemporaryDirectory() as t:
            datos = ac._recolectar(self._base_limpia(t), 48, 15, AHORA)
            self.assertEqual(datos["hallazgos"], [])
            self.assertTrue(json.loads(ac._json(datos))["ok"])

    def test_main_exit_1_y_json_parseable_con_fallos(self):
        with tempfile.TemporaryDirectory() as t:
            base = self._base_con_fallos(t)
            datos = ac._recolectar(base, 48, 15, AHORA)
            self.assertEqual(len({h["tipo"] for h in datos["hallazgos"]}), 2)
            os.environ["AUDITOR_CRONS_DIR"] = str(base)
            try:
                self.assertEqual(ac.main(["--json"]), 1)
                self.assertEqual(ac.main([]), 1)
            finally:
                os.environ.pop("AUDITOR_CRONS_DIR", None)

    def test_main_exit_0_base_limpia(self):
        with tempfile.TemporaryDirectory() as t:
            os.environ["AUDITOR_CRONS_DIR"] = str(self._base_limpia(t))
            try:
                self.assertEqual(ac.main(["--json"]), 0)
            finally:
                os.environ.pop("AUDITOR_CRONS_DIR", None)


if __name__ == "__main__":
    unittest.main()
