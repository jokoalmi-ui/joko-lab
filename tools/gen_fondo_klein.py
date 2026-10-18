#!/usr/bin/python3
"""Generador de fondos de ficha con FLUX.2 [klein] 4B (ComfyUI API). Sustituye a gen_comfy.py (SDXL) como predeterminado.

Uso:
  /usr/bin/python3 ~/joko-lab/tools/gen_fondo_klein.py "<prompt escena>" <salida.png> \
      [--seed 42] [--steps 20] [--size 1024] [--prefix lab/fondo_klein]

Notas:
- Requiere ComfyUI vivo en 127.0.0.1:8188 y ~11 GB de VRAM libres (klein ~4 GB + activaciones).
  Con LM Studio cargado hay que hacer `lms unload --all` antes y recargar despues.
- FLUX.2 usa BasicGuider: el NEGATIVO no se aplica (no hay CFG). El flag --negative existe solo
  para dejar constancia del texto que pide la skill; no cambia el resultado.
- Rechaza sobrescribir la salida si ya existe, salvo --force.
- Guarda junto al PNG un .json con prompt/seed/steps/modelo para trazabilidad.
"""
import argparse, json, os, shutil, sys, time, urllib.error, urllib.request, uuid

HOST = os.environ.get("COMFY_HOST", "http://127.0.0.1:8188")
UNET = "flux-2-klein-4b-fp8.safetensors"
CLIP = "qwen_3_4b_fp4_flux2.safetensors"
VAE = "flux2-vae.safetensors"


def workflow(prompt, steps, w, h, seed, prefix):
    return {
        "1": {"class_type": "UNETLoader", "inputs": {"unet_name": UNET, "weight_dtype": "default"}},
        "2": {"class_type": "CLIPLoader", "inputs": {"clip_name": CLIP, "type": "flux2"}},
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": VAE}},
        "4": {"class_type": "CLIPTextEncode", "inputs": {"text": prompt, "clip": ["2", 0]}},
        "5": {"class_type": "BasicGuider", "inputs": {"model": ["1", 0], "conditioning": ["4", 0]}},
        "6": {"class_type": "KSamplerSelect", "inputs": {"sampler_name": "euler"}},
        "7": {"class_type": "Flux2Scheduler", "inputs": {"steps": steps, "width": w, "height": h}},
        "8": {"class_type": "RandomNoise", "inputs": {"noise_seed": seed}},
        "9": {"class_type": "EmptyFlux2LatentImage", "inputs": {"width": w, "height": h, "batch_size": 1}},
        "10": {"class_type": "SamplerCustomAdvanced", "inputs": {"noise": ["8", 0], "guider": ["5", 0],
               "sampler": ["6", 0], "sigmas": ["7", 0], "latent_image": ["9", 0]}},
        "11": {"class_type": "VAEDecode", "inputs": {"samples": ["10", 0], "vae": ["3", 0]}},
        "12": {"class_type": "SaveImage", "inputs": {"images": ["11", 0], "filename_prefix": prefix}},
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("prompt")
    ap.add_argument("out")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--steps", type=int, default=20)
    ap.add_argument("--size", type=int, default=1024, help="lado en px (multiplo de 16)")
    ap.add_argument("--prefix", default="lab/fondo_klein")
    ap.add_argument("--negative", default="", help="solo trazabilidad: FLUX.2 no aplica negativo")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    if a.size % 16:
        sys.exit("--size debe ser multiplo de 16")
    if os.path.exists(a.out) and not a.force:
        sys.exit(f"ya existe {a.out} (usa --force para sobrescribir)")
    try:
        st = json.loads(urllib.request.urlopen(f"{HOST}/system_stats", timeout=8).read())
        print(f"ComfyUI {st['system']['comfyui_version']}", flush=True)
    except Exception as e:
        sys.exit(f"ComfyUI no responde en {HOST}: {e}")

    t0 = time.time()
    body = {"prompt": workflow(a.prompt, a.steps, a.size, a.size, a.seed, a.prefix), "client_id": str(uuid.uuid4())}
    req = urllib.request.Request(f"{HOST}/prompt", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    pid = json.loads(urllib.request.urlopen(req, timeout=30).read())["prompt_id"]
    print("prompt_id", pid, flush=True)
    while True:
        h = json.loads(urllib.request.urlopen(f"{HOST}/history/{pid}", timeout=10).read())
        if pid in h:
            if h[pid].get("status", {}).get("status_str") == "error":
                sys.exit("ERROR en ComfyUI: " + json.dumps(h[pid]["status"], ensure_ascii=False)[:600])
            imgs = h[pid]["outputs"].get("12", {}).get("images") or []
            if imgs:
                break
        time.sleep(2)
    img = imgs[0]
    src = os.path.join("/home/jokoalmi/ComfyUI/output", img.get("subfolder", ""), img["filename"])
    shutil.copy2(src, a.out)
    meta = {"modelo": UNET, "clip": CLIP, "vae": VAE, "prompt": a.prompt, "negativo_no_aplicado": a.negative,
            "seed": a.seed, "steps": a.steps, "px": f"{a.size}x{a.size}", "segundos": round(time.time() - t0, 1),
            "bytes": os.path.getsize(a.out)}
    with open(a.out + ".json", "w", encoding="utf-8") as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=2)
    print(json.dumps(meta, ensure_ascii=False))


if __name__ == "__main__":
    main()
