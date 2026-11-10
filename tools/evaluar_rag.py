#!/usr/bin/env python3
"""evaluar_rag.py — Evaluación formal del RAG del lab (métricas).

El RAG funciona rápido, pero ¿recupera lo correcto? Este script ejecuta consultas
reales contra LanceDB y calcula recall@k, MRR@k y foco (nº de ficheros distintos
en el top-k, indicador de ruido).

GROUND TRUTH (08-nov-2026): el acierto se decide por la RUTA del documento
objetivo, no por un fragmento de texto. La versión anterior usaba substrings
genéricos ("hora", "decision", "hel", "entren") que aparecen en cualquier
fichero: medido el 08-11, el control negativo "receta de paella" daba acierto
en 11/11 consultas. Un banco así no mide nada (RULE-015).

Los controles negativos (objetivo = None) no se evalúan por ruta: se reporta la
distancia del top-1 para comprobar que el espacio vectorial separa lo ajeno.

NOTA sobre precision@k (10-nov-2026): NO se implementa. El banco v2 tiene UN
documento objetivo por consulta, así que la precisión estaría topada en 1/k
(20% con k=5) por construcción, no por ruido real. MRR y foco miden lo que
precision@k pretendía medir sin ese techo artificial.

Uso:
  python3 evaluar_rag.py                # evaluación completa (k=5)
  python3 evaluar_rag.py --k 10         # top-k configurable
  python3 evaluar_rag.py --detalle      # muestra cada consulta
  python3 evaluar_rag.py --json         # salida legible por máquina

No modifica nada: solo consulta el LanceDB.
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

LAB = Path.home() / "joko-lab"
DB_PATH = LAB / ".lancedb"

# Candidatos que se re-ordenan de forma exacta antes de cortar el top-k.
# El 10-nov-2026 se midió que el índice IvfHnswFlat con ef por defecto pierde
# el documento correcto en k=5 (5/6 aciertos) y lo devuelve primero en k=20:
# es imprecisión del ANN, no del documento. Con refine=20: 6/6 y MRR 0.542->0.708.
REFINE = 20


# (consulta real, ruta del documento objetivo relativa al lab, nota)
# objetivo None = control negativo (no debería recuperarse nada relevante).
CONSULTAS = [
    ("por que la GPU desaparece cuando el portatil se suspende",
     "research/diagnostico-gpu-suspend-resume-20260823.md", "gap lexico"),
    ("resultados del experimento EXP-HEL respuestas con herramientas",
     "01-knowledge/experiments/EXP-HEL-001-via-c-baseline.md", "tecnica"),
    ("que es HyDE y como expande las consultas de busqueda",
     "research/experimento-hyde-20260831.md", "tecnica"),
    ("seguridad de la IA mesa redonda tabletop Sophia",
     "research/tabletop-seguridad-ia-20260821.md", "nombre propio"),
    ("formato TOON frente a JSON eficiencia de tokens",
     "research/analisis-toon-formato-llm-20261016.md", "siglas"),
    ("Bonsai 2 27B de Nichonauta en local",
     "research/analisis-nichonauta-bonsai2-27b-2026-09-19.md", "nombre propio"),
    ("hasta que hora hay que esperar antes de decir la hora exacta", None, "control"),
    ("receta de paella valenciana para ocho personas", None, "control"),
]


def _ruta_abs(p: str) -> str:
    if not p:
        return ""
    p = p if os.path.isabs(p) else str(LAB / p)
    return os.path.normpath(p)


def evaluar(k: int, detalle: bool, como_json: bool = False):
    import lancedb
    import torch
    from sentence_transformers import SentenceTransformer

    device = "cuda" if torch.cuda.is_available() else "cpu"
    t0 = time.time()
    if not como_json:
        print(f"[*] Cargando BGE-M3 ({device})...")
    model = SentenceTransformer("BAAI/bge-m3", device=device)
    if not como_json:
        print(f"    Listo en {time.time()-t0:.1f}s")

    tabla = lancedb.connect(str(DB_PATH)).open_table("joko_notes")

    filas = []
    for query, objetivo, nota in CONSULTAS:
        t0 = time.time()
        vec = model.encode(query, normalize_embeddings=True)
        res = tabla.search(vec).refine_factor(REFINE).limit(k).to_list()
        dt = time.time() - t0

        paths = [_ruta_abs(r.get("path") or "") for r in res]
        foco_k = len(set(paths))
        dist_top1 = res[0].get("_distance") if res else None
        if objetivo:
            abs_obj = _ruta_abs(objetivo)
            encontrado = abs_obj in paths
            posicion = (paths.index(abs_obj) + 1) if encontrado else None
        else:
            encontrado, posicion = None, None

        fila = dict(query=query, objetivo=objetivo, nota=nota,
                    encontrado=encontrado, posicion=posicion, foco=foco_k,
                    tiempo=round(dt, 3),
                    dist_top1=(round(float(dist_top1), 4) if dist_top1 is not None else None),
                    top1=(paths[0].replace(str(LAB) + "/", "") if paths else ""))
        filas.append(fila)

        if detalle or encontrado is False:
            estado = "OK " if encontrado else ("N/A" if encontrado is None else "FALLA")
            if not como_json:
                print(f"  [{estado}] {query[:58]}")
                if encontrado is False:
                    print(f"        esperado: {objetivo}")
                    print(f"        top1:     {fila['top1']}")

    pos = [f for f in filas if f["objetivo"]]
    neg = [f for f in filas if not f["objetivo"]]
    aciertos = sum(1 for f in pos if f["encontrado"])
    recall = aciertos / len(pos) if pos else 0.0
    mrr = (sum(1.0 / f["posicion"] for f in pos if f["posicion"]) / len(pos)) if pos else 0.0
    foco_medio = (sum(f["foco"] for f in filas) / len(filas)) if filas else 0.0
    t_medio = sum(f["tiempo"] for f in filas) / len(filas)
    d_pos = [f["dist_top1"] for f in pos if f["dist_top1"] is not None]
    d_neg = [f["dist_top1"] for f in neg if f["dist_top1"] is not None]

    resumen = dict(
        banco="v2-ruta", consultas=len(filas), con_objetivo=len(pos),
        recall_at_k=round(recall, 3), aciertos=aciertos, k=k,
        mrr_at_k=round(mrr, 3), foco_medio=round(foco_medio, 2),
        tiempo_medio_ms=round(t_medio * 1000),
        dist_top1_media_objetivo=(round(sum(d_pos) / len(d_pos), 4) if d_pos else None),
        dist_top1_media_control=(round(sum(d_neg) / len(d_neg), 4) if d_neg else None),
        fallos=[f["query"] for f in pos if not f["encontrado"]],
    )

    if como_json:
        print(json.dumps(dict(resumen=resumen, detalle=filas), ensure_ascii=False, indent=1))
    else:
        print("\n=== RESULTADOS ===")
        print(f"  recall@{k}: {aciertos}/{len(pos)} = {recall*100:.0f}%  (banco v2, ground truth = ruta)")
        print(f"  MRR@{k}: {mrr:.3f}  |  foco medio: {foco_medio:.2f} ficheros distintos por top-{k}")
        print(f"  tiempo medio: {t_medio*1000:.0f} ms")
        if resumen["dist_top1_media_objetivo"] is not None:
            print(f"  distancia top-1 media: objetivo {resumen['dist_top1_media_objetivo']}"
                  f" | control {resumen['dist_top1_media_control']}")
        if resumen["fallos"]:
            print(f"  fallos: {len(resumen['fallos'])}")
    return recall


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--k", type=int, default=5)
    ap.add_argument("--detalle", action="store_true")
    ap.add_argument("--json", action="store_true", dest="como_json")
    args = ap.parse_args()
    evaluar(args.k, args.detalle, args.como_json)


if __name__ == "__main__":
    main()
