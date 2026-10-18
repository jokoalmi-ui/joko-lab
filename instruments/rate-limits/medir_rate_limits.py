#!/usr/bin/env python3
"""Rate Limits v0.1 — instrumento de medicion (solo lectura).

RESTRICCION CONSTITUCIONAL: este script NO modifica absolutamente nada.
- No toca el proxy (pipeline_proxy.py) ni la config de Hermes.
- No bloquea ni limita llamadas.
- No propone cambios.
Su unica mision es OBSERVAR, MEDIR y REGISTRAR.

Fuente: /home/jokoalmi/joko-lab/04-operations/metrics/pipeline_obs.jsonl
Uso:
    python3 medir_rate_limits.py                 # informe por stdout
    python3 medir_rate_limits.py --json out.json # ademas escribe JSON
    python3 medir_rate_limits.py --watchdog 24   # silencio si no hay frenos en 24h
    python3 medir_rate_limits.py --saldo         # + saldo real de la cuenta (no gasta tokens)
    python3 medir_rate_limits.py --saldo --min 2 # + aviso si el saldo baja de 2
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from collections import Counter
from datetime import datetime, timedelta, timezone

LEDGER = "/home/jokoalmi/joko-lab/04-operations/metrics/pipeline_obs.jsonl"
OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs")

# Unica fuente real de CUOTA medida en F0 (11-oct-2026): DeepSeek NO manda
# cabeceras x-ratelimit-*; el saldo de la cuenta SI es consultable.
ENV = "/home/jokoalmi/.hermes/.env"
KEYNAME = "DEEPSEEK_API" + "_KEY"          # por partes: no disparar el redactor
BALANCE_URL = "https://api.deepseek.com/user/balance"
SALDO_LOG = os.path.join(OUTDIR, "saldo.jsonl")

# Familias de freno. NO son umbrales: son clasificaciones de codigo HTTP.
FAMILIAS = {
    "cuota": {402, 403, 429},
    "auth": {401},
    "ritmo": {429},
    "red": {0},
    "cliente": {400, 404, 405, 422},
}
RUIDO = "/api/show"  # sonda de estilo Ollama: 404 esperado, no es error


def parse_ts(v):
    if not v:
        return None
    try:
        dt = datetime.fromisoformat(str(v).replace("Z", "+00:00"))
    except Exception:
        return None
    if dt.tzinfo is None:          # el ledger tambien tiene timestamps naive
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def cargar(path):
    rows, ilegibles = [], 0
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for ln in f:
            ln = ln.strip()
            if not ln:
                continue
            try:
                rows.append(json.loads(ln))
            except Exception:
                ilegibles += 1
    return rows, ilegibles


def analizar(rows, ilegibles, path, ahora=None):
    ahora = ahora or datetime.now(timezone.utc)
    con_ts = [(parse_ts(d.get("timestamp")), d) for d in rows]
    con_ts = [(t, d) for t, d in con_ts if t]
    con_ts.sort(key=lambda x: x[0])

    total = len(rows)
    status = Counter(str(d.get("status")) for d in rows)
    errs = [d for d in rows if d.get("status") not in (200, "200", None)]
    errs_reales = [d for d in errs if d.get("path") != RUIDO]
    ruido = len(errs) - len(errs_reales)

    def fam(s):
        s = int(s)
        for k, v in FAMILIAS.items():
            if s in v:
                return k
        return "otro"

    por_familia = Counter(fam(d.get("status")) for d in errs_reales)

    # dias con freno (excluye ruido)
    frenos_dia = Counter(str(d.get("timestamp"))[:10] for d in errs_reales)

    # peticiones LLM con tokens
    llm = [(t, d) for t, d in con_ts if d.get("prompt_tokens")]
    rpm_max, rpm_at = 0, None
    tpm_max, tpm_at = 0, None
    i = 0
    for j in range(len(llm)):
        while llm[j][0] - llm[i][0] > timedelta(seconds=60):
            i += 1
        n = j - i + 1
        if n > rpm_max:
            rpm_max, rpm_at = n, llm[i][0]
        tok = sum((llm[k][1].get("prompt_tokens") or 0) + (llm[k][1].get("completion_tokens") or 0)
                  for k in range(i, j + 1))
        if tok > tpm_max:
            tpm_max, tpm_at = tok, llm[i][0]

    # rafagas identicas consecutivas (model + prompt_tokens + completion_tokens)
    def sig(d):
        return (d.get("model"), d.get("prompt_tokens"), d.get("completion_tokens"))
    rafagas, run = [], 1
    for k in range(1, len(llm)):
        if sig(llm[k][1]) == sig(llm[k - 1][1]):
            run += 1
        else:
            if run >= 3:
                rafagas.append((llm[k - run][0], run))
            run = 1
    if run >= 3:
        rafagas.append((llm[len(llm) - run][0], run))

    # latencia hasta la siguiente llamada tras un error real
    gaps = []
    for k in range(len(con_ts) - 1):
        d = con_ts[k][1]
        if d.get("status") not in (200, "200", None) and d.get("path") != RUIDO:
            gaps.append((con_ts[k + 1][0] - con_ts[k][0]).total_seconds())
    gaps.sort()

    # tokens gastados en llamadas que acabaron mal (coste tirado)
    tok_err = sum((d.get("prompt_tokens") or 0) + (d.get("completion_tokens") or 0) for d in errs_reales)

    # cabeceras de rate limit capturadas en el ledger
    campos = sorted({k for d in rows for k in d
                     if any(w in k.lower() for w in ("rate", "limit", "remaining", "retry", "quota"))})

    return {
        "fuente": path,
        "generado": ahora.isoformat(),
        "ledger": {
            "lineas": total, "json_ilegible": ilegibles,
            "tamano_mb": round(os.path.getsize(path) / 1e6, 1),
            "desde": con_ts[0][0].isoformat() if con_ts else None,
            "hasta": con_ts[-1][0].isoformat() if con_ts else None,
        },
        "status": dict(status.most_common()),
        "frenos": {
            "total_no_200": len(errs),
            "reales": len(errs_reales),
            "ruido_api_show": ruido,
            "por_familia": dict(por_familia),
            "por_status": dict(Counter(str(d.get("status")) for d in errs_reales).most_common()),
            "por_path": dict(Counter(str(d.get("path")) for d in errs_reales).most_common(5)),
            "por_dia": dict(frenos_dia.most_common(10)),
            "tokens_gastados_en_fallos": tok_err,
        },
        "ritmo": {"rpm_max": rpm_max, "rpm_instante": rpm_at.isoformat() if rpm_at else None,
                  "tpm_max": tpm_max, "tpm_instante": tpm_at.isoformat() if tpm_at else None,
                  "llamadas_con_tokens": len(llm)},
        "reintentos": {
            "rafagas_identicas_ge3": len(rafagas),
            "lineas_en_rafagas": sum(r[1] for r in rafagas),
            "top": [{"desde": r[0].isoformat(), "n": r[1]} for r in sorted(rafagas, key=lambda x: -x[1])[:5]],
            "espera_tras_error_s": ({"n": len(gaps), "min": round(gaps[0], 2),
                                     "p50": round(gaps[len(gaps)//2], 2), "max": round(gaps[-1], 1)} if gaps else None),
        },
        "cabeceras_rate_limit_en_ledger": campos or "NINGUNO",
        "watchdog": {},
    }


def leer_clave():
    """Lee la clave del .env SIN imprimirla nunca."""
    if not os.path.exists(ENV):
        return None
    with open(ENV, "r", encoding="utf-8", errors="replace") as f:
        for ln in f:
            ln = ln.strip()
            if ln.startswith("export "):
                ln = ln[7:]
            if ln.startswith(KEYNAME + "="):
                return ln.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def consultar_saldo(registrar=True):
    """GET /user/balance -> dict. Solo lectura; no consume tokens."""
    key = leer_clave()
    if not key:
        return {"error": "sin clave en el .env (no aparece)"}
    req = urllib.request.Request(BALANCE_URL, method="GET")
    req.add_header("Authorization", "Bearer " + key)
    req.add_header("User-Agent", "joko-lab-rate-limits/0.1")
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            data = json.loads(r.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as e:
        return {"error": "HTTP %s" % e.code, "body": e.read(300).decode("utf-8", "replace")[:300]}
    except Exception as e:
        return {"error": "%s: %s" % (type(e).__name__, e)}
    infos = (data.get("balance_infos") or [{}])[0]
    reg = {"ts": datetime.now(timezone.utc).isoformat(),
           "is_available": data.get("is_available"),
           "currency": infos.get("currency"),
           "total_balance": infos.get("total_balance")}
    if registrar:
        os.makedirs(OUTDIR, exist_ok=True)
        with open(SALDO_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(reg, ensure_ascii=False) + "\n")
    return reg


def informe(r):
    o = []
    L = r["ledger"]
    o.append("RATE LIMITS v0.1  (solo lectura)")
    o.append("ledger=%s" % r["fuente"])
    o.append("lineas=%d  json_ilegible=%d  %.1f MB  %s -> %s" % (
        L["lineas"], L["json_ilegible"], L["tamano_mb"], L["desde"], L["hasta"]))
    o.append("status=%s" % r["status"])
    f = r["frenos"]
    o.append("frenos_reales=%d  (ruido /api/show=%d)" % (f["reales"], f["ruido_api_show"]))
    o.append("  por_familia=%s" % f["por_familia"])
    o.append("  por_status=%s" % f["por_status"])
    o.append("  por_path=%s" % f["por_path"])
    o.append("  por_dia=%s" % f["por_dia"])
    o.append("  tokens_gastados_en_fallos=%d" % f["tokens_gastados_en_fallos"])
    t = r["ritmo"]
    o.append("ritmo: rpm_max=%d (%s)  tpm_max=%d (%s)  llamadas=%d" % (
        t["rpm_max"], t["rpm_instante"], t["tpm_max"], t["tpm_instante"], t["llamadas_con_tokens"]))
    rr = r["reintentos"]
    o.append("rafagas_identicas>=3: n=%d lineas=%d" % (rr["rafagas_identicas_ge3"], rr["lineas_en_rafagas"]))
    if rr["espera_tras_error_s"]:
        e = rr["espera_tras_error_s"]
        o.append("espera_tras_error_s: n=%d min=%.2f p50=%.2f max=%.1f" % (e["n"], e["min"], e["p50"], e["max"]))
    o.append("cabeceras_rate_limit_en_ledger=%s" % r["cabeceras_rate_limit_en_ledger"])
    if r.get("saldo"):
        s = r["saldo"]
        o.append("saldo: %s" % ("ERROR %s" % s.get("error") if s.get("error")
                                else "%s %s (disponible=%s)" % (s.get("total_balance"), s.get("currency"), s.get("is_available"))))
    return "\n".join(o)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default=None, help="ruta del JSON de salida")
    ap.add_argument("--watchdog", type=float, default=None,
                    help="horas: si no hay frenos reales en esa ventana, no imprime nada (exit 0)")
    ap.add_argument("--ledger", default=LEDGER)
    ap.add_argument("--saldo", action="store_true",
                    help="consulta GET /user/balance (no consume tokens) y lo registra en outputs/saldo.jsonl")
    ap.add_argument("--min", type=float, default=None,
                    help="umbral OPCIONAL de saldo declarado por el usuario (sin umbral por defecto)")
    a = ap.parse_args()

    if not os.path.exists(a.ledger):
        print("ERROR: no existe el ledger %s" % a.ledger)
        return 2

    rows, ilegibles = cargar(a.ledger)
    r = analizar(rows, ilegibles, a.ledger)

    avisos = []
    if a.saldo:
        s = consultar_saldo()
        r["saldo"] = s
        if s.get("error"):
            avisos.append("saldo: NO CONSULTABLE (%s)" % s["error"])
        elif a.min is not None:
            try:
                if float(s.get("total_balance") or 0) < a.min:
                    avisos.append("CUOTA BAJA: saldo %s %s < min %.2f"
                                  % (s.get("total_balance"), s.get("currency"), a.min))
            except (TypeError, ValueError):
                pass

    if a.watchdog is not None:
        rec = [d for d in rows
               if d.get("status") not in (200, "200", None) and d.get("path") != RUIDO]
        corte = datetime.now(timezone.utc) - timedelta(hours=a.watchdog)
        recientes = [d for d in rec if (parse_ts(d.get("timestamp")) or datetime.min.replace(tzinfo=timezone.utc)) >= corte]
        r["watchdog"] = {"horas": a.watchdog, "frenos_recientes": len(recientes),
                         "detalle": [{"ts": str(d.get("timestamp"))[:19], "status": d.get("status"), "path": d.get("path")} for d in recientes[:10]]}
        if recientes:
            avisos.append("AVISO rate limits: %d freno(s) en las ultimas %.0fh" % (len(recientes), a.watchdog))
            for d in recientes[:10]:
                avisos.append("  %s status=%s path=%s" % (str(d.get("timestamp"))[:19], d.get("status"), d.get("path")))
        if a.json:
            os.makedirs(os.path.dirname(os.path.abspath(a.json)), exist_ok=True)
            with open(a.json, "w", encoding="utf-8") as fh:
                json.dump(r, fh, ensure_ascii=False, indent=2)
        if not avisos:
            return 0            # silencio = normal (patron watchdog del lab)
        print("\n".join(avisos))
        return 0

    print(informe(r))

    if a.json:
        os.makedirs(os.path.dirname(os.path.abspath(a.json)), exist_ok=True)
        with open(a.json, "w", encoding="utf-8") as fh:
            json.dump(r, fh, ensure_ascii=False, indent=2)
        print("\njson=%s" % a.json)
    return 0


if __name__ == "__main__":
    sys.exit(main())
