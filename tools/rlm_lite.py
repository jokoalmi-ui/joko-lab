#!/usr/bin/env python3
"""
rlm_lite.py — consulta por CODIGO sobre un corpus local (RLM-lite) — Joko Lab.

Origen: replica a escala de lab del mecanismo de *Recursive Language Models*
(arXiv 2512.24601v1), validada en el experimento del 2026-09-18
(research/analisis-rlm-experimento-20260918.md): 3/4 preguntas de agregacion global
resueltas, frente a 0/4 del patron "fragmentos top-k" y 0/4 del patron "indice".

Idea: el modelo raiz NO ve el corpus; solo su tamano y su estructura. Lo inspecciona
escribiendo codigo (grep/count/peek/meta/sizes) y cierra con FINAL(...).

Uso:
  python3 rlm_lite.py --corpus RUTA [--pregunta "..."]... [--brazos rlm,rag,truncado]
                      [--out JSON] [--max-iters N]
  RUTA puede ser un fichero o un directorio (se recorren las extensiones de --ext).

Politica de seguridad (NO configurable, a proposito):
  1. REDACCION OBLIGATORIA en el punto unico de salida (call_llm): cualquier linea que
     contenga una marca sensible se sustituye por [LINEA REDACTADA] antes de enviarse
     al modelo. El contador se registra en el resultado.
  2. Sandbox: el codigo del modelo se ejecuta con builtins vacios, whitelist AST
     (sin import/open/exec/eval/dunder) y alarma de 5 s. Solo existen las funciones
     del corpus.
  3. Sin escrituras: la herramienta NUNCA modifica el corpus ni nada fuera de --out.
  4. La VERDAD de referencia NO la calcula esta herramienta: se cuenta aparte con
     Python/grep, para no autoevaluar al sujeto medido.
"""
import os, re, sys, json, time, glob, signal, argparse, subprocess, textwrap
from urllib import request as urlreq

SENSITIVE = ['sk-', 'password', 'contraseña', 'api_key', 'API_KEY', 'MEMORY.md',
             'USER.md', 'system_prompt', 'Maite', '1052590045', 'BEGIN PRIVATE',
             'ssh-rsa', 'auth.json', 'Bearer ']
MAX_ITERS = 8
MAX_OBS = 3000
LLM_TIMEOUT = 240
MAX_TOKENS = 4000
EXT_DEF = ['.md', '.txt', '.jsonl', '.py', '.sh', '.html', '.yaml', '.yml', '.csv']

# ---------------------------------------------------------------- credencial
def load_base_key():
    """Lee la credencial del lab DENTRO del proceso. Nunca se imprime ni se loguea."""
    key = None
    envp = '/home/jokoalmi/.hermes/.env'
    if os.path.exists(envp):
        for ln in open(envp):
            if ln.strip().startswith('DEEPSEEK_API_KEY='):
                key = ln.strip().split('=', 1)[1].strip()
                break
    base = 'https://api.deepseek.com/v1'
    try:
        a = json.load(open('/home/jokoalmi/.hermes/auth.json'))
        for e in (a.get('credential_pool') or {}).get('deepseek', []):
            if e.get('base_url'):
                base = e['base_url']
                break
    except Exception:
        pass
    return base, key

# ---------------------------------------------------------------- redaccion
_RED = {'lineas': 0, 'marcas': {}}

def redactar(texto):
    """Sustituye lineas con marcas sensibles. Devuelve (texto_limpio, n_lineas)."""
    if not texto:
        return texto, 0
    out, n = [], 0
    for ln in texto.split('\n'):
        hit = [m for m in SENSITIVE if m in ln]
        if hit:
            out.append('[LINEA REDACTADA: politica de sensibilidad del lab]')
            n += 1
            for m in hit:
                _RED['marcas'][m] = _RED['marcas'].get(m, 0) + 1
        else:
            out.append(ln)
    _RED['lineas'] += n
    return '\n'.join(out), n

