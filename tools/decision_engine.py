#!/usr/bin/env python3
"""decision_engine.py v2 — Action Layer de Joko Lab

Phase 2: Cognitive Engineering.
Tres mejoras sobre v1:
  1. Checklists obligatorias por tipo de tarea
  2. Conocimiento pasivo (informa) vs activo (cambia comportamiento)
  3. Gate de validacion: nada se auto-aplica sin origen documentado

Flujo:
  Usuario → Task Analyzer → Action Layer → [checklist + reglas] → Hermes
"""
import os, sys, json
from pathlib import Path

TOOL_DIR = os.path.expanduser("~/joko-lab/tools")
LAB_DIR  = os.path.expanduser("~/joko-lab")

# ═══════════════════════════════════════════════════
# 1. CONOCIMIENTO PASIVO vs ACTIVO
# ═══════════════════════════════════════════════════
# PASIVO: informa, no cambia comportamiento (fichas, docs, RAG)
# ACTIVO: modifica comportamiento (DEC, anti-patrones FATAL, politicas)

KNOWLEDGE_TYPES = {
    "DEC":       {"type": "activo", "can_modify": True,  "priority": 10},
    "FATAL":     {"type": "activo", "can_modify": True,  "priority": 10},
    "POLICY":    {"type": "activo", "can_modify": True,  "priority": 9},
    "RULE":      {"type": "activo", "can_modify": True,  "priority": 8},
    "PATTERN":   {"type": "pasivo", "can_modify": False, "priority": 5},
    "FICHA":     {"type": "pasivo", "can_modify": False, "priority": 3},
    "EXPERIMENT": {"type": "pasivo", "can_modify": False, "priority": 2},
    "OBS":       {"type": "pasivo", "can_modify": False, "priority": 1},
}

# ═══════════════════════════════════════════════════
# 2. CHECKLISTS OBLIGATORIAS POR TIPO DE TAREA
# ═══════════════════════════════════════════════════
# Cada tipo de tarea tiene pasos obligatorios.
# Si falta uno → STOP. No responde.

TASK_CHECKLISTS = {
    "prompt": {
        "name": "Generacion de Prompt",
        "mandatory": [
            {"id": "ficha_modelo",    "desc": "Consultar ficha del modelo destino"},
            {"id": "anti_patrones",   "desc": "Verificar anti-patrones del modelo"},
            {"id": "decisiones",      "desc": "Consultar decisiones activas"},
            {"id": "prompt_project",  "desc": "Activar Prompt Project (spec.yaml)"},
        ],
        "recommended": [
            {"id": "experimentos",    "desc": "Buscar experimentos relacionados"},
            {"id": "patrones",        "desc": "Aplicar patrones de prompt conocidos"},
        ],
    },
    "codigo": {
        "name": "Generacion de Codigo",
        "mandatory": [
            {"id": "patrones",        "desc": "Buscar patrones de codigo"},
            {"id": "decisiones",      "desc": "Consultar decisiones activas"},
            {"id": "benchmarks",      "desc": "Buscar benchmarks del modelo"},
        ],
        "recommended": [
            {"id": "experimentos",    "desc": "Buscar experimentos de codigo"},
        ],
    },
    "docker": {
        "name": "Docker / Infraestructura",
        "mandatory": [
            {"id": "recovery",        "desc": "Consultar procedimientos de recovery"},
            {"id": "incidentes",      "desc": "Buscar incidentes anteriores"},
            {"id": "configuracion",   "desc": "Verificar configuracion actual"},
        ],
        "recommended": [],
    },
    "analisis": {
        "name": "Analisis / Evaluacion",
        "mandatory": [
            {"id": "experimentos",    "desc": "Buscar experimentos previos"},
            {"id": "decisiones",      "desc": "Consultar decisiones relacionadas"},
        ],
        "recommended": [
            {"id": "patrones",        "desc": "Buscar patrones aplicables"},
            {"id": "anti_patrones",   "desc": "Verificar anti-patrones"},
        ],
    },
    "decision": {
        "name": "Toma de Decision",
        "mandatory": [
            {"id": "experimentos",    "desc": "Buscar experimentos que respalden"},
            {"id": "decisiones",      "desc": "Verificar decisiones existentes"},
            {"id": "evidencia",       "desc": "Evaluar nivel de evidencia (E1/E2/E3)"},
        ],
        "recommended": [],
    },
}

