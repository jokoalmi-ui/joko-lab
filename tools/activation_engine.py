#!/usr/bin/env python3
"""activation_engine.py — Knowledge Activation Layer

Busca RULE activas aplicables a la tarea actual.
No responde. No razona. Solo activa reglas.

El Activation Engine se sitúa entre Knowledge Resolver y Decision Engine:
  Usuario → Task Analyzer → Knowledge Resolver → Activation Engine → Decision Engine → Respuesta

Responde a la pregunta de Luis:
  "¿Qué conocimiento existente debe modificar esta ejecución?"

Uso:
  python3 activation_engine.py --task-type creatividad
  python3 activation_engine.py --prompt "escribe un poema creativo"
"""

import os, sys, yaml, re
from pathlib import Path
from datetime import datetime

OBJECTS_DIR = os.path.expanduser("~/joko-lab/01-knowledge/objects")


def _ko_to_legacy(ko: dict) -> dict:
    """Convierte un Knowledge Object v1 (objects/) al formato plano legacy.

    Los campos operativos (condicion, accion, prioridad, activa, validaciones,
    nota, alcance) viven en legacy_fields; los de gobierno (confidence,
    last_validated, dependencies) en la raiz del KO. Esta funcion aplana ambos
    para que el resto del codigo (activate, recalculate_confidence) no cambie.
    """
    legacy = dict(ko.get("legacy_fields", {}) or {})
    legacy.setdefault("id", ko.get("id"))
    legacy.setdefault("type", ko.get("type"))
    legacy.setdefault("status", ko.get("status", "activo"))
    legacy.setdefault("desc", ko.get("body", ""))
    legacy.setdefault("confianza", ko.get("confidence"))
    legacy.setdefault("ultima_revision", ko.get("last_validated") or ko.get("created"))
    if not legacy.get("origen"):
        deps = ko.get("dependencies") or []
        legacy["origen"] = deps[0] if deps else None
    return legacy


def load_rules() -> list:
    """Carga todas las RULE (type=RULE) desde objects/ (Knowledge Objects v1)."""
    rules = []
    if not os.path.isdir(OBJECTS_DIR):
        return rules
    for fname in sorted(os.listdir(OBJECTS_DIR)):
        if fname.endswith(".yaml") or fname.endswith(".yml"):
            try:
                with open(os.path.join(OBJECTS_DIR, fname)) as f:
                    ko = yaml.safe_load(f)
                if not isinstance(ko, dict) or ko.get("type") != "RULE":
                    continue
                rule = _ko_to_legacy(ko)
                rule["_file"] = fname
                rules.append(rule)
            except Exception:
                pass
    return rules


def load_policies() -> list:
    """Carga todas las POLICY (type=POLICY) desde objects/ (Knowledge Objects v1)."""
    policies = []
    if not os.path.isdir(OBJECTS_DIR):
        return policies
    for fname in sorted(os.listdir(OBJECTS_DIR)):
        if fname.endswith(".yaml") or fname.endswith(".yml"):
            try:
                with open(os.path.join(OBJECTS_DIR, fname)) as f:
                    ko = yaml.safe_load(f)
                if not isinstance(ko, dict) or ko.get("type") != "POLICY":
                    continue
                policy = _ko_to_legacy(ko)
                policy["_file"] = fname
                policies.append(policy)
            except Exception:
                pass
    return policies

def _match_rule(task_type: str, prompt_lower: str, rule: dict) -> bool:
    cond = rule.get("condicion", {}) or {}
    tipos = cond.get("tipo_tarea", [])
    keywords = cond.get("keywords", [])
    tipo_match = task_type in tipos or "cualquiera" in tipos
    kw_match = any(kw.lower() in prompt_lower for kw in keywords) if prompt_lower else (not keywords)
    if keywords and not kw_match:
        return False
    if not tipo_match:
        return False
    return True


def _es_block(rule: dict) -> bool:
    accion = rule.get("accion", {})
    return isinstance(accion, dict) and accion.get("accion") == "block"


def _es_modelo(rule: dict) -> bool:
    accion = rule.get("accion", {})
    return isinstance(accion, dict) and "modelo" in accion


def _mejor_modelo(rule: dict, current) -> bool:
    if current is None:
        return True
    return rule.get("prioridad", 0) > current.get("prioridad", 0)


def _aplicar_politicas(policies: list) -> list:
    policy_blocks = []
    for pol in policies:
        if not pol.get("activa", True):
            continue
        if pol.get("accion") == "block" or pol.get("accion") == "force_local":
            policy_blocks.append(pol)
    return policy_blocks


def _trace_modelo(model_selection: dict) -> dict:
    accion = model_selection.get("accion", {})
    modelo = accion.get("modelo", "?") if isinstance(accion, dict) else "?"
    return {
        "knowledge": model_selection.get("desc", ""),
        "evidence": [model_selection.get("origen", "?")],
        "decision": f"Seleccionar {modelo}",
        "proof": f"{model_selection.get('validaciones', '?')} validaciones, {model_selection.get('confianza', '?')} confianza",
        "timestamp": datetime.now().isoformat()
    }


