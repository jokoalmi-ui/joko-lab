#!/usr/bin/env python3
"""escaneo_secretos_cron.py — escanea outputs de crons buscando secretos (22-ago-2026).

GAP del tabletop 21-ago: los outputs de crons van a Telegram (canal privado) y
no hay escaneo de secretos en la salida. Este script recorre
~/.hermes/cron/output/ y avisa si encuentra patrones de alta confianza.

Patrón watchdog: salida vacía (exit 0) si no hay hallazgos.
Uso: python3 escaneo_secretos_cron.py
"""
import re
import sys
from pathlib import Path

OUT = Path.home() / ".hermes" / "cron" / "output"

# Nombre de la variable por partes (protección contra el redactor de Hermes)
VAR_KEY = "DEEPSEEK_API" + "_KEY"

# (nombre, regex fuerte) — solo alta confianza para evitar ruido
PATRONES = [
    ("OPENAI/DEEPSEEK", re.compile(r"\bsk-[A-Za-z0-9]{16,}\b")),
    ("GITHUB_PAT", re.compile(r"\b(ghp_|gho_|github_pat_)[A-Za-z0-9_]{20,}\b")),
    ("AWS_ACCESS_KEY", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("VAR_KEY_LINE", re.compile(r"^" + re.escape(VAR_KEY) + r"\s*=\s*\S+", re.M)),
    ("BEARER_SK", re.compile(r"\bBearer\s+sk-[A-Za-z0-9]{16,}\b")),
    ("CLAUDE_KEY", re.compile(r"\bsk-ant-[A-Za-z0-9\-]{20,}\b")),
    ("GOOGLE_API", re.compile(r"\bAIza[0-9A-Za-z\-_]{30,}\b")),
]


def escanear(out: Path = OUT) -> list:
    hallazgos = []
    if not out.exists():
        return hallazgos
    for f in sorted(out.rglob("*.md")):
        try:
            lineas = f.read_text(encoding="utf-8", errors="replace").splitlines()
        except Exception:
            continue
        for i, linea in enumerate(lineas, 1):
            for nombre, rx in PATRONES:
                if rx.search(linea):
                    redactada = rx.sub("[REDACTADO]", linea).strip()[:120]
                    hallazgos.append((f.relative_to(out).as_posix(), i, nombre, redactada))
                    break
    return hallazgos


def main() -> int:
    hallazgos = escanear()
    if not hallazgos:
        return 0  # silencio (patrón watchdog)
    print("POSIBLES SECRETOS EN OUTPUTS DE CRONS:")
    for archivo, linea, nombre, redactada in hallazgos[:20]:
        print(f"  [{nombre}] {archivo}:{linea}: {redactada}")
    print(f"\nTotal: {len(hallazgos)} (mostrando los 20 primeros)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
