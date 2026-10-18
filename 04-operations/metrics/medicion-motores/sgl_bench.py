#!/usr/bin/env python3
"""Banco de medida de motores de inferencia local (Joko Lab).

Instrumento CLIENTE unico: el mismo codigo mide cualquier motor que exponga
/v1/chat/completions (OpenAI compatible). Asi la cifra no depende de los
timings internos de cada motor (que no son comparables entre si).

Metricas por peticion:
  ttft_s        = t_primer_token - t_peticion
  decode_tok_s  = completion_tokens / (t_ultimo - t_primer_token)
  prefill_tok_s = prompt_tokens / ttft_s     (solo en la prueba de prefill)
  n_deltas      = chunks SSE con contenido (control cruzado del contador)

Uso:
  /usr/bin/python3 /tmp/sgl_bench.py --base-url http://localhost:1234 --model <id> --label lmstudio --out /tmp/bench_lmstudio.json
"""
import argparse, json, os, statistics, sys, threading, time, urllib.error, urllib.request

def chat(base, model, prompt, max_tokens, timeout=900):
    url = base.rstrip('/') + "/v1/chat/completions"
    body = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.0, "top_p": 1.0, "seed": 42,
        "max_tokens": max_tokens, "stream": True,
        "stream_options": {"include_usage": True},
    }
    def send(b):
        req = urllib.request.Request(url, data=json.dumps(b).encode(),
                                     headers={"Content-Type": "application/json"})
        return urllib.request.urlopen(req, timeout=timeout)
    t0 = time.perf_counter()
    try:
        try:
            r = send(body)
        except urllib.error.HTTPError as e:
            if e.code in (400, 422):
                body.pop("stream_options", None)
                r = send(body)
            else:
                raise
        t_first = None; n_deltas = 0; chars = 0; usage = None; last = t0
        with r:
            for raw in r:
                line = raw.decode('utf-8', 'replace').strip()
                if not line.startswith('data:'):
                    continue
                data = line[5:].strip()
                if data == '[DONE]':
                    break
                try:
                    j = json.loads(data)
                except Exception:
                    continue
                if j.get('usage'):
                    usage = j['usage']
                for c in (j.get('choices') or []):
                    piece = (c.get('delta') or {}).get('content')
                    if piece:
                        now = time.perf_counter()
                        if t_first is None:
                            t_first = now
                        n_deltas += 1; chars += len(piece); last = now
        t_end = time.perf_counter()
    except Exception as e:
        return {"error": "%s: %s" % (type(e).__name__, e), "wall_s": round(time.perf_counter() - t0, 3)}
    if t_first is None:
        return {"error": "sin tokens (respuesta vacia)", "wall_s": round(t_end - t0, 3)}
    ctok = (usage or {}).get('completion_tokens')
    ptok = (usage or {}).get('prompt_tokens')
    dec = max(t_end - t_first, 1e-9)
    out = {
        "ttft_s": round(t_first - t0, 4),
        "wall_s": round(t_end - t0, 4),
        "decode_s": round(dec, 4),
        "n_deltas": n_deltas,
        "usage_completion_tokens": ctok,
        "usage_prompt_tokens": ptok,
        "chars": chars,
    }
    tok = ctok if ctok else n_deltas
    out["tok_for_rate"] = tok
    out["decode_tok_s"] = round(tok / dec, 2)
    if ptok:
        out["prefill_tok_s"] = round(ptok / max(out["ttft_s"], 1e-9), 1)
    return out

def parallel(base, model, prompts, max_tokens):
    res = [None] * len(prompts)
    def w(i, p):
        res[i] = chat(base, model, p, max_tokens)
    t0 = time.perf_counter()
    ths = [threading.Thread(target=w, args=(i, p)) for i, p in enumerate(prompts)]
    for t in ths: t.start()
    for t in ths: t.join()
    wall = time.perf_counter() - t0
    ok = [r for r in res if r and 'error' not in r]
    tot = sum(r["tok_for_rate"] for r in ok)
    return {
        "n": len(prompts), "wall_s": round(wall, 3), "ok": len(ok),
        "aggregate_tok_s": round(tot / wall, 2) if wall > 0 else None,
        "per_request_tok_s": [r["decode_tok_s"] for r in ok],
        "ttft_s": [r["ttft_s"] for r in ok],
        "first_ttft_s": min([r["ttft_s"] for r in ok], default=None),
    }

FILLER = ("El laboratorio registra cada medicion con su hora real, su hardware y su build, "
          "porque una cifra sin contexto no es un dato sino una opinion. ")

