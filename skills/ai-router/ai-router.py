#!/usr/bin/env python3
"""
ai-router v0.3.0 — Enrutamiento inteligente entre modelos de IA.

Uso:
  python3 ai-router.py "tu consulta"
  python3 ai-router.py --vision /ruta/imagen.jpg "descripción opcional"
  python3 ai-router.py --diagnostico

Criterios:
  - Privacidad → Ollama (local)
  - Multimodal → LM Studio gemma-4-e4b (local) o Gemini (externo)
  - Razonamiento complejo → DeepSeek
  - Consulta simple → Ollama llama31-8b-64k (1.9s)
  - VRAM < 2 GB → modelo ligero
"""

import argparse
import json
import os
import subprocess
import sys
import urllib.request
import base64

# ─── CONFIGURACIÓN ─────────────────────────────────────────────────

OLLAMA_URL = "http://localhost:11434/v1"
LMSTUDIO_URL = "http://localhost:1234/v1"
MODELO_RAPIDO = "llama31-8b-64k"       # Ollama: consultas simples
MODELO_VISION = "google/gemma-4-e4b"    # LM Studio: visión local
MODELO_VISION_HD = "google/gemma-4-12b-qat"  # LM Studio: visión detallada

# Palabras clave que indican razonamiento complejo → DeepSeek
PALABRAS_RAZONAMIENTO = [
    "explica por qué", "compara", "encuentra el error", "diseña una solución",
    "analiza", "depura", "diagnostica", "optimiza", "arquitectura",
    "implementa", "refactoriza", "diseña un", "crea un script",
    "cómo funcionaría", "qué pasaría si", "alternativas",
]

# Palabras clave que indican datos privados → Ollama forzado
PALABRAS_PRIVACIDAD = [
    "contraseña", "password", "token", "api_key", "secreto",
    "credencial", "dni", "nif", "tarjeta", "cuenta bancaria",
    "información personal", "datos sensibles", "privado",
]


# ─── FUNCIONES AUXILIARES ─────────────────────────────────────────

def ejecutar_comando(cmd):
    """Ejecuta un comando y devuelve (código, stdout, stderr)."""
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return r.returncode, r.stdout.strip(), r.stderr.strip()
    except FileNotFoundError:
        return -1, "", f"Comando no encontrado: {cmd[0]}"
    except subprocess.TimeoutExpired:
        return -1, "", "Tiempo de espera agotado"


def vram_libre_mb():
    """Devuelve VRAM libre en MB o None si no se puede determinar."""
    cod, salida, _ = ejecutar_comando([
        "nvidia-smi", "--query-gpu=memory.free",
        "--format=csv,noheader,nounits"
    ])
    if cod == 0 and salida:
        try:
            return int(salida.strip())
        except ValueError:
            return None
    return None


def ram_disponible_gb():
    """Devuelve RAM disponible en GB o None."""
    cod, salida, _ = ejecutar_comando(["free", "-g"])
    if cod == 0:
        for linea in salida.split("\n"):
            if linea.startswith("Mem:"):
                partes = linea.split()
                if len(partes) >= 7:
                    try:
                        return int(partes[6])
                    except ValueError:
                        pass
    return None


def curl_api(url, payload):
    """Llama a una API OpenAI-compatible y devuelve la respuesta."""
    datos = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url, data=datos,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"error": str(e)}


def consultar_ollama(modelo, mensaje):
    """Consulta un modelo en Ollama."""
    payload = {
        "model": modelo,
        "messages": [{"role": "user", "content": mensaje}],
        "stream": False
    }
    return curl_api(f"{OLLAMA_URL}/chat/completions", payload)


def consultar_lmstudio(modelo, mensaje, imagen_b64=None, mime="image/jpeg"):
    """Consulta un modelo en LM Studio, opcionalmente con imagen."""
    if imagen_b64:
        content = [
            {"type": "text", "text": mensaje},
            {"type": "image_url", "image_url": {
                "url": f"data:{mime};base64,{imagen_b64}"
            }}
        ]
    else:
        content = mensaje

    payload = {
        "model": modelo,
        "messages": [{"role": "user", "content": content}],
        "stream": False
    }
    return curl_api(f"{LMSTUDIO_URL}/chat/completions", payload)


