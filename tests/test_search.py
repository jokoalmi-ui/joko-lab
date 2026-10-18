#!/usr/bin/env python3
"""
Tests de red de seguridad de search.py (28-sep-2026, sesión de auto-mejora).

POR QUÉ ESTE FICHERO: `tools/auditor_deuda_tools.py` sitúa a `search` como la
tool de MAYOR riesgo del lab (score 71: 1 ref en cron, 3 en scripts, 58 en
skills, 37 en código) y hasta hoy era la única del top con **cero tests** — es
la vía del RAG que usan a diario Hermes, las skills y memory_detective.

Qué cubre (sin tocar NADA del lab):
  - _construir_where   → cláusula where de LanceDB a partir de los filtros.
  - _calcular_rrf      → fusión por rango recíproco (Reciprocal Rank Fusion).
  - _busqueda_hibrida  → FTS + vectorial + RRF sobre una tabla LanceDB TEMPORAL.
  - _buscar_qs         → Query/Summary Indexing (umbral sim > 0.35, dedupe).
  - query_index        → flujo COMPLETO (dedupe por path, top_k, filtros,
                         telemetría, extras QS, fallback si falla la híbrida).
  - rerank_via_daemon  → contrato HTTP del daemon (urllib mockeado).
  - _log_query         → solo el camino de error: NUNCA debe lanzar.

AISLAMIENTO (crítico): toda la base de datos es temporal (`tempfile`); el
test NUNCA abre `/home/jokoalmi/joko-lab/.lancedb` ni escribe en
`/mnt/ssd_ia_datos/lab-state/rag-query-ledger.jsonl` (allí `_log_query` va
mockeado). El encoder y el reranker también van mockeados: no se llama a
LM Studio ni se carga torch.

REQUIERE el venv del RAG (search.py importa lancedb a nivel de módulo):
  ~/.venv/hermes-rag/bin/python3 -m unittest discover -s tests
Con el python3 del sistema hace skip limpio (pitfall 9 de refactor-seguro).
"""

import contextlib
import io
import json
import shutil
import sys
import tempfile
import unittest
import warnings
from pathlib import Path
from unittest import mock

TOOLS_DIR = str(Path(__file__).resolve().parent.parent / "tools")
sys.path.insert(0, TOOLS_DIR)

try:
    import lancedb
    import search as S
    DISPONIBLE = True
except ImportError as e:  # sin lancedb (python del sistema) → skip limpio
    DISPONIBLE = False
    _IMPORT_ERR = str(e)

# Vector de consulta fijo: evita depender del encoder (LM Studio / BGE-M3).
QV = [1.0, 0.0, 0.0]


def _fila(id_, path, text, vector, type_="KO", status="activo", tags="perfume"):
    """Fila del esquema de joko_notes (id, path, text, type, status, tags, vector)."""
    return {"id": id_, "path": path, "text": text, "type": type_,
            "status": status, "tags": tags, "vector": list(vector)}


def _crear_db_temporal(filas, summaries=None, consultas=None, con_fts=True):
    """Crea una LanceDB TEMPORAL con joko_notes (+ tablas QS opcionales)."""
    tmp = Path(tempfile.mkdtemp(prefix="test_search_"))
    db_path = tmp / "db"
    db = lancedb.connect(str(db_path))
    tabla = db.create_table("joko_notes", data=filas)
    if con_fts:
        try:
            # create_fts_index está deprecado en lancedb >= 0.25 (sigue
            # funcionando): se silencia el DeprecatedWarning para no inundar
            # la salida de la suite.
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                tabla.create_fts_index("text")
        except Exception:
            pass  # sin FTS la híbrida sigue funcionando (fts_ids = [])
    if summaries:
        db.create_table("joko_summaries", data=summaries)
    if consultas:
        db.create_table("joko_queries", data=consultas)
    return tmp, db_path, db, tabla


class _ReordenadorFalso:
    """Reranker de mentira: mantiene el orden de entrada (scores decrecientes)."""

    def predict(self, pares):
        return [float(len(pares) - i) for i in range(len(pares))]


