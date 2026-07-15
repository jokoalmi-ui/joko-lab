#!/usr/bin/env python3
"""
Decision Engine de Joko Lab v3.
Determinista. Sin LLM. Sin modificar config.yaml.

Lee state.json y policies/*.yaml, aplica precedencia y devuelve proveedor + modelo.

Uso:
  from decision_engine import decide
  resultado = decide()
  # -> {"provider": "gemini", "model": "gemini-2.5-pro", "reason": "..."}
"""

import json
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    import yaml
except ImportError:
    yaml = None  # fallback manual si no está instalado


# ─── Rutas ───────────────────────────────────────────────────────────────────
LAB_STATE = Path("/mnt/ssd_ia_datos/lab-state")
STATE_FILE = LAB_STATE / "state.json"
ULTIMA_DECISION = LAB_STATE / "ultima-decision.json"
POLICIES_DIR = LAB_STATE / "policies"
FALLBACK_PROVIDER = "deepseek"
FALLBACK_MODEL = "deepseek-v4-flash"


# ─── Carga YAML (con fallback sin librería externa) ──────────────────────────
def _parse_yaml_simple(text: str) -> dict:
    """Parser YAML mínimo para políticas simples (sin anidación compleja)."""
    result = {}
    current_key = None
    current_list = []
    in_list = False
    for line in text.split("\n"):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if not line.startswith(" ") and not line.startswith("\t"):
            in_list = False
            if current_key and current_list:
                result[current_key] = current_list
                current_list = []
            if ":" in stripped:
                current_key = stripped.split(":")[0].strip()
                rest = ":".join(stripped.split(":")[1:]).strip()
                if rest:
                    result[current_key] = _parse_value(rest)
                else:
                    result[current_key] = {}
                    current_list = []
        elif stripped.startswith("- "):
            in_list = True
            current_list.append(_parse_value(stripped[2:]))
    if current_key and current_list:
        result[current_key] = current_list
    return result


def _parse_value(v: str):
    v = v.strip().strip('"').strip("'")
    if v.lower() == "true":
        return True
    if v.lower() == "false":
        return False
    if v.lower() == "null" or v.lower() == "none":
        return None
    try:
        return int(v)
    except ValueError:
        pass
    try:
        return float(v)
    except ValueError:
        pass
    return v


def load_yaml(path: Path) -> dict:
    """Carga un YAML, con o sin librería PyYAML."""
    if not path.exists():
        return {}
    text = path.read_text()
    if yaml:
        data = yaml.safe_load(text)
        return data if isinstance(data, dict) else {}
    else:
        return _parse_yaml_simple(text)


# ─── Carga de estado ─────────────────────────────────────────────────────────
def load_state() -> dict:
    """Carga state.json. Si no existe, devuelve dict vacío."""
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def load_ultima_decision() -> Optional[dict]:
    """Carga la última decisión guardada (fallback en lab-state/)."""
    if ULTIMA_DECISION.exists():
        try:
            return json.loads(ULTIMA_DECISION.read_text())
        except (json.JSONDecodeError, OSError):
            return None
    return None


# ─── Evaluación de políticas ────────────────────────────────────────────────
# Precedencia: 1. privacidad → 2. disponibilidad → 3. costes → 4. horario → 5. modelos

def evaluar_privacidad(state: dict, policies: dict) -> Optional[dict]:
    """Política 1. Si datos_sensiles=true, forzar local."""
    priv = policies.get("privacidad", {})
    if priv.get("datos_sensibles", False):
        return {
            "provider": "ollama",
            "model": policies.get("modelos", {}).get("por_proveedor", {}).get("ollama", {}).get("default", "llama31-8b-64k"),
            "reason": "Privacidad: datos sensibles, forzar modo local",
        }
    return None


