#!/usr/bin/env python3
"""
analiza_charts.py — Analiza visualmente los PNG de cierre diario con GLM 4.6V
local (LM Studio) y devuelve el patrón según el método de Dani
(ascendente / descendente / banda lateral / L-swing).

Uso: python3 analiza_charts.py WDC,MRVL,FSLY,MCHP
Salida: texto por ticker con el patrón detectado por el modelo de visión.
Creado: 06-ago-2026 (EXP-002).
"""

import base64
import json
import os
import sys
import urllib.request

GRAFICAS = os.path.expanduser("~/joko-lab/lpa/experiments/bolsa/graficas")
URL = "http://localhost:1234/api/v0/chat/completions"
MODEL = "glm-4.6v-flash"

PROMPT = (
    "Analiza esta grafica de cierre diario de una accion (USD). Responde MUY breve: "
    "1) Patron segun la forma: ASCENDENTE (diente de sierra al alza), DESCENDENTE "
    "(caida libre), BANDA LATERAL (plana sin direccion), o L-SWING (caida seguida "
    "de remontada en forma de L). 2) El precio ultimo esta remontando desde el minimo "
    "o sigue cayendo? 3) Direccion general del tramo mas reciente (ultimos ~20 puntos). "
    "Formato: PATRON: X | ULTIMO TRAMO: sube/baja/plano | OBSERVACION: 1 frase."
)


def analizar(ticker):
    path = os.path.join(GRAFICAS, f"{ticker}.png")
    with open(path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": PROMPT},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}},
                ],
            }
        ],
        "temperature": 0.1,
        "max_tokens": 1200,
    }
    req = urllib.request.Request(
        URL, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=180) as r:
        data = json.loads(r.read().decode())
    try:
        content = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as e:
        return f"ERROR parse: {e} — RAW: {json.dumps(data)[:400]}"
    if not content or not content.strip():
        # Modelo con razonamiento: el análisis puede estar en reasoning_content
        reasoning = (data["choices"][0].get("message") or {}).get("reasoning_content") or ""
        if reasoning.strip():
            return f"[razonamiento GLM] {reasoning.strip()}"
        return f"CONTENT VACIO — RAW: {json.dumps(data)[:600]}"
    return content


def main():
    tickers = sys.argv[1].split(",") if len(sys.argv) > 1 else ["WDC", "MRVL", "FSLY", "MCHP"]
    for t in tickers:
        try:
            print(f"=== {t} ===")
            print(analizar(t))
            print()
        except Exception as e:  # noqa: BLE001
            print(f"{t}: ERROR {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
