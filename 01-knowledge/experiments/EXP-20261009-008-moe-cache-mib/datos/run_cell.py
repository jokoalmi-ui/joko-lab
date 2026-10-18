#!/usr/bin/env python3
"""EXP-20261009-008 - una celda de medida.

Uso:
  /usr/bin/python3 /tmp/exp008/run_cell.py --label E1_C0 --moe-cache-mib 0 \
      --ncmoe 24 --ngl 99 --prompt /tmp/exp008/prompt-E1-estructurada.txt \
      --npredict 128

Lanza llama-server (runtime 2.55.0 de LM Studio) en la ventana aislada :8099,
espera /health, pide una completion con sampling deterministico, recoge
timings + VRAM pico + RSS y mata el servidor por PID. Anade UNA linea JSON a
/tmp/exp008/cells.jsonl. No toca LM Studio (:1234), Ollama, ComfyUI ni n8n.
"""
import argparse, hashlib, json, os, signal, subprocess, sys, threading, time
import urllib.request, urllib.error

B = "/home/jokoalmi/.lmstudio/extensions/backends"
R255 = f"{B}/llama.cpp-linux-x86_64-nvidia-cuda12-avx2-2.55.0"
VEND = f"{B}/vendor/linux-llama-cuda12-vendor-v1"
BIN = f"{R255}/llama-server"
MODEL = ("/mnt/ssd_ia_datos/LM STUDIO/noctrex/"
         "Qwen3.6-35B-A3B-MXFP4_MOE-GGUF/Qwen3.6-35B-A3B-MXFP4_MOE.gguf")
OUTDIR = "/tmp/exp008"
OUT = f"{OUTDIR}/cells.jsonl"
HOST, PORT = "127.0.0.1", 8099


def run(c, t=60):
    try:
        r = subprocess.run(c, shell=True, capture_output=True, text=True, timeout=t)
        return ((r.stdout or "") + (r.stderr or "")).strip()
    except Exception as e:
        return f"EXC {e}"


def gpu_used():
    try:
        o = subprocess.run(["nvidia-smi", "--query-gpu=memory.used",
                            "--format=csv,noheader,nounits"],
                           capture_output=True, text=True, timeout=20).stdout
        return int(o.strip().split("\n")[0])
    except Exception:
        return -1


def mem_snapshot():
    free = run("free -m")
    swap = run("swapon --show")
    return {"free": free, "swapon": swap}


