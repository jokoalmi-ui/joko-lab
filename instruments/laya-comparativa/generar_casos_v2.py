#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera el set v2 (near-miss) de LAYA-COMPARATIVA.

Fuente de datos: coleccion.db en SOLO LECTURA (file:...?mode=ro).
Solo campos de catalogo: nombre, casa, año, familia olfativa, concentracion,
volumen, genero, precio. NO se leen notas_personales, sensaciones, situaciones
ni uso_diario (datos personales).

DEFINICION DE VERDAD: la verdad de cada caso la define EL PROPIO TEXTO del
estado que se le entrega al modelo. No la realidad, no la BD. Si la afirmacion
es derivable del texto -> true. Si no lo es (valor vecino, campo ausente,
negacion, soporte parcial) -> false. Eso hace el instrumento independiente de
si la BD tiene erratas.

Determinista: ORDER BY id + semilla fija. Reproducible.

NO llama a ninguna API. NO escribe nada fuera de su carpeta.
"""
import hashlib
import json
import os
import random
import sqlite3
import sys

DB = "/home/jokoalmi/perfume-ia/data/coleccion.db"
SEMILLA = 20260923
GOLDEN = "/home/jokoalmi/joko-lab/tools/golden_set_alucinaciones.json"
GOLDEN_SHA256 = "2a2da99cc7001128f9c58bc2812f78a590f1a13aa34195191dafa01934fbe1d1"
AQUI = os.path.dirname(os.path.abspath(__file__))

SQL = """
SELECT p.id, p.nombre AS nombre, c.nombre AS casa, p.año AS anio,
       f.nombre AS familia, p.concentracion AS concentracion,
       p.volumen_ml AS volumen, p.genero AS genero, p.precio AS precio
FROM perfumes p
JOIN casas c ON c.id = p.casa_id
LEFT JOIN familias_olfativas f ON f.id = p.familia_id
WHERE p.nombre IS NOT NULL AND TRIM(p.nombre) <> ''
  AND c.nombre IS NOT NULL AND TRIM(c.nombre) <> ''
