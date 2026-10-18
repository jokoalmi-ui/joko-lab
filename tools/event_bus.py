#!/usr/bin/env python3
"""event_bus.py — Sistema de eventos de Joko Lab

Capitalización automática: cuando se crea una DEC o EXP nueva,
el sistema reacciona automáticamente.

Eventos:
  dec.created     → Buscar RULE afectadas, sugerir activación
  exp.completed   → Buscar DEC relacionadas, sugerir revisión
  benchmark.new   → Buscar DEC que mencionen ese modelo, marcar revisión
  model.updated   → Invalidar DEC/EXP basadas en versión anterior

Uso:
  python3 event_bus.py --event dec.created --payload DEC-007
  python3 event_bus.py --watch  # Modo watcher (monitorea cambios)
"""

import os, sys, json, yaml, time
from pathlib import Path
from datetime import datetime

LAB_DIR = os.path.expanduser("~/joko-lab")
RULES_DIR = os.path.join(LAB_DIR, "01-knowledge", "rules")
DECISIONS_DIR = os.path.join(LAB_DIR, "01-knowledge", "decisions")
EXPERIMENTS_DIR = os.path.join(LAB_DIR, "01-knowledge", "experiments")
MODELS_DIR = os.path.join(LAB_DIR, "01-knowledge", "models")
METRICS_STORE = os.path.join(LAB_DIR, "04-operations", "metrics", "store.jsonl")

# ─── Handlers ───────────────────────────────────────────

def on_dec_created(dec_id: str) -> list:
    """Nueva DEC creada. Buscar RULEs afectadas y modelos relacionados."""
    actions = []
    
    # Buscar RULEs que referencien esta DEC
    if os.path.isdir(RULES_DIR):
        for fname in os.listdir(RULES_DIR):
            if not fname.endswith(".yaml"):
                continue
            try:
                with open(os.path.join(RULES_DIR, fname)) as f:
                    content = f.read()
                if dec_id in content:
                    actions.append({
                        "type": "rule_affected",
                        "file": fname,
                        "dec": dec_id,
                        "action": "Revisar RULE — la DEC origen ha cambiado"
                    })
            except Exception:
                pass
    
    # Buscar en el decision_engine si hay reglas hardcodeadas que referencien esta DEC
    de_path = os.path.join(LAB_DIR, "tools", "decision_engine.py")
    if os.path.exists(de_path):
        with open(de_path) as f:
            de_content = f.read()
        if dec_id in de_content:
            actions.append({
                "type": "hardcoded_rule_affected",
                "file": "decision_engine.py",
                "dec": dec_id,
                "action": "Revisar regla hardcodeada — mover a RULE YAML si es posible"
            })
    
    return actions


def on_exp_completed(exp_id: str) -> list:
    """Nuevo experimento completado. Buscar DECs relacionadas."""
    actions = []
    
    # Buscar el experimento para extraer qué modelo/prueba trata
    exp_path = os.path.join(EXPERIMENTS_DIR, exp_id) if exp_id.startswith("EXP-") else None
    if exp_path and os.path.isdir(exp_path):
        readme = os.path.join(exp_path, "README.md")
        if os.path.exists(readme):
            with open(readme) as f:
                content = f.read()[:1000]
            # Extraer nombres de modelos mencionados
            import re
            models = set(re.findall(r'(?:granite|gemma|deepseek|llama|dolphin|qwen|glm)[\w.-]*', content.lower()))
            for model in models:
                actions.append({
                    "type": "model_mentioned",
                    "exp": exp_id,
                    "model": model,
                    "action": f"Revisar DECs que mencionen {model}"
                })
    
    return actions