def vram_rss(pid):
    rss = -1
    try:
        with open(f"/proc/{pid}/status") as fh:
            for ln in fh:
                if ln.startswith("VmRSS:"):
                    rss = int(ln.split()[1])
    except Exception:
        pass
    return rss


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", required=True)
    ap.add_argument("--moe-cache-mib", type=int, default=0)
    ap.add_argument("--ncmoe", type=int, default=24)
    ap.add_argument("--ngl", type=int, default=99)
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--npredict", type=int, default=128)
    ap.add_argument("--ctx", type=int, default=4096)
    ap.add_argument("--ubatch", type=int, default=512)
    ap.add_argument("--threads", type=int, default=6)
    ap.add_argument("--seed", type=int, default=1234)
    ap.add_argument("--health-timeout", type=int, default=420)
    a = ap.parse_args()

    prompt = open(a.prompt, encoding="utf-8").read().strip()
    os.makedirs(OUTDIR, exist_ok=True)

    cmd = [BIN, "-m", MODEL, "--host", HOST, "--port", str(PORT),
           "-c", str(a.ctx), "-ngl", str(a.ngl), "-t", str(a.threads),
           "-ub", str(a.ubatch),
           "--no-warmup", "--n-predict", str(a.npredict)]
    if a.ngl > 0:
        cmd += ["-ncmoe", str(a.ncmoe)]
        if a.moe_cache_mib:
            cmd += ["--moe-cache-mib", str(a.moe_cache_mib)]

    env = dict(os.environ)
    env["LD_LIBRARY_PATH"] = f"{R255}:{VEND}:" + env.get("LD_LIBRARY_PATH", "")

    cell = {"label": a.label, "ts": run("date '+%F %T %Z'"), "ngl": a.ngl,
            "ncmoe": a.ncmoe if a.ngl > 0 else None,
            "moe_cache_mib": a.moe_cache_mib if a.ngl > 0 else None,
            "npredict": a.npredict, "ctx": a.ctx, "seed": a.seed,
            "ubatch": a.ubatch,
            "prompt_file": os.path.basename(a.prompt),
            "prompt_sha1": hashlib.sha1(prompt.encode()).hexdigest()[:12],
            "model": os.path.basename(MODEL),
            "model_bytes": os.path.getsize(MODEL),
            "cmd": " ".join(cmd), "gpu_used_before": gpu_used(),
            "mem_before": mem_snapshot()}

    logp = f"{OUTDIR}/server_{a.label}.log"
    log = open(logp, "w", encoding="utf-8")
    t0 = time.time()
    proc = subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT, env=env,
                            start_new_session=True)
    cell["pid"] = proc.pid

    peak = [cell["gpu_used_before"]]
    stop = threading.Event()

    def sampler():
        while not stop.is_set():
            peak[0] = max(peak[0], gpu_used())
            stop.wait(2.0)

    th = threading.Thread(target=sampler, daemon=True)
    th.start()

    # esperar /health
    healthy, died = False, False
    while time.time() - t0 < a.health_timeout:
        if proc.poll() is not None:
            died = True
            break
        try:
            with urllib.request.urlopen(f"http://{HOST}:{PORT}/health", timeout=3) as r:
                if r.status == 200:
                    healthy = True
                    break
        except Exception:
            pass
        time.sleep(3)
    cell["load_seconds"] = round(time.time() - t0, 1)
    cell["healthy"] = healthy
    if not healthy:
        cell["error"] = "server no arranco" + (" (proceso terminado)" if died else " (timeout health)")
        cell["vram_peak_total"] = peak[0]
        cell["log_tail"] = run(f"tail -6 {logp}")[-1200:]
        stop.set(); th.join(timeout=5)
        try:
            proc.send_signal(signal.SIGTERM); proc.wait(timeout=15)
        except Exception:
            try: os.kill(proc.pid, signal.SIGKILL)
            except Exception: pass
        log.close()
        cell["mem_after"] = mem_snapshot()
        with open(OUT, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(cell, ensure_ascii=False) + "\n")
        print(json.dumps(cell, ensure_ascii=False)[:1200])
        return 0

    cell["vram_after_load"] = gpu_used()
    cell["rss_kb_after_load"] = vram_rss(proc.pid)

    body = json.dumps({"prompt": prompt, "n_predict": a.npredict,
                       "temperature": 0, "seed": a.seed, "ignore_eos": True,
                       "cache_prompt": False, "stream": False}).encode()
    req = urllib.request.Request(f"http://{HOST}:{PORT}/completion", data=body,
                                headers={"Content-Type": "application/json"})
    tg = time.time()
    try:
        with urllib.request.urlopen(req, timeout=1800) as r:
            resp = json.loads(r.read().decode())
        cell["gen_wall_s"] = round(time.time() - tg, 1)
        t = resp.get("timings", {})
        for k in ("prompt_n", "prompt_ms", "prompt_per_second", "predicted_n",
                  "predicted_ms", "predicted_per_second"):
            if k in t:
                cell[k] = round(t[k], 3) if isinstance(t[k], float) else t[k]
        txt = resp.get("content", "")
        cell["text_md5"] = hashlib.md5(txt.encode()).hexdigest()
        cell["text_len"] = len(txt)
        cell["text_head"] = txt[:180].replace("\n", " ")
    except Exception as e:
        cell["error"] = f"completion fallo: {e}"

    cell["vram_peak_total"] = peak[0]
    cell["vram_after_gen"] = gpu_used()
    cell["rss_kb_after_gen"] = vram_rss(proc.pid)
    stop.set(); th.join(timeout=5)

    try:
        proc.send_signal(signal.SIGTERM); proc.wait(timeout=20)
    except Exception:
        try: os.kill(proc.pid, signal.SIGKILL)
        except Exception: pass
    log.close()
    cell["killed"] = True
    cell["log_tail"] = run(f"tail -3 {logp}")[-400:]
    cell["mem_after"] = mem_snapshot()

    with open(OUT, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(cell, ensure_ascii=False) + "\n")
    print(json.dumps(cell, ensure_ascii=False)[:1500])
    return 0


if __name__ == "__main__":
    sys.exit(main())
