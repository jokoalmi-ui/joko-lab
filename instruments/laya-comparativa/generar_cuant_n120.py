#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera el SET CONGELADO del subtipo CUANTIFICADOR (n=120) de LAYA-COMPARATIVA.

Para que sirve
--------------
El set v3 dejaba el cuantificador con 20 casos: Laya `typed-decisions` 20/20
frente a 11/20 de los tres modelos Ollama. Antes de convertirlo en tarea hay
que ver si ese 20/20 aguanta con una muestra mayor. Este script SOLO construye
y congela los casos. NO mide: no llama a ningun modelo ni a ninguna API.

Que NO toca
-----------
- NO sobrescribe casos_noul / v2 / v3 ni ningun resultado (.json de metricas).
- BD `coleccion.db` en SOLO LECTURA (file:...?mode=ro), solo campos de catalogo
  (nombre, casa, año, familia, concentracion, volumen, genero, precio).
  NO se leen notas_personales, sensaciones, situaciones ni uso_diario.

Definicion de verdad (la misma del rig)
---------------------------------------
La verdad la define EL TEXTO del estado entregado al modelo, no la realidad:
la afirmacion "Las 5 fichas incluidas ... indican <campo> de cada perfume" es
TRUE solo si el campo aparece en las 5 fichas; si falta en alguna, FALSE.

Diseno declarado (60 TRUE / 60 FALSE)
-------------------------------------
  A  5de5_full      40  TRUE   5 fichas de filas completas (>=4 campos), las 5 con el campo
  D  5de5_corta     20  TRUE   5 fichas CORTAS (<=3 campos), las 5 con el campo
  B  1de5_escaso    20  FALSE  1 ficha con el campo (precio, volumen o un campo parcial)
                               + 4 sin el campo  -> falta en 4 de 5
  C  4de5_falta1    40  FALSE  4 fichas con el campo + 1 sin el campo -> falta en 1 de 5
                               (esta es la definicion literal del rig: "falso si a UNA le falta")

