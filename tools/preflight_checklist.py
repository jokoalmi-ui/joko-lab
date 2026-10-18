#!/usr/bin/env python3
"""preflight_checklist.py - Verifica condiciones antes de responder

Ejecuta automaticamente antes de cada respuesta. Comprueba que
no se hayan saltado pasos criticos del protocolo.
"""
import os, sys, json, subprocess

CHECKS = {
    "rag_consultado": {
        "description": "Se ha consultado el RAG (Context Builder)",
        "command": "test -f /tmp/.rag_consultado",
        "critical": True,
        "pass_msg": "Contexto RAG recuperado",
        "fail_msg": "NO se consulto el RAG"
    },
    "anti_patrones_verificados": {
        "description": "Se verificaron anti-patrones del modelo destino",
        "command": "test -f /tmp/.antipatrones_verificados",
        "critical": True,
        "pass_msg": "Anti-patrones verificados",
        "fail_msg": "Anti-patrones NO verificados"
    },
    "ficha_modelo_consultada": {
        "description": "Se consulto la ficha del modelo seleccionado",
        "command": "test -f /tmp/.ficha_consultada",
        "critical": False,
        "pass_msg": "Ficha de modelo consultada",
        "fail_msg": "Ficha de modelo NO consultada"
    },
    "max_tokens_verificado": {
        "description": "max_tokens >= minimo requerido por el modelo",
        "command": "test -f /tmp/.max_tokens_ok",
        "critical": True,
        "pass_msg": "max_tokens suficiente",
        "fail_msg": "max_tokens puede ser insuficiente"
    },
    "temperature_verificada": {
        "description": "Temperature dentro del rango recomendado",
        "command": "test -f /tmp/.temperature_ok",
        "critical": False,
        "pass_msg": "Temperature en rango",
        "fail_msg": "Temperature fuera de rango recomendado"
    },
    "modelo_no_descartado": {
        "description": "El modelo no esta en la lista de descartados",
        "command": "test -f /tmp/.modelo_activo",
        "critical": True,
        "pass_msg": "Modelo activo y no descartado",
        "fail_msg": "MODELO DESCARTADO — no usar"
    }
}

def run_checks():
    results = []
    all_pass = True
    
    for check_id, check in CHECKS.items():
        passed = os.system(check["command"]) == 0
        if not passed and check["critical"]:
            all_pass = False
        results.append((check_id, check, passed))
    
    return results, all_pass

def mark_check(check_id: str):
    """Marca una verificacion como completada"""
    markers = {
        "rag_consultado": "/tmp/.rag_consultado",
        "anti_patrones_verificados": "/tmp/.antipatrones_verificados",
        "ficha_modelo_consultada": "/tmp/.ficha_consultada",
        "max_tokens_verificado": "/tmp/.max_tokens_ok",
        "temperature_verificada": "/tmp/.temperature_ok",
        "modelo_no_descartado": "/tmp/.modelo_activo",
    }
    if check_id in markers:
        open(markers[check_id], "w").close()

def clear_checks():
    """Limpia todas las marcas al inicio de una nueva consulta"""
    for check_id in CHECKS:
        marker = f"/tmp/.{check_id}"
        if os.path.exists(marker):
            os.remove(marker)

def format_report(results: list, all_pass: bool):
    lines = []
    lines.append("── PRE-FLIGHT CHECKLIST ──")
    
    for check_id, check, passed in results:
        status = "✅" if passed else "❌"
        msg = check["pass_msg"] if passed else check["fail_msg"]
        critical = " [CRITICO]" if check["critical"] and not passed else ""
        lines.append(f"  {status} {msg}{critical}")
    
    if all_pass:
        lines.append("  ✅ Todos los checks superados")
    else:
        lines.append("  ⚠ ALGUN CHECK CRITICO HA FALLADO")
    
    lines.append("──────────────────────────")
    return "\n".join(lines)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "mark":
        for check_id in sys.argv[2:]:
            mark_check(check_id)
    elif len(sys.argv) > 1 and sys.argv[1] == "clear":
        clear_checks()
    else:
        results, all_pass = run_checks()
        print(format_report(results, all_pass))
        sys.exit(0 if all_pass else 1)
