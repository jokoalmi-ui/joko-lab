#!/usr/bin/env python3
"""Analiza una captura de formato de presentacion con la API de Gemini.

Uso: python3 analizar_captura_gemini.py [ruta_imagen]
Lee la key de GOOGLE_API_KEY del .env de Hermes (no la muestra).
"""
import base64
import json
import os
import sys
import urllib.error
import urllib.request

# 1) Key desde el .env (sin exponerla)
KEY = None
ENV_PATH = "/home/jokoalmi/.hermes/.env"
with open(ENV_PATH, errors="replace") as f:
    for line in f:
        line = line.strip()
        if line.startswith("GOOGLE_API_KEY=") and not line.startswith("#"):
            KEY = line.split("=", 1)[1].strip()
            break
if not KEY:
    print("ERROR: GOOGLE_API_KEY no encontrada en", ENV_PATH)
    sys.exit(1)

# 2) Imagen por defecto: la captura del formato notas premium (06-ago)
DEFAULT_IMG = "/home/jokoalmi/.lmstudio/user-files/1786030918389 - 103.png"
path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_IMG
if not os.path.isfile(path):
    print("ERROR: no existe la imagen:", path)
    sys.exit(1)

with open(path, "rb") as f:
    b64 = base64.b64encode(f.read()).decode()
mime = "image/png" if path.lower().endswith(".png") else "image/jpeg"

# 3) Prompt de especificacion fina
PROMPT = (
    "Eres un disenador de presentaciones. Analiza esta captura de un formato de "
    "presentacion tipo notas de cuaderno y devuelve una ESPECIFICACION TECNICA en "
    "espanol para replicarla en HTML/CSS. Incluye:\n"
    "1) PALETA DE COLORES: codigos hex aproximados de fondo, titulos, subtitulos, acentos, checks.\n"
    "2) PAPEL: tipo (liso/rayado/punteado), color exacto, textura, margenes.\n"
    "3) ESPIRAL: posicion (izquierda/derecha), color, grosor, numero de anillas, distancia al borde.\n"
    "4) TIPOGRAFIAS: familia para titulo, cuerpo y texto manuscrito; tamano aprox (px), peso, color.\n"
    "5) ESTRUCTURA: orden vertical completo de los bloques (header, caja punteada, flujo, cita, columnas, estrellas, footer), columnas, jerarquia visual, espaciados aproximados.\n"
    "6) DETALLES: bordes (punteado/solido), esquinas redondeadas, sombras, iconos, estrellas, checks, separadores, CTA final.\n"
    "IMPORTANTE: completa TODOS los puntos 1-6 sin omitir ninguno. Se concreto y numerico donde puedas (px, hex). Responde SOLO la especificacion, sin preambulos."
)

# 4) Modelos candidatos (prueba en orden hasta que uno responda)
MODELS = [
    "gemini-3-flash-preview",
    "gemini-3-flash",
    "gemini-3-pro-preview",
    "gemini-2.5-flash-latest",
    "gemini-2.5-flash",
    "gemini-2.5-pro",
    "gemini-1.5-flash",
]

payload = {
    "contents": [{
        "parts": [
            {"text": PROMPT},
            {"inline_data": {"mime_type": mime, "data": b64}},
        ]
    }],
    "generationConfig": {"temperature": 0.1, "maxOutputTokens": 4096},
}

for model in MODELS:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={KEY}"
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            out = json.loads(r.read())
        text = out["candidates"][0]["content"]["parts"][0]["text"]
        print(f"MODELO USADO: {model}")
        print("=" * 60)
        print(text)
        # Guardar la especificacion completa en un archivo (no depende del pegado del terminal)
        out_path = "/home/jokoalmi/joko-lab/tfm/slides/ESPECIFICACION-GEMINI-portada.txt"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(f"MODELO: {model}\n\n")
            f.write(text)
        print("=" * 60)
        print("Guardado en:", out_path)
        sys.exit(0)
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")[:800]
        print(f"[{model}] HTTP {e.code}: {body[:300]}")
        continue
    except Exception as e:
        print(f"[{model}] ERROR: {e!r}")
        continue

print("Todos los modelos fallaron. Modelos disponibles en la API (solo lectura):")
try:
    url_list = f"https://generativelanguage.googleapis.com/v1beta/models?key={KEY}"
    req = urllib.request.Request(url_list)
    with urllib.request.urlopen(req, timeout=60) as r:
        out = json.loads(r.read())
    for m in out.get("models", []):
        name = m.get("name", "")
        methods = m.get("supportedGenerationMethods", [])
        if "generateContent" in methods:
            print(" -", name)
except Exception as e:
    print("ERROR listando modelos:", repr(e))
