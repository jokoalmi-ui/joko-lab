#!/usr/bin/env python3
"""
verificador_alucinaciones.py — Gate de veracidad para outputs del lab (Joko Lab)

Propósito: detectar y clasificar los 4 tipos de alucinación en cualquier texto
que el lab emita (respuesta, análisis, informe), y etiquetar el nivel de certeza
de forma explícita y visible.

Tipos cubiertos (taxonomía del reel codeby.akash + académica):
  1. sentence_contradiction  — el texto se contradice internamente (faithfulness)
  2. prompt_contradiction    — el texto desobedece instrucciones del prompt dado
  3. factual_check           — ¿tiene fuentes contrastables? (factuality/extrínseca)
  4. randomness              — ¿es relevante al tema pedido? (irrelevancia)

Etiqueta de certeza (salida):
  [VERIFICADO]      → hay fuentes/citas y sin contradicciones (🟢)
  [ALCANCE INTERNO] → trata conocimiento del lab verificado contra su BD (🟢)
  [NO VERIFICADO]   → afirma hechos externos SIN fuente (🔴 — bloquea si es factual)
  [REVISAR]         → hay contradicción interna o desviación de prompt (🟠)

Uso:
  python3 verificador_alucinaciones.py --texto "..." [--prompt "..." ] [--tema "x"] [--llm]
  python3 verificador_alucinaciones.py --archivo salida.md --prompt "..." --json
  echo "texto" | python3 verificador_alucinaciones.py --stdin

Dependencias:
  - Herramientas propias: confidence.py (etiquetas), no requiere internet
  - Opcional --llm: llama a GLM local (LM Studio :1234) como juez de contradicción
"""
import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path

# ── Integración con confidence.py (etiquetas estándar del lab) ──
sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    from confidence import to_label, from_label
    HAS_CONFIDENCE = True
except ImportError:
    HAS_CONFIDENCE = False


# ── Señales de AUTO-contradicción (referencia al propio texto, no al concepto) ──
# Fix 16-ago (2º): "se contradice" suelto daba falsos positivos en análisis que
# HABLAN sobre alucinaciones (taxonomía). Solo cuenta si se refiere al propio texto.
CONTRADICION_SIGNALS = [
    "este texto se contradice", "el texto se contradice", "la respuesta se contradice",
    "el análisis se contradice", "se contradice con lo anterior", "se contradice con lo dicho",
    "contradice lo que acaba", "contradice lo anterior", "contradice la afirmación anterior",
    "se contradice consigo", "dice lo contrario de lo que",
]
# Refutaciones explícitas (solo cuentan si hay 2+ o acompañan a negaciones del texto):
REFUTACION_PATTERNS = ["es falso que", "no es cierto que", "incorrecto afirmar", "es incorrecto que"]
NEGACION_PATTERNS = [
    r"\bno\s+(es|está|están|existe|existen|hay|tiene|tienen|funciona|debe|puede)\b",
    r"\bsin\s+(evidencia|fuente|datos|pruebas)\b",
]
AFIRMACION_PATTERNS = [
    r"\b(es|está|están|existe|existen|hay|tiene|tienen|funciona|debe|puede|confirmado|verificado)\b",
]


def _normalize(t: str) -> str:
    return re.sub(r"\s+", " ", t).strip().lower()


def _count_patterns(text: str, patterns: list) -> int:
    return sum(1 for p in patterns if re.search(p, _normalize(text)))


