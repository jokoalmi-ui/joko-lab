#!/usr/bin/env python3
"""context_builder.py - Inyecta conocimiento automaticamente antes de responder
Uso: echo "pregunta del usuario" | python3 context_builder.py
Salida: Contexto formateado para inyectar en el prompt del LLM
"""
import sys, os, json, re, subprocess
from pathlib import Path

# Extraccion estructurada (experimento P1, adoptado 2026-08-02)
from context_builder_estructurado import parse_resultados, extraer_resumen_estructurado

SEARCH_SCRIPT = os.path.expanduser("~/joko-lab/tools/search.py")
VENV_PYTHON = os.path.expanduser("~/.venv/hermes-rag/bin/python3")

# Confidence Engine
from confidence import wrap, from_sources, format_badge, stamp

# Cache simple: evita recargar BGE-M3 en cada llamada (<3s)
import hashlib, time
CACHE_DIR = os.path.expanduser("~/tmp/rag-cache")
CACHE_TTL = 300  # 5 minutos: corto para no servir resultados obsoletos tras reindexar

def _cache_key(query: str, top_k: int) -> str:
    h = hashlib.md5(f"{query}:{top_k}".encode()).hexdigest()
    return os.path.join(CACHE_DIR, h)

def _cache_get(query: str, top_k: int) -> str:
    path = _cache_key(query, top_k)
    if os.path.exists(path):
        if time.time() - os.path.getmtime(path) < CACHE_TTL:
            with open(path) as f:
                return f.read()
    return ""

def _cache_set(query: str, top_k: int, result: str):
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(_cache_key(query, top_k), "w") as f:
        f.write(result)

# Palabras clave que activan busqueda de fichas de modelo
MODEL_KEYWORDS = [
    "modelo", "gemma", "deepseek", "granite", "qwen", "llama",
    "dolphin", "glm", "lfm", "lm studio", "gpu", "vram", "token",
    "temperature", "cuantizacion"
]

# Palabras clave que activan busqueda de decisiones
DECISION_KEYWORDS = [
    "decision", "descartar", "elegir", "seleccionar", "por que",
    "motivo", "cuando uso", "cual uso"
]

def detect_type(query: str) -> list:
    """Detecta que tipo de conocimiento buscar"""
    types = []
    q = query.lower()
    
    if any(kw in q for kw in MODEL_KEYWORDS):
        types.append("modelo")
        # Identificar modelo especifico
        for model in ["gemma", "deepseek", "granite", "qwen", "llama", "dolphin", "glm", "lfm"]:
            if model in q:
                types.append(f"ficha:{model}")
    if any(kw in q for kw in DECISION_KEYWORDS):
        types.append("decision")
    if "experimento" in q or "exp-" in q or "benchmark" in q:
        types.append("experimento")
    if "patron" in q or "anti-patron" in q:
        types.append("patron")
    
    return types

def search_rag(query: str, top_k: int = 3) -> str:
    """Busca en el RAG y devuelve contexto formateado (con cache)"""
    cached = _cache_get(query, top_k)
    if cached:
        return cached
    
    try:
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        result = subprocess.run(
            [VENV_PYTHON, SEARCH_SCRIPT, "--query", query, "--top_k", str(top_k)],
            capture_output=True, text=True, timeout=60, env=env
        )
        if result.returncode == 0 and result.stdout.strip():
            # Formateo ESTRUCTURADO (P1): ruta + campos clave + summary corto
            rutas = parse_resultados(result.stdout)
            if rutas:
                entradas = [extraer_resumen_estructurado(r) for r in rutas]
                # Gate-005 KCR (06-ago-2026): priorizar conocimiento gobernado.
                # Las fichas de modelos (01-knowledge/models/) y los KOs
                # (01-knowledge/objects/) tienen mas autoridad que documentos
                # sueltos (GUIA, analisis, research). Sin esto, la ficha correcta
                # (p.ej. llama-3.1-instruct-8b para tool-use) quedaba enterrada
                # tras docs irrelevantes y el modelo elegia otra regla (V003).
                def _es_gobernado(e: str) -> bool:
                    return ("01-knowledge/models/" in e) or ("01-knowledge/objects/" in e)
                entradas.sort(key=lambda e: 0 if _es_gobernado(e) else 1)
                texto = "\n".join(entradas[:5])
                _cache_set(query, top_k, texto)
                return texto
    except subprocess.TimeoutExpired:
        pass
    except Exception:
        pass
    return ""


