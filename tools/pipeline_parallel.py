#!/usr/bin/env python3
"""pipeline_parallel.py — Patron 3: Parallelization CPU/GPU

Ejecuta CPU y GPU en paralelo:
- Mientras el LLM genera (GPU ocupada), la CPU procesa RAG,
  anti-patrones y verificacion.
- Cuando el LLM termina, los resultados CPU ya estan listos.

Uso:
  echo "pregunta del usuario" | python3 pipeline_parallel.py
"""
import os, sys, json, subprocess, threading, time, urllib.request
from queue import Queue

TOOL_DIR = os.path.expanduser("~/joko-lab/tools")
LMSTUDIO_API = "http://localhost:1234/v1/chat/completions"
VENV_PYTHON = os.path.expanduser("~/.venv/hermes-rag/bin/python3")

# ─── GPU: LLM en background ──────────────────────────
def llm_worker(prompt: str, model: str, params: dict, result_queue: Queue):
    """Ejecuta el LLM en la GPU y pone el resultado en la cola"""
    payload = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": "Responde de forma precisa y util."},
            {"role": "user", "content": prompt}
        ],
        "temperature": params.get("temperature", 0.3),
        "max_tokens": params.get("max_tokens", 1024),
        "stream": False
    }).encode()
    
    try:
        req = urllib.request.Request(
            LMSTUDIO_API, data=payload,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read())
            response = result['choices'][0]['message']['content']
            result_queue.put({"status": "ok", "response": response})
    except Exception as e:
        result_queue.put({"status": "error", "error": str(e)})

# ─── CPU: RAG + verificacion en paralelo ────────────
def cpu_worker(prompt: str, result_queue: Queue):
    """Ejecuta tareas CPU mientras el LLM genera"""
    cpu_results = {}
    
    # 1. Buscar anti-patrones relacionados (via context_builder)
    try:
        ctx = subprocess.run(
            [sys.executable, os.path.join(TOOL_DIR, "context_builder.py")],
            input=f"anti patrones para {prompt[:80]}",
            capture_output=True, text=True, timeout=15
        )
        cpu_results["anti_patrones"] = ctx.stdout[:500] if ctx.returncode == 0 else ""
    except Exception:
        cpu_results["anti_patrones"] = ""
    
    # 2. Buscar decisiones relacionadas
    try:
        dec = subprocess.run(
            [sys.executable, os.path.join(TOOL_DIR, "decision_router.py"), "--json"],
            input=prompt[:80],
            capture_output=True, text=True, timeout=15
        )
        if dec.returncode == 0:
            try:
                cpu_results["router"] = json.loads(dec.stdout)
            except json.JSONDecodeError:
                cpu_results["router"] = None
    except Exception:
        cpu_results["router"] = None
    
    # 3. Verificar preflight
    try:
        pf = subprocess.run(
            [sys.executable, os.path.join(TOOL_DIR, "preflight_checklist.py")],
            capture_output=True, text=True, timeout=5
        )
        cpu_results["preflight"] = pf.stdout[:300] if pf.returncode == 0 else ""
    except Exception:
        cpu_results["preflight"] = ""
    
    result_queue.put(cpu_results)

def parallel_pipeline(prompt: str, model: str = "granite-4.1-8b", 
                     params: dict = None) -> dict:
    """Ejecuta LLM (GPU) y CPU en paralelo"""
    if params is None:
        params = {"max_tokens": 1024, "temperature": 0.3}
    
    gpu_queue = Queue()
    cpu_queue = Queue()
    
    t0 = time.time()
    
    # Lanzar LLM en GPU
    llm_thread = threading.Thread(
        target=llm_worker, 
        args=(prompt, model, params, gpu_queue)
    )
    llm_thread.start()
    
    # Mientras GPU arranca, lanzar CPU inmediatamente
    cpu_thread = threading.Thread(
        target=cpu_worker,
        args=(prompt, cpu_queue)
    )
    cpu_thread.start()
    
    # Esperar a ambos
    llm_thread.join(timeout=120)
    cpu_thread.join(timeout=30)
    
    elapsed = time.time() - t0
    
    # Recoger resultados
    llm_result = gpu_queue.get() if not gpu_queue.empty() else {"status": "timeout"}
    cpu_result = cpu_queue.get() if not cpu_queue.empty() else {}
    
    return {
        "elapsed_ms": int(elapsed * 1000),
        "llm": llm_result,
        "cpu": cpu_result,
        "parallel": True,
        "estimated_saved_ms": int(max(0, (len(cpu_result) * 500) - (elapsed * 1000)))
    }

def format_output(result: dict) -> str:
    lines = []
    lines.append("══ PIPELINE PARALELO (CPU/GPU) ══")
    lines.append(f"  Tiempo total: {result['elapsed_ms']}ms")
    lines.append(f"  Paralelo: {'SI' if result.get('parallel') else 'NO'}")
    
    llm = result.get("llm", {})
    if llm.get("status") == "ok":
        lines.append("")
        lines.append("── GPU: LLM ──")
        lines.append(f"  {llm['response'][:300]}...")
    else:
        lines.append(f"  LLM: {llm.get('error', 'timeout')}")
    
    cpu = result.get("cpu", {})
    if cpu:
        lines.append("")
        lines.append("── CPU: Verificacion simultanea ──")
        if cpu.get("anti_patrones"):
            lines.append(f"  [Anti-patrones] OK")
        if cpu.get("router"):
            rec = cpu["router"].get("recommendation", {})
            if rec:
                lines.append(f"  [Router] {rec.get('model', '?')} ({cpu['router'].get('confidence', '?')})")
        if cpu.get("preflight"):
            lines.append(f"  [Preflight] OK")
    
    lines.append("════════════════════════════════")
    return "\n".join(lines)

if __name__ == "__main__":
    if not sys.stdin.isatty():
        prompt = sys.stdin.read().strip()
    elif len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
    else:
        print("Uso: echo 'pregunta' | python3 pipeline_parallel.py")
        sys.exit(1)
    
    result = parallel_pipeline(prompt)
    print(format_output(result))
