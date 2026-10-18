#!/usr/bin/env python3
"""RSI v0 — bucle de auto-mejora MEDIDO sobre la batería JSON/tool-calling del lab.

Tesis que se pone a prueba (Darwin Gödel Machine / GEPA): en un bucle de
auto-mejora el cuello de botella es el VERIFICADOR, no el proponente.

Reglas de diseño de este experimento (anti-gaming, 25-sep-2026):
  1. El EXAMEN no se toca: se lee tools/bateria_json_tool_calling.json y se
     verifica su sha256 contra el registrado. Si cambia, ABORTA.
  2. El CORRECTOR no se toca: se importa tools/evaluar_json_tool_calling.py y se
     usan SUS validadores (validar_json / validar_tool) y SU función de llamada
     (llamar_ollama) tal cual, con los mismos parámetros de la corrida de
     referencia (temp 0.0, seed 42, num_ctx 8192, think=False). Hash verificado.
  3. El ARTEFACTO que evoluciona es SOLO la instrucción que se antepone al
     prompt congelado. Nada más cambia.
  4. Sin fuga de respuestas: las instrucciones candidatas no contienen ninguno
     de los valores esperados del examen (se comprueba en código).
  5. ARCHIVO: toda variante se escribe en el .jsonl (nada se descarta), con sus
     métricas. Pareto por (pasan, segundos).
  6. RONDA 3 (25-sep): el MODO DE INFERENCIA es parámetro POR VARIANTE. Una
     variante puede traer "think": false | true | "low" | "medium" | "high"; si
     no lo trae, se usa el global (--think). Nada más del examen cambia.

Uso:
  python3 research/rsi-v0/rsi_v0_json.py --tag r1 --variantes research/rsi-v0/variantes_r1.json
"""
import argparse
import hashlib
import importlib.util
import json
import os
import sys
import time
import urllib.error

BASE = "/home/jokoalmi/joko-lab"
RUTA_INSTRUMENTO = os.path.join(BASE, "tools", "evaluar_json_tool_calling.py")
RUTA_BATERIA = os.path.join(BASE, "tools", "bateria_json_tool_calling.json")

SHA_INSTRUMENTO = "849c12fe093420bae89971566e190653c5ca50d3322b7e404e144d9f012e6121"
SHA_BATERIA = "30557a9df6ee2fca82f3a823ed8e5dea20baa56ebc21d00c7b6f51f011493080"

MODELO = "ibm/granite4.2:8b-q4_K_M"
HOST = "http://localhost:11434"
NUM_CTX = 8192


def sha256(ruta):
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()