@unittest.skipUnless(
    DISPONIBLE,
    f"deps del RAG no disponibles en este intérprete: {globals().get('_IMPORT_ERR', '')}")
class BaseTemporal(unittest.TestCase):
    """Base con limpieza de los directorios temporales creados por cada test."""

    def setUp(self):
        self._temporales = []

    def tearDown(self):
        for tmp in self._temporales:
            shutil.rmtree(tmp, ignore_errors=True)

    def crear(self, filas, summaries=None, consultas=None, con_fts=True):
        tmp, db_path, db, tabla = _crear_db_temporal(
            filas, summaries=summaries, consultas=consultas, con_fts=con_fts)
        self._temporales.append(tmp)
        return db_path, db, tabla

    def ejecutar_query_index(self, db_path, consulta="vetiver", top_k=3, **kwargs):
        """Ejecuta query_index con encoder/reranker/telemetría mockeados.

        Captura stdout Y stderr (los avisos de fallback de search.py van a
        stderr). Devuelve (salida_capturada, mock_de_log_query).
        """
        log = mock.Mock()
        with mock.patch.object(S, "DB_PATH", db_path), \
                mock.patch.object(S, "_encode", lambda _t: list(QV)), \
                mock.patch.object(S, "_daemon_disponible", lambda: False), \
                mock.patch.object(S, "get_reranker", lambda: _ReordenadorFalso()), \
                mock.patch.object(S, "_log_query", log):
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
                S.query_index(consulta, top_k=top_k, **kwargs)
        return buf.getvalue(), log


class TestConstruirWhere(BaseTemporal):
    """Cláusula where de LanceDB: 4 combinaciones posibles de filtros."""

    def test_sin_filtros_devuelve_vacio(self):
        self.assertEqual(S._construir_where(None, None), "")

    def test_solo_type(self):
        self.assertEqual(S._construir_where("RULE", None), "type = 'RULE'")

    def test_solo_status(self):
        self.assertEqual(S._construir_where(None, "activo"), "status = 'activo'")

    def test_type_y_status_unidos_por_and(self):
        self.assertEqual(S._construir_where("RULE", "activo"),
                         "type = 'RULE' AND status = 'activo'")

    def test_cadena_vacia_equivale_a_sin_filtro(self):
        # "" es falsy: no debe generar cláusula (contrato del `if filtro_type`)
        self.assertEqual(S._construir_where("", ""), "")


class TestCalcularRRF(BaseTemporal):
    """Fusión por rango recíproco: score = suma de 1/(K + rango), rango base 1."""

    def test_listas_vacias(self):
        self.assertEqual(S._calcular_rrf([], []), {})

    def test_una_sola_lista(self):
        self.assertEqual(S._calcular_rrf(["a", "b"], [], K=60),
                         {"a": 1 / 61, "b": 1 / 62})

    def test_aparece_en_ambas_listas_suma(self):
        scores = S._calcular_rrf(["a"], ["a"], K=60)
        self.assertAlmostEqual(scores["a"], 2 / 61, places=12)

    def test_documento_en_ambas_supera_a_documento_en_una(self):
        scores = S._calcular_rrf(["a", "b"], ["b"], K=60)
        self.assertGreater(scores["b"], scores["a"])

    def test_rango_base_uno_no_cero(self):
        # El primero de la lista es 1/(K+1), NO 1/K (off-by-one documentado)
        self.assertAlmostEqual(S._calcular_rrf(["a"], [], K=60)["a"], 1 / 61, places=12)

    def test_K_personalizado(self):
        self.assertAlmostEqual(S._calcular_rrf(["a"], [], K=0)["a"], 1.0, places=12)