def detectar_contradiccion_interna(texto: str, umbral_señales: int = 1) -> dict:
    """Detección heurística de sentence contradiction (auto-contradicción).

    Solo señales de AUTO-referencia ("el texto se contradice", "contradice lo
    anterior") + conflicto cercano del mismo verbo ("X es... no es X") cuentan.
    Las refutaciones ("es falso que") solo cuentan si hay 2+ o acompañan a
    negaciones del texto. (Fix 16-ago: 17% falsos positivos → análisis que
    HABLAN sobre alucinaciones disparaban "se contradice" suelto.)
    """
    t_norm = _normalize(texto)
    n_signals = sum(1 for s in CONTRADICION_SIGNALS if s in t_norm)
    n_refutaciones = sum(1 for r in REFUTACION_PATTERNS if r in t_norm)
    n_neg = _count_patterns(texto, NEGACION_PATTERNS)
    n_af = _count_patterns(texto, AFIRMACION_PATTERNS)
    # Señal fuerte: afirma y niega el MISMO atributo cerca ("está verificado... no está verificado").
    # Excluye condicionales: "si no está X" es una regla (si/no si), no contradicción.
    conflicto_cercano = bool(re.search(
        r"\b(?:es|está|están|existe|existen|tiene|tienen)\s+(\w{4,})\b.{0,80}(?<!\bsi\s)\bno\s+(?:es|está|están|existe|existen|tiene|tienen)\s+\1\b",
        t_norm
    ))
    refutacion_fuerte = (n_refutaciones >= 2) or (n_refutaciones >= 1 and n_neg >= 1)
    detectado = (n_signals >= umbral_señales) or conflicto_cercano or refutacion_fuerte
    severidad = "alta" if (conflicto_cercano or refutacion_fuerte) else ("media" if n_signals >= 1 else "baja")
    return {
        "tipo": "sentence_contradiction",
        "detectado": detectado,
        "severidad": severidad,
        "detalle": f"{n_signals} señales de auto-contradicción, {n_refutaciones} refutaciones, {n_neg} negaciones, {n_af} afirmaciones",
    }


def detectar_desviacion_prompt(texto: str, prompt: str | None) -> dict:
    """Prompt contradiction: el texto va contra instrucciones explícitas del prompt."""
    if not prompt:
        return {"tipo": "prompt_contradiction", "detectado": False,
                "severidad": "baja", "detalle": "sin prompt para contrastar"}
    t_norm = _normalize(texto)
    p_norm = _normalize(prompt)
    instrucciones = re.findall(
        r"(no\s+inventes|no\s+inventar|sin\s+inventar|solo\s+\w+|máximo\s+\w+|minimo\s+\w+|sin\s+\w+|formato\s+(?:json|texto|markdown|tabla)|en\s+español|exactamente)",
        p_norm)
    violaciones = []
    for inst in instrucciones:
        # "no inventes" / "no inventar" / "sin inventar": si el texto inventa (contiene "inventa*")
        if inst in ("no inventes", "no inventar", "sin inventar") and re.search(r"invent[ao]", t_norm):
            violaciones.append(f"el texto inventa pese a '{inst}'")
        elif inst.startswith("no ") and inst[3:] in t_norm:
            violaciones.append(f"aparece '{inst[3:]}' pese a 'no {inst[3:]}'")
        elif inst.startswith("formato ") and inst.split()[-1] not in t_norm:
            violaciones.append(f"no se respeta formato {inst.split()[-1]}")
    detectado = len(violaciones) > 0
    return {
        "tipo": "prompt_contradiction",
        "detectado": detectado,
        "severidad": "media" if detectado else "baja",
        "detalle": "; ".join(violaciones) if violaciones else "no se detecta desviación de instrucciones",
    }


