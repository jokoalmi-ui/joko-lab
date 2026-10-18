#!/usr/bin/env python3
"""
Critic Loop v0.1 — Instrumento científico para Joko Lab.

RESTRICCIÓN CONSTITUCIONAL:
    Este script NO modifica absolutamente nada.
    No toca HTML. No propone cambios. No escribe CSS. No optimiza.
    Su única misión es observar, medir y registrar.

INPUT:
    - Un archivo HTML (ej: ficha de perfume)
    - Un YAML de principios de diseño

PROCESS:
    Playwright → captura → LM Studio visión → evaluación por principio

OUTPUT:
    JSON con: principio, score, confidence, evidence[], uncertainty

Propósito real:
    Validar el instrumento de medida — ¿los principios del YAML
    producen evaluaciones consistentes entre modelos y en el tiempo?
"""

import argparse
import base64
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
import yaml
from playwright.sync_api import sync_playwright

# ─── CONSTITUTIONAL CONSTANTS ───────────────────────────────────
LMSTUDIO_URL = "http://localhost:1234/v1/chat/completions"
DEFAULT_MODEL = "glm-4.6v-flash"
OUTPUT_DIR = Path(__file__).parent / "outputs"
MAX_RETRIES = 3
REQUEST_TIMEOUT = 120
SCREENSHOT_WIDTH = 1440
SCREENSHOT_HEIGHT = 900


def load_principles(yaml_path: str) -> list[dict]:
    """Carga el YAML de principios. Solo extrae nombre y pregunta evaluable."""
    with open(yaml_path) as f:
        data = yaml.safe_load(f)
    principles = data.get("principles", [])
    return [
        {
            "name": p["name"],
            "question": p.get("question", ""),
            "evaluable": p.get("evaluable", True),
        }
        for p in principles
    ]


def capture_screenshot(source: str, is_url: bool = False) -> bytes:
    """Renderiza el HTML con Playwright y devuelve la captura en PNG.
    
    source: ruta a archivo HTML o URL completa.
    is_url: si True, source se trata como URL (http://...)
    """
    target = source if is_url else f"file://{os.path.abspath(source)}"
    print(f"  [capture] Abriendo {target}...", flush=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": SCREENSHOT_WIDTH, "height": SCREENSHOT_HEIGHT})
        page.goto(target, wait_until="load", timeout=20000)
        time.sleep(1.5)  # pausa para CDNs, fuentes, renderizado
        print(f"  [capture] Renderizado OK, tomando screenshot...", flush=True)
        screenshot = page.screenshot(full_page=True, type="png")
        browser.close()
    return screenshot


def build_prompt(principles: list[dict]) -> str:
    """Construye el prompt de evaluación para el modelo de visión."""
    principles_text = "\n".join(
        f"{i+1}. **{p['name']}** — {p['question']}"
        for i, p in enumerate(principles)
    )

    return f"""Eres un crítico de diseño objetivo y riguroso. No eres un diseñador. Eres un evaluador.

Tu tarea: evaluar esta captura de pantalla contra cada uno de los siguientes principios de diseño.

PRINCIPIOS A EVALUAR:
{principles_text}

INSTRUCCIONES:
- Para CADA principio, asigna un score de 0 a 10 (0 = totalmente incumplido, 10 = totalmente cumplido).
- Para CADA principio, indica tu CONFIDENCE (0.0 a 1.0) en tu propia evaluación.
- Para CADA principio, indica tu UNCERTAINTY: "low", "medium" o "high".
- Para CADA principio, proporciona de 1 a 3 evidencias visuales concretas que justifiquen tu score.
  Las evidencias deben describir elementos visuales específicos que ves en la captura.
- NO propongas cambios. NO sugieras mejoras. Solo evalúa lo que ves.
- Si un principio es demasiado ambiguo para ser evaluado, indícalo con confidence < 0.4
  y explica por qué en las evidencias.

Responde ÚNICAMENTE con un objeto JSON válido con esta estructura exacta:
{{
  "evaluations": [
    {{
      "principle": "nombre_del_principio",
      "score": 7,
      "confidence": 0.85,
      "uncertainty": "low",
      "evidence": ["evidencia visual 1", "evidencia visual 2"]
    }},
    ...
  ]
}}

NO incluyas texto antes ni después del JSON. Solo el JSON."""


def evaluate_with_lmstudio(screenshot: bytes, prompt: str, model: str) -> dict:
    """Envía la captura a LM Studio con el prompt de evaluación."""
    image_b64 = base64.b64encode(screenshot).decode("utf-8")

    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{image_b64}"},
                    },
                ],
            }
        ],
        "temperature": 0.1,
        "max_tokens": 8192,
    }

    for attempt in range(MAX_RETRIES):
        content = ""
        reasoning = ""
        try:
            print(f"  [lmstudio] Enviando prompt + captura a {model} (attempt {attempt+1}, max_tokens={payload.get('max_tokens','?')})...", flush=True)
            resp = requests.post(LMSTUDIO_URL, json=payload, timeout=REQUEST_TIMEOUT)
            resp.raise_for_status()
            data = resp.json()
            choice = data["choices"][0]
            content = choice["message"].get("content", "")
            reasoning = choice["message"].get("reasoning_content", "")
            finish = choice.get("finish_reason", "unknown")
            usage = data.get("usage", {})
            print(f"  [lmstudio] Finish: {finish}, content: {len(content)} chars, reasoning: {len(reasoning)} chars, tokens: {usage.get('completion_tokens','?')}", flush=True)

            # glm-4.6v puts evaluation in reasoning_content, content may be empty
            usable = content or reasoning
            if not usable:
                print(f"  [lmstudio] WARN: respuesta vacia, reintentando...", flush=True)
                continue

            # If only reasoning exists, extract JSON from it
            if not content and reasoning:
                print(f"  [lmstudio] Usando reasoning_content como respuesta...", flush=True)
                return _parse_json_response(reasoning)

            return _parse_json_response(content)

        except requests.exceptions.Timeout:
            print(f"  [lmstudio] TIMEOUT tras {REQUEST_TIMEOUT}s", flush=True)
        except Exception as e:
            print(f"  [lmstudio] ERROR: {e}", flush=True)

    # All retries exhausted
    return {"error": f"All {MAX_RETRIES} attempts failed", "evaluations": []}


