#!/usr/bin/env python3
"""Marcador por canal IG (Joko Lab) — SOLO LECTURA.

Junta las 3 fuentes que ya existen para decidir QUE CANAL SE QUEDA:
  1) informes del cron vigilar-canales-ig  -> piezas vistas + ultima publicacion
  2) 04-operations/metrics/triaje_canales.jsonl -> senal por titulo/alt (barata, por pieza)
  3) 04-operations/metrics/aplicabilidad_ledger.jsonl -> analisis a fondo y entradas reales

Uso:  python3 ~/joko-lab/tools/marcador_canales.py [--desde YYYY-MM-DD] [--min-vistas N]

No escribe NADA. La decision (ascender / mantener / retirar) la toma el usuario con
estos datos delante; el script nunca retira un canal.

Criterio de 'entra' (identico al del ledger, RULE-015):
  aporta cifra medida con fuente + tecnica implementable en el stack + idea de experimento.
La columna 'vistas' mide VOLUMEN (ruido potencial), no valor: por si sola no decide nada.
"""
import argparse, collections, glob, json, os, re, sys

OUT_CRON = os.path.expanduser('~/.hermes/cron/output/4d64ff821685')
LEDGER = os.path.expanduser('~/joko-lab/04-operations/metrics/aplicabilidad_ledger.jsonl')
TRIAJE = os.path.expanduser('~/joko-lab/04-operations/metrics/triaje_canales.jsonl')

URL = re.compile(r'instagram\.com/([A-Za-z0-9_.]+)/(?:p|reel)/([A-Za-z0-9_-]{11})')
FECHA = re.compile(r'(\d{2})-([a-z]{3})\s+(\d{2}):(\d{2})')
MES = {m: i + 1 for i, m in enumerate(
    ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic'])}


def leer_informes(desde):
    """-> {canal: {'piezas': {code: fecha}, 'informes': set, 'ultima': fecha}}"""
    canales = collections.defaultdict(lambda: {'piezas': {}, 'informes': set(), 'ultima': ''})
    for fn in sorted(glob.glob(os.path.join(OUT_CRON, '*.md'))):
        fecha_inf = os.path.basename(fn)[:10]
        if desde and fecha_inf < desde:
            continue
        for linea in open(fn, encoding='utf-8', errors='replace'):
            for ch, code in URL.findall(linea):
                d = FECHA.findall(linea)
                post = ''
                if d:
                    dd, mm, hh, mi = d[-1]
                    if mm in MES:
                        post = f"2026-{MES[mm]:02d}-{int(dd):02d} {hh}:{mi}"
                c = canales[ch]
                c['informes'].add(fecha_inf)
                c['piezas'][code] = post
                if post > c['ultima']:
                    c['ultima'] = post
    return canales


def leer_jsonl(path):
    """Lee un JSONL de datos saltando la linea de esquema (_schema)."""
    filas = []
    if not os.path.exists(path):
        return filas
    for l in open(path, encoding='utf-8'):
        l = l.strip()
        if not l:
            continue
        try:
            d = json.loads(l)
        except json.JSONDecodeError:
            continue
        if isinstance(d, dict) and '_schema' not in d:
            filas.append(d)
    return filas


def main():
    ap = argparse.ArgumentParser(description='Marcador por canal IG (solo lectura)')
    ap.add_argument('--desde', default='', help='solo informes desde YYYY-MM-DD')
    ap.add_argument('--min-vistas', type=int, default=1)
    a = ap.parse_args()

    canales = leer_informes(a.desde)
    triaje = collections.defaultdict(collections.Counter)
    for d in leer_jsonl(TRIAJE):
        triaje[d.get('canal', d.get('fuente', '?'))][d.get('senal') or d.get('veredicto') or '?'] += 1
    led = collections.defaultdict(collections.Counter)
    for d in leer_jsonl(LEDGER):
        led[d['fuente']][d.get('veredicto', '?')] += 1

    nombres = sorted(set(canales) | set(triaje) | set(led),
                     key=lambda c: (-len(canales.get(c, {'piezas': {}})['piezas']), c))
    print(f"{'canal':24s}{'vistas':>7s}{'inform.':>8s}{'ult.pub':>18s}"
          f"{'prom/ruido (n)':>21s}{'analiz':>7s}{'entra':>6s}")
    print('-' * 92)
    filas = 0
    for c in nombres:
        v = canales.get(c, {'piezas': {}, 'informes': set(), 'ultima': ''})
        nv = len(v['piezas'])
        if nv < a.min_vistas and not led[c] and not triaje[c]:
            continue
        t = triaje[c]
        prom = t.get('prometedor', 0) + t.get('entra', 0)
        ruido = t.get('ruido', 0) + t.get('no_entra', 0)
        ent = led[c].get('entra', 0)
        an = sum(led[c].values())
        filas += 1
        print(f"{c:24s}{nv:7d}{len(v['informes']):8d}{v['ultima'][:16]:>18s}"
              f"{f'{prom}/{ruido} (n={sum(t.values())})':>21s}{an:7d}{ent:6d}")
    print('-' * 92)
    total_vistas = sum(len(v['piezas']) for v in canales.values())
    total_triaje = sum(sum(t.values()) for t in triaje.values())
    total_an = sum(sum(t.values()) for t in led.values())
    total_en = sum(t.get('entra', 0) for t in led.values())
    print(f"{filas} canales | {total_vistas} piezas vistas | {total_triaje} filas de triaje | "
          f"{total_an} analizadas a fondo | {total_en} entradas reales")
    if total_triaje == 0:
        print('\nAVISO: triaje_canales.jsonl vacio o inexistente -> SIN evidencia por canal.')
        print('Sin ese dato, cualquier retirada de canal seria a priori (prohibido, RULE-015).')
        print('El volumen (columna vistas) mide RUIDO, no valor: no sirve para decidir solo.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
