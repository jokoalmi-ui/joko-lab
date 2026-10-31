#!/usr/bin/env python3
"""search.py - Busqueda semantica con re-ranking (BGE-M3 via LM Studio API o local)."""
import os, sys, argparse, json, lancedb, importlib.util
from pathlib import Path
import urllib.request

# Lazy import (fix 2-ago-2026): sentence_transformers/torch pesan ~7-8s al
# importar. Solo se importan cuando NO hay daemon (fallback local). El flujo
# normal (daemon reranker + LM Studio API) solo necesita urllib + lancedb.
# _lazy_st() devuelve (SentenceTransformer, CrossEncoder) bajo demanda.

VAULT_PATH = Path(os.path.expanduser("~/joko-lab"))
DB_PATH = VAULT_PATH / ".lancedb"
COLLECTION_NAME = "joko_notes"
MODEL_NAME = "BAAI/bge-m3"
# bge-reranker-m3 es un modelo GATED en HuggingFace: requiere HF_TOKEN.
# Repo_id REAL (verificado 2-ago-2026): BAAI/bge-reranker-v2-m3
# (BAAI/bge-reranker-m3 NO existe -> 404 Repository Not Found).
# Si no hay token, se usa el cross-encoder publico como fallback.
RERANKER_NAME = "BAAI/bge-reranker-v2-m3"
RERANKER_FALLBACK = "cross-encoder/ms-marco-MiniLM-L-6-v2"
DEVICE = "cpu"
# Fix 05-ago-2026 (latencia reranker): 10 pares -> 6s en CPU (bge-reranker-v2-m3,
# coste ~0.6s/par). El rerank solo refina el top del retrieve; con 5 pares el
# top-3 resultante es IDENTICO (verificado 05-ago: [0.738,0.413,0.799] igual) y
# la latencia baja a ~3s. Los textos completos se siguen devolviendo en results.
TOP_K_RETRIEVE = int(os.environ.get("JOKO_RAG_RETRIEVE", "5"))

# --- Anti-hub y expansion de consulta (19-oct-2026) -------------------------
# Medido con un banco de 20 consultas sobre este mismo buscador:
#   recall@5 global 9/20 (45%): consultas con vocabulario del documento 9/10,
#   consultas coloquiales con otro vocabulario 0/10. El gold SI esta indexado
#   (con una frase literal del propio documento sale en top-3 en 10/10).
#   Un solo fichero (04-operations/backlogs/2026-07-31-backlog.md, 889 KB)
#   aparecia en 13 de los 20 top-10: masa estadistica, no relevancia.
# El retrieve trae TOP_K_RETRIEVE=5 candidatos, asi que un hub ocupa huecos
# reales y desplaza al documento correcto.
HUB_KB = 120          # por encima de esto un fichero compite por tamano
HUB_CHUNKS = 3        # chunks del mismo path en el candidate set
HUB_PENALTY_MAX = 0.45

# Expansion coloquial -> tecnico (0 tokens, 0 modelos): el usuario pregunta
# "se me queda sin memoria" y la nota habla de "swap"/"VRAM".
EXPANSION_QUERY = [
    (("sin memoria", "queda sin memoria", "usa el disco", "usar el disco", "se queda sin memoria"),
     "swap memoria virtual VRAM RAM offload memoria insuficiente"),
    (("no estan en mis apuntes", "no esta en mis apuntes", "se inventa", "invente", "inventa datos"),
     "alucinacion grounding fidelidad verificacion de fuentes"),
    (("corrige respuestas", "modelo que corrige", "corrige", "evaluar respuestas"),
     "llm-as-judge evaluador juez rubrica evaluacion"),
    (("va mas rapido", "mas rapido", "por internet", "en la nube", "de pago"),
     "latencia tokens por segundo rendimiento benchmark API cloud coste"),
    (("sacar el texto", "pdf escaneado", "escanear", "escaneado"),
     "OCR extraccion de texto pymupdf tesseract docling"),
    (("cortar", "trozos", "trocear"),
     "chunking chunk fragmentacion split"),
    (("grafica", "tarjeta grafica", "cuanta grafica"),
     "GPU VRAM CUDA memoria de video"),
    (("por la noche", "trabaje solo", "solo sin que yo", "sin que yo este"),
     "cron programado automatizacion batch nocturno"),
    (("no recuerdo", "como llame", "buscador de apuntes"),
     "busqueda semantica recuperacion embeddings RAG indice"),
]


