#!/usr/bin/env python3
"""context_builder_estructurado.py - Variante ESTRUCTURADA del context builder (experimento P1)

Diferencias frente a context_builder.py (crudo):
  - Por cada resultado del RAG devuelve SOLO: ruta + campos clave del frontmatter
    (id/type/status) + summary corto del body (~2 lineas), en vez de snippets
    completos de hasta 25 lineas x 500 chars.
  - Objetivo: ~70 tokens/consulta en vez de ~280 (ahorro ~75%).
  - Misma interfaz: echo "pregunta" | python3 context_builder_estructurado.py

NO modifica el original. Creado 2026-08-02 para el experimento P1
(medir ahorro real de tokens: crudo vs estructurado, 4 dimensiones).
"""
import sys, os, json, re, subprocess, yaml
from pathlib import Path

SEARCH_SCRIPT = os.path.expanduser("~/joko-lab/tools/search.py")
VENV_PYTHON = os.path.expanduser("~/.venv/hermes-rag/bin/python3")

# Palabras clave que activan busqueda de fichas de modelo (igual que original)
MODEL_KEYWORDS = [
    "modelo", "gemma", "deepseek", "granite", "qwen", "llama",
    "dolphin", "glm", "lm studio", "gpu", "vram", "token",
    "temperature", "cuantizacion"
]
DECISION_KEYWORDS = [
    "decision", "descartar", "elegir", "seleccionar", "por que",
    "motivo", "cuando uso", "cual uso"
]


def detect_type(query: str) -> list:
    types = []
    q = query.lower()
    if any(kw in q for kw in MODEL_KEYWORDS):
        types.append("modelo")
        for model in ["gemma", "deepseek", "granite", "qwen", "llama", "dolphin", "glm"]:
            if model in q:
                types.append(f"ficha:{model}")
    if any(kw in q for kw in DECISION_KEYWORDS):
        types.append("decision")
    if "experimento" in q or "exp-" in q or "benchmark" in q:
        types.append("experimento")
    if "patron" in q or "anti-patron" in q:
        types.append("patron")
    return types


def parse_resultados(salida: str) -> list:
    """Extrae las rutas de los resultados de search.py.

    Formato de search.py:
        [1] ruta  (cos: 0.116 | rerank: 1.550)
        [2] ruta  ...
    """
    rutas = []
    for line in salida.split("\n"):
        m = re.match(r"^\[\d+\]\s+(\S+)\s+\(cos:", line.strip())
        if m:
            rutas.append(m.group(1))
    return rutas


def _parsear_frontmatter(raw: str) -> tuple:
    """Extrae (meta, body) del frontmatter YAML de un .md."""
    meta = {}
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", raw, re.DOTALL)
    body = raw
    if m:
        try:
            meta = yaml.safe_load(m.group(1)) or {}
        except Exception:
            meta = {}
        body = raw[m.end():]
    return meta, body


def _resumen_body(body: str, max_lineas: int = 2) -> list:
    """Primeras líneas no vacías ni headers del body."""
    resumen = []
    for line in body.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        resumen.append(line[:160])
        if len(resumen) >= max_lineas:
            break
    return resumen


def _resumen_markdown(rpath: str, raw: str) -> str:
    """Encapsula la rama .md: frontmatter YAML + summary del body."""
    meta, body = _parsear_frontmatter(raw)
    campos = _campos_clave(meta, ("id", "type", "status", "title"))
    resumen = _resumen_body(body)
    partes = [rpath]
    if campos:
        partes.append(" | ".join(campos))
    if resumen:
        partes.append("; ".join(resumen)[:320])
    return " | ".join(partes)


def _campos_clave(data, claves) -> list:
    """Devuelve ['k: v', ...] para las claves presentes en data."""
    return [f"{k}: {data.get(k)}" for k in claves if data.get(k)]


def _campos_legacy(lf):
    """Extrae los campos legacy_field comunes (condicion/accion/prioridad/nota)."""
    result = []
    for k in ("condicion", "accion", "prioridad", "nota"):
        if lf.get(k):
            result.append(f"{k}: {lf.get(k)}")
    return result


def _params_legacy(accion):
    """Extrae params del dict accion."""
    result = []
    params = accion.get("params") if isinstance(accion, dict) else None
    if isinstance(params, dict):
        for k, v in params.items():
            if v is not None:
                result.append(f"param_{k}: {v}")
    return result


