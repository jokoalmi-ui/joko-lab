#!/usr/bin/env python3
"""evaluator_optimizer.py - Bucle adversarial de mejora de prompts

Patron 4: Un agente evaluador critica un prompt contra una rubrica.
Un agente optimizador reescribe el prompt segun la critica.
Bucle hasta superar umbral o alcanzar maximo de iteraciones.

Uso:
  echo "prompt a mejorar" | python3 evaluator_optimizer.py
  python3 evaluator_optimizer.py "prompt a mejorar" --max-rounds 5
"""
import os, sys, json, subprocess, re
from pathlib import Path
import yaml

VENV_PYTHON = os.path.expanduser("~/.venv/hermes-rag/bin/python3")
LMSTUDIO_API = "http://localhost:1234/v1/chat/completions"
TOOL_DIR = os.path.expanduser("~/joko-lab/tools")

# Cargar rubrica desde YAML (v2)
def load_rubric() -> dict:
    rubric_path = os.path.join(TOOL_DIR, "evaluator_rubric.yaml")
    with open(rubric_path) as f:
        return yaml.safe_load(f)

RUBRIC_CFG = load_rubric()

# Construir funciones de check desde la config YAML
def build_checks(cfg):
    checks = []
    for rule in cfg["rules"]:
        rule_id = rule["id"]
        rule_desc = rule["desc"]
        rule_weight = rule.get("weight", 1)
        params = rule.get("params", {})
        rtype = rule.get("type", "keyword")
        
        if rtype == "length":
            min_len = params.get("min", 50)
            checks.append({
                "id": rule_id, "desc": rule_desc, "weight": rule_weight,
                "check": lambda p, m=min_len: len(p) > m
            })
        elif rtype == "complexity":
            max_nl = params.get("max_newlines", 10)
            max_and = params.get("max_and", 3)
            checks.append({
                "id": rule_id, "desc": rule_desc, "weight": rule_weight,
                "check": lambda p, nl=max_nl, ma=max_and: p.count("\n") < nl and p.count(" y ") < ma
            })
        elif rtype == "keyword":
            keywords = params.get("keywords", [])
            checks.append({
                "id": rule_id, "desc": rule_desc, "weight": rule_weight,
                "check": lambda p, kw=keywords: any(w in p.lower() for w in kw)
            })
    return checks

RUBRIC = build_checks(RUBRIC_CFG)
THRESHOLD = RUBRIC_CFG.get("threshold", 0.8)
MAX_ROUNDS = RUBRIC_CFG.get("max_rounds", 5)

def call_llm(system: str, prompt: str, model: str = "granite-4.1-8b", max_tokens: int = 1024) -> str:
    """Llama a un modelo local via LM Studio"""
    import urllib.request
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "max_tokens": max_tokens,
        "stream": False
    }
    req = urllib.request.Request(
        LMSTUDIO_API,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read())
            return result.get('choices',[{}])[0].get('message',{}).get('content','')
    except Exception as e:
        return f"[Error LLM: {e}]"

def evaluate_prompt(prompt: str) -> dict:
    """Evalua un prompt contra la rubrica ponderada + verificacion semantica"""
    results = []
    score = 0
    max_score = sum(r["weight"] for r in RUBRIC)
    
    for rule in RUBRIC:
        passed = rule["check"](prompt)
        results.append({
            "id": rule["id"],
            "desc": rule["desc"],
            "weight": rule["weight"],
            "passed": passed
        })
        if passed:
            score += rule["weight"]
    
    # Verificacion semantica: contradicciones, peticiones imposibles
    semantic_warnings = _check_semantics(prompt)
    
    return {
        "score": score,
        "max_score": max_score,
        "percentage": int((score / max_score) * 100) if max_score > 0 else 0,
        "results": results,
        "semantic_warnings": semantic_warnings,
        "passed": (score / max_score) >= THRESHOLD if max_score > 0 else False
    }

