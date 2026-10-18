#!/usr/bin/env python3
"""medicion-tamano.py — Prueba para la Leccion 0-B (serie IA y agentes).

Pregunta que responde: para los usos tipicos de un LLM (clasificar, extraer,
calcular), cuanto importa el TAMANO del modelo?

Tres tamanos, MISMA API (LM Studio), temperatura 0:
  2,6B  lfm2.5-2.6b        (razona antes de contestar)
  8B    granite-4.1-8b
  35B   qwen3.6-35b-a3b-mtp (MoE, razona antes de contestar)

Nota: los modelos 8B y 35B NO cargan si el VLM (glm-4.6v-flash) sigue
residente; hay que descargarlo antes (ver cabecera del JSON).

Se mide: aciertos por tarea (objetivos, sin juicio) y segundos por respuesta.
Registro crudo -> medicion-tamano-<fecha>.json
"""
import json, time, pathlib, datetime, re, urllib.request, urllib.error, sys

API = "http://localhost:1234/api/v0/chat/completions"
MODELOS = [
    ("2,6B", "lfm2.5-2.6b", {"clas": 900, "extrae": 1600, "calc": 1600}),
    ("8B", "granite-4.1-8b", {"clas": 400, "extrae": 200, "calc": 800}),
    ("35B", "qwen3.6-35b-a3b-mtp", {"clas": 2000, "extrae": 900, "calc": 3000}),
]

RESENAS = [
    "Pedí dos tazas y llegaron en 48 horas, muy bien embaladas.",
    "El paquete tardó once días y nadie contestó a mis correos.",
    "La cafetera va perfecta y costaba menos que en la tienda del barrio.",
    "Me cobraron dos veces y sigo esperando la devolución.",
    "El molinillo es justo el que buscaba, llegó sin un rasguño.",
]
ESPERADO_CLAS = ["POSITIVA", "NEGATIVA", "POSITIVA", "NEGATIVA", "POSITIVA"]

PROMPT_CLAS = (
    "Clasifica cada resena como POSITIVA o NEGATIVA segun la opinion del cliente.\n"
    "Responde SOLO con una linea por resena, en este formato: 1=POSITIVA\n\n"
    + "\n".join(f"{i+1}. {r}" for i, r in enumerate(RESENAS))
)

FACTURA = (
    "Factura F-2026-0918.\n"
    "Cliente: Erandio Hosteleria SL.\n"
    "Articulo: 4 x Cafetera Compacta a 89,50 EUR la unidad.\n"
    "Transporte: 12,00 EUR.\n"
    "Descuento aplicado: 10,00 EUR.\n"
)
PROMPT_EXTRAE = (
    FACTURA + "\nDime UNICAMENTE el importe del transporte en euros, sin texto adicional."
)
ESPERADO_EXTRAE = ["12,00", "12.00", "12"]

PROMPT_CALCULA = (
    FACTURA + "\nCalcula el total de la factura en euros (4 x 89,50 - 10,00 + 12,00). "
    "Responde solo con el numero."
)
ESPERADO_CALCULA = ["360", "360,00", "360.00"]  # 4 x 89,50 - 10,00 + 12,00 = 358 - 10 + 12 = 360,00

def num(s):
    if s is None:
        return None
    m = re.search(r"-?\d[\d.,]*", str(s))
    if not m:
        return None
    t = m.group(0)
    if "," in t:
        t = t.replace(".", "").replace(",", ".")
    else:
        t = t.replace(",", "")
    try:
        return float(t)
    except ValueError:
        return None

def igual(a, esperados):
    v = num(a)
    if v is None:
        return False
    return any(num(e) is not None and abs(v - num(e)) < 0.011 for e in esperados)

