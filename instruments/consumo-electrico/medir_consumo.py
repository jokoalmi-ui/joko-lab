#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""medir_consumo.py — instrumento SOLO-LECTURA de consumo electrico del lab (v0.1).

RESTRICCION CONSTITUCIONAL (molde `instruments/critic-loop`): NO modifica nada.
No toca config, no lanza ni para servicios, no bloquea/limita/reintenta, no eleva
privilegios. Solo OBSERVA, MIDE y REGISTRA. Escribe unicamente dentro de su
carpeta `outputs/`.

QUE MIDE
  - GPU (nvidia-smi): potencia muestreada + media/max, energia integrada (Wh)
    por suma P*dt, VRAM y utilizacion.
  - RAPL (intel-rapl): estado de cada dominio y, SOLO si es legible sin
    privilegio, la energia consumida en la ventana.
  - CPU (/proc/stat, /proc/loadavg): OCUPACION (no vatios: sin RAPL no hay
    vatios de CPU; no se estiman).

QUE NO HACE
  - No estima lo que no puede leer: lo declara NO LEGIBLE.
  - No fija umbrales: da cifras y su incertidumbre.
  - No cubre CPU, RAM, discos, ventiladores, USB ni perdidas de la fuente mas
    alla de lo que RAPL exponga. La medida "de pared" exigiria un medidor fisico.

USO
  /usr/bin/python3 medir_consumo.py --ventana 30 --etiqueta "reposo"
  /usr/bin/python3 medir_consumo.py --ventana 130 --etiqueta "bateria tool-calling"
  Opcional: --precio-kwh 0.15 (si se aporta, calcula coste en EUR; si no, NO calcula).
