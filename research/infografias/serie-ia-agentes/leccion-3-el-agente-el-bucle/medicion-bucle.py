#!/usr/bin/env python3
"""Medicion de la Leccion 3 (serie IA y agentes): el agente — el bucle.

Metrica del subnivel 3.5 del plan: PASOS POR TAREA, % DE TAREAS COMPLETADAS y
coste (tokens) POR TAREA RESUELTA.

Eje: separar el BUCLE de la HERRAMIENTA. Mismas 6 tareas al mismo modelo,
temperatura 0, cuatro condiciones:

  A) UNA VUELTA, SIN HERRAMIENTAS  -> se le pide la respuesta final directamente
     (no tiene los datos: no puede saberla)
  D) BUCLE DE SOLO PENSAMIENTO, SIN HERRAMIENTAS -> puede pensar hasta 4 turnos,
     pero no puede actuar sobre nada (bucle sin entorno = CoT largo)
  B) BUCLE + HERRAMIENTAS (ReAct)  -> piensa, actua, observa y repite hasta 6 pasos
  C) CONTROL: B con temperatura alta (0.8)

Por que estas cuatro: la que sostiene la tesis de la pieza es una RESTA. Si
"pensar mas" bastara, D resolveria tanto como B; si bastara con preguntar una
vez, A resolveria. La condicion que aisla la afirmacion "el bucle CIERRA tareas
porque actua sobre el entorno" es (B - D) y (B - A), no el acierto bruto.

Datos: tabla de pedidos reproducible embebida en el script (NO son del lab).
Guardado INCREMENTAL (.parcial) y REANUDABLE: al arrancar lee el parcial y salta
las filas ya hechas.

Uso:
  python3 medicion-bucle.py --modelo ibm/granite4.2:8b-q4_K_M --backend ollama \
      --json --salida medicion-bucle-<fecha>.json
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
    t["equivalencias"] = []          # numeros alternativos que cuentan como acierto
# T1 y T4 admiten tambien el importe con la parte entera sola; T5 admite el signo inverso
T1 = TAREAS[0]; T4 = TAREAS[3]; T5 = TAREAS[4]
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
    """Devuelve el primer objeto JSON **de tipo diccionario**, o None.

    Enmienda medida en el humo: en la condicion A el modelo contesta con un
    numero suelto ("507.3") y `json.loads` lo convertia en float -> el bucle
    petaba con TypeError al buscar "fin". Solo valen diccionarios.
    """
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
    """(resuelta, motivo, ok_num, ok_txt). Mira el numero esperado y, si aplica, el texto.

    Devuelve los dos aciertos por separado: en el humo, T1 en condicion B acerto el
    nombre ("Marta") pero no dio el importe. La metrica principal sigue siendo estricta
    (hacen falta las dos cosas si la tarea pide las dos), pero el desglose evita que un
    fallo de formato se lea como fallo de contenido.
    """
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
CABECERA_PENSAR = (
    "Resuelve la tarea razonando. NO tienes herramientas ni acceso a datos externos.\n"
    "Responde SIEMPRE con un unico JSON, sin texto fuera de el:\n"
    "  para seguir pensando: {\"pensar\": \"...\"}\n"
    "  para terminar:        {\"fin\": \"<respuesta corta con el numero>\"}\n"
    "En \"fin\" incluye SIEMPRE el numero pedido y, si la tarea pregunta por un nombre, tambien el nombre.\n\n"
)
CABECERA_DIRECTA = ("Responde a la tarea con el valor final.\n"
                    "Responde SOLO con el numero o el valor pedido, sin texto.\n\n")

MAX_PASOS_B, MAX_PASOS_D = 6, 4


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


def correr_tarea(backend, host, modelo, tarea, condicion, temperatura, max_pasos,
                 herramientas, cabecera):
    """Devuelve la fila de resultado de UNA tarea en UNA condicion."""
    mensajes = [{"role": "user", "content": cabecera + "TAREA: " + tarea["tarea"]}]
    pasos, llamadas, tokens_p, tokens_g, segs = 0, [], 0, 0, 0.0
    respuesta_final, traza, ultima = None, [], None
    fallos_json, declaro_fin = 0, False
    for _ in range(max_pasos):
        txt, seg, tp, tg = llamar(backend, host, modelo, mensajes, temperatura)
        pasos += 1
        ultima = txt
        tokens_p += tp
        tokens_g += tg
        segs += seg
        obj = primer_json(txt)
        traza.append({"paso": pasos, "respuesta": txt, "segundos": round(seg, 1)})
        if obj is None:
            fallos_json += 1
            if fallos_json >= 2:
                break
            mensajes.append({"role": "assistant", "content": txt})
            mensajes.append({"role": "user", "content":
                             "JSON invalido. Responde SOLO con el JSON, sin texto fuera."})
            continue
        if "fin" in obj:
            respuesta_final = str(obj.get("fin"))
            declaro_fin = True
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
        # objeto JSON con forma no reconocida
        mensajes.append({"role": "assistant", "content": txt})
        mensajes.append({"role": "user", "content":
                         "Formato no reconocido. Usa {\"accion\": ...} o {\"fin\": ...}."})
    # Enmienda medida en el humo: en la condicion A (una vuelta, sin protocolo) el
    # modelo contesta el numero suelto, no {"fin": ...}. Se juzga el texto literal
    # para no castigar a la condicion por un formato que no se le ha pedido. El
    # campo `cierre` deja constancia de si declaro fin o si se agoto el presupuesto.
    cierre = "fin" if declaro_fin else ("json_invalido" if fallos_json >= 2 else "agotado")
    if respuesta_final is None:
        respuesta_final = ultima
    resuelta, motivo, acierto_num, acierto_txt = juzgar(tarea, respuesta_final or "")
    return {"condicion": condicion, "tarea_id": tarea["id"], "tarea": tarea["tarea"],
            "esperado_num": tarea["num"], "esperado_txt": tarea["txt"],
            "temperature": temperatura, "pasos": pasos, "pasos_min_ref": tarea["pasos_min"],
            "herramientas_llamadas": len(llamadas), "llamadas": llamadas,
            "respuesta_final": respuesta_final, "cierre": cierre, "declaro_fin": declaro_fin,
            "resuelta": resuelta, "motivo": motivo,
            "acierto_numero": acierto_num, "acierto_texto": acierto_txt,
            "tokens_prompt": tokens_p, "tokens_generados": tokens_g,
            "tokens_total": tokens_p + tokens_g, "segundos": round(segs, 1),
            "traza": traza}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--modelo", required=True)
    ap.add_argument("--backend", choices=["ollama", "lmstudio"], default="ollama")
    ap.add_argument("--host", default=None)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--salida", default=None)
    args = ap.parse_args()

    host = args.host or ("http://127.0.0.1:11434" if args.backend == "ollama" else "http://127.0.0.1:1234")
    meta = {"fecha": datetime.now().astimezone().isoformat(timespec="seconds"),
            "modelo": args.modelo, "backend": args.backend, "host": host,
            "condiciones": {
                "A_una_vuelta_sin_herramientas": "una sola llamada, sin herramientas, se pide el valor final",
                "D_bucle_sin_herramientas": "hasta %d turnos de pensamiento, sin herramientas" % MAX_PASOS_D,
                "B_bucle_con_herramientas": "ReAct: piensa/actua/observa hasta %d pasos" % MAX_PASOS_B,
                "C_control_temp_alta": "igual que B con temperatura 0.8",
            },
            "enmiendas": []}
    filas = Parcial(args.salida, meta)

    # reanudacion: saltar lo ya hecho
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

    plan = []
    for t in TAREAS:
        plan.append((t, "A_una_vuelta_sin_herramientas", 0.0, 1, False, CABECERA_DIRECTA))
    for t in TAREAS:
        plan.append((t, "D_bucle_sin_herramientas", 0.0, MAX_PASOS_D, False, CABECERA_PENSAR))
    for t in TAREAS:
        plan.append((t, "B_bucle_con_herramientas", 0.0, MAX_PASOS_B, True, CABECERA_AGENTE))
    for t in TAREAS:
        plan.append((t, "C_control_temp_alta", 0.8, MAX_PASOS_B, True, CABECERA_AGENTE))

    for tarea, cond, temp, maxp, herr, cab in plan:
        k = "%s|%s" % (cond, tarea["id"])
        if k in hechas:
            continue
        try:
            fila = correr_tarea(args.backend, host, args.modelo, tarea, cond, temp, maxp, herr, cab)
        except urllib.error.URLError as e:
            fila = {"condicion": cond, "tarea_id": tarea["id"], "error": str(e)}
        filas.append(fila)
        print("%-30s %s pasos=%s llamadas=%s resuelta=%s tokens=%s (%.0fs)" % (
            cond, tarea["id"], fila.get("pasos"), fila.get("herramientas_llamadas"),
            fila.get("resuelta"), fila.get("tokens_total"), fila.get("segundos") or 0))
        sys.stdout.flush()

    resumen = {}
    for cond in ("A_una_vuelta_sin_herramientas", "D_bucle_sin_herramientas",
                 "B_bucle_con_herramientas", "C_control_temp_alta"):
        sub = [f for f in filas if f.get("condicion") == cond and "resuelta" in f]
        if not sub:
            continue
        resueltas = [f for f in sub if f["resuelta"]]
        con_fin = [f for f in sub if f.get("respuesta_final")]
        resumen[cond] = {
            "n": len(sub),
            "resueltas": len(resueltas),
            "aciertos_numero": sum(1 for f in sub if f.get("acierto_numero")),
            "aciertos_texto": sum(1 for f in sub if f.get("acierto_texto") is True),
            "resueltas_con_fin_declarado": sum(1 for f in resueltas if f.get("declaro_fin")),
            "con_fin_declarado": sum(1 for f in sub if f.get("declaro_fin")),
            "cierres": {c: sum(1 for f in sub if f.get("cierre") == c)
                        for c in ("fin", "agotado", "json_invalido")},
            "pct_resueltas": round(100.0 * len(resueltas) / len(sub), 1),
            "sin_respuesta_final": len(sub) - len(con_fin),
            "pasos_medios": round(sum(f["pasos"] for f in sub) / len(sub), 2),
            "pasos_medios_resueltas": round(sum(f["pasos"] for f in resueltas) / len(resueltas), 2) if resueltas else None,
            "herramientas_por_tarea": round(sum(f["herramientas_llamadas"] for f in sub) / len(sub), 2),
            "tokens_total": sum(f["tokens_total"] for f in sub),
            "tokens_por_tarea_resuelta": round(sum(f["tokens_total"] for f in sub) / len(resueltas), 0) if resueltas else None,
            "segundos_totales": round(sum(f["segundos"] for f in sub), 1),
        }

    salida = {"fecha": datetime.now().astimezone().isoformat(timespec="seconds"),
              "modelo": args.modelo, "backend": args.backend, "host": host,
              "datos": PEDIDOS, "herramientas": sorted(HERRAMIENTAS),
              "tareas": [{k: v for k, v in t.items() if k != "equivalencias"} for t in TAREAS],
              "max_pasos": {"B": MAX_PASOS_B, "D": MAX_PASOS_D},
              "condiciones": meta["condiciones"], "enmiendas": meta["enmiendas"],
              "resumen": resumen, "filas": filas}
    print("\nRESUMEN:", json.dumps(resumen, ensure_ascii=False, indent=2))
    if args.json:
        print(json.dumps(salida, ensure_ascii=False, indent=2))
    if args.salida:
        with open(args.salida, "w", encoding="utf-8") as fh:
            json.dump(salida, fh, ensure_ascii=False, indent=2)
        print("escrito:", args.salida)
    return 0


if __name__ == "__main__":
    sys.exit(main())
