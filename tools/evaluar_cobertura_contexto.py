#!/usr/bin/env python3
"""evaluar_cobertura_contexto.py — cobertura del CONTEXTO del RAG (en tools/ desde 06-oct-2026).

Cobertura del CONTEXTO del RAG del lab. Complementa a evaluar_rag.py.

  evaluar_rag.py mide recall@k:   "¿esta el documento esperado en el top-k?"
  este instrumento mide:          "¿el contexto recuperado contiene TODO lo que
                                   hace falta para responder?"

Origen (ledger de canales, 19-sep / dailydoseofds_): la mayoria de fallos del RAG
NO son alucinacion fuera de corpus sino COBERTURA PARCIAL — el contexto cubre
parte de la respuesta y el modelo completa el resto por su cuenta. recall@k no lo
ve: basta 1 chunk con el termino buscado para darlo por bueno.

Por consulta (sin LLM; la criba se FIJO despues de medir, no a priori — RULE-015):
  hechos            datos que exige una respuesta correcta (lista de variantes).
  en_corpus         hechos que existen en ALGUN chunk del indice = TECHO real.
  cobertura@k       hechos presentes en los top-k recuperados.
  cobertura@top1    hechos presentes en el 1er chunk.
  cobertura@presup. hechos presentes en los chunks que CABEN en --presupuesto
                    (condicion REAL: el modelo no ve todo el top-k).

Cajas por consulta (no un booleano):
  CUBIERTO | PARCIAL | CUBIERTO_RECUPERABLE (lo que falta no esta en el corpus)
  | FALLO_RECUPERACION (existe en el corpus y no llega al contexto)
  | ABSTENCION_CORRECTA (el corpus no lo tiene: un 0 aqui es lo CORRECTO).
Un hecho ausente del corpus no se imputa 0 ni 1: va al cubo no_calculable.

CURA 06-oct-2026 -- lo que HABLA del banco no es corpus: un chunk que documenta este
instrumento o su criba (marca [BANCO], o citar "cobertura@", "huecos medidos", "hechos
en corpus", o cualquiera de los IDS DE CASO) se EXCLUYE del TECHO y del TOP-K. Motivo MEDIDO: la GUIA y el asiento de pendientes.md que DOCUMENTABAN el hueco
hacian que el probe leyera la frase "NO estan en el corpus" como prueba de que SI
estaban -> techo fantasma (2 casos pasaron de techo 0/1 a 2 sin que el corpus ganara ni
un documento util). El TECHO BRUTO (antes de filtrar) se sigue imprimiendo: la
contaminacion no se esconde, se muestra.

CRIBA (fijada 06-oct-2026 sobre el baseline de 13 casos, set de40e6bec98a2525):
  ratio por caso = cobertura@k / techo  (techo = hechos exigibles que EXISTEN en corpus)
    VERDE  ratio 1,00        sirve TODO lo exigible
    AMBAR  0,50 - 0,99       sirve parte: hueco real, no fallo
    ROJO   ratio < 0,50      sirve MENOS de la mitad
    EXENTO techo 0           no hay hecho exigible: la abstencion es lo correcto
  global: sobre los casos COMPARABLES (techo igual al del baseline): VERDES no baja de 5
  y ROJOS no sube de 2. Un caso cuyo techo se movio (el corpus gano o perdio hechos)
  queda NO COMPARABLE y se excluye del veredicto en vez de contaminarlo.
  Los cortes caen en HUECOS de la distribucion medida (0,000 x2 | 0,500 x4 |
  0,667 x1 | 1,000 x4), asi que el valor exacto no es sensible en este set.
  NO se fija criba sobre los ratios AGREGADOS: 1 hecho = 4,3% del denom. EN CORPUS.

Controles obligatorios en la misma pasada (si fallan, rc=2 y ninguna cifra vale):
  positivo: un fragmento literal del propio indice debe encontrarse con el matcher.
  negativo: cadenas INVENTADAS no deben existir (si existen, hay falsos positivos).

NO mide si el modelo USA el contexto (medicion aparte).
NO modifica nada: solo consulta LanceDB en lectura.

Uso:
  python3 evaluar_cobertura_contexto.py [--k 5] [--presupuesto 6000]
                                       [--detalle] [--json]
"""
import argparse
import hashlib
import json
import re
import sys
import time
import unicodedata
from collections import Counter
from pathlib import Path

DB_PATH = Path.home() / "joko-lab/.lancedb"
TABLA = "joko_notes"

