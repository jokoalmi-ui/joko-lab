#!/bin/bash
# consulta-decision.sh — Consulta el Decision Engine / Runtime sin tocar config.
# Uso: bash consulta-decision.sh [hint]  (hint opcional: "codigo", "json", "vision"...)
# Salida: texto formateado con la decisión actual del Router.
set -euo pipefail
HINT="${1:-}"
if [ -n "$HINT" ]; then
    python3 /home/jokoalmi/hermes-lab/runtime/api.py --json 2>/dev/null | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(f\"Decisión actual: provider={d.get('provider')} | model={d.get('model')}\")
    print(f\"Política: {d.get('policy','?')} | Privacidad: {d.get('privacy','?')}\")
    if d.get('reason'): print(f\"Motivo: {d['reason']}\")
except Exception as e:
    print(f'Error leyendo decisión: {e}')
"
else
    python3 /home/jokoalmi/hermes-lab/runtime/api.py --provider 2>/dev/null
fi
