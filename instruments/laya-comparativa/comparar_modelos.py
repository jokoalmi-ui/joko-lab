#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compara resultados_*.json del rig LAYA-COMPARATIVA.

Solo LEE ficheros ya generados: no ejecuta ningun modelo, no descarga nada.
Uso:
  .venv/bin/python comparar_modelos.py resultados_ollama_v3.json resultados_ollama_qwen25[...]
  .venv/bin/python comparar_modelos.py v3          # todos los *_v3.json (noul)
"""
import glob
import json
import os
import sys

import motor

AQUI = os.path.dirname(os.path.abspath(__file__))


def cargar(ruta):
    with open(ruta, encoding="utf-8") as fh:
        return json.load(fh)


def es_noul(d):
    regs = d.get("registros") or []
    return bool(regs) and "p" in regs[0]


def etiqueta(d, ruta):
    m = d.get("meta", {})
    modelo = m.get("modelo_ollama") or m.get("modelo") or os.path.basename(ruta)
    if m.get("checkpoint"):
        modelo += f"/{m['checkpoint']}"
    return f"{modelo} [{m.get('set', '?')}]"


def main(argumentos):
    if not argumentos:
        rutas = sorted(glob.glob(os.path.join(AQUI, "resultados_*_v3.json")))
    elif len(argumentos) == 1 and not argumentos[0].endswith(".json"):
        suf = argumentos[0]
        rutas = sorted(glob.glob(os.path.join(AQUI, f"resultados_*_{suf}.json")))
    else:
        rutas = [a if os.path.isabs(a) else os.path.join(AQUI, a) for a in argumentos]

    datos = []
    for r in rutas:
        if not os.path.exists(r):
            print(f"AVISO: no existe {r}")
            continue
        d = cargar(r)
        if not es_noul(d):
            print(f"AVISO: {os.path.basename(r)} no es del bloque noul (se salta)")
            continue
        datos.append((os.path.basename(r), etiqueta(d, r), d))
    if not datos:
        print("No hay resultados que comparar.")
        return 1

    print("=" * 78)
    print("COMPARACION DE MODELOS — mismo set, mismo codigo de puntuacion")
    print("=" * 78)
    print(f"{'modelo':34s} {'n':>4s} {'acc':>7s} {'Brier':>7s} {'ECE5':>7s} "
          f"{'P50ms':>7s} {'conf.err':>8s}")
    for nombre, etq, d in datos:
        m = (d.get("metricas_globales") or d.get("metricas")
             or motor.resumen([(r["p"], r["gt"]) for r in d["registros"]
                               if r["p"] is not None]))
        print(f"{etq[:34]:34s} {m['n']:4d} {m['accuracy']:7.4f} {m.get('brier', 0):7.4f} "
              f"{m.get('ece5', 0):7.4f} {str(m.get('p50_ms')):>7s} "
              f"{str(m.get('confiado_y_fallado')):>8s}")

    print("\nPOR SUBTIPO (accuracy). Columnas en el orden de arriba:")
    subtipos = sorted({r["subtipo"] for _, _, d in datos for r in d["registros"]
                       if r.get("subtipo")})
    cabecera = "  " + f"{'subtipo':16s}{'n':>4s}"
    for _, etq, _d in datos:
        cabecera += f"  {etq.split(' ')[0][:16]:>16s}"
    print(cabecera)
    for s in subtipos:
        linea = "  " + f"{s:16s}"
        n_ref = 0
        for _, _, d in datos:
            regs = [r for r in d["registros"] if r.get("subtipo") == s and r["p"] is not None]
            n_ref = max(n_ref, len(regs))
        linea += f"{n_ref:4d}"
        for _, _, d in datos:
            regs = [r for r in d["registros"] if r.get("subtipo") == s and r["p"] is not None]
            if not regs:
                linea += f"  {'-':>16s}"
                continue
            aciertos = sum(1 for r in regs if (r["p"] >= 0.5) == r["gt"])
            linea += f"  {aciertos / len(regs):>16.4f}"
        print(linea)

    print("\nDISCREPANCIAS (casos donde los modelos NO coinciden en acertar):")
    if len(datos) >= 2:
        mapa = []
        for _, etq, d in datos:
            mapa.append({r["id"]: r for r in d["registros"]})
        comunes = set(mapa[0])
        for m in mapa[1:]:
            comunes &= set(m)
        ids = [r["id"] for r in datos[0][2]["registros"] if r["id"] in comunes]
        ndisc = 0
        for cid in ids:
            fila = [m.get(cid) for m in mapa]
            if any(f is None or f["p"] is None for f in fila):
                continue
            ok = [(f["p"] >= 0.5) == f["gt"] for f in fila]
            if len(set(ok)) > 1:
                ndisc += 1
                sub = fila[0].get("subtipo")
                print(f"  {cid:9s} {str(sub):15s} gt={str(fila[0]['gt']):5s} "
                      + "  ".join(f"{'OK' if o else 'FALLA'}" for o in ok))
        print(f"  total casos con discrepancia: {ndisc}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
