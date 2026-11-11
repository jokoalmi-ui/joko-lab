#!/usr/bin/env python3
# Recorta la figura (botella) del packshot: fondo claro -> alfa 0.
# v2: umbral alto (la sombra suave de estudio es fondo) + relleno de huecos
# internos por flood-fill del fondo desde el marco del bbox.
import sys
from collections import deque
from PIL import Image

src, dst = sys.argv[1], sys.argv[2]
TH = int(sys.argv[3]) if len(sys.argv) > 3 else 70
im = Image.open(src).convert("RGBA")
W, H = im.size
px = im.load()

mask = bytearray(W * H)
for y in range(H):
    base = y * W
    for x in range(W):
        r, g, b, a = px[x, y]
        if a > 10 and (abs(255 - r) + abs(255 - g) + abs(255 - b)) > TH:
            mask[base + x] = 1

# componente conexa mayor = figura
seen = bytearray(W * H)
best = None
best_area = 0
for y0 in range(H):
    for x0 in range(W):
        i0 = y0 * W + x0
        if not mask[i0] or seen[i0]:
            continue
        dq = deque([(x0, y0)])
        seen[i0] = 1
        area = 0
        minx = maxx = x0
        miny = maxy = y0
        while dq:
            x, y = dq.popleft()
            area += 1
            if x < minx: minx = x
            if x > maxx: maxx = x
            if y < miny: miny = y
            if y > maxy: maxy = y
            for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                if 0 <= nx < W and 0 <= ny < H:
                    j = ny * W + nx
                    if mask[j] and not seen[j]:
                        seen[j] = 1
                        dq.append((nx, ny))
        if area < 200:
            continue
        if area > best_area:
            best_area = area
            best = (minx, miny, maxx, maxy)

if not best:
    print("FALLO: no se encontro figura")
    sys.exit(1)

minx, miny, maxx, maxy = best
bw = maxx - minx + 1
bh = maxy - miny + 1

# fondo = píxeles sin máscara alcanzables desde el marco del bbox
fondo = bytearray(W * H)
dq = deque()
for x in range(minx, maxx + 1):
    for y in (miny, maxy):
        j = y * W + x
        if not mask[j] and not fondo[j]:
            fondo[j] = 1
            dq.append((x, y))
for y in range(miny, maxy + 1):
    for x in (minx, maxx):
        j = y * W + x
        if not mask[j] and not fondo[j]:
            fondo[j] = 1
            dq.append((x, y))
while dq:
    x, y = dq.popleft()
    for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
        if minx <= nx <= maxx and miny <= ny <= maxy:
            j = ny * W + nx
            if not mask[j] and not fondo[j]:
                fondo[j] = 1
                dq.append((nx, ny))

out = im.copy()
op = out.load()
for y in range(miny, maxy + 1):
    base = y * W
    for x in range(minx, maxx + 1):
        if fondo[base + x]:
            r, g, b, a = op[x, y]
            op[x, y] = (r, g, b, 0)

out = out.crop((minx, miny, maxx + 1, maxy + 1))
out.save(dst)
print(f"OK figura {out.size} bbox=({minx},{miny},{maxx},{maxy}) area={best_area} TH={TH} origen={W}x{H}")