def on_model_updated(model_name: str, new_version: str = "") -> list:
    """Modelo actualizado. Invalidar conocimiento basado en versión anterior."""
    actions = []
    
    # Buscar en RULEs
    if os.path.isdir(RULES_DIR):
        for fname in os.listdir(RULES_DIR):
            if not fname.endswith(".yaml"):
                continue
            try:
                with open(os.path.join(RULES_DIR, fname)) as f:
                    rule = yaml.safe_load(f)
                accion = rule.get("accion", {})
                modelo = accion.get("modelo", "") if isinstance(accion, dict) else ""
                if model_name.lower() in modelo.lower():
                    actions.append({
                        "type": "rule_outdated",
                        "file": fname,
                        "rule": rule.get("id"),
                        "model": model_name,
                        "new_version": new_version,
                        "action": f"RULE {rule.get('id')} basada en {model_name} — marcar para revisión"
                    })
            except Exception:
                pass
    
    # Buscar fichas de modelo
    for fname in os.listdir(MODELS_DIR) if os.path.isdir(MODELS_DIR) else []:
        if model_name.lower() in fname.lower():
            actions.append({
                "type": "model_card_outdated",
                "file": fname,
                "model": model_name,
                "action": f"Ficha de modelo {fname} — revisar con nueva versión {new_version}"
            })
    
    return actions


def on_benchmark_new(model_name: str, results: dict = None) -> list:
    """Nuevo benchmark. Buscar DECs que mencionen ese modelo."""
    actions = []
    
    # Mismo comportamiento que model_updated para el modelo específico
    actions.extend(on_model_updated(model_name, "benchmark"))
    
    actions.append({
        "type": "benchmark_registered",
        "model": model_name,
        "action": "Nuevo benchmark disponible. Revisar decisiones de selección de modelo."
    })
    
    return actions


# ─── Core ───────────────────────────────────────────────

EVENT_HANDLERS = {
    "dec.created": on_dec_created,
    "exp.completed": on_exp_completed,
    "model.updated": on_model_updated,
    "benchmark.new": on_benchmark_new,
}


def emit(event_type: str, payload: str) -> list:
    """Emite un evento y devuelve las acciones generadas."""
    handler = EVENT_HANDLERS.get(event_type)
    if not handler:
        return [{"type": "error", "action": f"Evento desconocido: {event_type}"}]
    
    actions = handler(payload)
    
    # Registrar en metrics store
    _log_event(event_type, payload, actions)
    
    return actions


def _log_event(event_type: str, payload: str, actions: list):
    """Registra el evento en metrics store."""
    entry = {
        "timestamp": datetime.now().isoformat(),
        "component": "event_bus",
        "metric": event_type,
        "value": payload,
        "extra": {"actions_count": len(actions), "actions": [a["type"] for a in actions]}
    }
    try:
        Path(METRICS_STORE).parent.mkdir(parents=True, exist_ok=True)
        with open(METRICS_STORE, "a") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
        pass


def format_actions(actions: list, event_type: str, payload: str) -> str:
    """Formatea las acciones para consumo humano."""
    lines = []
    lines.append("═══════════════════════════════════════════")
    lines.append("  EVENT BUS — Acciones generadas")
    lines.append("═══════════════════════════════════════════")
    lines.append(f"  Evento: {event_type}")
    lines.append(f"  Payload: {payload}")
    lines.append(f"  Acciones: {len(actions)}")
    lines.append("")
    
    for i, a in enumerate(actions, 1):
        icon = {"rule_affected": "📋", "hardcoded_rule_affected": "⚠", 
                "model_mentioned": "🔍", "rule_outdated": "⏰",
                "model_card_outdated": "📄", "benchmark_registered": "📊",
                "error": "❌"}.get(a.get("type", ""), "→")
        lines.append(f"  {icon} {a.get('action', '')}")
    
    lines.append("═══════════════════════════════════════════")
    return "\n".join(lines)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Event Bus — capitalización automática Joko Lab")
    parser.add_argument("--event", type=str, required=True, 
                       choices=list(EVENT_HANDLERS.keys()),
                       help="Tipo de evento")
    parser.add_argument("--payload", type=str, required=True,
                       help="ID de DEC, EXP, modelo, etc.")
    parser.add_argument("--version", type=str, default="",
                       help="Nueva versión (para model.updated)")
    
    args = parser.parse_args()
    
    if args.event == "model.updated" and args.version:
        actions = on_model_updated(args.payload, args.version)
    else:
        actions = emit(args.event, args.payload)
    
    print(format_actions(actions, args.event, args.payload))