def evaluar_disponibilidad(state: dict, policies: dict) -> Optional[dict]:
    """Política 2. Valida disponibilidad de proveedores según disponibilidad.yaml.
    - Si el proveedor que tocaría según horario no está disponible,
      hace fallback al siguiente disponible.
    - Si ningún proveedor cloud está disponible, fuerza local.
    - Si todo está caído, reporta error."""
    disp = policies.get("disponibilidad", {})
    reglas = disp.get("reglas", [])
    cloud = state.get("cloud", {})
    services = state.get("services", {})

    deepseek_ok = cloud.get("deepseek", {}).get("disponible", False)
    gemini_ok = cloud.get("gemini", {}).get("disponible", False)
    ollama_ok = services.get("ollama", {}).get("activo", False)

    # Si todos caídos, el sistema no puede operar
    if not deepseek_ok and not gemini_ok and not ollama_ok:
        return {
            "provider": "none",
            "model": "none",
            "reason": "Disponibilidad: ningún proveedor disponible",
        }

    # Si solo un cloud está disponible, forzar ese
    if deepseek_ok and not gemini_ok:
        return {
            "provider": "deepseek",
            "model": _modelo_por_proveedor("deepseek", policies),
            "reason": "Disponibilidad: Gemini no disponible, forzando DeepSeek",
        }
    if gemini_ok and not deepseek_ok:
        return {
            "provider": "gemini",
            "model": _modelo_por_proveedor("gemini", policies),
            "reason": "Disponibilidad: DeepSeek no disponible, forzando Gemini",
        }

    # Si ningún cloud está disponible pero Ollama sí, forzar local
    if not deepseek_ok and not gemini_ok and ollama_ok:
        return {
            "provider": "ollama",
            "model": _modelo_por_proveedor("ollama", policies),
            "reason": "Disponibilidad: cloud no disponible, forzando local",
        }

    return None


def evaluar_costes(state: dict, policies: dict) -> Optional[dict]:
    """Política 3. Si saldo mínimo no se cumple, forzar local."""
    costes = policies.get("costes", {})
    limites = costes.get("limites", {})
    saldo_minimo = limites.get("saldo_minimo_usd", 0)
    cloud = state.get("cloud", {})

    if saldo_minimo > 0:
        ds_saldo = cloud.get("deepseek", {}).get("saldo_usd")
        gm_saldo = cloud.get("gemini", {}).get("saldo_usd")

        # Si tenemos datos de saldo y están por debajo del mínimo
        if ds_saldo is not None and ds_saldo < saldo_minimo:
            return {
                "provider": "ollama",
                "model": "llama31-8b-64k",
                "reason": f"Costes: saldo DeepSeek ({ds_saldo} USD) bajo mínimo ({saldo_minimo} USD)",
            }
        if gm_saldo is not None and gm_saldo < saldo_minimo:
            return {
                "provider": "ollama",  # DeepSeek sigue disponible
                "model": "llama31-8b-64k",
                "reason": f"Costes: saldo Gemini ({gm_saldo} USD) bajo mínimo ({saldo_minimo} USD)",
            }

    return None


def evaluar_horario(state: dict, policies: dict) -> Optional[dict]:
    """Política 4. Elegir proveedor según la hora."""
    horario = policies.get("horario", {})
    reglas = horario.get("reglas", [])
    ahora = state.get("policies", {}).get("hora", {}).get("actual", "")
    franja_activa = state.get("policies", {}).get("hora", {}).get("franja_activa", "")

    if not ahora:
        return None

    # Convertir hora actual a minutos para comparar
    try:
        h, m = ahora.split(":")
        ahora_min = int(h) * 60 + int(m)
    except (ValueError, IndexError):
        return None

    for regla in reglas:
        rango = regla.get("horas", "")
        proveedor = regla.get("proveedor", "")
        if not rango or not proveedor:
            continue
        try:
            inicio_str, fin_str = rango.split("-")
            h_i, m_i = inicio_str.split(":")
            h_f, m_f = fin_str.split(":")
            inicio_min = int(h_i) * 60 + int(m_i)
            fin_min = int(h_f) * 60 + int(m_f)
        except (ValueError, IndexError):
            continue

        # Manejar rangos que cruzan la medianoche (ej: 12:00-03:00)
        if fin_min <= inicio_min:
            # Cruza medianoche
            if ahora_min >= inicio_min or ahora_min < fin_min:
                modelo = _modelo_por_proveedor(proveedor, policies)
                return {
                    "provider": proveedor,
                    "model": modelo,
                    "reason": f"Horario: {rango}, ahora {ahora}",
                }
        else:
            if inicio_min <= ahora_min < fin_min:
                modelo = _modelo_por_proveedor(proveedor, policies)
                return {
                    "provider": proveedor,
                    "model": modelo,
                    "reason": f"Horario: {rango}, ahora {ahora}",
                }

    # Fallback de horario.yaml
    fb = horario.get("fallback", {})
    proveedor_fb = fb.get("proveedor", FALLBACK_PROVIDER)
    modelo_fb = _modelo_por_proveedor(proveedor_fb, policies)
    return {
        "provider": proveedor_fb,
        "model": modelo_fb,
        "reason": f"Horario: sin regla aplicable, fallback a {proveedor_fb}",
    }


