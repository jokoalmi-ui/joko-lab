#!/usr/bin/env python3
"""F1 / Fase F1.3 — CONTRASTE con el ledger real (pipeline_obs.jsonl). SOLO LECTURA.

Objetivo: sacar el suelo REAL del prompt del pipeline cloud (tokenizador DeepSeek) y los
percentiles por modelo, para contrastar el orden de magnitud de F1.2.

Filtros obligatorios (skill validacion-instrumentos-medicion):
  status==200 · path != /api/show · model no nulo · prompt_tokens presente
  dedup de (timestamp, prompt_tokens, completion_tokens)

Estrategia de lectura: streaming linea a linea (el fichero son 9,2 MB / 33.247 lineas;
NO se carga entero ni se vuelca al contexto).

Salida: /tmp/f1-contexto/ledger_baseline.json
Uso:  python3 leer_ledger.py [--ruta PATH] [--dia YYYY-MM-DD]
"""
import json
import os
import sys

RUTA = "/home/jokoalmi/joko-lab/04-operations/metrics/pipeline_obs.jsonl"
SAL = "/tmp/f1-contexto/ledger_baseline.json"


def main():
    argv = sys.argv[1:]
    ruta, dia = RUTA, None
    for i, a in enumerate(argv):
        if a == "--ruta" and i + 1 < len(argv):
            ruta = argv[i + 1]
        if a == "--dia" and i + 1 < len(argv):
            dia = argv[i + 1]

    if not os.path.exists(ruta):
        raise SystemExit(f"ERROR: no existe {ruta}")

    total = saltadas = 0
    vistos = set()
    filas = []          # (timestamp, modelo, prompt_tokens, completion_tokens)
    with open(ruta, "r", encoding="utf-8", errors="replace") as f:
        for ln in f:
            total += 1
            if '"prompt_tokens": null' in ln or '"status": 200' not in ln:
                saltadas += 1
                continue
            try:
                r = json.loads(ln)
            except ValueError:
                saltadas += 1
                continue
            pt, m = r.get("prompt_tokens"), r.get("model")
            if r.get("status") != 200 or not pt or m in (None, "") or r.get("path") == "/api/show":
                saltadas += 1
                continue
            clave = (r.get("timestamp"), pt, r.get("completion_tokens"))
            if clave in vistos:
                saltadas += 1
                continue
            vistos.add(clave)
            ts = str(r.get("timestamp") or "")
            if dia and not ts.startswith(dia):
                continue
            filas.append((ts, m, int(pt), r.get("completion_tokens")))

    filas.sort()
    out = {"ruta": ruta, "lineas_totales": total, "lineas_descartadas": saltadas,
           "llamadas_limpias": len(filas), "filtro_dia": dia}

    if not filas:
        out["resultado"] = "no_calculable: 0 llamadas limpias con el filtro dado"
    else:
        por_modelo = {}
        for ts, m, pt, ct in filas:
            por_modelo.setdefault(m, []).append(pt)
        out["por_modelo"] = {}
        for m, v in por_modelo.items():
            v.sort()
            n = len(v)
            out["por_modelo"][m] = {
                "n": n, "min": v[0], "p10": v[max(0, int(n * 0.10) - 1)],
                "mediana": v[n // 2], "p90": v[max(0, int(n * 0.90) - 1)], "max": v[-1]}
        # SONDAS vs arranques: un prompt de ~85 tokens NO es una sesion del agente, es un
        # sondeo del proxy. El suelo real de una sesion nueva se busca POR ENCIMA de ese ruido.
        SUELO_SONDA = 1000
        sondas = sorted((f for f in filas if f[2] < SUELO_SONDA), key=lambda x: x[2])
        dom = max(por_modelo, key=lambda k: len(por_modelo[k]))
        peq = sorted((f for f in filas if f[1] == dom and f[2] >= SUELO_SONDA),
                     key=lambda x: x[2])[:15]
        out["modelo_dominante"] = dom
        out["sondas_menores_de_1000_tok"] = {
            "n": len(sondas), "min": sondas[0][2] if sondas else None,
            "nota": ("NO son arranques de sesion: son sondeos del proxy. Contarlos como "
                     "'contexto fijo' seria un falso suelo (el 85 que aparece en el ledger)")}
        out["candidatas_arranque_sesion"] = [
            {"timestamp": t, "prompt_tokens": p, "completion_tokens": c} for t, _m, p, c in peq]
        out["lectura"] = (f"El suelo del prompt de una sesion NUEVA es el menor prompt NO-sonda "
                          f"(>= {SUELO_SONDA} tok), no el minimo absoluto. Las consultas siguientes crecen "
                          "por acumulacion de conversacion. Tokenizador DeepSeek, distinto al local "
                          "-> comparar ORDEN DE MAGNITUD, nunca igualdad.")

    with open(SAL, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    print(f"lineas totales: {total} · descartadas: {saltadas} · limpias: {len(filas)}")
    for m, d in (out.get("por_modelo") or {}).items():
        print(f"  {m:22s} n={d['n']:6d}  min={d['min']:7d}  p10={d['p10']:7d}  "
              f"mediana={d['mediana']:7d}  p90={d['p90']:7d}  max={d['max']:8d}")
    if out.get("candidatas_arranque_sesion"):
        print(f"  modelo dominante {out['modelo_dominante']} — 5 prompts mas pequenos:")
        for c in out["candidatas_arranque_sesion"][:5]:
            print(f"    {c['timestamp']}  prompt={c['prompt_tokens']}  out={c['completion_tokens']}")
    print(f"escrito: {SAL}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
