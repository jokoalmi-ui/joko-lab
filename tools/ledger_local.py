#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ledger_local.py — ESPEJO LOCAL del instrumento de coste (Joko Lab).

Registra TAMBIEN los tokens que consume la inferencia LOCAL (LM Studio :1234,
Ollama :11434) para poder calcular "USD evitados" con la MISMA tabla de tarifas
que usa coste_ahorro.py para DeepSeek. Solo OBSERVA y REGISTRA: no cambia nada.

Por que existe: el ledger cloud (pipeline_obs.jsonl) registra SOLO DeepSeek, asi
que el lado local no era medible. Aqui cada consulta local deja una linea con sus
tokens; el informe diario ya puede comparar cloud (gastado) vs local (evitado).

Uso:
  # desde el router (JSON crudo de la API por stdin):
  printf '%s' "$resp" | ledger_local.py --desde-stdin --motor lmstudio \
      --modelo X --fuente llm-router.sh:auto --latencia 4.2
  # o con valores ya medidos:
  ledger_local.py --tokens 812 145 --motor ollama --modelo qwen2.5:7b
  # resumen agregado:
  ledger_local.py --resumen --dias 7

Salida: info de la linea registrada (o el resumen) a stdout. Nunca debe romper
al llamante: cualquier fallo se avisa por stderr y sale con codigo 0.
Creado: 2026-10-11. Autor: Hermes (agente) con autorizacion explicita del usuario.
"""
import argparse
import collections
import datetime
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:                                                            # tarifa unica
    from coste_ahorro import TARIFA, es_peak, TARIFA_FECHA      # noqa: F401
except Exception:                                               # degradacion segura
    TARIFA = {'deepseek-v4-flash': {'hit': 0.003, 'miss': 0.15, 'out': 0.60}}
    TARIFA_FECHA = 'n/d'

    def es_peak(ts, gmtoff):
        return False

BASE = '/home/jokoalmi/joko-lab'
LEDGER = os.path.join(BASE, '04-operations/metrics/ahorro_local_ledger.jsonl')
MODELO_TARIFA = 'deepseek-v4-flash'   # contra lo que se compara el ahorro


def ahora_iso():
    """Hora local medida por el reloj del sistema (no se asume)."""
    return datetime.datetime.now().isoformat(timespec='seconds')


def ahora_ts():
    return datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')


def a_float(x):
    """Normaliza numeros en formato local ('2,13' -> 2.13). None si no se puede."""
    if x is None:
        return None
    try:
        return float(str(x).replace(',', '.'))
    except Exception:
        return None


def extraer(d, motor):
    """Devuelve (prompt_tokens, completion_tokens, modelo, latencia_s) del JSON."""
    modelo = str(d.get('model') or '?')
    lat_ns = d.get('total_duration')          # Ollama nativo (ns)
    lat = round(lat_ns / 1e9, 2) if isinstance(lat_ns, (int, float)) and lat_ns else None
    if not motor:
        motor = 'ollama' if ('prompt_eval_count' in d or 'eval_count' in d) else 'lmstudio'
    u = d.get('usage') or {}
    p = u.get('prompt_tokens')
    c = u.get('completion_tokens')
    if p is None:
        p = d.get('prompt_eval_count')
    if c is None:
        c = d.get('eval_count')
    return (motor, int(p) if isinstance(p, (int, float)) else None,
            int(c) if isinstance(c, (int, float)) else None, modelo, lat)


def calcular(prompt_t, compl_t, factor, tarifa):
    """USD evitados frente a DeepSeek. `usd_evitado` = escenario sin cache (base
    conservadora: 1 miss = 50 hits); `usd_si_cache` = escenario optimista."""
    u_miss = prompt_t / 1e6 * tarifa['miss'] * factor
    u_out = compl_t / 1e6 * tarifa['out'] * factor
    u_hit = prompt_t / 1e6 * tarifa['hit'] * factor
    return round(u_miss + u_out, 8), round(u_hit + u_out, 8)


def escribir(linea, path):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(linea, ensure_ascii=False) + '\n')
        return True
    except OSError as e:
        print('[aviso] no se pudo escribir el ledger local: %s' % e, file=sys.stderr)
        return False


def registrar(motor, modelo, prompt_t, compl_t, fuente, latencia, path, etiqueta=None,
              ok=True):
    tarifa = TARIFA[MODELO_TARIFA]
    ts = ahora_ts()
    gmtoff = time.localtime().tm_gmtoff
    peak = es_peak(ts, gmtoff)
    factor = 2.0 if peak else 1.0
    if prompt_t is None or compl_t is None:
        print('[aviso] la respuesta no trae tokens (usage/prompt_eval_count): no se registra',
              file=sys.stderr)
        return None
    usd, usd_cache = calcular(prompt_t, compl_t, factor, tarifa)
    latencia = a_float(latencia)
    linea = {'ts': ts, 'motor': motor, 'modelo': modelo,
             'prompt_tokens': prompt_t, 'completion_tokens': compl_t,
             'total_tokens': prompt_t + compl_t,
             'usd_evitado': usd, 'usd_si_cache': usd_cache, 'factor_hora': factor,
             'peak': peak, 'fuente': fuente, 'etiqueta': etiqueta,
             'latencia_s': latencia, 'ok': bool(ok)}
    if escribir(linea, path):
        print('ESPEJO LOCAL: +1 linea  %s %s  prompt=%d out=%d  %s USD evitados  (%s)' % (
            motor, modelo, prompt_t, compl_t, ('%.6f' % usd).rstrip('0'), fuente))
        return linea
    return None


def leer(path):
    out = []
    if not os.path.exists(path):
        return out
    with open(path, encoding='utf-8', errors='replace') as f:
        for l in f:
            l = l.strip()
            if not l:
                continue
            try:
                out.append(json.loads(l))
            except Exception:
                continue
    return out


def resumen(dias, path):
    rows = [r for r in leer(path) if r.get('ok')]
    hoy = datetime.date.today()
    desde = (hoy - datetime.timedelta(days=dias - 1)).isoformat()
    ventana = [r for r in rows if str(r.get('ts', ''))[:10] >= desde]
    L = []
    L.append('ESPEJO LOCAL — resumen (%s, motor local vs tarifa %s de %s)' % (
        datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), MODELO_TARIFA, TARIFA_FECHA))
    L.append('Ledger: %s (%d lineas; %d en la ventana de %d dias)' % (
        os.path.basename(path), len(rows), len(ventana), dias))
    if not rows:
        L.append('  sin consultas locales registradas todavia')
        return '\n'.join(L)

    motores = collections.Counter(r.get('motor', '?') for r in rows)
    L.append('  motores (total): %s' % dict(motores))
    p = sum(r.get('prompt_tokens') or 0 for r in ventana)
    c = sum(r.get('completion_tokens') or 0 for r in ventana)
    usd = sum(r.get('usd_evitado') or 0 for r in ventana)
    usd_cache = sum(r.get('usd_si_cache') or 0 for r in ventana)
    peak = sum(1 for r in ventana if r.get('peak'))
    L.append('  ventana: n=%d  prompt %.2fM + salida %.3fM tokens' % (len(ventana), p / 1e6, c / 1e6))
    L.append('  USD evitados (equivalente DeepSeek): %.4f USD  [rango %.4f (si cacheado) - %.4f (sin cache)]'
             % (usd, usd_cache, usd))
    L.append('    (%d de las %d consultas cayeron en franja peak, x2)' % (peak, len(ventana)))
    por_dia = collections.defaultdict(float)
    for r in ventana:
        por_dia[str(r.get('ts', ''))[:10]] += r.get('usd_evitado') or 0
    if por_dia:
        L.append('    serie: ' + ' | '.join('%s %.4f' % (d[5:], v) for d, v in sorted(por_dia.items())))
    fuentes = collections.Counter(r.get('fuente', '?') for r in rows)
    L.append('  fuentes: %s' % dict(fuentes))
    lat = [r.get('latencia_s') for r in ventana if isinstance(r.get('latencia_s'), (int, float))]
    if lat:
        L.append('  latencia local: media %.2fs (min %.2f, max %.2f)' % (
            sum(lat) / len(lat), min(lat), max(lat)))
    return '\n'.join(L)


def main():
    ap = argparse.ArgumentParser(description='Espejo local del instrumento de coste')
    ap.add_argument('--desde-stdin', action='store_true', help='leer el JSON crudo de la API por stdin')
    ap.add_argument('--tokens', nargs=2, type=int, metavar=('PROMPT', 'COMPLETION'))
    ap.add_argument('--motor', default=None, help='lmstudio | ollama (si se omite, se detecta)')
    ap.add_argument('--modelo', default=None)
    ap.add_argument('--fuente', default='manual')
    ap.add_argument('--etiqueta', default=None)
    ap.add_argument('--latencia', default=None,
                    help='segundos; acepta coma decimal (se normaliza)')
    ap.add_argument('--resumen', action='store_true')
    ap.add_argument('--dias', type=int, default=7)
    ap.add_argument('--ledger', default=LEDGER, help='ruta alternativa (pruebas)')
    args = ap.parse_args()

    if args.resumen:
        print(resumen(args.dias, args.ledger))
        return 0

    if args.desde_stdin:
        crudo = sys.stdin.read()
        try:
            d = json.loads(crudo)
        except Exception as e:
            print('[aviso] JSON ilegible por stdin: %s' % e, file=sys.stderr)
            return 0
        if not isinstance(d, dict) or ('error' in d and not (d.get('usage') or d.get('eval_count'))):
            print('[aviso] la respuesta trae error o no es un dict: no se registra', file=sys.stderr)
            return 0
        motor, p, c, modelo, lat = extraer(d, args.motor)
        registrar(motor, args.modelo or modelo, p, c, args.fuente,
                  args.latencia if args.latencia is not None else lat, args.ledger, args.etiqueta)
        return 0

    if args.tokens:
        motor = args.motor or 'manual'
        registrar(motor, args.modelo or '?', args.tokens[0], args.tokens[1],
                  args.fuente, args.latencia, args.ledger, args.etiqueta)
        return 0

    ap.print_help()
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:      # nunca romper al llamante (el router confia en esto)
        print('[aviso] ledger_local fallo: %s' % e, file=sys.stderr)
        sys.exit(0)
