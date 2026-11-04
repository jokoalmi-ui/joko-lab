#!/usr/bin/env python3
"""nitidez_texto.py — mide si las letras de una ficha estan NITIDAS o DESENFOCADAS.

Motivo (04-11-2026): el usuario dijo "la nitidez de las letras es muy mala, estan como
desenfocadas" sobre una ficha que un medidor de bordes (RMS del laplaciano) daba por
BUENA: ese medidor premia cualquier borde, y el text-shadow anade bordes falsos. No
servia. Este mide otra cosa: cuanto de la caja de texto cae en zona intermedia.

  medio%   fraccion de pixeles con luminancia entre p20 y p80 de la caja.
           Letra nitida -> dos poblaciones (tinta y fondo), poco en medio.
           Letra desenfocada o con halo difuso -> mucho en medio. MENOS ES MEJOR.
  salto    p90 del gradiente |dL/dx|+|dL/dy| dentro de la caja. Letra nitida -> saltos
           grandes. MAS ES MEJOR.

VALIDACION OBLIGATORIA (RULE-015): tools/nitidez_texto.py --validar <png> <inv.json>
aplica un desenfoque gaussiano conocido y comprueba que el instrumento lo detecta.
Un numero sin control negativo no se publica.

Uso:
  /usr/bin/python3 tools/nitidez_texto.py <png> <inventario.json> [--json out]
  /usr/bin/python3 tools/nitidez_texto.py --validar <png> <inventario.json>
"""
import argparse, json, pathlib, sys
from PIL import Image, ImageFilter

MIN_PX = 12


def cajas(inv):
    out = []
    for i in inv:
        if (i.get('px') or 0) < MIN_PX or not (i.get('t') or '').strip():
            continue
        x, y, w, h = [int(i.get(k) or 0) for k in ('x', 'y', 'w', 'h')]
        if w > 2 and h > 2:
            out.append((x, y, w, h))
    return out


def medir(img, boxes):
    g = img.convert('L')
    W, H = g.size
    tot_m, tot_s, n = 0.0, 0.0, 0
    for (x, y, w, h) in boxes:
        box = g.crop((max(0, x - 1), max(0, y - 1), min(W, x + w + 1), min(H, y + h + 1)))
        bw, bh = box.size
        if bw < 4 or bh < 5:
            continue
        raw = box.tobytes()
        px = [raw[k] for k in range(0, len(raw), 1)]
        s = sorted(px)
        n_px = len(s)
        p20, p80 = s[int(.20 * n_px)], s[int(.80 * n_px)]
        if p80 - p20 < 24:          # caja sin contraste suficiente: no informa
            continue
        medio = sum(1 for v in px if p20 < v < p80) / n_px
        # gradiente horizontal y vertical
        saltos = []
        for yy in range(0, bh, 2):
            base = yy * bw
            for xx in range(1, bw):
                saltos.append(abs(raw[base + xx] - raw[base + xx - 1]))
        if bh > 1:
            for yy in range(1, bh, 2):
                base = yy * bw
                prev = base - bw
                for xx in range(0, bw):
                    saltos.append(abs(raw[base + xx] - raw[prev + xx]))
        if not saltos:
            continue
        saltos.sort()
        tot_m += medio * 100
        tot_s += saltos[int(.90 * len(saltos))]
        n += 1
    if not n:
        return None
    return {'medio': tot_m / n, 'salto': tot_s / n, 'cajas': n}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('png')
    ap.add_argument('inv', nargs='?')
    ap.add_argument('--json')
    ap.add_argument('--validar', action='store_true')
    a = ap.parse_args()
    img = Image.open(a.png).convert('RGB')
    inv = json.loads(pathlib.Path(a.inv).read_text())['items']

    base = medir(img, cajas(inv))
    if not base:
        print('ERROR: ninguna caja medible')
        return 2

    if a.validar:
        print(f'CONTROL NEGATIVO sobre {pathlib.Path(a.png).name}')
        print(f'  original     medio {base["medio"]:5.1f} %   salto {base["salto"]:5.1f}   ({base["cajas"]} cajas)')
        ok = True
        for sig in (0.8, 1.6, 2.4):
            blur = medir(img.filter(ImageFilter.GaussianBlur(sig)), cajas(inv))
            d = blur['medio'] - base['medio']
            print(f'  blur {sig:3.1f}px  medio {blur["medio"]:5.1f} %   salto {blur["salto"]:5.1f}   '
                  f'(medio {d:+.1f}, salto {blur["salto"] - base["salto"]:+.1f})')
            if d <= 0:
                ok = False
        print('INSTRUMENTO ' + ('VALIDO: el desenfoque sube medio y baja salto'
                                if ok else 'NO VALIDO: no separa nitido de borroso'))
        return 0 if ok else 2

    # el umbral no se inventa: se calibra en la propia imagen con un desenfoque de 0,8 px.
    # medido el 04-11 sobre fichas reales: 0,8 px de blur baja el salto ~45 %.
    ref = medir(img.filter(ImageFilter.GaussianBlur(0.8)), cajas(inv))
    assert ref is not None
    ratio = base['salto'] / max(1e-6, ref['salto'])
    print(f'NITIDEZ TEXTO — {pathlib.Path(a.png).name}')
    print(f'  salto   {base["salto"]:5.1f}   (referencia borrosa 0,8px: {ref["salto"]:5.1f})')
    print(f'  ratio   {ratio:5.2f}   (>=1,5 = nitida; <1,2 = se ve desenfocada)')
    print(f'  medio   {base["medio"]:5.1f} %  (informativo: no separa nitido de borroso)')
    print(f'  cajas   {base["cajas"]}')
    veredicto = 'NITIDA' if ratio >= 1.5 else ('DESENFOCADA' if ratio < 1.2 else 'DUDA')
    print(f'VEREDICTO {veredicto}')
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps({**base, 'veredicto': veredicto}, indent=1))
    return 0 if veredicto == 'NITIDA' else 2


if __name__ == '__main__':
    sys.exit(main())
