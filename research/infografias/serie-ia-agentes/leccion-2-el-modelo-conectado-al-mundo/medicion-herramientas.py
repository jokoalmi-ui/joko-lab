#!/usr/bin/env python3
"""Medicion de la Leccion 2 (serie IA y agentes): el modelo conectado al mundo.

Eje: separar CALCULAR de LLAMAR. La misma tanda de preguntas al mismo modelo,
temperatura 0, tres condiciones:

  A) los datos en el prompt, SIN herramienta -> se le pide el numero
     (si el modelo calcula por su cuenta, ese numero se compara con el real)
  B) los mismos datos + la funcion declarada -> se le pide la LLAMADA
     (el script ejecuta la funcion sobre los datos reales: el numero sale de codigo)
  C) control de temperatura: B con temperatura alta

Metricas (objetivas, automatizables):
  - A: % de respuestas cuyo numero coincide EXACTAMENTE con el calculado en Python.
  - B/C: % de llamadas bien formadas (JSON parseable con 'herramienta' + 'argumentos')
    y % con argumentos CORRECTOS (la ejecucion devuelve el resultado esperado).

Los datos NO son del lab: son un caso de ejemplo reproducible embebido en el script.
Guarda JSON crudo con las respuestas LITERALES, fecha y modelo.

Uso:
  python3 medicion-herramientas.py --modelo ibm/granite4.2:8b-q4_K_M --backend ollama --json \
      --salida medicion-herramientas-<fecha>.json
"""
import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime

# --- datos de ejemplo (reproducibles, NO del lab): gastos de un negocio pequeno
GASTOS = [
    {"id": 1, "mes": "marzo", "concepto": "luz", "importe": 412.80},
    {"id": 2, "mes": "marzo", "concepto": "material", "importe": 1290.45},
    {"id": 3, "mes": "marzo", "concepto": "luz", "importe": 388.15},
    {"id": 4, "mes": "abril", "concepto": "material", "importe": 2740.90},
    {"id": 5, "mes": "abril", "concepto": "luz", "importe": 501.30},
    {"id": 6, "mes": "abril", "concepto": "transporte", "importe": 175.60},
    {"id": 7, "mes": "mayo", "concepto": "material", "importe": 3120.75},
    {"id": 8, "mes": "mayo", "concepto": "transporte", "importe": 240.20},
]


# --- la funcion real: el "mundo" que el modelo NO tiene
def sumar_gastos(filtro: str, valor: str = None) -> dict:
    """Suma los importes filtrando por 'mes' o 'concepto'."""
    if filtro not in ("mes", "concepto"):
        raise ValueError("filtro debe ser 'mes' o 'concepto'")
    sel = [g for g in GASTOS if g[filtro] == valor]
    total = round(sum(g["importe"] for g in sel), 2)
    return {"filtro": filtro, "valor": valor, "n": len(sel), "total": total}


# --- calculo de referencia, hecho en Python (lo que se espera de cada pregunta)
def _total(filtro, valor):
    return sumar_gastos(filtro, valor)["total"]


PREGUNTAS = [
    {"q": "Cuanto suman los gastos de luz en total?", "filtro": "concepto", "valor": "luz"},
    {"q": "Cuanto se gasto en total en abril?", "filtro": "mes", "valor": "abril"},
    {"q": "Cuanto suman los gastos de material?", "filtro": "concepto", "valor": "material"},
    {"q": "Cuanto se gasto en total en marzo?", "filtro": "mes", "valor": "marzo"},
    {"q": "Cuanto suman los gastos de transporte?", "filtro": "concepto", "valor": "transporte"},
    {"q": "Cuanto se gasto en total en mayo?", "filtro": "mes", "valor": "mayo"},
]
for p in PREGUNTAS:
    p["esperado"] = _total(p["filtro"], p["valor"])

TABLA = "\n".join(
    f"| {g['id']} | {g['mes']} | {g['concepto']} | {g['importe']:.2f} |" for g in GASTOS
)

INSTRUCCION_A = (
    "Estos son los gastos de un negocio pequeno:\n\n"
    "| id | mes | concepto | importe |\n|---|---|---|---|\n" + TABLA + "\n\n"
)