def _check_semantics(prompt: str) -> list:
    """Verifica contradicciones semanticas y peticiones imposibles"""
    warnings = []
    p = prompt.lower()
    
    # Cargar checks semanticos de YAML
    semantic = RUBRIC_CFG.get("semantic_checks", {})
    
    # Contradicciones
    for pair in semantic.get("contradictions", []):
        if len(pair) == 2 and pair[0] in p and pair[1] in p:
            warnings.append(f"Posible contradiccion: '{pair[0]}' vs '{pair[1]}'")
    
    # Peticiones imposibles
    for phrase in semantic.get("impossible_requests", []):
        if phrase in p:
            warnings.append(f"Peticion imposible detectada: '{phrase}'")
    
    # Riesgo de perdida de informacion
    loss_keywords = semantic.get("information_loss_risk", {}).get("keywords", [])
    for kw in loss_keywords:
        if kw in p:
            warnings.append(f"Riesgo de cambio de significado detectado")
            break
    
    return warnings

def _consultar_seccion(consulta: str, etiqueta: str) -> str:
    """Consulta RAG y devuelve el bloque etiquetado, o '' si vacío."""
    ctx = _run_context_builder(consulta)
    if not ctx:
        return ""
    return f"[{etiqueta}]\n{ctx}\n[/{etiqueta}]"


def _consultar_antipatrones(cfg, prompt, model, knowledge) -> None:
    """Bloque anti-patrones: consulta RAG y añade el bloque si hay contexto."""
    if cfg.get("anti_patterns", True):
        ctx = _consultar_seccion(f"anti patrones prompt {model} " + prompt[:50], "Anti-patrones")
        if ctx:
            knowledge.append(ctx)


def _consultar_ficha_modelo(cfg, model, knowledge) -> None:
    """Bloque ficha de modelo: consulta RAG y añade el bloque si hay contexto."""
    if cfg.get("model_cards", True) and model:
        ctx = _consultar_seccion(f"ficha modelo {model} parametros recomendados", "Ficha modelo")
        if ctx:
            knowledge.append(ctx.replace("[/Ficha modelo]", "[/Ficha]"))


def _consultar_decisiones(cfg, model, knowledge) -> None:
    """Bloque decisiones: consulta RAG y añade el bloque si hay contexto."""
    if cfg.get("decisions", True):
        ctx = _consultar_seccion(f"decision sobre {model if model else 'modelos'}", "Decisiones")
        if ctx:
            knowledge.append(ctx)


def _integrate_lab_knowledge(prompt: str, model: str = "") -> str:
    """Consulta el laboratorio (anti-patrones, fichas, decisiones) y devuelve contexto"""
    cfg = RUBRIC_CFG.get("integrate_lab", {})
    if not cfg.get("enabled", False):
        return ""
    
    knowledge = []
    _consultar_antipatrones(cfg, prompt, model, knowledge)
    _consultar_ficha_modelo(cfg, model, knowledge)
    _consultar_decisiones(cfg, model, knowledge)
    return "\n".join(knowledge) if knowledge else ""

