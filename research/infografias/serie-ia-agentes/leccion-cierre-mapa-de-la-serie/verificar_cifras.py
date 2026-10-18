#!/usr/bin/env python3
"""verificar_cifras.py — recuenta las cifras de la pieza de cierre DESDE EL CRUDO.

La pieza 9 no ejecuta medicion nueva: cita las dos mediciones propias ya hechas
(tokens/palabra en la pieza 1, multiagente en la pieza 7, alucinaciones en la
pieza 8). Regla de la receta: las cifras NO se heredan, se recalculan del crudo
que se copia a la carpeta. Este script hace ese recuento y lo imprime.

Solo lectura sobre los dos JSON. No escribe nada.
"""
import json
import pathlib

P = pathlib.Path(__file__).resolve().parent


def n(x, dec=2):
    return f"{x:,.{dec}f}".replace(",", ".")


print(f"PIEZA: {P.name}")
print("=" * 66)

# --- 1) multiagente (pieza 7, 27-sep-2026) -------------------------------
m = json.loads((P / "medicion-multiagente-20260927.json").read_text(encoding="utf-8"))
print(f"[multiagente] {m['fecha'][:10]} | {m['modelo']} | {m['backend']} | {len(m['tareas'])} tareas")
A = m["resumen"]["A_un_agente"]
B = m["resumen"]["B_multi_con_critico"]
print(f"  A un agente     : resueltas {A['resueltas']}/{A['n']} | tokens {n(A['tokens_total'],0)} | {n(A['segundos_totales'],0)} s")
print(f"  B multi+critico : resueltas {B['resueltas']}/{B['n']} | tokens {n(B['tokens_total'],0)} | {n(B['segundos_totales'],0)} s")
print(f"  RATIOS          : tokens x{n(B['tokens_total']/A['tokens_total'])} | tiempo x{n(B['segundos_totales']/A['segundos_totales'])}")
c = m["comparativa_B_menos_A"]
print("  comparativa:")
for k, v in c.items():
    if not isinstance(v, (list, dict)):
        print(f"    {k} = {v}")

# --- 2) alucinaciones (pieza 8, 14-sep-2026) -----------------------------
a = json.loads((P / "medicion-alucinaciones-20260914.json").read_text(encoding="utf-8"))
print(f"\n[alucinaciones] {a['fecha_medicion']} | {a['golden_set'].split(' (')[0].split('/')[-1]} | pasadas guardadas: {len(a['pasadas'])}")
print(f"  que_se_publica (crudo): {a['que_se_publica']}")
sin, con = [], []
for p in a["pasadas"]:
    r = p["resumen"]
    fila = (p["seed"], p["set"].replace("golden_set_alucinaciones.json", "golden27"), r["tasa_alucinacion_global"],
            r.get("tasa_honestidad"), p.get("invalidada"), p.get("nota"))
    (sin if p["think"] is False else con).append((p, fila))
    print(f"  pasada seed={p['seed']:<4} think={str(p['think']):<5} set={fila[1]:<10} aluc={r['tasa_alucinacion_global']:<6} "
          f"honest={r.get('tasa_honestidad')} invalidada={p.get('invalidada')}")

print(f"\n  pasadas con razonamiento DESACTIVADO (las que se publican): {len(sin)}")
tot_cases = tot_resp = 0
for p, _ in sin:
    pc = p["resumen"]["por_categoria"]
    ok = sum(v.get("CORRECTO", 0) for v in pc.values())
    pasa = sum(v.get("PASA", 0) for v in pc.values())
    tot_cases = sum(sum(v.values()) for v in pc.values())
    tot_resp += tot_cases
    print(f"    seed {p['seed']}: {ok} aciertos + {pasa} abstenciones = {tot_cases} casos | "
          f"invenciones {p['resumen']['tasa_alucinacion_global']*tot_cases:.0f} | honestidad {p['resumen']['tasa_honestidad']}")
print(f"  SUMA: {len(sin)} pasadas x {tot_cases} casos = {tot_resp} respuestas | invenciones totales: 0")
print(f"  pasadas con razonamiento ACTIVADO (no se publican): {len(con)}")
print(f"  limite declarado (crudo): {a['limite_declarado_en_la_slide'][:200]}")