def nonce():
    return os.urandom(4).hex()

def long_prompt(n_repeat, tail, tag):
    # el nonce va AL PRINCIPIO: invalida cualquier prefijo cacheado, de modo que la
    # peticion mide prefill en FRIO de verdad (si no, se mide un acierto de cache).
    return "[%s] " % tag + (FILLER * n_repeat) + "\n\n" + tail

PROSE = ("Escribe en prosa continua, sin listas, un texto de unas 150 palabras sobre por que "
         "conviene medir antes de optimizar y que errores aparecen cuando se optimiza a ciegas.")
STRUCT = ("Devuelve exactamente 8 lineas numeradas. Cada linea: numero, nombre de un motor de "
          "inferencia y su caracteristica principal en menos de 12 palabras.")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--label", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--rounds", type=int, default=2)
    ap.add_argument("--prefix-repeats", type=int, default=60)
    ap.add_argument("--probe", action="store_true", help="una sola llamada corta para validar el instrumento")
    a = ap.parse_args()

    meta = {"label": a.label, "base_url": a.base_url, "model": a.model,
            "started": time.strftime("%Y-%m-%d %H:%M:%S %Z"), "rounds": a.rounds,
            "prefix_repeats": a.prefix_repeats}
    if a.probe:
        r = chat(a.base_url, a.model, "Responde solo: ok", 8)
        print(json.dumps({"probe": r}, ensure_ascii=False, indent=1))
        return

    data = {"meta": meta, "rounds": []}
    for rnd in range(1, a.rounds + 1):
        r = {"round": rnd}
        r["claseA_estructurada"] = chat(a.base_url, a.model, STRUCT, 192)
        r["claseB_prosa"] = chat(a.base_url, a.model, PROSE, 192)
        # prefill en FRIO: nonce distinto por ronda, para que no haya acierto de cache
        r["prefill_1token"] = chat(a.base_url, a.model,
                                   long_prompt(a.prefix_repeats, "Responde solo: ok", "frio-" + nonce()), 1)
        # prefijo REPETIDO a proposito: el MISMO nonce en las 3 peticiones -> la 1 es fria,
        # las 2 y 3 llegan con el prefijo ya cacheado (asi se mide el acierto de cache)
        r["prefijo_repetido"] = [
            chat(a.base_url, a.model,
                 long_prompt(a.prefix_repeats, "Pregunta %d: responde en dos frases." % i, "cache-%d" % rnd),
                 64)
            for i in range(1, 4)]
        r["conc2"] = parallel(a.base_url, a.model,
                              [PROSE + "\n[%s]" % nonce(), STRUCT + "\n[%s]" % nonce()], 128)
        r["conc4"] = parallel(a.base_url, a.model,
                              [PROSE + "\n[%s]" % nonce(), STRUCT + "\n[%s]" % nonce(),
                               PROSE + "\n[%s]" % nonce(), STRUCT + "\n[%s]" % nonce()], 128)
        data["rounds"].append(r)
        print("[%s] ronda %d lista" % (a.label, rnd), flush=True)

    def med(path_fn):
        vals = [path_fn(rr) for rr in data["rounds"]]
        vals = [v for v in vals if v]
        return round(statistics.median(vals), 2) if vals else None

    data["resumen"] = {
        "claseA_decode_tok_s_mediana": med(lambda x: x["claseA_estructurada"].get("decode_tok_s")),
        "claseB_decode_tok_s_mediana": med(lambda x: x["claseB_prosa"].get("decode_tok_s")),
        "claseA_ttft_mediana_s": med(lambda x: x["claseA_estructurada"].get("ttft_s")),
        "claseB_ttft_mediana_s": med(lambda x: x["claseB_prosa"].get("ttft_s")),
        "prefill_tok_s_mediana": med(lambda x: x["prefill_1token"].get("prefill_tok_s")),
        "prefijo_ttft_s": [[rr["prefijo_repetido"][i].get("ttft_s") for i in range(3)] for rr in data["rounds"]],
        "conc2_aggregate_tok_s": med(lambda x: x["conc2"].get("aggregate_tok_s")),
        "conc4_aggregate_tok_s": med(lambda x: x["conc4"].get("aggregate_tok_s")),
    }
    data["meta"]["finished"] = time.strftime("%Y-%m-%d %H:%M:%S %Z")
    with open(a.out, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print(json.dumps(data["resumen"], ensure_ascii=False, indent=1))

if __name__ == "__main__":
    main()