# ═══════════════════════════════════════════════════
# 3. REGLAS DE ACCION (v2 — con origen documentado y gate)
# ═══════════════════════════════════════════════════
# Cada regla tiene:
#   - origen: documento que la respalda (obligatorio)
#   - gate: nivel requerido (DEC > FATAL > POLICY)
#   - Solo conocimiento ACTIVO puede modificar comportamiento

RULES = [
    # ─── BLOQUEAR (FATAL) ───
    {
        "id": "FATAL-qwen35",
        "condition": lambda q: "qwen 3.5" in q.lower(),
        "action": "block",
        "reason": "DEC-001: Qwen 3.5 descartado (0/5 tests).",
        "origen": "DEC-001",
        "gate": "DEC",
        "knowledge_type": "activo"
    },
    {
        "id": "FATAL-glm-multi",
        "condition": lambda q: "glm" in q.lower() and (
            q.count("1.") + q.count("2.") + q.count("3.") >= 3 or q.count("\n") > 6),
        "action": "block",
        "reason": "Anti-patron FATAL: multi-instruccion a GLM → content vacio.",
        "origen": "anti-patterns/catalogo.md (linea 20)",
        "gate": "FATAL",
        "knowledge_type": "activo"
    },
    {
        "id": "FATAL-deepseek-tokens",
        "condition": lambda q: "deepseek" in q.lower() and "max_tokens" in q.lower() and
                              any(str(n) in q for n in [512, 768, 1024]),
        "action": "warn",
        "reason": "DeepSeek R1 necesita max_tokens >= 2048.",
        "origen": "anti-patterns/catalogo.md (linea 18)",
        "gate": "FATAL",
        "knowledge_type": "activo"
    },
    {
        "id": "FATAL-llama-texto",
        "condition": lambda q: "llama" in q.lower() and any(w in q.lower() for w in 
                              ["conversacion", "texto", "dialogo", "relato", "historia"]),
        "action": "block",
        "reason": "Anti-patron FATAL: Llama 3.1 responde con function calls, no texto.",
        "origen": "anti-patterns/catalogo.md (linea 22)",
        "gate": "FATAL",
        "knowledge_type": "activo"
    },
    
    # ─── ACTIVAR MODULOS (DEC + POLICY) ───
    {
        "id": "AUTO-prompt-project",
        "condition": lambda q: bool(
            re.search(r'(?:genera|crea|escribe|haz|dame)\s+(?:un\s+)?prompt\s+(?:para|con)\s+', q.lower())
        ),
        "action": "activate",
        "module": "prompt_project",
        "reason": "Prompt Project detectado (generacion de prompt para modelo).",
        "origen": "skill:prompt-engineering",
        "gate": "POLICY",
        "knowledge_type": "activo"
    },
    {
        "id": "AUTO-decision-router",
        "condition": lambda q: any(w in q.lower() for w in 
            ["que modelo", "cual uso", "recomiendas", "elige"]),
        "action": "activate",
        "module": "decision_router",
        "reason": "La consulta requiere seleccion de modelo.",
        "origen": "pipeline estandar",
        "gate": "POLICY",
        "knowledge_type": "activo"
    },
    
    # ─── INYECTAR (DEC activas) ───
    {
        "id": "INJECT-granite-json",
        "condition": lambda q: "json" in q.lower() and "granite" in q.lower(),
        "action": "inject",
        "content": "⚠ Granite 4.1: temp=0.3 para JSON puro, temp=0.7 lo envuelve en markdown.",
        "reason": "EXP-20260728-002 (T3): JSON valido pero envuelto en markdown.",
        "origen": "EXP-20260728-002",
        "gate": "DEC",
        "knowledge_type": "activo"
    },
    {
        "id": "INJECT-gemma-lento",
        "condition": lambda q: "gemma" in q.lower() and "rapido" not in q.lower(),
        "action": "inject",
        "content": "⚠ Gemma 4: lento (151s). Alternativa rapida: Granite 4.1 (5-15s).",
        "reason": "DEC-003: calidad > velocidad. Usuario debe saberlo.",
        "origen": "DEC-003",
        "gate": "DEC",
        "knowledge_type": "activo"
    },
    
    # ─── SELECCIONAR MODELO (DEC) ───
    {
        "id": "MODEL-json",
        "condition": lambda q: "json" in q.lower() and not any(
            m in q.lower() for m in ["gemma", "deepseek", "granite", "llama", "dolphin", "glm", "qwen"]),
        "action": "select_model",
        "model": "granite-4.1-8b",
        "params": {"temperature": 0.3, "max_tokens": 1024},
        "reason": "Granite 4.1 temp=0.3 → JSON puro sin markdown (5-15s).",
        "origen": "EXP-20260728-002",
        "gate": "DEC",
        "knowledge_type": "activo"
    },
    {
        "id": "MODEL-creatividad",
        "condition": lambda q: any(w in q.lower() for w in ["creativo", "relato", "poema"]) and
                              not any(m in q.lower() for m in ["gemma", "deepseek", "granite", "llama", "dolphin", "glm", "qwen"]),
        "action": "select_model",
        "model": "google/gemma-4-12b-qat",
        "params": {"temperature": 0.7, "max_tokens": 2048},
        "reason": "DEC-003: Gemma 4 para creatividad (calidad maxima).",
        "origen": "DEC-003",
        "gate": "DEC",
        "knowledge_type": "activo"
    },
    {
        "id": "MODEL-razonamiento",
        "condition": lambda q: any(w in q.lower() for w in ["razona", "paso a paso"]) and
                              not any(m in q.lower() for m in ["gemma", "deepseek", "granite", "llama", "dolphin", "glm", "qwen"]),
        "action": "select_model",
        "model": "deepseek-r1-distill-qwen-14b",
        "params": {"temperature": 0.3, "max_tokens": 2048},
        "reason": "DEC-002: DeepSeek R1 para razonamiento.",
        "origen": "DEC-002",
        "gate": "DEC",
        "knowledge_type": "activo"
    },
]