# ---------------------------------------------------------------- corpus
class Corpus:
    def __init__(self, files, root):
        self.files = list(files)
        self.root = os.path.realpath(root)
        self.rel = [os.path.relpath(f, self.root) for f in self.files]
        self.cache = {}
        self.shadow = {}          # rel -> texto ya redactado (para grep/peek)
    def text(self, rel):
        if rel not in self.cache:
            p = os.path.realpath(os.path.join(self.root, rel))
            if not p.startswith(self.root):
                raise ValueError('ruta fuera del corpus')
            if not os.path.isfile(p):
                raise ValueError('no existe: ' + rel)
            self.cache[rel] = open(p, encoding='utf-8', errors='replace').read()
        return self.cache[rel]
    def rtext(self, rel):
        """Texto con las lineas sensibles ya redactadas (lo que si puede ver el modelo)."""
        if rel not in self.shadow:
            self.shadow[rel] = redactar(self.text(rel))[0]
        return self.shadow[rel]
    # --- API expuesta al modelo ---
    def list_files(self):
        return list(self.rel)
    def count(self, patron):
        rx = re.compile(patron)
        tot = hits = 0
        for rel in self.rel:
            m = rx.findall(self.rtext(rel))
            if m:
                hits += 1; tot += len(m)
        return {'coincidencias': tot, 'ficheros': hits}
    def grep(self, patron, maxhits=60):
        rx = re.compile(patron)
        out = {}
        for rel in self.rel:
            ls = [l for l in self.rtext(rel).splitlines() if rx.search(l)]
            if ls:
                out[rel] = ls[:5]
                if len(out) >= maxhits:
                    break
        return out
    def peek(self, rel, inicio=0, n=2000):
        return self.rtext(rel)[inicio:inicio + n]
    def meta(self, rel):
        t = self.text(rel)
        return {'bytes': len(t.encode()), 'lineas': t.count('\n') + 1}
    def sizes(self):
        return {rel: len(self.text(rel).encode()) for rel in self.rel}

def build_corpus(path, exts):
    p = os.path.realpath(os.path.expanduser(path))
    if os.path.isfile(p):
        return [p], os.path.dirname(p)
    if not os.path.isdir(p):
        raise SystemExit('ruta inexistente: ' + p)
    files = []
    for root, _, fs in os.walk(p):
        for f in sorted(fs):
            if os.path.splitext(f)[1].lower() in exts:
                files.append(os.path.join(root, f))
    return sorted(files), p

# ---------------------------------------------------------------- sandbox
def sandbox_exec(code, C):
    """Ejecuta el codigo del modelo: builtins vacios + whitelist AST + alarma 5 s."""
    import ast
    banned_nodes = (ast.Import, ast.ImportFrom, ast.Global, ast.Nonlocal, ast.ClassDef,
                    ast.Lambda, ast.Delete, ast.With, ast.Raise, ast.Try, ast.Assert,
                    ast.FunctionDef, ast.AsyncFunctionDef, ast.Await, ast.Yield)
    banned_names = {'__import__', 'open', 'exec', 'eval', 'compile', 'input', 'globals',
                    'locals', 'vars', 'dir', 'getattr', 'setattr', 'delattr', 'memoryview',
                    'breakpoint', 'exit', 'quit'}
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, banned_nodes):
            raise ValueError('nodo no permitido: ' + type(node).__name__)
        if isinstance(node, ast.Name) and node.id in banned_names:
            raise ValueError('nombre no permitido: ' + node.id)
        if isinstance(node, ast.Attribute) and '__' in node.attr:
            raise ValueError('atributo dunder no permitido')
        if isinstance(node, ast.Name) and node.id.startswith('__'):
            raise ValueError('nombre dunder no permitido')
    buf, fin = [], {}
    env = {'__builtins__': {}, 'len': len, 'range': range, 'enumerate': enumerate,
           'sorted': sorted, 'sum': sum, 'min': min, 'max': max, 'str': str, 'int': int,
           'float': float, 'list': list, 'dict': dict, 'set': set, 'tuple': tuple, 'abs': abs,
           'round': round, 'zip': zip, 'any': any, 'all': all, 'repr': repr,
           'regex': lambda t, p: re.findall(p, t),
           'print': lambda *a, **k: buf.append(' '.join(str(x) for x in a)),
           'FINAL': lambda *a: fin.setdefault('v', ' '.join(str(x) for x in a)),
           'list_files': C.list_files, 'grep': C.grep, 'count': C.count, 'peek': C.peek,
           'meta': C.meta, 'sizes': C.sizes}
    env['FINAL_VAR'] = env['FINAL']
    def _alarm(signum, frame):
        raise TimeoutError('codigo excedio 5s')
    signal.signal(signal.SIGALRM, _alarm); signal.alarm(5)
    try:
        exec(compile(tree, '<modelo>', 'exec'), env)
    finally:
        signal.alarm(0)
    return '\n'.join(buf), fin.get('v')

