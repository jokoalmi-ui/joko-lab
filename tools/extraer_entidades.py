#!/usr/bin/env python3
"""extraer_entidades.py — extrae herramientas / modelos / organizaciones de cada
documento del lab y escribe una cache que consume tools/indexer.py.

Corre aparte del indexer (necesita el venv de GLiNER2, que el indexer no tiene):

    cd ~/joko-lab && ./.venv-gliner2/bin/python tools/extraer_entidades.py

Salida: ~/joko-lab/.lancedb/entity_cache.json
    {"version": 1, "modelo": "...", "docs": {rpath: {"sig": "mtime:size", "ents": [...]}}}

Incremental: si `sig` no cambia, no se vuelve a inferir. `--force` rehace todo.
Coste medido: ~130 ms/documento.
"""
import os, re, sys, json, time, argparse
from pathlib import Path

BASE = Path(os.path.expanduser("~/joko-lab"))
CACHE = BASE / ".lancedb" / "entity_cache.json"
VAULT_EXTRA = [(Path(os.path.expanduser("~/proyectos/biohacking-cerebral")), "biohacking/")]
MODELO = BASE / "models" / "gliner2.5-multi-v1"
MAX_CHARS = 1800
DESC = {
    "herramienta": "Nombre de software, aplicacion, comando o servicio tecnico",
    "modelo_ia": "Nombre de un modelo de inteligencia artificial o de lenguaje",
    "organizacion": "Nombre de una empresa, fundacion o proyecto institucional",
}
SIGLAS = re.compile(r"(?<![\w-])[A-Z][A-Z0-9_-]{1,12}(?![\w-])")
RUIDO = {"TXT", "JSON", "YAML", "TRUE", "FALSE", "NULL", "TODO", "OK", "MD", "PY", "SH", "SI", "NO"}


def limpiar(body: str) -> str:
    b = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", body)
    b = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", b)
    b = re.sub(r"```.*?```", " ", b, flags=re.S)
    b = re.sub(r"[|#>]+", " ", b)
    return re.sub(r"\s+", " ", b).strip()[:MAX_CHARS]


def cuerpo_de(raw: str) -> str:
    if raw.startswith("---"):
        m = re.search(r"\n---\s*\n", raw[3:])
        if m:
            return raw[3 + m.end():]
    return raw


def iterar_docs():
    for raiz, prefijo in [(BASE, "")] + VAULT_EXTRA:
        if not raiz.exists():
            continue
        for dp, dn, fn in os.walk(raiz):
            dn[:] = [d for d in dn if not d.startswith(".") and d != "node_modules"
                     and "BACKUP" not in d and ".bak" not in d]
            for f in fn:
                if not f.endswith(".md") or ".bak" in f:
                    continue
                p = Path(dp) / f
                try:
                    st = p.stat()
                    yield prefijo + str(p.relative_to(raiz)), p, f"{int(st.st_mtime)}:{st.st_size}"
                except OSError:
                    continue


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()

    cache = {"version": 1, "modelo": MODELO.name, "docs": {}}
    if CACHE.exists() and not a.force:
        try:
            cache = json.loads(CACHE.read_text(encoding="utf-8"))
        except Exception:
            pass

    from gliner2 import AutoExtractor
    import torch
    torch.cuda.reset_peak_memory_stats()
    t0 = time.time()
    model = AutoExtractor.from_pretrained(str(MODELO), map_location="cuda", quantize=True)
    print(f"[*] modelo cargado en {time.time()-t0:.1f}s", flush=True)

    pendientes = []
    for rpath, p, sig in iterar_docs():
        if not a.force and cache["docs"].get(rpath, {}).get("sig") == sig:
            continue
        pendientes.append((rpath, p, sig))
    if a.limit:
        pendientes = pendientes[:a.limit]
    print(f"[*] {len(pendientes)} documentos que procesar (cache: {len(cache['docs'])})", flush=True)

    t0 = time.time()
    for i, (rpath, p, sig) in enumerate(pendientes, 1):
        try:
            texto = limpiar(cuerpo_de(p.read_text(encoding="utf-8")))
            ents = set()
            if len(texto) >= 200:
                r = model.extract_entities(texto, DESC, include_confidence=False, include_spans=False)
                for items in (r.get("entities") or {}).values():
                    for it in items:
                        # Segun include_spans/include_confidence devuelve dict o str
                        t = it.get("text", "") if isinstance(it, dict) else str(it)
                        t = re.sub(r"\s+", " ", t).strip()
                        if 2 <= len(t) <= 45 and not t.isdigit():
                            ents.add(t)
            cache["docs"][rpath] = {"sig": sig, "ents": sorted(ents, key=str.lower)}
        except Exception as e:
            print(f"  [!] {rpath}: {type(e).__name__}: {e}", flush=True)
        if i % 200 == 0:
            print(f"  {i}/{len(pendientes)} ({time.time()-t0:.0f}s)", flush=True)
            CACHE.parent.mkdir(parents=True, exist_ok=True)
            CACHE.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")

    CACHE.parent.mkdir(parents=True, exist_ok=True)
    tmp = CACHE.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
    tmp.replace(CACHE)
    con = sum(1 for v in cache["docs"].values() if v.get("ents"))
    print(f"[✓] cache escrita: {len(cache['docs'])} docs, {con} con entidades "
          f"({time.time()-t0:.0f}s, {torch.cuda.max_memory_allocated()/1024**2:.0f} MiB pico)")


if __name__ == "__main__":
    main()