# ═══════════════════════════════════════════════════
# DETECTOR DE TIPO DE TAREA (para checklist)
# ═══════════════════════════════════════════════════

def detect_task_type(query: str) -> str:
    """Detecta tipo de tarea usando task_keywords.yaml (fuente unica)."""
    q = query.lower()
    
    # Cargar desde YAML
    import yaml
    kw_path = os.path.join(LAB_DIR, "01-knowledge", "task_keywords.yaml")
    try:
        with open(kw_path) as f:
            data = yaml.safe_load(f)
        task_types = data.get("task_types", {})
    except Exception:
        task_types = {}
    
    for task_name, config in task_types.items():
        for kw in config.get("keywords", []):
            if kw in q:
                return task_name
    
    return "general"

# ═══════════════════════════════════════════════════
# ACTION LAYER — Motor central
# ═══════════════════════════════════════════════════

def _procesar_reglas_engine(active_rules: list) -> tuple[list, dict | None]:
    """Procesa reglas del Activation Engine (prioridad maxima)."""
    blocks = []
    model_selection = None
    for ar in active_rules:
        rule_id = ar.get("id", "RULE-?")
        origen = ar.get("origen", "?")
        prioridad = ar.get("prioridad", 50)
        
        accion = ar.get("accion", {})
        if isinstance(accion, dict):
            if accion.get("accion") == "block":
                blocks.append({
                    "id": rule_id,
                    "condition": lambda q: True,
                    "action": "block",
                    "reason": ar.get("desc", accion.get("razon", "")),
                    "origen": origen,
                    "gate": "RULE",
                    "knowledge_type": "activo"
                })
            elif "modelo" in accion:
                if not model_selection or prioridad > model_selection.get("prioridad", 0):
                    model_selection = {
                        "id": rule_id,
                        "condition": lambda q: True,
                        "action": "select_model",
                        "model": accion["modelo"],
                        "params": accion.get("params", {"temperature": 0.5, "max_tokens": 1024}),
                        "reason": ar.get("desc", ""),
                        "origen": origen,
                        "gate": "RULE",
                        "knowledge_type": "activo",
                        "prioridad": prioridad
                    }
    return blocks, model_selection

