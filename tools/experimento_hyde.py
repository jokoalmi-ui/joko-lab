#!/usr/bin/env python3
"""Experimento HyDE vs RAG clásico — Joko Lab (31-ago-2026).

Compara retrieval clásico (query directa -> embedding -> búsqueda)
contra HyDE (LLM genera respuesta hipotética -> embedding de ESA -> búsqueda).

GROUND TRUTH (08-nov-2026): acierto por RUTA del documento objetivo, igual que
evaluar_rag.py. El banco anterior usaba fragmentos genéricos ("hora", "hel",
"decision") que aparecen en cualquier fichero, así que las cifras de HyDE
publicadas con él no son comparables.

Embeddings: por defecto con sentence-transformers local (BAAI/bge-m3, GPU),
sin depender de LM Studio. Con --emb api usa /api/v0/embeddings de LM Studio.
HyDE necesita un LLM generador (LM Studio): con --solo-clasico no se usa.

Solo lectura: no toca el índice LanceDB, solo consulta.
"""
import argparse
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, "/home/jokoalmi/joko-lab")
sys.path.insert(0, "/home/jokoalmi/joko-lab/tools")

import lancedb

LAB = Path.home() / "joko-lab"
DB_PATH = str(LAB / ".lancedb")
EMB_URL = "http://localhost:1234/api/v0/embeddings"
CHAT_URL = "http://localhost:1234/api/v0/chat/completions"

# (consulta real, ruta del documento objetivo relativa al lab) — banco v2
CONSULTAS = [
    ("por que la GPU desaparece cuando el portatil se suspende",
     "research/diagnostico-gpu-suspend-resume-20260823.md"),
    ("resultados del experimento EXP-HEL respuestas con herramientas",
     "01-knowledge/experiments/EXP-HEL-001-via-c-baseline.md"),
    ("que es HyDE y como expande las consultas de busqueda",
     "research/experimento-hyde-20260831.md"),
    ("seguridad de la IA mesa redonda tabletop Sophia",
     "research/tabletop-seguridad-ia-20260821.md"),
    ("formato TOON frente a JSON eficiencia de tokens",
     "research/analisis-toon-formato-llm-20261016.md"),
    ("Bonsai 2 27B de Nichonauta en local",
     "research/analisis-nichonauta-bonsai2-27b-2026-09-19.md"),
]

_modelo_st = None


def _ruta_abs(p: str) -> str:
    if not p:
        return ""
    p = p if os.path.isabs(p) else str(LAB / p)
    return os.path.normpath(p)


def coincide(res: list, objetivo: str) -> bool:
    """¿La ruta objetivo está entre los resultados?"""
    obj = _ruta_abs(objetivo)
    return any(_ruta_abs(r.get("path") or "") == obj for r in res)


def embed(texto: str, via: str = "local") -> list:
    global _modelo_st
    if via == "api":
        payload = {"model": "text-embedding-bge-m3", "input": [texto]}
        req = urllib.request.Request(
            EMB_URL, data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=60) as r:
            d = json.loads(r.read())
        return d["data"][0]["embedding"]
    if _modelo_st is None:
        import torch
        from sentence_transformers import SentenceTransformer
        dev = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"[*] Cargando BGE-M3 local ({dev})...")
        _modelo_st = SentenceTransformer("BAAI/bge-m3", device=dev)
    return _modelo_st.encode(texto, normalize_embeddings=True).tolist()


def hipotesis_hyde(query: str) -> str:
    """Genera la respuesta hipotética (documento ficticio) con el LLM local."""
    prompt = (
        "Eres un asistente que escribe un DOCUMENTO FICTICIO que respondería "
        "a la pregunta del usuario, como si ese documento existiera en un corpus "
        "de documentación técnica de un laboratorio de IA local (Joko Lab: "
        "scripts, herramientas Python, RAG, modelos locales, decisiones, "
        "experimentos). Escribe 2-3 frases factuales en español, estilo apunte "
        "técnico, con el detalle que tendría el documento real. NO respondas a "
        "la pregunta directamente: escribe el documento hipotético.\n\n"
        f"Pregunta: {query}\n\nDocumento hipotético:"
    )
    payload = {
        "model": "glm-4.6v-flash",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": 4000,
    }
    req = urllib.request.Request(
        CHAT_URL, data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=240) as r:
        d = json.loads(r.read())
    return d["choices"][0]["message"]["content"].strip()


