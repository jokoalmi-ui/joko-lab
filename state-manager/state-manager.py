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
SALDO_HISTORY_FILE = Path("/mnt/ssd_ia_datos/lab-state/saldo_history.json")

# ─── Constantes de coste ──────────────────────────────────────────────────────
TOKENS_POR_SESION=12500  # calculado de 12 sesiones, 2.44 MB, ~25% overhead (redondeado)
SESIONES_POR_DIA=4                # 12 sesiones / 3 días, recalibrar a los 7 días
PRECIO_DEEPSEEK = 0.875e-6        # $/token media 3:1 input/output
PRECIO_GEMINI = 0.75e-6           # $/token media 3:1 input/output


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
        "ram_mb": ram.get("MemTotal", 0),
        "ram_libre_mb": ram.get("MemFree", 0),
        "ram_disponible_mb": ram.get("MemAvailable", 0),
        "cpu_load": round(load, 2),
        "disco_root_gb": disco_root,
        "disco_ssd_gb": disco_ssd,
    }


def read_secret(name: str) -> str:
    """Lee un secreto de SECRETS_DIR. Devuelve '' si no existe."""
    path = Path("/mnt/ssd_ia_datos/lab-state/secrets") / name
    try:
        return path.read_text().strip()
    except Exception:
        return ""


def check_service(service: str, port: int) -> dict:
    """Comprueba si un servicio responde en un puerto."""
    out = cmd(["ss", "-tlnp"], timeout=5)
    return {"activo": f":{port}" in out}


def check_n8n() -> dict:
    """Healthcheck de n8n via HTTP."""
    out = cmd(["curl", "-sf", "--max-time", "5", "http://127.0.0.1:5678/healthz"])
    if out:
        return {"activo": True, "version": out.strip()[:20]}
    return {"activo": False, "version": None}


def check_ollama() -> dict:
    """Modelos instalados en Ollama via Docker."""
    out = cmd([
        "docker", "compose", "-f", "/home/jokoalmi/automation-stack/docker-compose.yml",
        "exec", "-T", "ollama", "ollama", "list"
    ])
    modelos = []
    version = None
    if out:
        lines = out.strip().split("\n")
        for line in lines[1:]:
            parts = line.split()
            if parts:
                modelos.append(parts[0])
    # Versión
    ver = cmd([
        "docker", "compose", "-f", "/home/jokoalmi/automation-stack/docker-compose.yml",
        "exec", "-T", "ollama", "ollama", "--version"
    ])
    if ver:
        version = ver.strip()
    return {
        "activo": len(modelos) > 0 or bool(ver),
        "version": version,
        "modelos": modelos,
        "modelo_cargado": None,
    }


def check_lmstudio() -> dict:
    """Estado de LM Studio via API HTTP."""
    out = cmd(["curl", "-sf", "--max-time", "5", "http://localhost:1234/api/v0/models"])
    modelos = []
    if out:
        try:
            data = json.loads(out)
            modelos = [m["id"] for m in data.get("data", [])]
        except (json.JSONDecodeError, KeyError, TypeError):
            pass
    return {"activo": len(modelos) > 0, "version": None, "modelos": modelos}


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


# ─── check_cost(): Sprint 3.4 — Observabilidad de costes reales ──────────────

def _contar_sesiones() -> int:
    """Usa SESIONES_POR_DIA constante. No cuenta archivos acumulados (daria sobreestimacion creciente)."""
    return SESIONES_POR_DIA


def _leer_saldo_anterior() -> tuple[float | None, str | None]:
    """Lee el saldo anterior guardado de saldo_history.json.
    Devuelve (saldo_anterior, timestamp) o (None, None)."""
    if not SALDO_HISTORY_FILE.exists():
        return None, None
    try:
        data = json.loads(SALDO_HISTORY_FILE.read_text())
        return data.get("deepseek_saldo_anterior"), data.get("ultima_actualizacion")
    except (json.JSONDecodeError, KeyError):
        return None, None


def _guardar_saldo_actual(saldo: float | None):
    """Guarda el saldo actual para la próxima comparación."""
    data = {
        "deepseek_saldo_anterior": saldo,
        "ultima_actualizacion": datetime.now(timezone.utc).isoformat(),
    }
    SALDO_HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(SALDO_HISTORY_FILE, "w") as f:
        json.dump(data, f, indent=2)