def detectar_fuentes(texto: str, tema: str | None) -> dict:
    """Factual check: ¿el texto aporta fuentes contrastables (URLs, citas, refs)?"""
    t_norm = _normalize(texto)
    urls = re.findall(r"https?://[^\s)\]]+", texto)
    citas = re.findall(r"\((?:fuente|fuentes|ver|ref|según|source)\s*[:：]?\s*[^)]+\)", texto, re.I)
    refs = re.findall(r"(?:research/|analisis-|\.md\b)", texto)
    verificadores = re.findall(r"\[VERIFICADO\]|\[ALCANCE INTERNO\]|verificado|fuente oficial", texto, re.I)
    n_fuentes = len(urls) + len(citas) + len(refs)
    # Heurística: tema factual (números, fechas, porcentajes, nombres propios)
    n_datos = len(re.findall(r"\d{2,}|\d+%|€|\$|20\d\d", texto))

    # Auto-referencia al propio lab: métricas internas (tests, GPU, servicios, RAG)
    # → conocimiento interno verificado contra su BD → ALCANCE_INTERNO, no hechos externos
    es_estado_interno = bool(re.search(
        r"(joko lab|el lab|del lab|nuestro sistema|servicios?|gpu|vram|tests?|suite|ran \d+ tests|"
        r"lancedb|rag|recall|filas?|procesos?|memoria|disco|temperatura)",
        t_norm))

    if es_estado_interno and not urls:
        return {"tipo": "factual_check", "detectado": False, "severidad": "baja",
                "detalle": "estado interno del lab (tests/GPU/servicios) — ALCANCE INTERNO",
                "fuentes": 0, "etiqueta": "ALCANCE_INTERNO"}

    # Heurística: tema factual (números, fechas, porcentajes, nombres propios)
    factual = n_datos >= 2 or tema is not None
    if not factual:
        return {"tipo": "factual_check", "detectado": False, "severidad": "baja",
                "detalle": "no parece afirmar hechos externos (o no contrastable)", "fuentes": n_fuentes,
                "etiqueta": "ALCANCE_INTERNO"}
    if n_fuentes >= 1 or verificadores:
        return {"tipo": "factual_check", "detectado": False, "severidad": "baja",
                "detalle": f"{n_fuentes} fuente(s)/cita(s) encontradas", "fuentes": n_fuentes,
                "etiqueta": "VERIFICADO"}
    return {"tipo": "factual_check", "detectado": True, "severidad": "alta",
            "detalle": "afirma hechos SIN fuente contrastable — NO VERIFICADO", "fuentes": 0,
            "etiqueta": "NO_VERIFICADO"}


def detectar_relevancia(texto: str, tema: str | None) -> dict:
    """Randomness: ¿el texto es relevante al tema pedido? (solapamiento léxico con stemming simple)"""
    if not tema:
        return {"tipo": "randomness", "detectado": False, "severidad": "baja",
                "detalle": "sin tema para contrastar relevancia"}
    tema_words = set(re.findall(r"[a-záéíóúñ]{4,}", _normalize(tema)))
    texto_words = set(re.findall(r"[a-záéíóúñ]{4,}", _normalize(texto)))
    if len(tema_words) < 3:
        # Tema corto (1-2 palabras): no se puede juzgar relevancia por solapamiento
        # (falsos positivos: "economía" vs "PIB/INE"). No marcar.
        return {"tipo": "randomness", "detectado": False, "severidad": "baja",
                "detalle": "tema demasiado corto para juzgar relevancia léxica"}

    def _raiz(p: str) -> str:
        # Stemming simple: prefijo de 5+ chars (recuperación→recup, recupera→recup)
        return p[:5] if len(p) >= 5 else p

    tema_raices = {_raiz(w) for w in tema_words}
    texto_raices = {_raiz(w) for w in texto_words}
    overlap = len(tema_raices & texto_raices) / len(tema_raices)
    detectado = overlap < 0.15
    return {
        "tipo": "randomness",
        "detectado": detectado,
        "severidad": "media" if detectado else "baja",
        "detalle": f"solapamiento léxico con tema: {overlap:.0%}",
    }


def juez_llm(texto: str, tema: str | None, endpoint: str = "http://localhost:1234/api/v0/chat/completions",
             model: str = "glm-4.6v-flash", intentos: int = 2) -> dict:
    """Juez LLM local (GLM) para contradicción semántica — opcional, no bloqueante."""
    for intento in range(intentos):
        try:
            prompt = (
                "Eres un revisor de veracidad. Analiza el siguiente texto y responde SOLO en JSON "
                "con 2 campos: contradiccion_interna (true/false), desviacion_prompt (true/false).\n\n"
                f"TEMA: {tema or 'sin tema'}\nTEXTO:\n{texto[:3000]}"
            )
            payload = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 250,
                "temperature": 0.0,
            }
            req = urllib.request.Request(endpoint, data=json.dumps(payload).encode(),
                                         headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=120) as r:
                resp = json.load(r)
            content = (resp.get("choices", [{}])[0].get("message", {}).get("content") or
                       resp.get("choices", [{}])[0].get("message", {}).get("reasoning_content") or "{}")
            # Extraer JSON del texto de respuesta (puede venir con prosa alrededor)
            m = re.search(r"\{.*\}", content, re.S)
            if m:
                data = json.loads(m.group(0))
                if "contradiccion_interna" in data or "desviacion_prompt" in data:
                    return {"usado": True, "contradiccion_interna": bool(data.get("contradiccion_interna")),
                            "desviacion_prompt": bool(data.get("desviacion_prompt"))}
        except Exception:
            # Reintentar una vez ante respuesta atípica (bug GLM razonar en voz alta)
            if intento == intentos - 1:
                return {"usado": False, "error": "no se pudo obtener respuesta JSON del juez"}
    return {"usado": False, "error": "sin respuesta"}


