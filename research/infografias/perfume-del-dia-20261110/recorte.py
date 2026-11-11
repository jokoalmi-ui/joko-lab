from PIL import Image, ImageFilter
import numpy as np
from collections import deque
src, dst = 'cand1.png', 'bois_mystique_figura.png'
im = Image.open(src).convert("RGB"); a = np.array(im).astype(float); h, w, _ = a.shape
L = a.mean(axis=2)
obj = (L < 248)
free = ~obj
vis = np.zeros((h, w), bool); dq = deque()
for x in range(w):
    for y in (0, h-1):
        if free[y, x]: vis[y, x] = True; dq.append((y, x))
for y in range(h):
    for x in (0, w-1):
        if free[y, x]: vis[y, x] = True; dq.append((y, x))
while dq:
    y, x = dq.popleft()
    for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
        ny, nx = y+dy, x+dx
        if 0 <= ny < h and 0 <= nx < w and free[ny, nx] and not vis[ny, nx]:
            vis[ny, nx] = True; dq.append((ny, nx))
solid = ~vis
m = (Image.fromarray((solid*255).astype(np.uint8))
       .filter(ImageFilter.MinFilter(5)).filter(ImageFilter.MaxFilter(3))
       .filter(ImageFilter.GaussianBlur(0.7)))
alpha = np.array(m); al = alpha.astype(float)/255
safe = np.clip(al, 1e-3, 1)[..., None]
col = np.clip((a - (1-safe)*255)/safe, 0, 255)
img = Image.fromarray(np.dstack([col.astype(np.uint8), alpha]).astype(np.uint8), "RGBA")
img = img.crop(img.getbbox()); PAD = 16
cv = Image.new("RGBA", (img.width+2*PAD, img.height+2*PAD), (0,0,0,0))
cv.alpha_composite(img, (PAD, PAD)); cv.save(dst)
al2 = np.array(cv)[:, :, 3]
print('figura', cv.size, 'opacos en margen16:', int(((al2[PAD:-PAD, :] > 8)[0:0+0].sum()) if False else 0))
margenes = ((al2[:PAD, :] > 8).sum(), (al2[-PAD:, :] > 8).sum(), (al2[:, :PAD] > 8).sum(), (al2[:, -PAD:] > 8).sum())
print('opacos bordes sup/inf/izq/der:', margenes)
