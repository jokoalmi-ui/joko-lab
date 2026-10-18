#!/usr/bin/env python3
"""
Ejecutor del banco de verificación determinista para Joko Lab / Hermes.

Lanza cada pregunta del banco como una conversación NUEVA y AISLADA
(sin historial previo, sin memoria persistente, temperature=0), y evalúa
la respuesta con reglas deterministas (ver comparador.py) — no con el
juicio de otro modelo ni del propio Hermes.

Modos:
  --use-lab:   Ejecuta la pregunta a través del pipeline Joko Lab
               (Context Builder → Knowledge Resolver → Activation Engine)
               y mide capitalización real, no conocimiento del LLM desnudo.
  Sin --use-lab: Pregunta directa al LLM (mide conocimiento bruto del modelo).

Uso básico:
    python3 run_eval.py --model granite-4.1-8b
    python3 run_eval.py --model granite-4.1-8b --use-lab

Requiere que el servidor de inferencia (LM Studio, Ollama, etc.) esté
corriendo con un endpoint compatible OpenAI en --endpoint.
"""
import argparse
import datetime
import json
import os
import sys
import subprocess
from pathlib import Path

import requests
import yaml

from comparador import evaluar

LAB_TOOLS = os.path.expanduser("~/joko-lab/tools")
DEFAULT_SYSTEM_PROMPT = (
    "Eres Hermes, el asistente del laboratorio Joko Lab. "
    "Responde de forma breve y directa. Usa los datos del contexto si se proporcionan."
)


def cargar_banco(ruta: str) -> list:
    with open(ruta, "r", encoding="utf-8") as f:
        banco = yaml.safe_load(f)
    for item in banco:
        for campo in ("id", "pregunta", "tipo", "respuesta_esperada", "fuente"):
            if campo not in item:
                raise ValueError(f"Item sin campo obligatorio '{campo}': {item}")
    return banco


def cargar_system_prompt(ruta: str | None) -> str:
    if ruta is None:
        return DEFAULT_SYSTEM_PROMPT
    return Path(ruta).read_text(encoding="utf-8").strip()


def construir_contexto_lab(pregunta: str) -> str:
    """Ejecuta el pipeline Joko Lab y devuelve contexto enriquecido.
    Context Builder → Knowledge Resolver → Activation Engine."""
    partes = []
    venv_python = os.path.expanduser("~/.venv/hermes-rag/bin/python3")
    
    # 1. Context Builder (RAG)
    try:
        ctx = subprocess.run(
            [venv_python, os.path.join(LAB_TOOLS, "context_builder.py")],
            input=pregunta, capture_output=True, text=True, timeout=90
        )
        if ctx.stdout.strip():
            partes.append("[CONTEXTO DEL LABORATORIO]\n" + ctx.stdout.strip()[:12000])
    except Exception:
        pass
    
    # 2. Knowledge Resolver
    try:
        kr = subprocess.run(
            [sys.executable, os.path.join(LAB_TOOLS, "knowledge_resolver.py")],
            input=pregunta, capture_output=True, text=True, timeout=60
        )
        if kr.stdout.strip():
            partes.append("[CONOCIMIENTO ESTRUCTURADO]\n" + kr.stdout.strip()[:12000])
    except Exception:
        pass
    
    # 3. Activation Engine
    try:
        sys.path.insert(0, LAB_TOOLS)
        from activation_engine import activate
        from decision_engine import detect_task_type
        task_type = detect_task_type(pregunta)
        activation = activate(task_type, pregunta)
        if activation.get("total_active", 0) > 0:
            reglas = []
            if activation.get("model_selection"):
                ms = activation["model_selection"]
                reglas.append(f"  → {ms.get('id','?')}: {ms.get('desc','')}")
            if activation.get("blocks"):
                for b in activation["blocks"]:
                    reglas.append(f"  → {b.get('id','?')}: {b.get('desc','')} [BLOQUEO]")
            if reglas:
                partes.append("[REGLAS ACTIVAS]\n" + "\n".join(reglas))
    except Exception:
        pass
    
    return "\n\n".join(partes) if partes else ""


