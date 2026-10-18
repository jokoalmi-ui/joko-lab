#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de ROUTING de Laya sobre los 27 casos congelados.

NO descarga pesos. NO necesita torch: el routing del paquete es Python puro
(laya/lang.py no importa nada externo) y Router.route() "decide sin cargar ni
ejecutar nada" (docstring del propio paquete).

Que comprueba: a que checkpoint manda el Router un texto en ESPANOL.
Hipotesis H1 original: "el Router manda el espanol al checkpoint ingles".
El codigo del paquete la matiza: consulta 3 reglas (script no latino,
language != en, language_undecided -> default). Aqui se mide el reparto real.

Uso:  PYTHONPATH=<src del paquete> python3 test_routing.py
      (o dentro del venv donde este instalado: python3 test_routing.py)
"""
import collections
import json
import os
import sys

import laya
from laya import Router
from laya.lang import analyse   # el __init__ lo exporta como laya.detect_language

AQUI = os.path.dirname(os.path.abspath(__file__))
FICHERO = "casos_noul.json"
DETALLE = True


def cargar():
    global FICHERO
    FICHERO = "casos_v2_noul.json" if "v2" in sys.argv else "casos_noul.json"
    with open(os.path.join(AQUI, FICHERO), "r", encoding="utf-8") as fh:
        return json.load(fh)["casos"]


def texto_de(caso):
    if caso["state"]:
        return caso["state"]
    return {"texto": caso["afirmacion"]}


def main():
    global DETALLE
    casos = cargar()
    DETALLE = ("--detalle" in sys.argv) or len(casos) <= 40
    router = Router()          # sin preload: no carga ni descarga nada
    router_ml = Router(default="multilingual")

    print("=" * 96)
    print("TEST DE ROUTING — Laya", laya.__version__, "| torch importado:", "torch" in sys.modules,
          "| fichero:", FICHERO, "| casos:", len(casos))
    print("=" * 96)
    if DETALLE:
        print(f"{'caso':9s} {'bl':2s} {'script':7s} {'idioma':6s} {'ing':4s} {'indec':5s} "
              f"{'diac':6s} {'-> modelo':14s} razon")
        print("-" * 96)

    reparto, reparto_ml, indecisos, no_ingles = collections.Counter(), collections.Counter(), [], []
    for c in casos:
        st = texto_de(c)
        det = analyse(st)
        dec = router.route(st, {"afirmacion": {"type": "noul", "instructions": c["instrucciones"]}})
        dec_ml = router_ml.route(st)
        reparto[dec["model"]] += 1
        reparto_ml[dec_ml["model"]] += 1
        if det["language_undecided"] and det["script"] == "latin":
            indecisos.append(c["id"])
        if not det["is_english"]:
            no_ingles.append(c["id"])
        if DETALLE:
            print(f"{c['id']:9s} {c['bloque']:2s} {det['script']:7s} {str(det['language']):6s} "
                  f"{str(det['is_english']):4s} {str(det['language_undecided']):5s} "
                  f"{det['diacritic_rate']:<6.4f} {dec['model']:14s} {dec['reason'][:58]}")

    print("-" * 96)
    print("\nREPARTO DEL ROUTER (default='english', el de fabrica):")
    for k, v in reparto.most_common():
        print(f"   {k:14s} {v:3d}/{len(casos)}")
    print("\nREPARTO CON Router(default='multilingual'):")
    for k, v in reparto_ml.most_common():
        print(f"   {k:14s} {v:3d}/{len(casos)}")
    if len(casos) <= 40:
        print(f"\ncasos con idioma INDECISO (van al default, no al multilingue): {len(indecisos)} {indecisos}")
        print(f"casos 'no ingles' por deteccion: {len(no_ingles)} {no_ingles}")
    else:
        print(f"\ncasos con idioma INDECISO: {len(indecisos)}/{len(casos)}  (lista con --detalle)")
        print(f"casos 'no ingles' por deteccion: {len(no_ingles)}/{len(casos)}")

    # El prompt real que ve el modelo es state + pregunta. Se mide ese conjunto tambien.
    print("\n--- Mismo test con el PROMPT SIMULADO (state + afirmacion juntos) ---")
    rep2, rep2_ml = collections.Counter(), collections.Counter()
    for c in casos:
        st = texto_de(c)
        base = st["texto"] if isinstance(st, dict) else str(st)
        juntos = {"texto": base + " || " + c["afirmacion"]}
        rep2[router.route(juntos)["model"]] += 1
        rep2_ml[router_ml.route(juntos)["model"]] += 1
    for etiqueta, rep in (("default='english'", rep2), ("default='multilingual'", rep2_ml)):
        print(f"   {etiqueta:24s} " + "  ".join(f"{k}={v}" for k, v in rep.most_common()))

    # Comprobacion del instrumento: comparar mi ECE con el ece_score del propio paquete.
    print("\n--- CONTRASTE DE ECE: mio (motor.py) vs laya.ece_score ---")
    try:
        import inspect
        sys.path.insert(0, AQUI)
        import motor
        print("   firma laya.ece_score:", inspect.signature(laya.ece_score))
        vectores = [
            [(1.0, True), (1.0, True), (0.5, True), (0.5, False)],
            [(0.5, False), (0.5, False)],
            [(0.9, True), (0.9, False), (0.1, False)],
        ]
        for v in vectores:
            p = [x[0] for x in v]
            y = [1 if x[1] else 0 for x in v]
            try:
                suyo = laya.ece_score(p, y)
            except TypeError:
                suyo = laya.ece_score(v)
            mio = motor.ece(v)
            print(f"   {v} -> mio={mio:.4f}  laya={suyo}")
    except Exception as exc:  # noqa: BLE001
        print("   contraste no disponible:", type(exc).__name__, exc)

    return 0


if __name__ == "__main__":
    sys.exit(main())