# --- SET DE CASOS (borrador 2, 06-oct-2026) ----------------------------------
# hechos: una lista de VARIANTES por hecho; el hecho cuenta si aparece CUALQUIER
# variante (>=3 chars, para no cazar subcadenas accidentales).
# "esperada" = CAJA HIPOTESIS del autor: el instrumento la contrasta y marca el
# desvio. Es una hipotesis A FALSAR, no un resultado.
#   heredados = consultas del instrumento anterior (temas que el corpus cubre bien)
#   dirigidos = disenados para estrenar las cajas que el baseline dejo VACIAS
#               (FALLO_RECUPERACION, ABSTENCION_CORRECTA, CUBIERTO_RECUPERABLE)
CASOS = [
    # --- heredados (comparables con la pasada baseline de las 15:16) ---
    {"id": "modelos-locales", "query": "modelos locales LM Studio VRAM A2000",
     "hechos": [["lm studio", "lmstudio"], ["vram"], ["a2000"]]},
    {"id": "lancedb-compactacion", "query": "compactacion de LanceDB versiones optimize",
     "hechos": [["lancedb"], ["compact"], ["optimize"]]},
    {"id": "refactor-complejidad",
     "query": "estado de la refactorizacion del lab complejidad funciones",
     "hechos": [["refactor"], ["complejidad"]]},
    {"id": "cafeina-foco", "query": "prueba 1 de cafeina seguimiento energia foco",
     "hechos": [["cafeina"], ["energia"], ["foco"]]},
    {"id": "exp-hel",
     "query": "resultados del experimento EXP-HEL respuestas con herramientas",
     "hechos": [["exp-hel"], ["herramienta"]]},
    {"id": "rag-ruido-router", "esperada": "PARCIAL",
     "query": "configuracion del router de LangChain para agentes en produccion",
     "hechos": [["langchain"], ["router"]]},

    # --- dirigidos: estrenar ABSTENCION_CORRECTA (fuera del dominio del lab) ---
    {"id": "abst-impresora3d", "esperada": "ABSTENCION_CORRECTA",
     "query": "como calibro la primera capa de una impresora 3D Prusa MK4 con Klipper",
     "hechos": [["prusa"], ["klipper"]]},
    {"id": "abst-dato-vivo", "esperada": "ABSTENCION_CORRECTA",
     "query": "cuantos chunks tiene el indice RAG y cuanto ocupa en disco",
     # CURA 06-oct-2026: se quito el hecho ["espacio en disco"]. MEDIDO: es una frase
     # GENERICA que aparece en un espejo externo de skills sin relacion
     # (performing-memory-forensics-with-volatility3: "Espacio en disco suficiente")
     # -> falso positivo del matcher, no cobertura. Un dato VIVO (el valor de hoy) no
     # tiene documento que lo sostenga: su unico rastro eran docs que hablan del banco.
     # CURA 06-oct-2026 (2a): el hecho era el NUMERO DESNUDO ["45552"], que el matcher
     # ya no acepta (un numero no es verificable: casa con horas y con otros numeros).
     # Se declara VALOR+ETIQUETA. OJO: el valor CADUCA (el indice ya tiene 45591 chunks);
     # el techo sigue siendo 0 mientras ningun documento lo afirme.
     "hechos": [["45552 chunks", "45552 entradas"]]},

    # --- dirigido: documentado en corpus y RECUPERADO (reclasificado desde ROJO) ---
    # CURA 06-oct-2026 (2a). El caso era `fallo-detalle-reel`, esperaba FALLO_RECUPERACION
    # y declaraba DOS HECHOS FALSOS, MEDIDOS con sondas de solo lectura:
    #   - "corpus_abstention" -> 0 chunks en el corpus: el reel NO tiene rubrica de
    #     abstencion (mide answer relevance, groundedness, retrieval quality, tool-call).
    #     La palabra solo existia DENTRO de este instrumento.
    #   - "19 33" -> casaba con HORAS ("19:33") y con OTRO numero ("19.337"): el techo
    #     1/2 era fantasma, no cobertura. Por eso el matcher ya no admite hechos sin letra.
    #   - la consulta pedia algo inexistente ("rubrica de abstencion") y dejaba el documento
    #     real FUERA del top-20 (puesto 26); con la consulta de abajo sale 2o (d=0.319) con
    #     3 de sus chunks en el top-5 y sus hechos sostenidos por el PROPIO documento:
    #     NO habia fallo de recuperacion, era un caso mal disenado.
    # La caja FALLO_RECUPERACION queda SIN ESTRENAR a proposito: no se fabrica un fallo.
    # Para estrenarla hay que MEDIR un hueco real (candidato: `multi-rendimiento-local`,
    # que hoy espera CUBIERTO y sale PARCIAL).
    {"id": "cub-detalle-reel", "esperada": "CUBIERTO",
     "query": "como evaluar pipelines RAG con LLMs evals de retrieval y contexto",
     "hechos": [["gauravgoyalai"], ["groundedness"], ["retrieval quality"]]},
    # CURA 06-oct-2026: "esperada" era FALLO_RECUPERACION -> FALSADO al medir. El dato
    # de dosis vive en `coleccion.db` (uso_diario), NO en documentos, y por diseno no
    # debe estar. El "hecho en corpus" que lo hacia parecer un fallo de RECUPERACION
    # era DOCUMENTACION del propio hueco (GUIA + este asiento) = techo fantasma. Lo
    # correcto es que el RAG diga que no lo tiene (ABSTENCION_CORRECTA) y lo responda
    # el codigo contra la BD.
    {"id": "fallo-dato-bd-perfume", "esperada": "ABSTENCION_CORRECTA",
     "query": "que dosis de perfume se registro el 5 de octubre y con cual",
     "hechos": [["turathi"], ["4 sprays", "cuatro sprays"]]},

    # --- dirigido: estrenar CUBIERTO_RECUPERABLE (mitad en corpus, mitad no) ---
    # "klipper" esta medido como AUSENTE (caso abst-impresora3d: techo 0/2).
    {"id": "cub-recup-mixto", "esperada": "CUBIERTO_RECUPERABLE",
     "query": "compactacion de LanceDB y calibracion de impresora 3D Klipper",
     "hechos": [["lancedb"], ["compact"], ["klipper"]]},

    # --- dirigidos: multi-dato y distractor de sentido ---
    {"id": "multi-rendimiento-local", "esperada": "CUBIERTO",
     "query": "rendimiento medido del modelo local en tokens por segundo y comparacion con la nube",
     "hechos": [["tokens/s", "tok/s"], ["deepseek"]]},
    {"id": "distractor-modelo", "esperada": "PARCIAL",
     "query": "modelo de negocio y monetizacion del lab frente al modelo local",
     "hechos": [["monetiz"], ["negocio"]]},
]