class TestBusquedaHibrida(BaseTemporal):
    """Híbrida FTS + vectorial + RRF sobre tabla temporal (sin modelo alguno)."""

    def test_columnas_resultado(self):
        _, _, tabla = self.crear([_fila("1", "p1.md", "vetiver amaderado", [1, 0, 0])])
        df = S._busqueda_hibrida(tabla, "vetiver", list(QV), 5)
        for col in ("id", "path", "text", "hybrid_rank", "_origen", "_orden_rrf"):
            self.assertIn(col, df.columns)
        self.assertNotIn("vector", df.columns)  # se descarta del DataFrame

    def test_documento_en_ambos_indices_marca_fts_mas_vec(self):
        _, _, tabla = self.crear([_fila("1", "p1.md", "vetiver amaderado", [1, 0, 0])])
        df = S._busqueda_hibrida(tabla, "vetiver", list(QV), 5)
        self.assertEqual(list(df["_origen"]), ["fts+vec"])
        # aparece con rango 0 en AMBAS listas → 1/61 + 1/61 = 2/61
        self.assertAlmostEqual(df.iloc[0]["hybrid_rank"], 2 / 61, places=12)

    def test_origen_fts_solo_si_solo_lo_trae_bm25(self):
        # A: coincide en texto pero su vector es el MÁS lejano → solo FTS
        # B: no coincide en texto pero su vector es idéntico a la query → solo vec
        filas = [_fila("A", "pa.md", "vetiver profundo", [0, 1, 0]),
                 _fila("B", "pb.md", "citrico luminoso", [1, 0, 0])]
        _, _, tabla = self.crear(filas)
        df = S._busqueda_hibrida(tabla, "vetiver", list(QV), 1)
        self.assertEqual(list(df["id"]), ["A"])
        self.assertEqual(list(df["_origen"]), ["fts"])

    def test_origen_vec_solo_si_solo_lo_trae_el_vector(self):
        # 3 filas y limit=2: A solo entra por FTS; el top-2 vectorial son B y C
        filas = [_fila("A", "pa.md", "vetiver profundo", [0, 1, 0]),
                 _fila("B", "pb.md", "citrico luminoso", [1, 0, 0]),
                 _fila("C", "pc.md", "nota salina", [0.98, 0.02, 0])]
        _, _, tabla = self.crear(filas)
        df = S._busqueda_hibrida(tabla, "vetiver", list(QV), 2)
        origenes = dict(zip(df["id"], df["_origen"]))
        self.assertEqual(origenes, {"A": "fts", "B": "vec"})

    def test_respeta_limit(self):
        filas = [_fila(str(i), f"p{i}.md", "vetiver", [1, 0.1 * i, 0]) for i in range(4)]
        _, _, tabla = self.crear(filas)
        self.assertEqual(len(S._busqueda_hibrida(tabla, "vetiver", list(QV), 2)), 2)

    def test_filtro_type_excluye_el_resto(self):
        filas = [_fila("1", "p1.md", "vetiver", [1, 0, 0], type_="KO"),
                 _fila("2", "p2.md", "vetiver", [0.9, 0.1, 0], type_="DOC")]
        _, _, tabla = self.crear(filas)
        df = S._busqueda_hibrida(tabla, "vetiver", list(QV), 5, filtro_type="KO")
        self.assertEqual(set(df["type"]), {"KO"})
        self.assertEqual(list(df["id"]), ["1"])

    def test_filtro_type_y_status(self):
        filas = [_fila("1", "p1.md", "vetiver", [1, 0, 0], status="activo"),
                 _fila("2", "p2.md", "vetiver", [0.9, 0.1, 0], status="borrador")]
        _, _, tabla = self.crear(filas)
        df = S._busqueda_hibrida(tabla, "vetiver", list(QV), 5,
                                 filtro_type="KO", filtro_status="activo")
        self.assertEqual(list(df["id"]), ["1"])

    def test_sin_coincidencias_devuelve_vacio(self):
        _, _, tabla = self.crear([_fila("1", "p1.md", "vetiver", [1, 0, 0], type_="DOC")])
        df = S._busqueda_hibrida(tabla, "vetiver", list(QV), 5, filtro_type="NADA")
        self.assertTrue(df.empty)

    def test_orden_por_hybrid_rank_decreciente(self):
        filas = [_fila("1", "p1.md", "vetiver", [1, 0, 0]),
                 _fila("2", "p2.md", "vetiver", [0.9, 0.1, 0]),
                 _fila("3", "p3.md", "vetiver", [0.8, 0.2, 0])]
        _, _, tabla = self.crear(filas)
        df = S._busqueda_hibrida(tabla, "vetiver", list(QV), 5)
        ranks = list(df["hybrid_rank"])
        self.assertEqual(ranks, sorted(ranks, reverse=True))

    def test_sin_indice_fts_no_rompe(self):
        # con_fts=False → la búsqueda FTS falla y se ignora (fts_ids = [])
        filas = [_fila("1", "p1.md", "vetiver", [1, 0, 0])]
        _, _, tabla = self.crear(filas, con_fts=False)
        df = S._busqueda_hibrida(tabla, "vetiver", list(QV), 5)
        self.assertEqual(list(df["id"]), ["1"])


