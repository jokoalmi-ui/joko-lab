#!/usr/bin/env python3
"""registrar_hel_diario.py — Instrumentación EXP-HEL-001.

Detecta preguntas de estado del usuario en las sesiones de HOY y las registra
en respuestas_hel.jsonl si no están ya. Cron diario sugerido: 22:30.

Uso: python3 registrar_hel_diario.py [-fecha YYYY-MM-DD]
  Sin argumentos: procesa hoy y los 2 dias anteriores (auto-backfill).
"""
import json, os, re, sys
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

SESIONES_DIR = os.environ.get('HEL_SESIONES_DIR', '/home/jokoalmi/joko-lab/04-operations/metrics/sesiones')
LEDGER = os.environ.get('HEL_LEDGER', '/home/jokoalmi/joko-lab/04-operations/metrics/respuestas_hel.jsonl')
TZ = ZoneInfo('Europe/Madrid')  # CET/CEST real; antes UTC+2 fijo (desfasaba 1 h en invierno)

RUIDO = [
    r'^\$', r'jokoalmi@', r'^cd ', r'^ls ', r'^python3? ', r'^cat ', r'^grep ',
    r'^bash ', r'^sudo ', r'^git ', r'^docker ', r'^nano ', r'^chmod', r'^cp ',
    r'^mv ', r'^rm ', r'^find ', r'^curl ', r'^source ', r'^export ', r'^kill',
    r'^http', r'^www\.', r'^\[IMPORTANT', r'^\[The user sent', r'^\*\*', r'^#',
    r'^&', r'^\./', r'^lms ', r'^npm ', r'^pip ', r'^systemctl', r'^ffmpeg',
    r'^el vapor', r'^igual prefiero', r'^he estado desmontando', r'^igual pregunto',
    r'^si , eso hay que', r'^el ID', r'^vamos a sustituir', r'^quiero mejorar',
    r'^quiero ejecutar', r'^dame en un txt', r'^la version correcta',
    r'^se puede seguir', r'^que no habia leido', r'^asi ya esta bastante',
    r'^tengamos 2', r'^analiza la infograf', r'^puedes enviarme',
    r'^voy a cambiar', r'^son 20 p[aá]ginas', r'^cerramos', r'^esto es un mensaje',
    r'^https://', r'^si$', r'^sigue', r'^contin[uú]a', r'^anota', r'^hazlo',
    r'^ok$', r'^vale$', r'^perfecto', r'^dime', r'^a ver',
    r'gin tonic', r'^descarga dolphin', r'^revisa porque estoy en la sesion',
    r'^si acabo', r'^dale por acabada',
    # C2 (14-ago-2026): patrones del golden set del corte (38 entradas ruido).
    # Ajustados al texto REAL del ledger (tildes, mayusculas, casos no listados
    # en el diseno). 'perfume' generico se descarto: rompia 2 genuinas
    # ("clasificacion de cada perfume").
    r'^ok reinicio', r'si con lo más urgente', r'entonces no queda nada',
    r'estado de la marea', r'entreno', r'sorteo', r'depende de que perfume sea',
    r'bolsa', r'carrusel', r'notebooklm', r'slides', r'infograf',
    r'a la disciplina', r'material aprovechable', r'chuncless', r'vamos con ello',
    r'coordinar sesiones', r'multi-agente', r'anota como norma',
    r'analiza el formato', r'independientemente de que valor', r'en 0\.3',
    r'analiza y anota', r'pregunta inversa', r'que aportaria',
    r'la tienes ya en lms studio', r'como definirias',
    r'de todas maneras en casa slide', r'coge la guia',
    r'se ha quedado muy corto', r'te doy a dejar los datos',
    r'he creado un directorio llamado usage', r'pasame esto',
    r'si comprueba', r'si y deja pendiente', r'al tope seg',
    r'revisa los comentarios', r'ese es el detalle', r'revisa ahora que puedes',
]

# Keywords de estado — el usuario pregunta sobre el SISTEMA
KEYWORDS_ESTADO = [
    'estado', 'pendiente', 'urgente', 'importante', 'revisa', 'revisión', 'revision',
    'analiza', 'informe', 'ledger', 'sistema', 'queda', 'completo', 'general',
    'actualiza las tareas', 'refactor', 'sesión activa', 'sesion activa',
    'lab', 'chequeo',
]

def es_ruido(t: str) -> bool:
    return any(re.search(p, t, re.IGNORECASE) for p in RUIDO)

def es_pregunta_estado(texto: str) -> bool:
    t = texto.strip().lower()
    if len(t) < 6 or len(t) > 300:
        return False
    if es_ruido(t):
        return False
    return any(kw in t for kw in KEYWORDS_ESTADO)

def cargar_existentes() -> set:
    """Conjunto de (fecha, descripcion[:50]) ya registradas."""
    vistos = set()
    if os.path.exists(LEDGER):
        with open(LEDGER) as f:
            for line in f:
                try:
                    d = json.loads(line)
                    vistos.add((d['ts'][:10], d['descripcion'][:50]))
                except Exception:
                    pass
    return vistos

