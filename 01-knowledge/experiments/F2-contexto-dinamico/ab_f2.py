#!/usr/bin/env python3
"""F2.3 - instrumento del A/B de la palanca de contexto.

Solo lectura. Compara una VENTANA de intervencion contra la linea base congelada y,
sobre todo, mide la VARIABILIDAD NATURAL del dia a dia: el umbral de decision sale de esa
banda observada, nunca de un numero elegido antes de ver los datos (RULE-015).

Uso:
  python3 ab_f2.py                 # tabla diaria (28 d) + banda natural + estado del A/B
  python3 ab_f2.py --desde 2026-09-26T19:30        # anade el tramo de intervencion
  python3 ab_f2.py --desde ... --hasta 2026-10-03  # cierra la ventana
  python3 ab_f2.py --json          # salida JSON para archivar
"""
import argparse
import collections
import datetime as dt
import json
import statistics

LEDGER = "/home/jokoalmi/joko-lab/04-operations/metrics/pipeline_obs.jsonl"
UMBRAL = 1000          # filas del proxy por debajo de esto son sondas, no contexto real
VENTANA_131K = 131072  # ventana de un modelo de 128k: por encima, el contexto no cabe


def carga():
    filas = []
    with open(LEDGER, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            pt = r.get("prompt_tokens")
            if r.get("path") != "/v1/chat/completions" or not isinstance(pt, int) or pt < UMBRAL:
                continue
            try:
                d = dt.datetime.fromisoformat(str(r["timestamp"]).replace("Z", "+00:00"))
            except Exception:
                continue
            filas.append({"t": d, "pt": pt,
                          "hit": r.get("prompt_cache_hit_tokens"),
                          "miss": r.get("prompt_cache_miss_tokens")})
    return filas


def stats(filas):
    v = sorted(f["pt"] for f in filas)
    n = len(v)
    if not n:
        return None
    p = lambda q: v[min(n - 1, max(0, int(n * q) - 1 if q < 1 else n - 1))]
    c = [f for f in filas if isinstance(f["hit"], int) and isinstance(f["miss"], int) and f["hit"] + f["miss"] > 0]
    hit = 100 * sum(f["hit"] for f in c) / sum(f["hit"] + f["miss"] for f in c) if c else None
    return {"n": n, "min": v[0], "p25": p(.25), "p50": statistics.median(v), "p75": p(.75),
            "p90": p(.90), "max": v[-1], "media": statistics.mean(v),
            "pct_131k": 100 * sum(1 for x in v if x > VENTANA_131K) / n,
            "pct_200k": 100 * sum(1 for x in v if x > 200000) / n,
            "cache_hit_pct": hit}


def linea(s, etiqueta):
    if not s:
        return f"  {etiqueta:26s} sin filas"
    h = f"{s['cache_hit_pct']:5.1f}%" if s["cache_hit_pct"] is not None else "   n/d"
    return (f"  {etiqueta:26s} n={s['n']:5d} p50={s['p50']:8.0f} p90={s['p90']:8.0f} "
            f"max={s['max']:8d} >131k={s['pct_131k']:5.1f}% >200k={s['pct_200k']:4.1f}% cache={h}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--desde")
    ap.add_argument("--hasta")
    ap.add_argument("--dias", type=int, default=28)
    ap.add_argument("--banda-dias", type=int, default=14,
                    help="dias del REGIMEN ACTUAL sobre los que medir la banda natural "
                         "(incluir la transicion de regimen la contamina: ver F2.3-protocolo.md)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    filas = carga()
    hoy = max(f["t"] for f in filas)
    base_desde = hoy - dt.timedelta(days=a.dias)
    por_dia = collections.defaultdict(list)
    for f in filas:
        por_dia[f["t"].date()].append(f)

    dias = [d for d in sorted(por_dia) if d >= base_desde.date()]
    tabla = [(str(d), stats(por_dia[d])) for d in dias]
    # banda natural: solo dias del REGIMEN ACTUAL con volumen suficiente para que la
    # mediana sea comparable. Meter la transicion de regimen (31-ago..4-sep) dispara la
    # amplitud a >200% y deja la banda inservible.
    corte = (hoy - dt.timedelta(days=a.banda_dias)).date()
    solidos = [(f, s) for f, s in tabla if s["n"] >= 300 and dt.date.fromisoformat(f) >= corte]
    banda = None
    if len(solidos) >= 4:
        p50s = sorted(s["p50"] for _, s in solidos)
        p90s = sorted(s["p90"] for _, s in solidos)
        ses = sorted(s["pct_200k"] for _, s in solidos)
        banda = {"dias": [f for f, _ in solidos], "n_dias": len(solidos),
                 "p50_min": p50s[0], "p50_max": p50s[-1],
                 "p90_min": p90s[0], "p90_max": p90s[-1],
                 "pct200k_max": ses[-1],
                 "p50_sd": statistics.pstdev([s["p50"] for _, s in solidos]),
                 "variacion_p50_pct": 100 * (p50s[-1] - p50s[0]) / statistics.median(p50s),
                 "variacion_p90_pct": 100 * (p90s[-1] - p90s[0]) / statistics.median(p90s)}
    base7 = [f for f in filas if f["t"] >= hoy - dt.timedelta(days=7)]
    out = {"generado": dt.datetime.now().isoformat(timespec="seconds"),
           "ledger": LEDGER, "filas_utiles": len(filas),
           "rango": [min(f["t"] for f in filas).isoformat(timespec="seconds"),
                     hoy.isoformat(timespec="seconds")],
           "base_7d": stats(base7), "banda_natural": banda,
           "por_dia": {f: s for f, s in tabla}}

    if a.desde:
        ini = dt.datetime.fromisoformat(a.desde)
        fin = dt.datetime.fromisoformat(a.hasta) if a.hasta else None
        vent = [f for f in filas if f["t"] >= ini and (fin is None or f["t"] <= fin)]
        prev = [f for f in filas if ini - dt.timedelta(days=7) <= f["t"] < ini]
        prev = [f for f in prev if f["t"] >= base_desde]
        out["intervencion"] = {"desde": ini.isoformat(timespec="seconds"),
                               "hasta": fin.isoformat(timespec="seconds") if fin else "abierta",
                               "ventana": stats(vent), "7d_previos": stats(prev)}

    if a.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return

    print(f"ledger: {len(filas)} filas utiles | rango {out['rango'][0][:10]} -> {out['rango'][1][:10]}")
    print(f"\n=== por dia (ultimos {a.dias}) ===")
    for f, s in tabla:
        print(linea(s, f))
    print("\n=== linea base congelada (ultimos 7 dias) ===")
    print(linea(out["base_7d"], "7 dias"))
    if banda:
        b = banda
        print(f"\n=== variabilidad NATURAL del dia a dia ({b['n_dias']} dias con n>=300) ===")
        print(f"  p50 diario: {b['p50_min']:.0f} .. {b['p50_max']:.0f} tok (sd {b['p50_sd']:.0f}, "
              f"amplitud {b['variacion_p50_pct']:.1f}%)")
        print(f"  p90 diario: {b['p90_min']:.0f} .. {b['p90_max']:.0f} tok (amplitud {b['variacion_p90_pct']:.1f}%)")
        print(f"  % >200k: maximo diario observado {b['pct200k_max']:.1f}%")
        print("  -> el umbral de decision sale de esta banda, no de un numero a priori")
    if "intervencion" in out:
        i = out["intervencion"]
        print(f"\n=== A/B ===\n  ventana {i['desde'][:16]} -> {i['hasta'][:16] if i['hasta'] != 'abierta' else 'abierta'}")
        print(linea(i["7d_previos"], "7d previos"))
        print(linea(i["ventana"], "ventana"))


if __name__ == "__main__":
    main()