def _parse_json_response(text: str) -> dict:
    """Extrae y parsea el JSON de la respuesta del modelo, manejando markdown."""
    text = text.strip()
    # Quitar bloques de código markdown si existen
    if text.startswith("```json"):
        text = text[7:]
    if text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return json.loads(text.strip())


def compute_agreement(results: list[dict]) -> dict:
    """Calcula métricas de acuerdo entre evaluaciones de distintos modelos.

    No usado en v0.1 (single-model), pero disponible para multi-model runs."""
    return {"note": "Multi-model agreement requires >=2 model evaluations"}


def run(
    source: str,
    yaml_path: str,
    model: str = DEFAULT_MODEL,
    tag: str = "",
    is_url: bool = False,
) -> dict:
    """Ejecuta el bucle completo de evaluación."""
    principles = load_principles(yaml_path)
    print(f"[critic-loop] Cargados {len(principles)} principios")

    print(f"[critic-loop] Capturando {source}...")
    screenshot = capture_screenshot(source, is_url=is_url)
    print(f"[critic-loop] Captura: {len(screenshot)} bytes")

    prompt = build_prompt(principles)

    print(f"[critic-loop] Evaluando con {model}...")
    start = time.time()
    result = evaluate_with_lmstudio(screenshot, prompt, model)
    elapsed = time.time() - start

    if "error" in result:
        print(f"[critic-loop] ERROR: {result['error']}")
        return result

    timestamp = datetime.now(timezone.utc).isoformat()
    source_label = source.replace("://", "_").replace("/", "_")[:60]
    record = {
        "meta": {
            "instrument": "critic-loop",
            "version": "0.1",
            "timestamp": timestamp,
            "source": source,
            "yaml_path": os.path.abspath(yaml_path),
            "model": model,
            "elapsed_seconds": round(elapsed, 1),
            "screenshot_bytes": len(screenshot),
            "principles_count": len(principles),
            "tag": tag,
            "notes": [
                "Constitutional constraint: this instrument does NOT modify anything.",
                "It only observes, measures, and records.",
                "Purpose: validate whether design principles are consistently evaluable.",
            ],
        },
        "evaluations": result.get("evaluations", []),
        "aggregates": _compute_aggregates(result.get("evaluations", [])),
    }

    # Guardar
    model_safe = model.replace("/", "_")
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{source_label}_{model_safe}_{ts}.json"
    output_path = OUTPUT_DIR / filename
    with open(output_path, "w") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)

    print(f"[critic-loop] Resultado guardado en {output_path}")
    return record


def _compute_aggregates(evaluations: list[dict]) -> dict:
    """Calcula métricas agregadas de la evaluación."""
    if not evaluations:
        return {"error": "no evaluations"}
    scores = [e["score"] for e in evaluations if "score" in e]
    confidences = [e["confidence"] for e in evaluations if "confidence" in e]
    n = len(evaluations)

    low_conf = [e for e in evaluations if e.get("confidence", 0) < 0.4]
    high_uncertainty = [e for e in evaluations if e.get("uncertainty") == "high"]

    return {
        "mean_score": round(sum(scores) / len(scores), 2) if scores else None,
        "min_score": min(scores) if scores else None,
        "max_score": max(scores) if scores else None,
        "mean_confidence": round(sum(confidences) / len(confidences), 3) if confidences else None,
        "low_confidence_principles": [e["principle"] for e in low_conf],
        "high_uncertainty_principles": [e["principle"] for e in high_uncertainty],
        "evaluated_count": n,
        "flag": "INSTRUMENT_WARNING" if len(low_conf) > n * 0.3 else "ok",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Critic Loop v0.1 — Joko Lab")
    parser.add_argument("source", help="Ruta al archivo HTML o URL completa")
    parser.add_argument(
        "--url", action="store_true", help="La fuente es una URL (http://...) en lugar de un archivo"
    )
    parser.add_argument(
        "--yaml",
        default="/home/jokoalmi/perfume-ia/governance/design-principles.yaml",
        help="Ruta al YAML de principios",
    )
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Modelo de LM Studio a usar")
    parser.add_argument("--tag", default="", help="Etiqueta opcional (ej: v17, prod)")
    args = parser.parse_args()

    result = run(args.source, args.yaml, args.model, args.tag, is_url=args.url)

    if "error" in result:
        print(f"\nFALLO: {result['error']}")
        sys.exit(1)

    print(f"\n[critic-loop] Completado.")
    agg = result.get("aggregates", {})
    print(f"  Mean score: {agg.get('mean_score', 'N/A')}")
    print(f"  Mean confidence: {agg.get('mean_confidence', 'N/A')}")
    print(f"  Low confidence principles: {agg.get('low_confidence_principles', [])}")
    print(f"  Flag: {agg.get('flag', 'N/A')}")