def _resumen_yaml(rpath: str, raw: str) -> str:
    """Encapsula la rama .yaml/.yml: aplanar campos clave."""
    try:
        data = yaml.safe_load(raw)
    except Exception:
        return f"{rpath}  (yaml no parseable)"
    if not isinstance(data, dict):
        return rpath
    partes = [rpath]
    campos = _campos_clave(data, ("id", "type", "status", "domain", "scope"))
    if campos:
        partes.append(" | ".join(campos))
    body = data.get("body")
    if isinstance(body, str):
        partes.append(f"body: {body[:200]}")
    lf = data.get("legacy_fields") or {}
    if not isinstance(lf, dict):
        lf = {}
    partes.extend(_campos_legacy(lf))
    accion = lf.get("accion") or {}
    partes.extend(_params_legacy(accion))
    return " | ".join(partes[:8])  # limite: entrada compacta


def extraer_resumen_estructurado(rpath: str) -> str:
    """Devuelve una entrada compacta por ruta: campos clave + summary corto."""
    base = os.path.expanduser("~/joko-lab")
    fpath = Path(base) / rpath
    if not fpath.exists():
        return f"{rpath}  (archivo no encontrado)"
    try:
        raw = fpath.read_text(encoding="utf-8")
    except Exception as e:
        return f"{rpath}  (error lectura: {e})"

    if fpath.suffix == ".md":
        return _resumen_markdown(rpath, raw)
    return _resumen_yaml(rpath, raw)


def search_rag_estructurado(query: str, top_k: int = 5) -> str:
    """Busca en el RAG y devuelve contexto ESTRUCTURADO (compacto)."""
    try:
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        result = subprocess.run(
            [VENV_PYTHON, SEARCH_SCRIPT, "--query", query, "--top_k", str(top_k)],
            capture_output=True, text=True, timeout=60, env=env
        )
        if result.returncode != 0 or not result.stdout.strip():
            return ""
        rutas = parse_resultados(result.stdout)
        if not rutas:
            return ""
        entradas = [extraer_resumen_estructurado(r) for r in rutas]
        return "\n".join(entradas[:5])
    except Exception:
        return ""


def get_model_card(model_name: str) -> str:
    """Ficha de modelo: version compacta (ruta + campos clave)."""
    model_files = {
        "deepseek": "deepseek-r1-14b.md",
        "gpt": "gpt-oss-20b.md",
        "gemma": "gemma-4-12b.md",
        "granite": "granite-4.1-8b.md",
        "qwen": "qwen3-14b.md",
        "llama": "llama-3.1-instruct-8b.md",
        "dolphin": "dolphin-cyber-lora-8b.md",
        "glm": "glm-4.6v-flash.md"
    }
    for key, filename in model_files.items():
        if key in model_name.lower():
            path = os.path.expanduser(f"~/joko-lab/01-knowledge/models/{filename}")
            if os.path.exists(path):
                return extraer_resumen_estructurado(f"01-knowledge/models/{filename}")
    return ""


def build_context(user_input: str) -> str:
    """Construye el contexto ESTRUCTURADO para inyectar."""
    types = detect_type(user_input)

    if not types:
        rag = search_rag_estructurado(user_input, 2)
        if rag:
            return f"[Contexto RAG]\n{rag}\n[/Contexto]"
        return ""

    parts = []
    rag = search_rag_estructurado(user_input, 5)
    if rag:
        parts.append(f"[Contexto RAG]\n{rag}\n[/Contexto]")

    for t in types:
        if t.startswith("ficha:"):
            model = t.split(":", 1)[1]
            card = get_model_card(model)
            if card:
                parts.append(f"[Ficha: {model}]\n{card}\n[/Ficha]")

    if "decision" in types:
        decision = search_rag_estructurado(f"decision sobre {user_input}", 2)
        if decision:
            parts.append(f"[Decisiones]\n{decision}\n[/Decisiones]")

    return "\n\n".join(parts)


if __name__ == "__main__":
    if not sys.stdin.isatty():
        user_input = sys.stdin.read().strip()
    elif len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
    else:
        sys.exit(0)

    context = build_context(user_input)
    if context:
        print(context)
    else:
        print("[Contexto: sin resultados especificos]")