def check_cost() -> dict:
    """Consulta costes reales de DeepSeek y estima Gemini.

    DeepSeek: API directa vía /user/balance (único endpoint oficial).
              El gasto diario se calcula por diferencia de saldo entre lecturas.
              Si el saldo subió (recarga manual), se marca como recarga_detectada.

    Gemini:   No tiene API de billing con API key simple. Solo estimación.
    """
    costes = {}

    # ── DeepSeek: API directa ──────────────────────────────────────────────
    ds_saldo = None
    ds_fuente = "estimacion"
    ds_gasto = None
    ds_recarga = None

    try:
        key = read_secret("deepseek.key")
        if key:
            r = cmd([
                "curl", "-s", "--max-time", "10",
                "-H", f"Authorization: Bearer {key}",
                "-H", "Accept: application/json",
                "https://api.deepseek.com/user/balance"
            ])
            if r:
                data = json.loads(r)
                ds_saldo = float(data["balance_infos"][0]["total_balance"])
                ds_fuente = "api_directa"

                # Comparar con saldo anterior para calcular gasto
                saldo_anterior, ts_anterior = _leer_saldo_anterior()
                if saldo_anterior is not None:
                    diff = ds_saldo - saldo_anterior
                    if diff < 0:
                        # Gasto real: el saldo bajó
                        ds_gasto = round(abs(diff), 4)
                        log(f"DeepSeek gasto real: ${ds_gasto:.4f} "
                            f"(saldo: {saldo_anterior} → {ds_saldo})")
                    elif diff > 0:
                        # Recarga manual detectada
                        ds_recarga = True
                        log(f"⚠️ DeepSeek: saldo subió de {saldo_anterior} a {ds_saldo} "
                            f"— recarga manual detectada. Gasto no computable.")
                    else:
                        # Sin cambio
                        log(f"DeepSeek saldo sin cambios: ${ds_saldo}")
                else:
                    log(f"DeepSeek saldo actual: ${ds_saldo} "
                        f"(primera lectura, sin referencia anterior)")

                # Guardar saldo actual para próxima comparación
                _guardar_saldo_actual(ds_saldo)
            else:
                log("⚠️ DeepSeek: /user/balance no devolvió datos")
        else:
            log("⚠️ DeepSeek: no hay API key para consultar balance")
    except Exception as e:
        log(f"⚠️ DeepSeek: error al consultar balance — {e}")

    # ── Gemini: solo estimación ────────────────────────────────────────────
    log("⚠️ Gemini: coste estimado — no hay API de billing disponible con API key simple")

    # ── Estimación basada en actividad ──────────────────────────────────────
    sesiones = _contar_sesiones()
    coste_estimado_ds = round(sesiones * TOKENS_POR_SESION * PRECIO_DEEPSEEK, 6)
    coste_estimado_gm = round(sesiones * TOKENS_POR_SESION * PRECIO_GEMINI, 6)

    costes["deepseek"] = {
        "saldo_actual_usd": ds_saldo,
        "fuente": ds_fuente,
        "gasto_diario_estimado_usd": ds_gasto if ds_fuente == "api_directa" else coste_estimado_ds,
        "recarga_detectada": ds_recarga if ds_recarga else (False if ds_fuente == "api_directa" else None),
        "ultima_actualizacion": datetime.now(timezone.utc).isoformat(),
    }
    costes["gemini"] = {
        "saldo_actual_usd": None,
        "fuente": "estimacion",
        "gasto_diario_estimado_usd": coste_estimado_gm,
        "ultima_actualizacion": datetime.now(timezone.utc).isoformat(),
    }

    total = round((coste_estimado_ds + coste_estimado_gm), 6)
    costes["total_diario_estimado_usd"] = total
    costes["total_mensual_estimado_usd"] = round(total * 30, 4)
    costes["nota"] = "Gemini es estimado — solo DeepSeek tiene API de billing (/user/balance)"

    log(f"Costes: DeepSeek=${costes['deepseek']['gasto_diario_estimado_usd']} "
        f"Gemini=${costes['gemini']['gasto_diario_estimado_usd']} "
        f"total=${total}/día ({sesiones} sesiones, {TOKENS_POR_SESION} tok/sesión)")

    return costes


# ─── Fin check_cost() ────────────────────────────────────────────────────────


def collect_state() -> dict:
    """Recopila todo el estado. Combina datos rápidos (cada tick) con lentos (cada 5 ticks)."""
    return _merge_state(_collect_fast(), _collect_slow())


def _collect_fast() -> dict:
    """Datos que cambian rápido: GPU, n8n healthz, cloud disponibilidad, hora, costes."""
    gpu = get_gpu()
    n8n = check_n8n()
    gemini_key = read_secret("gemini.key")
    deepseek_key = read_secret("deepseek.key")
    cloud = {
        "deepseek": check_cloud("deepseek", "https://api.deepseek.com/v1/models", api_key=deepseek_key),
        "gemini": check_cloud("gemini", "https://generativelanguage.googleapis.com/v1beta/models", api_key=gemini_key),
    }
    policies = get_policies_state()
    costes = check_cost()
    return {"gpu": gpu, "cloud": cloud, "policies": policies, "n8n": n8n, "costes": costes}


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
        "costes": fast.get("costes", {}),
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