def llama(modelo, prompt, max_tokens):
    body = json.dumps({
        "model": modelo, "temperature": 0, "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}],
    }).encode()
    req = urllib.request.Request(API, data=body, headers={"Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=1800) as r:
        d = json.loads(r.read().decode())
    dt = round(time.time() - t0, 1)
    msg = d["choices"][0]["message"]
    return (msg.get("content") or "").strip(), dt, d["choices"][0].get("finish_reason"), \
           (msg.get("reasoning_content") or msg.get("reasoning") or "")

def etiquetas(txt):
    out = []
    for i in range(len(RESENAS)):
        m = re.search(rf"^\s*\**{i+1}\**\s*[=:.\-]\s*\**\s*([A-Za-zÁÉÍÓÚáéíóúñÑ]+)", txt, re.M)
        out.append((m.group(1).upper() if m else "")[:9])
    return out

res = {
    "fecha": datetime.date.today().isoformat(),
    "hora_inicio": datetime.datetime.now().strftime("%H:%M:%S"),
    "api": "LM Studio (localhost:1234), temperature 0",
    "aviso": "Los modelos 8B y 35B solo cargan tras descargar glm-4.6v-flash (VRAM).",
    "prueba": {"clasificar": f"5 resenas -> POSITIVA/NEGATIVA (esperado: {','.join(ESPERADO_CLAS)})",
               "extraer": "importe del transporte de una factura (esperado 12,00 EUR)",
               "calcular": "4 x 89,50 - 10,00 + 12,00 (esperado 370,00 EUR)"},
    "modelos": [],
}
for etiqueta, mid, mx in MODELOS:
    fila = {"tamano": etiqueta, "modelo": mid}
    print(f"--- {etiqueta} ({mid}) ---", flush=True)

    txt, dt, fr, rz = llama(mid, PROMPT_CLAS, mx["clas"])
    ets = etiquetas(txt)
    aciertos = sum(1 for e, x in zip(ESPERADO_CLAS, ets) if e == x)
    fila["clasificar"] = {"aciertos": aciertos, "n": len(RESENAS), "segundos": dt,
                          "finish_reason": fr, "salida": txt[:900], "razonamiento": rz[:400]}
    print(f"  clasificar {aciertos}/5 en {dt}s (fin={fr}) -> {ets}", flush=True)

    txt2, dt2, fr2, rz2 = llama(mid, PROMPT_EXTRAE, mx["extrae"])
    ok2 = igual(txt2, ESPERADO_EXTRAE)
    fila["extraer"] = {"acierto": ok2, "segundos": dt2, "finish_reason": fr2,
                       "salida": txt2[:600], "razonamiento": rz2[:400]}
    print(f"  extraer {'OK' if ok2 else 'FALLO'} en {dt2}s (fin={fr2}) -> {txt2[:80]!r}", flush=True)

    txt3, dt3, fr3, rz3 = llama(mid, PROMPT_CALCULA, mx["calc"])
    ok3 = igual(txt3, ESPERADO_CALCULA)
    fila["calcular"] = {"acierto": ok3, "segundos": dt3, "finish_reason": fr3,
                        "salida": txt3[:900], "razonamiento": rz3[:400]}
    print(f"  calcular {'OK' if ok3 else 'FALLO'} en {dt3}s (fin={fr3}) -> {txt3[:80]!r}", flush=True)

    fila["segundos_total"] = round(dt + dt2 + dt3, 1)
    res["modelos"].append(fila)
    # volcado incremental: si algo corta, lo medido no se pierde
    tmp = pathlib.Path(__file__).parent / "medicion-tamano-parcial.json"
    tmp.write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")

res["hora_fin"] = datetime.datetime.now().strftime("%H:%M:%S")
out = pathlib.Path(__file__).parent / f"medicion-tamano-{datetime.date.today().strftime('%Y%m%d')}.json"
out.write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
print("JSON:", out)
print("\nRESUMEN")
for f in res["modelos"]:
    print(f"{f['tamano']:>5s} | clasificar {f['clasificar']['aciertos']}/5 | "
          f"extraer {'si' if f['extraer']['acierto'] else 'no'} | "
          f"calcular {'si' if f['calcular']['acierto'] else 'no'} | "
          f"{f['segundos_total']}s")
