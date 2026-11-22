#!/usr/bin/env python3
"""Candidatos para la ficha del perfume del dia, FILTRADOS POR TEMPORADA.

Problema que resuelve: el flujo elegia por clima y exclusion de 60 dias, sin
mirar la temporada, y llego a proponer un perfume de primavera/verano en
noviembre. Pero `perfumes.temporada` es ORIENTATIVO (47 % del historial real
cae "fuera" de su etiqueta), asi que no se usa como filtro binario: se puntua
la compatibilidad y solo se bloquea lo OPUESTO, con fallback declarado.

Uso:
  candidatos_ficha.py --fecha 2026-11-18 [--media 17.7] [--json salida.json]
                      [--dias-exclusion 60] [--incluir-fuera]

Salida: ranking de elegibles + bloqueados por temporada con motivo.
Solo lectura sobre coleccion.db.
"""
import argparse
import collections
import datetime
import json
import re
import sqlite3
import unicodedata
from pathlib import Path

DB = "/home/jokoalmi/perfume-ia/data/coleccion.db"
FICHAS = Path("/home/jokoalmi/joko-lab/research/infografias")

# Estaciones astronomicas (hemisferio norte)
EST = [((3, 20), (6, 20), "primavera"), ((6, 21), (9, 22), "verano"),
       ((9, 23), (12, 20), "otono"), ((12, 21), (3, 19), "invierno")]
ADY = {"primavera": ("invierno", "verano"), "verano": ("primavera", "otono"),
       "otono": ("verano", "invierno"), "invierno": ("otono", "primavera")}
# Mitades del anio: es la agrupacion que corta de verdad el error. Un perfume
# etiquetado SOLO con estaciones de la mitad opuesta no se recomienda.
MITAD = {"primavera": "calida", "verano": "calida",
         "otono": "fria", "invierno": "fria"}


def estacion(d):
    md = (d.month, d.day)
    for ini, fin, nom in EST:
        if ini <= fin:
            if ini <= md <= fin:
                return nom
        elif md >= ini or md <= fin:
            return nom
    raise ValueError("fecha sin estacion: %s" % d)


def estacion_efectiva(d, media):
    """La etiqueta del calendario se corrige con la temperatura prevista:
    el lab ya usa el clima real por encima del mes (6-7 C en agosto = invierno)."""
    e = estacion(d)
    if media is None:
        return e, "calendario"
    if e in ("primavera", "otono"):
        if media < 12.0:
            return "invierno", "clima (media %.1f C)" % media
        if media > 26.0:
            return "verano", "clima (media %.1f C)" % media
    return e, "calendario"


def norm_estaciones(txt):
    """Normaliza el campo sucio: 'Primavera/Verano/Otoño', 'otoño, invierno',
    'otono,invierno', 'otoño-invierno' -> lista de estaciones."""
    if not txt:
        return []
    s = unicodedata.normalize("NFKD", txt).encode("ascii", "ignore").decode().lower()
    s = s.replace("/", ",").replace("-", ",").replace(" y ", ",")
    out = []
    for x in re.split(r"[,\s]+", s):
        x = x.strip()
        if x in ("primavera", "verano", "otono", "invierno") and x not in out:
            out.append(x)
    return out


