#!/usr/bin/env python3
"""
medir_p1.py - Experimento P1: contexto RAG CRUDO vs ESTRUCTURADO
Medicion en 4 dimensiones: tokens, latencia, precision, cobertura.

Uso:
    python3 medir_p1.py                          # medicion completa (requiere LLM en :1234)
    python3 medir_p1.py --no-llm                 # solo contexto (sin llamadas al LLM)
    python3 medir_p1.py --model granite-4.1-8b   # modelo explicito
    python3 medir_p1.py --endpoint http://localhost:1234

Salida: tabla por item + resumen agregado. NO modifica nada del lab.
Creado 2026-08-02 para P1 (backlog 31-jul).
"""
import argparse
import datetime
import os
import subprocess
import sys
import time

import requests
import yaml

from comparador import evaluar

LAB_TOOLS = os.path.expanduser("~/joko-lab/tools")
VENV_PYTHON = os.path.expanduser("~/.venv/hermes-rag/bin/python3")
CRUDO = os.path.join(LAB_TOOLS, "context_builder.py")
ESTRUCTURADO = os.path.join(LAB_TOOLS, "context_builder_estructurado.py")
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


def ejecutar_context_builder(script: str, pregunta: str) -> tuple[str, float]:
    """Ejecuta un context builder y devuelve (contexto, tiempo_construccion)."""
    t0 = time.perf_counter()
    try:
        r = subprocess.run(
            [VENV_PYTHON, script],
            input=pregunta, capture_output=True, text=True, timeout=90
        )
        ctx = r.stdout.strip()
    except Exception as e:
        ctx = f"[ERROR: {e}]"
    dt = time.perf_counter() - t0
    return ctx, dt


def estimar_tokens(texto: str) -> int:
    """Estimacion aproximada: ~4 chars/token (heuristica estandar)."""
    return max(1, len(texto) // 4)


def fuentes_de(item: dict) -> list:
    """Extrae rutas fuente del item (pueden venir separadas por '+')."""
    return [s.strip() for s in str(item["fuente"]).split("+") if s.strip()]


def cobertura_de(contexto: str, item: dict) -> tuple[bool, list]:
    """¿Aparecen las fuentes esperadas en el contexto? Devuelve (ok, faltantes)."""
    faltantes = []
    for fuente in fuentes_de(item):
        nombre = os.path.basename(fuente)  # ej: RULE-002.yaml
        if nombre not in contexto:
            faltantes.append(nombre)
    return (len(faltantes) == 0, faltantes)


def preguntar_llm(endpoint: str, model: str, contexto: str, pregunta: str, timeout: int = 90):
    """Una vuelta al LLM con contexto inyectado. Devuelve (respuesta, usage, tiempo)."""
    user_content = (
        "Usa el siguiente contexto del laboratorio Joko Lab para responder "
        "con precisión. Si el contexto contiene la respuesta, úsala literalmente.\n\n"
        f"{contexto}\n\n"
        f"PREGUNTA: {pregunta}"
    )
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": DEFAULT_SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ],
        "temperature": 0,
    }
    t0 = time.perf_counter()
    r = requests.post(f"{endpoint}/v1/chat/completions", json=payload, timeout=timeout)
    r.raise_for_status()
    dt = time.perf_counter() - t0
    data = r.json()
    resp = data["choices"][0]["message"]["content"]
    usage = data.get("usage") or {}
    return resp, usage, dt


def medir_variante(script: str, item: dict, endpoint: str, model: str, usar_llm: bool) -> dict:
    ctx, t_ctx = ejecutar_context_builder(script, item["pregunta"])
    tokens_ctx = estimar_tokens(ctx)
    ok_cob, faltantes = cobertura_de(ctx, item)

    resultado = {
        "t_construccion": t_ctx,
        "tokens_contexto_est": tokens_ctx,
        "cobertura": ok_cob,
        "faltantes": faltantes,
        "contexto": ctx,
    }

    if usar_llm and ctx and not ctx.startswith("[ERROR"):
        try:
            resp, usage, t_llm = preguntar_llm(endpoint, model, ctx, item["pregunta"])
            correcto = evaluar(item, resp)
            resultado.update({
                "respuesta": resp,
                "correcto": correcto,
                "t_llm": t_llm,
                "t_total": t_ctx + t_llm,
                "prompt_tokens": usage.get("prompt_tokens"),
                "completion_tokens": usage.get("completion_tokens"),
                "total_tokens": usage.get("total_tokens"),
            })
        except Exception as e:
            resultado.update({
                "respuesta": f"[ERROR LLM: {e}]",
                "correcto": False,
                "t_llm": None,
                "t_total": None,
                "prompt_tokens": None,
                "total_tokens": None,
            })
    return resultado