def verificar(texto: str, prompt: str | None = None, tema: str | None = None,
              usar_llm: bool = False) -> dict:
    """Ejecuta los 4 checks y devuelve veredicto + etiqueta de certeza."""
    checks = [
        detectar_contradiccion_interna(texto),
        detectar_desviacion_prompt(texto, prompt),
        detectar_fuentes(texto, tema),
        detectar_relevancia(texto, tema),
    ]

    # Juez LLM (si se pide): refina contradicción interna / desviación
    llm = None
    if usar_llm:
        llm = juez_llm(texto, tema)
        if llm.get("usado") and llm.get("contradiccion_interna"):
            checks[0]["detectado"] = True
            checks[0]["detalle"] += " (confirmado por juez LLM)"
        if llm.get("usado") and llm.get("desviacion_prompt"):
            checks[1]["detectado"] = True
            checks[1]["detalle"] += " (confirmado por juez LLM)"

    any_contradiccion = checks[0]["detectado"] or checks[1]["detectado"]
    factual = checks[2]
    irrelevante = checks[3]["detectado"]

    # Veredicto y etiqueta de certeza (visible)
    if any_contradiccion or irrelevante:
        veredicto = "REVISAR"
        etiqueta = "[REVISAR]"
    elif factual["etiqueta"] == "NO_VERIFICADO":
        veredicto = "BLOQUEADO_SIN_FUENTE"
        etiqueta = "[NO VERIFICADO]"
    elif factual["etiqueta"] == "VERIFICADO":
        veredicto = "OK"
        etiqueta = "[VERIFICADO]"
    else:
        veredicto = "OK_INTERNO"
        etiqueta = "[ALCANCE INTERNO]"

    return {
        "veredicto": veredicto,
        "etiqueta": etiqueta,
        "checks": checks,
        "llm_judge": llm,
    }


def main():
    ap = argparse.ArgumentParser(description="Gate de veracidad del lab (4 tipos de alucinación)")
    ap.add_argument("--texto", help="texto a verificar")
    ap.add_argument("--archivo", help="leer texto desde archivo")
    ap.add_argument("--stdin", action="store_true", help="leer texto desde stdin")
    ap.add_argument("--prompt", help="prompt original (para prompt_contradiction)")
    ap.add_argument("--tema", help="tema esperado (para relevancia)")
    ap.add_argument("--llm", action="store_true", help="usar GLM local como juez (opcional)")
    ap.add_argument("--json", action="store_true", help="salida JSON")
    args = ap.parse_args()

    if args.archivo:
        texto = Path(args.archivo).read_text(encoding="utf-8")
    elif args.stdin:
        texto = sys.stdin.read()
    else:
        texto = args.texto or ""

    if not texto.strip():
        print("ERROR: no hay texto. Usa --texto, --archivo o --stdin.")
        sys.exit(2)

    resultado = verificar(texto, prompt=args.prompt, tema=args.tema, usar_llm=args.llm)

    if args.json:
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
    else:
        print(f"VEREDICTO: {resultado['veredicto']} {resultado['etiqueta']}")
        for c in resultado["checks"]:
            estado = "⚠️" if c["detectado"] else "✅"
            print(f"  {estado} {c['tipo']}: {c['detalle']}")

    # Exit code útil para gates: 1 si hay problema que bloquee
    sys.exit(1 if resultado["veredicto"] in ("REVISAR", "BLOQUEADO_SIN_FUENTE") else 0)


if __name__ == "__main__":
    main()
