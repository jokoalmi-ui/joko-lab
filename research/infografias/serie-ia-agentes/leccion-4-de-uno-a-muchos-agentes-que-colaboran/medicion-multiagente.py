#!/usr/bin/env python3
"""Medicion de la Leccion 4 (serie IA y agentes): de uno a muchos.

Metrica del subnivel 4.5 del plan: COSTE (tokens) Y LATENCIA MULTI-AGENTE vs UN
SOLO AGENTE, NUMERO DE REINTENTOS y MEJORA DE PRECISION AL ANADIR UN CRITICO.

Eje: los agentes NO mejoran por sumar agentes, y el critic... hay que medirlo.
Mismas 6 tareas, mismo mundo, mismo modelo y temperatura 0 que la Leccion 3
(comparabilidad): dos condiciones.

  A) UN AGENTE: un solo agente con herramientas (ReAct) -> respuesta final.
  B) MULTI-AGENTE: A + un CRITICO independiente que comprueba el dato con las
     mismas herramientas y, si marca "incorrecto", el agente recibe el motivo y
     REINTENTA una vez. B INCLUYE el coste y la latencia de A: es A + critico +
     (reintento), y asi se declara.

La resta que sostiene la afirmacion de la pieza es (B - A): que se gana en
aciertos y que se paga en tokens, segundos y llamadas al modelo. Si el critico
acierta igual que A, el eje es el COSTE, no la precision, y se enuncia asi.

CRITICO: el veredicto del critico NO se juzga aqui contra la verdad de Python
(eso seria regalarle la respuesta); se registra su veredicto y su motivo
LITERALES. La precision de cada condicion se mide aparte con `juzgar()`.

Datos: tabla de pedidos reproducible embebida en el script (NO son del lab).
Guardado INCREMENTAL (.parcial) y REANUDABLE.

Uso:
  python3 medicion-multiagente.py --modelo ibm/granite4.2:8b-q4_K_M \
      --backend ollama --json --salida medicion-multiagente-<fecha>.json
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime

# --- el "mundo": pedidos de una tienda pequena (reproducible, NO del lab)
PEDIDOS = [
    {"id": 1, "mes": "enero", "cliente": "Ana", "importe": 118.40},
    {"id": 2, "mes": "enero", "cliente": "Luis", "importe": 342.10},
    {"id": 3, "mes": "febrero", "cliente": "Ana", "importe": 91.75},
    {"id": 4, "mes": "febrero", "cliente": "Marta", "importe": 507.30},
    {"id": 5, "mes": "marzo", "cliente": "Luis", "importe": 226.90},
    {"id": 6, "mes": "marzo", "cliente": "Marta", "importe": 468.55},
    {"id": 7, "mes": "marzo", "cliente": "Ana", "importe": 154.20},
    {"id": 8, "mes": "abril", "cliente": "Luis", "importe": 389.95},
]
CAMPOS = ("mes", "cliente")


# --- herramientas reales: el entorno que el modelo no tiene
def listar():
    return {"pedidos": [dict(p) for p in PEDIDOS],
            "total": round(sum(p["importe"] for p in PEDIDOS), 2)}


def buscar(campo, valor):
    if campo not in CAMPOS:
        raise ValueError("campo debe ser 'mes' o 'cliente'")
    sel = [dict(p) for p in PEDIDOS if p[campo] == valor]
    return {"pedidos": sel, "total": round(sum(p["importe"] for p in sel), 2)}


def sumar(campo, valor):
    return {"total": buscar(campo, valor)["total"]}


def detalle(id):
    for p in PEDIDOS:
        if p["id"] == id:
            return dict(p)
    raise ValueError("id inexistente")


HERRAMIENTAS = {
    "listar": (listar, {}),
    "buscar": (buscar, {"campo": "mes|cliente", "valor": "string"}),
    "sumar": (sumar, {"campo": "mes|cliente", "valor": "string"}),
    "detalle": (detalle, {"id": "int"}),
}


# --- calculo de referencia en Python: lo que se espera de cada tarea
def _max_cliente():
    tot = {c: round(sum(p["importe"] for p in PEDIDOS if p["cliente"] == c), 2)
           for c in sorted({p["cliente"] for p in PEDIDOS})}
    c = max(tot, key=lambda k: tot[k])
    return c, tot[c]


def _pct_pedido4():
    tot = round(sum(p["importe"] for p in PEDIDOS), 2)
    return round(detalle(4)["importe"] / tot * 100, 1)


TAREAS = [
    {"id": "T1", "tarea": "Cual es el pedido con el importe mas alto y de que cliente es?",
     "num": 507.30, "txt": "marta", "pasos_min": 1},
    {"id": "T2", "tarea": "Cuanto suman los pedidos de Ana en total?",
     "num": 364.35, "txt": None, "pasos_min": 1},
    {"id": "T3", "tarea": "Cual fue el pedido mas caro de marzo y cuanto importaba?",
     "num": 468.55, "txt": None, "pasos_min": 1},
    {"id": "T4", "tarea": "Que cliente ha gastado mas en total y cuanto?",
     "num": _max_cliente()[1], "txt": _max_cliente()[0].lower(), "pasos_min": 3},
    {"id": "T5", "tarea": "Cuanta diferencia hay entre el total de febrero y el de abril?",
     "num": round(507.30 + 91.75 - 389.95, 2), "txt": None, "pasos_min": 2},
    {"id": "T6", "tarea": "Que porcentaje del total de todos los pedidos representa el pedido 4? Redondea a 1 decimal.",
     "num": _pct_pedido4(), "txt": None, "pasos_min": 2},
]
for t in TAREAS:
    t["equivalencias"] = []
T1 = TAREAS[0]; T5 = TAREAS[4]
T1["equivalencias"] = [507.3]
T5["equivalencias"] = [abs(T5["num"])]


def post_json(url, payload, timeout=600):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def llamar(backend, host, modelo, mensajes, temperature):
    """Devuelve (texto, segundos, tokens_prompt, tokens_generados)."""
    if backend == "ollama":
        payload = {"model": modelo, "messages": mensajes, "stream": False,
                   "options": {"temperature": temperature, "seed": 42, "num_ctx": 8192}}
        t0 = time.time()
        resp = post_json(host + "/api/chat", payload)
        return (resp.get("message", {}).get("content") or "", time.time() - t0,
                resp.get("prompt_eval_count") or 0, resp.get("eval_count") or 0)
    payload = {"model": modelo, "messages": mensajes, "temperature": temperature,
               "seed": 42, "stream": False}
    t0 = time.time()
    resp = post_json(host + "/v1/chat/completions", payload)
    msg = (resp.get("choices") or [{}])[0].get("message", {})
    uso = resp.get("usage") or {}
    return (msg.get("content") or "", time.time() - t0,
            uso.get("prompt_tokens") or 0, uso.get("completion_tokens") or 0)


def quitar_vallas(txt):
    t = txt.strip()
    t = re.sub(r"^```[a-zA-Z]*\s*", "", t)
    t = re.sub(r"\s*```$", "", t)
    return t.strip()


def primer_json(txt):
    """Primer objeto JSON de tipo diccionario, o None (un numero suelto no vale)."""
    for cand in (txt, quitar_vallas(txt)):
        try:
            o = json.loads(cand)
            if isinstance(o, dict):
                return o
        except Exception:
            pass
    m = re.search(r"\{.*\}", txt, re.S)
    if m:
        try:
            o = json.loads(m.group(0))
            return o if isinstance(o, dict) else None
        except Exception:
            return None
    return None


def numeros(txt):
    if not txt:
        return []
    out = []
    for n in re.findall(r"-?\d+(?:[.,]\d+)?", txt.replace(" ", "")):
        try:
            out.append(round(float(n.replace(",", ".")), 2))
        except Exception:
            pass
    return out


def juzgar(tarea, respuesta):
    """(resuelta, motivo, ok_num, ok_txt) contra la verdad calculada en Python."""
    nums = numeros(respuesta)
    ok_num = any(abs(n - tarea["num"]) <= 0.011 for n in nums) or \
        any(abs(n - e) <= 0.011 for e in tarea["equivalencias"] for n in nums)
    ok_txt = None
    if tarea["txt"]:
        ok_txt = tarea["txt"] in (respuesta or "").lower()
    if ok_num and ok_txt is not False:
        return True, ("numero+texto" if tarea["txt"] else "numero"), ok_num, ok_txt
    if ok_num and ok_txt is False:
        return False, "numero si, nombre no", ok_num, ok_txt
    if ok_txt and not ok_num:
        return False, "nombre si, numero no", ok_num, ok_txt
    return False, "no coincide", ok_num, ok_txt


class Parcial(list):
    """Vuelca el JSON parcial en cada append (una interrupcion no pierde la tanda)."""

    def __init__(self, ruta, meta):
        super().__init__()
        self.ruta = ruta
        self.meta = meta

    def append(self, x):
        super().append(x)
        if self.ruta:
            try:
                with open(self.ruta + ".parcial", "w", encoding="utf-8") as fh:
                    json.dump({**self.meta, "filas": list(self)}, fh, ensure_ascii=False, indent=2)
            except Exception as e:
                print("[aviso] no se pudo volcar el parcial:", e)
        return None


def clave(fila):
    return "%s|%s" % (fila.get("condicion"), fila.get("tarea_id"))


# --- protocolos
CABECERA_AGENTE = (
    "Eres un agente que trabaja en un bucle: piensas, actua y observas.\n"
    "Tienes estas herramientas:\n"
    "- listar() -> {\"pedidos\": [{\"id\",\"mes\",\"cliente\",\"importe\"}], \"total\": numero}\n"
    "- buscar(campo, valor) -> {\"pedidos\": [...], \"total\": numero}  (campo: \"mes\" o \"cliente\")\n"
    "- sumar(campo, valor) -> {\"total\": numero}\n"
    "- detalle(id) -> {\"id\",\"mes\",\"cliente\",\"importe\"}\n\n"
    "Responde SIEMPRE con un unico JSON, sin texto fuera de el:\n"
    "  para usar una herramienta: {\"accion\": \"<herramienta>\", \"argumentos\": {...}}\n"
    "  para terminar:              {\"fin\": \"<respuesta corta con el numero>\"}\n"
    "No inventes datos: si no los tienes, pide la herramienta.\n"
    "En \"fin\" incluye SIEMPRE el numero pedido y, si la tarea pregunta por un nombre, tambien el nombre.\n\n"
)
CABECERA_CRITICO = (
    "Eres un REVISOR independiente. Otro agente ha respondido a una tarea y tu decides\n"
    "si su respuesta es correcta. NO te fies de lo que dice: comprueba el dato real con\n"
    "estas herramientas:\n"
    "- listar() -> {\"pedidos\": [{\"id\",\"mes\",\"cliente\",\"importe\"}], \"total\": numero}\n"
    "- buscar(campo, valor) -> {\"pedidos\": [...], \"total\": numero}  (campo: \"mes\" o \"cliente\")\n"
    "- sumar(campo, valor) -> {\"total\": numero}\n"
    "- detalle(id) -> {\"id\",\"mes\",\"cliente\",\"importe\"}\n\n"
    "Responde SIEMPRE con un unico JSON, sin texto fuera de el:\n"
    "  para consultar: {\"accion\": \"<herramienta>\", \"argumentos\": {...}}\n"
    "  para juzgar:    {\"veredicto\": \"ok\"|\"incorrecto\", \"motivo\": \"<una frase>\"}\n\n"
)
MAX_PASOS_A, MAX_PASOS_CRITICO, MAX_PASOS_REVISION = 6, 3, 3


def ejecutar(nombre, args):
    if nombre not in HERRAMIENTAS:
        return {"error": "herramienta desconocida: %s" % nombre}
    fn = HERRAMIENTAS[nombre][0]
    if not isinstance(args, dict):
        return {"error": "argumentos deben ser un objeto JSON"}
    try:
        return fn(**args)
    except TypeError as e:
        return {"error": "argumentos invalidos: %s" % e}
    except Exception as e:
        return {"error": "ejecucion fallida: %s" % e}


def bucle(backend, host, modelo, mensajes, temperatura, max_pasos, herramientas, termina):
    """Bucle piensa/actua/observa GENERICO.

    termina: claves del JSON que cierran el turno (["fin"] para el agente,
    ["veredicto"] para el critico). Devuelve un dict con el JSON final, el texto
    de la ultima respuesta, pasos, tokens, segundos, traza y herramientas usadas.
    """
    pasos, tokens_p, tokens_g, segs = 0, 0, 0, 0.0
    llamadas, traza, final, ultimo = [], [], None, None
    cierre, fallos_json = "agotado", 0
    for _ in range(max_pasos):
        txt, seg, tp, tg = llamar(backend, host, modelo, mensajes, temperatura)
        pasos += 1
        ultimo = txt
        tokens_p += tp
        tokens_g += tg
        segs += seg
        traza.append({"paso": pasos, "respuesta": txt, "segundos": round(seg, 1)})
        obj = primer_json(txt)
        if obj is None:
            fallos_json += 1
            if fallos_json >= 2:
                cierre = "json_invalido"
                break
            mensajes.append({"role": "assistant", "content": txt})
            mensajes.append({"role": "user", "content":
                             "JSON invalido. Responde SOLO con el JSON, sin texto fuera."})
            continue
        if any(k in obj for k in termina):
            final, cierre = obj, "termino"
            break
        if "accion" in obj and herramientas:
            nombre = obj.get("accion")
            res = ejecutar(nombre, obj.get("argumentos"))
            llamadas.append({"herramienta": nombre, "argumentos": obj.get("argumentos"),
                             "resultado": res})
            mensajes.append({"role": "assistant", "content": txt})
            mensajes.append({"role": "user", "content": "OBSERVACION: " + json.dumps(res, ensure_ascii=False)})
            continue
        if "pensar" in obj and not herramientas:
            mensajes.append({"role": "assistant", "content": txt})
            mensajes.append({"role": "user", "content": "Sigue pensando o da la respuesta final con {\"fin\": ...}."})
            continue
        if herramientas and "pensar" in obj:
            mensajes.append({"role": "assistant", "content": txt})
            mensajes.append({"role": "user", "content":
                             "No puedes pensar y quedarte ahi: usa una herramienta con {\"accion\": ...} o termina con {\"fin\": ...}."})
            continue
        mensajes.append({"role": "assistant", "content": txt})
        mensajes.append({"role": "user", "content":
                         "Formato no reconocido. Usa %s." % " o ".join(
                             '{"%s": ...}' % k for k in termina)})
    return {"final": final, "ultimo": ultimo, "pasos": pasos, "cierre": cierre,
            "tokens_prompt": tokens_p, "tokens_generados": tokens_g,
            "tokens_total": tokens_p + tokens_g, "segundos": round(segs, 1),
            "herramientas_llamadas": len(llamadas), "llamadas": llamadas, "traza": traza}


def respuesta_de(r, clave_final):
    if r["final"] and clave_final in r["final"]:
        return str(r["final"][clave_final])
    return r["ultimo"]


def correr_agente(backend, host, modelo, tarea, temperatura, extra=""):
    """Condicion A: un solo agente con herramientas, una respuesta final."""
    mensajes = [{"role": "user", "content": CABECERA_AGENTE + "TAREA: " + tarea["tarea"] + extra}]
    r = bucle(backend, host, modelo, mensajes, temperatura, MAX_PASOS_A, True, ("fin",))
    rf = respuesta_de(r, "fin")
    resuelta, motivo, ok_num, ok_txt = juzgar(tarea, rf or "")
    return {"condicion": "A_un_agente", "tarea_id": tarea["id"], "tarea": tarea["tarea"],
            "esperado_num": tarea["num"], "esperado_txt": tarea["txt"], "temperature": temperatura,
            "pasos": r["pasos"], "cierre": r["cierre"], "llamadas": r["llamadas"],
            "herramientas_llamadas": r["herramientas_llamadas"],
            "respuesta_final": rf, "resuelta": resuelta, "motivo": motivo,
            "acierto_numero": ok_num, "acierto_texto": ok_txt,
            "tokens_prompt": r["tokens_prompt"], "tokens_generados": r["tokens_generados"],
            "tokens_total": r["tokens_total"], "segundos": r["segundos"], "traza": r["traza"]}


def correr_critico(backend, host, modelo, tarea, respuesta, temperatura):
    """Critico independiente: comprueba con las herramientas y juzga."""
    cuerpo = ("TAREA: " + tarea["tarea"] + "\n"
              "RESPUESTA DEL AGENTE: " + str(respuesta) + "\n"
              "Comprueba el dato real y juzga.")
    mensajes = [{"role": "user", "content": CABECERA_CRITICO + cuerpo}]
    r = bucle(backend, host, modelo, mensajes, temperatura, MAX_PASOS_CRITICO, True, ("veredicto",))
    ver = ""
    motivo = ""
    if r["final"]:
        ver = str(r["final"].get("veredicto", "")).strip().lower()
        motivo = str(r["final"].get("motivo", "")).strip()
    return {"veredicto": ver, "motivo": motivo, "infraccion": ver not in ("ok", "correcto", "correcta"),
            "pasos": r["pasos"], "cierre": r["cierre"], "llamadas": r["llamadas"],
            "herramientas_llamadas": r["herramientas_llamadas"],
            "tokens_prompt": r["tokens_prompt"], "tokens_generados": r["tokens_generados"],
            "tokens_total": r["tokens_total"], "segundos": r["segundos"], "traza": r["traza"]}


def correr_multi(backend, host, modelo, tarea, temperatura, fila_a):
    """Condicion B: A + critico + (si el critico discrepa) UN reintento del agente.

    B INCLUYE el coste y la latencia de A. Los tokens y los segundos que se
    publican en B son A + critico + reintento, y la resta (B - A) es lo que
    cuesta el critico.
    """
    respuesta_a = fila_a.get("respuesta_final")
    trazas = {"A": fila_a.get("traza", []), "critico": [], "revision": []}
    crit = correr_critico(backend, host, modelo, tarea, respuesta_a, temperatura)
    trazas["critico"] = crit["traza"]
    pasos = fila_a["pasos"] + crit["pasos"]
    llamadas = len(fila_a["llamadas"]) + len(crit["llamadas"])
    tp = fila_a["tokens_prompt"] + crit["tokens_prompt"]
    tg = fila_a["tokens_generados"] + crit["tokens_generados"]
    segs = fila_a["segundos"] + crit["segundos"]

    revision = None
    respuesta_final, cierre = respuesta_a, fila_a.get("cierre")
    if crit["infraccion"]:
        extra = ("\nTu respuesta anterior fue: " + str(respuesta_a) +
                 "\nUn revisor independiente dice que esta MAL: " + (crit["motivo"] or "(sin motivo)") +
                 "\nVuelve a comprobar el dato con las herramientas y da la respuesta final corregida.\n")
        r = correr_agente(backend, host, modelo, tarea, temperatura, extra=extra)
        revision = r
        trazas["revision"] = r["traza"]
        pasos += r["pasos"]
        llamadas += len(r["llamadas"])
        tp += r["tokens_prompt"]
        tg += r["tokens_generados"]
        segs += r["segundos"]
        respuesta_final, cierre = r["respuesta_final"], r["cierre"]

    resuelta, motivo, ok_num, ok_txt = juzgar(tarea, respuesta_final or "")
    cambio = (respuesta_final or "").strip() != (respuesta_a or "").strip()
    return {"condicion": "B_multi_con_critico", "tarea_id": tarea["id"], "tarea": tarea["tarea"],
            "esperado_num": tarea["num"], "esperado_txt": tarea["txt"], "temperature": temperatura,
            "pasos": pasos, "cierre": cierre, "llamadas": (fila_a["llamadas"] +
                                                           crit["llamadas"] +
                                                           (revision["llamadas"] if revision else [])),
            "herramientas_llamadas": (fila_a["herramientas_llamadas"] + crit["herramientas_llamadas"] +
                                      (revision["herramientas_llamadas"] if revision else 0)),
            "respuesta_antes_del_critico": respuesta_a, "respuesta_final": respuesta_final,
            "veredicto_critico": crit["veredicto"], "motivo_critico": crit["motivo"],
            "reintentos": 1 if revision else 0, "cambio_tras_critico": cambio,
            "resuelta": resuelta, "motivo": motivo,
            "acierto_numero": ok_num, "acierto_texto": ok_txt,
            "tokens_prompt": tp, "tokens_generados": tg, "tokens_total": tp + tg,
            "segundos": round(segs, 1), "trazas": trazas}


def resumen_cond(filas, cond):
    sub = [f for f in filas if f.get("condicion") == cond and "resuelta" in f]
    if not sub:
        return {}
    resueltas = [f for f in sub if f["resuelta"]]
    return {"n": len(sub), "resueltas": len(resueltas),
            "pct_resueltas": round(100.0 * len(resueltas) / len(sub), 1),
            "tokens_total": sum(f["tokens_total"] for f in sub),
            "tokens_por_tarea": round(sum(f["tokens_total"] for f in sub) / len(sub), 0),
            "segundos_totales": round(sum(f["segundos"] for f in sub), 1),
            "segundos_por_tarea": round(sum(f["segundos"] for f in sub) / len(sub), 1),
            "llamadas_modelo": sum(f["pasos"] for f in sub),
            "llamadas_por_tarea": round(sum(f["pasos"] for f in sub) / len(sub), 2),
            "herramientas_por_tarea": round(sum(f["herramientas_llamadas"] for f in sub) / len(sub), 2)}


def comparar(filas):
    """La resta que sostiene (o tumba) la afirmacion de la pieza: B - A."""
    A = {f["tarea_id"]: f for f in filas if f.get("condicion") == "A_un_agente" and "resuelta" in f}
    B = {f["tarea_id"]: f for f in filas if f.get("condicion") == "B_multi_con_critico" and "resuelta" in f}
    comunes = sorted(set(A) & set(B))
    rescates, estropeos = [], []
    for k in comunes:
        if not A[k]["resuelta"] and B[k]["resuelta"]:
            rescates.append(k)
        if A[k]["resuelta"] and not B[k]["resuelta"]:
            estropeos.append(k)
    tok_a = sum(A[k]["tokens_total"] for k in comunes)
    tok_b = sum(B[k]["tokens_total"] for k in comunes)
    seg_a = sum(A[k]["segundos"] for k in comunes)
    seg_b = sum(B[k]["segundos"] for k in comunes)
    reint = [k for k in comunes if B[k].get("reintentos")]
    util = [k for k in reint if not A[k]["resuelta"] and B[k]["resuelta"]]
    return {"n_tareas_comparables": len(comunes),
            "aciertos_A": sum(1 for k in comunes if A[k]["resuelta"]),
            "aciertos_B": sum(1 for k in comunes if B[k]["resuelta"]),
            "rescates_por_el_critico": rescates, "estropeos_por_el_critico": estropeos,
            "reintentos_disparados": len(reint), "reintentos_utiles": len(util),
            "reintentos_inutiles": len(reint) - len(util),
            "tokens_A": tok_a, "tokens_B": tok_b, "tokens_B_menos_A": tok_b - tok_a,
            "factor_tokens_B_sobre_A": round(tok_b / tok_a, 2) if tok_a else None,
            "segundos_A": round(seg_a, 1), "segundos_B": round(seg_b, 1),
            "segundos_B_menos_A": round(seg_b - seg_a, 1),
            "factor_segundos_B_sobre_A": round(seg_b / seg_a, 2) if seg_a else None,
            "llamadas_A": sum(A[k]["pasos"] for k in comunes),
            "llamadas_B": sum(B[k]["pasos"] for k in comunes)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--modelo", required=True)
    ap.add_argument("--backend", choices=["ollama", "lmstudio"], default="ollama")
    ap.add_argument("--host", default=None)
    ap.add_argument("--tareas", default=None, help="subconjunto, ej: T1,T3 (humo)")
    ap.add_argument("--temperatura", type=float, default=0.0)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--salida", default=None)
    args = ap.parse_args()

    host = args.host or ("http://127.0.0.1:11434" if args.backend == "ollama" else "http://127.0.0.1:1234")
    condiciones = {
        "A_un_agente": "un agente con herramientas (ReAct), hasta %d pasos" % MAX_PASOS_A,
        "B_multi_con_critico": ("A + critico independiente (hasta %d pasos, con herramientas) "
                                "y UN reintento del agente si el critico discrepa; B INCLUYE el coste de A"
                                % MAX_PASOS_CRITICO),
    }
    filas = Parcial(args.salida, {"fecha": datetime.now().astimezone().isoformat(timespec="seconds"),
                                  "modelo": args.modelo, "backend": args.backend, "host": host,
                                  "condiciones": condiciones})
    hechas = set()
    if args.salida and os.path.exists(args.salida + ".parcial"):
        try:
            with open(args.salida + ".parcial", encoding="utf-8") as fh:
                prev = json.load(fh)
            for f in prev.get("filas", []):
                if "resuelta" in f:
                    filas.append(f)
                    hechas.add(clave(f))
            print("[reanudado] filas ya hechas:", len(hechas))
        except Exception as e:
            print("[aviso] parcial ilegible, se empieza de cero:", e)

    sel = TAREAS if not args.tareas else [t for t in TAREAS if t["id"] in args.tareas.split(",")]
    resA = {f["tarea_id"]: f for f in filas
            if f.get("condicion") == "A_un_agente" and "resuelta" in f}
    for t in sel:
        ka, kb = "A_un_agente|" + t["id"], "B_multi_con_critico|" + t["id"]
        if ka not in hechas:
            try:
                fa = correr_agente(args.backend, host, args.modelo, t, args.temperatura)
            except urllib.error.URLError as e:
                fa = {"condicion": "A_un_agente", "tarea_id": t["id"], "error": str(e)}
            filas.append(fa)
            resA[t["id"]] = fa
            print("A_un_agente  %s pasos=%s resuelta=%s tokens=%s (%.0fs) -> %s" % (
                t["id"], fa.get("pasos"), fa.get("resuelta"), fa.get("tokens_total"),
                fa.get("segundos") or 0, str(fa.get("respuesta_final"))[:60]))
            sys.stdout.flush()
        if kb in hechas or t["id"] not in resA:
            continue
        try:
            fb = correr_multi(args.backend, host, args.modelo, t, args.temperatura, resA[t["id"]])
        except urllib.error.URLError as e:
            fb = {"condicion": "B_multi_con_critico", "tarea_id": t["id"], "error": str(e)}
        filas.append(fb)
        print("B_multi      %s pasos=%s veredicto=%s reintentos=%s resuelta=%s tokens=%s (%.0fs) -> %s" % (
            t["id"], fb.get("pasos"), fb.get("veredicto_critico"), fb.get("reintentos"),
            fb.get("resuelta"), fb.get("tokens_total"), fb.get("segundos") or 0,
            str(fb.get("respuesta_final"))[:60]))
        sys.stdout.flush()

    resumen = {"A_un_agente": resumen_cond(filas, "A_un_agente"),
               "B_multi_con_critico": resumen_cond(filas, "B_multi_con_critico")}
    comp = comparar(filas)
    salida = {"fecha": datetime.now().astimezone().isoformat(timespec="seconds"),
              "leccion": "L4 De uno a muchos: agentes que colaboran",
              "metrica_plan": ("coste y latencia multi-agente vs un solo agente; numero de "
                               "reintentos; mejora de precision al anadir un critico"),
              "modelo": args.modelo, "backend": args.backend, "host": host,
              "datos": PEDIDOS, "herramientas": sorted(HERRAMIENTAS),
              "tareas": [{k: v for k, v in t.items() if k != "equivalencias"} for t in TAREAS],
              "max_pasos": {"A": MAX_PASOS_A, "critico": MAX_PASOS_CRITICO, "revision": MAX_PASOS_REVISION},
              "condiciones": condiciones, "resumen": resumen, "comparativa_B_menos_A": comp,
              "filas": filas}
    print("\nRESUMEN:", json.dumps(resumen, ensure_ascii=False, indent=2))
    print("\nB - A:", json.dumps(comp, ensure_ascii=False, indent=2))
    if args.json:
        print(json.dumps(salida, ensure_ascii=False, indent=2))
    if args.salida:
        with open(args.salida, "w", encoding="utf-8") as fh:
            json.dump(salida, fh, ensure_ascii=False, indent=2)
        print("escrito:", args.salida)
    return 0


if __name__ == "__main__":
    sys.exit(main())
