#!/usr/bin/env python3
"""auto_dispatcher.py — Ejecuta automaticamente la recomendacion del router

Recibe la salida del decision_router en JSON y ejecuta
el modelo recomendado contra LM Studio sin intervencion manual.

Uso:
  echo "necesito JSON" | python3 decision_router.py --json |
  python3 auto_dispatcher.py "mi prompt real aqui"

  O todo en uno:
  echo "mi prompt" | python3 auto_pipeline.py
"""
import os, sys, json, subprocess, urllib.request

TOOL_DIR = os.path.expanduser("~/joko-lab/tools")
LMSTUDIO_API = "http://localhost:1234/v1/chat/completions"

def load_model(model_id: str) -> bool:
    """Carga un modelo en LM Studio via API"""
    try:
        req = urllib.request.Request(
            f"http://localhost:1234/api/v0/models/{model_id}",
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            info = json.loads(resp.read())
            if info.get("state") == "loaded":
                return True
        
        # Intentar cargar
        payload = json.dumps({"model": model_id}).encode()
        req = urllib.request.Request(
            "http://localhost:1234/api/v1/models/load",
            data=payload,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read())
            return result.get("status") in ("ok", "loaded")
    except Exception:
        return False

def call_model(model_id: str, prompt: str, params: dict) -> str:
    """Llama al modelo recomendado con los parametros del router"""
    payload = json.dumps({
        "model": model_id,
        "messages": [
            {"role": "system", "content": "Responde de forma precisa y util."},
            {"role": "user", "content": prompt}
        ],
        "temperature": params.get("temperature", 0.3),
        "max_tokens": params.get("max_tokens", 1024),
        "stream": False
    }).encode()
    
    req = urllib.request.Request(
        LMSTUDIO_API,
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read())
            return result['choices'][0]['message']['content']
    except Exception as e:
        return f"[Error: {e}]"

def dispatch(router_json: str, user_prompt: str) -> dict:
    """Orquesta: router → cargar modelo → ejecutar → devolver"""
    try:
        route = json.loads(router_json)
    except json.JSONDecodeError:
        return {"error": "Router no devolvio JSON valido", "raw": router_json[:200]}
    
    if not route.get("recommendation"):
        fb = route.get("fallback", {})
        model = fb.get("model", "granite-4.1-8b")
        params = fb.get("params", {"max_tokens": 1024, "temperature": 0.3})
        confidence = "BAJA (fallback)"
    else:
        rec = route["recommendation"]
        model = rec.get("model", "granite-4.1-8b")
        params = rec.get("params", {"max_tokens": 1024, "temperature": 0.3})
        confidence = route.get("confidence", "MEDIA")
    
    # Cargar modelo
    loaded = load_model(model)
    if not loaded:
        return {"error": f"No se pudo cargar {model}", "model": model}
    
    # Ejecutar
    response = call_model(model, user_prompt, params)
    
    return {
        "model": model,
        "params": params,
        "confidence": confidence,
        "loaded": loaded,
        "response": response
    }

if __name__ == "__main__":
    if not sys.stdin.isatty():
        router_json = sys.stdin.read().strip()
    else:
        print("Uso: decision_router.py | auto_dispatcher.py 'prompt'")
        sys.exit(1)
    
    user_prompt = sys.argv[1] if len(sys.argv) > 1 else "Responde brevemente."
    
    result = dispatch(router_json, user_prompt)
    
    if "error" in result:
        print(f"❌ {result['error']}")
    else:
        print(f"══ AUTO-DISPATCHER ══")
        print(f"  Modelo:  {result['model']}")
        print(f"  Temp:    {result['params'].get('temperature')}")
        print(f"  Tokens:  {result['params'].get('max_tokens')}")
        print(f"  Confianza: {result['confidence']}")
        print(f"  ── Respuesta ──")
        print(f"  {result['response'][:500]}")
