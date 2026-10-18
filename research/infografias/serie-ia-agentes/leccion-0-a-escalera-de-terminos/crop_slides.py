#!/usr/bin/env python3
"""crop_slides.py — recorta full.png en slides 1080x1350."""
from PIL import Image
import sys, pathlib
lec = pathlib.Path(__file__).parent
nombres = ["slide-1-portada","slide-2-que-es","slide-3-como-funciona","slide-4-confusion",
           "slide-5-ejemplo","slide-6-dato","slide-7-cierre"]
im = Image.open(lec / "full.png")
W, H = im.size
n = min(H // 1350, len(nombres))
for i in range(n):
    im.crop((0, i*1350, W, (i+1)*1350)).save(lec / "slides" / (nombres[i] + ".png"))
print(f"crops ok: {n} slides de {W}x{H}")
