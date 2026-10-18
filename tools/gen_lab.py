#!/usr/bin/env python3
"""gen_lab.py — genera una imagen con ComfyUI (SDXL) vía API local.
Uso: python3 gen_lab.py "prompt" salida.png [--size 768] [--seed 42] [--steps 20] [--neg "texto"] [--retrato]
Serie infografias IA/agentes (Joko Lab). Requiere ComfyUI arrancado (systemctl --user start comfyui)."""
import json, sys, time, uuid, argparse, urllib.request

COMFY = "http://127.0.0.1:8188"
NEG_DEF = ("text, letters, words, typography, watermark, signature, blurry, low quality, distorted, "
           "cluttered, full bleed background, orange background, dark background, photo, realistic")

def post(path, payload):
    req = urllib.request.Request(COMFY + path, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

def workflow(p, neg, seed, steps, w, h):
    return {
        "3": {"class_type": "KSampler", "inputs": {"seed": seed, "steps": steps, "cfg": 7.0,
              "sampler_name": "euler", "scheduler": "normal", "denoise": 1.0,
              "model": ["4", 0], "positive": ["6", 0], "negative": ["7", 0], "latent_image": ["5", 0]}},
        "4": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "sd_xl_base_1.0.safetensors"}},
        "5": {"class_type": "EmptyLatentImage", "inputs": {"width": w, "height": h, "batch_size": 1}},
        "6": {"class_type": "CLIPTextEncode", "inputs": {"text": p, "clip": ["4", 1]}},
        "7": {"class_type": "CLIPTextEncode", "inputs": {"text": neg, "clip": ["4", 1]}},
        "8": {"class_type": "VAEDecode", "inputs": {"samples": ["3", 0], "vae": ["4", 2]}},
        "9": {"class_type": "SaveImage", "inputs": {"filename_prefix": "lab_gen", "images": ["8", 0]}},
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("prompt"); ap.add_argument("out")
    ap.add_argument("--size", type=int, default=768)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--steps", type=int, default=20)
    ap.add_argument("--neg", default=NEG_DEF)
    ap.add_argument("--retrato", action="store_true", help="768x1024 en vez de cuadrado")
    a = ap.parse_args()
    w, h = (768, 1024) if a.retrato else (a.size, a.size)
    pid = post("/prompt", {"prompt": workflow(a.prompt, a.neg, a.seed, a.steps, w, h), "client_id": str(uuid.uuid4())})["prompt_id"]
    t0 = time.time()
    while time.time() - t0 < 600:
        h_ = urllib.request.urlopen(f"{COMFY}/history/{pid}").read()
        hist = json.loads(h_)
        if pid in hist:
            for node in hist[pid].get("outputs", {}).values():
                for img in node.get("images", []):
                    src = f"{COMFY}/view?filename={img['filename']}&subfolder={img.get('subfolder','')}&type={img['type']}"
                    open(a.out, "wb").write(urllib.request.urlopen(src).read())
                    print(f"OK: {a.out} ({w}x{h}, {round(time.time()-t0,1)}s)")
                    return
        time.sleep(2)
    print("TIMEOUT sin imagen"); sys.exit(1)

if __name__ == "__main__":
    main()
