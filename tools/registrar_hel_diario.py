#!/usr/bin/env python3
"""registrar_hel_diario.py — Instrumentación EXP-HEL-001.

Detecta preguntas de estado del usuario en las sesiones de HOY y las registra
en respuestas_hel.jsonl si no están ya. Cron diario sugerido: 22:30.

Uso: python3 registrar_hel_diario.py [--fecha YYYY-MM-DD]
"""
import json, os, re, sys
from datetime import datetime, timezone, timedelta

SESIONES_DIR = '/home/jokoalmi/joko-lab/04-operations/metrics/sesiones'
LEDGER = '/home/jokoalmi/joko-lab/04-operations/metrics/respuestas_hel.jsonl'
TZ = timezone(timedelta(hours=2))

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

def main():
    hoy, t0, t1 = _parsear_fecha()

    existentes = cargar_existentes()
    fname = f'sesiones-{hoy.replace("-", "")}.jsonl'
    fpath = os.path.join(SESIONES_DIR, fname)
    if not os.path.exists(fpath):
        print(f'  {hoy}: sin sesiones (archivo {fname} no existe)')
        return

    nuevas = []
    with open(fpath) as f:
        for line in f:
            try:
                d = json.loads(line)
            except Exception:
                continue
            nuevas.extend(_escanear_sesion(d, hoy, t0, t1, existentes))

    with open(LEDGER, 'a') as f:
        for e in nuevas:
            f.write(json.dumps(e, ensure_ascii=False) + '\n')
    print(f'{hoy}: {len(nuevas)} nuevas respuestas de estado registradas')
    for e in nuevas:
        print(f"  {e['ts'][:16]} | {e['descripcion'][:60]}")

if __name__ == '__main__':
    main()
