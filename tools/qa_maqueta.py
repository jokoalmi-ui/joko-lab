#!/usr/bin/env python3
"""qa_maqueta.py — revisa los FALLOS DE MAQUETA de una ficha ANTES de enviarla (Joko Lab, 04-11-2026).

Nace de un fallo real: la ficha se envió con el sello reducido a tres líneas
sueltas en la esquina, y con las tres filas de "Si te gusta, prueba" cuyas
columnas bailaban entre sí 20-54 px. El verificador de contraste no lo veía:
el texto era legible, simplemente estaba mal puesto.

Reglas (cada una imprime QUE y DONDE):
  M1 huérfano     un grupo de <=4 textos aislado >70 px de sus vecinos
  M2 margen       texto a <40 px del borde lateral, <18 px del superior o <14 px del inferior
  M3 rejilla      en filas consecutivas con >=3 columnas, la misma columna no puede
                  variar mas de 6 px entre filas (columnas que bailan)
  M4 hueco        hueco vertical >130 px entre dos bloques de texto (aviso, no fallo)
  M5 solape       dos cajas de texto se solapan mas del 30 % del area de la menor

Uso:
  /usr/bin/python3 tools/qa_maqueta.py <ficha.html> [--alto 1440] [--json out]
  exit 0 = MAQUETA OK | 2 = FALLOS

LIMITE DECLARADO: trabaja sobre el inventario de texto (nodos con contenido),
no sobre imagenes ni formas. Un desalineado grafico (logos, QR) no lo detecta.
"""
import argparse, json, pathlib, subprocess, sys, tempfile

TOOLS = pathlib.Path(__file__).resolve().parent
PY = '/usr/bin/python3'


def filas(items, tol=8):
    out = []
    for i in sorted(items, key=lambda i: (i['y'], i['x'])):
        if out and abs(i['y'] - out[-1][0]['y']) <= tol:
            out[-1].append(i)
        else:
            out.append([i])
    return [sorted(f, key=lambda i: i['x']) for f in out]