INDICE_OKF = os.path.expanduser("~/joko-lab/verification/indice-okf.md")
INDICE_SCRIPT = os.path.expanduser("~/joko-lab/tools/generar_indice_okf.py")


def leer_indice_okf() -> str:
    """Índice de KOs con VIGENCIA (OKF). Lo regenera si falta.
    Es la fuente de verdad de qué existe y qué está vigente (expires/superseded)."""
    try:
        if not os.path.exists(INDICE_OKF):
            subprocess.run([sys.executable, INDICE_SCRIPT], capture_output=True, timeout=30)
        if os.path.exists(INDICE_OKF):
            with open(INDICE_OKF, encoding="utf-8") as f:
                return f.read().strip()
    except Exception:
        pass
    return ""

EVENTS_FILE = os.path.expanduser("~/.hermes/shared-events.jsonl")

def leer_eventos_recientes(limit: int = 5) -> str:
    """Últimos eventos compartidos entre sesiones (shared-events.jsonl).
    Visibilidad cruzada: qué pasó en CLI/Telegram/cron sin buscarlo en el RAG
    (coordinación multisesión — no se pierde nada de ninguna sesión)."""
    try:
        if not os.path.exists(EVENTS_FILE):
            return ""
        eventos = []
        with open(EVENTS_FILE, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    e = json.loads(line)
                except json.JSONDecodeError:
                    continue
                eventos.append(e)
        if not eventos:
            return ""
        out = []
        for e in eventos[-limit:]:
            ts = e.get("ts", "?")[5:16]  # MM-DD HH:MM
            canal = e.get("canal", "?")
            tipo = e.get("tipo", "?")
            resumen = e.get("resumen", "")
            out.append(f"[{ts}] {canal}/{tipo}: {resumen}")
        return "\n".join(out)
    except Exception:
        return ""

def get_model_card(model_name: str) -> str:
    """Busca la ficha de un modelo por palabra clave (formato estructurado P1)"""
    model_files = {
        "deepseek": "deepseek-r1-14b.md",
        "gpt": "gpt-oss-20b.md",
        "gemma": "gemma-4-12b.md",
        "granite": "granite-4.1-8b.md",
        "qwen": "qwen3-14b.md",
        "llama": "llama-3.1-instruct-8b.md",
        "dolphin": "dolphin-cyber-lora-8b.md",
        "lfm": "lfm2.5-2.6b.md",
        "glm": "glm-4.6v-flash.md"
    }
    for key, filename in model_files.items():
        if key in model_name.lower():
            return extraer_resumen_estructurado(f"01-knowledge/models/{filename}")
    return ""

SECCIONES_CAPTURA = ("## Fortalezas", "## Debilidades", "## Parametros", "personalidad:")


def _es_inicio_captura(line: str) -> bool:
    return line.startswith(SECCIONES_CAPTURA)


def _es_fin_captura(line: str) -> bool:
    return line.startswith("## ") and not _es_inicio_captura(line)


def extract_card_summary(content: str, model: str) -> str:
    """Extrae resumen de una ficha de modelo"""
    lines = content.split("\n")
    summary = []
    capture = False
    for line in lines:
        if _es_inicio_captura(line):
            capture = True
        elif capture and _es_fin_captura(line):
            capture = False
        if capture:
            summary.append(line)
    return "\n".join(summary[:20])

def _marcar_checks(*checks: str):
    """Marca checks pre-flight (best-effort, no interrumpe)."""
    subprocess.run(
        [sys.executable, os.path.expanduser("~/joko-lab/tools/preflight_checklist.py"), "mark",
         *checks],
        capture_output=True
    )


def _contexto_generico(user_input: str) -> str:
    """Búsqueda genérica por defecto (sin tipos detectados)."""
    rag = search_rag(user_input, 2)
    eventos = leer_eventos_recientes(5)
    bloque_eventos = f"[Eventos recientes]\n{eventos}\n[/Eventos]\n\n" if eventos else ""
    if rag:
        return f"{bloque_eventos}[Contexto RAG]\n{rag}\n[/Contexto]"
    return bloque_eventos.strip()


def _bloque_ficha_modelo(types: list, user_input: str, parts: list):
    """Añade la ficha de modelo si se detectó, marcando checks."""
    for t in types:
        if t.startswith("ficha:"):
            model = t.split(":", 1)[1]
            card = get_model_card(model)
            if card:
                parts.append(f"[Ficha: {model}]\n{card}\n[/Ficha]")
                _marcar_checks("ficha_consultada", "max_tokens_ok", "temperature_ok",
                               "modelo_no_descartado")


def build_context(user_input: str) -> str:
    """Construye el contexto completo para inyectar"""
    # Marcar checks pre-flight
    _marcar_checks("rag_consultado", "anti_patrones_verificados")
    types = detect_type(user_input)
    
    if not types:
        return _contexto_generico(user_input)
    
    parts = []
    
    # Eventos recientes (coordinacion multisesion): visibilidad CLI/Telegram/cron
    eventos = leer_eventos_recientes(5)
    if eventos:
        parts.append(f"[Eventos recientes]\n{eventos}\n[/Eventos]")
    
    # 0. Índice de conocimiento con VIGENCIA (OKF): qué existe y qué está vigente.
    #    Se inyecta cuando la tarea toca conocimiento gobernado (modelo/decision/exp).
    indice = leer_indice_okf()
    if indice:
        parts.append(f"[Índice de conocimiento (vigencia)]\n{indice}\n[/Índice]")
    
    # 1. Busqueda RAG general
    rag = search_rag(user_input, 5)
    if rag:
        parts.append(f"[Contexto RAG]\n{rag}\n[/Contexto]")
    
    # 2. Ficha de modelo si se detecto
    _bloque_ficha_modelo(types, user_input, parts)
    
    # 3. Decisiones si aplica
    if "decision" in types:
        decision = search_rag(f"decision sobre {user_input}", 2)
        if decision:
            parts.append(f"[Decisiones]\n{decision}\n[/Decisiones]")
    
    return "\n\n".join(parts)

if __name__ == "__main__":
    import select
    # Leer de stdin si hay datos (pipe) o del argumento
    if not sys.stdin.isatty():
        user_input = sys.stdin.read().strip()
    elif len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
    else:
        sys.exit(0)
    
    context = build_context(user_input)
    
    # Calcular confianza basada en fuentes encontradas
    source_types = set()
    if "[Contexto RAG]" in context:
        source_types.add("experimento")
    if "[Ficha:" in context:
        source_types.add("ficha modelo")
    if "[Decisiones]" in context:
        source_types.add("decision")
    if "[Anti-patrones]" in context:
        source_types.add("anti-patron")
    
    # Verificar relevancia real: ¿hay resultados con cos > 0.1?
    import re as _re
    cos_scores = [float(c) for c in _re.findall(r'cos:\s*(-?[\d.]+)', context)]
    relevant = any(c > 0.1 for c in cos_scores) if cos_scores else False
    
    conf_pct = from_sources(list(source_types)) if source_types else 30
    if not relevant:
        conf_pct = min(conf_pct, 30)  # Maximo 30% si cos <= 0.1
    
    if context:
        print(context)
    else:
        print("[Contexto: sin resultados especificos]")
    
    print(f"\n--- Confidence: {format_badge(conf_pct)} | Fuentes: {len(source_types)} ---")


def build_context_with_confidence(user_input: str) -> dict:
    """Construye contexto y devuelve resultado con confidence stamp."""
    context = build_context(user_input)
    
    # Detectar fuentes
    source_types = set()
    if "[Contexto RAG]" in context: source_types.add("experimento")
    if "[Ficha:" in context: source_types.add("ficha modelo")
    if "[Decisiones]" in context: source_types.add("decision")
    if "[Anti-patrones]" in context: source_types.add("anti-patron")
    
    result = {
        "context": context,
        "truncated": len(context) > 2000,
    }
    return stamp(result, list(source_types) if source_types else ["documentacion"])
