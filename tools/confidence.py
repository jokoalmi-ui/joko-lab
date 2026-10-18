#!/usr/bin/env python3
"""confidence.py - Wrapper comun para anyadir confianza a cualquier componente

Cada componente del pipeline puede envolver su resultado con:
  result:    el resultado original
  confidence: 0-100%
  evidence:  fuentes que respaldan el resultado
  assumptions: que estamos asumiendo
"""
import os, json

def wrap(result: any, confidence: int, evidence: list = None, assumptions: list = None) -> dict:
    """Envuelve un resultado con metadatos de confianza"""
    return {
        "result": result,
        "confidence": confidence,
        "evidence": evidence or [],
        "assumptions": assumptions or []
    }

def from_sources(sources: list, weights: dict = None) -> int:
    """Calcula confianza basada en el peso de las fuentes consultadas.
    
    sources: lista de tipos de fuente (ej: ["experimento", "decision"])
    weights: pesos opcionales (default: los del knowledge_resolver)
    
    Returns: 0-100% de confianza
    """
    if not sources:
        return 20  # Sin fuentes, confianza minima
    
    default_weights = {
        "experimento": 10,
        "decision": 9,
        "benchmark": 8,
        "anti-patron": 7,
        "patron": 6,
        "skill": 5,
        "ficha modelo": 4,
        "auditoria": 3,
        "documentacion": 2,
        "sesion": 1,
    }
    w = weights or default_weights
    
    total = sum(w.get(s, 1) for s in sources)
    max_possible = len(sources) * 10
    confidence = int((total / max_possible) * 100) if max_possible > 0 else 20
    
    return min(confidence, 100)

def from_evidence_count(total_items: int, items_with_evidence: int) -> int:
    """Confianza basada en proporcion de items con evidencia"""
    if total_items == 0:
        return 10
    return int((items_with_evidence / total_items) * 100)

def merge(*confidences: dict) -> dict:
    """Combina multiples resultados con confianza en uno solo"""
    if not confidences:
        return wrap(None, 0)
    
    # Media de confianzas
    avg_conf = sum(c.get("confidence", 50) for c in confidences) // len(confidences)
    
    # Unir evidencias
    all_evidence = []
    for c in confidences:
        all_evidence.extend(c.get("evidence", []))
    
    # Unir supuestos
    all_assumptions = []
    for c in confidences:
        all_assumptions.extend(c.get("assumptions", []))
    
    return {
        "result": [c.get("result") for c in confidences],
        "confidence": avg_conf,
        "evidence": list(set(all_evidence)),
        "assumptions": list(set(all_assumptions))
    }

def format_badge(confidence: int) -> str:
    """Devuelve un badge visual de confianza"""
    if confidence >= 90:
        return f"🟢 {confidence}% — ALTA"
    elif confidence >= 60:
        return f"🟡 {confidence}% — MEDIA"
    elif confidence >= 30:
        return f"🟠 {confidence}% — BAJA"
    else:
        return f"🔴 {confidence}% — MINIMA"

# ── Conversión unificada label ↔ int (fuente única) ──
LABEL_TO_INT = {"ALTA": 90, "MEDIA": 60, "BAJA": 30, "MINIMA": 10}

def to_label(confidence: int) -> str:
    """Convierte valor numérico 0-100 a etiqueta estandar"""
    if confidence >= 90: return "ALTA"
    if confidence >= 60: return "MEDIA"
    if confidence >= 30: return "BAJA"
    return "MINIMA"

def from_label(label: str) -> int:
    """Convierte etiqueta estandar a valor numérico (default: 30 para BAJA)"""
    return LABEL_TO_INT.get(label.upper(), 30)

def stamp(result: dict, sources: list, extra_evidence: list = None) -> dict:
    """Añade campo confidence y evidence a cualquier resultado.
    Uso: return stamp({'modelo': 'gemma', 'params': {...}}, ['decision', 'experimento'])
    """
    conf_int = from_sources(sources)
    evidence = list(sources)
    if extra_evidence:
        evidence.extend(extra_evidence)
    result["confidence"] = conf_int
    result["confidence_label"] = to_label(conf_int)
    result["evidence"] = evidence
    return result

def trace(result: dict, knowledge: str, evidence: list, decision: str, proof: str = "") -> dict:
    """Añade trazabilidad completa a cualquier resultado de componente.
    
    Responde las 4 preguntas del Hardening Nivel 4:
      1. ¿Qué sabe? → knowledge
      2. ¿De dónde lo sabe? → evidence
      3. ¿Qué decisión toma? → decision
      4. ¿Cómo demuestra que era correcta? → proof
    
    Uso:
      return trace(
          {'modelo': 'gemma', 'params': {...}},
          knowledge='DEC-003: Gemma 4 para creatividad',
          evidence=['DEC-003', 'EXP-021', 'EXP-035'],
          decision='Seleccionar Gemma 4 con temp=0.7',
          proof='3 validaciones, 94% confianza'
      )
    """
    result["_trace"] = {
        "knowledge": knowledge,
        "evidence": evidence,
        "decision": decision,
        "proof": proof or "pendiente de verificación",
        "timestamp": datetime.now().isoformat()
    }
    # También añadir confidence estándar
    return stamp(result, evidence)
