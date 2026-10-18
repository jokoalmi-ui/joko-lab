#!/usr/bin/env python3
"""
fusion_total.py — FUSIÓN TOTAL: patrón escritor+revisor (A2+, #13, 25-ago-2026).

2-3 modelos locales ESCRIBEN cada uno una respuesta a la pregunta; los jueces
(llm_as_judge) evalúan cada respuesta; se elige la mejor por promedio.

Diseño validado con el juicio ciego de redacción del 25-ago: gemma-4-12b
(Director Creativo, RULE-001) ganó a gpt-oss y a DeepSeek en T1/T2; gpt-oss
es el modelo de razonamiento (RULE-003). Por defecto:
  Escritores: E1 = gemma-4-12b-qat (redacción) · E2 = gpt-oss-20b (razonamiento)
  Jueces:     J1 = glm-4.6v-flash · J2 = gpt-oss-20b  (llm_as_judge, n_juicios)

Uso:
  python3 tools/fusion_total.py --pregunta "..." [--contexto "..."] [--json]
  echo '{"pregunta":"...","contexto":"..."}' | python3 tools/fusion_total.py --stdin

Flags:
  --escritores "m1,m2,m3"   modelos que escriben (default gemma+gpt-oss)
  --juez1 / --juez2         jueces (default GLM / gpt-oss)
  --n-juicios N             llamadas por juez (default 3, hereda robustez 25-ago)
  --temp-escritor T         temperatura de los escritores (default 0.4)
  --swap                    swap automático de VRAM (unload/load entre modelos)
  --log                     registra en SQLite (reutiliza llm_as_judge)
  --json                    salida JSON

Nota VRAM (12 GB): gemma (6.66) y gpt-oss (11.28) no caben juntos; GLM (7.41)
tampoco convive con gpt-oss. Con --swap el script carga/descarga bajo demanda
(patrón validado en llm_as_judge 21-ago). Sin --swap, usar solo modelos que
quepan juntos o aceptar UN_JUEZ/UN_ESCRITOR degradado.
"""
import argparse
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from llm_as_judge import (juzgar, consolidar, _cargar_bajo_demanda,
                          _modelo_cargado, _modelos_cargados,
                          _restaurar_estado, _guardar_log,
                          JUEZ1_DEF, JUEZ2_DEF)

ENDPOINT = "http://localhost:1234/api/v0/chat/completions"
ESCRITOR1_DEF = "google/gemma-4-12b-qat"   # redacción — Director Creativo (RULE-001, juicio 25-ago)
ESCRITOR2_DEF = "openai/gpt-oss-20b"       # razonamiento (RULE-003)

_PROMPT_ESCRITOR = """Eres un escritor experto en español (Joko Lab). Responde a la petición con calidad, directo, sin relleno. NO razones en voz alta: da SOLO la respuesta final.

PETICIÓN: {pregunta}
CONTEXTO DISPONIBLE (puede estar vacío): {contexto}
"""


def generar(escritor: str, pregunta: str, contexto: str,
            temp: float = 0.4, timeout: int = 600) -> dict:
    """Pide a UN escritor que genere una respuesta. Devuelve dict con content/tiempo/error."""
    if not _modelo_cargado(escritor):
        if not _cargar_bajo_demanda(escritor, swap=True):
            print(f"  [escritor] {escritor} no cargado — omitido", file=sys.stderr)
            return {"escritor": escritor, "usado": False,
                    "error": "no se pudo cargar (VRAM)"}
        print(f"  [escritor] {escritor} cargado bajo demanda", file=sys.stderr)
    prompt = (_PROMPT_ESCRITOR
              .replace("{pregunta}", pregunta[:2000])
              .replace("{contexto}", (contexto or "")[:3000]))
    try:
        payload = {"model": escritor,
                   "messages": [{"role": "user", "content": prompt}],
                   "max_tokens": 2048, "temperature": temp}
        req = urllib.request.Request(ENDPOINT, data=json.dumps(payload).encode(),
                                     headers={"Content-Type": "application/json"})
        t0 = time.time()
        with urllib.request.urlopen(req, timeout=timeout) as r:
            resp = json.load(r)
        elapsed = time.time() - t0
        msg = resp.get("choices", [{}])[0].get("message", {})
        content = (msg.get("content")
                   or msg.get("reasoning_content")
                   or msg.get("reasoning") or "")
        if not content.strip():
            return {"escritor": escritor, "usado": False, "error": "respuesta vacía (finish=length?)"}
        return {"escritor": escritor, "usado": True,
                "content": content.strip(), "tiempo_s": round(elapsed, 1)}
    except Exception as e:
        return {"escritor": escritor, "usado": False, "error": str(e)[:120]}


