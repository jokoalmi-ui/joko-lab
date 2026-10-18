#!/usr/bin/env python3
"""Experimento HyDE vs RAG clásico — Joko Lab (31-ago-2026).

Compara retrieval clásico (query directa -> embedding -> búsqueda)
contra HyDE (LLM genera respuesta hipotética -> embedding de ESA -> búsqueda)
usando las 8 consultas REALES del evaluador del lab (evaluar_rag.py).

Solo lectura: no toca el índice LanceDB, solo consulta.
"""
import os, sys, json, time, re, unicodedata, argparse

sys.path.insert(0, "/home/jokoalmi/joko-lab")
sys.path.insert(0, "/home/jokoalmi/joko-lab/tools")

import lancedb
import urllib.request

DB_PATH = "/home/jokoalmi/joko-lab/.lancedb"
EMB_URL = "http://localhost:1234/api/v0/embeddings"
CHAT_URL = "http://localhost:1234/api/v0/chat/completions"

# Consultas reales del evaluador (query, fragmento esperado)
CONSULTAS = [
    ("estado de la refactorizacion del lab complejidad funciones", "complejidad"),
    ("que dijo el usuario sobre el horario de China UTC", "hora"),
    ("prueba 1 de cafeina seguimiento energia foco", "cafeina"),
    ("entrenador de fuerza kettlebell tensor ficha", "entren"),
    ("modelos locales LM Studio VRAM A2000", "lm-studio"),
    ("decisiones de arquitectura lideres del lab", "decision"),
    ("resultados del experimento EXP-HEL respuestas con herramientas", "hel"),
    ("compactacion de LanceDB versiones optimize", "lancedb"),
]


def _normalizar(s: str) -> str:
    s = s.lower()
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    return s


def embed(texto: str) -> list:
    payload = {"model": "text-embedding-bge-m3", "input": [texto]}
    req = urllib.request.Request(
        EMB_URL,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        d = json.loads(r.read())
    return d["data"][0]["embedding"]


def hipotesis_hyde(query: str) -> str:
    """Genera la respuesta hipotética (documento ficticio) con GLM local."""
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
        CHAT_URL,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=240) as r:
        d = json.loads(r.read())
    return d["choices"][0]["message"]["content"].strip()


def buscar(emb: list, top_k: int = 5):
    db = lancedb.connect(DB_PATH)
    tbl = db.open_table("joko_notes")
    # Búsqueda vectorial por distancia coseno
    res = tbl.search(emb).metric("cosine").limit(top_k).to_list()
    return res


def evaluar(k: int = 5):
    print(f"=== EXPERIMENTO HyDE vs RAG CLÁSICO ({len(CONSULTAS)} consultas, top-{k}) ===\n")
    tabla = []
    for query, esperado in CONSULTAS:
        # --- RAG clásico ---
        t0 = time.time()
        emb_q = embed(query)
        res_q = buscar(emb_q, k)
        t_clasico = time.time() - t0
        hit_clasico = any(_normalizar(esperado) in _normalizar(str(r.get("text", ""))) or
                          _normalizar(esperado) in _normalizar(str(r.get("path", ""))) or
                          _normalizar(esperado) in _normalizar(str(r.get("title", "")))
                          for r in res_q)

        # --- HyDE ---
        try:
            t0 = time.time()
            doc_hip = hipotesis_hyde(query)
            t_gen = time.time() - t0
            emb_h = embed(doc_hip)
            res_h = buscar(emb_h, k)
            t_hyde = time.time() - t0
            hit_hyde = any(_normalizar(esperado) in _normalizar(str(r.get("text", ""))) or
                           _normalizar(esperado) in _normalizar(str(r.get("path", ""))) or
                           _normalizar(esperado) in _normalizar(str(r.get("title", "")))
                           for r in res_h)
        except Exception as e:
            doc_hip = f"ERROR: {e}"
            res_h = []
            hit_hyde = False
            t_hyde = t_clasico
            t_gen = 0

        estado = "✅" if (hit_clasico or hit_hyde) else "❌"
        cambio = "=" if hit_clasico == hit_hyde else ("↑" if hit_hyde and not hit_clasico else "↓")
        tabla.append((query, esperado, hit_clasico, hit_hyde, t_clasico, t_hyde, doc_hip[:150], cambio, estado))
        print(f"{estado} {query[:55]}")
        print(f"    clásico: {'HIT' if hit_clasico else 'miss'} ({t_clasico:.1f}s) | HyDE: {'HIT' if hit_hyde else 'miss'} ({t_hyde:.1f}s) {cambio}")
        if doc_hip.startswith("ERROR"):
            print(f"    ⚠ hipótesis: {doc_hip[:80]}")
        else:
            print(f"    hipótesis: {doc_hip[:100]}...")

    # Resumen
    n_clasico = sum(1 for t in tabla if t[2])
    n_hyde = sum(1 for t in tabla if t[3])
    n_mejora = sum(1 for t in tabla if t[3] and not t[2])
    n_empeora = sum(1 for t in tabla if t[2] and not t[3])
    print(f"\n=== RESUMEN (top-{k}) ===")
    print(f"  RAG clásico: {n_clasico}/{len(CONSULTAS)} recall")
    print(f"  HyDE:        {n_hyde}/{len(CONSULTAS)} recall")
    print(f"  Mejoras (miss→HIT): {n_mejora} | Empeora (HIT→miss): {n_empeora} | Iguales: {len(CONSULTAS)-n_mejora-n_empeora}")
    print(f"  Latencia media clásico: {sum(t[4] for t in tabla)/len(tabla):.1f}s | HyDE: {sum(t[5] for t in tabla)/len(tabla):.1f}s")
    return tabla


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", type=int, default=5)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    tabla = evaluar(args.k)
    if args.json:
        print(json.dumps([{"query": t[0], "esperado": t[1], "clasico": t[2], "hyde": t[3],
                           "t_clasico": round(t[4],1), "t_hyde": round(t[5],1),
                           "hipotesis": t[6], "cambio": t[7]} for t in tabla], ensure_ascii=False, indent=2))
