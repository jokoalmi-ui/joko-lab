#!/usr/bin/env python3
"""RSI v0 — arnés v2 (batería v2 / corrector v2). Fichero NUEVO; el v1 no se toca.

Cambios respecto al arnés v1 (`rsi_v0_json.py`), todos por los hallazgos del 25-sep:
  1. Usa el CORRECTOR v2 (`tools/evaluar_json_tool_calling_v2.py`), que puntúa
     varias llamadas, la ausencia correcta de llamadas, y TRANSMITE `think` tal
     cual (el v1 solo enviaba `False`).
  2. GUARDIA ANTI-ERRATUM: si dos variantes piden niveles de `think` distintos y
     el payload resultante sería el mismo, ABORTA. Así no se puede volver a
     medir «niveles» que nunca salieron de la máquina.
  3. Registra por llamada `thinking_chars`, `n_tool_calls` y `nombres`: el
     discriminador de razonamiento y el de tool-calling, sin inferencias.
  4. El banco v2 es una PROPUESTA hasta que el usuario lo apruebe: si no se pasa
     `--bateria`, exige `--propuesta-ok` explícito.

Uso:
  python3 research/rsi-v0/rsi_v0_json_v2.py --tag s1 --bateria <banco.json> \
      --variantes <variantes.json> [--solo-casos id1,id2] [--think-level omit|false|high]
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
RUTA_CORRECTOR = os.path.join(BASE, "tools", "evaluar_json_tool_calling_v2.py")
PROPUESTA = os.path.join(BASE, "research", "rsi-v0", "propuesta-examen-v2.json")

MODELO = "ibm/granite4.2:8b-q4_K_M"
HOST = "http://localhost:11434"
NUM_CTX = 8192


def sha256(ruta):
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()


def cargar_corrector():
    spec = importlib.util.spec_from_file_location("corrector_v2", RUTA_CORRECTOR)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def valores_esperados(bateria):
    """Valores que el examen espera, para prohibir fugas en las candidatas."""
    vals = set()
    for c in bateria["casos"]:
        comp = c.get("comprueba", {})
        for clave in ("iguales", "args_iguales", "args_contiene"):
            for _, v in (comp.get(clave) or {}).items():
                vals.add(str(v))
        for _, regla in (comp.get("valor_en") or {}).items():
            if isinstance(regla, dict) and regla.get("esperado"):
                vals.add(str(regla["esperado"]))
    return {v for v in vals if len(v) >= 3}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", required=True)
    ap.add_argument("--variantes", required=True, help="JSON con [{id, instr, origen, think?}]")
    ap.add_argument("--bateria", default="", help="banco de casos; vacío = propuesta (exige --propuesta-ok)")
    ap.add_argument("--propuesta-ok", action="store_true",
                    help="confirma que se corre la propuesta de examen todavía NO aprobada")
    ap.add_argument("--outdir", default=os.path.join(BASE, "research", "rsi-v0"))
    ap.add_argument("--solo-casos", default="")
    ap.add_argument("--think-level", default="omit",
                    choices=["omit", "false", "true", "low", "medium", "high"],
                    help="nivel por defecto si la variante no trae 'think'")
    ap.add_argument("--timeout", type=float, default=180.0,
                    help="segundos por llamada antes de abortarla (los casos duros razonan >180 s)")
    ap.add_argument("--continuar", action="store_true",
                    help="añadir al jsonl del tag existente en vez de abortar")
    args = ap.parse_args()

    if not args.bateria:
        if not args.propuesta_ok:
            print("[ABORT] El banco v2 sigue siendo una PROPUESTA sin aprobar "
                  f"({PROPUESTA}). Añade --propuesta-ok para correrla, o pasa --bateria.")
            return 5
        args.bateria = PROPUESTA

    mod = cargar_corrector()
    s_c, s_b = sha256(RUTA_CORRECTOR), sha256(args.bateria)
    print(f"[integridad] corrector v2 {s_c[:16]}…  banco {s_b[:16]}…", flush=True)

    bateria = json.load(open(args.bateria, encoding="utf-8"))
    variantes = json.load(open(args.variantes, encoding="utf-8"))
    casos = bateria["casos"]
    if args.solo_casos:
        ids = {x.strip() for x in args.solo_casos.split(",")}
        casos = [c for c in casos if c["id"] in ids]

    # --- GUARDIA ANTI-ERRATUM: niveles distintos deben producir payloads distintos ---
    nivel_default = mod.NIVELES[args.think_level]
    print("[guardia] payload 'think' por variante:", flush=True)
    for v in variantes:
        tv = v.get("think", nivel_default)
        print(f"    {v['id']:<16} think={v.get('think', args.think_level)!r:<10} -> payload {mod.payload_think(tv)!r}",
              flush=True)
    niveles_distintos = {mod.payload_think(v.get("think", nivel_default)) for v in variantes}
    pedidos = {v.get("think", args.think_level) for v in variantes}
    if len(pedidos) > 1 and len(niveles_distintos) == 1:
        print("[ABORT] Variantes con niveles DISTINTOS pero MISMO payload de 'think': "
              "se volvería a medir el mismo caso creyendo que cambia el nivel.")
        return 6

    esperados = valores_esperados(bateria)
    for v in variantes:
        instr = v.get("instr") or ""
        fugas = sorted(e for e in esperados if e.lower() in instr.lower())
        if fugas:
            print(f"[ABORT] La variante {v['id']} filtra valores esperados del examen: {fugas}")
            return 4
    print(f"[fugas] {len(variantes)} variantes, 0 valores esperados citados", flush=True)

    # --- VALIDEZ DE LA RONDA (hallazgo 26-sep): la ronda r9 salió "0/5" porque Ollama se
    # cayó a las 23:27 (host apagado), no porque el modelo fallara: sus 10 llamadas
    # murieron con RemoteDisconnected / ConnectionResetError en ~0,00 s. Un error de
    # transporte NO es un fallo del modelo: si aparece, la ronda se marca INVALIDA.
    TOKENS_INFRA = ("RemoteDisconnected", "ConnectionResetError", "ConnectionRefusedError",
                    "Connection refused", "Connection aborted", "BrokenPipeError",
                    "NewConnectionError", "Max retries exceeded", "URLError",
                    "Name or service not known", "Temporary failure in name resolution")

    def clasificar_error(error):
        """'timeout' (el modelo no acabó a tiempo: es una medida) | 'infra' (no hubo respuesta) | ''."""
        if not error:
            return ""
        bajo = error.lower()
        if "timed out" in bajo or "timeout" in bajo:
            return "timeout"
        return "infra"  # error de conexión o no clasificado: el modelo no llegó a responder

    os.makedirs(args.outdir, exist_ok=True)
    ruta_jsonl = os.path.join(args.outdir, f"variantes_v2_{args.tag}.jsonl")
    if os.path.exists(ruta_jsonl) and os.path.getsize(ruta_jsonl) > 0 and not args.continuar:
        print(f"[ABORT] {ruta_jsonl} ya existe: reutilizar el --tag duplicaría las filas del jsonl. "
              "Usa otro --tag o añade --continuar.")
        return 7

    t0 = time.time()
    for v in variantes:
        instr = v.get("instr") or ""
        tv = v.get("think", nivel_default)
        for caso in casos:
            prompt = (instr + "\n\n" + caso["prompt"]) if instr else caso["prompt"]
            t_ini = time.time()
            try:
                resp, dt = mod.llamar_ollama(MODELO, prompt, caso.get("herramientas"),
                                              HOST, num_ctx=NUM_CTX, think=tv, timeout=args.timeout)
                error = None
            except urllib.error.URLError as e:
                resp, dt, error = None, round(time.time() - t_ini, 2), f"URLError: {e}"
            except Exception as e:  # noqa: BLE001
                resp, dt, error = None, round(time.time() - t_ini, 2), f"{type(e).__name__}: {e}"

            if resp is None:
                fila = {"variante": v["id"], "caso": caso["id"], "tipo": caso["tipo"], "pasa": False,
                        "fallos": [f"ERROR {error}"], "segundos": dt, "respuesta": "",
                        "thinking_chars": 0, "n_tool_calls": 0, "nombres": [], "error": error}
            else:
                texto, tcs, think_txt = mod.extraer(resp, "ollama")
                pares = mod.nombres_args(tcs)
                fallos = mod.puntuar(caso, texto, tcs)
                fila = {"variante": v["id"], "caso": caso["id"], "tipo": caso["tipo"],
                        "pasa": not fallos, "fallos": fallos, "segundos": round(dt, 2),
                        "respuesta": (texto or json.dumps(tcs, ensure_ascii=False))[:400],
                        "thinking_chars": len(think_txt), "n_tool_calls": len(pares),
                        "nombres": [n for n, _ in pares], "error": None}
            fila.update({"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "modelo": MODELO, "num_ctx": NUM_CTX,
                         "think": tv, "think_payload": mod.payload_think(tv),
                         "temperature": 0.0, "seed": 42, "instr_len": len(instr),
                         "origen_instr": v.get("origen", ""), "sha_corrector_v2": s_c, "sha_banco": s_b,
                         "banco": os.path.basename(args.bateria)})
            with open(ruta_jsonl, "a", encoding="utf-8") as f:
                f.write(json.dumps(fila, ensure_ascii=False) + "\n")
            marca = "PASA " if fila["pasa"] else "FALLA"
            print(f"[{marca}] {v['id']:<14} {caso['id']:<20} {fila['segundos']:>6.1f}s think={fila['think_payload']!r:<10} "
                  f"calls={fila['n_tool_calls']} thinking={fila['thinking_chars']}ch"
                  f"{'' if fila['pasa'] else ' | ' + '; '.join(fila['fallos'])[:100]}", flush=True)

    filas = [json.loads(l) for l in open(ruta_jsonl, encoding="utf-8")]
    resumen = {}
    for v in variantes:
        fs = [f for f in filas if f["variante"] == v["id"]]
        clases = {f["caso"]: clasificar_error(f.get("error")) for f in fs}
        casos_infra = [c for c, k in clases.items() if k == "infra"]
        casos_timeout = [c for c, k in clases.items() if k == "timeout"]
        todos_error = bool(fs) and all(f.get("error") for f in fs)
        valida = not casos_infra and not todos_error
        resumen[v["id"]] = {"pasan": sum(1 for f in fs if f["pasa"]), "total": len(fs),
                            "valida": valida, "errores_infra": len(casos_infra),
                            "casos_error_infra": casos_infra, "timeouts": len(casos_timeout),
                            "casos_timeout": casos_timeout, "todo_error": todos_error,
                            "segundos": round(sum(f["segundos"] for f in fs), 1),
                            "segundos_por_llamada": round(sum(f["segundos"] for f in fs) / len(fs), 2) if fs else 0.0,
                            "thinking_chars_medio": round(sum(f["thinking_chars"] for f in fs) / len(fs), 1) if fs else 0.0,
                            "instr_len": len(v.get("instr") or ""), "origen": v.get("origen", ""),
                            "think": v.get("think", args.think_level),
                            "think_payload": mod.payload_think(v.get("think", nivel_default)),
                            "casos_fallados": [f["caso"] for f in fs if not f["pasa"]]}
    pareto = []
    for vid, r in sorted(resumen.items(), key=lambda kv: (-kv[1]["pasan"], kv[1]["segundos"])):
        dominado = any(o["pasan"] >= r["pasan"] and o["segundos"] <= r["segundos"]
                       and (o["pasan"] > r["pasan"] or o["segundos"] < r["segundos"])
                       for oid, o in resumen.items() if oid != vid)
        pareto.append({"variante": vid, "pasan": r["pasan"], "segundos": r["segundos"],
                       "dominada": dominado, "casos_fallados": r["casos_fallados"]})
    rondas_invalidas = [vid for vid, r in resumen.items() if not r["valida"]]
    out = {"tag": args.tag, "arnes": "v2", "corrector": "v2", "modelo": MODELO, "num_ctx": NUM_CTX,
           "ronda_valida": not rondas_invalidas, "rondas_invalidas": rondas_invalidas,
           "temperature": 0.0, "seed": 42, "sha_corrector_v2": s_c, "banco": args.bateria,
           "sha_banco": s_b, "casos": [c["id"] for c in casos],
           "segundos_totales": round(time.time() - t0, 1), "resumen": resumen, "pareto": pareto,
           "jsonl": ruta_jsonl}
    ruta_res = os.path.join(args.outdir, f"resumen_v2_{args.tag}.json")
    json.dump(out, open(ruta_res, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("\n== RESUMEN v2 (pasan/total) ==", flush=True)
    for r in pareto:
        rr = resumen[r["variante"]]
        print(f"  {r['variante']:<14} {r['pasan']}/{rr['total']} {r['segundos']:>6.1f}s "
              f"({rr['segundos_por_llamada']}s/llamada) thinking_medio={rr['thinking_chars_medio']}ch "
              f"payload={rr['think_payload']!r} dominada={r['dominada']} "
              f"falla={','.join(r['casos_fallados']) or '-'}", flush=True)
        print(f"    validez={'VALIDA' if rr['valida'] else 'INVALIDA'} infra={rr['errores_infra']} "
              f"timeout={rr['timeouts']}"
              f"{' casos_infra=' + ','.join(rr['casos_error_infra']) if rr['casos_error_infra'] else ''}"
              f"{' casos_timeout=' + ','.join(rr['casos_timeout']) if rr['casos_timeout'] else ''}",
              flush=True)
    if rondas_invalidas:
        det = "; ".join(
            f"{vid}: " + ("errores de conexion (infra)" if resumen[vid]["errores_infra"]
                          else "todas las llamadas acabaron en error")
            for vid in rondas_invalidas)
        print(f"\n[RONDA INVALIDA] {det}. NO contar esos resultados como fallos del modelo.", flush=True)
    print(f"\nresumen -> {ruta_res}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
