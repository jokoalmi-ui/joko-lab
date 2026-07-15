#!/usr/bin/env python3
"""
Runtime API de Joko Lab v3.
Implementa Runtime.resolve() según CONTRACT.md v1.0.

Uso:
  from runtime.api import resolve
  decision = resolve()

CLI:
  python3 runtime/api.py [--json] [--provider]
"""
import json
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

# ─── El DE es importado como librería ────────────────────────────────────
# Se añade la ruta del proyecto para poder importar decision_engine
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "decision-engine"))

from decision_engine import decide as _decide  # noqa: E402


# ─── Rutas ───────────────────────────────────────────────────────────────
LAB_STATE = Path("/mnt/ssd_ia_datos/lab-state")
ULTIMA_DECISION = LAB_STATE / "ultima-decision.json"
DECISION_LOG = LAB_STATE / "logs" / "decision.log"
DECISION_LEDGER = LAB_STATE / "logs" / "decision-ledger.json"


# ─── Funciones auxiliares ────────────────────────────────────────────────
def _generar_decision_id() -> str:
    """Genera un ID único para cada decisión: YYYYMMDD-HHMMSS-xxxxxxxx."""
    ahora = datetime.now()
    suffix = uuid.uuid4().hex[:8]
    return f"{ahora.strftime('%Y%m%d-%H%M%S')}-{suffix}"


def _determinar_privacy(provider: str) -> str:
    """Determina si la decisión es cloud o local."""
    if provider in ("ollama", "lmstudio"):
        return "local"
    elif provider in ("none",):
        return "unknown"
    return "cloud"


def _determinar_verification(provider: str) -> str:
    """Nivel de verificación según el proveedor."""
    if provider == "none":
        return "NONE"
    if provider == "ollama":
        return "MEDIUM"
    return "LOW"


def _calcular_expires(provider: str) -> str | None:
    """Calcula la expiración de la decisión."""
    if provider == "none":
        return None
    # Las decisiones en cloud expiran en 30 min, local en 60 min
    minutos = 30 if provider != "ollama" else 60
    exp = datetime.now(timezone.utc).astimezone()
    try:
        from datetime import timedelta
        exp = exp + timedelta(minutes=minutos)
    except Exception:
        return None
    return exp.isoformat()


def _registrar_decision(decision: dict, duration_ms: float):
    """Escribe la decisión en ultima-decision.json, decision.log y decision-ledger.json."""
    # ultima-decision.json (sobrescritura)
    ULTIMA_DECISION.parent.mkdir(parents=True, exist_ok=True)
    tmp = ULTIMA_DECISION.with_suffix(".tmp")
    tmp.write_text(json.dumps(decision, indent=2))
    tmp.rename(ULTIMA_DECISION)

    # decision.log (append JSON por línea)
    ts = datetime.now().isoformat()
    log_entry = {
        "timestamp": ts,
        "component": "RuntimeAPI",
        "operation": "resolve",
        "provider": decision["provider"],
        "model": decision["model"],
        "policy": decision["policy"],
        "decision_id": decision["decision_id"],
        "reason": decision["reason"],
        "duration_ms": round(duration_ms, 1),
        "status": "success" if decision["provider"] != "none" else "error",
    }
    with open(DECISION_LOG, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    # decision-ledger.json (historial agregado, útil para consultas)
    # Extraer las políticas involucradas del reason
    policies_involucradas = []
    reason_lower = decision["reason"].lower()
    for p in ["privacidad", "disponibilidad", "costes", "horario", "preferencias"]:
        if decision["policy"] and p in decision["policy"]:
            policies_involucradas.append(f"policy:{p}")
        elif p in reason_lower and f"policy:{p}" not in policies_involucradas:
            policies_involucradas.append(f"policy:{p}")

    ledger_entry = {
        "timestamp": ts,
        "provider": decision["provider"],
        "model": decision["model"],
        "reason": policies_involucradas if policies_involucradas else [f"policy:{decision['policy']}"],
        "latency_ms": round(duration_ms, 1),
        "fallback": "FALLBACK" in decision["reason"],
        "privacy": decision["privacy"],
        "decision_id": decision["decision_id"],
    }
    # El ledger es un JSON array. Si no existe, se crea.
    entries = []
    if DECISION_LEDGER.exists():
        try:
            entries = json.loads(DECISION_LEDGER.read_text())
            if not isinstance(entries, list):
                entries = []
        except (json.JSONDecodeError, OSError):
            entries = []
    entries.append(ledger_entry)
    # Máximo 1000 entradas para que el archivo no crezca indefinidamente
    if len(entries) > 1000:
        entries = entries[-1000:]
    tmp_ledger = DECISION_LEDGER.with_suffix(".tmp")
    tmp_ledger.write_text(json.dumps(entries, indent=2))
    tmp_ledger.rename(DECISION_LEDGER)


# ─── API pública ─────────────────────────────────────────────────────────
def resolve(task_hint: str = "") -> dict:
    """
    Runtime.resolve() — única puerta de entrada al Decision Engine.

    Args:
        task_hint: Pista opcional sobre el tipo de tarea (reservado).

    Returns:
        dict con todos los campos del contrato (provider, model, reason,
        policy, privacy, verification, confidence, expires, decision_id).
    """
    start = time.time()

    # Llamar al DE (puro, solo decide)
    raw = _decide(task_hint)

    duration_ms = (time.time() - start) * 1000

    # Determinar qué política ganó según el reason
    policy_name = "unknown"
    for p in ["privacidad", "disponibilidad", "costes", "horario", "preferencias"]:
        if raw.get("reason", "").lower().startswith(p):
            policy_name = f"{p}.yaml"
            break

    # Construir la respuesta completa del contrato
    decision = {
        "provider": raw.get("provider", "none"),
        "model": raw.get("model", "none"),
        "reason": raw.get("reason", "ERROR: decisión vacía"),
        "policy": policy_name,
        "privacy": _determinar_privacy(raw.get("provider", "none")),
        "verification": _determinar_verification(raw.get("provider", "none")),
        "confidence": 1.0 if raw.get("provider", "none") != "none" else 0.0,
        "expires": _calcular_expires(raw.get("provider", "none")),
        "decision_id": _generar_decision_id(),
    }

    # Registrar la decisión
    _registrar_decision(decision, duration_ms)

    return decision


# ─── CLI ─────────────────────────────────────────────────────────────────
def main():
    if "--json" in sys.argv:
        result = resolve()
        print(json.dumps(result, indent=2))
    elif "--provider" in sys.argv:
        result = resolve()
        print(f"{result['provider']}/{result['model']}")
    else:
        result = resolve()
        print(f"Proveedor:     {result['provider']}")
        print(f"Modelo:        {result['model']}")
        print(f"Razón:         {result['reason']}")
        print(f"Política:      {result['policy']}")
        print(f"Privacidad:    {result['privacy']}")
        print(f"Verificación:  {result['verification']}")
        print(f"Confianza:     {result['confidence']}")
        print(f"Expira:        {result['expires']}")
        print(f"ID Decisión:   {result['decision_id']}")


if __name__ == "__main__":
    main()
