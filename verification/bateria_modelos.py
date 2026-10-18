#!/usr/bin/env python3
"""Bateria de pruebas exigentes para modelos locales (Joko Lab, 06-ago-2026).

8 dimensiones, evaluacion DETERMINISTA (keywords/parseo, sin LLM juez):
  A1 razonamiento numerico (moneda 3x, P(2 caras) = 3/8)
  A2 razonamiento con restricciones (problema de edades -> ecuacion)
  B1 codigo one-shot (boton contador HTML)
  B2 corregir bug Python (indice fuera de rango)
  C1 tool calling JSON estricto
  D1 espanol con 3 requisitos
  E1 consistencia (misma pregunta 2x)
  F1 latencia (tok/s de generacion)

Uso: python3 bateria_modelos.py --model <id> [--salida salida.jsonl]
"""
import argparse
import json
import os
import re
import sys
import time
import tempfile

import requests

ENDPOINT = "http://localhost:1234/v1/chat/completions"

# ─── Pruebas ─────────────────────────────────────────────

PRUEBAS = {}

def prueba(nombre, prompt, evaluar, max_tokens=400):
    PRUEBAS[nombre] = (prompt, evaluar, max_tokens)

def contiene(txt, *kws, normalizar=True):
    t = txt.lower()
    if normalizar:
        import unicodedata
        t = unicodedata.normalize("NFKD", t)
        t = "".join(c for c in t if not unicodedata.combining(c))
    return all(kw.lower() in t for kw in kws)

# A1: probabilidad exacta 2 caras en 3 lanzamientos = 3/8 (acepta LaTeX \frac{3}{8})
def eval_a1(r):
    r_norm = r.replace("\\frac{3}{8}", "3/8").replace("\\frac38", "3/8").replace("\\dfrac{3}{8}", "3/8")
    return contiene(r_norm, "3/8") or ("0.375" in r_norm.replace(",", ".")) or ("0,375" in r_norm)

prueba("A1_razonamiento_numerico",
    "Lanzas una moneda justa 3 veces. Cual es la probabilidad de obtener exactamente 2 caras? Da la respuesta como fraccion irreducible.",
    eval_a1,
    max_tokens=2000)

# A2: problema de edades -> x = 12 (Maria 24, Ana 12; en 5 anios Maria 29, Ana 17 -> 29 != 3*17...
#    version cerrada: "Maria tiene el doble que Ana. Hace 3 anios Maria tenia el triple que Ana.
#    Edad de Ana ahora: 2(x-3)=3(x-3) no... usar: Maria=2A; (M-3)=3(A-3) -> 2A-3=3A-9 -> A=6.
#    Comprobar: Maria 12, hace 3: 9 y 3 -> 9=3*3 OK. Ana ahora = 6.
prueba("A2_razonamiento_restricciones",
    "Maria tiene el doble de edad que Ana. Hace 3 anios, Maria tenia el triple que Ana. Que edad tiene Ana ahora? Responde solo con el numero.",
    lambda r: re.search(r"\b6\b", r) is not None,
    max_tokens=1500)

# B1: codigo one-shot HTML boton contador
prueba("B1_codigo_one_shot",
    "Genera un archivo HTML completo y funcional: un boton que al pulsarlo incrementa y muestra un contador en pantalla. Incluye <button> y JavaScript.",
    lambda r: contiene(r, "button") and (contiene(r, "onclick") or contiene(r, "addeventlistener") or contiene(r, "queryselector")),
    max_tokens=1500)

# B2: corregir bug Python (indice fuera de rango)
prueba("B2_corregir_bug",
    "Este codigo falla: nums = [1,2,3]\nprint(nums[3])\nCorrige el error. Responde con el codigo corregido.",
    lambda r: (contiene(r, "nums[2]") or contiene(r, "len(nums)") or contiene(r, "nums[-1]") or contiene(r, "nums[0:3]")),
    max_tokens=300)

# C1: tool calling JSON estricto
def eval_tool(r):
    # Limpiar fences de markdown y extraer el primer objeto JSON valido
    import re as _re
    raw = r
    fences = _re.findall(r"```(?:json)?\s*(.*?)```", r, _re.DOTALL)
    if fences:
        raw = fences[0]
    # 1) Parseo directo del texto (JSON plano, con llaves anidadas)
    try:
        parsed = json.loads(raw.strip())
        if parsed.get("funcion") == "buscar_tiempo" and parsed.get("args", {}).get("ciudad") == "Bilbao":
            return True
    except json.JSONDecodeError:
        pass
    # 2) Primer objeto JSON balanceado del texto (tolerante a razonamiento despues)
    for i in range(len(raw)):
        if raw[i] == "{":
            try:
                cand = _balancear_json(raw[i:])
                parsed = json.loads(cand)
                if parsed.get("funcion") == "buscar_tiempo" and parsed.get("args", {}).get("ciudad") == "Bilbao":
                    return True
            except (json.JSONDecodeError, ValueError):
                continue
    # 3) Formato nativo de tool calling: {"name": ..., "parameters": {...}}
    m = _re.search(r'"name"\s*:\s*"([^"]+)"[^}]*"ciudad"\s*:\s*"([^"]+)"', raw)
    if m:
        nombre, ciudad = m.group(1), m.group(2)
        if "tiempo" in nombre and ciudad == "Bilbao":
            return True
    return False


