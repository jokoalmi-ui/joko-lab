#!/usr/bin/env python3
"""
Muestra la evolución de precisión a lo largo de las ejecuciones guardadas
en history.jsonl, y qué preguntas fallan más a menudo (candidatas a mirar
si el conocimiento del lab sobre ese tema está mal indexado o mal escrito).

Uso:
    python3 analizar_historial.py --history history.jsonl
"""
import argparse
import json
from collections import defaultdict


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--history", default="history.jsonl")
    args = parser.parse_args()

    fallos_por_id = defaultdict(int)
    ejecuciones_por_id = defaultdict(int)
    filas = []

    with open(args.history, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            r = json.loads(linea)
            filas.append(r)
            for item in r["detalle"]:
                ejecuciones_por_id[item["id"]] += 1
                if not item["correcto"]:
                    fallos_por_id[item["id"]] += 1

    print("=== Tendencia de precisión ===")
    for r in filas:
        barra = "#" * round(r["precision"] * 40)
        print(f"{r['timestamp'][:16]}  {r['precision']*100:5.1f}%  {barra}")

    print("\n=== Preguntas que más fallan ===")
    ranking = sorted(fallos_por_id.items(), key=lambda x: x[1], reverse=True)
    for qid, fallos in ranking:
        total = ejecuciones_por_id[qid]
        print(f"  {qid}: falló {fallos}/{total} veces "
              f"({fallos/total*100:.0f}%) — revisar la fuente/indexación de esta pregunta")

    if not ranking:
        print("  (ninguna pregunta ha fallado todavía)")


if __name__ == "__main__":
    main()