def preguntar_en_frio(pregunta: str, endpoint: str, model: str,
                       system_prompt: str, use_lab: bool = False, timeout: int = 60) -> str:
    """Conversación de una sola vuelta, sin historial ni memoria persistente.
    temperature=0 para que el resultado sea reproducible.
    Si use_lab=True, inyecta contexto del pipeline Joko Lab antes de preguntar."""
    
    user_content = pregunta
    if use_lab:
        contexto = construir_contexto_lab(pregunta)
        if contexto:
            user_content = (
                "Usa el siguiente contexto del laboratorio Joko Lab para responder "
                "con precisión. Si el contexto contiene la respuesta, úsala literalmente.\n\n"
                f"{contexto}\n\n"
                f"PREGUNTA: {pregunta}"
            )
    
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        "temperature": 0,
    }
    r = requests.post(f"{endpoint}/v1/chat/completions", json=payload, timeout=timeout)
    r.raise_for_status()
    data = r.json()
    return data["choices"][0]["message"]["content"], data.get("usage")


def ejecutar(banco: list, endpoint: str, model: str, system_prompt: str,
             use_lab: bool = False) -> dict:
    detalle = []
    aciertos = 0
    for item in banco:
        try:
            respuesta, usage = preguntar_en_frio(item["pregunta"], endpoint, model, system_prompt, use_lab)
            correcto = evaluar(item, respuesta)
        except Exception as e:
            respuesta = f"[ERROR: {e}]"
            usage = None
            correcto = False
        if correcto:
            aciertos += 1
        detalle.append({
            "id": item["id"],
            "pregunta": item["pregunta"],
            "fuente": item["fuente"],
            "respuesta": respuesta,
            "correcto": correcto,
            "usage": usage,
        })
    total = len(banco)
    return {
        "timestamp": datetime.datetime.now().isoformat(),
        "model": model,
        "use_lab": use_lab,
        "total": total,
        "aciertos": aciertos,
        "precision": round(aciertos / total, 3) if total else 0.0,
        "detalle": detalle,
    }


def guardar_historial(resultado: dict, ruta: str):
    with open(ruta, "a", encoding="utf-8") as f:
        f.write(json.dumps(resultado, ensure_ascii=False) + "\n")


def imprimir_reporte(resultado: dict):
    modo = "CON LAB" if resultado.get("use_lab") else "SIN LAB"
    print(f"\n=== Verificación {resultado['timestamp']} [{modo}] ===")
    print(f"Modelo: {resultado['model']}")
    print(f"Precisión: {resultado['aciertos']}/{resultado['total']} "
          f"({resultado['precision'] * 100:.1f}%)\n")
    for item in resultado["detalle"]:
        marca = "OK   " if item["correcto"] else "FALLO"
        print(f"  [{marca}] {item['id']}: {item['pregunta']}")
        if not item["correcto"]:
            print(f"          fuente:    {item['fuente']}")
            print(f"          respuesta: {item['respuesta'][:200]}")
    print()


def main():
    parser = argparse.ArgumentParser(description="Verificación determinista de Hermes / Joko Lab")
    parser.add_argument("--bank", default="bank.yaml", help="Ruta al banco de preguntas (yaml)")
    parser.add_argument("--history", default="history.jsonl", help="Ruta al historial acumulado (jsonl)")
    parser.add_argument("--endpoint", default="http://localhost:1234", help="Endpoint compatible OpenAI")
    parser.add_argument("--model", default="hermes-local", help="Nombre del modelo tal como lo expone el servidor")
    parser.add_argument("--system-prompt-file", default=None,
                         help="Ruta al system prompt REAL de producción (recomendado)")
    parser.add_argument("--fail-under", type=float, default=0.7,
                         help="Si la precisión cae por debajo de este umbral, el script sale con código 1 (útil para cron/CI)")
    parser.add_argument("--use-lab", action="store_true",
                         help="Inyecta contexto del pipeline Joko Lab antes de cada pregunta (mide capitalización)")
    args = parser.parse_args()

    banco = cargar_banco(args.bank)
    system_prompt = cargar_system_prompt(args.system_prompt_file)

    resultado = ejecutar(banco, args.endpoint, args.model, system_prompt, args.use_lab)
    guardar_historial(resultado, args.history)
    imprimir_reporte(resultado)

    if resultado["precision"] < args.fail_under:
        sys.exit(1)


if __name__ == "__main__":
    main()
