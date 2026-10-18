#!/usr/bin/env python3
"""orchestrator.py — Fases 1-2 del Orchestrator + Workers

Flujo:
  1. Task Understanding → goal estructurado
  2. Planning → plan.yaml con steps ordenados
  3. [Fase 3 pendiente] Execution con Blackboard

Integra los componentes existentes en un pipeline unificado.

Uso:
  echo "necesito generar JSON estructurado" | python3 orchestrator.py
  python3 orchestrator.py "escribe un poema creativo"
"""

import os, sys, json, subprocess
from pathlib import Path

TOOL_DIR = os.path.expanduser("~/joko-lab/tools")
sys.path.insert(0, TOOL_DIR)

def run_phase1(query: str) -> dict:
    """Fase 1: Task Understanding."""
    from task_understanding import analyze
    return analyze(query)

def run_phase2(task: dict) -> dict:
    """Fase 2: Planning."""
    from planning_engine import build_plan
    return build_plan(task)

def run_pipeline(query: str) -> dict:
    """Pipeline completo Fase 1 + Fase 2."""
    # Fase 1
    task = run_phase1(query)
    
    # Fase 2
    plan = run_phase2(task)
    
    # Integrar con Activation Engine si existe
    try:
        from activation_engine import activate
        activation = activate(task.get("artifact_type", "general"), query)
        plan["activation"] = {
            "model_selection": activation.get("model_selection", {}).get("id") if activation.get("model_selection") else None,
            "blocks": [b["id"] for b in activation.get("blocks", [])],
            "total_active": activation.get("total_active", 0)
        }
    except ImportError:
        plan["activation"] = {"status": "activation_engine no disponible"}
    
    return {
        "query": query,
        "task": task,
        "plan": plan,
    }

def format_output(result: dict) -> str:
    """Formatea el resultado del orchestrator."""
    lines = []
    lines.append("═══════════════════════════════════════════")
    lines.append("  ORCHESTRATOR — Pipeline F1+F2")
    lines.append("═══════════════════════════════════════════")
    
    task = result.get("task", {})
    plan = result.get("plan", {})
    
    # Fase 1
    lines.append(f"  F1 — TASK UNDERSTANDING")
    lines.append(f"  Goal: {task.get('goal', task.get('artifact_type', '?'))}")
    lines.append(f"  Tipo: {task.get('artifact_type', '?')}")
    lines.append(f"  Complejidad: {task.get('complexity', '?')}")
    
    # Fase 2
    lines.append("")
    lines.append(f"  F2 — PLANNING")
    lines.append(f"  Confianza estimada: {plan.get('estimated_confidence', '?')}%")
    
    steps = plan.get("steps", [])
    if steps:
        lines.append(f"  Steps: {len(steps)}")
        for i, step in enumerate(steps, 1):
            lines.append(f"    {i}. {step.get('worker', '?')}: {step.get('purpose', step.get('description', '?'))}")
    
    # Activation
    activation = plan.get("activation", {})
    if activation and activation.get("total_active", 0) > 0:
        lines.append("")
        lines.append(f"  ACTIVATION ENGINE: {activation['total_active']} reglas activas")
        if activation.get("model_selection"):
            lines.append(f"    Modelo: {activation['model_selection']}")
        if activation.get("blocks"):
            lines.append(f"    Bloques: {', '.join(activation['blocks'])}")
    
    lines.append("═══════════════════════════════════════════")
    return "\n".join(lines)


if __name__ == "__main__":
    # Leer entrada
    if not sys.stdin.isatty():
        query = sys.stdin.read().strip()
    elif len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        print("Uso: echo 'objetivo' | python3 orchestrator.py")
        sys.exit(1)
    
    result = run_pipeline(query)
    print(format_output(result))
    
    # Opción JSON
    if "--json" in sys.argv:
        print(json.dumps(result, ensure_ascii=False, indent=2))
