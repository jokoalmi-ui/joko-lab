#!/usr/bin/env python3
"""Genera imágenes con ComfyUI vía API local (headless) — 18-ago-2026.
Uso: ./venv/bin/python gen_comfy.py "prompt" salida.png [--seed 42] [--steps 20] [--size 1024]
Requiere: servidor ComfyUI arrancado (./venv/bin/python main.py --listen 127.0.0.1)

--size: lado del EmptyLatentImage (por defecto 512). SDXL está entrenado a 1024:
generar a 1024 evita que el fondo se amplíe ×2,6 al montarlo en la ficha de
1080×1350 (medido 26-ago... 26-sep, herramienta medir_contraste_ficha.py).
"""
import json, sys, time, urllib.request, uuid, argparse, os

COMFY = "http://127.0.0.1:8188"

def queue_prompt(workflow):
    data = json.dumps({"prompt": workflow, "client_id": str(uuid.uuid4())}).encode()
    req = urllib.request.Request(f"{COMFY}/prompt", data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

def get_history(pid):
    with urllib.request.urlopen(f"{COMFY}/history/{pid}") as r:
        return json.loads(r.read())

def wait_image(pid, timeout=300):
    t0 = time.time()
    while time.time() - t0 < timeout:
        h = get_history(pid)
        if pid in h:
            outs = h[pid].get("outputs", {})
            for node in outs.values():
                for img in node.get("images", []):
                    return img
        time.sleep(2)
    raise TimeoutError(f"Sin imagen tras {timeout}s")

def build_workflow(prompt, seed, steps, outname, size=512):
    """Workflow mínimo SDXL: CheckpointLoader → CLIPTextEncode×2 → KSampler → VAEDecode → SaveImage"""
    ckpt = "sd_xl_base_1.0.safetensors"
    return {
        "3": {"class_type": "KSampler", "inputs": {
            "seed": seed, "steps": steps, "cfg": 7.0, "sampler_name": "euler",
            "scheduler": "normal", "denoise": 1.0,
            "model": ["4", 0], "positive": ["6", 0], "negative": ["7", 0], "latent_image": ["5", 0]}},
        "4": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": ckpt}},
        "5": {"class_type": "EmptyLatentImage", "inputs": {"width": size, "height": size, "batch_size": 1}},
        "6": {"class_type": "CLIPTextEncode", "inputs": {"text": prompt, "clip": ["4", 1]}},
        "7": {"class_type": "CLIPTextEncode", "inputs": {"text": "blurry, low quality, distorted, watermark", "clip": ["4", 1]}},
        "8": {"class_type": "VAEDecode", "inputs": {"samples": ["3", 0], "vae": ["4", 2]}},
        "9": {"class_type": "SaveImage", "inputs": {"filename_prefix": "lab_gen", "images": ["8", 0]}},
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("prompt")
    ap.add_argument("out")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--steps", type=int, default=20)
    ap.add_argument("--size", type=int, default=512,
                    help="lado del latente en px (512 por defecto; 1024 = nativo SDXL)")
    args = ap.parse_args()

    wf = build_workflow(args.prompt, args.seed, args.steps, os.path.basename(args.out), args.size)
    r = queue_prompt(wf)
    pid = r.get("prompt_id")
    if not pid:
        print("ERROR:", r); sys.exit(1)
    print(f"Cola: {pid} — esperando...")
    img = wait_image(pid)
    src = f"{COMFY}/view?filename={img['filename']}&subfolder={img.get('subfolder','')}&type={img['type']}"
    with urllib.request.urlopen(src) as resp, open(args.out, "wb") as f:
        f.write(resp.read())
    print(f"OK: {args.out} ({os.path.getsize(args.out)} bytes, {args.size}x{args.size})")

if __name__ == "__main__":
    main()
