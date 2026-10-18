#!/usr/bin/env python3
"""Rango frio<->calido por perfume (E, 20-sep-2026). SOLO LECTURA de coleccion.db.

Que hace
  Convierte `perfumes.sensaciones` (JSON array de etiquetas) en un indice termico
  -1.0 (frio) .. +1.0 (calido) por perfume, y comprueba si ese indice predice la
  temperatura a la que el perfume se ha usado de verdad (`uso_diario.clima_temp`).

Que NO hace
  No escribe en la BD. La escritura de la tabla derivada `rango_termico` la hace
  tools/rango_termico_write.py (con gate + backup + verificacion), que importa
  `calcular` de este fichero.

LIMITE DECLARADO (medido 20-sep-2026, no opinion)
  El indice NO discrimina: r = -0.062 sobre 72 usos con clima_temp; medias por banda
  frio 26.0 / medio 26.1 / calido 25.6 C. Causas probables: (a) `clima_temp` guardaba
  la MAXIMA del dia (metrica vieja, hasta 19-sep-2026), no la temperatura de la
  decision; (b) 74 usos en 39 perfumes (26 con un solo uso); (c) la eleccion real
  depende de mas cosas que la temperatura. CONCLUSION: el indice es un dato
  DECLARADO (lo que las etiquetas de sensaciones dicen), NO una prediccion validada.
  No venderlo como "lo que funciona" (RULE-013/RULE-015).

Uso:
  python3 rango_termico.py                 # resumen + validacion
  python3 rango_termico.py --perfume 997   # un perfume concreto (Flamenco)
  python3 rango_termico.py --json          # volcado completo (para la tabla)
  python3 rango_termico.py --top 15        # mas calidos / mas frios

Fail-closed: si la BD no se puede leer, AVISA y rc=2 (nunca silencio).
"""
import argparse
import json
import sqlite3
import sys

DB = "/home/jokoalmi/perfume-ia/data/coleccion.db"

# Etiquetas de `sensaciones` -> peso termico. Negativo = frio, positivo = calido.
# Solo se usan las etiquetas que EXISTEN en la BD (comprobado 20-sep-2026:
# 320 de 328 perfumes con sensaciones; las que no tienen peso se cuentan aparte).
PESOS = {
    "marino": -1.0, "fresco": -0.8, "citrico": -0.6, "ligero": -0.5, "mineral": -0.4,
    "seco": -0.3, "verde": -0.3, "brillante": -0.2, "limpio": -0.2, "herbal": -0.2,
    "vibrante": -0.1, "alegre": -0.1, "floral": -0.1, "frutal": -0.1, "natural": -0.1,
    "suave": 0.0, "elegante": 0.0, "clasico": 0.0, "discreto": 0.0, "renovado": 0.0,
    "mistico": 0.0, "romantico": 0.0, "serio": 0.0, "te": 0.0,
    "imponente": 0.1, "masculino": 0.1, "complejo": 0.1, "almizclado": 0.2,
    "protector": 0.2, "sensual": 0.2, "penetrante": 0.2, "profundo": 0.3,
    "confortable": 0.3, "exotico": 0.3, "intenso": 0.3, "lujoso": 0.3,
    "envolvente": 0.3, "amaderado": 0.4, "embriagador": 0.4, "oscuro": 0.4,
    "balsamico": 0.4, "especiado": 0.5, "cuero": 0.5, "tabaco": 0.5, "terroso": 0.5,
    "cremoso": 0.5, "resinoso": 0.6, "dulce": 0.6, "ahumado": 0.6, "oriental": 0.7,
    "animal": 0.7, "calido": 0.8, "ambarado": 0.8, "gourmand": 0.9,
}
ORDEN = {"primavera": 0, "verano": 1, "otoño": 2, "invierno": 3}
ALIAS = {"primavera": "primavera", "verano": "verano", "otono": "otoño",
         "invierno": "invierno"}


def norm_estaciones(txt):
    """'otoño-invierno' -> (['otoño','invierno'], True). Devuelve (lista, es_compuesta).

    La norma del lab (perfume-ia/references/clasificacion-temporada-detalle.md) dice
    que un valor COMPUESTO no es valido para decants: el estuche tiene 4 secciones.
    Aqui solo se detecta y se marca; NO se corrige (eso exige criterio olfativo).
    """
    if not txt:
        return [], False
    t = txt.strip().lower().replace("/", ",").replace("-", ",").replace(";", ",")
    t = t.replace(" y ", ",")
    fuera = []
    for trozo in t.split(","):
        k = trozo.strip().replace("á", "a").replace("é", "e").replace("í", "i")
        k = k.replace("ó", "o").replace("ú", "u").replace("ñ", "n")
        if k in ALIAS:
            v = ALIAS[k]
            if v not in fuera:
                fuera.append(v)
    fuera.sort(key=lambda e: ORDEN[e])
    return fuera, len(fuera) > 1