def compat(ests, efectiva):
    """2 = incluye la estacion del dia, 1 = misma mitad del anio,
    0 = solo la mitad opuesta (BLOQUEADO), None = sin dato."""
    if not ests:
        return None
    if efectiva in ests:
        return 2
    m = MITAD[efectiva]
    if any(MITAD[e] == m for e in ests):
        return 1
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fecha", required=True)
    ap.add_argument("--media", type=float, default=None,
                    help="media del pronostico del dia de uso (C)")
    ap.add_argument("--dias-exclusion", type=int, default=60)
    ap.add_argument("--incluir-fuera", action="store_true",
                    help="listar tambien los bloqueados por temporada")
    ap.add_argument("--json", default=None)
    a = ap.parse_args()

    fecha = datetime.date.fromisoformat(a.fecha)
    efectiva, origen = estacion_efectiva(fecha, a.media)

    con = sqlite3.connect("file:%s?mode=ro" % DB, uri=True)
    con.row_factory = sqlite3.Row
    perf = list(con.execute(
        "SELECT p.id, p.nombre, p.temporada, p.posee, c.nombre AS casa "
        "FROM perfumes p LEFT JOIN casas c ON c.id = p.casa_id"))
    rt = {r["perfume_id"]: dict(r) for r in con.execute(
        "SELECT perfume_id, indice, banda FROM rango_termico")}
    ultimo = {r["perfume_id"]: r["f"] for r in con.execute(
        "SELECT perfume_id, MAX(fecha) f FROM uso_diario GROUP BY perfume_id")}
    decant = {r["perfume_id"]: r["estado"] for r in con.execute(
        "SELECT perfume_id, estado FROM decants")}
    con.close()

    # fichas generadas en disco (exclusion aunque no haya fila en uso_diario):
    # el nombre del PNG final es perfume_del_dia_v5_<slug>.png; se mapea por slug
    def slug(s):
        s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
        return re.sub(r"[^a-z0-9]+", "_", s).strip("_")

    disco = {}  # slug del perfume -> fecha de la ficha mas reciente
    for d in FICHAS.glob("perfume-del-dia-*"):
        try:
            fd = datetime.date(int(d.name[-8:-4]), int(d.name[-4:-2]), int(d.name[-2:]))
        except ValueError:
            continue
        if (fecha - fd).days >= a.dias_exclusion:
            continue
        for png in d.glob("perfume_del_dia_v5_*.png"):
            sp = png.stem.replace("perfume_del_dia_v5_", "", 1)
            disco[sp] = max(fd, disco.get(sp, fd))

    eleg, fuera, sin_dato, excl = [], [], [], []
    for p in perf:
        ests = norm_estaciones(p["temporada"])
        c = compat(ests, efectiva)
        item = {
            "id": p["id"], "nombre": p["nombre"], "casa": p["casa"],
            "temporada": p["temporada"], "estaciones_norm": ests,
            "compat": c, "posee": p["posee"],
            "banda": (rt.get(p["id"]) or {}).get("banda"),
            "indice": (rt.get(p["id"]) or {}).get("indice"),
            "ultimo_uso": ultimo.get(p["id"]), "decant": decant.get(p["id"]),
        }
        if item["ultimo_uso"]:
            du = (fecha - datetime.date.fromisoformat(item["ultimo_uso"][:10])).days
            item["dias_desde_uso"] = du
        else:
            item["dias_desde_uso"] = None
        # cruce con fichas en disco (el SQL solo no las ve: caso Akdeniz 24-sep)
        df = disco.get(slug(p["nombre"]))
        if df:
            dd = (fecha - df).days
            item["ficha_en_disco"] = df.isoformat()
            item["dias_desde_uso"] = dd if item["dias_desde_uso"] is None else min(item["dias_desde_uso"], dd)
        if c is None:
            sin_dato.append(item)
        elif c == 0:
            fuera.append(item)
        elif (item["dias_desde_uso"] is None or item["dias_desde_uso"] >= a.dias_exclusion):
            eleg.append(item)
        else:
            excl.append(item)

    eleg.sort(key=lambda x: (-x["compat"], x["dias_desde_uso"] if x["dias_desde_uso"]
                             is not None else 9999, x["nombre"]))
    fuera.sort(key=lambda x: x["nombre"])

    print("FECHA %s | estacion efectiva: %s (%s)" % (fecha, efectiva, origen))
    print("ELEGIBLES %d | bloqueados por temporada %d | en exclusion %d | sin temporada %d"
          % (len(eleg), len(fuera), len(excl), len(sin_dato)))
    if not eleg:
        print("AVISO: pool vacio -> revisar exclusion o ampliar temporada a mano")
    print("\n-- top 12 elegibles (compat 2=misma estacion, 1=adyacente):")
    for p in eleg[:12]:
        print("  %d %-30s %-14s compat=%s banda=%-6s sin_usar=%s decant=%s"
              % (p["compat"], p["nombre"][:30], (p["casa"] or "")[:14],
                 p["compat"], p["banda"], p["dias_desde_uso"], p["decant"]))
    if a.incluir_fuera:
        print("\n-- BLOQUEADOS por temporada (%d):" % len(fuera))
        for p in fuera:
            print("  %-34s declarada=%-24s" % (p["nombre"][:34], str(p["temporada"])[:24]))
    if sin_dato:
        print("\n-- sin temporada declarada (%d): %s"
              % (len(sin_dato), ", ".join(p["nombre"] for p in sin_dato)))
    if a.json:
        Path(a.json).write_text(json.dumps({
            "fecha": a.fecha, "estacion_efectiva": efectiva, "origen": origen,
            "media": a.media, "elegibles": eleg, "bloqueados_temporada": fuera,
            "excluidos_por_uso": excl, "sin_temporada": sin_dato},
            ensure_ascii=False, indent=1), encoding="utf-8")
        print("\nJSON -> %s" % a.json)
    return 0


raise SystemExit(main())