def _parsear_fecha() -> tuple:
    """Devuelve (hoy, t0, t1) desde el argumento --fecha o la fecha actual."""
    hoy = sys.argv[2] if len(sys.argv) > 2 and sys.argv[1] == '--fecha' else datetime.now(TZ).strftime('%Y-%m-%d')
    t0 = datetime.strptime(hoy + ' 00:00', '%Y-%m-%d %H:%M').replace(tzinfo=TZ).timestamp()
    t1 = datetime.strptime(hoy + ' 23:59', '%Y-%m-%d %H:%M').replace(tzinfo=TZ).timestamp()
    return hoy, t0, t1

def _mensaje_valido(m: dict, d: dict, t0: float, t1: float) -> tuple | None:
    """Devuelve (ts, desc) si el mensaje es una pregunta de estado válida en el rango, si no None."""
    if not isinstance(m, dict) or m.get('role') != 'user':
        return None
    contenido = m.get('content', '')
    if not isinstance(contenido, str) or not es_pregunta_estado(contenido):
        return None
    ts = m.get('timestamp') or d.get('started_at') or 0
    if not isinstance(ts, (int, float)) or not (t0 <= ts <= t1):
        return None
    return (ts, contenido.strip()[:150])

def _mensajes_usuario(d: dict, t0: float, t1: float) -> list:
    """Mensajes de usuario de la sesión, en el rango temporal, que son preguntas de estado."""
    out = []
    for m in (d.get('messages') or []):
        r = _mensaje_valido(m, d, t0, t1)
        if r:
            out.append(r)
    return out

def _escanear_sesion(d: dict, hoy: str, t0: float, t1: float, existentes: set) -> list:
    """Extrae las preguntas de estado nuevas de una sesión."""
    nuevas = []
    for ts, desc in _mensajes_usuario(d, t0, t1):
        clave = (hoy, desc[:50])
        if clave in existentes:
            continue
        ts_iso = datetime.fromtimestamp(ts, TZ).isoformat()
        nuevas.append({
            'ts': ts_iso,
            'contexto': f'instrumentado {hoy} sesion {d.get("id","?")} ({d.get("source","")})',
            'tipo_pregunta': 'estado',
            'descripcion': desc,
            # QUE palabra disparo el match. Aditivo (03-nov-2026): permite
            # auditar falsos positivos a posteriori sin cambiar el filtro,
            # que se mantiene intacto para no romper la serie historica.
            'match': next((k for k in KEYWORDS_ESTADO if k in desc.lower()), ''),
            # Confianza del match (03-nov-2026). El filtro historico deja pasar
            # texto que solo MENCIONA estado ('analiza', 'lab', 'revisa'): en el
            # backfill 30-09..02-11 solo el 27% eran preguntas con '?'. No se
            # cambia el filtro (romperia la serie); se estratifica al analizar.
            'confianza_match': ('alta' if ('?' in desc or
                                next((k for k in KEYWORDS_ESTADO if k in desc.lower()), '') in
                                ('estado', 'pendiente', 'completo', 'fallo', 'error', 'funciona',
                                 'terminado', 'resultado', 'avance', 'urgente'))
                                else 'baja'),
            # C1 (14-ago-2026): activacion_declarada deja de escribirse como true fijo.
            # Auto-reporte != metrica (leccion KVC-001). Metrica primaria fase 2 =
            # activacion_verificada (rellenada por tools/verificar_hel.py, C3).
            'activacion_declarada': None,
            # Intervencion fase 2 (opcion A, 14-ago-2026): true mientras la
            # activacion deliberada este activa. Permite medir por periodo sin
            # depender de la fecha (cada paso medido con su propia traza).
            'intervencion_activa': True,
            'activacion_verificada': None,
            'evidencia': None,
            'resultado': 'desconocido',
            'coste_tokens': None,
            'latencia': None,
        })
        existentes.add(clave)
    return nuevas

def _resolver_fichero(hoy: str):
    """Devuelve (ruta|None, comprimido, motivo). Distingue 'sin sesiones hoy' de 'patron roto'."""
    import glob
    d = hoy.replace('-', '')
    cands = [
        (f'sesiones-delta-{d}.jsonl', False),
        (f'sesiones-{d}.jsonl', False),
        (f'sesiones-delta-{d}.jsonl.zst', True),
        (f'sesiones-{d}.jsonl.zst', True),
    ]
    for name, comp in cands:
        p = os.path.join(SESIONES_DIR, name)
        if os.path.exists(p):
            return p, comp, 'ok'
    recientes = sorted(glob.glob(os.path.join(SESIONES_DIR, 'sesiones-delta-*.jsonl')))
    if not recientes:
        recientes = sorted(glob.glob(os.path.join(SESIONES_DIR, '*sesiones-*.jsonl*')))
    if recientes:
        return None, False, f'sin sesiones hoy (patron correcto; ultimo fichero: {os.path.basename(recientes[-1])})'
    return None, False, 'PATRON_ROTO'


