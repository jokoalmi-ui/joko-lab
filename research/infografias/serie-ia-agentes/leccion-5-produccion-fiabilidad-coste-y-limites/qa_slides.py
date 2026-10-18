#!/usr/bin/env python3
"""qa_slides.py — control objetivo del carrusel 5: tamano, fondo, margenes + PDF."""
from PIL import Image
import pathlib

lec = pathlib.Path(__file__).parent
CREMA = (245, 239, 230)
def cerca(px, ref, tol=12):
    return all(abs(px[i] - ref[i]) <= tol for i in range(3))

for f in sorted((lec / "slides").glob("*.png")):
    im = Image.open(f).convert("RGB")
    W, H = im.size
    px = im.load()
    esquinas = [px[2, 2], px[W - 3, 2], px[2, H - 3], px[W - 3, H - 3]]
    fondo_ok = all(cerca(e, CREMA) for e in esquinas)
    borde = 0
    for x in range(0, W, 7):
        for y in (5, H - 6):
            if not cerca(px[x, y], CREMA, 20):
                borde += 1
    for y in range(0, H, 7):
        for x in (5, W - 6):
            if not cerca(px[x, y], CREMA, 20):
                borde += 1
    print(f"{f.name}: {W}x{H} fondo_ok={fondo_ok} px_borde_no_crema={borde}")

ims = [Image.open(p).convert("RGB") for p in sorted((lec / "slides").glob("*.png"))]
pdf = lec / "carrusel-leccion-5.pdf"
ims[0].save(pdf, save_all=True, append_images=ims[1:], resolution=150.0)
print("PDF:", pdf, pdf.stat().st_size, "bytes,", len(ims), "paginas")
