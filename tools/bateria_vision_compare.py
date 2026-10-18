#!/usr/bin/env python3
"""
Batería de pruebas: LFM 2.5 VL 3B vs GLM-4.6v-flash (visión local)
5 tareas REALES del lab (patrón batería PRODUCCIÓN) + métricas.

Uso:
  1. Descargar GLM  (lms unload glm-4.6v-flash)
  2. Cargar LFM VL  (lms load LFM2.5-VL-3B-GGUF)  → ejecutar con --modelo lfm
  3. Descargar LFM  (lms unload) + cargar GLM      → ejecutar con --modelo glm
  4. Comparar salidas JSON
"""
import json, base64, urllib.request, io, sys, time, os
from PIL import Image

API = "http://localhost:1234/api/v0/chat/completions"
IMAGENES = {
    "sueño_ocr": "/home/jokoalmi/.hermes/image_cache/img_1c63b7d42a99.jpg",
    "frasco_adonis": "/home/jokoalmi/joko-lab/research/infografias/perfume-del-dia-20260821/adonis_frasco_real.png",
    "fondo_sdxl": "/home/jokoalmi/joko-lab/research/infografias/perfume-del-dia-20260821/adonis_fondo.png",
    "infografia": "/home/jokoalmi/joko-lab/research/infografias/perfume-del-dia-20260821/perfume_del_dia_v4_adonis.png",
}

TAREAS = [
    ("sueño_ocr", "Transcribe los datos de esta captura de app de sueño: puntos, duración, horas (ej: 00:38→07:06), % REM/Ligero/Profundo, FC, SpO2, respiración. Responde SOLO los valores, sin razonar."),
    ("frasco_adonis", "¿Qué frasco de perfume se ve? ¿Qué casa y nombre aparecen en la etiqueta? Responde directo."),
    ("fondo_sdxl", "Describe esta imagen en 1 frase: qué escena muestra (lugar, luz, elementos)."),
    ("infografia", "¿Se ve la tarjeta 'Si te gusta, prueba' con alternativas de perfume en esta infografía? ¿Y el pie con QR? Responde SI/NO directo."),
]

def b64_imagen(ruta, max_px=512):
    im = Image.open(ruta).convert('RGB')
    im.thumbnail((max_px, max_px))
    buf = io.BytesIO()
    im.save(buf, format='JPEG', quality=80)
    return base64.b64encode(buf.getvalue()).decode()

def consulta(modelo, imagen_b64, texto, max_tokens=800):
    payload = {
        "model": modelo,
        "messages": [{"role": "user", "content": [
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{imagen_b64}"}},
            {"type": "text", "text": texto}
        ]}],
        "max_tokens": max_tokens,
        "temperature": 0.2
    }
    t0 = time.time()
    req = urllib.request.Request(API, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    try:
        resp = json.loads(urllib.request.urlopen(req, timeout=180).read())
        elapsed = time.time() - t0
        msg = resp['choices'][0]['message']
        content = msg.get('content') or ''
        # tokens si los da
        usage = resp.get('usage', {})
        return {"ok": True, "content": content, "segundos": round(elapsed, 1),
                "tokens_out": usage.get('completion_tokens', '?')}
    except Exception as e:
        return {"ok": False, "error": str(e), "segundos": round(time.time() - t0, 1)}

def main():
    modelo = sys.argv[1] if len(sys.argv) > 1 else "LFM2.5-VL-3B-GGUF"
    print(f"=== BATERÍA VISIÓN — {modelo} ===")
    print(f"Hora: {time.strftime('%H:%M:%S')}")
    print(f"VRAM inicio:", end=" ")
    try:
        import subprocess
        out = subprocess.run(["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
                             capture_output=True, text=True).stdout.strip()
        print(out + " MiB")
    except Exception:
        print("?")
    print()

    resultados = {}
    for nombre, prompt in TAREAS:
        ruta = IMAGENES[nombre]
        if not os.path.exists(ruta):
            print(f"[{nombre}] ⚠️ imagen no existe: {ruta}")
            continue
        print(f"--- TAREA: {nombre} ---")
        b64 = b64_imagen(ruta)
        r = consulta(modelo, b64, prompt)
        if r["ok"]:
            print(f"  ({r['segundos']}s, {r['tokens_out']} tok out)")
            print(f"  → {r['content'][:400]}")
        else:
            print(f"  ❌ ERROR: {r.get('error')}")
        resultados[nombre] = r
        print()

    # Guardar JSON
    salida = f"/tmp/bateria_vision_{modelo.split('/')[-1]}.json"
    with open(salida, "w") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)
    print(f"Guardado: {salida}")
    print(f"VRAM final:", end=" ")
    try:
        import subprocess
        out = subprocess.run(["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
                             capture_output=True, text=True).stdout.strip()
        print(out + " MiB")
    except Exception:
        print("?")

if __name__ == "__main__":
    main()