# CONTROLES NEGATIVOS: cadenas inventadas que NO deben existir en el indice.
CONTROLES_NEGATIVOS = [
    "protocolo orbital de sillas",
    "modelo cuantico zx 9",
    "tostador hidroponico lunar",
]

# --- CRIBA (FIJADA 06-oct-2026) -----------------------------------------------
# Se fijo DESPUES de validar el instrumento (controles OK + 4 pasadas) y de mirar la
# distribucion real por caso del BASELINE (pasada 15:37:53 CEST del 06-oct, 13 casos,
# 45552 chunks, 23 hechos en corpus); ratio = cob@5/techo =
#   1,000 x5 (modelos-locales, lancedb-compactacion, refactor-complejidad, cafeina-foco,
#             cub-recup-mixto 2/2)
#   0,500 x4 (exp-hel, rag-ruido-router, multi-rendimiento-local, distractor-modelo)
#   0,000 x2 (abst-dato-vivo 0/1, fallo-detalle-reel 0/1)
#   EXENTOS 2 (techo 0: abst-impresora3d, fallo-dato-bd-perfume)
# = 5 VERDES + 4 AMBARES + 2 ROJOS + 2 EXENTOS = 13 casos: los conteos de abajo
# (verdes=5, rojos=2) son los de ESA pasada, no una meta elegida a mano.
# Los dos cortes caen en los HUECOS de esa distribucion: (0,500; 1,000) y (0,000; 0,500).
CRIBA_FIJADA = "06-oct-2026"
CRIBA_VERDE = 1.00
CRIBA_ROJO = 0.50
# RECTIFICACION 06-oct-2026 (2a): el caso `fallo-detalle-reel` (ROJO 0/1 de esa pasada)
# resulto ser un caso MAL DISENADO, no un fallo de recuperacion (medido: con su consulta
# el documento real no entra ni en el top-20; con la consulta correcta sale 2o y sus
# hechos los sostiene el propio documento). Pasa a `cub-detalle-reel` (esperada CUBIERTO)
# y el matcher deja de admitir hechos sin letra. Los cortes (1,00 / 0,50) y los limites
# globales (VERDES >= 5, ROJOS <= 2) NO se tocan. La distribucion de arriba es la de la
# pasada del 15:37:53 y NO se reescribe (regla de edicion correctiva: se anade).
# Baseline MEDIDO: pasada 15:37:53 CEST del 06-oct-2026 (set de40e6bec98a2525, 45552
# chunks, 23 hechos en corpus). El TECHO POR CASO entra en la criba a proposito: el
# indice se reindexa a diario y, cuando el corpus gana o pierde hechos, el techo de un
# caso cambia y su ratio se mueve SOLO. Un caso con techo distinto al del baseline no es
# comparable y se excluye del veredicto (se lista), en vez de contarlo como fallo.
CRIBA_BASELINE = {
    "chunks": 45552,
    "hechos_en_corpus": 23,
    "verdes": 5,
    "rojos": 2,
    "techo_por_caso": {
        "modelos-locales": 3, "lancedb-compactacion": 3, "refactor-complejidad": 2,
        "cafeina-foco": 3, "exp-hel": 2, "rag-ruido-router": 2, "abst-impresora3d": 0,
        "abst-dato-vivo": 1, "fallo-detalle-reel": 1, "fallo-dato-bd-perfume": 0,
        "cub-recup-mixto": 2, "multi-rendimiento-local": 2, "distractor-modelo": 2,
    },
}
CRIBA_GLOBAL_VERDES_MIN = CRIBA_BASELINE["verdes"]  # no bajar de 5 VERDE
CRIBA_GLOBAL_ROJOS_MAX = CRIBA_BASELINE["rojos"]    # no subir de 2 ROJO