def _sesiones_en_state_db(fecha: str) -> int:
    """Cuantas sesiones hay en state.db para ese dia (fuente original)."""
    import sqlite3
    db = os.path.expanduser('~/.hermes/state.db')
    if not os.path.exists(db):
        return -1
    t0 = datetime.strptime(fecha + ' 00:00', '%Y-%m-%d %H:%M').replace(tzinfo=TZ).timestamp()
    t1 = datetime.strptime(fecha + ' 23:59', '%Y-%m-%d %H:%M').replace(tzinfo=TZ).timestamp()
    try:
        con = sqlite3.connect(f'file:{db}?mode=ro', uri=True, timeout=5)
        n = con.execute('SELECT count(*) FROM sessions WHERE started_at >= ? AND started_at < ?',
                        (t0, t1)).fetchone()[0]
        con.close()
        return n
    except Exception:
        return -1


def _iter_lineas(fpath, comp):
    """Itera lineas del fichero, descomprimiendo .zst con el binario zstd."""
    import subprocess
    if comp:
        with subprocess.Popen(['zstd', '-dc', fpath], stdout=subprocess.PIPE,
                              text=True, errors='ignore') as p:
            for line in p.stdout:
                yield line
    else:
        with open(fpath, errors='ignore') as f:
            for line in f:
                yield line


def _procesar(hoy, t0, t1, fpath, comp) -> int:
    antes = os.path.getsize(LEDGER) if os.path.exists(LEDGER) else 0
    existentes = cargar_existentes()

    nuevas = []
    for line in _iter_lineas(fpath, comp):
        try:
            d = json.loads(line)
        except Exception:
            continue
        nuevas.extend(_escanear_sesion(d, hoy, t0, t1, existentes))

    with open(LEDGER, 'a') as f:
        for e in nuevas:
            f.write(json.dumps(e, ensure_ascii=False) + '\n')
    despues = os.path.getsize(LEDGER)
    print(f'{hoy}: {len(nuevas)} nuevas respuestas de estado registradas'
          f' (fuente {os.path.basename(fpath)}; ledger {antes}->{despues} bytes)')
    for e in nuevas:
        print(f"  {e['ts'][:16]} | {e['descripcion'][:60]}")
    return len(nuevas)


def _rango(fecha: str) -> tuple:
    t0 = datetime.strptime(fecha + ' 00:00', '%Y-%m-%d %H:%M').replace(tzinfo=TZ).timestamp()
    t1 = datetime.strptime(fecha + ' 23:59', '%Y-%m-%d %H:%M').replace(tzinfo=TZ).timestamp()
    return t0, t1


def main():
    """Por defecto procesa hoy y los 2 dias anteriores (auto-backfill).

    Motivo: el consolidador escribe el delta del dia anterior a las 22:30 y este
    job corre a las 22:35. Si el consolidador falla, el PC esta apagado o el
    fichero llega tarde, el dia se perderia para siempre. Con 3 dias de ventana
    el registro se autorrepara sin intervencion. --fecha sigue forzando UN dia.
    """
    if '--fecha' in sys.argv:
        objetivo = [sys.argv[sys.argv.index('--fecha') + 1]]
        estricto = True
    else:
        hoy = datetime.now(TZ).date()
        objetivo = [(hoy - timedelta(days=k)).isoformat() for k in (2, 1, 0)]
        estricto = False

    total = 0
    alerta = False
    for fecha in objetivo:
        t0, t1 = _rango(fecha)
        fpath, comp, motivo = _resolver_fichero(fecha)
        if fpath is None:
            if motivo == 'PATRON_ROTO':
                print(f'ERROR {fecha}: no existe ningun sesiones-delta-*.jsonl ni '
                      f'sesiones-{fecha}.jsonl — el patron de fichero esta roto', file=sys.stderr)
                sys.exit(1)
            n = _sesiones_en_state_db(fecha) if fecha != datetime.now(TZ).strftime('%Y-%m-%d') else 0
            if n > 0:
                # El dato existe en la fuente pero no hay fichero consolidado:
                # perdida silenciosa de consolidacion (paso del 01 al 15-oct-2026).
                print(f'AVISO {fecha}: {motivo} PERO state.db tiene {n} sesiones '
                      f'— falta consolidar (ver tools/mantenimiento/reconsolidar_rango.py)',
                      file=sys.stderr)
                alerta = True
                continue
            print(f'{fecha}: {motivo}')
            continue
        total += _procesar(fecha, t0, t1, fpath, comp)
    if len(objetivo) > 1:
        print(f'TOTAL ventana {objetivo[0]}..{objetivo[-1]}: {total} nuevas')
    if alerta:
        print('ALERTA: hay dias con sesiones en state.db y sin fichero consolidado', file=sys.stderr)
        sys.exit(2)
    if estricto and total == 0:
        return


if __name__ == '__main__':
    main()
