#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Chequeo GRUESO por visión local (GLM-4.6V-flash, API directa LM Studio).
NO dictamina contraste (07-oct). Solo preguntas atómicas:
texto inventado en el fondo / botella visible / artefactos."""
import base64, io, json, urllib.request
from PIL import Image

PNG = "/home/jokoalmi/joko-lab/research/infografias/perfume-del-dia-20261012/perfume_del_dia_v5_aquafortis.png"
im = Image.open(PNG).convert("RGB")
if max(im.size) > 1024:
    e = 1024 / max(im.size)
    im = im.resize((int(im.width * e), int(im.height * e)), Image.LANCZOS)
buf = io.BytesIO(); im.save(buf, format="JPEG", quality=88)
b64 = base64.b64encode(buf.getvalue()).decode()
print(f"imagen enviada: {im.size}  jpeg {len(buf.getvalue())//1024} KB")

prompt = ("Responde SOLO con lo que ves, en 4 lineas numeradas, sin rodeos:\n"
          "1) ¿Aparece algun texto, letra o palabra escrita en el FONDO de la imagen (fuera del texto propio "
          "de la ficha)? Si si, transcribelo.\n"
          "2) ¿Se ve una botella de perfume? ¿Cuantas?\n"
          "3) ¿Hay algun objeto raro, deforme, mano o cara extrana?\n"
          "4) ¿Que se ve en la esquina superior derecha de la imagen?")

body = json.dumps({
    "model": "glm-4.6v-flash",
    "messages": [{"role": "user", "content": [
        {"type": "text", "text": prompt},
        {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64," + b64}},
    ]}],
    "temperature": 0.2, "max_tokens": 4000,
}).encode()

req = urllib.request.Request("http://localhost:1234/api/v0/chat/completions", data=body,
                            headers={"Content-Type": "application/json"})
with urllib.request.urlopen(req, timeout=240) as r:
    d = json.load(r)
msg = d["choices"][0]["message"]
print("--- content ---")
print(msg.get("content") or "(VACIO -> se agoto razonando; NO es un NO)")
print("--- usage ---")
print(json.dumps(d.get("usage", {}), ensure_ascii=False))