def activate(task_type: str, prompt: str = "", context: dict = None) -> dict:
    """Activa reglas aplicables a la tarea actual.
    
    Args:
        task_type: tipo de tarea (creatividad, json, razonamiento, etc.)
        prompt: texto del prompt del usuario (para matching por keywords)
        context: contexto adicional (decisiones, fichas, etc.)
    
    Returns:
        {
            "active_rules": [...],     # RULEs aplicables ordenadas por prioridad
            "active_policies": [...],  # POLICYs aplicables
            "blocks": [...],           # RULEs/POLICYs que bloquean 
            "model_selection": {...},  # RULE que selecciona modelo (si hay)
            "total_active": N
        }
    """
    rules = load_rules()
    policies = load_policies()
    prompt_lower = prompt.lower() if prompt else ""
    
    active = []
    blocks = []
    model_selection = None
    
    for rule in rules:
        if not rule.get("activa", True):
            continue
        
        if not _match_rule(task_type, prompt_lower, rule):
            continue
        
        if _es_block(rule):
            blocks.append(rule)
        elif _es_modelo(rule):
            if _mejor_modelo(rule, model_selection):
                model_selection = rule
        else:
            active.append(rule)
    
    active.sort(key=lambda r: r.get("prioridad", 0), reverse=True)
    
    policy_blocks = _aplicar_politicas(policies)
    
    if model_selection:
        model_selection["_trace"] = _trace_modelo(model_selection)
    
    _log_activation(task_type, active, blocks, policy_blocks, model_selection)

    return {
        "active_rules": active,
        "active_policies": policy_blocks,
        "blocks": blocks + policy_blocks,
        "model_selection": model_selection,
        "total_active": len(active) + len(blocks) + len(policy_blocks),
    }


def _log_activation(task_type, active, blocks, policy_blocks, model_selection):
    """Registro de activacion en activation-ledger.jsonl (telemetria F1).
    Solo anade una linea JSONL. Nunca interrumpe el flujo."""
    try:
        import json as _json
        from datetime import datetime as _dt
        entry = {
            "timestamp": _dt.now().isoformat(),
            "task_type": task_type,
            "active_rules": [r.get("id") for r in active],
            "blocks": [r.get("id") for r in blocks],
            "policies": [p.get("id") for p in policy_blocks],
            "model_selection": model_selection.get("id") if model_selection else None,
        }
        path = os.path.expanduser("/mnt/ssd_ia_datos/lab-state/activation-ledger.jsonl")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "a", encoding="utf-8") as f:
            f.write(_json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
        pass  # telemetria nunca debe romper la activacion

def format_activation(result: dict) -> str:
    """Formatea el resultado de activación para consumo humano."""
    lines = []
    lines.append("═══════════════════════════════════════════")
    lines.append("  ACTIVATION ENGINE — Reglas activadas")
    lines.append("═══════════════════════════════════════════")
    lines.append(f"  Reglas activas: {result['total_active']}")
    lines.append("")
    
    if result["blocks"]:
        lines.append("── 🚫 BLOQUEOS ──")
        for b in result["blocks"]:
            lines.append(f"  ❌ {b['id']} (prioridad {b.get('prioridad','?')})")
            lines.append(f"     {b.get('desc', b.get('nota', ''))[:100]}")
        lines.append("")
    
    if result["model_selection"]:
        m = result["model_selection"]
        accion = m.get("accion", {})
        modelo = accion.get("modelo", "?") if isinstance(accion, dict) else "?"
        lines.append("── 🎯 MODELO SELECCIONADO ──")
        lines.append(f"  {m['id']}: {modelo} (prioridad {m.get('prioridad','?')})")
        lines.append(f"  {m.get('desc', '')[:100]}")
        lines.append("")
    
    if result["active_rules"]:
        lines.append("── ▶ REGLAS ACTIVAS ──")
        for r in result["active_rules"]:
            lines.append(f"  → {r['id']} [{r.get('origen','?')}] p={r.get('prioridad','?')}")
            lines.append(f"    {r.get('desc','')[:100]}")
        lines.append("")
    
    if not result["total_active"]:
        lines.append("  Sin reglas activas para esta tarea.")
        lines.append("  El Decision Engine usará fallback por defecto.")
    
    lines.append("═══════════════════════════════════════════")
    return "\n".join(lines)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Activation Engine — Knowledge Activation Layer")
    parser.add_argument("--task-type", type=str, help="Tipo de tarea (creatividad, json, razonamiento, etc.)")
    parser.add_argument("--prompt", type=str, help="Prompt del usuario (para matching por keywords)")
    parser.add_argument("--json", action="store_true", help="Salida JSON")
    
    args = parser.parse_args()
    
    task_type = args.task_type or "general"
    prompt = args.prompt or ""
    
    result = activate(task_type, prompt)
    
    if args.json:
        import json
        # Simplificar para JSON (quitar objetos yaml internos)
        clean = {
            "total_active": result["total_active"],
            "blocks": [{"id": b["id"], "desc": b.get("desc", ""), "prioridad": b.get("prioridad")} for b in result["blocks"]],
            "model_selection": result["model_selection"]["id"] if result["model_selection"] else None,
            "active_rules": [{"id": r["id"], "origen": r.get("origen"), "prioridad": r.get("prioridad")} for r in result["active_rules"]],
        }
        print(json.dumps(clean, ensure_ascii=False, indent=2))
    else:
        print(format_activation(result))