Determinista: ORDER BY id + semilla fija. Reproducible.
Escribe SOLO en su carpeta: casos_cuant_n120.json y MANIFIESTO-cuant-n120.txt
"""
import hashlib
import json
import os
import random
import sqlite3
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from generar_casos_v2 import CAMPOS, INSTR_CON_TEXTO, SQL, fmt   # noqa: E402
from generar_casos_v3 import ficha                               # noqa: E402

DB = "/home/jokoalmi/perfume-ia/data/coleccion.db"
SEMILLA = 20260924
N_A, N_D, N_B, N_C = 40, 20, 20, 40
FICHAS_POR_CASO = 5


def sha256(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def fecha_real():
    """La fecha la da el reloj del sistema, no una constante escrita a mano."""
    return subprocess.check_output(["date", "+%Y-%m-%d %H:%M:%S %Z"]).decode().strip()


def ncampos(r):
    return len([c for c in CAMPOS if fmt(c, r.get(c))])


def etiqueta(c):
    """Como aparece el campo en el texto de la ficha: 'Año', 'Familia olfativa'..."""
    return CAMPOS[c][1].capitalize()


def grupo(pool, k, offset):
    """k filas distintas por id Y por texto de ficha (una ficha repetida no es
    una prueba distinta). El paso se elige COPRIMO con el tamano del pool y el
    arranque es el offset: asi cada offset produce un conjunto distinto (el
    fallo anterior fue un paso 3 con offset i*3+1 sobre un pool de 108: el
    arranque se repetia cada 36 y la variante A se quedaba en 36 casos)."""
    n = len(pool)
    if n < k:
        return []
    paso = 1
    for cand in (7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61,
                 67, 71, 73, 79, 83, 89, 97, 101, 103, 107):
        if n % cand:
            paso = cand
            break
    out, textos = [], set()
    for intento in range(n * 4):
        r = pool[(offset % n + intento * paso + len(out) * 5) % n]
        t = ficha(r)
        if r["id"] in {x["id"] for x in out} or t in textos:
            continue
        out.append(r)
        textos.add(t)
        if len(out) == k:
            return out
    return out


def afirmacion(g, clave):
    """MISMO formato que el set v3 (comparabilidad literal)."""
    return (f"Las {len(g)} fichas incluidas, entre ellas {g[0]['nombre'].strip()}, "
            f"indican {CAMPOS[clave][0].lower()} {CAMPOS[clave][1]} de cada perfume.")


def main():
    rnd = random.Random(SEMILLA)
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    filas = [dict(r) for r in con.execute(SQL)]
    con.close()

    utiles = [r for r in filas if ncampos(r) >= 4]
    cortas = [r for r in filas if 0 < ncampos(r) <= 3]
    tiene = lambda r, c: bool(fmt(c, r.get(c)))          # noqa: E731
    pools = {c: [r for r in filas if tiene(r, c)] for c in CAMPOS}
    print(f"filas: {len(filas)}  utiles(>=4 campos): {len(utiles)}  cortas(1-3): {len(cortas)}")
    print("cobertura total: " + ", ".join(f"{c}={len(pools[c])}" for c in CAMPOS))
    print("cobertura en utiles: " + ", ".join(
        f"{c}={sum(1 for r in utiles if tiene(r, c))}" for c in CAMPOS))

    llenos = [c for c in ("anio", "concentracion", "genero", "familia")
              if all(tiene(r, c) for r in utiles)]
    print(f"campos con cobertura TOTAL dentro de utiles: {llenos}")

    casos, n = [], [0]

    def nuevo(af, gt, state, variante, clave, campos_ficha):
        n[0] += 1
        return {
            "id": f"cuant-{n[0]:03d}",
            "bloque": "H",
            "subtipo": "cuantificador",
            "variante": variante,
            "origen": "generado-cuantificador",
            "interno": False,
            "gt": gt,
            "state": {"texto": state},
            "afirmacion": af,
            "instrucciones": INSTR_CON_TEXTO.format(af=af),
            "n_fichas": FICHAS_POR_CASO,
            "campos_por_ficha": campos_ficha,
            "campo_clave": clave,
        }

    claves = set()

    def anadir(g, gt, variante, clave):
        """Anade con dedup global por (texto del estado, afirmacion). False si repetido."""
        texto = " ".join(ficha(r) for r in g)
        af = afirmacion(g, clave)
        if (texto, af) in claves:
            return False
        claves.add((texto, af))
        casos.append(nuevo(af, gt, texto, variante, clave, [ncampos(r) for r in g]))
        return True

    # ---------- A: 5 de 5, filas completas -> TRUE ----------
    hechos_a = 0
    for i in range(N_A * 8):
        if hechos_a >= N_A:
            break
        clave = llenos[i % len(llenos)]
        pool = [r for r in utiles if tiene(r, clave)]
        g = grupo(pool, FICHAS_POR_CASO, offset=i)
        if len(g) < FICHAS_POR_CASO:
            continue
        if not anadir(g, True, "5de5_full", clave):
            continue
        hechos_a += 1
    print(f"A 5de5_full  : {hechos_a}")

    # ---------- D: 5 de 5, pero fichas CORTAS -> TRUE ----------
    hechos_d = 0
    for i in range(N_D * 8):
        if hechos_d >= N_D:
            break
        clave = llenos[i % len(llenos)]
        pool = [r for r in cortas if tiene(r, clave)]
        if len(pool) < FICHAS_POR_CASO:
            pool = [r for r in filas if tiene(r, clave) and ncampos(r) < 4]
        g = grupo(pool, FICHAS_POR_CASO, offset=i)
        if len(g) < FICHAS_POR_CASO:
            continue
        if not anadir(g, True, "5de5_corta", clave):
            continue
        hechos_d += 1
    print(f"D 5de5_corta : {hechos_d}")

    # ---------- B: la fila escasa + 4 sin el campo -> FALSE ----------
    hechos_b = 0
    for i in range(N_B * 8):
        if hechos_b >= N_B:
            break
        campos_b = [c for c in ("precio", "volumen", "familia", "genero",
                                "concentracion") if pools[c]]
        if not campos_b:
            continue
        clave = campos_b[i % len(campos_b)]
        donante = pools[clave][(i // len(campos_b)) % len(pools[clave])]
        sin = [r for r in filas if not tiene(r, clave) and r["id"] != donante["id"]]
        resto = grupo(sin, FICHAS_POR_CASO - 1, offset=i)
        g = [donante] + resto
        if len(g) < FICHAS_POR_CASO:
            continue
        if not anadir(g, False, "1de5_escaso", clave):
            continue
        hechos_b += 1
    print(f"B 1de5_escaso: {hechos_b}")

    # ---------- C: 4 con el campo + 1 sin el campo -> FALSE ----------
    hechos_c = 0
    for i in range(N_C * 8):
        if hechos_c >= N_C:
            break
        clave = llenos[i % len(llenos)]
        con = [r for r in pools[clave] if tiene(r, clave)]
        sin = [r for r in filas if not tiene(r, clave)]
        cuatro = grupo(con, FICHAS_POR_CASO - 1, offset=i)
        falta = grupo(sin, 1, offset=i)
        if len(cuatro) < FICHAS_POR_CASO - 1 or not falta:
            continue
        g = cuatro + falta          # la que NO trae el campo va al final
        if not anadir(g, False, "4de5_falta1", clave):
            continue
        hechos_c += 1
    print(f"C 4de5_falta1: {hechos_c}")

    # ---------- dedup: mismo texto Y misma afirmacion = caso repetido ----------
    vistos, limpios = set(), []
    for c in casos:
        k = (c["state"]["texto"], c["afirmacion"])
        if k in vistos:
            continue
        vistos.add(k)
        limpios.append(c)
    dups = len(casos) - len(limpios)
    casos = limpios
    esperado = N_A + N_D + N_B + N_C
    if dups or len(casos) != esperado:
        print(f"ABORTADO: {len(casos)} casos != objetivo {esperado} (duplicados {dups})")
        return 4
    rnd.shuffle(casos)
    for i, c in enumerate(casos, 1):
        c["id"] = f"cuant-{i:03d}"

    longs = sorted(len(c["state"]["texto"]) for c in casos)
    por_variante = {}
    for c in casos:
        por_variante[c["variante"]] = por_variante.get(c["variante"], 0) + 1
    golden = [[c["id"], c["gt"]] for c in casos]
    meta = {
        "set": "cuant-n120",
        "descripcion": "subtipo cuantificador congelado, n para decidir si el 20/20 aguanta",
        "semilla": SEMILLA,
        "sql": " ".join(SQL.split()),
        "db": DB,
        "db_sha256": sha256(DB),
        "diseno": {"5de5_full": N_A, "5de5_corta": N_D, "1de5_escaso": N_B, "4de5_falta1": N_C},
        "total": len(casos),
        "gt_true": sum(1 for c in casos if c["gt"]),
        "gt_false": sum(1 for c in casos if not c["gt"]),
        "por_subtipo": {"cuantificador": len(casos)},
        "por_variante": por_variante,
        "duplicados_descartados": dups,
        "caracteres_state_min": longs[0],
        "caracteres_state_mediana": longs[len(longs) // 2],
        "caracteres_state_max": longs[-1],
        "verdad": "definida por el texto del estado entregado (no por la realidad)",
        "golden_set_sha256": hashlib.sha256(
            json.dumps(golden, separators=(",", ":")).encode()).hexdigest(),
        "generado": fecha_real(),
    }
    ruta = os.path.join(AQUI, "casos_cuant_n120.json")
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump({"meta": meta, "casos": casos}, f, ensure_ascii=False, indent=1)

    # manifiesto: cifras calculadas por script, nunca transcritas a mano
    sha = sha256(ruta)
    manif = os.path.join(AQUI, "MANIFIESTO-cuant-n120.txt")
    with open(manif, "w", encoding="utf-8") as f:
        f.write("SET CONGELADO — CUANTIFICADOR n=120 (LAYA-COMPARATIVA)\n")
        f.write(f"generado      : {meta['generado']}\n")
        f.write(f"fichero       : {ruta}\n")
        f.write(f"sha256 casos  : {sha}\n")
        f.write(f"golden sha256 : {meta['golden_set_sha256']}\n")
        f.write(f"db sha256     : {meta['db_sha256']}\n")
        f.write(f"total / true / false : {meta['total']} / {meta['gt_true']} / {meta['gt_false']}\n")
        f.write(f"por variante  : {json.dumps(por_variante, ensure_ascii=False)}\n")
        f.write(f"state chars   : min {longs[0]} / mediana {longs[len(longs)//2]} / max {longs[-1]}\n")
        f.write(f"duplicados    : {dups}\n")
        f.write("NO se ha medido nada con este set: solo se ha construido y congelado.\n")

    print(f"\nTOTAL: {len(casos)}  (true {meta['gt_true']} / false {meta['gt_false']})  duplicados descartados: {dups}")
    print(f"por variante: {por_variante}")
    print(f"state chars: min {longs[0]} / mediana {longs[len(longs)//2]} / max {longs[-1]}")
    print(f"escrito: {ruta}")
    print(f"sha256 casos  : {sha}")
    print(f"golden sha256 : {meta['golden_set_sha256']}")
    print(f"manifiesto    : {manif}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