def main() -> int:
    ap = argparse.ArgumentParser(description="Fusión total: N escritores + jueces (patrón escritor+revisor)")
    ap.add_argument("--pregunta", default="")
    ap.add_argument("--contexto", default="")
    ap.add_argument("--escritores", default=f"{ESCRITOR1_DEF},{ESCRITOR2_DEF}",
                    help="modelos que escriben, separados por coma")
    ap.add_argument("--juez1", default=JUEZ1_DEF)
    ap.add_argument("--juez2", default=JUEZ2_DEF)
    ap.add_argument("--n-juicios", type=int, default=3)
    ap.add_argument("--temp-escritor", type=float, default=0.4)
    ap.add_argument("--swap", action="store_true",
                    help="swap automático de VRAM entre modelos (lento pero completo)")
    ap.add_argument("--log", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--stdin", action="store_true")
    ap.add_argument("--verifica", action="store_true",
                    help="verifica fidelidad de datos contra la fuente antes de emitir "
                         "(fail-closed: si la ganadora FALLA, prueba la siguiente candidata)")
    ap.add_argument("--escala-cloud", action="store_true",
                    help="si --verifica da NO_FIABLE, escala a DeepSeek cloud (proxy :9911) "
                         "y devuelve su respuesta etiquetada (local-first con respaldo cloud)")
    args = ap.parse_args()

    if args.stdin:
        try:
            data = json.load(sys.stdin)
            pregunta = data.get("pregunta", "")
            contexto = data.get("contexto", "")
        except Exception as e:
            print(f"ERROR stdin: {e}")
            return 1
    else:
        pregunta, contexto = args.pregunta, args.contexto
    if not pregunta.strip():
        print("ERROR: --pregunta vacía")
        return 1

    escritores = [m.strip() for m in args.escritores.split(",") if m.strip()]
    if not escritores:
        print("ERROR: --escritores vacío")
        return 1

    estado_original = _modelos_cargados() if args.swap else set()

    # ── FASE 1: ESCRIBIR ──────────────────────────────────────────────
    print(f"FASE 1/2 — {len(escritores)} escritores generan respuesta...", file=sys.stderr)
    candidatos = []
    for w in escritores:
        print(f"  → {w} escribiendo...", file=sys.stderr)
        r = generar(w, pregunta, contexto, temp=args.temp_escritor)
        if r.get("usado"):
            candidatos.append(r)
            print(f"    ✓ {len(r['content'])} chars en {r['tiempo_s']}s", file=sys.stderr)
        else:
            print(f"    ✗ {r.get('error', 'fallo')}", file=sys.stderr)

    if not candidatos:
        res = {"estado": "SIN_ESCRITOR",
               "detalle": "Ningún escritor pudo generar respuesta (LM Studio apagado o VRAM)."}
        print(json.dumps(res, ensure_ascii=False, indent=2) if args.json else res)
        return 1

    # ── FASE 2: JUZGAR ────────────────────────────────────────────────
    print(f"FASE 2/2 — {len(candidatos)} respuestas a evaluar con jueces...", file=sys.stderr)
    evaluados = []
    for c in candidatos:
        j1 = juzgar(c["content"], pregunta, contexto, args.juez1,
                    swap=args.swap, n_juicios=args.n_juicios)
        j2 = juzgar(c["content"], pregunta, contexto, args.juez2,
                    swap=args.swap, n_juicios=args.n_juicios)
        cons = consolidar(j1, j2)
        evaluados.append({**c, "jueces": cons})
        print(f"  [{c['escritor']}] → {cons.get('veredicto')} ({cons.get('promedio')})",
              file=sys.stderr)

    # ── SELECCIÓN: mejor promedio entre los que no FALLAN por fidelidad ──
    def _puntaje(e):
        prom = e["jueces"].get("promedio", 0)
        v = e["jueces"].get("veredicto", "FALLA")
        return prom if v != "FALLA" else -1.0

    evaluados.sort(key=_puntaje, reverse=True)

    # ── VERIFICADOR DE FIDELIDAD (opcional, fail-closed) ──
    # Si --verifica: cruzar datos de la respuesta ganadora contra la fuente
    # (pregunta + contexto). Si FALLA, probar la siguiente candidata.
    verificacion = None
    verif_candidatos = []  # diagnóstico: veredicto+discrepancias por candidato
    if args.verifica:
        from verificador_fidelidad import verificar
        fuente = pregunta + "\n\n" + (contexto or "")
        for cand in evaluados:
            v = verificar(cand["content"], fuente)
            verif_candidatos.append({
                "escritor": cand["escritor"],
                "veredicto": v["veredicto"],
                "discrepancias": v["discrepancias"],
            })
            if v["veredicto"] != "FALLA":
                mejor = cand
                verificacion = v
                break
        else:
            # Ninguna candidata pasa el verificador → fail-closed, no emitir
            mejor = None
            verificacion = {"veredicto": "NO_FIABLE",
                            "discrepancias": ["ninguna candidata pasa el verificador de fidelidad"]}
            print("  [verifica] NINGUNA candidata fiable → NO se emite respuesta",
                  file=sys.stderr)
            # Guardar respuestas + discrepancias para diagnóstico sin re-ejecutar
            try:
                with open("/tmp/fusion_debug_nofiable.json", "w") as f:
                    json.dump({
                        "pregunta": pregunta,
                        "contexto": contexto,
                        "verificaciones": verif_candidatos,
                        "candidatos": [{"escritor": e["escritor"], "content": e.get("content", "")}
                                       for e in evaluados],
                    }, f, ensure_ascii=False, indent=2)
                print("  [verifica] diagnóstico guardado en /tmp/fusion_debug_nofiable.json",
                      file=sys.stderr)
            except Exception as e:
                print(f"  [verifica] no se pudo guardar diagnóstico: {e}", file=sys.stderr)
    else:
        mejor = evaluados[0]

    if args.swap:
        _restaurar_estado(estado_original)
        print("  [fusion] estado de modelos restaurado", file=sys.stderr)
    if args.log and mejor is not None:
        _guardar_log(mejor["jueces"], pregunta, mejor["content"])

    if mejor is None:
        # Fail-closed: ninguna candidata pasó el verificador de fidelidad.
        # Con --escala-cloud: reenviar la pregunta a DeepSeek cloud (proxy :9911)
        # y devolver su respuesta etiquetada (local-first con respaldo cloud).
        if args.escala_cloud:
            print("  [escala-cloud] local NO_FIABLE → preguntando a DeepSeek cloud...",
                  file=sys.stderr)
            try:
                sys.path.insert(0, str(Path(__file__).resolve().parent))
                from local_cloud_orchestrator import ejecutar_cloud, escribir_ledger
                payload_cloud = pregunta
                if contexto:
                    payload_cloud = f"{pregunta}\n\nContexto:\n{contexto}"
                r = ejecutar_cloud(payload_cloud)
                escribir_ledger({"ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                                 "tipo": "fusion-redaccion", "intento_local": True,
                                 "local_ok": False, "cloud_ok": r.get("ok"),
                                 "motivo": "verificador de fidelidad NO_FIABLE"})
                if r.get("ok"):
                    res = {"estado": "FUSION_CLOUD",
                           "origen": "cloud",
                           "motivo": "verificador de fidelidad local NO_FIABLE",
                           "respuesta": r["salida"],
                           "latencia_s": r.get("latencia_s"),
                           "candidatos": [{"escritor": e["escritor"],
                                           "veredicto": e["jueces"].get("veredicto"),
                                           "promedio": e["jueces"].get("promedio")}
                                          for e in evaluados]}
                    if args.json:
                        print(json.dumps(res, ensure_ascii=False, indent=2))
                    else:
                        print("=== FUSIÓN TOTAL (escritor+revisor) ===")
                        print("FUSION_CLOUD: respaldo de DeepSeek cloud "
                              "(el verificador local bloqueó a los escritores locales)")
                        print(f"Latencia cloud: {r.get('latencia_s')}s")
                        print("\n--- RESPUESTA (cloud) ---")
                        print(r["salida"])
                    return 0
                # Cloud también falló → NO_FIABLE real
                print(f"  [escala-cloud] cloud falló: {r.get('stderr', '')[:200]}",
                      file=sys.stderr)
            except Exception as e:
                print(f"  [escala-cloud] error al escalar: {e}", file=sys.stderr)

        res = {"estado": "NO_FIABLE",
               "verificacion": verificacion,
               "candidatos": [{"escritor": e["escritor"],
                               "veredicto": e["jueces"].get("veredicto"),
                               "promedio": e["jueces"].get("promedio")} for e in evaluados]}
        if args.json:
            print(json.dumps(res, ensure_ascii=False, indent=2))
        else:
            print("=== FUSIÓN TOTAL (escritor+revisor) ===")
            print("NO_FIABLE: ninguna candidata pasó el verificador de fidelidad.")
            print(f"Discrepancias: {verificacion.get('discrepancias', [])}")
        return 2

    res = {
        "estado": "FUSION",
        "mejor": {"escritor": mejor["escritor"],
                  "veredicto": mejor["jueces"].get("veredicto"),
                  "promedio": mejor["jueces"].get("promedio"),
                  "respuesta": mejor["content"]},
        "verificacion": ({"veredicto": verificacion.get("veredicto"),
                          "discrepancias": verificacion.get("discrepancias", [])}
                         if verificacion else None),
        "candidatos": [{"escritor": e["escritor"],
                        "veredicto": e["jueces"].get("veredicto"),
                        "promedio": e["jueces"].get("promedio"),
                        "chars": len(e.get("content", "")),
                        "tiempo_s": e.get("tiempo_s")} for e in evaluados],
    }

    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print("=== FUSIÓN TOTAL (escritor+revisor) ===")
        print(f"Mejor respuesta: {mejor['escritor']} | {mejor['jueces'].get('veredicto')} ({mejor['jueces'].get('promedio')})")
        if verificacion:
            print(f"Fidelidad: {verificacion.get('veredicto')} | "
                  f"{len(verificacion.get('discrepancias', []))} discrepancia(s)")
        for e in evaluados:
            print(f"  [{e['escritor']}] {e['jueces'].get('veredicto')} ({e['jueces'].get('promedio')}) | {e.get('tiempo_s')}s")
        print("\n--- MEJOR RESPUESTA ---")
        print(mejor["content"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
