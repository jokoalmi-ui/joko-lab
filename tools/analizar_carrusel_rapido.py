#!/usr/bin/env python3
"""analizar_carrusel_rapido.py — Análisis de carruseles OPTIMIZADO (v2, 10-ago-2026).

Métodos aplicados (estudio de optimización):
1. VARIAS IMÁGENES POR LLAMADA — GLM acepta array de imágenes en un mensaje
   (cada imagen se codifica en el mismo prefill; menos overhead de llamadas).
2. PARALELISMO — los lotes de imágenes se lanzan con ThreadPoolExecutor
   (la GPU trabaja mientras se codifican los siguientes).

Uso: python3 analizar_carrusel_rapido.py <dir> [--lote 3] [--max_px 512]
"""
import base64, json, urllib.request, io, sys, time, os
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image

API = "http://localhost:1234/api/v0/chat/completions"
MODEL = "glm-4.6v-flash"
PROMPT = ("Da la respuesta directa, sin razonar en voz alta. "
          "Para CADA imagen de este lote, identifícala como 'IMAGEN N:' y "
          "resume en español: tema, puntos clave, herramientas. "
          "Separa cada imagen con una línea en blanco.")

def _cargar_imagen(path, max_px):
    """Carga y redimensiona la imagen, devuelve (indice, base64, path)."""
    idx = int(os.path.basename(path).split('_')[1].split('.')[0])
    img = Image.open(path)
    img.thumbnail((max_px, max_px))
    buf = io.BytesIO()
    img.save(buf, format='JPEG', quality=72)
    b64 = base64.b64encode(buf.getvalue()).decode()
    return (idx, b64, path)

def analizar_lote(imagenes, max_px=512):
    """Analiza un lote de imágenes en UNA llamada. Devuelve el texto."""
    # Cargar todas las imágenes del lote
    cargadas = [_cargar_imagen(p, max_px) for p in imagenes]
    cargadas.sort()  # por índice
    # Construir content: [img1, img2, ..., text]
    content = []
    for idx, b64, path in cargadas:
        content.append({"type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{b64}"}})
    content.append({"type": "text", "text": PROMPT})

    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": content}],
        "max_tokens": 1200,
        "temperature": 0.2
    }
    req = urllib.request.Request(API, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=400) as r:
        resp = json.loads(r.read())
    elapsed = time.time() - t0
    msg = resp["choices"][0]["message"]
    out = msg.get("content", "") or f"[REASONING] {msg.get('reasoning_content','')[:300]}"
    return out, elapsed

def main():
    args = sys.argv[1:]
    if not args:
        print("Uso: analizar_carrusel_rapido.py <dir> [--lote N] [--max_px N]")
        return
    d = args[0]
    lote_size = 3
    max_px = 512
    if '--lote' in args:
        lote_size = int(args[args.index('--lote')+1])
    if '--max_px' in args:
        max_px = int(args[args.index('--max_px')+1])

    # Listar imágenes ordenadas
    ext = ('.jpg', '.jpeg', '.png', '.webp')
    paths = sorted([os.path.join(d, f) for f in os.listdir(d) if f.lower().endswith(ext)])
    total = len(paths)
    print(f"Analizando {total} imágenes | lote={lote_size} | max_px={max_px}")

    lotes = [paths[i:i+lote_size] for i in range(0, total, lote_size)]
    t_ini = time.time()

    # PARALELISMO REAL: GLM tiene slots paralelos (config "parallel": 4)
    # -> cada imagen como request independiente, hasta 3-4 concurrentes
    # (verificado 11-ago: 3 imagenes en paralelo = 39s vs ~87s/individual)
    max_conc = 3
    resultados = {}
    with ThreadPoolExecutor(max_workers=max_conc) as ex:
        # Lanzar TODAS las imagenes como requests independientes (cada lote = 1 img)
        futures = {}
        for path in paths:
            fut = ex.submit(_analizar_una, path, max_px)
            futures[fut] = path
        for i, fut in enumerate(as_completed(futures), 1):
            path = futures[fut]
            try:
                out, elapsed = fut.result()
                resultados[path] = out
                print(f"  [{elapsed:.0f}s] {os.path.basename(path)} ✓", flush=True)
            except Exception as e:
                print(f"  ERROR {os.path.basename(path)}: {str(e)[:100]}", flush=True)

    t_total = time.time() - t_ini
    print(f"\n=== TOTAL: {t_total:.0f}s para {total} imágenes "
          f"({t_total/max(1,total):.1f}s/img) ===")
    # Imprimir resultados en orden
    for path in paths:
        print(f"\n### {os.path.basename(path)}")
        print(resultados.get(path, "(fallo)"))


def _analizar_una(path, max_px=512):
    """Analiza UNA imagen (request independiente, va en paralelo)."""
    idx, b64, _ = _cargar_imagen(path, max_px)
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": [
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
            {"type": "text", "text": PROMPT}
        ]}],
        "max_tokens": 400,
        "temperature": 0.2
    }
    req = urllib.request.Request(API, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=400) as r:
        resp = json.loads(r.read())
    elapsed = time.time() - t0
    msg = resp["choices"][0]["message"]
    out = msg.get("content", "") or f"[REASONING] {msg.get('reasoning_content','')[:300]}"
    return out, elapsed

if __name__ == '__main__':
    main()
