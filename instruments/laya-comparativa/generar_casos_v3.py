#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera el set v3 (casos DUROS) de LAYA-COMPARATIVA.

v3 = v1 + v2 (177, intactos) + 135 casos duros nuevos.
Los duros buscan los puntos donde un modelo pequeño suele romperse:

  multihop      dos fichas; comparar un campo y atribuir OTRO del ganador
  comparacion   dos fichas; comparacion numerica explicita (precio, volumen, año)
  distractor    dos fichas; el valor de una atribuido a la otra
  no_aparece    negacion de ausencia: "el campo X no aparece" (verdadero si falta)
  cuantificador "las N fichas indican X" (falso si a UNA le falta)
  aguja         estado largo (8 fichas) con una afirmacion sobre UNA sola

Fuente: coleccion.db en SOLO LECTURA, solo campos de catalogo.
DEFINICION DE VERDAD: la define EL TEXTO del estado entregado al modelo.
Determinista: ORDER BY id + semilla fija.
NO llama a ninguna API. NO escribe fuera de su carpeta.
"""
import hashlib
import json
import os
import random
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generar_casos_v2 import CAMPOS, INSTR_CON_TEXTO, SQL, fmt   # noqa: E402

DB = "/home/jokoalmi/perfume-ia/data/coleccion.db"
SEMILLA = 20260923
AQUI = os.path.dirname(os.path.abspath(__file__))


def ficha(r):
    """El MISMO formato de ficha que usa el set v2 (comparabilidad)."""
    return " ".join(
        [f"FICHA DE COLECCIÓN — {r['nombre'].strip()} ({r['casa'].strip()})."]
        + [f"{CAMPOS[c][1].capitalize()}: {fmt(c, r.get(c))}."
           for c in CAMPOS if fmt(c, r.get(c))]
    )


def main():
    rnd = random.Random(SEMILLA + 3)

    # --- v1 + v2 intactos (v3 es superconjunto) ---
    ruta_v2 = os.path.join(AQUI, "casos_v2_noul.json")
    if not os.path.exists(ruta_v2):
        print("ABORTADO: falta casos_v2_noul.json. Ejecuta antes generar_casos_v2.py")
        return 3
    base = json.load(open(ruta_v2, encoding="utf-8"))
    heredados = [dict(c) for c in base["casos"]]
    print(f"heredados de v2 (incluye v1): {len(heredados)}")

    # --- filas de la BD (solo lectura) ---
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    filas = [dict(r) for r in con.execute(SQL)]
    con.close()
    utiles = [r for r in filas if len([c for c in CAMPOS if fmt(c, r.get(c))]) >= 4]
    print(f"filas utilizables: {len(utiles)}")

    casos = []
    n = [0]

    def nuevo(af, subtipo, gt, state):
        n[0] += 1
        return {
            "id": f"hard-{n[0]:03d}",
            "bloque": "H",
            "subtipo": subtipo,
            "origen": "generado-duro",
            "interno": False,
            "gt": gt,
            "state": {"texto": state},
            "afirmacion": af,
            "instrucciones": INSTR_CON_TEXTO.format(af=af),
        }

    def par(i, salto):
        """Dos filas distintas y deterministas."""
        a = utiles[i % len(utiles)]
        b = utiles[(i * 7 + salto) % len(utiles)]
        return (a, b) if a["id"] != b["id"] else (a, utiles[(i + 3) % len(utiles)])

    # pools por campo: garantizan pares comparables (el error anterior fue
    # emparejar filas arbitrarias, de las que casi ninguna tenia precio Y volumen)
    pools = {c: [r for r in utiles if fmt(c, r.get(c))] for c in CAMPOS}
    print("pool por campo: " + ", ".join(f"{c}={len(v)}" for c, v in pools.items()))

    # ---------- 1) multihop: 25 (comparar AÑO y atribuir OTRO campo del ganador) ----------
    # Nota medida: en esta BD precio=1 fila y volumen=1 fila de 328, asi que el
    # eje de comparacion solo puede ser el año (108/108 con dato).
    hechos = 0
    for i in range(25):
        atr = "concentracion" if i % 2 == 0 else "familia"
        pool = [r for r in pools["anio"] if fmt(atr, r.get(atr))]
        if len(pool) < 2:
            continue
        a = pool[(i * 3) % len(pool)]
        b = pool[(i * 5 + 1) % len(pool)]
        if a["id"] == b["id"]:
            continue
        va, vb = float(a["anio"]), float(b["anio"])
        if va == vb:
            continue
        ganador, otro = (a, b) if va > vb else (b, a)
        v_gan, v_otro = fmt(atr, ganador.get(atr)), fmt(atr, otro.get(atr))
        if i % 2 == 0 or not v_otro or v_otro == v_gan:
            valor, gt = v_gan, True          # afirmacion verdadera
        else:
            valor, gt = v_otro, False        # el valor del PERDEDOR atribuido al ganador
        af = (f"Comparando {a['nombre'].strip()} y {b['nombre'].strip()}, el más reciente "
              f"tiene {CAMPOS[atr][1]} {valor}.")
        casos.append(nuevo(af, "multihop", gt, ficha(a) + " " + ficha(b)))
        hechos += 1
    print(f"multihop: {hechos}")

    # ---------- 2) comparacion: 25 (eje unico disponible: el año) ----------
    hechos = 0
    for i in range(25):
        campo = "anio"
        pool = pools[campo]
        if len(pool) < 2:
            continue
        a = pool[(i * 3) % len(pool)]
        b = pool[(i * 5 + 1) % len(pool)]
        if a["id"] == b["id"]:
            continue
        va, vb = float(a[campo]), float(b[campo])
        if va == vb:
            continue
        primero, segundo = (a, b) if i % 2 == 0 else (b, a)
        vp, vs = (va, vb) if i % 2 == 0 else (vb, va)
        n1, n2 = primero["nombre"].strip(), segundo["nombre"].strip()
        af = f"El año de {n1} es posterior al año de {n2}."
        casos.append(nuevo(af, "comparacion", vp > vs, ficha(a) + " " + ficha(b)))
        hechos += 1
    print(f"comparacion: {hechos}")

    # ---------- 3) distractor: 25 (valor de una ficha atribuido a la otra) ----------
    hechos = 0
    for i in range(25):
        a, b = par(i, 13)
        presentes = [c for c in CAMPOS if fmt(c, a.get(c)) and fmt(c, b.get(c))]
        if not presentes:
            continue
        c = presentes[i % len(presentes)]
        if i % 2 == 0:      # verdadera
            af = f"{CAMPOS[c][0]} {CAMPOS[c][1]} de {a['nombre'].strip()} es {fmt(c, a.get(c))}."
            gt = True
        else:               # falsa: el valor que aparece es el de la OTRA ficha
            af = f"{CAMPOS[c][0]} {CAMPOS[c][1]} de {a['nombre'].strip()} es {fmt(c, b.get(c))}."
            gt = False
        casos.append(nuevo(af, "distractor", gt, ficha(a) + " " + ficha(b)))
        hechos += 1
    print(f"distractor: {hechos}")

    # ---------- 4) no_aparece: 25 (negacion de ausencia) ----------
    hechos = 0
    for i in range(25):
        r = utiles[(i * 3) % len(utiles)]
        presentes = [c for c in CAMPOS if fmt(c, r.get(c))]
        ausentes = [c for c in CAMPOS if not fmt(c, r.get(c))]
        if i % 2 == 0 and ausentes:
            c = ausentes[i % len(ausentes)]
            gt = True
        elif presentes:
            c = presentes[i % len(presentes)]
            gt = False
        else:
            continue
        af = f"{CAMPOS[c][0]} {CAMPOS[c][1]} de {r['nombre'].strip()} no aparece en la ficha."
        casos.append(nuevo(af, "no_aparece", gt, ficha(r)))
        hechos += 1
    print(f"no_aparece: {hechos}")

    # ---------- 5) cuantificador: 20 ("las N fichas indican X") ----------
    # Las VERDADERAS usan campos con cobertura total (año/familia/concentracion/
    # genero: 108/108). Las FALSAS meten a proposito la unica fila que trae
    # precio o volumen entre otras 4 que no lo traen.
    llenos = [c for c in ("anio", "familia", "concentracion", "genero") if len(pools[c]) >= 20]
    hechos = 0
    for i in range(20):
        grupo = []
        if i % 2 == 0:
            clave = llenos[i % len(llenos)]
            j = i * 3
            while len(grupo) < 5:
                r = utiles[(j * 7 + len(grupo) * 5) % len(utiles)]
                if all(r["id"] != g["id"] for g in grupo):
                    grupo.append(r)
                j += 1
            gt = True
        else:
            escasos = [c for c in ("precio", "volumen") if pools[c]]
            if not escasos:
                continue
            clave = escasos[i % len(escasos)]
            grupo = [pools[clave][0]]
            j = i * 5
            while len(grupo) < 5:
                r = utiles[(j * 3 + len(grupo) * 7) % len(utiles)]
                if all(r["id"] != g["id"] for g in grupo) and not fmt(clave, r.get(clave)):
                    grupo.append(r)
                j += 1
            gt = False
        state = " ".join(ficha(r) for r in grupo)
        af = (f"Las {len(grupo)} fichas incluidas, entre ellas "
              f"{grupo[0]['nombre'].strip()}, indican "
              f"{CAMPOS[clave][0].lower()} {CAMPOS[clave][1]} de cada perfume.")
        casos.append(nuevo(af, "cuantificador", gt, state))
        hechos += 1
    print(f"cuantificador: {hechos}")

    # ---------- 6) aguja: 15 (estado largo: 8 fichas, pregunta por UNA) ----------
    hechos = 0
    for i in range(15):
        grupo, j = [], i * 9
        while len(grupo) < 8:
            r = utiles[(j * 3 + len(grupo) * 11) % len(utiles)]
            if all(r["id"] != g["id"] for g in grupo):
                grupo.append(r)
            j += 1
        diana = grupo[i % len(grupo)]
        otras = [r for r in grupo if r["id"] != diana["id"]]
        presentes = [c for c in CAMPOS if fmt(c, diana.get(c))]
        if not presentes:
            continue
        c = presentes[i % len(presentes)]
        if i % 2 == 0:
            af = f"{CAMPOS[c][0]} {CAMPOS[c][1]} de {diana['nombre'].strip()} es {fmt(c, diana.get(c))}."
            gt = True
        else:
            donante = [r for r in otras if fmt(c, r.get(c)) and fmt(c, r.get(c)) != fmt(c, diana.get(c))]
            if not donante:
                continue
            af = (f"{CAMPOS[c][0]} {CAMPOS[c][1]} de {diana['nombre'].strip()} es "
                  f"{fmt(c, donante[0].get(c))}.")
            gt = False
        casos.append(nuevo(af, "aguja", gt, " ".join(ficha(r) for r in grupo)))
        hechos += 1
    print(f"aguja: {hechos}")

    todos = heredados + casos
    # deduplicado: dos casos son duplicados solo si coinciden estado Y afirmacion
    # (afirmaciones iguales con estados distintos SI son juicios distintos)
    vistos, limpios, dups = set(), [], 0
    for c in todos:
        clave_dedup = ((c["state"] or {}).get("texto", ""), c["afirmacion"])
        if clave_dedup in vistos:
            dups += 1
            continue
        vistos.add(clave_dedup)
        limpios.append(c)
    todos = limpios

    longs = sorted(len((c["state"] or {}).get("texto", "")) for c in todos)
    meta = {
        "set": "v3-duros",
        "semilla": SEMILLA + 3,
        "sql": " ".join(SQL.split()),
        "heredados_de_v2": len(heredados),
        "duros_nuevos": len(casos),
        "total": len(todos),
        "gt_true": sum(1 for c in todos if c["gt"]),
        "gt_false": sum(1 for c in todos if not c["gt"]),
        "por_subtipo": {},
        "caracteres_state_min": longs[0],
        "caracteres_state_mediana": longs[len(longs) // 2],
        "caracteres_state_max": longs[-1],
        "verdad": "definida por el texto del estado entregado (no por la realidad)",
        "v2_sha256": hashlib.sha256(open(ruta_v2, "rb").read()).hexdigest(),
    }
    for c in todos:
        meta["por_subtipo"][c["subtipo"]] = meta["por_subtipo"].get(c["subtipo"], 0) + 1
    afs = [c["afirmacion"] for c in todos]
    meta["afirmaciones_duplicadas"] = len(afs) - len(set(afs))
    meta["afirmaciones_duplicadas_descartadas"] = dups

    ruta = os.path.join(AQUI, "casos_v3_noul.json")
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump({"meta": meta, "casos": todos}, f, ensure_ascii=False, indent=1)

    print(f"\nTOTAL v3: {len(todos)}  (true {meta['gt_true']} / false {meta['gt_false']})")
    print(f"  por subtipo: {meta['por_subtipo']}")
    print(f"  duplicadas : {meta['afirmaciones_duplicadas']}")
    print(f"  state chars: min {meta['caracteres_state_min']} / "
          f"mediana {meta['caracteres_state_mediana']} / max {meta['caracteres_state_max']}")
    print(f"escrito: {ruta}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
