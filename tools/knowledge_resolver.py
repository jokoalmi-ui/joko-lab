#!/usr/bin/env python3
"""knowledge_resolver.py - Sintetiza documentos en conocimiento estructurado

Entre el Context Builder y la respuesta final, esta capa transforma
documentos brutos en hechos, conflictos, hipotesis y decisiones activas.

Uso: python3 context_builder.py "pregunta" | python3 knowledge_resolver.py
     O: echo "pregunta" | python3 knowledge_resolver.py (busca automaticamente)
"""
import os, sys, json, re, subprocess
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Optional

# Confidence Engine
from confidence import wrap, from_sources, from_evidence_count, format_badge, stamp

# ─── Pesos de fuentes ─────────────────────────────────────
SOURCE_WEIGHTS = {
    "experimento":      10,  # Datos reales, reproducibles
    "decision":         9,   # Aprobada, con evidencia
    "benchmark":        8,   # Resultados cuantitativos
    "anti-patron":      7,   # Confirmado por experimentos
    "patron":           6,   # Validado por uso repetido
    "skill":            5,   # Conocimiento estructurado
    "ficha modelo":     4,   # Perfil documentado
    "auditoria":        3,   # Analisis externo
    "documentacion":    2,   # Notas, informes
    "codigo fuente":    1,   # Implementacion de referencia
    "sesion":           0,   # Conversacion sin estructura
}

@dataclass
class KnowledgeItem:
    type: str             # "hecho", "conflicto", "hipotesis", "decision", "accion"
    content: str          # Texto del conocimiento
    source: str           # Documento de origen
    source_type: str      # Tipo de fuente (experimento, decision, ...)
    confidence: str       # "ALTA", "MEDIA", "BAJA", "E3", "E2", "E1"
    weight: int = 0       # Peso computado
    evidence: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        if self.weight == 0:
            self.weight = SOURCE_WEIGHTS.get(self.source_type, 1)

@dataclass
class Synthesis:
    query: str = ""
    facts: List[KnowledgeItem] = field(default_factory=list)
    conflicts: List[KnowledgeItem] = field(default_factory=list)
    hypotheses: List[KnowledgeItem] = field(default_factory=list)
    decisions: List[KnowledgeItem] = field(default_factory=list)
    actions: List[KnowledgeItem] = field(default_factory=list)
    sources_consulted: List[str] = field(default_factory=list)

def extract_sources(raw_text: str) -> list:
    """Extrae nombres de fuentes del texto del context_builder"""
    sources = []
    # Patrones de fuentes tipicas
    patterns = [
        r'EXP-\d{8}-\d{3}',
        r'DEC-\d{3}',
        r'[A-Z][A-Za-z0-9_-]+\.md',
        r'[A-Z][A-Za-z0-9_-]+\.py',
        r'contract\.md',
        r'SKILL\.(md|yaml)',
    ]
    for pattern in patterns:
        matches = re.findall(pattern, raw_text)
        sources.extend(matches)
    return list(set(sources))

def classify_line(line: str) -> Optional[tuple]:
    """Clasifica una linea de texto en tipo de conocimiento"""
    l = line.lower().strip()
    
    # Detectar conflictos
    if any(w in l for w in ["pero", "conflicto", "sin embargo", "contradice", 
                             "por otro lado", "aunque", "en cambio"]):
        # Verificar que realmente hay oposicion
        if any(w in l for w in ["pero", "sin embargo", "contradice"]):
            return ("conflicto", "MEDIA")
    
    # Detectar hechos con evidencia
    if any(w in l for w in ["e3", "validado", "confirmado", "demostrado", 
                             "5/5", "fatal", "siempre"]):
        return ("hecho", "ALTA")
    
    # Detectar hipotesis
    if any(w in l for w in ["e2", "hipotesis", "parece", "probablemente",
                             "sugiere", "podria", "cabe"]):
        return ("hipotesis", "MEDIA")
    
    # Detectar decisiones
    if any(w in l for w in ["dec-", "se decidio", "designar", "usar por defecto",
                             "no usar", "rechazar"]):
        return ("decision", "ALTA")
    
    # Detectar acciones
    if any(w in l for w in ["habria que", "deberia", "propuesta", "implementar",
                             "crear", "anyadir", "modificar", "actualizar"]):
        return ("accion", "MEDIA")
    
    # Detectar observaciones (E1)
    if any(w in l for w in ["e1", "observacion", "se ha visto"]):
        return ("hipotesis", "BAJA")
    
    return None

