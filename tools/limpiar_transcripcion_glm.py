#!/usr/bin/env python3
"""limpiar_transcripcion_glm.py — Corrige nombres propios y términos técnicos
de una transcripción usando GLM local.

MEJORA 13-ago-2026: whisper `small` transcribe mejor que `base` pero aún falla
con nombres propios ("Munchot"→Moonshot, "Haginface"→HuggingFace). Este script
pasa la transcripción por GLM (modelo de texto local) con un prompt de
corrección que preserva el contenido.

USO:
    python3 limpiar_transcripcion_glm.py <archivo.txt> [salida.txt]
    (si no se da salida, imprime la versión limpia)
"""
import sys
import os
import json
import urllib.request

LM_API = "http://localhost:1234/api/v0/chat/completions"
MODELO = "glm-4.6v-flash"  # usa el modelo cargado por defecto (detecta si hay otro)


def modelo_cargado() -> str:
    """Detecta el modelo cargado en LM Studio (fallback: glm-4.6v-flash)."""
    try:
        with urllib.request.urlopen("http://localhost:1234/api/v0/models", timeout=5) as r:
            d = json.loads(r.read())
        for m in d.get("data", []):
            if m.get("state") == "loaded":
                return m.get("id")
    except Exception:
        pass
    return MODELO


def limpiar(texto: str) -> str:
    """Envía la transcripción a GLM para corregir nombres/tecnicismos."""
    # Recortar a bloques de ~3000 chars para no saturar el contexto
    bloques = [texto[i:i + 3000] for i in range(0, len(texto), 3000)]
    resultado = []
    modelo = modelo_cargado()
    print(f"📝 Limpiando con modelo: {modelo}", flush=True)

    for bloque in bloques:
        payload = {
            "model": modelo,
            "messages": [
                {"role": "system", "content": (
                    "Eres un corrector de transcripciones de audio técnico. "
                    "Corrige nombres propios, marcas y términos técnicos de IA "
                    "que Whisper haya transcrito mal (ej: 'Munchot'→'Moonshot', "
                    "'Haginface'→'HuggingFace', 'llama.cp'→'llama.cpp'). "
                    "Mantén TODO el contenido, solo corrige errores. "
                    "No añadas ni elimines información.")},
                {"role": "user", "content": bloque},
            ],
            "max_tokens": 2500,
            "temperature": 0.1,
        }
        req = urllib.request.Request(
            LM_API, data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=180) as r:
            d = json.loads(r.read())
        resultado.append(d["choices"][0]["message"]["content"])

    return "\n".join(resultado)


def main():
    if len(sys.argv) < 2:
        print("Uso: limpiar_transcripcion_glm.py <archivo.txt> [salida.txt]")
        sys.exit(1)

    entrada = sys.argv[1]
    salida = sys.argv[2] if len(sys.argv) > 2 else None

    with open(entrada, encoding="utf-8") as f:
        texto = f.read()

    print(f"📝 Limpiando {len(texto)} chars con {MODELO}...", flush=True)
    limpio = limpiar(texto)

    if salida:
        with open(salida, "w", encoding="utf-8") as f:
            f.write(limpio)
        print(f"✅ Limpia guardada: {salida}")
    else:
        print(limpio)


if __name__ == "__main__":
    main()
