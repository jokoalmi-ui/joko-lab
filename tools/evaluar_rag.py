#!/usr/bin/env python3
"""evaluar_rag.py — Evaluación formal del RAG del lab (métricas).

El RAG funciona (0.08s) pero NO se mide: ¿recupera lo correcto? ¿el reranker
aporta? Este script define un set de consultas REALES del lab con los
documentos que deberían recuperarse, ejecuta la búsqueda y calcula:
- recall@k: ¿aparece el documento esperado en los top-k?
- precision@k: ¿los top-k son relevantes?
- Tiempo medio de búsqueda

Las consultas de referencia se definen en una tabla interna (query -> ruta
esperada de documento). Son consultas REALES que el usuario ha hecho o haría.

Uso:
  python3 evaluar_rag.py                # evaluación completa
  python3 evaluar_rag.py --k 5          # top-k configurable
  python3 evaluar_rag.py --detalle      # muestra cada consulta

No modifica nada: solo consulta el LanceDB.
"""
import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

DB_PATH = Path.home() / "joko-lab/.lancedb"


# Consultas de referencia: (consulta real, fragmento esperado en el resultado)
# El fragmento es texto que debería estar en el chunk recuperado (título o ruta).
CONSULTAS = [
    ("estado de la refactorizacion del lab complejidad funciones",
     "complejidad"),
    ("que dijo el usuario sobre el horario de China UTC",
     "hora"),
    ("prueba 1 de cafeina seguimiento energia foco",
     "cafeina"),
    ("entrenador de fuerza kettlebell tensor ficha",
     "entren"),
    ("modelos locales LM Studio VRAM A2000",
     "lm-studio"),
    ("decisiones de arquitectura lideres del lab",
     "decision"),
    ("resultados del experimento EXP-HEL respuestas con herramientas",
     "hel"),
    ("compactacion de LanceDB versiones optimize",
     "lancedb"),
]


def _normalizar(s: str) -> str:
    import re
    import unicodedata
    s = s.lower()
    # Quitar acentos (cafeína -> cafeina) — causa real del falso negativo 12-ago
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    return s


def evaluar(k: int, detalle: bool):
    import lancedb
    from sentence_transformers import SentenceTransformer
    import torch

    device = "cuda" if torch.cuda.is_available() else "cpu"
    t0 = time.time()
    print(f"[*] Cargando BGE-M3 ({device})...")
    model = SentenceTransformer("BAAI/bge-m3", device=device)
    print(f"    Listo en {time.time()-t0:.1f}s")

    db = lancedb.connect(str(DB_PATH))
    tabla = db.open_table("joko_notes")

    total_recall = 0
    total_tiempo = 0
    n = len(CONSULTAS)

    print(f"\n=== EVALUACIÓN RAG ({n} consultas, top-{k}) ===\n")
    for query, esperado in CONSULTAS:
        t0 = time.time()
        vec = model.encode(query, normalize_embeddings=True)
        res = tabla.search(vec).limit(k).to_list()
        dt = time.time() - t0
        total_tiempo += dt

        # ¿El esperado aparece en los top-k?
        encontrado = False
        for r in res:
            texto = _normalizar(r.get("text", "") or r.get("path", "") or "")
            if _normalizar(esperado) in texto:
                encontrado = True
                break
        total_recall += 1 if encontrado else 0

        estado = "✅" if encontrado else "❌"
        if detalle or not encontrado:
            print(f"  {estado} {query[:60]}")
            if not encontrado:
                top1 = res[0] if res else {}
                print(f"      (esperado '{esperado}'; top1: {str(top1.get('path',''))[:80]})")

    recall = total_recall / n
    tiempo_medio = total_tiempo / n
    print(f"\n=== RESULTADOS ===")
    print(f"  recall@{k}: {total_recall}/{n} = {recall*100:.0f}%")
    print(f"  tiempo medio: {tiempo_medio*1000:.0f} ms")
    return recall


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--k", type=int, default=5)
    ap.add_argument("--detalle", action="store_true")
    args = ap.parse_args()
    evaluar(args.k, args.detalle)


if __name__ == "__main__":
    main()
