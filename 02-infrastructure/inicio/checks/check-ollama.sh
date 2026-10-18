#!/bin/bash
# check-ollama.sh — Verifica que Ollama responde
# Retorna: 0 = OK, 1 = WARNING, 2 = ERROR

if ! curl -s --max-time 3 http://localhost:11434/api/tags >/dev/null 2>&1; then
    echo "ERROR: Ollama no responde en localhost:11434"
    exit 2
fi

MODELS=$(curl -s --max-time 3 http://localhost:11434/api/tags 2>/dev/null | python3 -c "import sys,json; data=json.load(sys.stdin); print(len(data.get('models',[])))" 2>/dev/null)
if [ -z "$MODELS" ]; then
    MODELS="0"
fi

echo "OK: $MODELS modelos disponibles"
exit 0
