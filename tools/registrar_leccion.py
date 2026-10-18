#!/usr/bin/env python3
"""registrar_leccion.py — Ledger de lecciones estructurado (memoria episódica).

Cierra el GAP de memoria episódica del lab (13-ago-2026, análisis
"Memoria de agentes 3 tipos"): el lab registraba fallos informalmente en
pitfalls de skills; este ledger los estructura como episodios buscables
(tried_list → causa_raiz → fix), igual que el patrón Episode del carrusel.

USO:
    # Registrar una lección (modo interactivo por argumentos)
    python3 registrar_leccion.py add \
        --dominio router \
        --titulo "R1 se corta con max_tokens bajo" \
        --tried "max_tokens=400, R1 razona y se corta en el pensamiento" \
        --causa "R1-14B razona antes de responder; 400 tokens no bastan" \
        --fix "MAX_TOKENS=1200 para tareas de resumen (router respeta env)" \
        --ref "tools/llm-router.sh"

    # Buscar lecciones por dominio o texto
    python3 registrar_leccion.py buscar "max_tokens"
    python3 registrar_leccion.py buscar --dominio router

    # Listar todo
    python3 registrar_leccion.py listar

Salida: JSONL en 04-operations/metrics/lecciones_ledger.jsonl.
Regla RULE-008: hace backup del ledger antes de escribir.
"""
import json, os, shutil, sys
from datetime import datetime, timezone, timedelta

LEDGER = '/home/jokoalmi/joko-lab/04-operations/metrics/lecciones_ledger.jsonl'
TZ = timezone(timedelta(hours=2))

CAMPOS = ['dominio', 'titulo', 'tried', 'causa_raiz', 'fix', 'ref']


def _backup():
    """RULE-008: backup antes de escribir."""
    if os.path.exists(LEDGER):
        shutil.copy2(LEDGER, LEDGER + '.bak-20260814')


def _proximo_id():
    if not os.path.exists(LEDGER):
        return 'LEC-20260814-001'
    n = 0
    with open(LEDGER, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
                lec = d.get('leccion_id', '')
                if lec.startswith('LEC-'):
                    num = int(lec.rsplit('-', 1)[-1])
                    n = max(n, num)
            except Exception:
                continue
    return f'LEC-20260814-{n + 1:03d}'


def add(args):
    """Añade una lección. Verifica que no exista un duplicado exacto."""
    datos = {}
    for c in CAMPOS:
        v = getattr(args, c, None)
        if v:
            datos[c] = v
    if not datos.get('titulo'):
        print('ERROR: --titulo es obligatorio', file=sys.stderr)
        sys.exit(1)

    # Anti-duplicado: mismo título (normalizado) ya registrado
    titulo_norm = datos['titulo'].strip().lower()
    if os.path.exists(LEDGER):
        with open(LEDGER, encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    d = json.loads(line)
                    if d.get('titulo', '').strip().lower() == titulo_norm:
                        print(f'⚠️  Ya existe: {d.get("leccion_id")} "{d.get("titulo")}" '
                              f'({d.get("fecha")}) — no duplicar', file=sys.stderr)
                        sys.exit(2)
                except Exception:
                    continue

    _backup()
    entrada = {
        'leccion_id': _proximo_id(),
        'fecha': datetime.now(TZ).strftime('%Y-%m-%d %H:%M %Z'),
        **datos,
    }
    with open(LEDGER, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entrada, ensure_ascii=False) + '\n')
    print(f'✅ Lección {entrada["leccion_id"]} registrada')
    print(json.dumps(entrada, ensure_ascii=False, indent=2))


def buscar(args):
    """Busca por texto o por dominio (búsqueda simple en todos los campos)."""
    if not os.path.exists(LEDGER):
        print('Ledger vacío (aún no hay lecciones)')
        return
    q = getattr(args, 'texto', None)
    dom = getattr(args, 'dominio', None)
    encontradas = 0
    with open(LEDGER, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except Exception:
                continue
            if dom and d.get('dominio', '').lower() != dom.lower():
                continue
            if q:
                blob = json.dumps(d, ensure_ascii=False).lower()
                if q.lower() not in blob:
                    continue
            encontradas += 1
            print(f'--- {d.get("leccion_id")} [{d.get("dominio")}] {d.get("fecha")}')
            print(f'    {d.get("titulo")}')
            if d.get('tried'):
                print(f'    INTENTOS: {d["tried"]}')
            if d.get('causa_raiz'):
                print(f'    CAUSA: {d["causa_raiz"]}')
            if d.get('fix'):
                print(f'    FIX: {d["fix"]}')
            if d.get('ref'):
                print(f'    REF: {d["ref"]}')
    if encontradas == 0:
        print('Sin resultados')
    else:
        print(f'\n{encontradas} lección(es)')


def listar(_args):
    buscar(_args)


def main():
    import argparse
    p = argparse.ArgumentParser(add_help=False)
    sub = p.add_subparsers(dest='sub', required=True)

    a = sub.add_parser('add')
    for c in CAMPOS:
        a.add_argument(f'--{c}')

    b = sub.add_parser('buscar')
    b.add_argument('texto', nargs='?', default=None)
    b.add_argument('--dominio', default=None)

    sub.add_parser('listar')

    args = p.parse_args(sys.argv[1:])
    if args.sub == 'add':
        add(args)
    elif args.sub in ('buscar', 'listar'):
        buscar(args)
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == '__main__':
    main()
