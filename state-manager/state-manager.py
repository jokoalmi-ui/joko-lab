#!/usr/bin/env python3
"""State Manager de Joko Lab v3.
Recopila estado del laboratorio cada 60 segundos y escribe state.json.
Contrato definido en state.schema.json.

Uso:
  python3 state-manager.py                 # una ejecución
  python3 state-manager.py --watch         # bucle cada 60s
"""

import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# ─── Rutas ───────────────────────────────────────────────────────────────────
STATE_FILE = Path("/mnt/ssd_ia_datos/lab-state/state.json")
LOG_FILE = Path("/mnt/ssd_ia_datos/lab-state/state-manager.log")
SCHEMA_FILE = Path("/mnt/ssd_ia_datos/lab-state/state.schema.json")


def log(msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def cmd(args: list[str], timeout=10) -> str:
    """Ejecuta un comando y devuelve stdout. Vacío si falla."""
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip()
    except Exception:
        return ""


def get_gpu() -> dict:
    """Estado de la GPU via nvidia-smi."""
    out = cmd([
        "nvidia-smi",
        "--query-gpu=name,memory.total,memory.used,memory.free,utilization.gpu,temperature.gpu",
        "--format=csv,noheader,nounits"
    ])
    if not out:
        return {
            "modelo": "no detectada",
            "vram_total_mb": 0, "vram_usada_mb": 0, "vram_libre_mb": 0,
            "temp_c": 0, "utilizacion_pct": 0
        }
    parts = [p.strip() for p in out.split(",")]
    try:
        return {
            "modelo": parts[0] if len(parts) > 0 else "desconocido",
            "vram_total_mb": int(float(parts[1])) if len(parts) > 1 else 0,
            "vram_usada_mb": int(float(parts[2])) if len(parts) > 2 else 0,
            "vram_libre_mb": int(float(parts[3])) if len(parts) > 3 else 0,
            "utilizacion_pct": int(float(parts[4])) if len(parts) > 4 else 0,
            "temp_c": int(float(parts[5])) if len(parts) > 5 else 0,
        }
    except (ValueError, IndexError):
        return {
            "modelo": "error-parsing", "vram_total_mb": 0, "vram_usada_mb": 0,
            "vram_libre_mb": 0, "temp_c": 0, "utilizacion_pct": 0
        }


def get_system() -> dict:
    """RAM, CPU, disco desde /proc y df."""
    # RAM
    ram = {}
    try:
        with open("/proc/meminfo") as f:
            for line in f:
                for key in ("MemTotal", "MemFree", "MemAvailable"):
                    if line.startswith(key + ":"):
                        val = int(line.split()[1]) // 1024  # kB → MB
                        ram[key] = val
    except Exception:
        ram = {"MemTotal": 0, "MemFree": 0, "MemAvailable": 0}

    # CPU load
    load = 0.0
    try:
        load = float(open("/proc/loadavg").read().split()[0])
    except Exception:
        pass

    # Disco
    disco_root = disco_ssd = 0
    for line in cmd(["df", "-B1G", "--output=target,avail"]).split("\n"):
        parts = line.split()
        if len(parts) == 2:
            mount, avail = parts[0], parts[1]
            if mount == "/":
                disco_root = int(avail)
            elif mount == "/mnt/ssd_ia_datos":
                disco_ssd = int(avail)

    return {
        "ram_total_gb": round(ram.get("MemTotal", 0) / 1024, 1),
        "ram_libre_gb": round(ram.get("MemFree", 0) / 1024, 1),
        "ram_disponible_gb": round(ram.get("MemAvailable", 0) / 1024, 1),
        "cpu_load": load,
        "disco_root_libre_gb": disco_root,
        "disco_ssd_libre_gb": disco_ssd,
    }


def check_ollama() -> dict:
    """Comprueba si Ollama responde y qué modelos tiene."""
    r = cmd(["curl", "-s", "--max-time", "3", "http://localhost:11434/api/tags"])
    activo = bool(r)
    version = ""
    modelos = []
    modelo_cargado = None

    if activo:
        # Versión vía exec si estamos en el host
        v = cmd(["docker", "compose", "-f", "/home/jokoalmi/automation-stack/docker-compose.yml",
                  "exec", "ollama", "ollama", "--version"], timeout=5)
        version = v.replace("ollama version is ", "").strip() if v else ""

        # Modelos disponibles
        try:
            data = json.loads(r)
            modelos = [m["name"] for m in data.get("models", [])]
        except Exception:
            pass

        # Modelo cargado ahora
        ps = cmd(["curl", "-s", "--max-time", "3", "http://localhost:11434/api/ps"])
        if ps:
            try:
                pdata = json.loads(ps)
                if pdata.get("models"):
                    modelo_cargado = pdata["models"][0].get("name")
            except Exception:
                pass

    return {
        "activo": activo,
        "version": version or None,
        "modelos": modelos,
        "modelo_cargado": modelo_cargado,
    }


def check_lmstudio() -> dict:
    """Comprueba si LM Studio responde y obtiene modelos."""
    r = cmd(["curl", "-s", "--max-time", "3", "http://localhost:1234/api/v0/models"])
    activo = bool(r)
    modelos = []
    if activo:
        try:
            data = json.loads(r)
            modelos = [m["id"] for m in data.get("data", []) if m.get("type") in ("vlm", "llm")]
        except Exception:
            pass
    return {"activo": activo, "version": None, "modelos": modelos}


def check_n8n() -> dict:
    """Comprueba si n8n responde en puerto 5678."""
    r = cmd(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
              "--max-time", "3", "http://localhost:5678/healthz"])
    activo = r in ("200", "204")
    version = ""
    if activo:
        logs = cmd(["docker", "compose", "-f", "/home/jokoalmi/automation-stack/docker-compose.yml",
                     "logs", "--tail=30", "n8n"], timeout=5)
        for line in logs.split("\n"):
            if "Version:" in line:
                version = line.split("Version:")[-1].strip()
                break
    return {"activo": activo, "version": version or None}