ORDER BY p.id
"""

# campo -> (articulo, etiqueta)
CAMPOS = {
    "anio": ("El", "año"),
    "familia": ("La", "familia olfativa"),
    "concentracion": ("La", "concentración"),
    "volumen": ("El", "volumen"),
    "genero": ("El", "género"),
    "precio": ("El", "precio"),
}

INSTR_CON_TEXTO = (
    "Usa UNICAMENTE el texto del estado que se te da. Decide si la afirmacion "
    "es verdadera segun ese texto. Si el texto no contiene el dato, la "
    "afirmacion es falsa. Afirmacion: «{af}»"
)
INSTR_SIN_TEXTO = (
    "Sin texto de apoyo. Decide si la afirmacion es verdadera en el mundo real. "
    "Afirmacion: «{af}»"
)


def fmt(campo, valor):
    if valor is None:
        return None
    if campo == "precio":
        try:
            return f"{float(valor):.2f}".replace(".", ",") + " EUR"
        except (TypeError, ValueError):
            return None
    if campo == "volumen":
        return f"{int(valor)} ml"
    return str(valor).strip() or None


def main():
    rnd = random.Random(SEMILLA)

    # --- golden set congelado: se conserva v1 dentro de v2 como marca 'origen' ---
    raw = open(GOLDEN, "rb").read()
    if hashlib.sha256(raw).hexdigest() != GOLDEN_SHA256:
        print("ABORTADO: el golden set congelado ha cambiado")
        return 2
    golden = json.loads(raw)["preguntas"]

    # --- filas de la BD (solo lectura) ---
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    filas = [dict(r) for r in con.execute(SQL)]
    con.close()

    # valores posibles por campo (para "vecinos plausibles")
    universo = {c: [] for c in CAMPOS}
    for r in filas:
        for c in CAMPOS:
            v = fmt(c, r.get(c))
            if v:
                universo[c].append(v)
    universo = {c: sorted(set(v)) for c, v in universo.items()}

    # filas utilizables: al menos 3 campos con dato ademas de nombre y casa
    utiles = []
    for r in filas:
        presentes = [c for c in CAMPOS if fmt(c, r.get(c))]
        if len(presentes) >= 4:
            utiles.append((r, presentes))
    print(f"filas totales en la BD      : {len(filas)}")
    print(f"filas utilizables (>=4 campos): {len(utiles)}")

    # 30 filas repartidas por todo el catalogo (paso regular, determinista)
    paso = max(1, len(utiles) // 30)
    seleccion = utiles[::paso][:30]
    print(f"filas seleccionadas         : {len(seleccion)}")

    def vecino(campo, actual):
        cands = [v for v in universo[campo] if v != actual]
        return rnd.choice(cands) if cands else None

    casos = []
    n = 0

    def nuevo(af, bloque, subtipo, gt, state, origen, interno=False):
        nonlocal n
        n += 1
        return {
            "id": f"gen-{n:03d}",
            "bloque": bloque,
            "subtipo": subtipo,
            "origen": origen,
            "interno": interno,
            "gt": gt,
            "state": ({"texto": state} if state else None),
            "afirmacion": af,
            "instrucciones": (INSTR_CON_TEXTO if state else INSTR_SIN_TEXTO).format(af=af),
        }

    for i, (r, presentes) in enumerate(seleccion):
        nombre, casa = r["nombre"].strip(), r["casa"].strip()
        state = " ".join(
            [f"FICHA DE COLECCIÓN — {nombre} ({casa})."]
            + [f"{CAMPOS[c][1].capitalize()}: {fmt(c, r.get(c))}."
               for c in CAMPOS if fmt(c, r.get(c))]
        )
        # 1) verdadera, literal (control facil)
        c1 = rnd.choice(presentes)
        v1 = fmt(c1, r.get(c1))
        casos.append(nuevo(
            f"{CAMPOS[c1][0]} {CAMPOS[c1][1]} de {nombre} es {v1}.",
            "A", "literal", True, state, "generado"))
        # 2) verdadera, parafraseada (orden y forma distintos)
        c2 = rnd.choice(presentes)
        v2 = fmt(c2, r.get(c2))
        casos.append(nuevo(
            f"En la ficha de {nombre}, {CAMPOS[c2][0].lower()} "
            f"{CAMPOS[c2][1]} consta como {v2}.",
            "A", "parafrasis", True, state, "generado"))
        # 3) falsa, valor vecino (el dato esta, pero con otro valor)
        c3 = rnd.choice(presentes)
        v3 = fmt(c3, r.get(c3))
        v3v = vecino(c3, v3)
        if v3v:
            casos.append(nuevo(
                f"{CAMPOS[c3][0]} {CAMPOS[c3][1]} de {nombre} es {v3v}.",
                "A", "valor_vecino", False, state, "generado"))
        # 4) falsa, campo AUSENTE del state (hay que notar la ausencia)
        ausentes = [c for c in CAMPOS if not fmt(c, r.get(c))]
        if ausentes:
            c4 = rnd.choice(ausentes)
            base = vecino(c4, None)
            if base:
                casos.append(nuevo(
                    f"{CAMPOS[c4][0]} {CAMPOS[c4][1]} de {nombre} es {base}.",
                    "A", "campo_ausente", False, state, "generado"))
        # 5) falsa, negacion de un dato que SI esta
        if i % 2 == 0:
            c5 = rnd.choice(presentes)
            v5 = fmt(c5, r.get(c5))
            casos.append(nuevo(
                f"{CAMPOS[c5][0]} {CAMPOS[c5][1]} de {nombre} no es {v5}.",
                "A", "negacion", False, state, "generado"))
        # 6) falsa, soporte parcial (una clausula cierta + una falsa)
        if i % 2 == 1 and len(presentes) >= 2:
            ca, cb = rnd.sample(presentes, 2)
            va = fmt(ca, r.get(ca))
            vb = vecino(cb, fmt(cb, r.get(cb)))
            if vb:
                casos.append(nuevo(
                    f"{CAMPOS[ca][0]} {CAMPOS[ca][1]} de {nombre} es {va} y "
                    f"{CAMPOS[cb][0]} {CAMPOS[cb][1]} es {vb}.",
                    "A", "soporte_parcial", False, state, "generado"))

    # --- casos del golden set: se reutilizan TAL CUAL desde el v1 ya verificado ---
    # (reutilizarlos garantiza que v1 queda contenido en v2, con el mismo state,
    #  la misma instruccion y el mismo gt; asi los dos sets son comparables)
    ruta_v1 = os.path.join(AQUI, "casos_noul.json")
    if not os.path.exists(ruta_v1):
        print("ABORTADO: falta casos_noul.json (el v1). Ejecuta antes preparar_casos.py")
        return 3
    v1 = json.load(open(ruta_v1, encoding="utf-8"))
    if v1["meta"]["golden_set_sha256"] != GOLDEN_SHA256:
        print("ABORTADO: el v1 no procede del golden set congelado")
        return 2
    for c in v1["casos"]:
        c2 = dict(c)
        c2.setdefault("origen", "golden")
        c2.setdefault("subtipo", {"A": "grounding", "B": "trampa", "D": "memoria"}.get(c2["bloque"], "?"))
        casos.append(c2)

    # --- casos choice con opciones reales de la BD (4 opciones < limite 20) ---
    choice = []
    for i, (r, presentes) in enumerate(seleccion[:20]):
        c = rnd.choice([x for x in presentes if len(universo[x]) >= 4])
        correcto = fmt(c, r.get(c))
        opciones = [correcto]
        while len(opciones) < 4:
            v = vecino(c, correcto)
            if v and v not in opciones:
                opciones.append(v)
        rnd.shuffle(opciones)
        choice.append({
            "id": f"cho-{i+1:02d}",
            "origen": "generado",
            "interno": False,
            "campo": CAMPOS[c][1],
            "state": {"texto": " ".join(
                [f"FICHA DE COLECCIÓN — {r['nombre'].strip()} ({r['casa'].strip()})."]
                + [f"{CAMPOS[x][1].capitalize()}: {fmt(x, r.get(x))}."
                   for x in CAMPOS if fmt(x, r.get(x))])},
            "pregunta": f"¿Cuál es {CAMPOS[c][0].lower() if CAMPOS[c][0]=='El' else 'la'} "
                        f"{CAMPOS[c][1]} de {r['nombre'].strip()}?",
            "opciones": opciones,
            "gt": correcto,
        })

    meta_noul = {
        "set": "v2-near-miss",
        "semilla": SEMILLA,
        "sql": " ".join(SQL.split()),
        "filas_bd_totales": len(filas),
        "filas_seleccionadas": len(seleccion),
        "golden_sha256": GOLDEN_SHA256,
        "verdad": "definida por el texto del estado entregado (no por la realidad)",
        "total": len(casos),
        "por_origen": {},
        "por_subtipo": {},
        "gt_true": sum(1 for c in casos if c["gt"]),
        "gt_false": sum(1 for c in casos if not c["gt"]),
    }
    for c in casos:
        meta_noul["por_origen"][c["origen"]] = meta_noul["por_origen"].get(c["origen"], 0) + 1
        meta_noul["por_subtipo"][c["subtipo"]] = meta_noul["por_subtipo"].get(c["subtipo"], 0) + 1

    afs = [c["afirmacion"] for c in casos]
    dups = len(afs) - len(set(afs))
    meta_noul["afirmaciones_duplicadas"] = dups

    ruta_noul = os.path.join(AQUI, "casos_v2_noul.json")
    ruta_choice = os.path.join(AQUI, "casos_v2_choice.json")
    with open(ruta_noul, "w", encoding="utf-8") as f:
        json.dump({"meta": meta_noul, "casos": casos}, f, ensure_ascii=False, indent=1)
    with open(ruta_choice, "w", encoding="utf-8") as f:
        json.dump({"meta": {"set": "v2-choice", "semilla": SEMILLA, "total": len(choice)},
                   "casos": choice}, f, ensure_ascii=False, indent=1)

    print(f"casos noul                  : {len(casos)}  (true {meta_noul['gt_true']} / false {meta_noul['gt_false']})")
    print(f"  por origen                : {meta_noul['por_origen']}")
    print(f"  por subtipo               : {meta_noul['por_subtipo']}")
    print(f"  afirmaciones duplicadas   : {dups}")
    print(f"casos choice                : {len(choice)}")
    print(f"escrito: {ruta_noul}")
    print(f"escrito: {ruta_choice}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