"""

import argparse
import json
import os
import statistics
import subprocess
import sys
import time
from datetime import datetime

AQUI = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(AQUI, "outputs")
QUERY_GPU = "power.draw,utilization.gpu,memory.used,memory.total,temperature.gpu"


def ahora():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def leer_gpu():
    """Devuelve (dict, error). error != None si no se pudo medir."""
    try:
        r = subprocess.run(
            ["nvidia-smi", "--query-gpu=" + QUERY_GPU, "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=10)
    except FileNotFoundError:
        return None, "nvidia-smi no encontrado en PATH"
    except subprocess.TimeoutExpired:
        return None, "nvidia-smi: timeout"
    if r.returncode != 0:
        return None, "nvidia-smi exit %s: %s" % (r.returncode, (r.stderr or "").strip()[:200])
    lineas = [l for l in (r.stdout or "").strip().splitlines() if l.strip()]
    if not lineas:
        return None, "nvidia-smi sin salida"
    campos = [c.strip() for c in lineas[0].split(",")]

    def num(x):
        try:
            return float(x)
        except ValueError:
            return None

    return {
        "potencia_w": num(campos[0]),
        "util_pct": num(campos[1]),
        "vram_mib": num(campos[2]),
        "vram_total_mib": num(campos[3]),
        "temp_c": num(campos[4]),
    }, None


def dominios_rapl():
    base = "/sys/class/powercap"
    out = []
    if not os.path.isdir(base):
        return out
    for n in sorted(os.listdir(base)):
        if not n.startswith("intel-rapl"):
            continue
        ruta = os.path.join(base, n)
        if not os.path.isdir(ruta):
            continue
        item = {"dominio": n, "nombre": None, "legible": False,
                "energy_uj": None, "error": None}
        try:
            with open(os.path.join(ruta, "name")) as f:
                item["nombre"] = f.read().strip()
        except Exception as e:
            item["error"] = "name: %s" % type(e).__name__
        try:
            with open(os.path.join(ruta, "energy_uj")) as f:
                item["energy_uj"] = int(f.read().strip())
                item["legible"] = True
                item["error"] = None
        except PermissionError:
            item["error"] = "energy_uj: PermissionError (requiere privilegio)"
        except FileNotFoundError:
            item["error"] = "energy_uj: no existe"
        except Exception as e:
            item["error"] = "energy_uj: %s" % type(e).__name__
        out.append(item)
    return out


def leer_cpu():
    try:
        with open("/proc/stat") as f:
            campos = f.readline().split()
        v = [int(x) for x in campos[1:]]
    except Exception:
        return None
    idle = v[3] + (v[4] if len(v) > 4 else 0)
    return {"busy": sum(v) - idle, "total": sum(v)}


def leer_loadavg():
    try:
        with open("/proc/loadavg") as f:
            return f.read().split()[:3]
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser(description="Medidor solo-lectura de consumo electrico (GPU/RAPL/CPU).")
    ap.add_argument("--ventana", type=float, default=30.0, help="segundos a muestrear (def. 30)")
    ap.add_argument("--intervalo", type=float, default=1.0, help="segundos entre muestras (def. 1.0)")
    ap.add_argument("--etiqueta", default="", help="que estaba corriendo durante la ventana (lo aporta quien mide)")
    ap.add_argument("--precio-kwh", type=float, default=None,
                    help="EUR/kWh; si se aporta, calcula coste. Si no, NO se calcula ningun coste.")
    ap.add_argument("--out", default=None, help="fichero JSON de la corrida (def. outputs/consumo-<fecha>.json)")
    ap.add_argument("--jsonl", default=None, help="fichero JSONL append (def. outputs/consumo.jsonl)")
    args = ap.parse_args()

    os.makedirs(OUT_DIR, exist_ok=True)
    gpu_err = None
    muestras = []
    rapl_ini = dominios_rapl()
    cpu_ini = leer_cpu()
    t0 = time.monotonic()
    t_prev = None
    p_prev = None
    energia_wh = 0.0
    while True:
        t = time.monotonic()
        g, err = leer_gpu()
        if err:
            gpu_err = err
        if g:
            muestras.append({"t_s": round(t - t0, 3), "hora": ahora(), **g})
            p_act = g.get("potencia_w")
            if p_prev is not None and p_act is not None and t_prev is not None:
                dt = t - t_prev
                energia_wh += ((p_prev + p_act) / 2.0) * dt / 3600.0
            p_prev = p_act
        t_prev = t
        if t - t0 >= args.ventana:
            break
        time.sleep(max(0.05, min(args.intervalo, args.ventana - (time.monotonic() - t0))))
    dur = round(time.monotonic() - t0, 3)
    rapl_fin = dominios_rapl()
    cpu_fin = leer_cpu()

    # --- GPU agregada ---
    pot = [m["potencia_w"] for m in muestras if m.get("potencia_w") is not None]
    util = [m["util_pct"] for m in muestras if m.get("util_pct") is not None]
    vram = [m["vram_mib"] for m in muestras if m.get("vram_mib") is not None]
    temp = [m["temp_c"] for m in muestras if m.get("temp_c") is not None]
    gpu = {
        "muestras": len(muestras),
        "error": gpu_err,
        "potencia_w": {"media": round(statistics.mean(pot), 2) if pot else None,
                       "max": round(max(pot), 2) if pot else None,
                       "min": round(min(pot), 2) if pot else None},
        "energia_wh_integrada": round(energia_wh, 4),
        "util_pct_media": round(statistics.mean(util), 2) if util else None,
        "vram_mib_max": max(vram) if vram else None,
        "temp_c_max": max(temp) if temp else None,
    }

    # --- RAPL: energia de la ventana (solo dominios legibles) ---
    rapl = []
    ini_por_nombre = {d["dominio"]: d for d in rapl_ini}
    for d in rapl_fin:
        i = ini_por_nombre.get(d["dominio"], {})
        item = {"dominio": d["dominio"], "nombre": d["nombre"], "legible": d["legible"], "error": d["error"]}
        if d["legible"] and i.get("legible") and d.get("energy_uj") is not None and i.get("energy_uj") is not None:
            j = (d["energy_uj"] - i["energy_uj"]) / 1e6
            item["energia_j_ventana"] = round(j, 3)
            item["potencia_media_w_ventana"] = round(j / dur, 3) if dur else None
        rapl.append(item)

    # --- CPU: ocupacion (no vatios) ---
    cpu: dict = {"loadavg_1_5_15": leer_loadavg()}
    if cpu_ini and cpu_fin:
        db = cpu_fin["busy"] - cpu_ini["busy"]
        dt_ = cpu_fin["total"] - cpu_ini["total"]
        cpu["ocupacion_pct_ventana"] = round(100.0 * db / dt_, 2) if dt_ > 0 else None

    registro = {
        "instrumento": "consumo-electrico v0.1",
        "fecha": ahora(),
        "etiqueta": args.etiqueta,
        "ventana_pedida_s": args.ventana,
        "ventana_real_s": dur,
        "intervalo_s": args.intervalo,
        "gpu": gpu,
        "rapl": rapl,
        "cpu": cpu,
        "coste_eur": None,
        "limites_de_medicion": [
            "GPU: potencia muestreada con nvidia-smi (integracion trapezoidal sobre las muestras reales).",
            "CPU/RAM/SoC: solo medibles por RAPL; si energy_uj no es legible, NO se estiman.",
            "NO cubre discos, ventiladores, USB ni perdidas de la fuente.",
            "La medida 'de pared' exige un medidor fisico: este instrumento no la sustituye.",
        ],
    }
    if args.precio_kwh is not None and gpu["energia_wh_integrada"] is not None:
        registro["coste_eur"] = {
            "precio_kwh": args.precio_kwh,
            "base": "energia GPU integrada",
            "eur": round(gpu["energia_wh_integrada"] / 1000.0 * args.precio_kwh, 6),
            "nota": "solo energia GPU; no incluye CPU/resto del sistema",
        }
        registro["limites_de_medicion"].append("El coste en EUR cubre SOLO la energia de la GPU.")

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ruta_json = args.out or os.path.join(OUT_DIR, "consumo-%s.json" % stamp)
    registro_serie = dict(registro, serie=muestras)
    with open(ruta_json, "w", encoding="utf-8") as f:
        json.dump(registro_serie, f, ensure_ascii=False, indent=1)
    ruta_jsonl = args.jsonl or os.path.join(OUT_DIR, "consumo.jsonl")
    with open(ruta_jsonl, "a", encoding="utf-8") as f:
        f.write(json.dumps(registro, ensure_ascii=False) + "\n")

    print(json.dumps({
        "json": ruta_json, "jsonl": ruta_jsonl, "ventana_real_s": dur,
        "gpu_potencia_w_media": gpu["potencia_w"]["media"], "gpu_potencia_w_max": gpu["potencia_w"]["max"],
        "gpu_energia_wh": gpu["energia_wh_integrada"], "gpu_vram_mib_max": gpu["vram_mib_max"],
        "rapl_legible": [d["dominio"] for d in rapl if d["legible"]],
        "rapl_no_legible": [d["dominio"] for d in rapl if not d["legible"]],
        "cpu_ocupacion_pct": cpu.get("ocupacion_pct_ventana"),
    }, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