# ---------------------------------------------------------------- LLM (punto unico de salida)
def call_llm(messages, base, key, model, max_tokens=MAX_TOKENS):
    """UNICO punto de salida hacia el modelo: aqui se redacta TODO lo que se envia."""
    limpio = []
    red_local = 0
    for m in messages:
        c, n = redactar(m.get('content') or '')
        red_local += n
        limpio.append({'role': m['role'], 'content': c})
    body = json.dumps({'model': model, 'messages': limpio, 'max_tokens': max_tokens,
                       'temperature': 0}).encode()
    req = urlreq.Request(base.rstrip('/') + '/chat/completions', data=body,
                         headers={'Content-Type': 'application/json',
                                  'Authorization': 'Bearer ' + key})
    t0 = time.time()
    with urlreq.urlopen(req, timeout=LLM_TIMEOUT) as r:
        d = json.loads(r.read().decode())
    ch = (d.get('choices') or [{}])[0]
    txt = ch.get('message', {}).get('content') or ''
    u = d.get('usage') or {}
    u['finish_reason'] = ch.get('finish_reason')
    return txt, u, time.time() - t0, red_local

# ---------------------------------------------------------------- brazos
RLM_SYS = textwrap.dedent("""\
    Eres la raiz de un Recursive Language Model (RLM).
    Tienes un corpus de {n} fichero(s) ({b} bytes) que NO ves: solo conoces su tamano.
    Para responder tienes que INSPECCIONARLO escribiendo codigo Python.
    Funciones disponibles (ya existen, no las importes):
      list_files()                  -> lista de rutas relativas
      grep(patron)                  -> dict ruta -> [hasta 5 lineas que casan] (patron regex)
      count(patron)                 -> dict con 'coincidencias' y 'ficheros' (conteo en TODO el corpus)
      peek(ruta, inicio=0, n=2000)  -> fragmento de texto
      meta(ruta)                    -> dict con 'bytes' y 'lineas'
      sizes()                       -> dict ruta -> bytes
      regex(texto, patron), print(...), FINAL(respuesta)
    - Para terminar: llama a FINAL(<respuesta>) dentro del codigo, o escribe la linea FINAL(<respuesta>).
    Solo puedes usar esas funciones y Python basico (for, if, len, sorted, sum, listas, dicts).
    No hay imports, ni open(), ni exec/eval.
    Responde SIEMPRE con UN UNICO bloque ```python ...``` y nada mas (sin explicaciones).
""")

def arm_rlm(C, pregunta, base, key, model, max_iters=MAX_ITERS):
    n_b = sum(len(C.text(r).encode()) for r in C.rel)
    msgs = [{'role': 'system', 'content': RLM_SYS.format(n=len(C.rel), b=n_b)},
            {'role': 'user', 'content': pregunta}]
    iters, tokens, red, trace = 0, {'in': 0, 'out': 0}, 0, []
    t0 = time.time()
    while iters < max_iters:
        iters += 1
        try:
            txt, usage, dt, rl = call_llm(msgs, base, key, model)
            red += rl
        except Exception as e:
            trace.append(f'[iter {iters}] ERROR LLM: {e}')
            break
        tokens['in'] += usage.get('prompt_tokens', 0)
        tokens['out'] += usage.get('completion_tokens', 0)
        trace.append(f"[iter {iters}] finish={usage.get('finish_reason')} content={len(txt)}B "
                     f"reasoning={usage.get('completion_tokens_details',{}).get('reasoning_tokens')}")
        msgs.append({'role': 'assistant', 'content': txt})
        mfin = re.search(r'FINAL\((.*?)\)\s*$', txt.strip(), re.S)
        if mfin:
            return {'respuesta': mfin.group(1).strip(), 'iters': iters, 'tokens': tokens,
                    'seg': round(time.time() - t0, 1), 'redactadas': red, 'trace': trace}
        mcode = re.search(r'```(?:python)?\s*(.*?)```', txt, re.S)
        if not mcode:
            msgs.append({'role': 'user', 'content': 'No veo bloque ```python```. Responde solo con un bloque de codigo o FINAL(...).'})
            trace.append(f'[iter {iters}] sin bloque de codigo')
            continue
        try:
            out, finv = sandbox_exec(mcode.group(1), C)
            obs = out[:MAX_OBS] or '(sin salida impresa)'
            trace.append(f'[iter {iters}] code={len(mcode.group(1))}B -> obs={len(obs)}B'
                         + (f' FINAL_fn={finv}' if finv else ''))
            if finv is not None:
                return {'respuesta': str(finv).strip(), 'iters': iters, 'tokens': tokens,
                        'seg': round(time.time() - t0, 1), 'redactadas': red, 'trace': trace,
                        'cierre': 'FINAL() dentro del codigo'}
        except Exception as e:
            obs = f'ERROR: {e}'
            trace.append(f'[iter {iters}] code ERROR: {e}')
        msgs.append({'role': 'user', 'content': 'SALIDA:\n' + obs})
    return {'respuesta': None, 'iters': iters, 'tokens': tokens, 'seg': round(time.time() - t0, 1),
            'redactadas': red, 'trace': trace, 'nota': 'no cerro con FINAL'}

