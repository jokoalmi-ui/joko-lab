#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificador INDEPENDIENTE del set congelado CUANTIFICADOR n=120.

No se fia del campo `gt`: vuelve a deducir la verdad leyendo el TEXTO del estado,
que es la unica fuente de verdad admitida en el rig.

Comprueba, caso a caso:
  1. que el estado tiene exactamente 5 fichas,
  2. que la afirmacion declara "Las 5 fichas ... indican <campo> ...",
  3. cuantas de las 5 fichas contienen ese campo ("Año:", "Familia olfativa:"...),
  4. verdad derivada = (aparece en las 5). Se compara con `gt`.

Ademas: ids unicos, afirmaciones unicas, ninguna ficha repetida dentro del mismo
estado, subtipo correcto, reparto gt, integridad del sha256 del manifiesto.

NO mide con ningun modelo. Solo valida el material congelado.
Fail-closed: cualquier discrepancia -> exit 1.
"""
import hashlib
import json
import os
import re
import sys
from collections import Counter

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from generar_casos_v2 import CAMPOS   # noqa: E402

MARCA = "FICHA DE COLECCIÓN — "


def sha256(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def campo_de_afirmacion(af):
    """Deduce el campo desde el texto de la afirmacion, sin mirar `campo_clave`."""
    m = re.search(r"indican (el|la) (.+?) de cada perfume\.?$", af.strip())
    if not m:
        return None
    etiqueta = m.group(2).strip().lower()
    for c, (_art, txt) in CAMPOS.items():
        if txt.lower() == etiqueta:
            return c
    return None


def main():
    ruta = os.path.join(AQUI, "casos_cuant_n120.json")
    manif = os.path.join(AQUI, "MANIFIESTO-cuant-n120.txt")
    datos = json.load(open(ruta, encoding="utf-8"))
    casos = datos["casos"]
    fallos, avisos = [], []

    # --- integridad del manifiesto ---
    sha_real = sha256(ruta)
    if os.path.exists(manif):
        txt = open(manif, encoding="utf-8").read()
        if sha_real not in txt:
            fallos.append(f"manifiesto no contiene el sha256 real ({sha_real})")
        g_meta = datos["meta"]["golden_set_sha256"]
        if g_meta not in txt:
            fallos.append("manifiesto no contiene el golden_set_sha256 del meta")
    else:
        fallos.append("falta el manifiesto")

    ids, afs, derivadas = set(), set(), {"true": 0, "false": 0}
    repes, pares = Counter(), set()
    por_variante = {}
    rango_campos = []

    for c in casos:
        cid = c["id"]
        if cid in ids:
            fallos.append(f"{cid}: id repetido")
        ids.add(cid)
        if c["afirmacion"] in afs:
            repes[c["afirmacion"]] += 1     # el rig lo admite: misma afirmacion, estado distinto
        afs.add(c["afirmacion"])
        par = (c["state"]["texto"], c["afirmacion"])
        if par in pares:
            fallos.append(f"{cid}: caso repetido (mismo estado Y misma afirmacion)")
        pares.add(par)
        if c["subtipo"] != "cuantificador":
            fallos.append(f"{cid}: subtipo {c['subtipo']}")

        texto = c["state"]["texto"]
        partes = [p for p in texto.split(MARCA) if p.strip()]
        if texto.count(MARCA) != 5 or len(partes) != 5:
            fallos.append(f"{cid}: el estado no tiene 5 fichas ({texto.count(MARCA)})")
            continue

        campo = campo_de_afirmacion(c["afirmacion"])
        if campo is None:
            fallos.append(f"{cid}: no se puede deducir el campo de la afirmacion")
            continue
        if campo != c["campo_clave"]:
            fallos.append(f"{cid}: campo de la afirmacion ({campo}) != campo_clave ({c['campo_clave']})")

        etq = CAMPOS[campo][1].capitalize() + ":"
        presentes = sum(1 for p in partes if etq in p)
        m = re.search(r"Las (\d+) fichas incluidas, entre ellas (.+?), indican", c["afirmacion"])
        if not m or m.group(1) != "5":
            fallos.append(f"{cid}: la afirmacion no declara 5 fichas")
        else:
            mencionada = m.group(2).strip()
            if mencionada not in texto:
                fallos.append(f"{cid}: la ficha mencionada ('{mencionada}') no esta en el estado")

        if len({p.strip() for p in partes}) != 5:
            avisos.append(f"{cid}: dos fichas con texto identico dentro del estado")

        verdad = presentes == 5
        if verdad != bool(c["gt"]):
            fallos.append(f"{cid}: gt={c['gt']} pero el TEXTO da {verdad} "
                          f"(variante {c['variante']}, campo {campo}, aparecen {presentes}/5)")
        derivadas["true" if verdad else "false"] += 1
        por_variante[c["variante"]] = por_variante.get(c["variante"], 0) + 1
        rango_campos.append(len(c["campos_por_ficha"]))

    # --- comprobaciones de conjunto ---
    diseno = datos["meta"]["diseno"]
    esperado = sum(diseno.values())
    if len(casos) != esperado:
        fallos.append(f"total {len(casos)} != diseno declarado {esperado}")
    if (derivadas["true"] != datos["meta"]["gt_true"]
            or derivadas["false"] != datos["meta"]["gt_false"]):
        fallos.append("el reparto gt del meta no coincide con el derivado del texto")
    gt_esperado = {"5de5_full": True, "5de5_corta": True,
                   "1de5_escaso": False, "4de5_falta1": False}
    for v, esp in gt_esperado.items():
        malos = [c["id"] for c in casos if c["variante"] == v and bool(c["gt"]) != esp]
        if malos:
            fallos.append(f"variante {v}: {len(malos)} casos con gt inesperado ({malos[:3]})")
        if por_variante.get(v, 0) != diseno.get(v, 0):
            fallos.append(f"variante {v}: {por_variante.get(v, 0)} casos != diseno {diseno.get(v, 0)}")
    for v in por_variante:
        if v not in gt_esperado:
            avisos.append(f"variante no declarada en el verificador: {v}")
    rep = {k: v for k, v in repes.items() if v >= 1}
    if rep:
        avisos.append(f"{len(rep)} afirmaciones se repiten (de {len(afs)} unicas; la mas "
                      f"repetida {max(rep.values()) + 1} veces); el rig lo admite porque cada "
                      f"repeticion lleva un estado distinto")

    print("=" * 66)
    print("VERIFICACION INDEPENDIENTE — casos_cuant_n120.json")
    print("=" * 66)
    print(f"ficheros        : {os.path.basename(ruta)}  sha256 {sha_real[:16]}")
    print(f"casos           : {len(casos)}")
    print(f"gt en meta      : {datos['meta']['gt_true']} true / {datos['meta']['gt_false']} false")
    print(f"gt derivado     : {derivadas['true']} true / {derivadas['false']} false")
    print(f"por variante    : {json.dumps(por_variante, ensure_ascii=False)}")
    print(f"variantes meta  : {json.dumps(datos['meta']['por_variante'], ensure_ascii=False)}")
    print(f"ids unicos      : {len(ids)} / afirmaciones unicas: {len(afs)}")
    print(f"avisos          : {len(avisos)}")
    for a in avisos[:10]:
        print(f"  - {a}")
    print(f"FALLOS          : {len(fallos)}")
    for f in fallos[:20]:
        print(f"  - {f}")
    print("VEREDICTO       : " + ("SET CONGELADO VALIDO" if not fallos else "INVALIDO — no usar"))
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())
