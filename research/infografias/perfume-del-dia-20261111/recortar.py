import sys, numpy as np
from PIL import Image, ImageFilter
from collections import deque

src, dst = sys.argv[1], sys.argv[2]
im = Image.open(src).convert("RGBA")
arr = np.array(im)
alpha0 = arr[:, :, 3]
print("alpha min/max:", alpha0.min(), alpha0.max(), "pct_transparente:", round(100*(alpha0 < 8).mean(), 1))

rgba = im
if alpha0.min() < 8:
    # ya trae transparencia: recortar por alfa y descontaminar
    a = np.array(im.convert("RGB")).astype(float)
    al = alpha0.astype(float) / 255.0
    safe = np.clip(al, 1e-3, 1)[..., None]
    col = np.clip((a - (1 - safe) * 255) / safe, 0, 255)
    solid_mask = alpha0 > 8
    print("usa alfa original")
else:
    a = np.array(im.convert("RGB")).astype(float); h, w, _ = a.shape
    L = a.mean(axis=2); mx = a.max(axis=2); mn = a.min(axis=2)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1) * 255, 0)
    gold = (sat > 55) & (L > 60) & (L < 250)
    ys, xs = np.where(gold)
    gx0, gx1 = xs.min(), xs.max()
    dark = (L < 110) & (np.abs(a[:, :, 0] - a[:, :, 2]) < 40)
    dy, dx = np.where(dark)
    bx0, bx1 = max(0, min(gx0, dx.min()) - 14), min(w - 1, max(gx1, dx.max()) + 14)
    print("banda x:", bx0, bx1, "| gold x:", gx0, gx1, "| dark x:", dx.min(), dx.max())
    band = np.zeros((h, w), bool); band[:, bx0:bx1 + 1] = True
    obj = (L < 237) & band
    free = ~obj; vis = np.zeros((h, w), bool); dq = deque()
    for x in range(w):
        for y in (0, h - 1):
            if free[y, x]: vis[y, x] = True; dq.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if free[y, x]: vis[y, x] = True; dq.append((y, x))
    while dq:
        y, x = dq.popleft()
        for dyy, dxx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dyy, x + dxx
            if 0 <= ny < h and 0 <= nx < w and free[ny, nx] and not vis[ny, nx]:
                vis[ny, nx] = True; dq.append((ny, nx))
    solid = (~vis) & band
    m = (Image.fromarray((solid * 255).astype(np.uint8))
         .filter(ImageFilter.MinFilter(5)).filter(ImageFilter.MaxFilter(3))
         .filter(ImageFilter.GaussianBlur(0.7)))
    alpha = np.array(m); al = alpha.astype(float) / 255
    safe = np.clip(al, 1e-3, 1)[..., None]
    col = np.clip((a - (1 - safe) * 255) / safe, 0, 255)
    rgba = Image.fromarray(np.dstack([col.astype(np.uint8), alpha]).astype(np.uint8), "RGBA")

img = rgba.crop(rgba.getbbox())
PAD = 16
cv = Image.new("RGBA", (img.width + 2 * PAD, img.height + 2 * PAD), (0, 0, 0, 0))
cv.alpha_composite(img, (PAD, PAD))
cv.save(dst)
bb = cv.getbbox()
print("figura final:", cv.size, "bbox:", bb, "alto figura:", bb[3] - bb[1])
marg = 16
al_f = np.array(cv)[:, :, 3]
print("opacos(>8) en margenes:",
      int((al_f[:marg] > 8).sum()), int((al_f[-marg:] > 8).sum()),
      int((al_f[:, :marg] > 8).sum()), int((al_f[:, -marg:] > 8).sum()))