INSTRUCCION_B = INSTRUCCION_A + (
    "Tienes disponible esta funcion:\n"
    'sumar_gastos(filtro, valor) -> {"total": numero}\n'
    "  filtro: \"mes\" o \"concepto\"\n"
    "  valor: el mes (marzo/abril/mayo) o el concepto (luz/material/transporte)\n"
    "No calcules tu: si la pregunta necesita una suma, pide la funcion.\n"
    "Responde SOLO con JSON valido, sin texto antes ni despues, con esta forma:\n"
    '{"herramienta": "sumar_gastos", "argumentos": {"filtro": "...", "valor": "..."}}\n\n'
    "Pregunta: <PREGUNTA>"
)

INSTRUCCION_A_FULL = INSTRUCCION_A + "Pregunta: <PREGUNTA>\nResponde SOLO con el numero, sin texto."


INSTRUCCION_S = (
    "Eres un asistente util. Responde en espanol, breve y directo.\n\n"
    "Pregunta: <PREGUNTA>\n"
    "Responde SOLO con el numero, sin texto."
)


def post_json(url, payload, timeout=300):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def llamar(backend, host, modelo, prompt, temperature):
    if backend == "ollama":
        payload = {"model": modelo, "messages": [{"role": "user", "content": prompt}],
                   "stream": False,
                   "options": {"temperature": temperature, "seed": 42, "num_ctx": 8192}}
        t0 = time.time()
        resp = post_json(host + "/api/chat", payload)
        return (resp.get("message", {}).get("content") or ""), time.time() - t0
    payload = {"model": modelo, "messages": [{"role": "user", "content": prompt}],
               "temperature": temperature, "seed": 42, "stream": False}
    t0 = time.time()
    resp = post_json(host + "/v1/chat/completions", payload)
    msg = (resp.get("choices") or [{}])[0].get("message", {})
    return (msg.get("content") or ""), time.time() - t0


def quitar_vallas(txt):
    t = txt.strip()
    t = re.sub(r"^```[a-zA-Z]*\s*", "", t)
    t = re.sub(r"\s*```$", "", t)
    return t.strip()


def primer_json(txt):
    """Devuelve el primer objeto JSON parseable del texto, o None."""
    for cand in (txt, quitar_vallas(txt)):
        try:
            return json.loads(cand)
        except Exception:
            pass
    m = re.search(r"\{.*\}", txt, re.S)
    if m:
        try:
            return json.loads(m.group(0))
        except Exception:
            return None
    return None


def numero_de(txt):
    """Ultimo numero con decimales o entero del texto (para la condicion A)."""
    nums = re.findall(r"-?\d+(?:[.,]\d+)?", txt.replace(" ", ""))
    if not nums:
        return None
    try:
        return round(float(nums[-1].replace(",", ".")), 2)
    except Exception:
        return None


def ejecutar_llamada(obj):
    """Ejecuta la llamada del modelo contra la funcion real. Devuelve (ok, detalle)."""
    if not isinstance(obj, dict):
        return False, "no es un objeto JSON"
    if obj.get("herramienta") != "sumar_gastos":
        return False, f"herramienta inesperada: {obj.get('herramienta')!r}"
    args = obj.get("argumentos")
    if not isinstance(args, dict):
        return False, "sin 'argumentos' como objeto"
    try:
        r = sumar_gastos(args.get("filtro"), args.get("valor"))
    except Exception as e:
        return False, f"ejecucion fallida: {e}"
    return True, r