def _norm_txt(s: str) -> str:
    """Minusculas y sin acentos, para comparar claves coloquiales."""
    import unicodedata
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def expandir_query(q: str) -> tuple:
    """Devuelve (query_expandida, terminos_anadidos). Sin match, (q, [])."""
    ql = _norm_txt(q)
    extra = []
    for claves, terminos in EXPANSION_QUERY:
        if any(k in ql for k in claves):
            extra.extend(terminos.split())
    vistos, limpio = set(), []
    for t in extra:
        if t.lower() not in vistos:
            vistos.add(t.lower()); limpio.append(t)
    if not limpio:
        return q, []
    return q + " " + " ".join(limpio), limpio


def penalizacion_hub(path: str, n_chunks: int) -> float:
    """Penaliza documentos-hub por tamano y por masa de chunks."""
    import math
    p = 0.0
    if n_chunks > HUB_CHUNKS:
        p += 0.06 * math.log2(n_chunks / HUB_CHUNKS)
    kb = 0.0
    for cand in (os.path.join(str(VAULT_PATH), path), path):
        try:
            kb = os.path.getsize(cand) / 1024.0
            break
        except OSError:
            continue
    if kb > HUB_KB:
        p += 0.10 * math.log2(kb / HUB_KB)
    return round(min(p, HUB_PENALTY_MAX), 3)

# Asegurar que joko-lab/ está en sys.path para importar tools.lmstudio_embeddings
if str(VAULT_PATH) not in sys.path:
    sys.path.insert(0, str(VAULT_PATH))

# Carga de modulos hermanos por RUTA, no por paquete (fix 19-oct-2026, medido).
# Si PYTHONPATH incluye ~/.hermes/hermes-agent, `from tools.X import ...` resuelve
# al paquete tools/ del agente: es paquete REGULAR (tiene __init__.py) y gana al
# tools/ del repo, que es namespace (sin __init__.py), aunque el del repo vaya
# antes en sys.path. El ImportError resultante lo tragaba _check_api() y el
# buscador degradaba al encoder local sin decir nada -> 0 resultados por rc=1.
# Cargando el fichero del repo por ruta, el resultado no depende del entorno.
_TOOLS_DIR = Path(__file__).resolve().parent


def _cargar_modulo_local(nombre: str):
    """Carga tools/<nombre>.py del propio repo y lo cachea en sys.modules."""
    cachado = sys.modules.get(f"joko_tools_{nombre}")
    if cachado is not None:
        return cachado
    fichero = _TOOLS_DIR / f"{nombre}.py"
    spec = importlib.util.spec_from_file_location(f"joko_tools_{nombre}", fichero)
    if spec is None or spec.loader is None:
        raise ImportError(f"search.py: no se pudo cargar {fichero} (fail-closed)")
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[f"joko_tools_{nombre}"] = modulo
    spec.loader.exec_module(modulo)
    return modulo


def _avisar_tools_ajeno():
    """Avisa si el paquete `tools` importable no es el del repo (entorno sucio)."""
    ajeno = sys.modules.get("tools")
    if ajeno is None:
        return None
    rutas = [Path(p).resolve() for p in getattr(ajeno, "__path__", [])]
    if _TOOLS_DIR not in rutas:
        print(f"  [aviso] paquete 'tools' importado desde {rutas or '?'} (no es el del repo); "
              f"se usan modulos del repo por ruta", file=sys.stderr)
        return ajeno
    return None

# Cache
_encoder = None
_reranker = None
_use_api = None


def _lazy_st():
    """Importa sentence_transformers solo cuando hace falta (fallback local)."""
    from sentence_transformers import SentenceTransformer
    from sentence_transformers.cross_encoder import CrossEncoder
    return SentenceTransformer, CrossEncoder

# Daemon del reranker (fix cuello de botella 2-ago-2026): cargar el modelo
# una vez en un proceso persistente evita ~11s de import+CUDA por subprocess.
RERANKER_DAEMON_URL = "http://127.0.0.1:8765"
_use_daemon = None


def _daemon_disponible() -> bool:
    """Comprueba si el daemon del reranker responde (timeout corto)."""
    global _use_daemon
    if _use_daemon is None:
        try:
            urllib.request.urlopen(RERANKER_DAEMON_URL + "/health", timeout=1)
            _use_daemon = True
        except Exception:
            _use_daemon = False
    return _use_daemon


