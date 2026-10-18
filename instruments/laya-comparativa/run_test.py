#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LAYA-COMPARATIVA — runner.

Uso:
  python3 run_test.py --selftest                 # verifica el motor de metricas (sin red)
  python3 run_test.py --entorno                  # informe de entorno (solo lectura)
  python3 run_test.py --backend stub             # verificacion offline del arnes
  python3 run_test.py --backend stub --dry-run   # muestra payloads sin ejecutar
  python3 run_test.py --backend ollama           # baseline local (granite4.2:8b, 0 EUR)
  python3 run_test.py --backend laya --checkpoint router
  python3 run_test.py --backend laya --checkpoint typed-decisions
  python3 run_test.py --backend jev              # requiere token en ~/.config/joko-lab/jev.env

Escribe resultados_<backend>[_<checkpoint>].json EN ESTA CARPETA. Nada mas.
"""
import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone

import motor

AQUI = os.path.dirname(os.path.abspath(__file__))


def sha256(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def tabla_por_bloque(registros):
    out = {}
    for b in ("A", "B", "D"):
        pares = [(r["p"], r["gt"]) for r in registros
                 if r["bloque"] == b and r["p"] is not None]
        if pares:
            out[b] = motor.resumen(pares)
    return out


def tabla_por_subtipo(registros):
    out = {}
    sub = sorted({r.get("subtipo") for r in registros if r.get("subtipo")})
    for s in sub:
        pares = [(r["p"], r["gt"]) for r in registros
                 if r.get("subtipo") == s and r["p"] is not None]
        if pares:
            out[s] = motor.resumen(pares)
    return out


def cmd_choice(args):
    fichero = "casos_choice.json" if args.set_casos == "v1" else "casos_v2_choice.json"
    ruta = os.path.join(AQUI, fichero)
    if not os.path.exists(ruta):
        print(f"BLOQUEADO: falta {fichero}")
        return 5
    datos = json.load(open(ruta, encoding="utf-8"))
    casos = datos["casos"]
    print("=" * 68)
    print("LAYA-COMPARATIVA — bloque choice (elegir 1 de N)")
    print("=" * 68)
    print(f"casos        : {len(casos)}")
    print(f"fichero      : {fichero}  sha256 {sha256(ruta)[:16]}")
    print(f"backend      : {args.backend}")
    print()
    try:
        salida = motor.ejecutar_choice(
            casos, args.backend, {"modelo_ollama": args.modelo_ollama},
            verbose=args.verbose)
    except ImportError as exc:
        print("BLOQUEADO:", exc)
        return 5
    except motor.BackendError as exc:
        print("BLOQUEADO:", exc)
        return 5
    m = salida["metricas"]
    print(f"  n={m['n']}  accuracy={m['accuracy']}"
          f"  P50={m['p50_ms']} ms  P95={m['p95_ms']} ms")
    fallos = [r for r in salida["registros"] if not r["acierto"]]
    if fallos:
        print(f"\n  fallos: {len(fallos)}")
        for r in fallos[:12]:
            print(f"    {r['id']:8s} gt={r['gt']!r:24s} elegida={r['elegida']!r}")
    nombre = f"resultados_choice_{args.backend}"
    if args.set_casos == "v2":
        nombre += "_v2"
    ruta_out = os.path.join(AQUI, nombre + ".json")
    with open(ruta_out, "w", encoding="utf-8") as fh:
        json.dump({"meta": {
            "backend": args.backend, "set": args.set_casos,
            "fichero_casos": fichero, "casos": len(casos),
            "casos_sha256": sha256(ruta),
            "ejecutado": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
            "host": motor.info_entorno()},
            "metricas": m, "registros": salida["registros"]}, fh,
            ensure_ascii=False, indent=1)
    print(f"\nresultados escritos: {ruta_out}")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--backend", choices=sorted(motor.BACKENDS))
    ap.add_argument("--checkpoint", default="router",
                    choices=["router", "english", "multilingual", "typed-decisions"])
    ap.add_argument("--modelo-ollama", default="ibm/granite4.2:8b-q4_K_M")
    ap.add_argument("--excluir-internos", action="store_true")
    ap.add_argument("--set", dest="set_casos", default="v1",
                    choices=["v1", "v2", "v3", "cuant"],
                    help="v1 = 27 congelados; v2 = +150 near-miss; v3 = +casos duros; "
                         "cuant = 120 congelados SOLO del subtipo cuantificador")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--entorno", action="store_true")
    ap.add_argument("--choice", action="store_true",
                    help="bloque choice (elegir 1 de N) en vez del bloque noul")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        total, fallos = motor.selftest()
        if fallos:
            print(f"SELFTEST: {total - len(fallos)} PASS / {len(fallos)} FALLO de {total} comprobaciones")
            for f in fallos:
                print("  -", f)
            return 1
        print(f"SELFTEST: {total} PASS / 0 FALLO de {total} comprobaciones (motor de metricas verificado)")
        return 0

    if args.entorno:
        info = motor.info_entorno()
        print(json.dumps(info, ensure_ascii=False, indent=1))
        if not info.get("laya"):
            print("\nNOTA: el paquete 'laya' NO esta instalado.")
            print("  Instalarlo + descargar checkpoints es lo que requiere TU OK:")
            print("    python3 -m pip install laya        (o 'laya[fast]' para el camino GPU)")
            print("  Pesos: ~843 MB por checkpoint; el Router precarga los tres (~2,5 GB).")
        return 0

    if not args.backend:
        ap.print_help()
        return 0

    if args.choice:
        return cmd_choice(args)

    fichero = {"v1": "casos_noul.json", "v2": "casos_v2_noul.json",
               "v3": "casos_v3_noul.json",
               "cuant": "casos_cuant_n120.json"}[args.set_casos]
    datos = motor.cargar_casos(fichero)
    casos = [c for c in datos["casos"]
             if not (args.excluir_internos and c["interno"])]
    ruta_casos = os.path.join(AQUI, fichero)

    print("=" * 68)
    print("LAYA-COMPARATIVA")
    print("=" * 68)
    print(f"casos        : {len(casos)} de {len(datos['casos'])}"
          f"{' (internos excluidos)' if args.excluir_internos else ''}")
    print(f"casos sha256 : {sha256(ruta_casos)[:16]}")
    gs = (datos["meta"].get("golden_set_sha256")
          or datos["meta"].get("golden_sha256")
          or datos["meta"].get("v2_sha256", "?"))
    print(f"golden set   : {gs[:16]}")
    print(f"fichero      : {fichero}")
    if datos["meta"].get("por_subtipo"):
        print(f"subtipo      : {datos['meta']['por_subtipo']}")
    print(f"backend      : {args.backend}"
          f"{' (' + args.checkpoint + ')' if args.backend == 'laya' else ''}")
    print()

    if args.dry_run:
        print("--dry-run: payloads que se enviarian (no se ejecuta nada) --")
        for c in casos[:3]:
            print(f"\n[{c['id']}] bloque {c['bloque']}  gt={c['gt']}")
            print("  state     :", json.dumps(c["state"], ensure_ascii=False)[:220])
            print("  preguntas :", json.dumps(
                {"afirmacion": {"type": "noul", "instructions": c["instrucciones"]}},
                ensure_ascii=False, indent=2)[:600])
        print(f"\n(... {max(0, len(casos) - 3)} casos mas)")
        return 0

    opts = {"modelo_ollama": args.modelo_ollama, "checkpoint": args.checkpoint}

    if args.backend == "laya":
        import importlib.util
        if importlib.util.find_spec("laya") is None:
            print("BLOQUEADO: el paquete 'laya' no esta instalado.")
            print("  Requiere tu OK explicito:")
            print("    python3 -m pip install laya")
            print("  Mas la descarga de pesos (~843 MB por checkpoint) del Hub de Hugging Face.")
            print("  Ejecuta primero:  python3 run_test.py --entorno")
            return 5

    try:
        salida = motor.ejecutar(casos, args.backend, opts, verbose=args.verbose)
    except ImportError as exc:
        print("BLOQUEADO:", exc)
        return 5
    except motor.BackendError as exc:
        print("BLOQUEADO:", exc)
        return 5
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR del backend {args.backend}: {type(exc).__name__}: {exc}")
        return 6

    m = salida["metricas"]
    print("METRICAS GLOBALES")
    if m.get("n"):
        print(f"  n={m['n']}  accuracy={m['accuracy']}  Brier={m['brier']}  ECE(5 bins)={m['ece5']}")
        print(f"  confianza media={m['conf_media']}  sesgo={m['sesgo_conf_menos_acierto']}"
              f"  confiado_y_fallado={m['confiado_y_fallado']}  seguro_y_acertado={m['seguro_y_acertado']}")
        print(f"  latencia P50={m['p50_ms']} ms  P95={m['p95_ms']} ms")
    else:
        print("  sin datos utilizables")
    print("\nPOR BLOQUE (A=grounding, B=trampas, D=memoria)")
    for b, mm in tabla_por_bloque(salida["registros"]).items():
        print(f"  {b}: n={mm['n']} accuracy={mm['accuracy']} Brier={mm['brier']}"
              f" ECE={mm['ece5']} sesgo={mm['sesgo_conf_menos_acierto']}")
    tabla_sub = tabla_por_subtipo(salida["registros"])
    if tabla_sub:
        print("\nPOR SUBTIPO (ordenado de peor a mejor: aqui se rompe un modelo)")
        for s, mm in sorted(tabla_sub.items(), key=lambda kv: kv[1]["accuracy"]):
            print(f"  {s:16s} n={mm['n']:3d} accuracy={mm['accuracy']:.4f}"
                  f" Brier={mm['brier']:.4f} ECE={mm['ece5']:.4f}")
    if salida["errores"]:
        print(f"\nERRORES: {salida['errores']} casos sin respuesta"
              f" (ej: {salida['primer_error']})")

    nombre = f"resultados_{args.backend}"
    if args.backend == "laya":
        nombre += f"_{args.checkpoint}"
    if args.backend == "ollama":
        suf = "".join(ch for ch in args.modelo_ollama.split("/")[-1] if ch.isalnum())
        nombre += "_" + suf
    if args.set_casos != "v1":
        nombre += "_" + args.set_casos
    if args.excluir_internos:
        nombre += "_sininternos"
    ruta = os.path.join(AQUI, nombre + ".json")
    with open(ruta, "w", encoding="utf-8") as fh:
        json.dump({
            "meta": {
                "backend": args.backend,
                "modelo_ollama": (args.modelo_ollama
                                  if args.backend == "ollama" else None),
                "num_ctx": (int(os.environ.get("LAYA_NUM_CTX", "8192"))
                            if args.backend == "ollama" else None),
                "checkpoint": args.checkpoint if args.backend == "laya" else None,
                "casos": len(casos),
                "casos_sha256": sha256(ruta_casos),
                "set": args.set_casos,
                "fichero_casos": fichero,
                "golden_set_sha256": gs,
                "ejecutado": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
                "host": motor.info_entorno(),
            },
            "metricas_globales": salida["metricas"],
            "metricas_por_bloque": tabla_por_bloque(salida["registros"]),
            "metricas_por_subtipo": tabla_por_subtipo(salida["registros"]),
            "errores": salida["errores"],
            "registros": salida["registros"],
        }, fh, ensure_ascii=False, indent=1)
    print(f"\nresultados escritos: {ruta}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
