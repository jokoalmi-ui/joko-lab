#!/usr/bin/env python3
"""task_understanding.py — Fase 1 del Orchestrator

Analiza la consulta del usuario y devuelve un objetivo estructurado.
No llama a ningun worker. Solo responde: "Que quiere realmente el usuario?"

Uso:
  echo "necesito generar JSON estructurado" | python3 task_understanding.py
"""
import sys, re, os

TOOL_DIR = os.path.expanduser("~/joko-lab/tools")

# Deteccion de tipo de artefacto esperado — cargado desde YAML (fuente unica)
def _load_artifact_keywords():
    """Carga el mapeo de artefactos desde task_keywords.yaml"""
    import yaml
    kw_path = os.path.join(os.path.expanduser("~/joko-lab"), "01-knowledge", "task_keywords.yaml")
    try:
        with open(kw_path) as f:
            data = yaml.safe_load(f)
        return {k: v["keywords"] for k, v in data.get("artifact_types", {}).items()}
    except Exception:
        return {}

ARTIFACT_KEYWORDS = _load_artifact_keywords()

def _detectar_artefacto(q: str) -> str:
    """Devuelve el tipo de artefacto esperado según keywords."""
    for art, keywords in ARTIFACT_KEYWORDS.items():
        for kw in keywords:
            if kw in q:
                return art
    return "respuesta"


def _detectar_complejidad(q: str) -> str:
    """Devuelve la complejidad según longitud y marcadores."""
    if len(q) > 200:
        return "alta"
    if len(q) > 80 or any(w in q for w in ["paso a paso", "detallado", "completo"]):
        return "media"
    return "baja"


def _detectar_restricciones(q: str) -> list:
    """Devuelve las restricciones detectadas en la consulta."""
    constraints = []
    if "solo" in q or "unicamente" in q:
        constraints.append("respuesta concisa")
    if "json" in q:
        constraints.append("formato json")
    if "no inventes" in q:
        constraints.append("sin alucinaciones")
    if "local" in q:
        constraints.append("solo local")
    return constraints


def analyze(query: str) -> dict:
    """Analiza la consulta y devuelve un objetivo estructurado"""
    q = query.lower()
    
    # Detectar tipo de artefacto esperado
    artifact = _detectar_artefacto(q)
    
    # Detectar complejidad
    complexity = _detectar_complejidad(q)
    
    # Detectar restricciones
    constraints = _detectar_restricciones(q)
    
    # Detectar si requiere conocimiento del lab
    needs_lab = any(w in q for w in ["modelo", "gemma", "deepseek", "granite", 
                                      "decision", "experimento", "patron", "joko"])
    
    # Detectar si requiere busqueda RAG
    needs_rag = any(w in q for w in ["documentado", "registrado", "guardado",
                                      "sesion anterior", "recuerdas", "hemos hablado"])
    
    return {
        "query": query,
        "goal": query[:100],
        "artifact_type": artifact,
        "complexity": complexity,
        "constraints": constraints,
        "needs_lab_knowledge": needs_lab,
        "needs_rag": needs_rag,
        "suggested_pipeline": _suggest_pipeline(artifact, complexity, needs_lab, needs_rag)
    }

def _suggest_pipeline(artifact: str, complexity: str, needs_lab: bool, needs_rag: bool) -> list:
    """Sugiere los pasos del pipeline basado en el analisis"""
    steps = []
    
    if needs_rag or artifact in ("busqueda", "analisis", "informe"):
        steps.append("context_builder")
    
    if needs_lab:
        steps.append("knowledge_resolver")
    
    if artifact in ("decision", "prompt"):
        steps.append("decision_router")
    
    if artifact in ("prompt",):
        steps.append("evaluator_optimizer")
    
    if not steps:
        steps.append("llm_direct")
    
    return steps

def format_output(analysis: dict) -> str:
    lines = []
    lines.append("══ TASK UNDERSTANDING ══")
    lines.append(f"  Objetivo: {analysis['goal'][:80]}")
    lines.append(f"  Artefacto esperado: {analysis['artifact_type']}")
    lines.append(f"  Complejidad: {analysis['complexity']}")
    if analysis.get("constraints"):
        lines.append(f"  Restricciones: {', '.join(analysis['constraints'])}")
    lines.append(f"  Requiere lab: {analysis['needs_lab_knowledge']}")
    lines.append(f"  Requiere RAG: {analysis['needs_rag']}")
    lines.append(f"  Pipeline sugerido: {' → '.join(analysis['suggested_pipeline'])}")
    lines.append("════════════════════")
    return "\n".join(lines)

if __name__ == "__main__":
    if not sys.stdin.isatty():
        query = sys.stdin.read().strip()
    elif len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        print("Uso: echo 'objetivo' | python3 task_understanding.py")
        sys.exit(1)
    
    analysis = analyze(query)
    print(format_output(analysis))
