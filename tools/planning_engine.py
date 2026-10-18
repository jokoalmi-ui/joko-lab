#!/usr/bin/env python3
"""planning_engine.py — Fase 2 del Orchestrator

Recibe el objetivo estructurado de task_understanding.py y disena
un plan de ejecucion con pasos ordenados y workers asignados.

Uso:
  echo '{"goal":"necesito JSON","artifact_type":"prompt",...}' | python3 planning_engine.py
"""
import sys, os, json

TOOL_DIR = os.path.expanduser("~/joko-lab/tools")

# Catalogo de workers disponibles
WORKERS = {
    "context_builder": {
        "script": "context_builder.py",
        "description": "Recupera contexto del RAG (documentos, sesiones, fichas)",
        "produces": "contexto_formateado",
        "confidence_impact": 20
    },
    "knowledge_resolver": {
        "script": "knowledge_resolver.py",
        "description": "Sintetiza documentos en conocimiento estructurado",
        "produces": "hechos_decisiones_conflictos",
        "confidence_impact": 25
    },
    "decision_router": {
        "script": "decision_router.py",
        "description": "Recomienda modelo y parametros basado en evidencia",
        "produces": "modelo_recomendado_params",
        "confidence_impact": 30
    },
    "evaluator_optimizer": {
        "script": "evaluator_optimizer.py",
        "description": "Mejora prompts por bucle adversarial con gate",
        "produces": "prompt_mejorado_verificado",
        "confidence_impact": 15
    },
    "evidence_collector": {
        "script": "evidence_collector.py",
        "description": "Decide si un resultado merece registrarse como conocimiento",
        "produces": "nivel_evidencia_acciones",
        "confidence_impact": 10
    },
}

def build_plan(task: dict) -> dict:
    """Construye un plan de ejecucion a partir del objetivo"""
    steps = []
    estimated_confidence = 30  # Confianza inicial sin contexto
    
    # Paso 1: Si necesita RAG o conocimiento, empezar con Context Builder
    if task.get("needs_rag") or task.get("needs_lab_knowledge"):
        steps.append({
            "order": len(steps) + 1,
            "worker": "context_builder",
            "input": task.get("goal", ""),
            "expected_output": "Contexto relevante del laboratorio",
            "purpose": "Recuperar documentos, sesiones y fichas relacionadas"
        })
        estimated_confidence += WORKERS["context_builder"]["confidence_impact"]
    
    # Paso 2: Knowledge Resolver si hay contexto
    if steps and task.get("needs_lab_knowledge"):
        steps.append({
            "order": len(steps) + 1,
            "worker": "knowledge_resolver",
            "input": "Salida del Context Builder",
            "expected_output": "Hechos, decisiones y conflictos estructurados",
            "purpose": "Sintetizar documentos en conocimiento accionable"
        })
        estimated_confidence += WORKERS["knowledge_resolver"]["confidence_impact"]
    
    # Paso 3: Decision Router si necesita elegir modelo
    if task.get("artifact_type") in ("decision", "prompt", "codigo"):
        steps.append({
            "order": len(steps) + 1,
            "worker": "decision_router",
            "input": "Salida del Knowledge Resolver + objetivo original",
            "expected_output": "Modelo recomendado con parametros",
            "purpose": "Seleccionar el mejor modelo basado en evidencia"
        })
        estimated_confidence += WORKERS["decision_router"]["confidence_impact"]
    
    # Paso 4: Evaluator-Optimizer si es un prompt
    if task.get("artifact_type") == "prompt":
        steps.append({
            "order": len(steps) + 1,
            "worker": "evaluator_optimizer",
            "input": "Prompt original + recomendacion del router",
            "expected_output": "Prompt optimizado y verificado contra modelo destino",
            "purpose": "Mejorar el prompt y validar respuesta real"
        })
        estimated_confidence += WORKERS["evaluator_optimizer"]["confidence_impact"]
    
    # Paso 5: Evidence Collector (siempre al final si hay mejora)
    if len(steps) > 1:
        steps.append({
            "order": len(steps) + 1,
            "worker": "evidence_collector",
            "input": "Resultado del ultimo paso",
            "expected_output": "Nivel de evidencia y acciones recomendadas",
            "purpose": "Evaluar si el resultado merece registro como conocimiento"
        })
    
    return {
        "goal": task.get("goal", ""),
        "artifact_type": task.get("artifact_type", "desconocido"),
        "steps": steps,
        "total_workers": len(steps),
        "estimated_confidence": min(estimated_confidence, 100),
        "ready": len(steps) > 0
    }

def format_output(plan: dict) -> str:
    lines = []
    lines.append("══ PLANNING ENGINE ══")
    lines.append(f"  Objetivo: {plan['goal'][:80]}")
    lines.append(f"  Tipo: {plan['artifact_type']}")
    lines.append(f"  Confianza estimada: {plan['estimated_confidence']}%")
    lines.append(f"  Workers: {plan['total_workers']}")
    lines.append("")
    
    for step in plan["steps"]:
        worker_info = WORKERS.get(step["worker"], {})
        lines.append(f"  Paso {step['order']}: {step['worker']}")
        lines.append(f"    Proposito: {step['purpose']}")
        lines.append(f"    Entrada: {step['input'][:80]}")
        lines.append(f"    Salida esperada: {step['expected_output']}")
        lines.append("")
    
    lines.append("═════════════════")
    return "\n".join(lines)

if __name__ == "__main__":
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
    else:
        print("Uso: task_understanding.py | tee /dev/stderr | planning_engine.py")
        sys.exit(1)
    
    try:
        task = json.loads(raw)
    except json.JSONDecodeError:
        # Intentar extraer campos de la salida de task_understanding
        task = {
            "goal": raw,
            "artifact_type": "desconocido",
            "needs_rag": "busca" in raw.lower() or "encuentra" in raw.lower(),
            "needs_lab_knowledge": "modelo" in raw.lower()
        }
    
    plan = build_plan(task)
    print(format_output(plan))