def _procesar_regla_hardcodeada(rule: dict, query: str) -> str | None:
    """Evalua una regla hardcodeada y devuelve el tipo de accion o None."""
    try:
        if not rule["condition"](query):
            return None
    except Exception:
        return None
    
    kt = rule.get("knowledge_type", "pasivo")
    if kt != "activo":
        return None
    
    return rule["action"]

def _aplicar_accion(accion: str, rule: dict, blocks, activations, injections, model_selection, warnings):
    """Aplica una acción de regla a las listas correspondientes.
    Devuelve model_selection (posiblemente actualizado)."""
    if accion == "block":
        blocks.append(rule)
    elif accion == "activate":
        activations.append(rule)
    elif accion == "inject":
        injections.append(rule)
    elif accion == "select_model" and not model_selection:
        model_selection = rule
    elif accion == "warn":
        warnings.append(rule)
    return model_selection


def _procesar_reglas_hardcodeadas(query, blocks, activations, injections, model_selection, warnings):
    """Procesa las reglas hardcodeadas de compatibilidad (RULES global)."""
    for rule in RULES:
        accion = _procesar_regla_hardcodeada(rule, query)
        if accion is None:
            continue
        model_selection = _aplicar_accion(accion, rule, blocks, activations,
                                          injections, model_selection, warnings)
    return model_selection


def _construir_resultado(query, task_type, checklist, blocks, activations, injections, model_selection, warnings) -> dict:
    """Construye el dict de resultado de evaluate()."""
    return {
        "query": query,
        "task_type": task_type,
        "checklist": checklist,
        "blocked": len(blocks) > 0,
        "blocks": blocks,
        "activations": activations,
        "injections": injections,
        "model_selection": model_selection,
        "warnings": warnings,
        "rules_triggered": len(blocks) + len(activations) + len(injections) + len(warnings) + (1 if model_selection else 0)
    }


def evaluate(query: str, active_rules: list = None) -> dict:
    """Evalua la consulta contra reglas activas.
    
    Args:
        query: consulta del usuario
        active_rules: reglas pre-activadas desde Activation Engine (opcional)
    """
    task_type = detect_task_type(query)
    checklist = TASK_CHECKLISTS.get(task_type, {})
    
    blocks = []
    activations = []
    injections = []
    model_selection = None
    warnings = []
    
    # 1. Procesar reglas del Activation Engine (prioridad máxima)
    blocks, model_selection = _procesar_reglas_engine(active_rules or [])
    
    # 2. Procesar reglas hardcodeadas existentes (compatibilidad)
    model_selection = _procesar_reglas_hardcodeadas(query, blocks, activations,
                                                    injections, model_selection, warnings)
    
    return _construir_resultado(query, task_type, checklist, blocks, activations,
                                injections, model_selection, warnings)

def evaluate_with_activation(query: str) -> dict:
    """Pipeline completo: Activation Engine → Decision Engine.
    Entrada unica para el pipeline Joko Lab."""
    task_type = detect_task_type(query)
    
    # Paso 1: Activation Engine busca RULE activas
    sys.path.insert(0, TOOL_DIR)
    try:
        from activation_engine import activate as ae_activate
        activation = ae_activate(task_type, query)
    except Exception as e:
        activation = {"total_active": 0, "active_rules": [], "blocks": [], "model_selection": None, "error": str(e)}
    
    # Paso 2: Extraer reglas activas para el Decision Engine
    active_rules = activation.get("active_rules", [])
    if activation.get("model_selection"):
        active_rules = [activation["model_selection"]] + active_rules
    active_rules = activation.get("blocks", []) + active_rules
    
    # Paso 3: Decision Engine aplica reglas
    result = evaluate(query, active_rules)
    result["activation"] = activation
    return result