class FilasParciales(list):
    """Lista que vuelca el JSON parcial en cada append.

    Motivo medido: una ejecucion que agota el tiempo de espera mataba el proceso y
    se perdian las 24 llamadas. Con esto, el fichero .parcial siempre tiene el
    estado y un corte no obliga a repetir lo ya medido.
    """

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
            "modelo": args.modelo, "backend": args.backend, "host": host}
    filas = FilasParciales(args.salida, meta)

    for p in PREGUNTAS:
        # --- A: los datos en el prompt, sin herramienta
        prompt_a = INSTRUCCION_A_FULL.replace("<PREGUNTA>", p["q"])
        try:
            txt, seg = llamar(args.backend, host, args.modelo, prompt_a, 0.0)
            num = numero_de(txt)
            filas.append({"condicion": "A_sin_herramienta", "pregunta": p["q"],
                          "esperado": p["esperado"], "obtenido": num,
                          "exacto": num == p["esperado"], "segundos": round(seg, 1),
                          "respuesta_literal": txt})
            print(f"A | {p['q'][:38]:38s} esperado={p['esperado']:>9.2f} obtenido={num} exacto={num == p['esperado']}")
        except urllib.error.URLError as e:
            filas.append({"condicion": "A_sin_herramienta", "pregunta": p["q"], "error": str(e)})
            print("A | ERROR:", e)

    for p in PREGUNTAS:
        # --- S: la misma pregunta SIN los datos y SIN herramienta
        prompt_s = INSTRUCCION_S.replace("<PREGUNTA>", p["q"])
        try:
            txt, seg = llamar(args.backend, host, args.modelo, prompt_s, 0.0)
            num = numero_de(txt)
            no_da_numero = num is None
            filas.append({"condicion": "S_sin_datos", "pregunta": p["q"], "esperado": p["esperado"],
                          "obtenido": num, "exacto": num == p["esperado"], "no_da_numero": no_da_numero,
                          "segundos": round(seg, 1), "respuesta_literal": txt})
            print(f"S | {p['q'][:38]:38s} esperado={p['esperado']:>9.2f} obtenido={num} exacto={num == p['esperado']} sin_numero={no_da_numero}")
        except urllib.error.URLError as e:
            filas.append({"condicion": "S_sin_datos", "pregunta": p["q"], "error": str(e)})
            print("S | ERROR:", e)

    for temp, nombre in ((0.0, "B_con_herramienta"), (0.8, "C_con_herramienta_temp_alta")):
        for p in PREGUNTAS:
            prompt_b = INSTRUCCION_B.replace("<PREGUNTA>", p["q"])
            try:
                txt, seg = llamar(args.backend, host, args.modelo, prompt_b, temp)
                obj = primer_json(txt)
                ok, detalle = ejecutar_llamada(obj) if obj is not None else (False, "sin JSON")
                bien_formada = isinstance(obj, dict) and "herramienta" in obj and "argumentos" in obj
                correcta = isinstance(detalle, dict) and detalle.get("total") == p["esperado"]
                filas.append({"condicion": nombre, "pregunta": p["q"], "temperature": temp,
                              "esperado": p["esperado"], "llamada": obj, "bien_formada": bien_formada,
                              "ejecutada_ok": ok, "resultado": detalle, "correcta": correcta,
                              "segundos": round(seg, 1), "respuesta_literal": txt})
                print(f"{nombre[0]} | {p['q'][:32]:32s} bien_formada={bien_formada} correcta={correcta} -> {detalle if not isinstance(detalle, dict) else detalle.get('total')}")
            except urllib.error.URLError as e:
                filas.append({"condicion": nombre, "pregunta": p["q"], "error": str(e)})
                print(f"{nombre[0]} | ERROR:", e)

    resumen = {}
    for cond in ("A_sin_herramienta", "S_sin_datos", "B_con_herramienta", "C_con_herramienta_temp_alta"):
        sub = [f for f in filas if f.get("condicion") == cond and "respuesta_literal" in f]
        if cond in ("A_sin_herramienta", "S_sin_datos"):
            resumen[cond] = {"n": len(sub),
                             "numeros_exactos": sum(1 for f in sub if f.get("exacto")),
                             "sin_numero": sum(1 for f in sub if f.get("no_da_numero"))}
        else:
            resumen[cond] = {"n": len(sub),
                             "bien_formadas": sum(1 for f in sub if f.get("bien_formada")),
                             "correctas": sum(1 for f in sub if f.get("correcta"))}

    salida = {"fecha": datetime.now().astimezone().isoformat(timespec="seconds"),
              "modelo": args.modelo, "backend": args.backend, "host": host,
              "n_preguntas": len(PREGUNTAS), "datos": GASTOS,
              "esperados": {p["q"]: p["esperado"] for p in PREGUNTAS},
              "resumen": resumen, "filas": filas}
    print("\nRESUMEN:", json.dumps(resumen, ensure_ascii=False))
    if args.json:
        print(json.dumps(salida, ensure_ascii=False, indent=2))
    if args.salida:
        with open(args.salida, "w", encoding="utf-8") as fh:
            json.dump(salida, fh, ensure_ascii=False, indent=2)
        print("escrito:", args.salida)
    return 0


if __name__ == "__main__":
    sys.exit(main())