def cargar_instrumento():
    spec = importlib.util.spec_from_file_location("instrumento_jtc", RUTA_INSTRUMENTO)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def valores_esperados(bateria):
    """Todos los valores que el examen espera, para prohibir fugas en las candidatas."""
    vals = set()
    for c in bateria["casos"]:
        comp = c.get("comprueba", {})
        for k, v in (comp.get("iguales") or {}).items():
            vals.add(str(v))
        for k, v in (comp.get("args_iguales") or {}).items():
            vals.add(str(v))
        for k, v in (comp.get("args_contiene") or {}).items():
            vals.add(str(v))
        for k, regla in (comp.get("valor_en") or {}).items():
            if isinstance(regla, dict):
                e = regla.get("esperado")
                if e:
                    vals.add(str(e))
    return {v for v in vals if len(v) >= 3}  # los cortos (23.0) no son filtrables de forma útil


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", required=True)
    ap.add_argument("--variantes", required=True, help="JSON con [{id, instr, origen}]")
    ap.add_argument("--outdir", default=os.path.join(BASE, "research", "rsi-v0"))
    ap.add_argument("--solo-casos", default="", help="ids separados por coma (opcional)")
    ap.add_argument("--think", action="store_true",
                    help="Ollama: activar razonamiento (think=None). Por defecto se desactiva (think=false). "
                         "Una variante puede sobreescribirlo con su clave \"think\" (low/medium/high).")
    args = ap.parse_args()
    think_val = None if args.think else False

    # --- Verificación de integridad: examen y corrector congelados ---
    s_i, s_b = sha256(RUTA_INSTRUMENTO), sha256(RUTA_BATERIA)
    print(f"[integridad] corrector {s_i[:16]}…  examen {s_b[:16]}…", flush=True)
    if s_i != SHA_INSTRUMENTO or s_b != SHA_BATERIA:
        print("[ABORT] El instrumento o el examen han CAMBIADO respecto al hash registrado.")
        print(f"  esperado corrector {SHA_INSTRUMENTO}\n  obtenido          {s_i}")
        print(f"  esperado examen   {SHA_BATERIA}\n  obtenido          {s_b}")
        return 3

    mod = cargar_instrumento()
    bateria = json.load(open(RUTA_BATERIA, encoding="utf-8"))
    variantes = json.load(open(args.variantes, encoding="utf-8"))
    casos = bateria["casos"]
    if args.solo_casos:
        ids = {x.strip() for x in args.solo_casos.split(",")}
        casos = [c for c in casos if c["id"] in ids]

    # --- Control de fugas: ninguna candidata puede citar valores esperados ---
    esperados = valores_esperados(bateria)
    for v in variantes:
        instr = v.get("instr") or ""
        fugas = sorted(e for e in esperados if e.lower() in instr.lower())
        if fugas:
            print(f"[ABORT] La variante {v['id']} filtra valores esperados del examen: {fugas}")
            return 4
    print(f"[fugas] {len(variantes)} variantes, 0 valores esperados del examen citados", flush=True)

    os.makedirs(args.outdir, exist_ok=True)
    ruta_jsonl = os.path.join(args.outdir, f"variantes_{args.tag}.jsonl")

    t0 = time.time()
    for v in variantes:
        instr = v.get("instr") or ""
        for caso in casos:
            prompt = (instr + "\n\n" + caso["prompt"]) if instr else caso["prompt"]
            tv = v.get("think", think_val)  # ronda 3: nivel de razonamiento por variante
            try:
                resp, dt = mod.llamar_ollama(MODELO, prompt, caso.get("herramientas"),
                                             HOST, num_ctx=NUM_CTX, think=tv)
                error = None
            except urllib.error.URLError as e:
                resp, dt, error = None, 0.0, f"URLError: {e}"
            except Exception as e:  # noqa: BLE001
                resp, dt, error = None, 0.0, f"{type(e).__name__}: {e}"

            if resp is None:
                fila = {"variante": v["id"], "caso": caso["id"], "tipo": caso["tipo"],
                        "pasa": False, "fallos": [f"ERROR {error}"], "segundos": dt,
                        "respuesta": "", "error": error}
            else:
                texto, tcs = mod.extraer_texto(resp, "ollama")
                fallos = (mod.validar_tool(caso, tcs) if caso["tipo"] == "tool_calling"
                          else mod.validar_json(caso, texto))
                fila = {"variante": v["id"], "caso": caso["id"], "tipo": caso["tipo"],
                        "pasa": not fallos, "fallos": fallos, "segundos": round(dt, 2),
                        "respuesta": (texto or json.dumps(tcs, ensure_ascii=False))[:400],
                        "error": None}
            fila.update({"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "modelo": MODELO,
                         "num_ctx": NUM_CTX, "think": tv, "temperature": 0.0, "seed": 42,
                         "instr_len": len(instr), "origen_instr": v.get("origen", "")})
            with open(ruta_jsonl, "a", encoding="utf-8") as f:
                f.write(json.dumps(fila, ensure_ascii=False) + "\n")
            marca = "PASA " if fila["pasa"] else "FALLA"
            print(f"[{marca}] {v['id']:<14} {caso['id']:<18} {fila['segundos']:>6.1f}s "
                  f"{'' if fila['pasa'] else '| ' + '; '.join(fila['fallos'])[:110]}", flush=True)

    # --- Resumen + Pareto (todas las variantes, nada se descarta) ---
    filas = [json.loads(l) for l in open(ruta_jsonl, encoding="utf-8")]
    resumen = {}
    for v in variantes:
        fs = [f for f in filas if f["variante"] == v["id"]]
        resumen[v["id"]] = {
            "pasan": sum(1 for f in fs if f["pasa"]), "total": len(fs),
            "segundos": round(sum(f["segundos"] for f in fs), 1),
            "instr_len": len(v.get("instr") or ""), "origen": v.get("origen", ""),
            "think": v.get("think", think_val),
            "casos_fallados": [f["caso"] for f in fs if not f["pasa"]],
        }
    pareto = []
    for vid, r in sorted(resumen.items(), key=lambda kv: (-kv[1]["pasan"], kv[1]["segundos"])):
        dominado = any(o["pasan"] >= r["pasan"] and o["segundos"] <= r["segundos"]
                       and (o["pasan"] > r["pasan"] or o["segundos"] < r["segundos"])
                       for oid, o in resumen.items() if oid != vid)
        pareto.append({"variante": vid, "pasan": r["pasan"], "segundos": r["segundos"],
                       "dominada": dominado, "casos_fallados": r["casos_fallados"]})
    out = {"tag": args.tag, "modelo": MODELO, "num_ctx": NUM_CTX, "think": think_val,
           "temperature": 0.0, "seed": 42, "sha_corrector": s_i, "sha_examen": s_b,
           "casos": [c["id"] for c in casos], "segundos_totales": round(time.time() - t0, 1),
           "resumen": resumen, "pareto": pareto, "jsonl": ruta_jsonl}
    ruta_res = os.path.join(args.outdir, f"resumen_{args.tag}.json")
    json.dump(out, open(ruta_res, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("\n== RESUMEN (pasan/total) ==", flush=True)
    for r in pareto:
        print(f"  {r['variante']:<14} {r['pasan']}/{resumen[r['variante']]['total']} "
              f"{r['segundos']:>6.1f}s  dominada={r['dominada']}  "
              f"falla={','.join(r['casos_fallados']) or '-'}", flush=True)
    print(f"\nresumen -> {ruta_res}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