def chunks(C, size=900):
    out = []
    for rel in C.rel:
        t = C.rtext(rel)
        for i in range(0, len(t), size):
            out.append((rel, t[i:i + size]))
    return out

def bm25_topk(cs, pregunta, k=10):
    import math
    toks = lambda s: re.findall(r'[a-záéíóúñ0-9_]+', s.lower())
    q = set(toks(pregunta))
    df, post = {}, []
    for rel, c in cs:
        s = set(toks(c)); post.append(s)
        for t in s:
            df[t] = df.get(t, 0) + 1
    N = len(cs); avg = sum(len(c) for _, c in cs) / max(1, N)
    scores = []
    for i, (rel, c) in enumerate(cs):
        L = len(c); s = 0.0
        for t in q:
            f = c.lower().count(t)
            if f:
                s += (f * 2.2 / (f + 1.2 * (0.25 + 0.75 * L / avg))) * \
                     math.log(1 + (N - df.get(t, 0) + 0.5) / (df.get(t, 0) + 0.5))
        scores.append((s, i))
    scores.sort(reverse=True)
    return [cs[i] for _, i in scores[:k]]

RAG_PROMPT = """Responde a esta pregunta usando SOLO los fragmentos recuperados de un corpus local.

PREGUNTA: {q}

FRAGMENTOS RECUPERADOS ({k} de {tot}):
{frags}

Responde con el dato exacto, sin explicaciones. Si los fragmentos no bastan, di EXACTAMENTE: INSUFICIENTE."""

TRUNC_PROMPT = """Responde a esta pregunta sobre un corpus local del que se te da el indice completo
(ruta + primera linea + bytes) pero NO el contenido.

PREGUNTA: {q}

INDICE:
{idx}

Responde con el dato exacto, sin explicaciones. Si el indice no basta, di EXACTAMENTE: INSUFICIENTE."""

TRUNC1_PROMPT = """Responde a esta pregunta sobre un corpus de {b} bytes del que solo se te da su PRIMERA PARTE.

PREGUNTA: {q}

PRIMERA PARTE DEL CORPUS (primeros {n} caracteres de {tot}):
{tx}

Responde con el dato exacto, sin explicaciones. Si no basta, di EXACTAMENTE: INSUFICIENTE."""

def arm_rag(C, pregunta, base, key, model):
    t0 = time.time()
    cs = chunks(C)
    top = bm25_topk(cs, pregunta, 10)
    frags = '\n\n'.join(f'--- {rel}\n{c}' for rel, c in top)
    p = RAG_PROMPT.format(q=pregunta, k=len(top), tot=len(cs), frags=frags[:20000])
    txt, usage, _, rl = call_llm([{'role': 'user', 'content': p}], base, key, model, max_tokens=1800)
    return {'respuesta': txt.strip(), 'iters': 1,
            'tokens': {'in': usage.get('prompt_tokens', 0), 'out': usage.get('completion_tokens', 0)},
            'seg': round(time.time() - t0, 1), 'redactadas': rl, 'trace': [f'top10 de {len(cs)} chunks']}