class TestBuscarQS(BaseTemporal):
    """Query/Summary Indexing: umbral sim > 0.35 y paths únicos."""

    def test_sin_tablas_qs_devuelve_vacio(self):
        _, db, _ = self.crear([_fila("1", "p1.md", "vetiver", [1, 0, 0])])
        self.assertEqual(S._buscar_qs(db, list(QV)), [])

    def test_umbral_de_similitud_descarta_lejanos(self):
        _, db, _ = self.crear(
            [_fila("1", "p1.md", "vetiver", [1, 0, 0])],
            summaries=[{"path": "cerca.md", "vector": [1, 0, 0]},
                       {"path": "lejos.md", "vector": [0, 1, 0]}])
        # cerca.md → distancia 0 → sim 1.0 (pasa); lejos.md → sim 0.0 (fuera)
        self.assertEqual(S._buscar_qs(db, list(QV)), ["cerca.md"])

    def test_dedupe_entre_summaries_y_queries(self):
        _, db, _ = self.crear(
            [_fila("1", "p1.md", "vetiver", [1, 0, 0])],
            summaries=[{"path": "s.md", "vector": [1, 0, 0]}],
            consultas=[{"path": "s.md", "vector": [1, 0, 0]},
                       {"path": "q.md", "vector": [1, 0, 0]}])
        self.assertEqual(S._buscar_qs(db, list(QV)), ["s.md", "q.md"])