def check_service(name: str, port: int) -> dict:
    """Comprueba si un servicio responde en un puerto (solo conectividad)."""
    r = cmd(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
              "--max-time", "3", f"http://localhost:{port}"])
    return {"activo": r in ("200", "204", "302", "404")}


SECRETS_DIR = Path("/mnt/ssd_ia_datos/lab-state/secrets")


def read_secret(name: str) -> str:
    """Lee una clave de archivo. Vacío si no existe."""
    path = SECRETS_DIR / name
    if path.exists():
        return path.read_text().strip()
    return ""


def check_cloud(name: str, url: str, api_key: str = "") -> dict:
    """Comprueba si una API cloud responde. Opcionalmente con API key."""
    headers = []
    params = ""
    if api_key:
        if name == "gemini":
            params = f"?key={api_key}"
        else:
            headers = ["-H", f"Authorization: Bearer {api_key}"]

    r = cmd(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
              "--max-time", "5", url + params] + headers)
    # 200/201 = autenticado y OK
    # 204 = sin contenido pero OK
    # 401/403 = API existe pero key inválida — NO considerar como disponible
    disponible = r in ("200", "201", "204")
    return {"disponible": disponible, "saldo_usd": None, "latencia_ms": None}


def get_policies_state() -> dict:
    """Evalúa políticas básicas (hora, ahorro)."""
    ahora = datetime.now()
    hora_str = ahora.strftime("%H:%M")

    # Franja horaria según horario.yaml
    hora_int = ahora.hour + ahora.minute / 60
    if 3 <= hora_int < 12:
        franja = "03:00-12:00"
    else:
        franja = "12:00-03:00"

    return {
        "hora": {
            "actual": hora_str,
            "franja_activa": franja,
        },
        "ahorro": {
            "activo": False,  # reservado para futura política
        }
    }


def collect_state() -> dict:
    """Recopila todo el estado. Combina datos rápidos (cada tick) con lentos (cada 5 ticks)."""
    return _merge_state(_collect_fast(), _collect_slow())


def _collect_fast() -> dict:
    """Datos que cambian rápido: GPU, n8n healthz, cloud disponibilidad, hora."""
    gpu = get_gpu()
    n8n = check_n8n()
    gemini_key = read_secret("gemini.key")
    cloud = {
        "deepseek": check_cloud("deepseek", "https://api.deepseek.com/v1/models"),
        "gemini": check_cloud("gemini", "https://generativelanguage.googleapis.com/v1beta/models", api_key=gemini_key),
    }
    policies = get_policies_state()
    return {"gpu": gpu, "cloud": cloud, "policies": policies, "n8n": n8n}


_fast_cache = {}  # cache para datos lentos


def _collect_slow() -> dict:
    """Datos que cambian lento: versiones, modelos instalados, servicios estables."""
    system = get_system()
    services = {
        "ollama": check_ollama(),
        "lmstudio": check_lmstudio(),
        "stirling_pdf": check_service("stirling-pdf", 8081),
        "pdf_cleaner": check_service("pdf-cleaner", 8000),
        "monitor_flask": check_service("monitor-flask", 5000),
    }
    return {"system": system, "services": services}


def _merge_state(fast: dict, slow: dict) -> dict:
    """Combina fast + slow en un solo state.json."""
    state = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "gpu": fast.get("gpu", {}),
        "system": slow.get("system", {}),
        "services": {
            "ollama": slow.get("services", {}).get("ollama", {"activo": False, "version": None, "modelos": [], "modelo_cargado": None}),
            "lmstudio": slow.get("services", {}).get("lmstudio", {"activo": False, "version": None, "modelos": []}),
            "n8n": fast.get("n8n", {"activo": False, "version": None}),
            "stirling_pdf": slow.get("services", {}).get("stirling_pdf", {"activo": False}),
            "pdf_cleaner": slow.get("services", {}).get("pdf_cleaner", {"activo": False}),
            "monitor_flask": slow.get("services", {}).get("monitor_flask", {"activo": False}),
        },
        "cloud": fast.get("cloud", {}),
        "policies": fast.get("policies", {}),
    }
    return state


def write_state(state: dict):
    """Escribe state.json atómicamente."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = STATE_FILE.with_suffix(".tmp")
    with open(tmp, "w") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
    tmp.rename(STATE_FILE)
    log(f"state.json escrito ({len(json.dumps(state))} bytes)")


def run_once():
    """Una ejecución completa: fast + slow siempre."""
    state = _merge_state(_collect_fast(), _collect_slow())
    write_state(state)
    log("Estado actualizado.")


def run_watch(fast_interval=60, slow_interval=5):
    """Bucle principal. fast_interval en segundos, slow_interval en ticks."""
    log(f"Modo watch: fast cada {fast_interval}s, slow cada {slow_interval} ticks. Ctrl+C para salir.")
    tick = 0
    slow_data = _collect_slow()
    while True:
        fast_data = _collect_fast()
        state = _merge_state(fast_data, slow_data)
        write_state(state)
        tick += 1
        if tick % slow_interval == 0:
            log("Tick lento: recopilando datos estables...")
            slow_data = _collect_slow()
        time.sleep(fast_interval)


if __name__ == "__main__":
    if "--watch" in sys.argv:
        run_watch()
    else:
        run_once()
