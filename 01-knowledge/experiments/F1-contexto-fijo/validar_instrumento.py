#!/usr/bin/env python3
"""F1 / Fase F1.1 — VALIDACIÓN DEL INSTRUMENTO (RULE-015). BLOQUEANTE.

Sin esta fase, ninguna cifra de F1.2 vale. Comprueba, contra el endpoint local:
  V1 determinismo      mismo payload x3            -> varianza debe ser 0
  V2 linealidad        unidad x1,x2,x3             -> incrementos constantes
  V3 suelo             prompt de 1 char            -> offset explicito (no oculto)
  V4 ratio chars/token prosa vs JSON               -> si baila, el formato reconstruido esta mal
  V5 contraste ledger  aplica el ratio al ledger   -> coherencia de orden de magnitud

NO fija umbrales (RULE-015: primero baseline, despues umbral).
NO carga modelos: usa el que ya esta en VRAM. Si el modelo no esta cargado, PARA con error.

Uso:  python3 validar_instrumento.py [--base http://127.0.0.1:1234/v1] [--modelo ID]
"""
import json
import sys
import urllib.error
import urllib.request

BASE_DEF = "http://127.0.0.1:1234/v1"
TIMEOUT = 240
SAL = "/tmp/f1-contexto/validacion_instrumento.json"


def pide(url, payload):
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": "Bearer lm-studio"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.loads(r.read().decode("utf-8", "replace"))


def modelo_disponible(base, pedido=None):
    with urllib.request.urlopen(base + "/models", timeout=30) as r:
        d = json.loads(r.read().decode("utf-8", "replace"))
    ids = [m["id"] for m in d.get("data", [])]
    if not ids:
        raise SystemExit("ERROR: /models no devuelve ningun modelo. No se inventa ningun id.")
    if pedido and pedido not in ids:
        raise SystemExit(f"ERROR: el modelo {pedido!r} no esta en /models: {ids}")
    return pedido or ids[0], ids


def tokens(base, modelo, texto):
    """prompt_tokens REAL del endpoint para `texto` como mensaje de sistema."""
    d = pide(base + "/chat/completions", {
        "model": modelo, "temperature": 0, "max_tokens": 1,
        "messages": [{"role": "system", "content": texto}]})
    u = d.get("usage") or {}
    if u.get("prompt_tokens") is None:
        raise SystemExit(f"ERROR: respuesta sin usage.prompt_tokens: {list(u)}")
    return int(u["prompt_tokens"])