def _fuente_para_buffer(texto: str, sources: list) -> str:
    for s in sources:
        if s.lower() in texto.lower():
            return s
    return "desconocido"


def _crear_item(current_type, confidence, texto, source, source_type) -> KnowledgeItem:
    return KnowledgeItem(
        type=current_type or "hecho",
        content=texto[:300],
        source=source,
        source_type=source_type,
        confidence=confidence,
    )


def _clasificar_y_anadir(synth, item, current_type) -> None:
    if current_type in ("conflicto", "conflict"):
        synth.conflicts.append(item)
    elif current_type == "hipotesis":
        synth.hypotheses.append(item)
    elif current_type == "decision":
        synth.decisions.append(item)
    elif current_type == "accion":
        synth.actions.append(item)
    else:
        synth.facts.append(item)


def extract_knowledge_items(raw_text: str, sources: list) -> Synthesis:
    """Extrae items de conocimiento estructurado del texto"""
    synth = Synthesis()
    synth.sources_consulted = sources
    
    lines = raw_text.split("\n")
    current_type = None
    current_confidence = "BAJA"
    buffer = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Detectar secciones
        classified = classify_line(line)
        if classified:
            # Guardar buffer anterior
            if buffer:
                text = " ".join(buffer)
                source = _fuente_para_buffer(text, sources)
                item = _crear_item(current_type, current_confidence, text, source, guess_source_type(source))
                _clasificar_y_anadir(synth, item, current_type)
            
            current_type = classified[0]
            current_confidence = classified[1]
            buffer = [line]
        else:
            buffer.append(line)
    
    # Ultimo buffer
    if buffer:
        text = " ".join(buffer)
        item = _crear_item(current_type, current_confidence, text, "desconocido", "documentacion")
        _clasificar_y_anadir(synth, item, current_type)
    
    return synth

def guess_source_type(source: str) -> str:
    """Adivina el tipo de fuente por su nombre"""
    s = source.lower()
    if s.startswith("exp-"):
        return "experimento"
    if s.startswith("dec-"):
        return "decision"
    if "skill" in s:
        return "skill"
    if s.endswith(".md") and "model" in s:
        return "ficha modelo"
    if s.endswith(".py"):
        return "codigo fuente"
    if "patron" in s or "pattern" in s:
        return "patron"
    return "documentacion"

def _limpiar_texto_item(texto: str) -> str:
    texto = re.sub(r'^\[Contexto RAG\]\s*', '', texto)
    texto = re.sub(r'\[/?Contexto\]', '', texto)
    texto = re.sub(r'\(cos:\s*[\d.-]+\s*\|\s*rerank:\s*[\d.-]+\)', '', texto)
    return texto.strip()


def _calcular_confianza(synth: Synthesis) -> tuple[int, int, int]:
    total_items = len(synth.facts) + len(synth.conflicts) + len(synth.hypotheses) + len(synth.decisions)
    high_conf = sum(1 for i in synth.facts if i.confidence == "ALTA") + len(synth.decisions)
    conf_pct = int((high_conf / max(total_items, 1)) * 100)
    return (high_conf, total_items, conf_pct)


