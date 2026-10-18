#!/usr/bin/env python3
"""metrics_store.py — Almacén unificado de métricas de Joko Lab

Fuente única. Todas las herramientas escriben aquí.
Formato: JSONL (una línea JSON por evento).
Consultable por fecha, componente y tipo.

Uso:
  python3 metrics_store.py --component decision_router --metric confidence --value 85
  python3 metrics_store.py --query-last-week
  python3 metrics_store.py --query-component decision_router
"""

import os, sys, json
from datetime import datetime, timedelta
from pathlib import Path

STORE_PATH = os.path.expanduser("~/joko-lab/04-operations/metrics/store.jsonl")

def append(component: str, metric: str, value, extra: dict = None) -> dict:
    """Añade una entrada al store."""
    entry = {
        "timestamp": datetime.now().isoformat(),
        "component": component,
        "metric": metric,
        "value": value,
    }
    if extra:
        entry["extra"] = extra
    
    Path(STORE_PATH).parent.mkdir(parents=True, exist_ok=True)
    with open(STORE_PATH, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry

def query_last_week() -> list:
    """Devuelve entradas de los últimos 7 días."""
    cutoff = datetime.now() - timedelta(days=7)
    return _query_since(cutoff)

def query_last_24h() -> list:
    """Devuelve entradas de las últimas 24 horas."""
    cutoff = datetime.now() - timedelta(hours=24)
    return _query_since(cutoff)

def query_component(component: str, days: int = 30) -> list:
    """Devuelve entradas de un componente específico."""
    cutoff = datetime.now() - timedelta(days=days)
    results = []
    try:
        with open(STORE_PATH) as f:
            for line in f:
                entry = json.loads(line.strip())
                if entry.get("component") == component:
                    ts = datetime.fromisoformat(entry["timestamp"])
                    if ts >= cutoff:
                        results.append(entry)
    except FileNotFoundError:
        pass
    return results

def _query_since(cutoff: datetime) -> list:
    results = []
    try:
        with open(STORE_PATH) as f:
            for line in f:
                entry = json.loads(line.strip())
                ts = datetime.fromisoformat(entry["timestamp"])
                if ts >= cutoff:
                    results.append(entry)
    except FileNotFoundError:
        pass
    return results

def summary_week() -> dict:
    """Resumen agregado de la última semana."""
    entries = query_last_week()
    if not entries:
        return {"entries": 0, "components": {}, "message": "Sin datos esta semana."}
    
    components = {}
    for e in entries:
        comp = e["component"]
        if comp not in components:
            components[comp] = {"count": 0, "metrics": {}}
        components[comp]["count"] += 1
        metric = e["metric"]
        if metric not in components[comp]["metrics"]:
            components[comp]["metrics"][metric] = []
        components[comp]["metrics"][metric].append(e["value"])
    
    # Promedios
    for comp in components:
        for metric in components[comp]["metrics"]:
            vals = components[comp]["metrics"][metric]
            if all(isinstance(v, (int, float)) for v in vals):
                components[comp]["metrics"][metric] = {
                    "avg": round(sum(vals) / len(vals), 1),
                    "min": min(vals),
                    "max": max(vals),
                    "count": len(vals)
                }
    
    return {
        "entries": len(entries),
        "from": entries[0]["timestamp"] if entries else None,
        "to": entries[-1]["timestamp"] if entries else None,
        "components": components
    }

def format_summary(summary: dict) -> str:
    lines = []
    lines.append("═══════════════════════════════════════════")
    lines.append("  METRICS STORE — Resumen semanal")
    lines.append("═══════════════════════════════════════════")
    lines.append(f"  Entradas totales: {summary['entries']}")
    if summary.get("from"):
        lines.append(f"  Desde: {summary['from'][:19]}")
        lines.append(f"  Hasta: {summary['to'][:19]}")
    lines.append("")
    
    for comp, data in sorted(summary.get("components", {}).items()):
        lines.append(f"  {comp} ({data['count']} eventos)")
        for metric, vals in data["metrics"].items():
            if isinstance(vals, dict):
                lines.append(f"    {metric}: avg={vals['avg']} min={vals['min']} max={vals['max']} n={vals['count']}")
            else:
                lines.append(f"    {metric}: {len(vals)} valores no numéricos")
        lines.append("")
    
    lines.append("═══════════════════════════════════════════")
    return "\n".join(lines)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Metrics Store — almacén unificado Joko Lab")
    parser.add_argument("--component", type=str, help="Componente que reporta")
    parser.add_argument("--metric", type=str, help="Nombre de la métrica")
    parser.add_argument("--value", type=str, help="Valor de la métrica")
    parser.add_argument("--extra", type=str, help="JSON extra (opcional)")
    parser.add_argument("--query-last-week", action="store_true")
    parser.add_argument("--query-component", type=str)
    parser.add_argument("--summary", action="store_true", help="Resumen semanal")

    args = parser.parse_args()

    if args.component and args.metric and args.value is not None:
        try:
            val = json.loads(args.value)
        except (json.JSONDecodeError, ValueError):
            val = args.value
        extra = json.loads(args.extra) if args.extra else None
        entry = append(args.component, args.metric, val, extra)
        print(json.dumps(entry, ensure_ascii=False))

    elif args.summary:
        print(format_summary(summary_week()))

    elif args.query_last_week:
        for e in query_last_week():
            print(json.dumps(e, ensure_ascii=False))

    elif args.query_component:
        for e in query_component(args.query_component):
            print(json.dumps(e, ensure_ascii=False))

    else:
        parser.print_help()