# RECTIFICACION 06-oct-2026 (cura): los techos de `abst-dato-vivo` (baseline 1) y
# `fallo-dato-bd-perfume` (baseline 0 -> 2 en la tarde) se midieron con el probe
# CONTAMINADO, ANTES de esta cura: venian de documentacion del propio banco, no de
# corpus util. Con el probe curado sus techos son 0 (EXENTO) y los dos quedan NO
# COMPARABLES -- ahora no por el reindexado, sino por la cura. Los cortes (1,00 / 0,50)
# y los limites globales (VERDES >= 5, ROJOS <= 2) NO se tocan.

# --- LO QUE NO CUENTA COMO CORPUS (cura 06-oct-2026) --------------------------
BANCO_MARCA = "[BANCO]"
# CALIBRADO el 06-oct MIDIENDO que dispara cada pieza (cura_calibra.py). Se DESCARTARON
# por sobre-disparo: "top-5" (13 chunks en 9 ficheros, 5 legitimos de research/ y
# GUIA-APRENDIZAJE), "banco de pruebas" (2 ficheros legitimos), "en corpus" a secas
# (prosa comun) y "techo real". Los ids de caso son el discriminador mas fuerte: solo
# existen en la documentacion del banco.
BANCO_HABLA = re.compile(
    r"\[BANCO\]|cobertura@|evaluar_cobertura_contexto|huecos? medidos"
    r"|hechos en corpus"
    r"|abst-dato-vivo|abst-impresora3d|fallo-dato-bd-perfume"
    r"|fallo-detalle-reel|cub-detalle-reel"
    r"|cub-recup-mixto|rag-ruido-router|multi-rendimiento-local|distractor-modelo",
    re.I)


def _es_doc_banco(txt):
    """True si el chunk HABLA del banco de pruebas: no es corpus util."""
    return bool(BANCO_HABLA.search(txt or ""))


def _norm(s):
    s = (s or "").lower()
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9\s]", " ", s)


def _hecho_valido(v):
    """Un hecho debe contener al menos UNA LETRA: un numero desnudo no es verificable.
    MEDIDO 06-oct-2026: el hecho "19 33" casaba con HORAS ("19:33:36" -> "19 33 36") y
    con OTRO numero ("19.337" -> "19 337") y metia un techo fantasma (1/2) en el caso
    `fallo-detalle-reel`. Un hecho sin letra NO se acepta (fail-closed)."""
    return bool(re.search(r"[a-z]", _norm(v)))


def _casa(texto_norm, v):
    """Match con FRONTERA DE DIGITO: un numero no casa dentro de otro mayor.
    "19 33" NO casa con "19 337"; "45552" NO casa con "455522"."""
    n = _norm(v)
    if not n:
        return False
    for m in re.finditer(re.escape(n), texto_norm):
        antes = texto_norm[m.start() - 1] if m.start() else " "
        despues = texto_norm[m.end()] if m.end() < len(texto_norm) else " "
        if not antes.isdigit() and not despues.isdigit():
            return True
    return False


def _hechos_sin_letra(hechos):
    """Hechos INVALIDOS (numericos desnudos). Se listan: no deben pasar en silencio."""
    return [v[0] if v else "?" for v in hechos if not any(_hecho_valido(x) for x in v)]


