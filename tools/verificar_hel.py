#!/usr/bin/env python3
"""verificar_hel.py — Verificación automática de activación (C3, EXP-HEL-001 fase 2).

Replica el verifier manual usado en el corte del 14-ago-2026:
- Para cada entrada de respuestas_hel.jsonl con activacion_verificada = null,
  localiza la sesión (id en 'contexto') y el user message cuyo timestamp esté
  en ±180s del ts de la entrada.
- Comprueba si el PRIMER assistant message posterior tuvo tool_calls reales
  (regla de la PRIMERA respuesta, corregida el 10-ago tras el falso 100%).
- Rellena activacion_verificada (true/false) + evidencia.
- Entradas sin user message en rango: se dejan null y se listan (revisión manual).

Solo lectura salvo la escritura final sobre el ledger (con backup previo RULE-008).
Uso: python3 tools/verificar_hel.py [--dry-run] [--fecha YYYY-MM-DD]
"""
import argparse, ast, json, os, re, shutil, sys
from datetime import datetime, timezone, timedelta

SESIONES_DIR = '/home/jokoalmi/joko-lab/04-operations/metrics/sesiones'
LEDGER = '/home/jokoalmi/joko-lab/04-operations/metrics/respuestas_hel.jsonl'
TZ = timezone(timedelta(hours=2))
VENTANA_S = 180  # ±180s, misma regla que el corte


def _epoch(ts_iso: str) -> float:
    """Convierte el ts ISO del ledger (con offset +02:00) a epoch."""
    try:
        return datetime.fromisoformat(ts_iso).timestamp()
    except Exception:
        return 0.0


def _tool_calls_reales(raw) -> list:
    """tool_calls llega serializado como string ('None' o repr de lista)."""
    if raw is None:
        return []
    if isinstance(raw, list):
        return raw
    s = str(raw).strip()
    if not s or s == 'None':
        return []
    try:
        parsed = ast.literal_eval(s)
        return parsed if isinstance(parsed, list) else []
    except Exception:
        # JSON válido o fallback: cualquier contenido distinto de None cuenta
        try:
            parsed = json.loads(s)
            return parsed if isinstance(parsed, list) else []
        except Exception:
            return [] if s in ('', 'None', 'null') else [{'id': s}]


def _id_sesion(contexto: str) -> str | None:
    m = re.search(r'sesion\s+([A-Za-z0-9_]+)', contexto or '')
    return m.group(1) if m else None


def _cargar_sesiones(fecha: str) -> list:
    fpath = os.path.join(SESIONES_DIR, f'sesiones-{fecha}.jsonl')
    if not os.path.exists(fpath):
        return []
    out = []
    with open(fpath) as f:
        for line in f:
            try:
                out.append(json.loads(line))
            except Exception:
                continue
    return out


def _verificar_entrada(entrada: dict, sesiones: list) -> tuple:
    """Devuelve (verificada: bool|None, evidencia: str|None, motivo: str|None)."""
    sid = _id_sesion(entrada.get('contexto', ''))
    if not sid:
        return None, None, 'sin id de sesion en contexto'
    sesion = next((s for s in sesiones if s.get('id') == sid), None)
    if not sesion:
        return None, None, f'sesion {sid} no encontrada en sesiones-{sid[:8]}.jsonl'
    msgs = sesion.get('messages') or []
    target = _epoch(entrada.get('ts', ''))
    # user message más cercano dentro de la ventana
    mejor = None
    mejor_d = VENTANA_S + 1
    for i, m in enumerate(msgs):
        if not isinstance(m, dict) or m.get('role') != 'user':
            continue
        ts = m.get('timestamp')
        if not isinstance(ts, (int, float)):
            continue
        d = abs(ts - target)
        if d <= VENTANA_S and d < mejor_d:
            mejor = (i, m)
            mejor_d = d
    if not mejor:
        return None, None, f'no hay user message en +-{VENTANA_S}s del ts'
    i_user = mejor[0]
    for m in msgs[i_user + 1:]:
        if not isinstance(m, dict) or m.get('role') != 'assistant':
            continue
        tcs = _tool_calls_reales(m.get('tool_calls'))
        if tcs:
            # tool_name del primer mensaje tool posterior, si existe
            tool = None
            for t in msgs[i_user + 1:]:
                if isinstance(t, dict) and t.get('role') == 'tool' and t.get('tool_call_id') == tcs[0].get('call_id', tcs[0].get('id')):
                    tool = t.get('tool_name')
                    break
            ev = f'tools: {tool}' if tool else 'primera respuesta con tool_calls'
            return True, ev, None
        # primer assistant message sin tool_calls: respuesta de memoria
        return False, 'primera respuesta sin tool_calls (memoria)', None
    return None, None, 'sin assistant message posterior'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true', help='no escribe el ledger')
    ap.add_argument('--fecha', default=None, help='solo entradas con ts de esta fecha (YYYY-MM-DD)')
    args = ap.parse_args()

    with open(LEDGER) as f:
        lineas = f.readlines()
    entradas = []
    for ln in lineas:
        try:
            entradas.append(json.loads(ln))
        except Exception:
            entradas.append(None)

    pendientes = []
    for i, e in enumerate(entradas):
        if e is None or e.get('activacion_verificada') is not None:
            continue
        if args.fecha and not str(e.get('ts', '')).startswith(args.fecha):
            continue
        pendientes.append((i, e))

    if not pendientes:
        print('  nada pendiente de verificar')
        return

    # agrupar por fecha de sesión para cargar cada archivo una vez
    por_fecha = {}
    for i, e in pendientes:
        sid = _id_sesion(e.get('contexto', ''))
        fecha = sid[:8] if sid and len(sid) >= 8 else str(e.get('ts', ''))[:10].replace('-', '')
        por_fecha.setdefault(fecha, set()).add(i)
    cache_sesiones = {f: _cargar_sesiones(f) for f in por_fecha}

    verificadas = 0
    sin_matchear = []
    for i, e in pendientes:
        sid = _id_sesion(e.get('contexto', ''))
        fecha = sid[:8] if sid and len(sid) >= 8 else str(e.get('ts', ''))[:10].replace('-', '')
        v, ev, motivo = _verificar_entrada(e, cache_sesiones.get(fecha, []))
        if v is None:
            sin_matchear.append((i, e, motivo))
            continue
        entradas[i] = dict(e)
        entradas[i]['activacion_verificada'] = v
        entradas[i]['evidencia'] = ev
        verificadas += 1

    if not args.dry_run and verificadas:
        # RULE-008: backup antes de escribir
        bak = LEDGER + '.bak-' + datetime.now(TZ).strftime('%Y%m%d')
        if not os.path.exists(bak):
            shutil.copy2(LEDGER, bak)
        with open(LEDGER, 'w') as f:
            for e in entradas:
                f.write(json.dumps(e, ensure_ascii=False) + '\n')
        print(f'  ledger actualizado ({verificadas} verificaciones); backup: {os.path.basename(bak)}')
    elif args.dry_run:
        print(f'  [dry-run] {verificadas} verificaciones listas para escribir (sin tocar ledger)')
    else:
        print('  sin cambios (solo quedan entradas sin matchear)')

    for i, e, motivo in sin_matchear:
        print(f'  SIN MATCHEAR #{i+1} | {e.get("ts","")[:16]} | {motivo} | {e.get("descripcion","")[:60]}')
    print(f'  resumen: {verificadas} verificadas, {len(sin_matchear)} sin matchear')


if __name__ == '__main__':
    main()
