#!/usr/bin/env python3
"""
rag_telemetry.py — Observabilidad del pipeline RAG (F4).

Registra por consulta: tiempos por paso, tokens, resultados.
Formato: JSONL append en 04-operations/metrics/rag_telemetry.jsonl

Pasos medidos:
  embed:     query → vector (BGE-M3 vía LM Studio API)
  retrieve:  búsqueda en LanceDB
  rerank:    CrossEncoder (daemon CPU)
  total:     tiempo total de la búsqueda

Uso:
  from rag_telemetry import log_consulta
  log_consulta(query=..., pasos={...}, tokens=..., resultados=...)
"""
import json, os, time
from datetime import datetime
from pathlib import Path

LOG_PATH = Path(os.path.expanduser("~/joko-lab/04-operations/metrics/rag_telemetry.jsonl"))
# Ledger real donde search.py escribe (telemetria F1+F4)
LEDGER_REAL = Path("/mnt/ssd_ia_datos/lab-state/rag-query-ledger.jsonl")


def log_consulta(query: str, pasos: dict, tokens_estimados: int = 0,
                 n_resultados: int = 0, origen: str = "cli"):
    """Registra una consulta RAG con sus métricas por paso."""
    entrada = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "origen": origen,
        "query": query[:200],           # truncar queries largas
        "tokens_estimados": tokens_estimados,
        "n_resultados": n_resultados,
        **pasos,                        # {embed_s: x, retrieve_s: y, rerank_s: z, total_s: t}
    }
    try:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_PATH, "a") as f:
            f.write(json.dumps(entrada, ensure_ascii=False) + "\n")
    except Exception as e:
        # La telemetría nunca debe romper la búsqueda
        print(f"[telemetry] Error escribiendo log: {e}", file=os.sys.stderr)
    return entrada


def _leer_entradas(fuente) -> list:
    """Lee el JSONL del ledger y devuelve las entradas parseables."""
    entradas = []
    with open(fuente) as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entradas.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return entradas


def _calcular_medias(ultimas: list) -> dict:
    """Media de tiempos por campo en la ventana."""
    medias = {}
    for campo in ("embed_s", "retrieve_s", "rerank_s", "total_s"):
        valores = [e.get("tiempos", {}).get(campo, 0) for e in ultimas if "tiempos" in e]
        valores = [v for v in valores if v]
        if valores:
            medias[campo] = round(sum(valores) / len(valores), 3)
    return medias


def resumen_ultimas(n: int = 10) -> dict:
    """Resumen de las últimas N consultas (para informes/dashboard).
    Lee el ledger real de search.py (rag-query-ledger.jsonl)."""
    fuente = LEDGER_REAL if LEDGER_REAL.exists() else LOG_PATH
    if not fuente.exists():
        return {"total": 0}
    entradas = _leer_entradas(fuente)
    ultimas = entradas[-n:]
    if not ultimas:
        return {"total": len(entradas)}
    return {
        "total_consultas": len(entradas),
        "ventana": len(ultimas),
        "medias_seg": _calcular_medias(ultimas),
        "fuente": str(fuente),
    }