def arm_trunc(C, pregunta, base, key, model):
    t0 = time.time()
    if len(C.rel) == 1:
        t = C.rtext(C.rel[0])
        p = TRUNC1_PROMPT.format(b=len(t.encode()), q=pregunta, n=20000, tot=len(t), tx=t[:20000])
    else:
        idx = '\n'.join(f'{r} | {C.rtext(r).splitlines()[0][:80] if C.rtext(r).strip() else "(vacio)"} | {C.meta(r)["bytes"]}B'
                        for r in C.rel)
        p = TRUNC_PROMPT.format(q=pregunta, idx=idx[:20000])
    txt, usage, _, rl = call_llm([{'role': 'user', 'content': p}], base, key, model, max_tokens=1800)
    return {'respuesta': txt.strip(), 'iters': 1,
            'tokens': {'in': usage.get('prompt_tokens', 0), 'out': usage.get('completion_tokens', 0)},
            'seg': round(time.time() - t0, 1), 'redactadas': rl, 'trace': ['indice']}

# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description='RLM-lite: consulta por codigo sobre un corpus local')
    ap.add_argument('--corpus', required=True, help='fichero o directorio')
    ap.add_argument('--pregunta', action='append', default=[], help='repetible')
    ap.add_argument('--brazos', default='rlm,rag,truncado')
    ap.add_argument('--ext', default=','.join(EXT_DEF))
    ap.add_argument('--out', default=None)
    ap.add_argument('--max-iters', type=int, default=MAX_ITERS)
    ap.add_argument('--listar', action='store_true', help='solo listar el corpus y salir')
    a = ap.parse_args()

    exts = [e if e.startswith('.') else '.' + e for e in a.ext.split(',') if e.strip()]
    files, root = build_corpus(a.corpus, exts)
    if a.listar:
        tot = sum(os.path.getsize(f) for f in files)
        print(f'corpus: {len(files)} fichero(s) | {tot:,} B | raiz {root}')
        for r in [os.path.relpath(f, root) for f in files]:
            print('  ', r)
        return
    if not files:
        raise SystemExit('corpus vacio')
    C = Corpus(files, root)
    base, key = load_base_key()
    if not key:
        raise SystemExit('sin credencial DEEPSEEK_API_KEY en el entorno del lab')
    model = os.environ.get('RLM_MODEL', 'deepseek-v4-flash')
    out = a.out or time.strftime('/tmp/rlm_lite_%Y%m%d-%H%M%S.json')

    def log(*x):
        print(' '.join(str(i) for i in x), flush=True)

    log('=== rlm_lite ===', subprocess.run(['date', '+%Y-%m-%d %H:%M:%S %Z'],
        capture_output=True, text=True).stdout.strip())
    log(f'corpus: {len(C.rel)} fichero(s) | {sum(os.path.getsize(f) for f in files):,} B | raiz {root}')
    log('modelo raiz:', model, '| redaccion obligatoria: ON')
    brazos = [b.strip() for b in a.brazos.split(',') if b.strip()]
    res = {}
    for q in (a.pregunta or []):
        log('\n--- pregunta:', q)
        entry = {'pregunta': q, 'brazos': {}}
        for arm in brazos:
            fn = {'rlm': lambda: arm_rlm(C, q, base, key, model, a.max_iters),
                  'rag': lambda: arm_rag(C, q, base, key, model),
                  'truncado': lambda: arm_trunc(C, q, base, key, model)}.get(arm)
            if not fn:
                continue
            try:
                r = fn()
            except Exception as e:
                r = {'respuesta': None, 'error': str(e)}
            entry['brazos'][arm] = r
            log(f'  [{arm:9s}] {r.get("seg")}s iters={r.get("iters")} '
                f'tok={r.get("tokens",{}).get("in")}+{r.get("tokens",{}).get("out")} '
                f'redactadas={r.get("redactadas")}')
            log('     resp:', str(r.get('respuesta'))[:400].replace('\n', ' '))
            json.dump(res, open(out, 'w'), ensure_ascii=False, indent=1)
        res[str(len(res) + 1)] = entry
    json.dump(res, open(out, 'w'), ensure_ascii=False, indent=1)
    log('\nlineas redactadas antes de enviar:', _RED['lineas'], '| marcas:', _RED['marcas'])
    log('escrito:', out)

if __name__ == '__main__':
    main()
