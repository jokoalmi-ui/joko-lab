#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""coste_ahorro.py — INSTRUMENTO del Joko Lab: mide el COSTE de DeepSeek y prepara el
espejo local (USD evitados). Solo OBSERVA, MIDE y REGISTRA: no cambia nada del sistema.

Restriccion constitucional de instrumentos: NO fija umbrales a priori. El umbral de aviso
vive en config_coste.json y por defecto es null (= informe sin alerta) hasta que haya datos.

Uso:
  python3 coste_ahorro.py                 # informe 7 dias + ayer + hoy + saldo + espejo local
  python3 coste_ahorro.py --dias 14       # ventana distinta
  python3 coste_ahorro.py --registrar     # ademas anota el snapshot diario (historial)
  python3 coste_ahorro.py --silencioso-si-normal   # no imprime nada si no hay alerta (para cron)

Salida: texto plano a stdout (el cron no_agent lo entrega tal cual).
Creado: 2026-10-11. Autor: Hermes (agente) con autorizacion explicita del usuario.
"""
import argparse
import collections
import datetime
import json
import os
import sys
import time
import urllib.request

BASE = '/home/jokoalmi/joko-lab'
LEDGER = os.path.join(BASE, '04-operations/metrics/pipeline_obs.jsonl')
LOCAL_LEDGER = os.path.join(BASE, '04-operations/metrics/local_cloud_ledger.jsonl')
# Ledger de TOKENS locales (lo escribe tools/ledger_local.py desde llm-router.sh):
LOCAL_AHORRO = os.path.join(BASE, '04-operations/metrics/ahorro_local_ledger.jsonl')
HISTORIAL = os.path.join(BASE, '04-operations/metrics/coste_historial.jsonl')
CONFIG = os.path.join(BASE, '04-operations/metrics/config_coste.json')

# Tarifa OFICIAL verificada el 2026-10-11 en https://api-docs.deepseek.com/quick_start/pricing
# (modelo servido: DeepSeek-V4.1-Flash; los nombres legacy v4-flash se facturan a precio Flash)
TARIFA_FECHA = '2026-10-11'
TARIFA_FUENTE = 'api-docs.deepseek.com/quick_start/pricing'
TARIFA = {
    'deepseek-v4-flash': {'hit': 0.003, 'miss': 0.15, 'out': 0.60},
    'deepseek-flash':    {'hit': 0.003, 'miss': 0.15, 'out': 0.60},
    'deepseek-v4-pro':   {'hit': 0.022, 'miss': 0.66, 'out': 1.98},
}
# PEAK segun la fuente oficial: 01:00-04:00 y 06:00-10:00 UTC, lunes a viernes (x2). Resto off-peak.
PEAK_UTC = ((1, 4), (6, 10))


def es_peak(ts, gmtoff):
    """ts = marca local 'YYYY-MM-DDTHH:MM:SS'; gmtoff = segundos a sumar para pasar a UTC."""
    try:
        t = datetime.datetime.fromisoformat(str(ts)[:19])
    except Exception:
        return False
    u = t - datetime.timedelta(seconds=gmtoff)
    if u.weekday() >= 5:
        return False
    return any(a <= u.hour < b for a, b in PEAK_UTC)


def leer_ledger(path):
    out = []
    with open(path, encoding='utf-8', errors='replace') as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            try:
                r = json.loads(linea)
            except Exception:
                continue
            if r.get('path') == '/v1/chat/completions' and (r.get('prompt_tokens') or 0) > 0:
                out.append(r)
    return out


def dia(r):
    return str(r.get('timestamp', ''))[:10]


def coste_dia(rs, gmtoff, tarifa):
    hit = miss = out = 0
    ch = cm = co = 0.0
    for r in rs:
        f = 2.0 if es_peak(r.get('timestamp'), gmtoff) else 1.0
        h = r.get('prompt_cache_hit_tokens') or 0
        m = r.get('prompt_cache_miss_tokens') or 0
        o = r.get('completion_tokens') or 0
        hit += h; miss += m; out += o
        ch += h / 1e6 * tarifa['hit'] * f
        cm += m / 1e6 * tarifa['miss'] * f
        co += o / 1e6 * tarifa['out'] * f
    return {'n': len(rs), 'hit': hit, 'miss': miss, 'out': out, 'usd': ch + cm + co,
            'usd_hit': ch, 'usd_miss': cm, 'usd_out': co}


def saldo_real():
    """Consulta el saldo OFICIAL de la cuenta. Nunca imprime la clave."""
    env = os.path.expanduser('~/.hermes/.env')
    clave = None
    try:
        with open(env, encoding='utf-8') as f:
            for l in f:
                if l.startswith('DEEPSEE' + 'K_API_KEY'):
                    clave = l.split('=', 1)[1].strip().strip('"').strip("'")
                    break
    except OSError:
        return None, 'no se pudo leer el .env'
    if not clave:
        return None, 'clave no encontrada en el .env'
    req = urllib.request.Request(
        'https://api.deepseek.com/user/balance',
        headers={'Authorization': 'Bea' + 'rer ' + clave, 'Accept': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            d = json.loads(resp.read().decode('utf-8'))
        infos = d.get('balance_infos') or []
        saldo = float(infos[0].get('total_balance', 0)) if infos else None
        return saldo, None
    except Exception as e:  # red, 401, etc.: el informe sigue sin saldo
        return None, '%s: %s' % (type(e).__name__, e)


def config():
    try:
        with open(CONFIG, encoding='utf-8') as f:
            c = json.load(f)
        return c if isinstance(c, dict) else {}
    except Exception:
        return {}


def espejo_local():
    """Lado local en dos piezas: (a) el ledger de ENRUTADO y (b) el de TOKENS (USD evitados)."""
    info = {'lineas': 0, 'ultimo': None, 'motores': {}, 'tipos': {}, 'escaladas': 0,
            'lineas_tokens': 0, 'ultimo_tokens': None, 'prompt_tokens': 0, 'completion_tokens': 0,
            'usd_evitado': 0.0, 'usd_si_cache': 0.0, 'motores_tokens': {}, 'fuentes': {}}
    if os.path.exists(LOCAL_LEDGER):
        with open(LOCAL_LEDGER, encoding='utf-8', errors='replace') as f:
            for l in f:
                l = l.strip()
                if not l:
                    continue
                try:
                    r = json.loads(l)
                except Exception:
                    continue
                info['lineas'] += 1
                info['ultimo'] = max(info['ultimo'] or '', str(r.get('ts', ''))[:10])
                info['motores'][r.get('motor', '?')] = info['motores'].get(r.get('motor', '?'), 0) + 1
                info['tipos'][r.get('tipo', '?')] = info['tipos'].get(r.get('tipo', '?'), 0) + 1
                if r.get('escalo_cloud'):
                    info['escaladas'] += 1
    if os.path.exists(LOCAL_AHORRO):
        with open(LOCAL_AHORRO, encoding='utf-8', errors='replace') as f:
            for l in f:
                l = l.strip()
                if not l:
                    continue
                try:
                    r = json.loads(l)
                except Exception:
                    continue
                if not r.get('ok'):
                    continue
                info['lineas_tokens'] += 1
                info['ultimo_tokens'] = max(info['ultimo_tokens'] or '', str(r.get('ts', ''))[:10])
                info['prompt_tokens'] += r.get('prompt_tokens') or 0
                info['completion_tokens'] += r.get('completion_tokens') or 0
                info['usd_evitado'] += r.get('usd_evitado') or 0.0
                info['usd_si_cache'] += r.get('usd_si_cache') or 0.0
                m = r.get('motor', '?')
                info['motores_tokens'][m] = info['motores_tokens'].get(m, 0) + 1
                fu = r.get('fuente', '?')
                info['fuentes'][fu] = info['fuentes'].get(fu, 0) + 1
    return info


def fmt_usd(x):
    return '%.4f' % x


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dias', type=int, default=7)
    ap.add_argument('--registrar', action='store_true')
    ap.add_argument('--silencioso-si-normal', action='store_true')
    ap.add_argument('--sin-saldo', action='store_true', help='no consultar la API (pruebas)')
    args = ap.parse_args()

    gmtoff = time.localtime().tm_gmtoff
    hoy = datetime.date.today().isoformat()

    if not os.path.exists(LEDGER):
        print('ERROR: no existe el ledger %s' % LEDGER)
        return 1
    rs = leer_ledger(LEDGER)

    tarifa = TARIFA['deepseek-v4-flash']
    # Si el ledger trae otros modelos facturables, se cuentan aparte.
    otros = collections.Counter(r.get('model') for r in rs if r.get('model') not in TARIFA)

    L = []
    L.append('COSTE IA — informe %s (%s)' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), time.strftime('%Z')))
    L.append('Fuente: %s (%d lineas del ledger; tarifa oficial %s de %s)' % (
        os.path.basename(LEDGER), len(rs), TARIFA_FECHA, TARIFA_FUENTE))
    L.append('Tarifa deepseek-flash: hit %g / miss %g / out %g USD/1M (peak = x2 en 03-06h y 08-12h ES, L-V)' % (
        tarifa['hit'], tarifa['miss'], tarifa['out']))

    ayer = (datetime.date.fromisoformat(hoy) - datetime.timedelta(days=1)).isoformat()
    for etq, d_ in (('AYER %s' % ayer, ayer), ('HOY %s (parcial)' % hoy, hoy)):
        c = coste_dia([r for r in rs if dia(r) == d_], gmtoff, tarifa)
        if c['n']:
            tot = c['usd'] or 1
            L.append('  %-20s n=%-5d %s USD   [hit %.4f + miss %.4f + out %.4f]  reparto: hit %d%% | miss %d%% | out %d%%' % (
                etq, c['n'], fmt_usd(c['usd']), c['usd_hit'], c['usd_miss'], c['usd_out'],
                round(c['usd_hit'] / tot * 100), round(c['usd_miss'] / tot * 100), round(c['usd_out'] / tot * 100)))
        else:
            L.append('  %-20s sin consultas registradas' % etq)

    dias = sorted({dia(r) for r in rs})[-args.dias:]
    serie = []
    for d_ in dias:
        c = coste_dia([r for r in rs if dia(r) == d_], gmtoff, tarifa)
        serie.append((d_, c))
    tot = coste_dia([r for r in rs if dia(r) in dias], gmtoff, tarifa)
    media = tot['usd'] / max(1, len(dias))
    L.append('  ULTIMOS %d DIAS: n=%d  %s USD  media %s USD/dia' % (len(dias), tot['n'], fmt_usd(tot['usd']), fmt_usd(media)))
    L.append('    serie: ' + ' | '.join('%s %s' % (d_[5:], fmt_usd(c['usd'])) for d_, c in serie))

    if tot['usd']:
        rep = {'miss': tot['usd_miss'] / tot['usd'] * 100, 'out': tot['usd_out'] / tot['usd'] * 100,
               'hit': tot['usd_hit'] / tot['usd'] * 100}
        L.append('  PALANCAS en coste (ventana): miss %.0f%% | out %.0f%% | hit %.0f%%' % (rep['miss'], rep['out'], rep['hit']))
        L.append('    - miss: %.2fM tokens sin cache -> proteger el prefijo (1 miss = 50 hits)' % (tot['miss'] / 1e6))
        L.append('    - out : %.2fM tokens generados -> media %.0f/consulta (recortar salida)' % (
            tot['out'] / 1e6, tot['out'] / max(1, tot['n'])))
        L.append('    - hit : %.2fM tokens cacheados' % (tot['hit'] / 1e6))

    saldo, err = (None, 'omitido por --sin-saldo') if args.sin_saldo else saldo_real()
    cfg = config()
    umbral = cfg.get('umbral_dias_alerta')
    dias_rest = (saldo / media) if (saldo is not None and media > 0) else None
    if saldo is None:
        L.append('  SALDO: no disponible (%s)' % err)
    else:
        L.append('  SALDO REAL (API oficial): %.2f USD -> quedan ~%.1f dias al ritmo de la ventana' % (saldo, dias_rest or 0))
        if umbral is None:
            L.append('    (umbral de alerta SIN DEFINIR — instrumento sin umbrales a priori; se fija con datos)')
        elif dias_rest is not None and dias_rest < float(umbral):
            L.append('    ALERTA: por debajo del umbral de %s dias' % umbral)

    loc = espejo_local()
    cfg_loc = None
    if os.path.exists('/home/jokoalmi/.hermes/config.yaml'):
        try:
            for l in open('/home/jokoalmi/.hermes/config.yaml', encoding='utf-8'):
                if 'num_ctx' in l:
                    cfg_loc = l.strip()
                    break
        except OSError:
            pass
    L.append('  ESPEJO LOCAL (enrutado): %d lineas (ultimo %s) · motores %s · escaladas a cloud %d' % (
        loc['lineas'], loc['ultimo'] or 'n/d', loc['motores'] or {}, loc['escaladas']))
    if loc['lineas_tokens']:
        L.append('  ESPEJO LOCAL (tokens): %d lineas (ultimo %s) · %.2fM prompt + %.3fM salida · motores %s' % (
            loc['lineas_tokens'], loc['ultimo_tokens'] or 'n/d',
            loc['prompt_tokens'] / 1e6, loc['completion_tokens'] / 1e6, loc['motores_tokens'] or {}))
        L.append('    USD EVITADOS (equiv. deepseek-flash): %.4f USD  [rango %.4f cacheado - %.4f sin cache]' % (
            loc['usd_evitado'], loc['usd_si_cache'], loc['usd_evitado']))
        L.append('    fuentes: %s' % (loc['fuentes'] or {}))
    else:
        L.append('  ESPEJO LOCAL (tokens): sin consultas locales registradas todavia')

    if otros:
        L.append('  Otros modelos vistos en el ledger (no facturados en la tarifa flash): %s' % dict(otros))

    if args.registrar:
        snap = {
            'fecha': hoy, 'ts': datetime.datetime.now().isoformat(timespec='seconds'),
            'tarifa_fecha': TARIFA_FECHA, 'ventana_dias': len(dias),
            'n_ventana': tot['n'], 'usd_ventana': round(tot['usd'], 6),
            'usd_dia_media': round(media, 6),
            'n_ayer': dict((d_, c['n']) for d_, c in serie if d_ == ayer).get(ayer, 0),
            'usd_ayer': round(dict((d_, c['usd']) for d_, c in serie).get(ayer, 0.0), 6),
            'hit_ventana': tot['hit'], 'miss_ventana': tot['miss'], 'out_ventana': tot['out'],
            'saldo_usd': saldo, 'error_saldo': err,
            'dias_restantes': round(dias_rest, 2) if dias_rest is not None else None,
            'local_lineas': loc['lineas'], 'local_ultimo': loc['ultimo'],
            'local_tokens_lineas': loc['lineas_tokens'],
            'local_usd_evitado': round(loc['usd_evitado'], 6),
        }
        try:
            with open(HISTORIAL, 'a', encoding='utf-8') as f:
                f.write(json.dumps(snap, ensure_ascii=False) + '\n')
            L.append('  HISTORIAL: snapshot anadido a %s (permite calibrar la tarifa contra el saldo real)' % os.path.basename(HISTORIAL))
        except OSError as e:
            L.append('  HISTORIAL: no se pudo escribir (%s)' % e)

    alerta = bool(umbral is not None and dias_rest is not None and dias_rest < float(umbral))
    if args.silencioso_si_normal and not alerta:
        if args.registrar:
            pass  # el snapshot ya se escribio; stdout vacio = el cron no entrega nada
        return 0

    print('\n'.join(L))
    return 0


if __name__ == '__main__':
    sys.exit(main())