def _balancear_json(s: str) -> str:
    """Devuelve el objeto JSON balanceado desde la primera '{'."""
    depth = 0
    in_str = False
    escape = False
    for i, ch in enumerate(s):
        if escape:
            escape = False
            continue
        if ch == "\\" and in_str:
            escape = True
            continue
        if ch == '"':
            in_str = not in_str
            continue
        if in_str:
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return s[: i + 1]
    raise ValueError("JSON no balanceado")

prueba("C1_tool_calling_json",
    "Tienes una funcion: buscar_tiempo(ciudad: str) -> str\nDevuelve SOLO un JSON valido con la llamada para Bilbao.\nFormato: {\"funcion\": \"buscar_tiempo\", \"args\": {\"ciudad\": \"Bilbao\"}}",
    eval_tool,
    max_tokens=800)

# D1: espanol con 3 requisitos
prueba("D1_espanol_requisitos",
    "Escribe una receta de tortilla de patatas en espanol que mencione: 3 huevos, patatas, cebolla, sal y aceite de oliva. Termina con la frase: Buen provecho.",
    lambda r: contiene(r, "huevos") and contiene(r, "patatas") and contiene(r, "cebolla") and contiene(r, "aceite") and contiene(r, "buen provecho"),
    max_tokens=1500)

# E1: consistencia (se evalua en el bucle: dos llamadas, comparacion normalizada)
prueba("E1_consistencia",
    "Que es un 'commit' en git? Explica en una frase.",
    None,  # evaluacion especial
    max_tokens=100)

# F1: latencia (se mide en el bucle, no se evalua como PASS/FAIL)


def normalizar_texto(t):
    t = t.lower().strip()
    import unicodedata
    t = unicodedata.normalize("NFKD", t)
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = re.sub(r"\s+", " ", t)
    return t


def llamar(model, prompt, max_tokens):
    t0 = time.time()
    r = requests.post(ENDPOINT, json={
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0,
        "max_tokens": max_tokens,
    }, timeout=300)
    dt = time.time() - t0
    r.raise_for_status()
    data = r.json()
    msg = data["choices"][0]["message"]
    # LFM 2.5 y modelos con razonamiento encubierto: el contenido real puede
    # estar en reasoning_content si content queda vacio (finish_reason=length
    # por agotar max_tokens en el razonamiento). Concatenar ambos.
    content = (msg.get("content") or "") + (msg.get("reasoning_content") or "")
    usage = data.get("usage", {})
    return content.strip(), dt, usage


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--salida", default=os.path.expanduser("~/joko-lab/04-operations/metrics/bateria_modelos.jsonl"))
    args = parser.parse_args()

    resultados = []
    tiempos = {}
    tokens_gen = 0

    for nombre, (prompt, evaluar, max_tokens) in PRUEBAS.items():
        try:
            content, dt, usage = llamar(args.model, prompt, max_tokens)
        except Exception as e:
            resultados.append({"prueba": nombre, "pass": False, "error": str(e)})
            continue
        tiempos[nombre] = round(dt, 2)
        tokens_gen += usage.get("completion_tokens", 0) or 0

        if nombre == "E1_consistencia":
            # Segunda llamada para comparar
            content2, dt2, _ = llamar(args.model, prompt, max_tokens)
            tiempos["E1_segunda"] = round(dt2, 2)
            eq = normalizar_textor(content) == normalizar_textor(content2) or \
                 normalizar_textor(content)[:40] == normalizar_textor(content2)[:40]
            resultados.append({"prueba": nombre, "pass": bool(eq),
                               "respuesta1": content[:150], "respuesta2": content2[:150]})
        elif evaluar is not None:
            ok = evaluar(content)
            resultados.append({"prueba": nombre, "pass": bool(ok), "respuesta": content[:400]})
        # F1 se mide con tiempos acumulados

    # Latencia: tok/s de la prueba mas larga (B1 como proxy de generacion)
    latencia_toks = round(tokens_gen / max(sum(tiempos.values()), 0.01), 1)

    fila = {
        "fecha": "2026-08-06",
        "model": args.model,
        "resultados": resultados,
        "puntuacion": sum(1 for r in resultados if r.get("pass")),
        "total": len(PRUEBAS),
        "tiempos_s": tiempos,
        "tokens_generados": tokens_gen,
        "latencia_tok_s": latencia_toks,
    }

    os.makedirs(os.path.dirname(args.salida), exist_ok=True)
    with open(args.salida, "a", encoding="utf-8") as f:
        f.write(json.dumps(fila, ensure_ascii=False) + "\n")

    print(f"=== {args.model} ===")
    for r in resultados:
        marca = "PASS" if r.get("pass") else "FAIL"
        print(f"  [{marca}] {r['prueba']}" + (f" — {r.get('respuesta','')[:60]!r}" if r.get("respuesta") else ""))
    print(f"  Puntuacion: {fila['puntuacion']}/{fila['total']} | Latencia: {latencia_toks} tok/s | Tiempos: {tiempos}")
    print(f"  Salida: {args.salida}")
    sys.exit(0)


def normalizar_textor(t):
    return normalizar_texto(t)


if __name__ == "__main__":
    main()
