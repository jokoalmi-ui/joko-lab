#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""desglose_coste.py — DESGLOSE del gasto DeepSeek: franja horaria y tamano de salida.

SOLO LECTURA sobre el ledger de observabilidad. Reutiliza TARIFA y es_peak de
coste_ahorro.py, de modo que la tarifa y la definicion de pico son las mismas que
las del informe diario (no se duplica logica ni se inventan precios).

Responde a: donde se va el dinero y cuanto se podria recortar.
  - reparto por franja horaria (local ES) y pico vs valle (tarifa x2)
  - tamano de salida por consulta (p50/p90/p95) y simulacion de recortes
  - coste del prefijo cacheado (hit) vs sin cachear (miss)
  - TECHO: suma de las 3 palancas medidas (A1 salida -30%, A4 pico->valle, miss -30%)

Uso:
  python3 tools/desglose_coste.py [--dias 7] [--ledger RUTA]

Instrumento de medida: no modifica nada, no escribe, no llama a ninguna API.
"""
import argparse
import datetime as dt
import json
import os
import sys
import time

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, 'tools'))
import coste_ahorro as ca  # noqa: E402  (TARIFA, es_peak, LEDGER)

LEDGER_DEF = getattr(ca, 'LEDGER', os.path.join(BASE, '04-operations/metrics/pipeline_obs.jsonl'))
GES = 1e6
FRANJAS = [('00-03 valle', 0, 3), ('03-06 PICO', 3, 6), ('06-08 valle', 6, 8),
           ('08-12 PICO', 8, 12), ('12-24 valle', 12, 24)]


def pct(xs, q):
    if not xs:
        return 0
    xs = sorted(xs)
    return xs[min(int(round(q / 100.0 * (len(xs) - 1))), len(xs) - 1)]


def cargar(ledger, dias, gmtoff):
    """Devuelve las filas de la ventana, ya con coste calculado."""
    t0 = dt.datetime.now() - dt.timedelta(days=dias)
    filas, mal = [], 0
    with open(ledger, encoding='utf-8', errors='replace') as f:
        for raw in f:
            raw = raw.strip()
            if not raw:
                continue
            try:
                d = json.loads(raw)
            except Exception:
                mal += 1
                continue
            if d.get('provider') != 'deepseek' or d.get('path') != '/v1/chat/completions':
                continue
            ts = str(d.get('timestamp') or '')
            try:
                t = dt.datetime.fromisoformat(ts[:19])
            except Exception:
                mal += 1
                continue
            if t < t0:
                continue
            m = d.get('model') or 'deepseek-v4-flash'
            tar = ca.TARIFA.get(m) or ca.TARIFA['deepseek-v4-flash']
            hit = int(d.get('prompt_cache_hit_tokens') or 0)
            mis = int(d.get('prompt_cache_miss_tokens') or 0)
            out = int(d.get('completion_tokens') or 0)
            pr = int(d.get('prompt_tokens') or (hit + mis))
            pk = bool(ca.es_peak(ts, gmtoff))
            k = 2.0 if pk else 1.0
            c = (hit * tar['hit'] + mis * tar['miss'] + out * tar['out']) / GES * k
            filas.append(dict(t=t, h=t.hour, p=pk, model=m, tar=tar,
                              hit=hit, mis=mis, out=out, pr=pr, c=c))
    return filas, mal, t0


def informe(filas, mal, t0, dias, gmtoff):
    L = []
    add = L.append
    N = len(filas)
    TOT = sum(f['c'] for f in filas) or 0.0
    if not N:
        return ['SIN DATOS en la ventana %s' % t0.isoformat(timespec='seconds')]
    add('DESGLOSE DE COSTE (ventana %d dias: %s -> %s)'
        % (dias, t0.isoformat(timespec='seconds'), dt.datetime.now().isoformat(timespec='seconds')))
    add('  n=%d  TOTAL %.4f USD  media %.4f USD/dia  %.4f USD/consulta  (no-parseadas %d)'
        % (N, TOT, TOT / dias, TOT / N, mal))
    add('  tarifa %s (%s) | pico x2: 03-06 y 08-12 hora local, L-V'
        % (ca.TARIFA_FECHA, ca.TARIFA_FUENTE))

    add('')
    add('1) POR FRANJA (hora local)')
    for nom, a, b in FRANJAS:
        g = [f for f in filas if a <= f['h'] < b]
        if not g:
            continue
        c = sum(x['c'] for x in g)
        pr = sum(x['pr'] for x in g)
        hi = sum(x['hit'] for x in g)
        add('   %-12s n=%5d  %8.4f USD  %5.1f%%  prompt %6.2fM (hit %4.1f%%)  out %5.2fM'
            % (nom, len(g), c, 100 * c / TOT, pr / GES, 100 * hi / max(pr, 1), sum(x['out'] for x in g) / GES))

    add('')
    add('2) PICO vs VALLE')
    cp = sum(f['c'] for f in filas if f['p'])
    npk = sum(1 for f in filas if f['p'])
    add('   PICO x2: n=%d  %.4f USD (%.1f%%)   VALLE: n=%d  %.4f USD (%.1f%%)'
        % (npk, cp, 100 * cp / TOT, N - npk, TOT - cp, 100 * (TOT - cp) / TOT))
    add('   A4 (mover TODO el pico a valle): -%.4f USD/ventana = -%.4f USD/dia'
        % (cp / 2, cp / 2 / dias))

    add('')
    add('3) POR HORA')
    horas = {}
    for f in filas:
        a = horas.setdefault(f['h'], [0, 0.0])
        a[0] += 1
        a[1] += f['c']
    for h in range(24):
        n, c = horas.get(h, (0, 0.0))
        add('   %02d:00  n=%4d  %7.4f USD  %5.1f%%  %s'
            % (h, n, c, 100 * c / TOT, '#' * int(round(200 * c / TOT))))

    add('')
    add('4) POR DIA')
    dias_ = {}
    for f in filas:
        k = f['t'].date().isoformat()
        a = dias_.setdefault(k, [0, 0.0])
        a[0] += 1
        a[1] += f['c']
    for k in sorted(dias_):
        n, c = dias_[k]
        add('   %s  n=%4d  %7.4f USD' % (k, n, c))

    add('')
    add('5) SALIDA (completion_tokens por consulta)')
    outs = [f['out'] for f in filas]
    cout = sum(f['out'] * f['tar']['out'] / GES * (2.0 if f['p'] else 1.0) for f in filas)
    add('   total %.2fM  coste %.4f USD (%.1f%% del gasto)  media %.0f  max %d'
        % (sum(outs) / GES, cout, 100 * cout / TOT, sum(outs) / N, max(outs)))
    add('   p25 %d | p50 %d | p75 %d | p90 %d | p95 %d | p99 %d'
        % (pct(outs, 25), pct(outs, 50), pct(outs, 75), pct(outs, 90), pct(outs, 95), pct(outs, 99)))
    add('   top 10%% de consultas mas largas = %.1f%% del coste de salida'
        % (100 * sum(sorted(outs, reverse=True)[:max(1, N // 10)]) / max(sum(outs), 1)))
    a1 = cout * 0.30
    add('   A1 (-30%% lineal): -%.4f USD/ventana (-%.1f%% del total)  |  cap p90: -%.4f  |  cap p95: -%.4f'
        % (a1, 100 * a1 / TOT,
           cout * (1 - sum(min(f['out'], pct(outs, 90)) for f in filas) / max(sum(outs), 1)),
           cout * (1 - sum(min(f['out'], pct(outs, 95)) for f in filas) / max(sum(outs), 1))))

    add('')
    add('6) PREFIJO (hit vs miss)')
    prm = [f['pr'] for f in filas]
    th = sum(f['hit'] for f in filas)
    tm = sum(f['mis'] for f in filas)
    cm = sum(f['mis'] * f['tar']['miss'] / GES * (2.0 if f['p'] else 1.0) for f in filas)
    ch = sum(f['hit'] * f['tar']['hit'] / GES * (2.0 if f['p'] else 1.0) for f in filas)
    add('   prompt medio %.0f  p50 %d  p95 %d  max %d' % (sum(prm) / N, pct(prm, 50), pct(prm, 95), max(prm)))
    add('   hit %.2fM  miss %.2fM  ratio hit %.1f%%  (~%.0f tokens nuevos por consulta)'
        % (th / GES, tm / GES, 100 * th / max(th + tm, 1), tm / N))
    add('   coste miss %.4f USD (%.1f%%)  |  coste hit %.4f USD (%.1f%%)'
        % (cm, 100 * cm / TOT, ch, 100 * ch / TOT))
    a2 = cm * 0.30
    add('   A2 (miss -30%%): -%.4f USD/ventana (-%.1f%% del total)'
        % (a2, 100 * a2 / TOT))

    a4 = cp / 2
    add('')
    add('TECHO MEDIDO (A1 + A2 + A4, teoricos y simultaneos)')
    add('   A1 salida -30%%: %.4f | A2 miss -30%%: %.4f | A4 pico->valle: %.4f'
        % (a1, a2, a4))
    add('   TOTAL TEORICO %.4f USD/ventana = %.4f USD/dia -> ritmo %.4f USD/dia (desde %.4f)'
        % (a1 + a2 + a4, (a1 + a2 + a4) / dias, max(TOT - (a1 + a2 + a4), 0) / dias, TOT / dias))
    add('   OJO: A4 es solo parcialmente evitable (la franja de trabajo real) y A2 no se ')
    add('   controla del todo -> el techo es el MAXIMO calculable, no una prevision.')
    return L


def main():
    ap = argparse.ArgumentParser(description='Desglose del gasto DeepSeek (solo lectura).')
    ap.add_argument('--dias', type=int, default=7)
    ap.add_argument('--ledger', default=LEDGER_DEF)
    a = ap.parse_args()
    gmtoff = time.localtime().tm_gmtoff
    if not os.path.exists(a.ledger):
        print('LEDGER no encontrado: %s' % a.ledger)
        return 1
    filas, mal, t0 = cargar(a.ledger, a.dias, gmtoff)
    print('\n'.join(informe(filas, mal, t0, a.dias, gmtoff)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