class TestQueryIndex(BaseTemporal):
    """Flujo completo con base temporal, encoder, reranker y telemetría mockeados."""

    def _filas_base(self):
        return [_fila("a1", "01-knowledge/a.md", "vetiver amaderado", [1, 0, 0]),
                _fila("a2", "01-knowledge/a.md", "vetiver amaderado (chunk 2)", [0.9, 0.1, 0]),
                _fila("b1", "01-knowledge/b.md", "citrico luminoso", [0, 1, 0], type_="DOC")]

    def test_dedupe_por_path(self):
        db_path, _, _ = self.crear(self._filas_base())
        salida, _ = self.ejecutar_query_index(db_path, top_k=5)
        self.assertEqual(salida.count("01-knowledge/a.md"), 1)

    def test_respeta_top_k(self):
        db_path, _, _ = self.crear(self._filas_base())
        salida, _ = self.ejecutar_query_index(db_path, top_k=1)
        self.assertEqual(len([l for l in salida.splitlines() if l.startswith("[")]), 1)

    def test_filtro_type_llega_a_la_busqueda(self):
        db_path, _, _ = self.crear(self._filas_base())
        salida, _ = self.ejecutar_query_index(db_path, top_k=5, filtro_type="DOC")
        self.assertIn("01-knowledge/b.md", salida)
        self.assertNotIn("01-knowledge/a.md", salida)

    def test_registra_telemetria_con_tiempos_por_paso(self):
        db_path, _, _ = self.crear(self._filas_base())
        _, log = self.ejecutar_query_index(db_path, top_k=2)
        self.assertEqual(log.call_count, 1)
        pasos = log.call_args.kwargs.get("pasos") or log.call_args.args[3]
        self.assertEqual(set(pasos), {"embed_s", "retrieve_s", "rerank_s", "total_s"})

    def test_extra_qs_marcado_y_anexado(self):
        # z.md existe en joko_notes (orthogonal → no entra en el top vectorial) y
        # aparece en joko_summaries → debe anexarse con _origen "qs".
        filas = [_fila("a1", "01-knowledge/a.md", "vetiver amaderado", [1, 0, 0]),
                 _fila("z1", "01-knowledge/z.md", "otra cosa", [0, 0, 1])]
        db_path, _, _ = self.crear(filas,
                                   summaries=[{"path": "01-knowledge/z.md",
                                               "vector": [1, 0, 0]}])
        salida, _ = self.ejecutar_query_index(db_path, top_k=1)
        self.assertIn("01-knowledge/z.md", salida)
        self.assertIn("| qs)", salida)

    def test_fallback_vectorial_si_falla_la_hibrida(self):
        db_path, _, _ = self.crear(self._filas_base())
        with mock.patch.object(S, "_busqueda_hibrida",
                               side_effect=RuntimeError("fts roto")):
            salida, _ = self.ejecutar_query_index(db_path, top_k=2)
        self.assertIn("usando solo vectorial", salida)
        self.assertIn("01-knowledge/a.md", salida)

    def test_cae_al_reranker_local_si_el_daemon_falla(self):
        db_path, _, _ = self.crear(self._filas_base())
        with mock.patch.object(S, "DB_PATH", db_path), \
                mock.patch.object(S, "_encode", lambda _t: list(QV)), \
                mock.patch.object(S, "_daemon_disponible", lambda: True), \
                mock.patch.object(S, "rerank_via_daemon",
                                  side_effect=RuntimeError("daemon caido")), \
                mock.patch.object(S, "get_reranker", lambda: _ReordenadorFalso()), \
                mock.patch.object(S, "_log_query", mock.Mock()):
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
                S.query_index("vetiver", top_k=2)
        self.assertIn("Daemon fallo", buf.getvalue())

    def test_sin_base_de_datos_aborta_con_systemexit(self):
        with mock.patch.object(S, "DB_PATH", Path(tempfile.gettempdir()) / "no_existe_xyz"):
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
                with self.assertRaises(SystemExit) as ctx:
                    S.query_index("vetiver")
        self.assertEqual(ctx.exception.code, 1)


class TestRerankViaDaemon(BaseTemporal):
    """Contrato HTTP del daemon del reranker (urllib mockeado, sin red real)."""

    def test_envia_query_y_textos_y_devuelve_scores(self):
        capturado = {}

        class _Respuesta:
            def read(self):
                return json.dumps({"scores": [0.9, 0.1]}).encode("utf-8")

            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

        def _urlopen(req, timeout=None):
            capturado["url"] = req.full_url
            capturado["body"] = json.loads(req.data.decode("utf-8"))
            return _Respuesta()

        with mock.patch.object(S.urllib.request, "urlopen", _urlopen):
            scores = S.rerank_via_daemon("vetiver", ["t1", "t2"])
        self.assertEqual(scores, [0.9, 0.1])
        self.assertTrue(capturado["url"].endswith("/rerank"))
        self.assertEqual(capturado["body"], {"query": "vetiver", "texts": ["t1", "t2"]})

    def test_propaga_el_error_del_daemon(self):
        with mock.patch.object(S.urllib.request, "urlopen",
                               side_effect=OSError("connection refused")):
            with self.assertRaises(OSError):
                S.rerank_via_daemon("vetiver", ["t1"])


class TestLogQuery(BaseTemporal):
    """La telemetría NUNCA debe romper la búsqueda (camino de error solamente:
    el camino feliz escribiría en /mnt/ssd_ia_datos y NO se testea aquí)."""

    def test_resultado_invalido_no_lanza(self):
        self.assertIsNone(S._log_query("q", 3, object()))

    def test_resultado_none_no_lanza(self):
        self.assertIsNone(S._log_query("q", 3, None))


if __name__ == "__main__":
    unittest.main(verbosity=2)
