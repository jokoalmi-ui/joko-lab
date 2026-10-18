#!/usr/bin/env python3
"""decision_router.py - Selecciona modelo y parametros basado en evidencia

Usa Decision Memory, fichas de modelo y anti-patrones para recomendar
el mejor modelo para una tarea sin que el usuario tenga que pedirlo.

Uso:
  echo "necesito generar JSON estructurado" | python3 decision_router.py
  python3 decision_router.py "tarea de razonamiento paso a paso"
"""
import os, sys, json, subprocess, re
from pathlib import Path

TOOL_DIR = os.path.expanduser("~/joko-lab/tools")
LAB_DIR = os.path.expanduser("~/joko-lab")
VENV_PYTHON = os.path.expanduser("~/.venv/hermes-rag/bin/python3")

# Confidence Engine
from confidence import wrap, from_sources, format_badge, stamp, from_label, to_label

# Cache de routing: se llena desde RAG y se refresca periodicamente
# NO hardcodeado. La unica fuente de verdad es el RAG + Decision Memory.
ROUTING_CACHE = {}

def _query_rag_routing(task_type: str) -> dict:
    """Consulta el RAG para encontrar la decision y ficha del mejor modelo.
    UNICA fuente de verdad. Sin hardcodeo."""
    decision_query = f"decision modelo para {task_type}"
    search = os.path.join(TOOL_DIR, "search.py")
    try:
        result = subprocess.run(
            [VENV_PYTHON, search, "-q", decision_query, "-k", "2"],
            capture_output=True, text=True, timeout=15
        )
        stdout = result.stdout[:800]
    except Exception:
        stdout = ""
    
    if not stdout.strip():
        return None
    
    # Intentar extraer modelo y decision del contexto RAG
    model_match = re.search(r'(?:modelo|model):\s*([^\s,]+)', stdout, re.IGNORECASE)
    decision_match = re.search(r'(DEC-\d+|EXP-\d+)', stdout)
    
    if model_match:
        return {
            "model": model_match.group(1),
            "params": {"max_tokens": 2048, "temperature": 0.5},
            "decision": decision_match.group(1) if decision_match else "RAG",
            "confidence": "MEDIA",
            "rag_context": stdout,
            "note": "Desde RAG (fuente unica)"
        }
    
    # Si hay contexto pero no se pudo parsear modelo, devolver contexto bruto
    return {
        "model": None,
        "params": {"max_tokens": 1024, "temperature": 0.3},
        "decision": "RAG",
        "confidence": "BAJA",
        "rag_context": stdout,
        "note": "RAG encontro contexto pero no se pudo extraer modelo especifico"
    }

# Mapeo de palabras clave a tipos de tarea — cargado desde YAML (fuente unica)
def _load_task_keywords():
    """Carga el mapeo de keywords desde task_keywords.yaml"""
    import yaml
    kw_path = os.path.join(LAB_DIR, "01-knowledge", "task_keywords.yaml")
    try:
        with open(kw_path) as f:
            data = yaml.safe_load(f)
        return {k: v["keywords"] for k, v in data.get("task_types", {}).items()}
    except Exception:
        return {}

TASK_KEYWORDS = _load_task_keywords()

def detect_task_type(query: str) -> list:
    """Detecta tipos de tarea por palabras clave"""
    q = query.lower()
    matches = []
    for task_type, keywords in TASK_KEYWORDS.items():
        for kw in keywords:
            if kw in q:
                matches.append(task_type)
                break
    return matches[:2]  # Max 2 tipos

def query_rag_decisions(task_types: list) -> str:
    """Consulta Decision Memory via RAG para los tipos de tarea"""
    query = "decision modelo seleccion " + " ".join(task_types)
    search_script = os.path.join(TOOL_DIR, "search.py")
    try:
        result = subprocess.run(
            [VENV_PYTHON, search_script, "-q", query, "-k", "2"],
            capture_output=True, text=True, timeout=15
        )
        return result.stdout
    except Exception:
        return ""