def _cabecera_output(result: dict) -> list[str]:
    lines = []
    lines.append("═══════════════════════════════════════════")
    lines.append("  ACTION LAYER v2 — Decision Engine")
    lines.append("═══════════════════════════════════════════")
    lines.append(f"  Tarea: {result['task_type'].upper()}")
    lines.append(f"  Reglas disparadas: {result['rules_triggered']}")
    lines.append("")
    return lines


def _seccion_checklist(cl: dict) -> list[str]:
    lines = []
    lines.append(f"── CHECKLIST OBLIGATORIA: {cl.get('name', '')} ──")
    for item in cl.get("mandatory", []):
        lines.append(f"  □ {item['desc']}")
    for item in cl.get("recommended", []):
        lines.append(f"  ○ {item['desc']} (recomendado)")
    lines.append("")
    return lines


def _seccion_bloqueos(blocks: list) -> list[str]:
    lines = []
    lines.append("── 🚫 BLOQUEADO ──")
    for b in blocks:
        lines.append(f"  ❌ {b['id']} [{b.get('gate','?')}]")
        lines.append(f"     {b['reason']}")
        lines.append(f"     Origen: {b['origen']}")
    lines.append("")
    return lines


def _seccion_activaciones(activations: list) -> list[str]:
    lines = []
    lines.append("── ▶ MODULOS ACTIVADOS ──")
    for a in activations:
        lines.append(f"  → {a['module']} [{a.get('gate','?')}]")
        lines.append(f"    {a['reason']}")
    lines.append("")
    return lines


def _seccion_inyecciones(injections: list) -> list[str]:
    lines = []
    lines.append("── 💉 RESTRICCIONES INYECTADAS ──")
    for i in injections:
        lines.append(f"  ⚠ {i['content']}")
        lines.append(f"    Origen: {i['origen']} [{i.get('gate','?')}]")
    lines.append("")
    return lines


def _seccion_modelo(m: dict) -> list[str]:
    lines = []
    lines.append("── 🎯 MODELO SELECCIONADO ──")
    lines.append(f"  {m['model']} [{m.get('gate','?')}]")
    lines.append(f"  temp={m['params']['temperature']}, max_tokens={m['params']['max_tokens']}")
    lines.append(f"  {m['reason']}")
    lines.append(f"  Origen: {m['origen']}")
    lines.append("")
    return lines


def _seccion_avisos(warnings: list) -> list[str]:
    lines = []
    lines.append("── ⚠ AVISOS ──")
    for w in warnings:
        lines.append(f"  {w['reason']}")
    lines.append("")
    return lines


def format_output(result: dict) -> str:
    lines = _cabecera_output(result)

    # ── CHECKLIST ──
    cl = result.get("checklist", {})
    if cl:
        lines += _seccion_checklist(cl)

    # ── ACCIONES ──
    if result["blocks"]:
        lines += _seccion_bloqueos(result["blocks"])

    if result["activations"]:
        lines += _seccion_activaciones(result["activations"])

    if result["injections"]:
        lines += _seccion_inyecciones(result["injections"])

    if result["model_selection"]:
        lines += _seccion_modelo(result["model_selection"])

    if result["warnings"]:
        lines += _seccion_avisos(result["warnings"])

    if not result["blocks"] and not result["activations"] and not result["model_selection"]:
        lines.append("  Sin reglas activas para esta consulta.")
        lines.append(f"  Tipo de tarea: {result.get('task_type', 'general')} → checklist minimo.")

    lines.append("═══════════════════════════════════════════")
    return "\n".join(lines)

if __name__ == "__main__":
    if not sys.stdin.isatty():
        query = sys.stdin.read().strip()
    elif len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        print("Uso: echo 'objetivo' | python3 decision_engine.py")
        sys.exit(1)
    
    result = evaluate_with_activation(query)
    print(format_output(result))