def buscar(emb: list, top_k: int = 5):
    db = lancedb.connect(DB_PATH)
    tbl = db.open_table("joko_notes")
    return tbl.search(emb).metric("cosine").limit(top_k).to_list()


def evaluar(k: int = 5, via: str = "local", solo_clasico: bool = False):
    print(f"=== EXPERIMENTO HyDE vs RAG CLÁSICO ({len(CONSULTAS)} consultas, top-{k}, "
          f"embeddings={via}) ===\n")
    tabla = []
    for query, objetivo in CONSULTAS:
        # --- RAG clásico ---
        t0 = time.time()
        res_q = buscar(embed(query, via), k)
        t_clasico = time.time() - t0
        hit_clasico = coincide(res_q, objetivo)

        # --- HyDE ---
        if solo_clasico:
            doc_hip, res_h, hit_hyde, t_hyde = "(omitido: --solo-clasico)", [], None, 0.0
        else:
            try:
                t0 = time.time()
                doc_hip = hipotesis_hyde(query)
                res_h = buscar(embed(doc_hip, via), k)
                t_hyde = time.time() - t0
                hit_hyde = coincide(res_h, objetivo)
            except Exception as e:
                doc_hip = f"ERROR: {e}"
                res_h, hit_hyde, t_hyde = [], False, t_clasico

        cambio = "=" if hit_hyde == hit_clasico else ("↑" if hit_hyde and not hit_clasico else "↓")
        if hit_hyde is None:
            cambio = "-"
        tabla.append((query, objetivo, hit_clasico, hit_hyde, t_clasico, t_hyde, doc_hip[:150], cambio))
        print(f"{'OK ' if hit_clasico else 'MISS'} {query[:55]}")
        if solo_clasico:
            print(f"    clásico: {'HIT' if hit_clasico else 'miss'} ({t_clasico:.1f}s) | HyDE: omitido")
        else:
            print(f"    clásico: {'HIT' if hit_clasico else 'miss'} ({t_clasico:.1f}s) | "
                  f"HyDE: {'HIT' if hit_hyde else 'miss'} ({t_hyde:.1f}s) {cambio}")
            print(f"    hipótesis: {doc_hip[:100]}...")

    n = len(tabla)
    n_clasico = sum(1 for t in tabla if t[2])
    print(f"\n=== RESUMEN (top-{k}) ===")
    print(f"  RAG clásico: {n_clasico}/{n} recall (ground truth = ruta)")
    print(f"  Latencia media clásico: {sum(t[4] for t in tabla)/n:.1f}s")
    if not solo_clasico:
        n_hyde = sum(1 for t in tabla if t[3])
        n_mejora = sum(1 for t in tabla if t[3] and not t[2])
        n_empeora = sum(1 for t in tabla if t[2] and not t[3])
        print(f"  HyDE:        {n_hyde}/{n} recall")
        print(f"  Mejoras (miss→HIT): {n_mejora} | Empeora (HIT→miss): {n_empeora} | "
              f"Iguales: {n - n_mejora - n_empeora}")
        print(f"  Latencia media HyDE: {sum(t[5] for t in tabla)/n:.1f}s")
    return tabla


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", type=int, default=5)
    parser.add_argument("--emb", choices=["local", "api"], default="local")
    parser.add_argument("--solo-clasico", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    tabla = evaluar(args.k, args.emb, args.solo_clasico)
    if args.json:
        print(json.dumps([{"query": t[0], "objetivo": t[1], "clasico": t[2], "hyde": t[3],
                           "t_clasico": round(t[4], 2), "t_hyde": round(t[5], 2),
                           "hipotesis": t[6], "cambio": t[7]} for t in tabla],
                         ensure_ascii=False, indent=2))
