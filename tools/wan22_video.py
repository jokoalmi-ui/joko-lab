#!/usr/bin/env python3
"""Vídeo generativo local con Wan 2.2 TI2V-5B en el ComfyUI del lab.

Imagen -> vídeo corto (3-5 s) en la RTX A2000 12 GB. Función principal = construir
el prompt de la API /prompt de ComfyUI desde cero, arrancar la generación, medir
tiempo y picos de VRAM/RAM/swap, y dejar el MP4 en la ruta pedida.

Coste medido en este host (30-oct-2026, A2000 12 GB, --lowvram):
  preset rapido  704x480, 49 frames  -> 124,0 s  | VRAM pico 11.832/11.898 MiB (99 %)
  preset calidad 1280x704, 81 frames -> 704,1 s  | VRAM pico 10.098/11.898 MiB (85 %)
Regla: el preset rapido es 3,4x mas eficiente por segundo de video pero NO deja
VRAM para nada mas mientras genera.

Uso:
  python3 wan22_video.py foto.png "descripcion del movimiento"
  python3 wan22_video.py foto.png "..." --preset calidad --out clip.mp4
  python3 wan22_video.py foto.png "..." --size 832x480 --frames 33 --seed 7

No arranca ni reinicia ComfyUI: si está parado, avisa y sale.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
import uuid

API = "http://127.0.0.1:8188"
COMFY = "/home/jokoalmi/ComfyUI"
UNET = "wan2.2_ti2v_5B_fp16.safetensors"
CLIP = "umt5_xxl_fp8_e4m3fn_scaled.safetensors"
VAE = "wan2.2_vae.safetensors"

PRESETS = {
    "rapido": (704, 480, 49, 20),
    "calidad": (1280, 704, 81, 20),
}

NEGATIVO = ("blurry, low quality, distorted, deformed limbs, extra arms, extra legs, "
            "extra fingers, duplicate subject, changing body shape, melting, floating, "
            "sliding, sudden movements, flickering, camera movement, cuts, subtitles, watermark")


def api_get(path, data=None, timeout=30):
    req = urllib.request.Request(API + path)
    if data is not None:
        req.add_header("Content-Type", "application/json")
        return json.load(urllib.request.urlopen(req, data=json.dumps(data).encode(), timeout=timeout))
    return json.load(urllib.request.urlopen(req, timeout=timeout))


def construir_prompt(img_name, texto, w, h, frames, steps, seed, fps, prefijo):
    """Los 12 nodos del workflow Wan22 TI2V-5B en formato API."""
    pos = (f"Locked camera, continuous shot. {texto.strip()} "
           "Keep the original design, colours and textures of the subject. No cuts.")
    return {
        "37": {"class_type": "UNETLoader",
               "inputs": {"unet_name": UNET, "weight_dtype": "default"}},
        "38": {"class_type": "CLIPLoader",
               "inputs": {"clip_name": CLIP, "type": "wan", "device": "default"}},
        "39": {"class_type": "VAELoader", "inputs": {"vae_name": VAE}},
        "60": {"class_type": "LoadImage", "inputs": {"image": img_name}},
        "55": {"class_type": "Wan22ImageToVideoLatent",
               "inputs": {"vae": ["39", 0], "width": w, "height": h,
                          "length": frames, "batch_size": 1, "start_image": ["60", 0]}},
        "6": {"class_type": "CLIPTextEncode",
              "inputs": {"clip": ["38", 0], "text": pos}},
        "7": {"class_type": "CLIPTextEncode",
              "inputs": {"clip": ["38", 0], "text": NEGATIVO}},
        "48": {"class_type": "ModelSamplingSD3",
               "inputs": {"model": ["37", 0], "shift": 8}},
        "3": {"class_type": "KSampler",
              "inputs": {"model": ["48", 0], "positive": ["6", 0], "negative": ["7", 0],
                         "latent_image": ["55", 0], "seed": seed, "steps": steps,
                         "cfg": 5, "sampler_name": "uni_pc", "scheduler": "simple",
                         "denoise": 1}},
        "8": {"class_type": "VAEDecodeTiled",
              "inputs": {"samples": ["3", 0], "vae": ["39", 0], "tile_size": 256,
                         "overlap": 64, "temporal_size": 8, "temporal_overlap": 4}},
        "57": {"class_type": "CreateVideo",
               "inputs": {"images": ["8", 0], "fps": fps}},
        "58": {"class_type": "SaveVideo",
               "inputs": {"video": ["57", 0], "filename_prefix": prefijo,
                          "format": "mp4", "codec": "h264"}},
    }


def picos(pid):
    """Muestrea RSS/swap/VRAM mientras dure la generación."""
    stop = threading.Event()
    pico = {"rss": 0, "swap": 0, "vram": 0, "temp": 0}

    def bucle():
        while not stop.is_set():
            try:
                for line in open(f"/proc/{pid}/status"):
                    if line.startswith("VmRSS:"):
                        pico["rss"] = max(pico["rss"], int(line.split()[1]) // 1024)
                    elif line.startswith("VmSwap:"):
                        pico["swap"] = max(pico["swap"], int(line.split()[1]) // 1024)
            except OSError:
                pass
            try:
                sal = subprocess.run(["nvidia-smi", "--query-gpu=memory.used,temperature.gpu",
                                      "--format=csv,noheader,nounits"],
                                     capture_output=True, text=True, timeout=10).stdout.strip()
                v, t = [int(x) for x in sal.split(",")]
                pico["vram"] = max(pico["vram"], v)
                pico["temp"] = max(pico["temp"], t)
            except Exception:
                pass
            stop.wait(2)

    h = threading.Thread(target=bucle, daemon=True)
    h.start()
    return stop, pico


def main():
    ap = argparse.ArgumentParser(description="Wan 2.2 TI2V-5B local (12 GB)")
    ap.add_argument("imagen")
    ap.add_argument("prompt")
    ap.add_argument("--preset", choices=sorted(PRESETS), default="rapido")
    ap.add_argument("--size", help="ANCHOxALTO, sobreescribe el preset")
    ap.add_argument("--frames", type=int, help="frames totales (4n+1)")
    ap.add_argument("--steps", type=int, default=20)
    ap.add_argument("--seed", type=int, default=1234)
    ap.add_argument("--fps", type=int, default=16)
    ap.add_argument("--out", help="ruta del mp4 resultante")
    ap.add_argument("--timeout", type=int, default=3600)
    a = ap.parse_args()

    w, h, frames, steps = PRESETS[a.preset]
    if a.size:
        w, h = (int(x) for x in a.size.lower().split("x"))
    if a.frames:
        frames = a.frames
    if a.steps:
        steps = a.steps

    if not os.path.isfile(a.imagen):
        sys.exit(f"FALTA la imagen: {a.imagen}")
    try:
        stats = api_get("/system_stats")
    except Exception:
        sys.exit("ComfyUI no responde en :8188. Arrancarlo es un cambio de servicio: pide OK antes.")
    dev = (stats.get("devices") or [{}])[0]
    print(f"ComfyUI {stats.get('system',{}).get('comfyui_version')} | {dev.get('name')} "
          f"| VRAM libre {int(dev.get('vram_free',0)/2**20)} MiB")

    info = api_get("/object_info")
    unets = info.get("UNETLoader", {}).get("input", {}).get("required", {}).get("unet_name", [[""]])[0]
    if UNET not in unets:
        sys.exit(f"ComfyUI no ve {UNET} en models/diffusion_models.")

    nombre = os.path.basename(a.imagen)
    destino_img = os.path.join(COMFY, "input", nombre)
    if os.path.abspath(a.imagen) != destino_img:
        shutil.copyfile(a.imagen, destino_img)
        print("imagen copiada a", destino_img)

    prefijo = "Wan22/" + (os.path.splitext(nombre)[0])[:40]
    prompt = construir_prompt(nombre, a.prompt, w, h, frames, steps, a.seed, a.fps, prefijo)
    print(f"config: {w}x{h} | {frames} frames | {frames/a.fps:.2f} s de vídeo | {steps} pasos "
          f"| seed {a.seed} | preset {a.preset}")

    pid = int(subprocess.run(["pgrep", "-f", "main.py --listen 127.0.0.1 --port 8188"],
                             capture_output=True, text=True).stdout.split()[0])
    t0 = time.time()
    stop, pico = picos(pid)
    try:
        r = api_get("/prompt", {"prompt": prompt, "client_id": str(uuid.uuid4())})
    except urllib.error.HTTPError as e:
        stop.set()
        sys.exit("ComfyUI rechazó el prompt:\n" + e.read().decode()[:1500])
    qid = r["prompt_id"]
    print("encolado", qid, flush=True)

    estado = None
    while time.time() - t0 < a.timeout:
        time.sleep(10)
        hist = api_get(f"/history/{qid}")
        if qid in hist:
            estado = hist[qid]
            break
        print(f"  {time.time()-t0:.0f}s ...", flush=True)
    stop.set()
    time.sleep(3)
    dur = time.time() - t0

    if estado is None:
        sys.exit(f"sin resultado tras {dur:.0f}s (límite {a.timeout})")

    ok = (estado.get("status") or {}).get("status_str")
    print(f"\ntiempo: {dur:.1f} s | vídeo: {frames/a.fps:.2f} s | {dur/(frames/a.fps):.1f} s de GPU por s de vídeo")
    print(f"picos: RSS {pico['rss']} MiB | swap {pico['swap']} MiB | VRAM {pico['vram']} MiB | temp {pico['temp']} °C")
    print("estado:", ok)

    creado = None
    for sal in (estado.get("outputs") or {}).values():
        for v in sal.values():
            if isinstance(v, list):
                for it in v:
                    if isinstance(it, dict) and it.get("filename"):
                        creado = os.path.join(COMFY, "output", it.get("subfolder") or "", it["filename"])
    if not creado or not os.path.exists(creado):
        sys.exit("no se encontró el mp4 de salida")
    print("salida:", creado, os.path.getsize(creado), "B")
    if a.out:
        shutil.copyfile(creado, a.out)
        print("copiado a", a.out)
    if ok != "success":
        print("AVISO: el estado no es success; revisar el mp4 antes de usarlo.")
        sys.exit(1)


if __name__ == "__main__":
    main()