def _presente(texto_norm, variantes):
    """True solo si alguna variante VALIDA casa. Un hecho sin letra cuenta como NO
    presente Y se reporta aparte (fail-closed: mejor un aviso que un techo fantasma)."""
    return any(len(v) >= 3 and _hecho_valido(v) and _casa(texto_norm, v) for v in variantes)


def _n_hechos(texto_norm, hechos):
    return sum(1 for v in hechos if _presente(texto_norm, v))


def _leer_corpus(tabla):
    """Barrido COMPLETO del indice (solo path/text, sin vectores)."""
    err1 = ""
    try:
        n = tabla.count_rows()
        filas = tabla.search().select(["path", "text"]).limit(n + 10).to_list()
        if filas:
            return filas, None
        err1 = "el barrido devolvio 0 filas"
    except Exception as e:
        err1 = "%s: %s" % (type(e).__name__, e)
    try:
        df = tabla.to_pandas()
        if "text" in df.columns:
            cols = [c for c in ("path", "text") if c in df.columns]
            return df[cols].to_dict("records"), None
    except Exception as e2:
        return None, "%s | fallback: %s: %s" % (err1, type(e2).__name__, e2)
    return None, err1


def evaluar(k, presupuesto, detalle, como_json):
    import lancedb
    import torch
    from sentence_transformers import SentenceTransformer

    out = (lambda *a: print(*a, file=sys.stderr)) if como_json else print

    device = "cuda" if torch.cuda.is_available() else "cpu"
    t0 = time.time()
    out("[*] Cargando BGE-M3 (%s)..." % device)
    model = SentenceTransformer("BAAI/bge-m3", device=device)
    out("    Listo en %.1fs" % (time.time() - t0))

    db = lancedb.connect(str(DB_PATH))
    tabla = db.open_table(TABLA)

    try:
        campos = sorted(tabla.schema.names)
    except Exception:
        campos = []
    if campos and "text" not in campos:
        out("INSTRUMENTO CIEGO: '%s' no tiene columna 'text' (campos: %s)" % (TABLA, campos))
        return 2

    filas, aviso = _leer_corpus(tabla)
    corpus_norm = None
    corpus_util, es_banco = [], []
    if filas is None:
        out("AVISO instrumento parcial: no pude barrer el corpus (%s)" % aviso)
        out("  -> en_corpus NO medido: FALLO_RECUPERACION y ABSTENCION_CORRECTA quedan NO_CALCULABLE")
    else:
        corpus_norm = [_norm(r.get("text", "")) for r in filas]
        es_banco = [_es_doc_banco(r.get("text") or "") for r in filas]
        corpus_util = [t for t, b in zip(corpus_norm, es_banco) if not b]
        out("[*] Corpus barrido: %d chunks | utiles %d | del banco (no cuentan) %d"
            % (len(filas), len(corpus_util), sum(es_banco)))
        if not corpus_util:
            out("AVISO: TODO el corpus es del banco de pruebas -> techo 0 en todos los casos")
        frag = (filas[0].get("text") or "")[:40]
        if not frag or _norm(frag) not in corpus_norm[0]:
            out("CONTROL POSITIVO FALLIDO: el matcher no encuentra un fragmento literal del indice -> instrumento roto")
            return 2
        falsos = [c for c in CONTROLES_NEGATIVOS if any(_norm(c) in t for t in corpus_norm)]
        if falsos:
            out("CONTROL NEGATIVO FALLIDO: %s -> el matcher tiene falsos positivos; ninguna cifra vale" % falsos)
            return 2
        out("[*] Controles OK (1 positivo, %d negativos)" % len(CONTROLES_NEGATIVOS))

    resumen = {
        "metrica": "cobertura_contexto",
        "tabla": TABLA,
        "k": k,
        "presupuesto_chars": presupuesto,
        "n_casos": len(CASOS),
        "set_sha256": hashlib.sha256(
            json.dumps(CASOS, ensure_ascii=False, sort_keys=True).encode("utf-8")
        ).hexdigest()[:16],
        "fecha": time.strftime("%Y-%m-%d %H:%M:%S"),
        "corpus_barrido": None if corpus_norm is None else len(corpus_norm),
        "corpus_util": None if corpus_norm is None else len(corpus_util),
        "chunks_banco": None if corpus_norm is None else sum(es_banco),
        "casos": [],
    }

    out("\n=== COBERTURA DEL CONTEXTO (%d casos, top-%d, presupuesto %d chars) ===\n"
        % (len(CASOS), k, presupuesto))
    for caso in CASOS:
        vec = model.encode(caso["query"], normalize_embeddings=True)
        # se piden k*3+5 y se descartan los del banco ANTES de cortar el top-k: un chunk
        # que documenta el banco no es evidencia de que el dato este en el corpus.
        res_todos = tabla.search(vec).limit(k * 3 + 5).to_list()
        n_banco_top = sum(1 for r in res_todos if _es_doc_banco(r.get("text") or ""))
        res = [r for r in res_todos if not _es_doc_banco(r.get("text") or "")][:k]
        textos = [r.get("text", "") or "" for r in res]
        rutas = [str(r.get("path", "") or "") for r in res]
        dists = [float(r.get("_distance", float("nan"))) for r in res]
        hechos = caso["hechos"]
        req = len(hechos)
        sin_letra = _hechos_sin_letra(hechos)
        esperada = caso.get("esperada")

        if corpus_norm is None:
            techo = techo_bruto = None
        else:
            techo_bruto = sum(1 for v in hechos
                              if any(_presente(t, v) for t in corpus_norm))
            techo = sum(1 for v in hechos
                        if any(_presente(t, v) for t in corpus_util))

        cob_k = _n_hechos(_norm("\n".join(textos)), hechos)
        cob_1 = _n_hechos(_norm(textos[0] if textos else ""), hechos)

        usados, acum = 0, []
        for t in textos:
            if acum and usados + len(t) > presupuesto:
                break
            acum.append(t)
            usados += len(t)
        cob_p = _n_hechos(_norm("\n".join(acum)), hechos)

        faltan = [
            (v[0] if v else "?") for v in hechos
            if not _presente(_norm("\n".join(textos)), v)
        ]

        # de DONDE sale cada hecho: auditable (corpus util vs descartado por banco)
        fuentes = {}
        if detalle and corpus_norm is not None:
            for v in hechos:
                util, desc = [], []
                for r, t, b in zip(filas, corpus_norm, es_banco):
                    if _presente(t, v):
                        (desc if b else util).append(str(r.get("path", "") or ""))
                fuentes[v[0]] = {"en_corpus": sorted(set(util))[:4],
                                 "descartado_banco": sorted(set(desc))[:4]}

        if cob_k == req:
            caja = "CUBIERTO"
        elif techo == 0:
            # el dato NO esta en el corpus: lo correcto es abstenerse. Va ANTES
            # de CUBIERTO_RECUPERABLE para que 0 == 0 no lo tape.
            caja = "ABSTENCION_CORRECTA"
        elif techo is not None and cob_k == techo and techo < req:
            caja = "CUBIERTO_RECUPERABLE"
        elif cob_k > 0:
            caja = "PARCIAL"
        elif techo is None:
            caja = "NO_CALCULABLE"
        else:
            caja = "FALLO_RECUPERACION"

        # --- criba por caso (fijada 06-oct-2026) ---
        if techo is None:
            ratio, criba = None, "NO_CALCULABLE"
        elif techo == 0:
            ratio, criba = None, "EXENTO"
        else:
            ratio = cob_k / techo
            criba = ("VERDE" if ratio >= CRIBA_VERDE
                     else ("ROJO" if ratio < CRIBA_ROJO else "AMBAR"))

        resumen["casos"].append({
            "id": caso["id"], "query": caso["query"], "caja": caja,
            "criba": criba, "ratio_cob": None if ratio is None else round(ratio, 3),
            "esperada": esperada,
            "dirigido_ok": None if not esperada else (caja == esperada),
            "hechos_req": req, "techo": techo, "techo_bruto": techo_bruto,
            "fuentes": fuentes, "banco_descartado_topk": n_banco_top,
            "cob_k": cob_k, "cob_top1": cob_1, "cob_presupuesto": cob_p,
            "faltan": faltan, "hechos_invalidos": sin_letra,
            "top1_path": rutas[0] if rutas else "",
            "chars_top_k": sum(len(t) for t in textos),
            "chunks_usados": len(acum), "chars_usados": usados,
            "dist_top1": None if not dists else round(dists[0], 4),
            "dist_media": None if not dists else round(sum(dists) / len(dists), 4),
        })

        if detalle or caja != "CUBIERTO":
            out("  %-21s | %-19s cob@%d %d/%d (techo %s) | cob@1 %d/%d | presup %d/%d"
                " [%d ch; usa %d/%d] | dist %.3f"
                % (caso["id"], caja, k, cob_k, req,
                   "n/d" if techo is None else "%d/%d" % (techo, req),
                   cob_1, req, cob_p, req,
                   sum(len(t) for t in textos), len(acum), usados,
                   dists[0] if dists else float("nan")))
            out("      criba: %s%s"
                % (criba, "" if ratio is None else " (ratio %.3f = %d/%d)" % (ratio, cob_k, techo)))
            if sin_letra:
                out("      HECHOS SIN LETRA (no verificables, no cuentan): %s"
                    % ", ".join(sin_letra))
            if esperada:
                out("      dirigido: esperaba %s -> %s"
                    % (esperada, "OK" if caja == esperada else "DESVIO"))
            if faltan:
                out("      faltan: %s" % ", ".join(faltan))
            if techo_bruto is not None and techo_bruto != techo:
                out("      techo: %s (bruto %s: %d hecho(s) del banco lo inflaban)"
                    % (techo, techo_bruto, techo_bruto - techo))
            if detalle:
                for f, src in fuentes.items():
                    out("      fuente %-20s corpus=%s | banco(descartado)=%s"
                        % (f, ", ".join(src["en_corpus"]) or "-",
                           ", ".join(src["descartado_banco"]) or "-"))
            if n_banco_top:
                out("      top-k: %d chunk(s) del banco descartados del contexto" % n_banco_top)
            if caja in ("FALLO_RECUPERACION", "PARCIAL") and rutas:
                out("      top1: %s" % rutas[0][:80])

    casos = resumen["casos"]
    cajas = Counter(c["caja"] for c in casos)
    req_total = sum(c["hechos_req"] for c in casos)
    cob_total = sum(c["cob_k"] for c in casos)
    p1_total = sum(c["cob_top1"] for c in casos)
    pp_total = sum(c["cob_presupuesto"] for c in casos)
    techo_total = sum(c["techo"] for c in casos if c["techo"] is not None)
    fuera = sum(c["hechos_req"] - (c["techo"] or 0) for c in casos if c["techo"] is not None)

    # --- criba global (fijada 06-oct-2026) ---
    # Solo se juzga lo COMPARABLE: un caso cuyo techo se movio respecto al baseline no
    # entra en el veredicto (se lista aparte).
    no_comp = [c["id"] for c in casos
               if c["techo"] is None
               or CRIBA_BASELINE["techo_por_caso"].get(c["id"]) != c["techo"]]
    comp = [c for c in casos if c["id"] not in no_comp]
    verdes = sum(1 for c in comp if c["criba"] == "VERDE")
    ambar = sum(1 for c in comp if c["criba"] == "AMBAR")
    rojos_ids = [c["id"] for c in comp if c["criba"] == "ROJO"]
    rojos = len(rojos_ids)
    exentos = sum(1 for c in comp if c["criba"] == "EXENTO")
    fallos = []
    if corpus_norm is None:
        veredicto = "NO CALCULABLE (sin barrido de corpus)"
    else:
        if verdes < CRIBA_GLOBAL_VERDES_MIN:
            fallos.append("VERDES %d < %d" % (verdes, CRIBA_GLOBAL_VERDES_MIN))
        if rojos > CRIBA_GLOBAL_ROJOS_MAX:
            fallos.append("ROJOS %d > %d (%s)"
                          % (rojos, CRIBA_GLOBAL_ROJOS_MAX, ", ".join(rojos_ids)))
        if verdes == 0:
            fallos.append("0 VERDE: instrumento ciego o corpus vacio")
        veredicto = ("OK (dentro del baseline)" if not fallos
                     else "FALLO: " + "; ".join(fallos))

    resumen["resumen"] = {
        "cajas": dict(cajas),
        "cobertura_pregunta@k": (cob_total / req_total) if req_total else None,
        "cobertura_recuperable@k": (cob_total / techo_total) if techo_total else None,
        "cobertura_top1": (p1_total / req_total) if req_total else None,
        "cobertura_presupuesto": (pp_total / req_total) if req_total else None,
        "hechos_req": req_total, "hechos_en_corpus": techo_total,
        "hechos_fuera_de_corpus": fuera,
        "casos_dirigidos": sum(1 for c in casos if c.get("esperada")),
        "dirigidos_ok": sum(1 for c in casos
                            if c.get("esperada") and c["caja"] == c["esperada"]),
        "criba": {
            "fijada": CRIBA_FIJADA,
            "caso_verde": CRIBA_VERDE, "caso_rojo": CRIBA_ROJO,
            "verdes": verdes, "ambar": ambar, "rojos": rojos, "exentos": exentos,
            "baseline": CRIBA_BASELINE,
            "corpus_actual_chunks": None if corpus_norm is None else len(corpus_norm),
            "verdes_minimo": CRIBA_GLOBAL_VERDES_MIN,
            "rojos_maximo": CRIBA_GLOBAL_ROJOS_MAX,
            "rojos_ids": rojos_ids,
            "no_comparables": no_comp,
            "veredicto": veredicto,
        },
    }

    resumen["veredicto"] = veredicto

    out("\n=== RESUMEN ===")
    for caja in ("CUBIERTO", "PARCIAL", "CUBIERTO_RECUPERABLE",
                 "FALLO_RECUPERACION", "ABSTENCION_CORRECTA", "NO_CALCULABLE"):
        out("  %-22s %d" % (caja, cajas.get(caja, 0)))
    sin_estrenar = [c for c in ("PARCIAL", "CUBIERTO_RECUPERABLE",
                                "FALLO_RECUPERACION", "ABSTENCION_CORRECTA")
                    if not cajas.get(c)]
    if sin_estrenar:
        out("  AVISO: cajas SIN NINGUN caso (no validadas en esta pasada): %s"
            % ", ".join(sin_estrenar))
    out("  cobertura@%d (denom. hechos requeridos): %s"
        % (k, "n/d" if not req_total else "%.2f (%d/%d)" % (cob_total / req_total, cob_total, req_total)))
    out("  cobertura@%d (denom. hechos EN CORPUS):  %s   <- techo real"
        % (k, "n/d" if not techo_total else "%.2f (%d/%d)" % (cob_total / techo_total, cob_total, techo_total)))
    out("  cobertura@top1 (denom. requeridos):      %s"
        % ("n/d" if not req_total else "%.2f (%d/%d)" % (p1_total / req_total, p1_total, req_total)))
    out("  cobertura@presupuesto(%d) (requeridos):  %s"
        % (presupuesto, "n/d" if not req_total else "%.2f (%d/%d)" % (pp_total / req_total, pp_total, req_total)))
    out("  hechos fuera de corpus (no_calculable):  %d de %d" % (fuera, req_total))
    dirigidos = [c for c in casos if c.get("esperada")]
    ok_dir = sum(1 for c in dirigidos if c["caja"] == c["esperada"])
    out("  casos dirigidos (caja esperada declarada): %d -> %d caen donde se disenaron"
        % (len(dirigidos), ok_dir))
    out("  CRIBA (fijada %s sobre el baseline; ratio = cob@%d / techo):"
        % (CRIBA_FIJADA, k))
    out("    VERDE (%.2f) %d | AMBAR (%.2f-%.2f) %d | ROJO (< %.2f) %d | EXENTO (techo 0) %d"
        % (CRIBA_VERDE, verdes, CRIBA_ROJO, CRIBA_VERDE, ambar, CRIBA_ROJO, rojos, exentos))
    out("    comparable: %d casos | NO comparable (techo movido desde el baseline): %s"
        % (len(comp), ", ".join(no_comp) or "ninguno"))
    out("    global: VERDES %d (minimo %d) | ROJOS %d (maximo %d): %s"
        % (verdes, CRIBA_GLOBAL_VERDES_MIN, rojos, CRIBA_GLOBAL_ROJOS_MAX,
           ", ".join(rojos_ids) or "ninguno"))
    out("    corpus: %s chunks (baseline %d) | utiles %s | del banco %s"
        " | hechos en corpus %d (baseline %d)"
        % ("n/d" if corpus_norm is None else len(corpus_norm), CRIBA_BASELINE["chunks"],
           "n/d" if corpus_norm is None else len(corpus_util),
           "n/d" if corpus_norm is None else sum(es_banco),
           techo_total, CRIBA_BASELINE["hechos_en_corpus"]))
    out("    VEREDICTO: %s" % veredicto)
    out("  NO hay criba sobre ratios AGREGADOS: 1 hecho = %.1f%% del denom. EN CORPUS"
        % (100.0 / techo_total if techo_total else 0.0))
    out("  NO medido aqui: si el modelo USA el contexto.")
    out("  set_sha256: %s" % resumen["set_sha256"])

    if como_json:
        print(json.dumps(resumen, ensure_ascii=False, indent=2))
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--k", type=int, default=5)
    ap.add_argument("--presupuesto", type=int, default=6000,
                    help="caracteres de contexto que se alimentan al modelo (parametro, no umbral)")
    ap.add_argument("--detalle", action="store_true")
    ap.add_argument("--json", action="store_true", help="salida JSON por stdout (humano a stderr)")
    args = ap.parse_args()
    return evaluar(args.k, args.presupuesto, args.detalle, args.json)


if __name__ == "__main__":
    sys.exit(main())
