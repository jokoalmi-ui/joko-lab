#!/usr/bin/env python3
"""
Tests de las funciones puras de tools/monitor_yt.py (auto-mejora 09-nov-2026).

Carencia que cubre: monitor_yt.py es la tool del cron de vigilancia de YouTube
(2 scripts + 1 cron) y llevaba 5 backups de ediciones manuales en 7 semanas
(.bak-20260925-jokioki, .bak-20261009-alta-notfound404, .bak-20261009-minviews,
.bak-20261017-ledger-outliers, .bak-20261026-eric-risco) SIN una sola prueba:
main() = 27 y cero red. Estas pruebas fijan la semantica de las piezas que
deciden QUE se avisa (parse del feed, umbral de outlier, filtro por título,
cierres del ledger) y del state (roundtrip atómico).

Todo con directorio temporal: NUNCA se toca el lab real ni la red.

Ejecución:
  cd ~/joko-lab && python3 -m unittest tests.test_monitor_yt -v
"""
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Optional

TOOLS_DIR = str(Path(__file__).resolve().parent.parent / "tools")
sys.path.insert(0, TOOLS_DIR)

import monitor_yt as my


def _entrada(vid: str = "v1", titulo: Optional[str] = "Un vídeo",
             fecha: Optional[str] = "2026-11-01T10:00:00+00:00",
             views: Optional[str] = "1234", con_video_id: bool = True):
    """Construye una <entry> de feed de YouTube con los campos dados."""
    partes = ["<entry>"]
    if con_video_id:
        partes.append(f"<yt:videoId>{vid}</yt:videoId>")
    if titulo is not None:
        partes.append(f"<title>{titulo}</title>")
    if fecha is not None:
        partes.append(f"<published>{fecha}</published>")
    if views is not None:
        partes.append(f'<media:group><media:statistics views="{views}"/></media:group>')
    partes.append("</entry>")
    return "".join(partes)


def _v(vid, views):
    return {"id": vid, "titulo": f"t-{vid}", "fecha": "2026-11-01T10:00:00+00:00",
            "views": views}


class TestParseFeed(unittest.TestCase):
    def test_dos_entradas_completas(self):
        xml = "<feed>" + _entrada("a", "Uno", views="10") + _entrada("b", "Dos", views="20") + "</feed>"
        r = my._parse_feed(xml)
        self.assertEqual([x["id"] for x in r], ["a", "b"])
        self.assertEqual(r[0]["titulo"], "Uno")
        self.assertEqual(r[0]["views"], 10)
        self.assertIsInstance(r[1]["views"], int)

    def test_sin_estadisticas_views_es_none(self):
        r = my._parse_feed("<feed>" + _entrada("a", views=None) + "</feed>")
        self.assertEqual(len(r), 1)
        self.assertIsNone(r[0]["views"])

    def test_sin_published_fecha_vacia(self):
        r = my._parse_feed("<feed>" + _entrada("a", fecha=None) + "</feed>")
        self.assertEqual(r[0]["fecha"], "")

    def test_entrada_sin_video_id_se_descarta(self):
        xml = "<feed>" + _entrada("a", con_video_id=False) + _entrada("b") + "</feed>"
        self.assertEqual([x["id"] for x in my._parse_feed(xml)], ["b"])

    def test_entrada_sin_titulo_se_descarta(self):
        xml = "<feed>" + _entrada("a", titulo=None) + "</feed>"
        self.assertEqual(my._parse_feed(xml), [])

    def test_titulo_multilinea_se_recorta(self):
        xml = "<feed>" + _entrada("a", titulo="  Linea uno\n  linea dos  ") + "</feed>"
        self.assertEqual(my._parse_feed(xml)[0]["titulo"], "Linea uno\n  linea dos")

    def test_feed_vacio(self):
        self.assertEqual(my._parse_feed(""), [])
        self.assertEqual(my._parse_feed("<feed></feed>"), [])


class TestDetectarOutliers(unittest.TestCase):
    def test_outlier_20x(self):
        videos = [_v("a", 1000), _v("b", 1000), _v("c", 1000), _v("d", 1000), _v("e", 20000)]
        r = my._detectar_outliers(videos, None)
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0]["id"], "e")
        self.assertEqual(r[0]["baseline"], 1000)
        self.assertEqual(r[0]["outlier_score"], 20.0)

    def test_todos_iguales_no_hay_outlier(self):
        videos = [_v(str(i), 1000) for i in range(5)]
        self.assertEqual(my._detectar_outliers(videos, None), [])

    def test_baseline_excluye_al_candidato(self):
        # otros = [100, 1000, 1000] -> mediana 1000; score 20.0
        videos = [_v("a", 100), _v("b", 1000), _v("c", 1000), _v("d", 20000)]
        r = my._detectar_outliers(videos, 50000)
        self.assertEqual(r[0]["baseline"], 1000)
        self.assertEqual(r[0]["outlier_score"], 20.0)
        self.assertEqual(r[0]["suscriptores"], 50000)

    def test_score_exactamente_10_entra(self):
        videos = [_v("a", 1000), _v("b", 1000), _v("c", 10000)]
        r = my._detectar_outliers(videos, None)
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0]["outlier_score"], 10.0)

    def test_score_9_9_no_entra(self):
        videos = [_v("a", 1000), _v("b", 1000), _v("c", 9900)]
        self.assertEqual(my._detectar_outliers(videos, None), [])

    def test_min_views_excluye_candidato(self):
        # score 50x pero por debajo de min_views=100
        videos = [_v("a", 1), _v("b", 1), _v("c", 1), _v("d", 50)]
        self.assertEqual(my._detectar_outliers(videos, None), [])
        self.assertEqual(len(my._detectar_outliers(videos, None, min_views=10)), 1)

    def test_views_none_no_es_candidato(self):
        videos = [_v("a", None), _v("b", 1000), _v("c", 1000), _v("d", 20000)]
        r = my._detectar_outliers(videos, None)
        self.assertEqual([x["id"] for x in r], ["d"])

    def test_lista_vacia(self):
        self.assertEqual(my._detectar_outliers([], None), [])

    def test_un_solo_video_no_tiene_baseline(self):
        self.assertEqual(my._detectar_outliers([_v("a", 99999)], None), [])

    def test_todos_views_cero_no_hay_outlier(self):
        videos = [_v("a", 0), _v("b", 0)]
        self.assertEqual(my._detectar_outliers(videos, None), [])


