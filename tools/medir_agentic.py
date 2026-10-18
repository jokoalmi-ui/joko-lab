#!/usr/bin/env python3
"""
medir_agentic.py — Medición Fase 3 del Agentic RAG Loop.

Compara el RAG CLÁSICO (1 búsqueda, sin reformulación) contra el AGENTIC
(loop con reformulación, máx 3 iteraciones) sobre TODOS los items del banco.

Qué mide (determinista, sin LLM):
  - cobertura_ok por item: ¿el contexto recuperado contiene lo que exige el
    item (keywords/fuentes)?
  - nº de búsquedas por modo (1 en clásico; 1-3 en agentic)
  - tiempo total por modo
  - items que el agentic RESUELVE y el clásico NO (la mejora real)
  - items donde el agentic NO aporta (ambos OK o ambos incompletos)

Los "aciertos" de esta medición son del RETRIEVAL (cobertura), no de un LLM:
el loop no genera tokens de LLM en su parte determinista. Para medir aciertos
del LLM sobre el contexto recuperado se usaría run_eval.py --use-lab aparte.

Uso:
  ~/.venv/hermes-rag/bin/python3 ~/joko-lab/tools/medir_agentic.py [--json]

Solo lectura: no modifica banco, índices ni KOs. search.py registra telemetría
en rag-query-ledger.jsonl (comportamiento normal). Escribe el historial de la
medición en verification/history-agentic.jsonl.
"""

import argparse
import datetime
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path.home() / "joko-lab" / "tools"))

import yaml

from agentic_loop import ejecutar_loop

BANCO_DEFAULT = Path.home() / "joko-lab" / "verification" / "bank.yaml"
HISTORY = Path.home() / "joko-lab" / "verification" / "history-agentic.jsonl"


def cargar_banco(ruta) -> list:
    with open(ruta, "r", encoding="utf-8") as f:
        banco = yaml.safe_load(f)
    for item in banco:
        for campo in ("id", "pregunta", "tipo", "respuesta_esperada", "fuente"):
            if campo not in item:
                raise ValueError(f"Item sin campo obligatorio '{campo}': {item}")
    return banco


def medir_modo(item: dict, max_iter: int, top_k: int) -> dict:
    """Ejecuta el loop con un límite de iteraciones y mide tiempo + búsquedas."""
    t0 = time.time()
    resultado = ejecutar_loop(item, top_k=top_k, max_iter=max_iter)
    duracion = round(time.time() - t0, 2)
    return {
        "max_iter": max_iter,
        "parada": resultado["parada"],
        "busquedas": resultado["iteraciones_usadas"],
        "duracion_s": duracion,
        "cobertura_ok": resultado["ultima_cobertura"]["cobertura_ok"],
        "faltantes": resultado["ultima_cobertura"]["faltantes"],
        "fuentes_esperadas": resultado["ultima_cobertura"]["fuentes_esperadas"],
        "fuentes_encontradas": resultado["ultima_cobertura"]["fuentes_encontradas"],
        "fuentes_completas": resultado["ultima_cobertura"]["fuentes_completas"],
        "paths_ultima": resultado["iteraciones"][-1]["paths"],
    }


def _parsear_args(argv=None) -> argparse.Namespace:
    """Construye y parsea los argumentos CLI. Acepta argv para testear."""
    parser = argparse.ArgumentParser(description="Medición clásico vs agentic (Fase 3)")
    parser.add_argument("--bank", default=str(BANCO_DEFAULT))
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--max-iter", type=int, default=3, help="Iteraciones máximas del modo agentic")
    parser.add_argument("--json", action="store_true", help="Salida JSON")
    parser.add_argument("--no-history", action="store_true", help="No guardar history-agentic.jsonl")
    return parser.parse_args(argv)


def _clasificar_y_contar(clasico: dict, agentic: dict, resumen: dict) -> str:
    """Actualiza los contadores del resumen según la cobertura de ambos modos
    y devuelve la marca de mejora. Los casos son mutuamente excluyentes:
    (no clásico y agentic) / (iguales) / (resto)."""
    if clasico["cobertura_ok"]:
        resumen["clasico_ok"] += 1
    if agentic["cobertura_ok"]:
        resumen["agentic_ok"] += 1

    if not clasico["cobertura_ok"] and agentic["cobertura_ok"]:
        resumen["agentic_resuelve_adicional"] += 1
        return "AGENTIC_RESUELVE"
    if clasico["cobertura_ok"] == agentic["cobertura_ok"]:
        resumen["sin_mejora"] += 1
        if not clasico["cobertura_ok"]:
            resumen["ambos_incompletos"] += 1
            return "AMBOS_INCOMPLETOS"
        return "SIN_MEJORA"
    return "CLASICO_MEJOR"  # teóricamente imposible (agentic parte de lo mismo)