def rerank_via_daemon(query: str, texts: list) -> list:
    """Re-ordena via daemon persistente. Lanza excepcion si falla."""
    payload = json.dumps({"query": query, "texts": texts}).encode("utf-8")
    req = urllib.request.Request(
        RERANKER_DAEMON_URL + "/rerank",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["scores"]


def _check_api():
    """Verifica si LM Studio API de embeddings está disponible.

    Fail-closed (19-oct-2026): antes un `except Exception` silencioso convertia
    cualquier fallo de importacion en "API no disponible" y el buscador degradaba
    al encoder local sin avisar. Si esto falla ahora, se ve la traza.
    """
    global _use_api
    if _use_api is None:
        _avisar_tools_ajeno()
        _use_api = _cargar_modulo_local("lmstudio_embeddings").is_available()
    return _use_api


def get_encoder():
    """Obtiene encoder: LM Studio API si disponible, BGE-M3 local como fallback."""
    global _encoder
    if _encoder is None:
        if _check_api():
            print("  [encoder] Usando LM Studio API (text-embedding-bge-m3)...", file=sys.stderr)
            _encoder = "api"  # marcador, el encode real va por API
        else:
            print("  [encoder] LM Studio no disponible, cargando BGE-M3 local...", file=sys.stderr)
            SentenceTransformer, _ = _lazy_st()
            import torch
            _encoder = SentenceTransformer(MODEL_NAME, device=DEVICE)
            if DEVICE == "cuda":
                _encoder.half()
    return _encoder


def _encode(text):
    """Codifica texto usando API o modelo local."""
    encoder = get_encoder()
    if encoder == "api":
        encode = _cargar_modulo_local("lmstudio_embeddings").encode
        import numpy as np
        v = encode(text)
        # Normalizar como lo haría SentenceTransformer
        v = v / np.linalg.norm(v)
        return v.flatten().tolist()
    else:
        return encoder.encode(text, normalize_embeddings=True).tolist()


def _intentar_reranker(nombre: str) -> object:
    """Carga un reranker intentando GPU primero; cae a CPU si CUDA falla (OOM)."""
    _, CrossEncoder = _lazy_st()
    try:
        import torch
        if torch.cuda.is_available():
            try:
                print(f"  [reranker] Cargando {nombre} en CUDA...", file=sys.stderr)
                return CrossEncoder(nombre, device="cuda")
            except Exception as e:
                print(f"  [reranker] CUDA fallo ({e}), cayo a CPU...", file=sys.stderr)
        return CrossEncoder(nombre, device="cpu")
    except Exception as e:
        print(f"  [reranker] No se pudo cargar {nombre}: {e}", file=sys.stderr)
        raise


def get_reranker():
    global _reranker
    if _reranker is None:
        # bge-reranker-m3 requiere HF_TOKEN (modelo gated). Sin token, fallback publico.
        if os.environ.get("HF_TOKEN") or os.path.exists(os.path.expanduser("~/.cache/huggingface/token")):
            try:
                _reranker = _intentar_reranker(RERANKER_NAME)
                return _reranker
            except Exception:
                print(f"  [reranker] Usando fallback {RERANKER_FALLBACK}...", file=sys.stderr)
                _reranker = _intentar_reranker(RERANKER_FALLBACK)
        else:
            print(f"  [reranker] Sin HF_TOKEN, usando {RERANKER_FALLBACK} (publico)...", file=sys.stderr)
            _reranker = _intentar_reranker(RERANKER_FALLBACK)
    return _reranker


def _construir_where(filtro_type: str, filtro_status: str) -> str:
    """Construye la cláusula where de LanceDB a partir de los filtros."""
    if filtro_type and filtro_status:
        return f"type = '{filtro_type}' AND status = '{filtro_status}'"
    if filtro_type:
        return f"type = '{filtro_type}'"
    if filtro_status:
        return f"status = '{filtro_status}'"
    return ""


def _calcular_rrf(fts_ids: list, vec_ids: list, K: int = 60) -> dict:
    """Fusión por rango recíproco: suma 1/(K + rango) por aparición."""
    scores = {}
    for rank, doc_id in enumerate(fts_ids):
        scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (K + rank + 1)
    for rank, doc_id in enumerate(vec_ids):
        scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (K + rank + 1)
    return scores


def _busqueda_hibrida(table, query_text: str, qv, limit: int,
                      filtro_type: str = None, filtro_status: str = None) -> "pd.DataFrame":
    """Búsqueda híbrida FTS + vectorial con fusión RRF (05-ago-2026).

    LanceDB soporta ambos índices (FTS Spanish + IVF_HNSW cosine). Los scores
    FTS (BM25) y vectoriales (distancia) NO son comparables entre sí, así que
    se fusionan por RANGO (Reciprocal Rank Fusion): cada lista ordena sus
    candidatos y el rango combinado decide. Devuelve DataFrame con columna
    `hybrid_rank` además de las columnas originales.

    filtro_type/filtro_status: pre-filtro por frontmatter (columnas type/status)
    ANTES de la búsqueda, usando la cláusula where de LanceDB.
    """
    import numpy as np
    K = 60  # constante RRF (estándar)

    # Pre-filtro opcional por frontmatter (P3 ampliado, 05-ago-2026)
    where_sql = _construir_where(filtro_type, filtro_status)

    def _apply_filter(query_builder):
        if where_sql:
            return query_builder.where(where_sql)
        return query_builder

    # 1. Búsqueda FTS (BM25) — si el índice existe
    try:
        fts = _apply_filter(table.search(query_text, query_type="fts")).limit(limit).to_pandas()
        fts_ids = list(fts["id"])
    except Exception:
        fts_ids = []

    # 2. Búsqueda vectorial
    vec = _apply_filter(table.search(qv)).limit(limit).to_pandas()
    vec_ids = list(vec["id"])

    # 3. RRF: sumar 1/(K + rango) por cada aparición
    scores_rrf = _calcular_rrf(fts_ids, vec_ids, K)

    # 4. Unir con los datos completos (sin pylance: to_pandas + filtro por id)
    df_todos = table.to_pandas().drop(columns=["vector"], errors="ignore")
    orden = sorted(scores_rrf.keys(), key=lambda d: scores_rrf[d], reverse=True)
    df_todos["hybrid_rank"] = [scores_rrf.get(i, 0.0) for i in df_todos["id"]]
    df_todos["_origen"] = ["fts+vec" if i in fts_ids and i in vec_ids
                           else ("fts" if i in fts_ids else "vec") for i in df_todos["id"]]
    df_todos = df_todos[df_todos["id"].isin(orden)].copy()
    df_todos["_orden_rrf"] = df_todos["id"].map({d: i for i, d in enumerate(orden)})
    df_todos = df_todos.sort_values("_orden_rrf").head(limit).reset_index(drop=True)
    return df_todos


def _buscar_qs(db, qv, top_k: int = 3) -> list:
    """Query/Summary Indexing (A1): busca en joko_summaries + joko_queries y
    devuelve los paths de los documentos recuperados por resumen/preguntas.

    Devuelve lista de paths ÚNICOS (ordenados por mejor similitud). Si las
    tablas no existen, devuelve [] (no rompe la búsqueda normal).
    """
    import numpy as np
    paths = []
    for tname in ("joko_summaries", "joko_queries"):
        if tname not in db.table_names():
            continue
        try:
            t = db.open_table(tname)
            df = t.search(qv).limit(top_k).to_pandas()
            for _, r in df.iterrows():
                d = r.get("_distance")
                sim = 1 - d if d is not None else 0.0
                if sim > 0.35 and r["path"] not in paths:
                    paths.append(r["path"])
        except Exception:
            continue
    return paths


def query_index(query_text: str, top_k: int = 3,
                filtro_type: str = None, filtro_status: str = None,
                aplicar_hub: bool = True, aplicar_expand: bool = True,
                retrieve: int = None, debug: bool = False):
    import time as _time
    _t0 = _time.time()
    if not DB_PATH.exists():
        print("ERROR: Base de datos no encontrada. Ejecuta indexer.py primero.", file=sys.stderr)
        sys.exit(1)

    retrieve = retrieve or TOP_K_RETRIEVE
    query_efectiva, terminos = expandir_query(query_text) if aplicar_expand else (query_text, [])
    if debug:
        print(f"  [expand] retrieve={retrieve} hub={aplicar_hub} "
              f"terminos={terminos or 'ninguno'}", file=sys.stderr)
    qv = _encode(query_efectiva)
    _t_embed = _time.time()

    db = lancedb.connect(str(DB_PATH))
    table = db.open_table(COLLECTION_NAME)

    # Búsqueda híbrida: FTS + vectorial + RRF (P3, 05-ago-2026)
    try:
        results = _busqueda_hibrida(table, query_efectiva, qv, retrieve,
                                    filtro_type=filtro_type, filtro_status=filtro_status)
    except Exception as e:
        # Fallback: solo vectorial (si falla FTS por cualquier motivo)
        print(f"  [hybrid] FTS fallo ({e}), usando solo vectorial...", file=sys.stderr)
        results = table.search(qv).limit(retrieve).to_pandas()
    _t_retrieve = _time.time()

    if results.empty:
        print("Sin resultados.")
        return

    # Re-ranking: daemon persistente primero, carga local como fallback
    pairs = [[query_efectiva, row["text"]] for _, row in results.iterrows()]
    texts = [row["text"] for _, row in results.iterrows()]
    if _daemon_disponible():
        try:
            scores = rerank_via_daemon(query_efectiva, texts)
        except Exception as e:
            print(f"  [reranker] Daemon fallo ({e}), usando carga local...", file=sys.stderr)
            reranker = get_reranker()
            scores = reranker.predict(pairs)
    else:
        reranker = get_reranker()
        scores = reranker.predict(pairs)
    _t_rerank = _time.time()

    results["rerank_score"] = scores
    results = results.sort_values("rerank_score", ascending=False)

    # Anti-hub (19-oct-2026): un fichero enorme o con muchos chunks gana huecos
    # por masa, no por relevancia. La penalizacion se resta al rerank ANTES del
    # dedupe por path (todos los chunks del mismo path reciben lo mismo).
    results["hub_penalty"] = 0.0
    if aplicar_hub:
        n_chunks = results["path"].value_counts().to_dict()
        results["hub_penalty"] = [penalizacion_hub(p, n_chunks.get(p, 1))
                                  for p in results["path"]]
        results["rerank_score"] = results["rerank_score"] - results["hub_penalty"]
        results = results.sort_values("rerank_score", ascending=False)

    # Peso de fuente (31-oct-2026): las tarjetas de sesion (type: session) son
    # evidencia secundaria, no norma. Factor MULTIPLICATIVO para que no copen los
    # huecos cuando existe documento canonico (RULE/DEC/nota). Medido sin factor:
    # 11/30 slots del top-3. Desactivable: JOKO_RAG_PESO_SESION=1.0.
    results["peso_fuente"] = 1.0
    peso_sesion = float(os.environ.get("JOKO_RAG_PESO_SESION", "0.90"))
    if peso_sesion != 1.0 and "type" in results.columns:
        es_sesion = results["type"].astype(str).str.strip().str.lower() == "session"
        if es_sesion.any():
            results.loc[es_sesion, "rerank_score"] = (
                results.loc[es_sesion, "rerank_score"] * peso_sesion)
            results.loc[es_sesion, "peso_fuente"] = peso_sesion
            results = results.sort_values("rerank_score", ascending=False)
    # Dedupe por path (07-ago): LanceDB guarda chunks; el mismo documento puede
    # entrar varias veces con scores distintos (verificado: ecosistema-gobernanza
    # x2, EXP-20260729-004 x2 en una misma consulta). Se mantiene el mejor y se
    # toman los top_k ÚNICOS.
    results = results.drop_duplicates(subset=["path"], keep="first").head(top_k)

    # Query/Summary Indexing (A1, 20-ago-2026): si existen las tablas
    # joko_summaries + joko_queries, recuperar DOCUMENTOS adicionales por
    # resumen/preguntas posibles (la consulta de estado "¿qué decidimos sobre
    # X?" matchea mejor el resumen que el chunk). Los paths nuevos se añaden
    # marcados como _origen="qs" (sin tocar el ranking híbrido ni el rerank).
    paths_vistos = set(results["path"])
    try:
        import pandas as pd  # import local (el módulo arranca sin pandas)
        extras = _buscar_qs(db, qv, top_k=3)
        for p in extras:
            if p in paths_vistos:
                continue
            # Traer el mejor chunk de joko_notes para ese documento
            chunk = table.search(qv).where(f"path = '{p}'").limit(1).to_pandas()
            if chunk.empty:
                continue
            row = chunk.iloc[0].copy()
            row["_origen"] = "qs"
            results = pd.concat([results, row.to_frame().T], ignore_index=True)
            paths_vistos.add(p)
    except Exception as e:
        print(f"  [qs] Tablas QS no disponibles ({e}) — buscando solo joko_notes.", file=sys.stderr)

    for idx, (_, row) in enumerate(results.iterrows()):
        sim = row.get("_distance", 0)
        if sim is not None:
            sim = 1 - sim
        else:
            sim = 0
        try:
            sim = float(sim)
            sim = None if sim != sim else sim   # NaN (fila qs sin _distance)
        except (TypeError, ValueError):
            sim = None
        origen = row.get("_origen", "vec")
        pen = row.get("hub_penalty", 0.0)
        try:
            pen = float(pen) if pen is not None else 0.0
        except (TypeError, ValueError):
            pen = 0.0
        pen = 0.0 if pen != pen else pen
        try:
            rr = float(row["rerank_score"])
            rr = None if rr != rr else rr
        except (TypeError, ValueError, KeyError):
            rr = None
        pen_txt = f" | hub: -{pen:.2f}" if pen > 0 else ""
        peso = row.get("peso_fuente", 1.0)
        try:
            peso = float(peso)
        except (TypeError, ValueError):
            peso = 1.0
        if peso < 1.0:
            pen_txt += f" | sesion x{peso:.2f}"
        sim_txt = f"{sim:.3f}" if sim is not None else "-"
        rr_txt = f"{rr:.3f}" if rr is not None else "-"
        print(f"[{idx+1}] {row['path']}  (cos: {sim_txt} | rerank: {rr_txt} | {origen}{pen_txt})")
        if row.get("tags"):
            print(f"    tags: {row['tags']}")
        text = row.get("text", "")
        print(f"    {text[:200].strip()}{'...' if len(text)>200 else ''}")
        print()

    print(f"--- Recuperados: {len(results)} de {TOP_K_RETRIEVE} ---", file=sys.stderr)

    # Telemetria F1+F4: registro de consulta con tiempos por paso
    pasos = {
        "embed_s": round(_t_embed - _t0, 3),
        "retrieve_s": round(_t_retrieve - _t_embed, 3),
        "rerank_s": round(_t_rerank - _t_retrieve, 3),
        "total_s": round(_time.time() - _t0, 3),
    }
    _log_query(query_text, top_k, results, pasos=pasos)


def _log_query(query_text, top_k, results, pasos=None):
    """Registro de consulta RAG en rag-query-ledger.jsonl (telemetria F1 + F4).
    Incluye tiempos por paso si se proporcionan. Nunca interrumpe el flujo."""
    try:
        from datetime import datetime as _dt
        paths = [str(row.get("path", "")) for _, row in results.iterrows()]
        entry = {
            "timestamp": _dt.now().isoformat(),
            "query": query_text,
            "top_k": top_k,
            "n_recuperados": len(results),
            "paths": paths,
        }
        if pasos:
            entry["tiempos"] = pasos
        log_path = os.path.expanduser("/mnt/ssd_ia_datos/lab-state/rag-query-ledger.jsonl")
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
        pass  # telemetria nunca debe romper la busqueda


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Busqueda semantica con re-ranking en Joko Lab")
    parser.add_argument("--query", "-q", required=True, help="Texto de busqueda")
    parser.add_argument("--top_k", "-k", type=int, default=3, help="Resultados a devolver")
    parser.add_argument("--no-rerank", action="store_true", help="Saltar re-ranking")
    parser.add_argument("--type", default=None, help="Filtrar por type del frontmatter (ej: RULE, DEC, experimento)")
    parser.add_argument("--status", default=None, help="Filtrar por status (ej: activo, completado, superseded)")
    parser.add_argument("--no-hub", action="store_true", help="Desactivar la penalizacion de documentos-hub")
    parser.add_argument("--no-expand", action="store_true", help="Desactivar la expansion coloquial->tecnico de la consulta")
    parser.add_argument("--retrieve", type=int, default=None, help="Candidatos a recuperar antes del rerank (defecto 5, env JOKO_RAG_RETRIEVE)")
    parser.add_argument("--debug", action="store_true", help="Mostrar expansion y parametros efectivos")
    args = parser.parse_args()
    query_index(args.query, args.top_k, filtro_type=args.type, filtro_status=args.status,
                aplicar_hub=not args.no_hub, aplicar_expand=not args.no_expand,
                retrieve=args.retrieve, debug=args.debug)
