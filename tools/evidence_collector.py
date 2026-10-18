#!/usr/bin/env python3
"""evidence_collector.py - Decide si un resultado tiene suficiente evidencia

Se coloca entre el Evaluator-Optimizer y el laboratorio para decidir
si registrar conocimiento nuevo. Solo registra si:
- El resultado es E3 (3+ condiciones distintas) O
- Se ha repetido N veces con exito O
- El impacto es medible y positivo

Uso:
  echo '{"score_final": 83, "rounds": 2, "improvement": 45}' | python3 evidence_collector.py
"""
import os, sys, json, yaml
from datetime import datetime
from pathlib import Path

LAB_DIR = os.path.expanduser("~/joko-lab")

# Umbrales de evidencia
THRESHOLDS = {
    "min_rounds_for_decision": 2,   # Minimo de rondas exitosas para registrar decision
    "min_improvement_pct": 20,      # Mejora minima (%) para considerar registro
    "min_observations_for_pattern": 3,  # Observaciones para crear patron (E3)
    "max_confidence_for_register": 90,  # Confianza minima para Decision Memory
}

def _accion_observacion(score_inicial, score_final, rounds) -> dict:
    return {
        "type": "observation",
        "file": "01-knowledge/experiments/prompt-experiments.md",
        "message": f"Mejora de {score_inicial}% a {score_final}% en {rounds} rondas"
    }


def _accion_hipotesis(improvement, rounds) -> dict:
    return {
        "type": "hypothesis",
        "file": "01-knowledge/patterns/",
        "message": f"Patron de mejora: el tipo de prompt mejora un {improvement}% con {rounds} rondas"
    }


def _accion_e3_candidato() -> dict:
    return {
        "type": "e3_candidate",
        "file": "04-operations/metrics/",
        "message": "Candidato a E3: verificar si hay 3+ observaciones independientes"
    }


def _calcular_improvement(result: dict, score_final, score_inicial) -> int:
    """Calcula el improvement si no viene dado."""
    improvement = result.get("improvement", 0)
    if not improvement and score_inicial > 0:
        return int(((score_final - score_inicial) / max(score_inicial, 1)) * 100)
    return improvement


def _nivel_evidencia(passed, improvement, rounds) -> str:
    """Determina el nivel de evidencia (ninguna/E1/E2)."""
    if passed and improvement >= THRESHOLDS["min_improvement_pct"] and rounds >= THRESHOLDS["min_rounds_for_decision"]:
        return "E2"
    if passed and improvement > 0:
        return "E1"
    return "ninguna"


def _next_step(evidence_level: str) -> str:
    """Siguiente paso según el nivel de evidencia."""
    if evidence_level == "E2":
        return "Ejecutar manualmente 2 experimentos mas en condiciones distintas para validar E3"
    if evidence_level == "E1":
        return "Esperar mas evidencia"
    return "Sin evidencia suficiente"


def evaluate_evidence(result: dict) -> dict:
    """Evalua si un resultado merece registrarse como conocimiento"""
    score_final = result.get("final_score", result.get("score_final", 0))
    score_inicial = result.get("initial_score", result.get("score_inicial", 0))
    rounds = result.get("total_rounds", result.get("rounds", 1))
    improvement = _calcular_improvement(result, score_final, score_inicial)
    
    passed = result.get("passed", score_final >= 80)
    
    # Evaluar si merece registro
    evidence_level = _nivel_evidencia(passed, improvement, rounds)
    actions = []
    
    # Nivel E1: mejora puntual
    if evidence_level == "E1":
        actions.append(_accion_observacion(score_inicial, score_final, rounds))
    
    # Nivel E2: mejora significativa con evidencia
    if evidence_level == "E2":
        actions.append(_accion_hipotesis(improvement, rounds))
        # E3: requiere 3 observaciones independientes (se verifica con el historico)
        # Aqui consultariamos el historico de metricas para ver si hay 3+
        # Por ahora, marcamos como candidato a E3
        actions.append(_accion_e3_candidato())
    
    return {
        "evidence_level": evidence_level,
        "should_register": evidence_level in ("E2", "E3"),
        "improvement": improvement,
        "actions": actions,
        "next_step": _next_step(evidence_level)
    }

def format_output(eval_result: dict) -> str:
    lines = []
    lines.append("══ EVIDENCE COLLECTOR ══")
    lines.append(f"  Nivel de evidencia: {eval_result['evidence_level']}")
    lines.append(f"  Mejora detectada:   {eval_result['improvement']}%")
    lines.append(f"  Registro automatico: {'SI' if eval_result['should_register'] else 'NO'}")
    lines.append("")
    
    if eval_result["actions"]:
        lines.append("  Acciones propuestas:")
        for a in eval_result["actions"]:
            lines.append(f"  [{a['type']}] → {a['file']}")
            lines.append(f"    {a['message']}")
    
    lines.append(f"  Siguiente paso: {eval_result['next_step']}")
    lines.append("══════════════════")
    return "\n".join(lines)

if __name__ == "__main__":
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
    elif len(sys.argv) > 1:
        raw = " ".join(sys.argv[1:])
    else:
        print("Uso: echo '{\"score_final\":83,...}' | python3 evidence_collector.py")
        sys.exit(1)
    
    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        try:
            result = yaml.safe_load(raw)
        except Exception:
            print("Error: entrada no es JSON/YAML valido")
            sys.exit(1)
    
    eval_result = evaluate_evidence(result)
    print(format_output(eval_result))