def _run_context_builder(query: str) -> str:
    """Ejecuta context_builder.py y devuelve solo el contenido relevante"""
    try:
        ctx_script = os.path.join(TOOL_DIR, "context_builder.py")
        result = subprocess.run(
            [sys.executable, ctx_script],
            input=query, capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0:
            output = result.stdout
            # Limpiar prefijos de contexto
            output = re.sub(r'^\[Contexto RAG\]\s*', '', output)
            output = re.sub(r'\[/?Contexto\]', '', output)
            return output.strip()[:1500]
    except Exception:
        pass
    return ""

def critic_llm(prompt: str, eval_result: dict) -> str:
    """Usa un LLM como critico avanzado (analisis semantico)"""
    failures = [r for r in eval_result["results"] if not r["passed"]]
    if not failures:
        return "El prompt cumple todos los criterios."
    
    failures_text = "\n".join([f"- {r['desc']}" for r in failures])
    system = "Eres un critico de prompts experto. Senala problemas concretos y sugiere mejoras especificas."
    critique = f"""Evalua este prompt y genera una critica constructiva.

Prompt a evaluar:
---
{prompt}
---

Problemas detectados automaticamente:
{failures_text}

Genera una critica que:
1. Explique POR QUE cada problema es un problema
2. Sugiera cambios CONCRETOS (no genericos)
3. Indique que mantener del prompt original

Critica:"""
    
    return call_llm(system, critique, max_tokens=512)

def optimize_llm(prompt: str, critique: str) -> str:
    """Usa un LLM para reescribir el prompt segun la critica"""
    system = "Eres un optimizador de prompts. Reescribes prompts siguiendo las criticas recibidas. Conservas la intencion original pero mejoras la claridad y estructura."
    
    optimize_prompt = f"""Reescribe este prompt para solucionar los problemas indicados en la critica.

Prompt original:
---
{prompt}
---

Critica recibida:
---
{critique}
---

Instrucciones:
- Conserva el proposito original del prompt
- Corrige SOLO los problemas mencionados
- No anyadas informacion que no estaba en el original
- Devuelve SOLO el prompt reescrito, sin explicaciones

Prompt mejorado:"""
    
    return call_llm(system, optimize_prompt, max_tokens=1024)

def _calcular_similitud(resp1: str, resp2: str) -> tuple:
    """Devuelve (same_exact, same_first_100, jaccard, same)."""
    same_exact = (resp1.strip() == resp2.strip())
    same_first_100 = (resp1.strip()[:100] == resp2.strip()[:100])
    words1 = set(resp1.lower().split())
    words2 = set(resp2.lower().split())
    jaccard = (len(words1 & words2) / len(words1 | words2)) if (words1 | words2) else 0
    same = same_exact or (same_first_100 and jaccard > 0.9)
    return same_exact, same_first_100, jaccard, same


def _metricas_estructura(resp: str) -> tuple:
    """Devuelve (len, has_structure)."""
    marcadores = ["json", "```", "##", "1.", "2."]
    return len(resp), any(w in resp.lower() for w in marcadores)


def evaluate_response(prompt1: str, prompt2: str, model: str = "granite-4.1-8b", 
                     max_tokens: int = 512) -> dict:
    """Ejecuta ambos prompts contra el modelo destino y compara respuestas.
    Devuelve cual es mejor y metricas.
    """
    sys_prompt = "Responde exactamente lo que pide el prompt. Sin explicaciones extras."
    
    # Ejecutar ambos prompts
    resp1 = call_llm(sys_prompt, prompt1, model, max_tokens)
    resp2 = call_llm(sys_prompt, prompt2, model, max_tokens)
    
    # Verificar si son identicas o casi identicas (cosmetico)
    same_exact, same_first_100, jaccard, same = _calcular_similitud(resp1, resp2)
    
    # Metricas de estructura
    len1, has_structure_1 = _metricas_estructura(resp1)
    len2, has_structure_2 = _metricas_estructura(resp2)
    
    # Puntuacion: mas largo + mas estructura = mejor (simplificado)
    score1 = len1 * (2 if has_structure_1 else 1)
    score2 = len2 * (2 if has_structure_2 else 1)
    
    return {
        "same": same,
        "same_exact": same_exact,
        "jaccard_similarity": round(jaccard, 3),
        "len1": len1, "len2": len2,
        "structure1": has_structure_1, "structure2": has_structure_2,
        "score1": score1, "score2": score2,
        "winner": "prompt1" if score1 > score2 else "prompt2" if score2 > score1 else "empate",
        "improvement": int(((score2 - score1) / max(score1, 1)) * 100) if score1 > 0 else 0,
        "response1_preview": resp1[:200],
        "response2_preview": resp2[:200]
    }

def _build_critique(current: str, eval_result: dict) -> str:
    """Genera la critica: automatica si hay pocos fallos, LLM si son complejos"""
    # 3. Criticar (con LLM si hay fallos complejos, o automatico si son pocos)
    failures = [r for r in eval_result["results"] if not r["passed"]]
    if len(failures) <= 2:
        # Critica automatica simple
        critique = "Problemas:\n" + "\n".join([f"- {r['desc']}" for r in failures])
    else:
        critique = critic_llm(current, eval_result)
    return critique

def _run_optimization_loop(prompt: str, max_rounds: int) -> tuple[list, str]:
    """Bucle de rondas: evaluar -> criticar -> optimizar. Devuelve (history, current)"""
    history = []
    current = prompt
    
    for round_num in range(1, max_rounds + 1):
        # 1. Evaluar
        eval_result = evaluate_prompt(current)
        
        round_data = {
            "round": round_num,
            "prompt": current,
            "score": eval_result["percentage"],
            "eval": eval_result
        }
        
        # 2. Si pasa el umbral, terminar
        if eval_result["passed"]:
            round_data["status"] = "APROBADO"
            round_data["critique"] = ""
            round_data["optimized"] = ""
            history.append(round_data)
            break
        
        # 3. Criticar (con LLM si hay fallos complejos, o automatico si son pocos)
        critique = _build_critique(current, eval_result)
        
        round_data["critique"] = critique
        
        # 4. Optimizar
        improved = optimize_llm(current, critique)
        round_data["optimized"] = improved
        
        # 5. Verificar que no empeoro
        if improved == current or len(improved) < 10:
            round_data["status"] = "ESTANCADO"
            history.append(round_data)
            break
        
        current = improved
        round_data["status"] = "MEJORADO"
        history.append(round_data)
    
    return history, current

def _apply_gate(prompt: str, current: str, model: str) -> tuple[str, bool, object]:
    """GATE: verifica contra el modelo destino que la mejora no sea cosmetica"""
    # ─── GATE: Verificacion contra modelo destino ───────────
    response_eval = None
    if prompt != current and model:
        try:
            response_eval = evaluate_response(prompt, current, model)
        except Exception:
            pass
    
    # Si la respuesta real no mejoro, la optimizacion fue COSMETICA
    # y la rechazamos (volvemos al original)
    # GATE fail-closed: si no hay verificacion, rechazar por defecto
    final = prompt   # Default: rechazar (fail-closed)
    cosmetic = True  # Default: no confiar sin evidencia
    
    if response_eval:
        same = response_eval.get("same") is True
        worse = response_eval.get("improvement", 0) < 0
        
        if not same and not worse:
            # Hay evidencia positiva de mejora → aceptar
            final = current
            cosmetic = False
    
    return final, cosmetic, response_eval

def improve_prompt(prompt: str, max_rounds: int = None, threshold: float = None, model: str = "") -> dict:
    """Bucle principal: evaluar -> criticar -> optimizar -> repetir"""
    if max_rounds is None:
        max_rounds = MAX_ROUNDS
    if threshold is None:
        threshold = THRESHOLD
    
    # Integrar conocimiento del laboratorio
    lab_context = _integrate_lab_knowledge(prompt, model)
    
    history, current = _run_optimization_loop(prompt, max_rounds)
    final, cosmetic, response_eval = _apply_gate(prompt, current, model)
    
    return {
        "original": prompt,
        "final": final,
        "accepted": final != prompt,
        "cosmetic_rejected": cosmetic,
        "total_rounds": len(history),
        "initial_score": history[0]["score"] if history else 0,
        "final_score": history[-1]["score"] if history else 0,
        "passed": history[-1]["eval"]["passed"] if history else False,
        "history": history,
        "response_eval": response_eval
    }

def _cabecera_informe(result: dict) -> list[str]:
    lines = []
    lines.append("═══════════════════════════════════════════")
    lines.append("  EVALUATOR-OPTIMIZER v2 — Informe")
    lines.append("═══════════════════════════════════════════")
    lines.append(f"  Prompt original: {result['original'][:80]}...")
    lines.append(f"  Puntuacion inicial: {result['initial_score']}%")
    lines.append(f"  Puntuacion final:   {result['final_score']}%")
    lines.append(f"  Rondas: {result['total_rounds']}")
    lines.append(f"  Estado: {'✅ APROBADO' if result['passed'] else '❌ NO PASO EL UMBRAL'}")
    lines.append("")
    return lines

def _seccion_historia(result: dict) -> list[str]:
    lines = []
    for h in result["history"]:
        status_icon = "✅" if h["status"] == "APROBADO" else "🔄" if h["status"] == "MEJORADO" else "⏹"
        lines.append(f"  Ronda {h['round']} [{status_icon}] Score: {h['score']}%")
        
        # Mostrar warnings semanticos
        eval_data = h.get("eval", {})
        warnings = eval_data.get("semantic_warnings", [])
        if warnings:
            for w in warnings:
                lines.append(f"    ⚠ {w}")
        
        if h.get("critique"):
            crit_lines = h["critique"].strip().split("\n")
            for cl in crit_lines[:3]:
                lines.append(f"    ├ {cl[:100]}")
        
        if h.get("optimized"):
            lines.append(f"    └ Prompt: {h['optimized'][:100]}...")
        lines.append("")
    return lines

def _seccion_gate(result: dict) -> list[str]:
    lines = []
    # Mostrar comparacion de respuestas reales
    resp_eval = result.get("response_eval")
    if resp_eval:
        lines.append("")
        lines.append("── GATE: RESPUESTA CONTRA MODELO DESTINO ──")
        if resp_eval.get("same") is True:
            lines.append("  ❌ OPTIMIZACION RECHAZADA (cosmetica)")
            lines.append("  Motivo: El prompt mejorado produce EXACTAMENTE la misma respuesta.")
            lines.append("  La mejora en la rubrica no se traduce en mejora real.")
        elif resp_eval.get("improvement", 0) < 0:
            lines.append("  ❌ OPTIMIZACION RECHAZADA (empeoro)")
            lines.append(f"  Motivo: La respuesta empeoro un {abs(resp_eval['improvement'])}%")
        elif result.get("cosmetic_rejected"):
            lines.append("  ❌ OPTIMIZACION RECHAZADA")
        else:
            lines.append("  ✅ OPTIMIZACION ACEPTADA (mejora real)")
            lines.append(f"  Mejora: {resp_eval['improvement']}% (score)")
            lines.append(f"  Original:  {resp_eval['len1']} chars" + (" [estructurado]" if resp_eval['structure1'] else ""))
            lines.append(f"  Mejorado:  {resp_eval['len2']} chars" + (" [estructurado]" if resp_eval['structure2'] else ""))
    return lines

def format_report(result: dict) -> str:
    """Formatea el resultado del bucle de mejora"""
    lines = _cabecera_informe(result) + _seccion_historia(result)
    
    if result["passed"]:
        lines.append("  Prompt final optimizado:")
        lines.append(f"  {result['final'][:300]}")
    
    lines += _seccion_gate(result)
    lines.append("═══════════════════════════════════════════")
    return "\n".join(lines)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Evaluator-Optimizer: mejora prompts por bucle adversarial")
    parser.add_argument("prompt", nargs="?", help="Prompt a mejorar")
    parser.add_argument("--max-rounds", type=int, default=5, help="Maximo de rondas de mejora")
    parser.add_argument("--threshold", type=float, default=0.8, help="Umbral de aprobacion (0-1)")
    parser.add_argument("--model", type=str, default="", help="Modelo destino para validar mejora real (ej: gemma-4-12b)")
    parser.add_argument("--validate", action="store_true", help="Ejecutar validacion completa contra modelo real")
    
    args = parser.parse_args()
    
    if args.prompt:
        prompt = args.prompt
    elif not sys.stdin.isatty():
        prompt = sys.stdin.read().strip()
    else:
        print("Uso: echo 'prompt' | python3 evaluator_optimizer.py [--model MODELO] [--validate]")
        sys.exit(1)
    
    # Si --validate sin --model, usar default
    model = args.model if args.model else ("granite-4.1-8b" if args.validate else "")
    
    result = improve_prompt(prompt, args.max_rounds, args.threshold, model)
    print(format_report(result))
    
    if args.validate and result.get("response_eval"):
        reval = result["response_eval"]
        if reval.get("same"):
            print(f"\n⚠ ADVERTENCIA: Mejora COSMETICA (Jaccard={reval.get('jaccard_similarity', '?')}). El prompt cambio pero la respuesta es casi identica.")
        else:
            print(f"\n✅ Mejora REAL confirmada (Jaccard={reval.get('jaccard_similarity', '?')}, mejora={reval.get('improvement', 0)}%)")