def indice_sensaciones(sens):
    """JSON array -> (indice, n_con_peso, etiquetas_sin_peso). None si no hay dato."""
    if not sens:
        return None, 0, []
    try:
        etiquetas = json.loads(sens)
    except Exception:
        return None, 0, []
    if not isinstance(etiquetas, list) or not etiquetas:
        return None, 0, []
    pesos, sin_peso = [], []
    for e in etiquetas:
        k = str(e).strip().lower().replace("á", "a").replace("é", "e")
        k = k.replace("í", "i").replace("ó", "o").replace("ú", "u")
        if k in PESOS:
            pesos.append(PESOS[k])
        else:
            sin_peso.append(str(e).strip())
    if not pesos:
        return None, 0, sin_peso
    return sum(pesos) / len(pesos), len(pesos), sin_peso


def banda(ix):
    if ix is None:
        return None
    if ix <= -0.3:
        return "frio"
    if ix >= 0.3:
        return "calido"
    return "medio"


def calcular(db=DB):
    """Devuelve (perfumes, usos, meta). Solo lectura."""
    con = sqlite3.connect("file:%s?mode=ro" % db, uri=True)
    perfumes = {}
    for pid, nombre, temporada, sens in con.execute(
            "SELECT id, nombre, temporada, sensaciones FROM perfumes"):
        ix, n, sin_peso = indice_sensaciones(sens)
        est, compuesta = norm_estaciones(temporada)
        perfumes[pid] = {"perfume_id": pid, "nombre": nombre, "indice": ix,
                         "banda": banda(ix), "n_etiquetas": n, "sin_peso": sin_peso,
                         "estaciones": est, "temporada_compuesta": compuesta}
    usos = [{"perfume_id": p, "fecha": f, "clima_temp": t}
            for p, f, t in con.execute(
                "SELECT perfume_id, fecha, clima_temp FROM uso_diario ORDER BY fecha")]
    con.close()
    return perfumes, usos, {"db": db}


def validacion(perfumes, usos):
    """Correlacion de Pearson entre indice y clima_temp de los usos. Devuelve dict."""
    pares = [(perfumes[u["perfume_id"]]["indice"], u["clima_temp"]) for u in usos
             if u["perfume_id"] in perfumes and u["clima_temp"] is not None
             and perfumes[u["perfume_id"]]["indice"] is not None]
    n = len(pares)
    if n < 3:
        return {"n": n, "r": None}
    xs = [p[0] for p in pares]
    ys = [p[1] for p in pares]
    mx, my = sum(xs) / n, sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in pares)
    den = (sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in ys)) ** 0.5
    r = num / den if den else None
    por_banda = {}
    for b in ("frio", "medio", "calido"):
        t = [y for x, y in pares
             if banda(x) == b]
        por_banda[b] = (round(sum(t) / len(t), 1) if t else None, len(t))
    return {"n": n, "r": round(r, 3) if r is not None else None, "por_banda": por_banda}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--perfume", type=int, default=None)
    ap.add_argument("--top", type=int, default=0)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--db", default=DB)
    a = ap.parse_args()
    try:
        perfumes, usos, _ = calcular(a.db)
    except Exception as e:
        print("AVISO rango_termico: no se puede leer la BD (%s: %s)" % (type(e).__name__, e))
        return 2
    if a.json:
        print(json.dumps({"perfumes": sorted(perfumes.values(), key=lambda d: d["perfume_id"]),
                          "validacion": validacion(perfumes, usos)}, ensure_ascii=False))
        return 0
    con_ix = [p for p in perfumes.values() if p["indice"] is not None]
    print("PERFUMES: %d | con indice: %d | sin sensaciones: %d"
          % (len(perfumes), len(con_ix), len(perfumes) - len(con_ix)))
    for b in ("frio", "medio", "calido"):
        print("  banda %-6s: %d" % (b, sum(1 for p in con_ix if p["banda"] == b)))
    comp = [p for p in perfumes.values() if p["temporada_compuesta"]]
    print("temporada COMPUESTA (norma del lab: no valida en decants): %d perfumes" % len(comp))
    v = validacion(perfumes, usos)
    print("VALIDACION vs usos: n=%s | r=%s" % (v["n"], v["r"]))
    for b, (med, n) in (v.get("por_banda") or {}).items():
        print("  banda %-6s -> clima_temp media %s C (n=%d)" % (b, med, n))
    if a.perfume:
        p = perfumes.get(a.perfume)
        print("PERFUME %s: %s" % (a.perfume, json.dumps(p, ensure_ascii=False) if p else "no existe"))
    if a.top:
        orden = sorted(con_ix, key=lambda p: p["indice"])
        print("--- mas FRIOS ---")
        for p in orden[:a.top]:
            print("  %+.2f %s" % (p["indice"], p["nombre"][:60]))
        print("--- mas CALIDOS ---")
        for p in orden[-a.top:][::-1]:
            print("  %+.2f %s" % (p["indice"], p["nombre"][:60]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