# ─── DETECCIÓN DE TAREA ──────────────────────────────────────────

def detectar_modo(texto):
    """
    Devuelve el modo de enrutamiento según el texto.
    Retorna: ("privacidad"|"vision"|"razonamiento"|"simple", proveedor, modelo)
    """
    texto_lower = texto.lower()

    # 1. Privacidad (máxima prioridad)
    for p in PALABRAS_PRIVACIDAD:
        if p in texto_lower:
            vram = vram_libre_mb()
            if vram and vram < 2000:
                return ("privacidad", "ollama", "llama3.2:1b")
            return ("privacidad", "ollama", MODELO_RAPIDO)

    # 2. Razonamiento complejo
    for p in PALABRAS_RAZONAMIENTO:
        if p in texto_lower:
            return ("razonamiento", "deepseek", None)

    # 3. Consulta simple (por defecto)
    return ("simple", "ollama", MODELO_RAPIDO)


def detectar_vision(ruta_imagen):
    """
    Comprueba si LM Studio tiene un modelo VLM cargado.
    Devuelve el modelo a usar o None.
    """
    try:
        req = urllib.request.Request("http://localhost:1234/api/v0/models")
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            for m in data.get("data", []):
                if m["state"] != "not-loaded" and m["type"] == "vlm":
                    # Preferir el más rápido disponible
                    if "e4b" in m["id"]:
                        return m["id"]
                    return m["id"]
    except Exception:
        pass
    return None


# ─── MODO DIAGNÓSTICO ────────────────────────────────────────────

def modo_diagnostico():
    """Muestra el estado actual del sistema y recomendación."""
    print("═" * 55)
    print("  ai-router — Diagnóstico del sistema")
    print("═" * 55)

    # VRAM
    vram = vram_libre_mb()
    if vram is not None:
        print(f"\n  GPU VRAM libre: {vram} MB / 12282 MB")
        if vram > 6000:
            print(f"  → Categoría: modelo completo (>6 GB)")
            print(f"  → Recomendado: llama31-8b-64k (1.9s) o gemma-4-e4b (0.5s)")
        elif vram > 2000:
            print(f"  → Categoría: modelo mediano (2-6 GB)")
            print(f"  → Recomendado: modelo 3B-4B")
        else:
            print(f"  → Categoría: VRAM baja (<2 GB)")
            print(f"  → Recomendado: modelo ligero 1B")
    else:
        print(f"\n  GPU VRAM: no disponible (nvidia-smi no encontrado)")

    # RAM
    ram = ram_disponible_gb()
    if ram is not None:
        print(f"\n  RAM disponible: {ram} GB")
    else:
        print(f"\n  RAM disponible: no disponible")

    # Modelos disponibles
    print(f"\n── Ollama ──")
    cod, salida, _ = ejecutar_comando([
        "curl", "-s", "http://localhost:11434/api/tags"
    ])
    if cod == 0 and salida:
        try:
            data = json.loads(salida)
            for m in data.get("models", []):
                nombre = m["name"]
                print(f"  {'✓' if nombre == 'llama31-8b-64k' else ' '} {nombre}")
        except json.JSONDecodeError:
            print("  (no disponible)")
    else:
        print("  (Ollama no responde)")

    print(f"\n── LM Studio ──")
    cod, salida, _ = ejecutar_comando([
        "curl", "-s", "http://localhost:1234/api/v0/models"
    ])
    if cod == 0 and salida:
        try:
            data = json.loads(salida)
            for m in data.get("data", []):
                estado = "✅" if m["state"] != "not-loaded" else " "
                print(f"  {estado} {m['id']}")
        except json.JSONDecodeError:
            print("  (no disponible)")
    else:
        print("  (LM Studio no responde)")

    print(f"\n  Recomendación general:")
    vram_val = vram or 9999
    if vram_val > 6000:
        print(f"  → Consultas rápidas: llama31-8b-64k (Ollama, 1.9s)")
        print(f"  → Visión local: gemma-4-e4b (LM Studio, 0.5s)")
        print(f"  → Razonamiento: DeepSeek")
    print()