def main():
    argv = sys.argv[1:]
    base = BASE_DEF
    pedido = None
    for i, a in enumerate(argv):
        if a == "--base" and i + 1 < len(argv):
            base = argv[i + 1]
        if a == "--modelo" and i + 1 < len(argv):
            pedido = argv[i + 1]
    base = base.rstrip("/")

    modelo, ids = modelo_disponible(base, pedido)
    print(f"endpoint: {base}")
    print(f"modelo:   {modelo}   (disponibles: {len(ids)})")
    out = {"base": base, "modelo": modelo, "checks": {}}

    # --- V1 determinismo -------------------------------------------------------
    texto = "F1-V1 " * 120
    v1 = [tokens(base, modelo, texto) for _ in range(3)]
    uni = len(set(v1)) == 1
    out["checks"]["V1_determinismo"] = {"valores": v1, "varianza_cero": uni}
    print(f"V1 determinismo  : {v1}  -> {'OK' if uni else 'FALLA (varianza != 0)'}")

    # --- V2 linealidad ---------------------------------------------------------
    unidad = "unidad-de-medicion F1 con palabras variadas para tokenizar. " * 40
    t1 = tokens(base, modelo, unidad)
    t2 = tokens(base, modelo, unidad + unidad)
    t3 = tokens(base, modelo, unidad * 3)
    d12, d23 = t2 - t1, t3 - t2
    desp = abs(d12 - d23) / max(1, d12)
    lineal = desp <= 0.02
    out["checks"]["V2_linealidad"] = {"t1": t1, "t2": t2, "t3": t3,
                                      "delta_1_2": d12, "delta_2_3": d23,
                                      "desviacion_relativa": round(desp, 4), "lineal_2pct": lineal}
    print(f"V2 linealidad    : {t1} -> {t2} -> {t3}  "
          f"(+{d12}, +{d23}, desv {desp:.2%}) -> {'OK' if lineal else 'FALLA'}")

    # --- V3 suelo --------------------------------------------------------------
    suelo = tokens(base, modelo, "x")
    out["checks"]["V3_suelo"] = {"tokens_con_1_char": suelo}
    print(f"V3 suelo (1 char): {suelo} tokens  -> offset explicito, se resta en F1.2")

    # --- V4 ratio chars/token por tipo ----------------------------------------
    prosa = ("En un sistema de agentes el contexto es un presupuesto: cada token que entra "
             "se paga en dinero, en latencia y en atencion. " * 60)
    jsontools = json.dumps({"type": "function", "function": {
        "name": "buscar_perfume",
        "description": "Busca perfumes por nombre o casa.",
        "parameters": {"type": "object", "properties": {
            "nombre": {"type": "string", "description": "texto parcial"},
            "limite": {"type": "integer", "description": "maximo de filas"}},
            "required": ["nombre"]}}}, ensure_ascii=False) * 40
    codigo = ("for f in /tmp/f1-contexto/*.py; do python3 -m py_compile \"$f\" && echo OK; done\n"
              "docker compose -f /home/jokoalmi/automation-stack/docker-compose.yml ps\n"
              "curl -s -m 8 http://localhost:1234/v1/models | head -c 300\n") * 30
    rp, rj = tokens(base, modelo, prosa), tokens(base, modelo, jsontools)
    rc = tokens(base, modelo, codigo)
    cpt_p, cpt_j, cpt_c = len(prosa) / rp, len(jsontools) / rj, len(codigo) / rc
    todos = [cpt_p, cpt_j, cpt_c]
    rango = (max(todos) - min(todos)) / max(todos)
    # RECTIFICADO 2026-09-16: el umbral del 10% era A PRIORI (contra RULE-015) y el baseline lo
    # desmiente: el ratio depende del TIPO de contenido (identificadores, llaves, rutas tokenizan
    # peor que la prosa). V4 pasa a INFORMATIVO, no bloqueante: la medicion de bloques de F1.2 es
    # DIRECTA (tokens del texto real), no derivada de ningun ratio. Lo unico que V4 limita es
    # cualquier estimacion chars->tokens, que se etiqueta con este rango.
    out["checks"]["V4_ratio_chars_token"] = {
        "prosa": {"chars": len(prosa), "tokens": rp, "chars_por_token": round(cpt_p, 2)},
        "json": {"chars": len(jsontools), "tokens": rj, "chars_por_token": round(cpt_j, 2)},
        "codigo": {"chars": len(codigo), "tokens": rc, "chars_por_token": round(cpt_c, 2)},
        "rango_relativo": round(rango, 4),
        "bloqueante": False,
        "consecuencia": ("toda estimacion chars->tokens lleva +-%d%% de error; las cifras de F1.2 "
                         "NO se derivan asi, se miden" % round(rango * 100)),
    }
    print(f"V4 ratio chars/tk: prosa {cpt_p:.2f} · JSON {cpt_j:.2f} · codigo {cpt_c:.2f}  "
          f"(rango {rango:.1%}) -> INFORMATIVO: estimaciones por chars con +-{rango:.0%}; F1.2 mide directo")

    # --- V5 contraste con el ledger -------------------------------------------
    v5 = {"disponible": False}
    try:
        import collections
        ruta = "/home/jokoalmi/joko-lab/04-operations/metrics/pipeline_obs.jsonl"
        vals, vistos = [], set()
        with open(ruta, "r", encoding="utf-8", errors="replace") as f:
            for ln in f:
                try:
                    r = json.loads(ln)
                except ValueError:
                    continue
                pt = r.get("prompt_tokens")
                if r.get("status") != 200 or not pt or r.get("model") in (None, ""):
                    continue
                if r.get("path") == "/api/show":
                    continue
                clave = (r.get("timestamp"), pt, r.get("completion_tokens"))
                if clave in vistos:
                    continue
                vistos.add(clave)
                vals.append((r["timestamp"], int(pt), r.get("model")))
        vals.sort()
        if vals:
            # el minimo absoluto del ledger son sondas del proxy (~85 tok), NO contexto de
            # agente: el suelo real se busca por encima de ese ruido.
            no_sonda = [v for v in vals if v[1] >= 1000]
            # ⚠️ BUG corregido en el acto: `min(tuplas)` compara por TIMESTAMP, no por tokens
            # -> devolvia el prompt mas ANTIGUO (25.625) en vez del mas pequeno (1.009).
            mn = min(no_sonda, key=lambda x: x[1]) if no_sonda else None
            v5 = {"disponible": True, "n_llamadas_limpias": len(vals),
                  "n_sondas_menores_1000": len(vals) - len(no_sonda),
                  "minimo_prompt_tokens_no_sonda": (mn[1] if mn else "no_calculable"),
                  "minimo_timestamp": (mn[0] if mn else None),
                  "minimo_modelo": (mn[2] if mn else None),
                  "minimo_absoluto_del_ledger": min(vals, key=lambda x: x[1])[1],
                  "nota": ("suelo del prompt REAL del pipeline cloud (tokenizador DeepSeek, "
                           "distinto al local): sirve de orden de magnitud, no de igualdad")}
            print(f"V5 ledger        : {len(vals)} llamadas limpias "
                  f"({len(vals) - len(no_sonda)} sondas <1000 tok excluidas); suelo no-sonda "
                  f"= {mn[1] if mn else 'no_calculable'} en {mn[0] if mn else '-'} "
                  f"({mn[2] if mn else '-'})")
    except OSError as e:
        v5 = {"disponible": False, "error": str(e)}
        print(f"V5 ledger        : no_calculable ({e})")

    out["checks"]["V5_contraste_ledger"] = v5
    out["veredicto_instrumento"] = (
        "VALIDADO (V1 determinismo y V2 linealidad OK; V3 fija el offset; "
        "V4 informativo: el ratio chars/token depende del tipo de contenido y F1.2 no lo usa)"
        if (uni and lineal)
        else "NO VALIDADO: revisar los checks que fallan ANTES de medir bloques")
    print(f"\nveredicto instrumento: {out['veredicto_instrumento']}")

    with open(SAL, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"escrito: {SAL}")
    return 0 if (uni and lineal) else 1


if __name__ == "__main__":
    sys.exit(main())
