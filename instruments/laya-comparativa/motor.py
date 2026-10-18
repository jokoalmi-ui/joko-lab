#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motor de LAYA-COMPARATIVA: métricas + backends.

Métricas implementadas: accuracy, Brier, ECE (por bins), sesgo de confianza,
latencia P50/P95. Backends: stub (offline), ollama (local), laya (local, PyPI
'laya'), jev (nube, requiere token).

No escribe nada fuera de esta carpeta. No imprime credenciales.
"""
import json
import math
import os
import re
import subprocess
import time
import urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------------------------------
# MÉTRICAS
# --------------------------------------------------------------------------


def ece(pares, n_bins=5):
    """Expected Calibration Error sobre pares (p, y_bool).

    ECE = suma_bins (n_bin/N) * |acc_bin - conf_bin|
    Con n pequeno el ECE es ruidoso: se reporta SIEMPRE a 5 bins y junto a Brier.
    """
    if not pares:
        return None
    bins = [[] for _ in range(n_bins)]
    for p, y in pares:
        p = min(max(float(p), 0.0), 1.0)
        i = min(int(p * n_bins), n_bins - 1)
        bins[i].append((p, y))
    n = len(pares)
    total = 0.0
    for b in bins:
        if not b:
            continue
        conf = sum(p for p, _ in b) / len(b)
        acc = sum(1 for _, y in b if y) / len(b)
        total += (len(b) / n) * abs(acc - conf)
    return total


def ece_vendor(pares, bins=15):
    """ECE con la MISMA convencion que laya.common.ece_score (bins=15 por defecto).

    El paquete define: edges = linspace(0,1,bins+1); bin i selecciona
    (conf >= lo si i==0 si no conf > lo) & (conf <= hi); peso sel.mean().
    Se replica aqui para poder comparar con las cifras publicadas por el
    proveedor (ECE 0.213 / 0.175 / 0.081), que usan 15 bins.
    """
    if not pares:
        return None
    edges = [i / bins for i in range(bins + 1)]
    n = len(pares)
    e = 0.0
    for i in range(bins):
        lo, hi = edges[i], edges[i + 1]
        sel = [(p, y) for p, y in pares
               if ((p >= lo) if i == 0 else (p > lo)) and (p <= hi)]
        if sel:
            conf = sum(p for p, _ in sel) / len(sel)
            acc = sum(1 for _, y in sel if y) / len(sel)
            e += (len(sel) / n) * abs(acc - conf)
    return e


def brier(pares):
    if not pares:
        return None
    return sum((p - (1.0 if y else 0.0)) ** 2 for p, y in pares) / len(pares)


def accuracy(pares):
    if not pares:
        return None
    return sum(1 for p, y in pares if (p >= 0.5) == bool(y)) / len(pares)


def pct(xs, q):
    if not xs:
        return None
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(round(q * (len(xs) - 1))))]


def resumen(pares, latencias=None, n_bins=5):
    if not pares:
        return {"n": 0}
    conf = sum(p for p, _ in pares) / len(pares)
    acc = accuracy(pares)
    return {
        "n": len(pares),
        "accuracy": round(acc, 4),
        "brier": round(brier(pares), 4),
        "ece5": round(ece(pares, n_bins), 4),
        "ece15_proveedor": round(ece_vendor(pares, 15), 4),
        "conf_media": round(conf, 4),
        "sesgo_conf_menos_acierto": round(conf - acc, 4),
        "confiado_y_fallado": sum(1 for p, y in pares if p >= 0.8 and not y),
        "seguro_y_acertado": sum(1 for p, y in pares if p >= 0.8 and y),
        "p50_ms": round(pct(latencias, 0.50) * 1000, 1) if latencias else None,
        "p95_ms": round(pct(latencias, 0.95) * 1000, 1) if latencias else None,
    }


def selftest():
    """Verifica el motor de metricas contra calculos explicitos."""
    fallos = []
    cuenta = [0]

    def ok(cond, msg):
        cuenta[0] += 1
        if not cond:
            fallos.append(msg)

    # 1) ECE de un caso perfecto: 1.0 con acierto, 0.5 con 1 acierto y 1 fallo -> 0
    ok(ece([(1.0, True), (1.0, True), (0.5, True), (0.5, False)]) == 0.0,
       "ECE perfecto deberia ser 0")
    # 2) dos casos a p=0.5, ambos fallados -> desvio 0.5 con peso 1.0 -> 0.5
    ok(abs(ece([(0.5, False), (0.5, False)]) - 0.5) < 1e-9,
       "ECE de 2 fallos a p=0.5 deberia ser 0.5")
    # 3) todos aciertos a p=1.0 -> 0
    ok(ece([(1.0, True)] * 7) == 0.0, "ECE de todo acierto a p=1 deberia ser 0")
    # 4) todos a p=0.0 y todos fallados -> 0 (conf 0, acc 0)
    ok(ece([(0.0, False)] * 4) == 0.0, "ECE de p=0 y fallo deberia ser 0")
    # 5) Brier de p=0.5 -> 0.25
    ok(abs(brier([(0.5, True), (0.5, False)]) - 0.25) < 1e-9, "Brier de p=0.5 deberia ser 0.25")
    # 6) Brier perfecto -> 0
    ok(brier([(1.0, True), (0.0, False)]) == 0.0, "Brier perfecto deberia ser 0")
    # 7) accuracy con umbral 0.5: 0.51 acierta, 0.49 falla, 0.5 acierta -> 2/3
    ok(abs(accuracy([(0.51, True), (0.49, True), (0.5, True)]) - 2 / 3) < 1e-9,
       "accuracy deberia ser 2/3")
    # 8) percentiles
    ok(pct([1, 2, 3, 4, 5], 0.5) == 3, "p50 de 1..5 deberia ser 3")
    ok(pct([1, 2, 3, 4, 5], 0.95) == 5, "p95 de 1..5 deberia ser 5")
    # 9) sesgo: todo a 0.9 con la mitad fallada -> sesgo positivo
    r = resumen([(0.9, True), (0.9, False)])
    ok(r["sesgo_conf_menos_acierto"] == 0.4, "sesgo deberia ser 0.4")
    ok(r["confiado_y_fallado"] == 1, "deberia contar 1 confiado y fallado")
    # 10) caso vacio no revienta
    ok(resumen([]) == {"n": 0}, "resumen vacio deberia devolver n=0")
    # 11) ECE con la convencion del proveedor (15 bins)
    ok(ece_vendor([(1.0, True), (1.0, True), (0.5, True), (0.5, False)]) == 0.0,
       "ECE proveedor: caso perfecto deberia ser 0")
    ok(abs(ece_vendor([(0.5, False), (0.5, False)]) - 0.5) < 1e-9,
       "ECE proveedor: dos fallos a p=0.5 deberia ser 0.5")
    # 12) la clave nueva viaja en el resumen
    ok("ece15_proveedor" in resumen([(0.9, True)]), "resumen deberia incluir ece15_proveedor")
    return cuenta[0], fallos


# --------------------------------------------------------------------------
# BACKENDS
# --------------------------------------------------------------------------


class BackendError(Exception):
    pass


def backend_stub(caso, _opts):
    """Backend de prueba, SIN modelo: dice 'si' salvo en los casos trampa.

    No mira el gt. Sirve para verificar el arnes, nunca es un resultado.
    """
    p = 0.15 if caso["id"].startswith("trap") else 0.9
    return p, "stub"


def _primer_float(texto):
    m = re.search(r"(\d+(?:[.,]\d+)?)", texto)
    if not m:
        return None
    v = float(m.group(1).replace(",", "."))
    if v > 1.0:            # el modelo respondio en porcentaje o en escala 0-100
        v = v / 100.0
    return min(max(v, 0.0), 1.0)


def backend_ollama(caso, opts):
    modelo = opts.get("modelo_ollama", "ibm/granite4.2:8b-q4_K_M")
    texto = ""
    if caso.get("state"):
        texto = json.dumps(caso["state"], ensure_ascii=False)
    prompt = (
        "Eres un verificador de afirmaciones. Devuelve UNICAMENTE un objeto JSON "
        'de la forma {"p": <numero entre 0 y 1>} con la probabilidad de que la '
        "AFIRMACION sea verdadera. Ni explicaciones ni texto fuera del JSON.\n\n"
        f"{caso['instrucciones']}\n"
    )
    if texto:
        prompt += f"\nTEXTO DEL ESTADO:\n{texto}\n"
    esquema = {
        "type": "object",
        "properties": {"p": {"type": "number", "minimum": 0.0, "maximum": 1.0}},
        "required": ["p"],
    }
    carga = {
        "model": modelo, "prompt": prompt, "stream": False, "format": esquema,
        "options": {"temperature": 0.0, "seed": 42, "num_predict": 64,
                    "num_ctx": int(os.environ.get("LAYA_NUM_CTX", "8192"))},
    }
    req = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=json.dumps(carga).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    crudo = data.get("response", "")
    p = None
    try:                                     # camino preferente: JSON restringido
        v = json.loads(crudo).get("p")
        if v is not None:
            p = float(v)
    except Exception:
        pass
    if p is None:                            # respaldo: ultimo numero del texto
        encontrados = re.findall(r"-?\d+(?:[.,]\d+)?", crudo)
        if encontrados:
            p = float(encontrados[-1].replace(",", "."))
    if p is None:
        raise BackendError(f"respuesta sin probabilidad: {crudo[:80]!r}")
    return max(0.0, min(1.0, p)), modelo


def backend_laya(caso, opts):
    """Laya local (paquete PyPI 'laya', upstream, NO MLX). Requiere instalar el paquete."""
    try:
        import laya  # noqa
    except ImportError as exc:
        raise BackendError("paquete 'laya' no instalado (pip install laya)") from exc

    modo = opts.get("checkpoint", "router")
    cache = opts.setdefault("_cache_laya", {})

    if modo == "router":
        from laya import Router
        if "obj" not in cache:
            cache["obj"] = Router(preload=True)
        agente = cache["obj"]
        meta = "router(auto)"
    else:
        if modo not in cache:
            cache[modo] = laya.load("convaiinnovations/laya",
                                    subfolder=None if modo == "english" else modo)
        agente = cache[modo]
        meta = f"laya[{modo}]"

    preguntas = {"afirmacion": {"type": "noul", "instructions": caso["instrucciones"]}}
    res = agente.predict(caso.get("state") or {}, preguntas)
    resp = res["answers"]["afirmacion"]
    if "noul" not in resp:
        raise BackendError(f"respuesta sin 'noul': {list(resp)}")
    etiqueta = meta
    if isinstance(res.get("routing"), dict):
        etiqueta = f"{meta}->{res['routing'].get('model')}"
    return float(resp["noul"]), etiqueta


def _leer_env_jev():
    ruta = os.path.expanduser("~/.config/joko-lab/jev.env")
    if not os.path.exists(ruta):
        raise BackendError(
            f"falta {ruta} (chmod 600). El token lo aporta el usuario; nunca por el chat.")
    env = {}
    with open(ruta, "r", encoding="utf-8") as fh:
        for linea in fh:
            linea = linea.strip()
            if not linea or linea.startswith("#") or "=" not in linea:
                continue
            k, v = linea.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def backend_jev(caso, opts):
    """Jev (TypeSafe) via Cloudflare Workers AI. Requiere token en ~/.config/joko-lab/jev.env."""
    env = _leer_env_jev()
    token = env.get("CLOUDFLARE_API_TOKEN")
    cuenta = env.get("CLOUDFLARE_ACCOUNT_ID")
    if not token or not cuenta:
        raise BackendError("jev.env sin CLOUDFLARE_API_TOKEN o CLOUDFLARE_ACCOUNT_ID")
    modelo = opts.get("modelo_jev", "@cf/typesafe/jev")
    carga = {
        "model": modelo,
        "input": {
            "state": caso.get("state") or {},
            "questions": {"afirmacion": {"type": "noul",
                                         "instructions": caso["instrucciones"]}},
        },
    }
    url = f"https://api.cloudflare.com/client/v4/accounts/{cuenta}/ai/run/{modelo}"
    req = urllib.request.Request(url, data=json.dumps(carga).encode("utf-8"),
                                 headers={"Content-Type": "application/json",
                                          "Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    try:
        p = float(data["result"]["answers"]["afirmacion"]["noul"])
    except (KeyError, TypeError) as exc:
        raise BackendError(f"respuesta inesperada de Jev: {json.dumps(data)[:200]}") from exc
    return p, f"jev:{data.get('result',{}).get('model','?')}"


BACKENDS = {
    "stub": backend_stub,
    "ollama": backend_ollama,
    "laya": backend_laya,
    "jev": backend_jev,
}


# --------------------------------------------------------------------------
# EJECUCIÓN
# --------------------------------------------------------------------------


def cargar_casos(nombre="casos_noul.json"):
    with open(os.path.join(AQUI, nombre), "r", encoding="utf-8") as fh:
        return json.load(fh)


def ejecutar(casos, backend, opts, verbose=False):
    fn = BACKENDS[backend]
    registros, pares, latencias = [], [], []
    for c in casos:
        t0 = time.perf_counter()
        try:
            p, etiqueta = fn(c, opts)
            error = None
        except BackendError as exc:
            p, etiqueta, error = None, None, str(exc)
        dt = time.perf_counter() - t0
        reg = {"id": c["id"], "bloque": c["bloque"], "subtipo": c.get("subtipo"),
               "gt": c["gt"], "p": p,
               "motor": etiqueta, "error": error, "ms": round(dt * 1000, 1)}
        registros.append(reg)
        if p is not None:
            pares.append((p, c["gt"]))
            latencias.append(dt)
        if verbose:
            print(f"  {c['id']:9s} gt={str(c['gt']):5s} p={p} {etiqueta or ''}"
                  f"{' ERROR: ' + error if error else ''}")
    errores = [r for r in registros if r["p"] is None]
    return {
        "registros": registros,
        "metricas": resumen(pares, latencias),
        "errores": len(errores),
        "primer_error": errores[0]["error"] if errores else None,
    }


def _normalizar_choice(c):
    """Acepta las dos formas de caso choice usadas en el rig (opciones | criteria)."""
    preg = c.get("pregunta") or c.get("instrucciones") or ""
    if c.get("opciones"):
        ops = [str(o) for o in c["opciones"]]
    else:
        ops = [str(o) for o in (c.get("criteria") or {}).keys()]
    return preg, ops


def backend_ollama_choice(caso, opts):
    """Primitiva choice contra un modelo local: elegir 1 de N (salida restringida)."""
    modelo = opts.get("modelo_ollama", "ibm/granite4.2:8b-q4_K_M")
    preg, ops = _normalizar_choice(caso)
    if not ops:
        raise BackendError("caso choice sin opciones")
    if caso.get("state"):
        texto = json.dumps(caso["state"], ensure_ascii=False)
    else:
        texto = "(sin texto de apoyo)"
    prompt = (
        "Elige UNA sola opcion: la correcta. Devuelve UNICAMENTE un objeto JSON "
        'de la forma {"etiqueta": "<opcion>"}, con el texto EXACTO de una de las '
        "opciones permitidas. Ni explicaciones ni texto fuera del JSON.\n\n"
        f"Pregunta: {preg}\n"
        f"Opciones permitidas: {json.dumps(ops, ensure_ascii=False)}\n\n"
        f"TEXTO DEL ESTADO:\n{texto}\n"
    )
    carga = {
        "model": modelo, "prompt": prompt, "stream": False,
        "format": {"type": "object",
                   "properties": {"etiqueta": {"type": "string", "enum": ops}},
                   "required": ["etiqueta"]},
        "options": {"temperature": 0.0, "seed": 42, "num_predict": 48,
                    "num_ctx": int(os.environ.get("LAYA_NUM_CTX", "8192"))},
    }
    req = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=json.dumps(carga).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    crudo = data.get("response", "")
    etiqueta = None
    try:
        etiqueta = json.loads(crudo).get("etiqueta")
    except Exception:
        pass
    if etiqueta is None:                     # respaldo: buscar una opcion literal
        for op in ops:
            if op and op in crudo:
                etiqueta = op
                break
    if etiqueta is None:
        raise BackendError(f"respuesta sin etiqueta: {crudo[:80]!r}")
    return etiqueta, modelo


BACKENDS_CHOICE = {"ollama": backend_ollama_choice}


def ejecutar_choice(casos, backend, opts, verbose=False):
    """Bloque choice: elegir 1 de N. Solo backends que devuelven etiqueta."""
    aciertos, registros, latencias = 0, [], []
    router = None
    if backend == "laya":
        from laya import Router  # noqa  (solo si se pide; requiere pesos)
        router = Router(preload=True)
    elif backend not in BACKENDS_CHOICE:
        raise BackendError(f"el backend '{backend}' no implementa choice")
    for c in casos:
        preg, ops = _normalizar_choice(c)
        t0 = time.perf_counter()
        if backend == "laya":
            preguntas = {"etiqueta": {"type": "choice", "instructions": preg,
                                      "criteria": {op: op for op in ops}}}
            res = router.predict(c.get("state") or {}, preguntas)
            elegida = res["answers"]["etiqueta"]["choice"]
            conf = res["answers"]["etiqueta"].get("confidence")
        else:
            elegida, _ = BACKENDS_CHOICE[backend](c, opts)
            conf = None
        dt = time.perf_counter() - t0
        acierto = elegida == c["gt"]
        aciertos += int(acierto)
        latencias.append(dt)
        registros.append({"id": c["id"], "gt": c["gt"], "elegida": elegida,
                          "acierto": acierto, "ms": round(dt * 1000, 1),
                          "conf": conf})
        if verbose:
            print(f"  {c['id']:9s} gt={c['gt']:22s} elegida={elegida}")
    return {"registros": registros, "metricas": {
        "n": len(casos), "accuracy": round(aciertos / max(len(casos), 1), 4),
        "p50_ms": round(pct(latencias, 0.5) * 1000, 1) if latencias else None,
        "p95_ms": round(pct(latencias, 0.95) * 1000, 1) if latencias else None}}


def info_entorno():
    info = {"python": None, "laya": None, "torch": None, "gpu": None,
            "ollama": None, "disco_home": None, "fecha": None}
    try:
        info["python"] = subprocess.run(["python3", "-V"], capture_output=True,
                                        text=True, timeout=10).stdout.strip()
    except Exception:
        pass
    import importlib.util
    for mod in ("laya", "torch"):
        info[mod] = importlib.util.find_spec(mod) is not None
    try:
        info["gpu"] = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.used,memory.total,utilization.gpu",
             "--format=csv,noheader,nounits"], capture_output=True, text=True,
            timeout=15).stdout.strip()
    except Exception:
        pass
    try:
        with urllib.request.urlopen("http://localhost:11434/api/tags", timeout=8) as r:
            info["ollama"] = [m["name"] for m in json.loads(r.read())["models"]]
    except Exception:
        pass
    try:
        info["disco_home"] = subprocess.run(["df", "-h", os.path.expanduser("~")],
                                            capture_output=True, text=True,
                                            timeout=10).stdout.strip().splitlines()[-1]
    except Exception:
        pass
    try:
        info["fecha"] = subprocess.run(["date"], capture_output=True, text=True,
                                       timeout=10).stdout.strip()
    except Exception:
        pass
    return info