def solape(a, b):
    ix = min(a['x'] + a['w'], b['x'] + b['w']) - max(a['x'], b['x'])
    iy = min(a['y'] + a['h'], b['y'] + b['h']) - max(a['y'], b['y'])
    if ix <= 0 or iy <= 0:
        return 0.0
    return (ix * iy) / max(1.0, min(a['w'] * a['h'], b['w'] * b['h']))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('html')
    ap.add_argument('--alto', type=int, default=1440)
    ap.add_argument('--json')
    a = ap.parse_args()
    html = pathlib.Path(a.html).expanduser().resolve()
    tmp = pathlib.Path(tempfile.mkdtemp(prefix='qa_maq_')) / 'inv.json'
    r = subprocess.run([PY, str(TOOLS / 'inventario_legibilidad.py'), str(html), '--json', str(tmp)],
                       capture_output=True, text=True)
    if r.returncode != 0 or not tmp.exists():
        print('ERROR inventario\n' + (r.stdout + r.stderr)[-600:])
        return 2
    items = [i for i in json.loads(tmp.read_text())['items']
             if (i.get('t') or '').strip() and (i.get('px') or 0) >= 12
             and (i.get('w') or 0) > 2 and (i.get('h') or 0) > 2]
    if not items:
        print('ERROR: sin nodos de texto')
        return 2

    fallos, avisos = [], []

    # M1 huérfanos
    fs = filas(items)
    tops = [(min(i['y'] for i in f), max(i['y'] + i['h'] for i in f), len(f)) for f in fs]
    for k, (y0, y1, n) in enumerate(tops):
        if n > 4:
            continue
        ant = tops[k - 1][1] if k else None
        sig = tops[k + 1][0] if k + 1 < len(tops) else None
        d_ant = (y0 - ant) if ant is not None else 999
        d_sig = (sig - y1) if sig is not None else 999
        if d_ant > 70 and d_sig > 30:
            txt = ' / '.join((i['t'] or '')[:14] for i in fs[k])
            fallos.append(f'M1 huérfano  y{y0:.0f} ({n} textos, {d_ant:.0f} px del anterior): "{txt}"')

    # M2 márgenes
    for i in items:
        if i['x'] < 40:
            fallos.append(f"M2 margen izq  x{i['x']:.0f} (min 40): {(i['t'] or '')[:26]!r}")
        if i['y'] < 18:
            fallos.append(f"M2 margen sup  y{i['y']:.0f} (min 18): {(i['t'] or '')[:26]!r}")
        if i['y'] + i['h'] > a.alto - 14:
            fallos.append(f"M2 margen inf  y{i['y'] + i['h']:.0f} (max {a.alto - 14}): {(i['t'] or '')[:26]!r}")

    # M3 rejilla
    for k in range(len(fs) - 1):
        f1, f2 = fs[k], fs[k + 1]
        if len(f1) < 3 or len(f1) != len(f2):
            continue
        dy = f2[0]['y'] - f1[0]['y']
        if not (25 <= dy <= 46):
            continue
        for c, (p, q) in enumerate(zip(f1, f2)):
            # vale alinear por la izquierda o por la derecha: si un borde coincide, hay eje
            izq = abs(p['x'] - q['x'])
            der = abs((p['x'] + p['w']) - (q['x'] + q['w']))
            if izq > 6 and der > 6:
                fallos.append(f"M3 columna {c + 1} baila {(p['x']):.0f}->{(q['x']):.0f} "
                              f"({q['x'] - p['x']:+.0f} px) en y{p['y']:.0f}/y{q['y']:.0f}: "
                              f"{(p['t'] or '')[:16]!r} vs {(q['t'] or '')[:16]!r}")

    # M3b rotulo apilado: dos o tres lineas cortas de un mismo rotulo sin eje comun
    for k in range(len(fs) - 1):
        f1, f2 = fs[k], fs[k + 1]
        if len(f1) != 1 or len(f2) != 1:
            continue
        dy = f2[0]['y'] - f1[0]['y']
        ratio = max(f1[0]['w'], f2[0]['w']) / max(1.0, min(f1[0]['w'], f2[0]['w']))
        izq = abs(f2[0]['x'] - f1[0]['x'])
        der = abs((f2[0]['x'] + f2[0]['w']) - (f1[0]['x'] + f1[0]['w']))
        if ratio < 2.2 and 12 <= dy <= 26 and izq > 6 and der > 6:
            fallos.append(f'M3b rotulo sin eje  x{f1[0]["x"]:.0f}->{f2[0]["x"]:.0f} '
                          f'({f2[0]["x"] - f1[0]["x"]:+.0f} px) en y{f1[0]["y"]:.0f}: '
                          f'"{(f1[0]["t"] or "")[:14]}" / "{(f2[0]["t"] or "")[:14]}"')

    # M4 huecos
    fin = None
    for y0, y1, n in tops:
        if fin is not None and y0 - fin > 130:
            avisos.append(f'M4 hueco {y0 - fin:.0f} px entre y{fin:.0f} e y{y0:.0f}')
        fin = max(fin or 0, y1)

    # M5 solapes
    s = sorted(items, key=lambda i: (i['y'], i['x']))
    for k in range(len(s)):
        for j in range(k + 1, min(k + 4, len(s))):
            # apilados en la misma columna: la caja del texto incluye el interlineado y
            # siempre muerde la linea siguiente. Eso es tipografia, no solape.
            apilado = (abs(s[j]['x'] - s[k]['x']) < 24 and
                       s[j]['y'] - s[k]['y'] < s[k]['h'] * 0.75)
            if apilado:
                continue
            v = solape(s[k], s[j])
            if v > 0.30:
                fallos.append(f"M5 solape {v:.0%} en y{s[j]['y']:.0f}: "
                              f"{(s[k]['t'] or '')[:20]!r} / {(s[j]['t'] or '')[:20]!r}")

    print(f'QA MAQUETA — {html.name}   ({len(items)} textos)')
    for f in fallos:
        print('  ' + f)
    for v in avisos:
        print('  ' + v)
    if not fallos:
        print('  sin fallos de maqueta')
    print(f'VEREDICTO MAQUETA {"OK" if not fallos else "FALLOS (" + str(len(fallos)) + ")"}')
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps({'ok': not fallos, 'fallos': fallos, 'avisos': avisos},
                                                   ensure_ascii=False, indent=1))
    return 0 if not fallos else 2


if __name__ == '__main__':
    sys.exit(main())