def evaluar_preferencias(state: dict, policies: dict) -> Optional[dict]:
    """Política 5. Preferencia por defecto según preferencias.yaml."""
    pref = policies.get("preferencias", {})
    fb = pref.get("fallback", {})
    proveedor = fb.get("proveedor", FALLBACK_PROVIDER)
    modelo = fb.get("modelo", FALLBACK_MODEL)
    return {
        "provider": proveedor,
        "model": modelo,
        "reason": f"Preferencia por defecto: {proveedor}/{modelo}",
    }


def _modelo_por_proveedor(proveedor: str, policies: dict) -> str:
    """Obtiene el modelo por defecto para un proveedor según política de modelos."""
    modelos = policies.get("modelos", {})
    por_prov = modelos.get("por_proveedor", {})
    info = por_prov.get(proveedor, {})
    return info.get("default", FALLBACK_MODEL)


# ─── Algoritmo principal ────────────────────────────────────────────────────
def decide(task_hint: str = "") -> dict:
    """
    Punto de entrada del Decision Engine.
    Evalúa políticas en orden de precedencia y devuelve:
      {"provider": str, "model": str, "reason": str}

    Args:
        task_hint: Pista opcional sobre el tipo de tarea (reservado para futuro).
    """
    start = time.time()
    state = load_state()
    if not state:
        # Fallback: state.json no existe
        ultima = load_ultima_decision()
        if ultima:
            result = ultima
            result["reason"] = "FALLBACK: state.json no disponible, usando última decisión"
        else:
            result = {
                "provider": FALLBACK_PROVIDER,
                "model": FALLBACK_MODEL,
                "reason": "FALLBACK: state.json no disponible, usando DeepSeek por defecto",
            }
        return result

    # Cargar políticas
    policies = {}
    for yaml_file in POLICIES_DIR.glob("*.yaml"):
        name = yaml_file.stem
        policies[name] = load_yaml(yaml_file)

    # Evaluar en orden de precedencia
    evaluadores = [
        ("privacidad", evaluar_privacidad),
        ("disponibilidad", evaluar_disponibilidad),
        ("costes", evaluar_costes),
        ("horario", evaluar_horario),
        ("preferencias", evaluar_preferencias),
    ]

    result = None
    for nombre, fn in evaluadores:
        try:
            r = fn(state, policies)
            if r is not None:
                result = r
                # Añadir nombre de política al reason si no está ya
                if not r["reason"].startswith(nombre.capitalize()):
                    result["reason"] = f"{nombre.capitalize()}: {r['reason']}"
                break
        except Exception as e:
            result = {
                "provider": FALLBACK_PROVIDER,
                "model": FALLBACK_MODEL,
                "reason": f"ERROR en política '{nombre}': {e}",
            }
            break

    if result is None:
        result = {
            "provider": FALLBACK_PROVIDER,
            "model": FALLBACK_MODEL,
            "reason": "Ninguna política aplicable, fallback por defecto",
        }

    return result


# ─── CLI ─────────────────────────────────────────────────────────────────────
def main():
    import sys
    if "--json" in sys.argv:
        result = decide()
        print(json.dumps(result, indent=2))
    elif "--reason" in sys.argv:
        result = decide()
        print(result["reason"])
    elif "--provider" in sys.argv:
        result = decide()
        print(f"{result['provider']}/{result['model']}")
    else:
        result = decide()
        print(f"Proveedor: {result['provider']}")
        print(f"Modelo:    {result['model']}")
        print(f"Razón:     {result['reason']}")


if __name__ == "__main__":
    main()