# ─── MODO PRINCIPAL ──────────────────────────────────────────────

def enrutar(texto, ruta_imagen=None):
    """
    Decide el proveedor y ejecuta la consulta.
    """
    if ruta_imagen:
        return enrutar_vision(texto, ruta_imagen)

    modo, proveedor, modelo = detectar_modo(texto)

    print(f"  [ai-router] Modo: {modo}")
    print(f"  [ai-router] Proveedor: {proveedor}", end="")
    if modelo:
        print(f" | Modelo: {modelo}")
    else:
        print()

    if proveedor == "deepseek":
        print(f"\n  ⚠ DeepSeek no está disponible desde este script.")
        print(f"  → Usa Hermes directamente para consultar DeepSeek.")
        print(f"  → Tu mensaje: {texto[:80]}...\n")
        return

    if proveedor == "ollama":
        print(f"\n  Consultando Ollama ({modelo})...")
        resp = consultar_ollama(modelo, texto)
        if "error" in resp:
            print(f"  ✗ Error: {resp['error']}")
            return
        try:
            print(f"\n{resp['choices'][0]['message']['content']}\n")
        except (KeyError, IndexError):
            print(f"  ✗ Respuesta inesperada: {json.dumps(resp, indent=2)[:200]}")
        return


def enrutar_vision(texto, ruta_imagen):
    """Enruta una tarea con imagen a LM Studio o Gemini."""

    if not os.path.isfile(ruta_imagen):
        print(f"  ✗ Archivo no encontrado: {ruta_imagen}")
        return

    # Leer y codificar imagen
    with open(ruta_imagen, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode("utf-8")

    ext = ruta_imagen.split(".")[-1].lower()
    mime = "image/png" if ext == "png" else "image/jpeg"

    # Detectar modelo VLM cargado en LM Studio
    modelo_vlm = detectar_vision(ruta_imagen)
    if modelo_vlm:
        print(f"  [ai-router] Modo: vision")
        print(f"  [ai-router] Proveedor: LM Studio | Modelo: {modelo_vlm}")
        print(f"\n  Procesando imagen ({os.path.getsize(ruta_imagen)} bytes)...")

        descripcion = texto or "Describe brevemente qué ves en esta imagen."
        resp = consultar_lmstudio(modelo_vlm, descripcion, img_b64, mime)
        if "error" in resp:
            print(f"  ✗ Error: {resp['error']}")
            return
        try:
            print(f"\n{resp['choices'][0]['message']['content']}\n")
        except (KeyError, IndexError):
            print(f"  ✗ Respuesta inesperada")
        return

    # Si no hay LM Studio, sugerir Gemini
    print(f"  [ai-router] Modo: vision")
    print(f"  [ai-router] No hay modelo VLM cargado en LM Studio.")
    print(f"  → Carga gemma-4-e4b en LM Studio o usa Gemini si está configurado.\n")


# ─── PUNTO DE ENTRADA ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="ai-router — Enrutamiento inteligente entre modelos de IA"
    )
    parser.add_argument("texto", nargs="?", help="Texto de la consulta")
    parser.add_argument("--vision", "-v", metavar="IMAGEN",
                        help="Ruta a una imagen para análisis multimodal")
    parser.add_argument("--diagnostico", "-d", action="store_true",
                        help="Mostrar diagnóstico del sistema")

    args = parser.parse_args()

    if args.diagnostico:
        modo_diagnostico()
        return

    if args.vision:
        enrutar_vision(args.texto or "Describe esta imagen.", args.vision)
        return

    if args.texto:
        enrutar(args.texto)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
