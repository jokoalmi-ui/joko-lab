#!/usr/bin/env python3
"""Sanea piezas.json para el archivo de F1 y verifica la copia por hash.

Se ejecuta desde /tmp/f1-contexto. Redacta las dos piezas con datos personales
(MEMORY.md y USER.md literales) al copiar piezas.json al archivo del lab, y
comprueba por md5 que todo lo demas se copio byte a byte.
"""
import hashlib
import json
import os

SRC = '/tmp/f1-contexto'
DEST = '/home/jokoalmi/joko-lab/01-knowledge/experiments/F1-contexto-fijo'


def md5(p):
    h = hashlib.md5()
    with open(p, 'rb') as fh:
        for b in iter(lambda: fh.read(65536), b''):
            h.update(b)
    return h.hexdigest()


piezas_src = os.path.join(SRC, 'piezas.json')
md5_piezas = md5(piezas_src)

d = json.load(open(piezas_src, encoding='utf-8'))
print('claves piezas.json:', list(d.keys()))
redactados = {}
for k, nombre in (('B2_memoria', 'MEMORY.md'), ('B2_user', 'USER.md')):
    v = d.get(k)
    n = len(v) if isinstance(v, str) else 0
    redactados[k] = (nombre, n)
    d[k] = (
        '[REDACTADO AL ARCHIVAR] Texto literal de %s (%d chars) eliminado de esta copia '
        'por contener datos personales. Regenerable con recolectar.py; md5 del piezas.json '
        'original en /tmp: %s' % (nombre, n, md5_piezas)
    )

d['_meta'] = dict(d.get('_meta') or {})
d['_meta']['archivado'] = {
    'fecha': '2026-09-16',
    'motivo': 'cierre del experimento F1 (coste del contexto fijo)',
    'redactado': {k: {'fuente': v[0], 'chars_eliminados': v[1]} for k, v in redactados.items()},
    'md5_piezas_original': md5_piezas,
}
out = os.path.join(DEST, 'piezas.json')
with open(out, 'w', encoding='utf-8') as fh:
    json.dump(d, fh, ensure_ascii=False, indent=1)
print('escrito', out, os.path.getsize(out), 'B')

# verificacion de la copia: hash origen == hash destino en todo lo copiado tal cual
excluidos = {'piezas.json', 'README.md', 'sanear_y_verificar.py'}
ok = mal = 0
for root, _dirs, files in os.walk(SRC):
    if '__pycache__' in root:
        continue
    for fn in files:
        rel = os.path.relpath(os.path.join(root, fn), SRC)
        if rel in excluidos or fn in ('system_prompt.txt', 'session_prompt.txt'):
            continue
        if md5(os.path.join(SRC, rel)) == md5(os.path.join(DEST, rel)):
            ok += 1
        else:
            mal += 1
            print('DESAJUSTE:', rel)
print('copias verificadas por md5: %d correctas, %d desajustes' % (ok, mal))

for f in ('fijo/system_prompt.txt', 'fijo/session_prompt.txt', 'piezas.json'):
    print('EXCLUIDO/REDACTADO %s -> %s B, md5 %s'
          % (f, os.path.getsize(os.path.join(SRC, f)), md5(os.path.join(SRC, f))))