def build_recommendation(query: str) -> dict:
    """Construye recomendacion basada en evidencia"""
    task_types = detect_task_type(query)
    
    # Si no se detecta tipo, devolver generico
    if not task_types:
        return {
            "query": query,
            "task_detected": None,
            "recommendation": None,
            "confidence": "BAJA",
            "source": "No se detecto tipo de tarea",
            "fallback": {
                "model": "granite-4.1-8b",
                "params": {"max_tokens": 1024, "temperature": 0.3},
                "note": "Modelo equilibrado por defecto. Rapido (5-15s)"
            }
        }
    
    # Buscar via RAG + mapa de capacidades (unica fuente de verdad)
    primary_type = task_types[0]
    route = _query_rag_routing(primary_type)
    
    # Si no esta en la tabla, buscar decisiones via RAG
    if not route:
        rag_result = query_rag_decisions(task_types)
        return {
            "query": query,
            "task_detected": primary_type,
            "recommendation": None,
            "confidence": "BAJA",
            "source": "No hay decision documentada para este tipo de tarea",
            "rag_context": rag_result[:500] if rag_result else "",
            "fallback": {
                "model": "granite-4.1-8b",
                "params": {"max_tokens": 1024, "temperature": 0.3},
                "note": "Ruta no documentada. Usar modelo equilibrado y documentar."
            }
        }
    
    # Verificar que el modelo no esta descartado
    if "qwen-3.5" in route["model"] or "descartado" in route.get("note", ""):
        return {
            "query": query,
            "task_detected": primary_type,
            "recommendation": None,
            "confidence": "ALTA",
            "source": "DEC-001: modelo descartado",
            "note": "El modelo designado para esta tarea fue descartado",
            "fallback": {
                "model": "granite-4.1-8b",
                "params": {"max_tokens": 1024, "temperature": 0.3},
                "note": "Modelo descartado. Usar alternativa."
            }
        }
    
    # Alternativa si el primario es lento (>50s) y hay un rapido disponible
    alternatives = []
    if primary_type == "creatividad":
        alternatives.append({
            "model": "granite-4.1-8b",
            "params": {"max_tokens": 1024, "temperature": 0.5},
            "note": "Alternativa rapida (5-15s) si no necesitas maxima calidad creativa",
            "tradeoff": "Velocidad > Calidad"
        })
    if primary_type == "razonamiento":
        alternatives.append({
            "model": "granite-4.1-8b",
            "params": {"max_tokens": 1024, "temperature": 0.3},
            "note": "Alternativa rapida (5-15s) para razonamiento simple",
            "tradeoff": "Velocidad > Profundidad"
        })
    
    result = {
        "query": query,
        "task_detected": primary_type,
        "recommendation": route,
        "source": f"{route['decision']} ({route.get('evidence', route.get('note', 'RAG'))})",
        "alternatives": alternatives if alternatives else None,
        "note": route.get("note", "")
    }
    return stamp(result, [route.get("decision", "RAG")], extra_evidence=[route.get("note", "")])

def format_output(rec: dict) -> str:
    """Formatea la recomendacion para consumo humano"""
    lines = []
    lines.append("═══════════════════════════════════════════")
    lines.append("  ROUTER DE DECISION — Recomendacion")
    lines.append("═══════════════════════════════════════════")
    lines.append(f"  Consulta: {rec['query'][:80]}")
    lines.append(f"  Tipo detectado: {rec['task_detected'] or 'ninguno'}")
    
    if rec.get("recommendation"):
        r = rec["recommendation"]
        lines.append("")
        lines.append("── RECOMENDACION ──")
        lines.append(f"  Modelo:       {r['model']}")
        lines.append(f"  max_tokens:   {r['params']['max_tokens']}")
        lines.append(f"  temperature:  {r['params']['temperature']}")
        lines.append(f"  Confianza:    {rec['confidence']}")
        lines.append(f"  Evidencia:    {rec['source']}")
        if rec.get("note"):
            lines.append(f"  Nota:         {rec['note']}")
        
        if rec.get("alternatives"):
            lines.append("")
            lines.append("── ALTERNATIVAS ──")
            for alt in rec["alternatives"]:
                lines.append(f"  → {alt['model']} ({alt['tradeoff']})")
                lines.append(f"    {alt['note']}")
    
    elif rec.get("fallback"):
        f = rec["fallback"]
        lines.append("")
        lines.append("── FALLBACK (sin decision documentada) ──")
        lines.append(f"  Modelo:       {f['model']}")
        lines.append(f"  max_tokens:   {f['params']['max_tokens']}")
        lines.append(f"  temperature:  {f['params']['temperature']}")
        lines.append(f"  Nota:         {f.get('note', 'Sin ruta documentada')}")
    
    elif rec.get("rag_context"):
        lines.append("")
        lines.append("── CONTEXTO RAG ──")
        lines.append(f"  {rec['rag_context'][:300]}")
    
    lines.append("═══════════════════════════════════════════")
    return "\n".join(lines)

if __name__ == "__main__":
    if not sys.stdin.isatty():
        query = sys.stdin.read().strip()
    elif len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        print("Uso: echo 'tarea' | python3 decision_router.py")
        sys.exit(1)
    
    rec = build_recommendation(query)
    
    # Modo JSON para auto_dispatcher
    if "--json" in sys.argv:
        print(json.dumps(rec, ensure_ascii=False, indent=2))
        sys.exit(0)
    
    print(format_output(rec))
    
    # Confidence badge
    from confidence import from_label
    conf = from_label(rec.get("confidence", "BAJA"))
    print(f"\n--- Confidence: {format_badge(conf)} | Decisión: {rec.get('source','RAG')} ---")