class TestSinAcentos(unittest.TestCase):
    def test_quita_tildes_y_baja(self):
        self.assertEqual(my._sin_acentos("Automatización"), "automatizacion")

    def test_diacriticos_varios(self):
        self.assertEqual(my._sin_acentos("ÁÉÍÓÚÑÜ"), "aeiounu")

    def test_texto_sin_acentos_igual(self):
        self.assertEqual(my._sin_acentos("MCP docker"), "mcp docker")


class TestPasaFiltro(unittest.TestCase):
    CID_FILTRADO = "UCCzFhEgRgG7wZhK5nUSg47g"  # Eric Risco
    CID_LIBRE = my.CANALES["Nichonauta"]

    def test_canal_sin_filtro_siempre_pasa(self):
        self.assertTrue(my._pasa_filtro(self.CID_LIBRE, "Recetas de cocina"))
        self.assertTrue(my._pasa_filtro(self.CID_LIBRE, ""))

    def test_titulo_fuera_de_tema_no_pasa(self):
        self.assertFalse(my._pasa_filtro(self.CID_FILTRADO, "Mi rutina de mañana"))

    def test_titulo_con_termino_pasa(self):
        self.assertTrue(my._pasa_filtro(self.CID_FILTRADO, "Agentes locales en Docker"))

    def test_termino_con_acento_en_el_titulo_pasa(self):
        self.assertTrue(my._pasa_filtro(self.CID_FILTRADO, "Automatización sin código"))

    def test_case_insensitive(self):
        self.assertTrue(my._pasa_filtro(self.CID_FILTRADO, "MEMORIA para agentes"))


class TestCargarCerrados(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.raiz = Path(self.tmp.name)
        (self.raiz / "tools").mkdir()
        (self.raiz / "04-operations" / "metrics").mkdir(parents=True)
        self.fich = self.raiz / "04-operations" / "metrics" / "outliers_cerrados.jsonl"
        self._orig_file = my.__file__
        my.__file__ = str(self.raiz / "tools" / "monitor_yt.py")

    def tearDown(self):
        my.__file__ = self._orig_file
        self.tmp.cleanup()

    def test_fichero_ausente_devuelve_vacio(self):
        self.assertEqual(my._cargar_cerrados(), {})

    def test_lee_ids_y_salta_lineas_rotas(self):
        self.fich.write_text(
            '{"id": "aaa", "motivo": "analizado"}\n'
            "NO ES JSON\n"
            "\n"
            '{"id": "bbb"}\n'
            '{"motivo": "sin id"}\n',
            encoding="utf-8")
        r = my._cargar_cerrados()
        self.assertEqual(sorted(r), ["aaa", "bbb"])
        self.assertEqual(r["aaa"]["motivo"], "analizado")

    def test_fichero_vacio(self):
        self.fich.write_text("", encoding="utf-8")
        self.assertEqual(my._cargar_cerrados(), {})


class TestState(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.ruta = Path(self.tmp.name) / "state" / "monitor_yt_state.json"
        self._orig = my.STATE_FILE
        my.STATE_FILE = self.ruta

    def tearDown(self):
        my.STATE_FILE = self._orig
        self.tmp.cleanup()

    def test_state_ausente_devuelve_dict_vacio(self):
        self.assertEqual(my._cargar_state(), {})

    def test_guardar_y_cargar_roundtrip(self):
        state = {"vid1": {"canal": "Canal", "titulo": "Título", "fecha": "2026-11-01T10:00:00+00:00"}}
        my._guardar_state(state)
        self.assertEqual(my._cargar_state(), state)

    def test_guardar_crea_directorio_y_no_deja_tmp(self):
        my._guardar_state({"a": {"canal": "C"}})
        self.assertTrue(self.ruta.exists())
        self.assertFalse(self.ruta.with_suffix(".json.tmp").exists())

    def test_json_corrupto_devuelve_dict_vacio(self):
        self.ruta.parent.mkdir(parents=True)
        self.ruta.write_text("{corrupto", encoding="utf-8")
        self.assertEqual(my._cargar_state(), {})


if __name__ == "__main__":
    unittest.main()