def _construir_resultado(args: argparse.Namespace, banco: list, resumen: dict,
                         detalle: list, tiempo_clasico: float,
                         tiempo_agentic: float) -> dict:
    """Monta el dict final de resultado con los tiempos redondeados."""
    resumen["tiempo_clasico_s"] = round(tiempo_clasico, 2)
    resumen["tiempo_agentic_s"] = round(tiempo_agentic, 2)
    return {
        "timestamp": datetime.datetime.now().isoformat(),
        "top_k": args.top_k,
        "max_iter_agentic": args.max_iter,
        "banco": args.bank,
        "resumen": resumen,
        "detalle": detalle,
    }


def _guardar_history(resultado: dict, no_history: bool) -> None:
    """Añade la medición al historial JSONL (a menos que no_history)."""
    if no_history:
        return
    try:
        HISTORY.parent.mkdir(parents=True, exist_ok=True)
        with open(HISTORY, "a", encoding="utf-8") as f:
            f.write(json.dumps(resultado, ensure_ascii=False) + "\n")
    except OSError as e:
        print(f"  [aviso] no se pudo guardar history: {e}", file=sys.stderr)


def _imprimir_json(resultado: dict) -> None:
    print(json.dumps(resultado, ensure_ascii=False, indent=2))


def _imprimir_texto(resultado: dict) -> list:
    """Devuelve las líneas de la salida legible (el llamador las imprime)."""
    r = resultado["resumen"]
    lineas = [f"\n=== Medición Agentic RAG — clásico vs agentic ({resultado['timestamp']}) ===",
              f"Banco: {resultado['banco']} ({r['total']} items) | top_k={resultado['top_k']} | agentic máx {resultado['max_iter_agentic']} iter",
              f"\nCobertura clásica (1 búsqueda):  {r['clasico_ok']}/{r['total']}",
              f"Cobertura agentic (loop):        {r['agentic_ok']}/{r['total']}",
              f"Items que el agentic RESUELVE y el clásico NO: {r['agentic_resuelve_adicional']}",
              f"Items sin mejora (ambos igual):  {r['sin_mejora']}",
              f"Items incompletos en ambos:      {r['ambos_incompletos']}",
              f"Tiempo clásico:  {r['tiempo_clasico_s']}s | agentic: {r['tiempo_agentic_s']}s",
              "\nPor item:"]
    for d in resultado["detalle"]:
        marca = {"AGENTIC_RESUELVE": "▲ AGENTIC", "SIN_MEJORA": "=  IGUAL",
                 "AMBOS_INCOMPLETOS": "✗ AMBOS", "CLASICO_MEJOR": "▼ CLÁSICO"}[d["mejora"]]
        lineas.append(f"  [{marca}] {d['id']}: {d['pregunta'][:70]}")
        if d["mejora"] == "AGENTIC_RESUELVE":
            lineas.append(f"          clásico faltaba: {d['clasico']['faltantes']}")
            lineas.append(f"          agentic búsquedas: {d['agentic']['busquedas']} ({d['agentic']['duracion_s']}s)")
        if d["mejora"] == "AMBOS_INCOMPLETOS":
            lineas.append(f"          faltantes: {d['agentic']['faltantes']}")
    lineas.append("")
    return lineas


def _medir_banco(banco: list, args: argparse.Namespace) -> tuple:
    """Mide cada item en ambos modos (clásico y agentic). Devuelve
    (detalle, resumen, tiempo_clasico, tiempo_agentic)."""
    detalle = []
    resumen = {
        "total": len(banco),
        "clasico_ok": 0,
        "agentic_ok": 0,
        "agentic_resuelve_adicional": 0,
        "sin_mejora": 0,
        "ambos_incompletos": 0,
    }
    tiempo_clasico = 0.0
    tiempo_agentic = 0.0

    for item in banco:
        clasico = medir_modo(item, max_iter=1, top_k=args.top_k)
        agentic = medir_modo(item, max_iter=args.max_iter, top_k=args.top_k)
        tiempo_clasico += clasico["duracion_s"]
        tiempo_agentic += agentic["duracion_s"]

        mejora = _clasificar_y_contar(clasico, agentic, resumen)

        detalle.append({
            "id": item["id"],
            "pregunta": item["pregunta"],
            "tipo": item["tipo"],
            "mejora": mejora,
            "clasico": clasico,
            "agentic": agentic,
        })

    return detalle, resumen, tiempo_clasico, tiempo_agentic


def main():
    args = _parsear_args()
    banco = cargar_banco(args.bank)
    detalle, resumen, tiempo_clasico, tiempo_agentic = _medir_banco(banco, args)

    resultado = _construir_resultado(args, banco, resumen, detalle,
                                     tiempo_clasico, tiempo_agentic)
    _guardar_history(resultado, args.no_history)

    if args.json:
        _imprimir_json(resultado)
    else:
        for linea in _imprimir_texto(resultado):
            print(linea)


if __name__ == "__main__":
    main()