def _detectar_boundaries(synth: Synthesis) -> list[str]:
    boundaries = []
    for item in synth.facts:
        if "descartado" in item.content.lower():
            boundaries.append("  ⚠ No usar modelos descartados")
        if "function call" in item.content.lower():
            boundaries.append("  ⚠ Este modelo responde con tool calls, no texto plano")
    if not boundaries:
        boundaries.append("  ✓ Sin restricciones especiales detectadas")
    return boundaries


def _seccion_fuentes(synth: Synthesis) -> list[str]:
    weighted = [(s, SOURCE_WEIGHTS.get(guess_source_type(s), 1)) for s in synth.sources_consulted]
    weighted.sort(key=lambda x: -x[1])
    lines = []
    for s, w in weighted[:8]:
        stars = "★" * min(3, max(1, w // 3))
        lines.append(f"  [{stars}] {s}")
    return lines


def _cabecera_sintesis(synth: Synthesis, conf_pct: int, high_conf: int, total_items: int) -> list[str]:
    """Cabecera con nivel de confianza global"""
    lines = []
    lines.append("═══════════════════════════════════════════")
    lines.append("  KNOWLEDGE RESOLVER — Sintesis")
    lines.append(f"  Query: {synth.query[:80]}")
    lines.append("═══════════════════════════════════════════")
    
    # Nivel de confianza global
    lines.append(f"  Confianza global: {conf_pct}% ({high_conf}/{max(total_items,1)} items con evidencia)")
    lines.append("")
    return lines


def _seccion_hechos(synth: Synthesis) -> list[str]:
    # 1. HECHOS CONFIRMADOS (prioridad maxima)
    lines = []
    if synth.facts:
        lines.append("── HECHOS CONFIRMADOS ──")
        for i, item in enumerate(synth.facts[:5], 1):
            weight_display = "★" * min(3, max(1, item.weight // 3))
            text = item.content[:200]
            text = _limpiar_texto_item(text)
            if not text:
                continue
            lines.append(f"  [{i}] {text}")
            lines.append(f"      Fuente: {item.source} ({item.source_type}) [{weight_display}]")
            if item.evidence:
                lines.append(f"      Evidencia: {item.evidence[0][:80]}")
        lines.append("")
    return lines


def _seccion_decisiones(synth: Synthesis) -> list[str]:
    # 2. DECISIONES ACTIVAS
    lines = []
    if synth.decisions:
        lines.append("── DECISIONES ACTIVAS ──")
        for i, item in enumerate(synth.decisions[:3], 1):
            lines.append(f"  [{i}] {item.content[:150]}")
        lines.append("")
    return lines


def _seccion_conflictos(synth: Synthesis) -> list[str]:
    # 3. CONFLICTOS DETECTADOS
    lines = []
    if synth.conflicts:
        lines.append("── CONFLICTOS DETECTADOS ──")
        for i, item in enumerate(synth.conflicts[:3], 1):
            lines.append(f"  ⚠ [{i}] {item.content[:200]}")
        lines.append("")
    return lines


def _seccion_hipotesis(synth: Synthesis) -> list[str]:
    # 4. HIPOTESIS
    lines = []
    if synth.hypotheses:
        lines.append("── HIPOTESIS PENDIENTES ──")
        for i, item in enumerate(synth.hypotheses[:3], 1):
            lines.append(f"  [?] {item.content[:150]}")
        lines.append("")
    return lines


def _seccion_acciones(synth: Synthesis) -> list[str]:
    # 5. ACCIONES RECOMENDADAS
    lines = []
    if synth.actions:
        lines.append("── ACCIONES RECOMENDADAS ──")
        for i, item in enumerate(synth.actions[:5], 1):
            lines.append(f"  → {item.content[:200]}")
        lines.append("")
    return lines


def _seccion_confianza(synth: Synthesis, conf_pct: int, high_conf: int, total_items: int) -> list[str]:
    # 6. CONFIANZA GLOBAL
    lines = []
    lines.append("── CONFIANZA ──")
    lines.append(f"  Puntuacion: {conf_pct}%")
    lines.append(f"  Items con evidencia: {high_conf}/{max(total_items,1)}")
    if synth.decisions:
        lines.append(f"  Decisiones activas aplicables: {len(synth.decisions)}")
    if synth.facts:
        lines.append(f"  Hechos confirmados: {len(synth.facts)}")
    if synth.conflicts:
        lines.append(f"  Conflictos detectados: {len(synth.conflicts)} — precaucion")
    lines.append("")
    return lines


def format_synthesis(synth: Synthesis) -> str:
    """Formatea la sintesis como texto estructurado"""
    high_conf, total_items, conf_pct = _calcular_confianza(synth)
    lines = []
    lines.extend(_cabecera_sintesis(synth, conf_pct, high_conf, total_items))
    lines.extend(_seccion_hechos(synth))
    lines.extend(_seccion_decisiones(synth))
    lines.extend(_seccion_conflictos(synth))
    lines.extend(_seccion_hipotesis(synth))
    lines.extend(_seccion_acciones(synth))
    lines.extend(_seccion_confianza(synth, conf_pct, high_conf, total_items))
    
    # 7. BOUNDARIES (restricciones inyectables)
    lines.append("── BOUNDARIES RECOMENDADOS ──")
    boundaries = _detectar_boundaries(synth)
    lines.extend(boundaries)
    lines.append("")
    
    # 8. FUENTES CONSULTADAS (ordenadas por peso)
    if synth.sources_consulted:
        lines.append("── FUENTES (por peso) ──")
        lines.extend(_seccion_fuentes(synth))
        lines.append("")
    
    lines.append("═══════════════════════════════════════════")
    return "\n".join(lines)

def main():
    result = resolve_with_confidence()
    if result:
        print(format_synthesis(result["synthesis"]))
        print(f"\n--- Confidence: {format_badge(result['confidence'])} | Items: {result['total_items']} ---")

def resolve_with_confidence(raw_input: str = None) -> dict:
    """Resuelve conocimiento y devuelve resultado con confidence stamp.
    Si no se pasa raw_input, se lee de stdin/argv (compatible con CLI)."""
    import subprocess
    
    if raw_input is None:
        if not sys.stdin.isatty():
            raw_input = sys.stdin.read().strip()
        elif len(sys.argv) > 1:
            raw_input = " ".join(sys.argv[1:])
        else:
            return None
    
    # Detectar si es una query o ya es contexto procesado
    is_query = len(raw_input) < 200 or not any(s in raw_input for s in ["EXP-", "DEC-", ".md"])
    
    if is_query:
        # Buscar contexto primero
        ctx_path = os.path.expanduser("~/joko-lab/tools/context_builder.py")
        venv = os.path.expanduser("~/.venv/hermes-rag/bin/python3")
        result = subprocess.run(
            [venv, ctx_path],
            input=raw_input, capture_output=True, text=True, timeout=30
        )
        context = result.stdout
    else:
        context = raw_input
    
    # Extraer fuentes
    sources = extract_sources(context)
    
    # Sintetizar conocimiento
    synth = extract_knowledge_items(context, sources)
    synth.query = raw_input[:100]
    
    # Formatear y mostrar
    output = format_synthesis(synth)
    print(output)
    
    # Anadir confianza con stamp
    total = len(synth.facts) + len(synth.conflicts) + len(synth.hypotheses) + len(synth.decisions)
    with_evidence = len([i for i in synth.facts if i.confidence == "ALTA"]) + len(synth.decisions)
    source_types = list(set(guess_source_type(s) for s in synth.sources_consulted))
    
    result = {
        "synthesis": synth,
        "total_items": total,
        "with_evidence": with_evidence,
    }
    return stamp(result, source_types, extra_evidence=[f"{total} items, {with_evidence} con evidencia"])

if __name__ == "__main__":
    main()