def resumen_numerico(vals: list) -> str:
    if not vals:
        return "n/d"
    return f"{sum(vals)/len(vals):.2f}"


def main():
    parser = argparse.ArgumentParser(description="P1: crudo vs estructurado (tokens, latencia, precision, cobertura)")
    parser.add_argument("--bank", default="bank.yaml", help="Ruta al banco de preguntas")
    parser.add_argument("--endpoint", default="http://localhost:1234", help="Endpoint OpenAI-compatible")
    parser.add_argument("--model", default="granite-4.1-8b", help="Modelo del servidor")
    parser.add_argument("--no-llm", action="store_true", help="Solo medir contexto, sin llamadas al LLM")
    parser.add_argument("--verbose", action="store_true", help="Mostrar contexto generado")
    args = parser.parse_args()

    banco = cargar_banco(args.bank)
    usar_llm = not args.no_llm

    print(f"=== P1: CRUDO vs ESTRUCTURADO — {datetime.datetime.now().isoformat()} ===")
    print(f"Modelo: {args.model} | LLM: {'SI' if usar_llm else 'NO (solo contexto)'} | Items: {len(banco)}\n")

    agg = {"crudo": [], "estructurado": []}

    for item in banco:
        print(f"--- {item['id']}: {item['pregunta']}")
        crudo = medir_variante(CRUDO, item, args.endpoint, args.model, usar_llm)
        est = medir_variante(ESTRUCTURADO, item, args.endpoint, args.model, usar_llm)
        agg["crudo"].append(crudo)
        agg["estructurado"].append(est)

        def fila(nombre, d):
            cob = "OK" if d["cobertura"] else f"FALTA {','.join(d['faltantes'])}"
            prec = f"{'OK' if d.get('correcto') else 'FALLO'}" if "correcto" in d else "-"
            ptok = d.get("prompt_tokens")
            ptok_s = f"{ptok}" if ptok is not None else "-"
            ttot = f"{d.get('t_total', 0):.1f}s" if d.get("t_total") else "-"
            return (f"  {nombre:<14} ctx={d['tokens_contexto_est']:>4}tok "
                    f"prompt={ptok_s:>6} cob={cob:<16} prec={prec:<5} "
                    f"t_ctx={d['t_construccion']:.1f}s t_total={ttot}")

        print(fila("CRUDO:", crudo))
        print(fila("ESTRUCTURADO:", est))
        if args.verbose and crudo["contexto"]:
            print(f"  [ctx crudo] {crudo['contexto'][:300]}")
        if args.verbose and est["contexto"]:
            print(f"  [ctx estr ] {est['contexto'][:300]}")
        print()

    # Resumen agregado
    def media(variante, campo):
        vals = [d.get(campo) for d in variante if d.get(campo) is not None]
        return resumen_numerico(vals)

    print("=== RESUMEN AGREGADO ===")
    hdr = f"{'Variante':<14} {'tok_ctx':>8} {'prompt_tok':>10} {'t_ctx(s)':>9} {'t_total(s)':>11} {'precision':>10} {'cobertura':>10}"
    print(hdr)
    for nombre, variante in (("CRUDO", agg["crudo"]), ("ESTRUCTURADO", agg["estructurado"])):
        aciertos = sum(1 for d in variante if d.get("correcto"))
        coberturas = sum(1 for d in variante if d["cobertura"])
        n = len(variante)
        print(
            f"{nombre:<14} {media(variante,'tokens_contexto_est'):>8} "
            f"{media(variante,'prompt_tokens'):>10} {media(variante,'t_construccion'):>9} "
            f"{media(variante,'t_total'):>11} {f'{aciertos}/{n}':>10} {f'{coberturas}/{n}':>10}"
        )
    print("\nNotas:")
    print("- tok_ctx: estimacion len/4 del contexto generado (no incluye system prompt)")
    print("- prompt_tok: usage.prompt_tokens real devuelto por la API (si LLM activo)")
    print("- cobertura: fuente esperada del banco presente en el contexto recuperado")


if __name__ == "__main__":
    main()
