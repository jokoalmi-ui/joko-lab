#!/usr/bin/env python3
"""index_query_summary.py — Query + Summary Indexing para el RAG (A1, 20-ago-2026).

Añade TABLAS NUEVAS al LanceDB existente (no toca joko_notes):
- joko_summaries: 1 fila por documento (resumen = description del frontmatter
  o inicio del body).
- joko_queries: N filas por documento (preguntas de estado que el usuario
  haría: "¿qué es X?", "¿qué decidimos sobre X?", "¿qué dice X sobre Y?",
  + títulos + secciones + tags).

Por qué: el RAG actual (joko_notes) indexa chunks; una pregunta de ESTADO
("¿qué decidimos sobre el corte de cafeína?") a veces no matchea el chunk
correcto. Query/Summary Indexing recupera el DOCUMENTO (path) por su resumen
o por preguntas posibles, y luego se traen los chunks del doc ganador.

Determinista (0 tokens LLM): reutiliza description del frontmatter + título +
secciones (## ) + tags. Incremental por sidecar de hashes (mismo patrón que
indexer.py). SOLO LECTURA del vault; escribe solo en las tablas nuevas.

Uso:
  python3 tools/index_query_summary.py [--force] [--dry-run] [--limit N]
  python3 tools/index_query_summary.py --dry-run --limit 5   # prueba rápida
"""
import os, re, sys, json, hashlib, argparse
from pathlib import Path
from typing import List, Dict, Any, Optional

# Reutiliza la lógica de indexer.py (frontmatter, exclusiones, hashes)
sys.path.insert(0, str(Path(__file__).resolve().parent))
import indexer as idx  # noqa: E402

VAULT_PATH = idx.VAULT_PATH
DB_PATH = idx.DB_PATH
QS_HASH_SIDECAR = DB_PATH / "qs_index_hashes.json"  # sidecar PROPIO de QS

SUMMARY_TABLE = "joko_summaries"
QUERY_TABLE = "joko_queries"

# Patrones de preguntas de estado (los que el usuario usa de verdad)
_PATRONES_ESTADO = [
    "¿qué es {t}?",
    "¿qué decidimos sobre {t}?",
    "¿qué dice {t}?",
    "¿cómo funciona {t}?",
    "¿dónde está {t}?",
    "información sobre {t}",
]

_SECCION_RE = re.compile(r"^##?\s+(.+)$", re.MULTILINE)


def _titulo_limpio(meta: dict, fpath: Path) -> str:
    t = str(meta.get("title") or fpath.stem or "")
    return t.strip()


def _description(meta: dict) -> str:
    d = meta.get("description") or meta.get("desc") or ""
    return str(d).strip()


def _secciones(body: str, max_n: int = 5) -> List[str]:
    secs = [m.group(1).strip() for m in _SECCION_RE.finditer(body)]
    # quitar títulos tipo "## Completadas" o muy largos
    out = []
    for s in secs:
        if len(s) > 60 or s.lower() in ("completadas", "historial"):
            continue
        out.append(s)
        if len(out) >= max_n:
            break
    return out


def _tags(meta: dict) -> List[str]:
    tg = meta.get("tags") or []
    if isinstance(tg, str):
        tg = [x.strip() for x in tg.split(",") if x.strip()]
    return [str(t).strip() for t in tg if str(t).strip()][:5]


def construir_filas(rpath: str, meta: dict, body: str, fpath: Path, tipo: str, estado: str) -> tuple[list, list]:
    """Devuelve (filas_summary, filas_query) para UN documento."""
    titulo = _titulo_limpio(meta, fpath)
    desc = _description(meta)
    # --- SUMMARY: description del frontmatter, o inicio del body ---
    if desc:
        texto_sum = f"{titulo}. {desc}"
    else:
        texto_sum = f"{titulo}. {body[:500]}"
    fila_sum = [{
        "id": f"{rpath}#sum",
        "path": rpath,
        "title": titulo,
        "type": tipo,
        "status": estado,
        "text": texto_sum,
    }]

    # --- QUERIES: patrones de estado + secciones + tags ---
    queries = set()
    for p in _PATRONES_ESTADO:
        queries.add(p.format(t=titulo))
    for s in _secciones(body):
        queries.add(f"¿qué dice {titulo} sobre {s}?")
        queries.add(f"{titulo}: {s}")
    for tg in _tags(meta):
        queries.add(f"¿qué es {tg}?")
        queries.add(f"información sobre {tg}")
    if desc:
        queries.add(desc[:200])

    filas_q = []
    for i, q in enumerate(sorted(queries)):
        if not q.strip():
            continue
        filas_q.append({
            "id": f"{rpath}#q{i}",
            "path": rpath,
            "title": titulo,
            "type": tipo,
            "status": estado,
            "text": q,
        })
    return fila_sum, filas_q


def hash_documento_qs(meta: dict, body: str, fpath: Path) -> str:
    """Hash propio: cualquier cambio en frontmatter/body regenera summary+queries."""
    titulo = str(meta.get("title", fpath.stem))
    fuente = f"{fpath}\n{titulo}\n{body}"
    return hashlib.sha256(fuente.encode("utf-8")).hexdigest()


def cargar_sidecar() -> Dict[str, str]:
    if QS_HASH_SIDECAR.exists():
        try:
            return json.loads(QS_HASH_SIDECAR.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def guardar_sidecar(hashes: Dict[str, str]) -> None:
    QS_HASH_SIDECAR.parent.mkdir(parents=True, exist_ok=True)
    tmp = QS_HASH_SIDECAR.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(hashes, ensure_ascii=False, indent=1), encoding="utf-8")
    tmp.replace(QS_HASH_SIDECAR)


def _recorrer_documentos(limit: Optional[int] = None):
    """Recorre los mismos archivos que indexer.py; devuelve por documento."""
    docs = []  # (rpath, meta, body, fpath, tipo, estado, hash)
    for root, dirs, files in os.walk(VAULT_PATH):
        dirs[:] = [d for d in dirs if not idx._excluir_directorio(root, d)]
        for file in files:
            if not (file.endswith(".md") or file.endswith(".yaml") or file.endswith(".yml")):
                continue
            if ".bak" in file or file.endswith(".BACKUP"):
                continue
            fpath = Path(root) / file
            rpath = str(fpath.relative_to(VAULT_PATH))
            try:
                raw = fpath.read_text(encoding="utf-8")
                meta, body, tipo, estado = idx._parsear_archivo(file, fpath, raw)
                docs.append((rpath, meta, body, fpath, tipo, estado,
                             hash_documento_qs(meta, body, fpath)))
            except Exception as e:
                print(f"  Error en {rpath}: {e}")
    for extra_path, prefijo in idx.VAULT_EXTRA:
        if not extra_path.exists():
            continue
        for root, dirs, files in os.walk(extra_path):
            dirs[:] = [d for d in dirs if not idx._excluir_directorio(root, d)]
            for file in files:
                if not (file.endswith(".md") or file.endswith(".yaml") or file.endswith(".yml")):
                    continue
                if ".bak" in file or file.endswith(".BACKUP"):
                    continue
                fpath = Path(root) / file
                rpath = prefijo + str(fpath.relative_to(extra_path))
                try:
                    raw = fpath.read_text(encoding="utf-8")
                    meta, body, tipo, estado = idx._parsear_archivo(file, fpath, raw)
                    docs.append((rpath, meta, body, fpath, tipo, estado,
                                 hash_documento_qs(meta, body, fpath)))
                except Exception as e:
                    print(f"  Error en {rpath}: {e}")
    if limit:
        docs = docs[:limit]
    return docs


_MODELO_QS: Dict[str, Any] = {}  # caché por dispositivo (ver _embeder)


def _embeder(textos: List[str], dev: str):
    """Embeddings: LM Studio API si disponible, si no BGE-M3 local.

    El modelo se cachea por dispositivo (15-oct-2026): se llama 2 veces (una
    por tabla) y antes CADA llamada construía un SentenceTransformer nuevo →
    dos BGE-M3 vivos a la vez = ~1,8 GB extra de pico (medido: 4,54 GiB de
    máximo con el tope de 4 GiB del scope de ejecución).
    """
    try:
        from tools.lmstudio_embeddings import encode, _is_available
        if _is_available():
            return encode(textos)
    except Exception:
        pass
    print(f"  [encoder] LM Studio no disponible, BGE-M3 local ({dev})...", file=sys.stderr)
    import torch
    modelo = _MODELO_QS.get(dev)
    if modelo is None:
        modelo = idx._cargar_modelo(dev)[0]
        _MODELO_QS[dev] = modelo
    return modelo.encode(textos, batch_size=16, normalize_embeddings=True)


def build_qs(force: bool = False, dry_run: bool = False, limit: Optional[int] = None,
             device: Optional[str] = None) -> int:
    dev = device or idx.DEVICE
    sidecar_previo = {} if force else cargar_sidecar()

    print("[*] Leyendo documentos (frontmatter + body)...")
    docs = _recorrer_documentos(limit)
    if not docs:
        print("[!] No se encontraron documentos")
        return 1

    # Clasificar por hash
    nuevos, modificados, sin_cambios = [], [], []
    for rpath, meta, body, fpath, tipo, estado, h in docs:
        if force or rpath not in sidecar_previo:
            nuevos.append((rpath, meta, body, fpath, tipo, estado, h))
        elif sidecar_previo[rpath] != h:
            modificados.append((rpath, meta, body, fpath, tipo, estado, h))
        else:
            sin_cambios.append(rpath)

    print(f"[*] {len(docs)} documentos: {len(nuevos)} nuevos, {len(modificados)} modificados, {len(sin_cambios)} sin cambios.")
    if not nuevos and not modificados:
        print("[✓] Sin cambios (sidecar QS al día).")
        return 0
    if dry_run:
        print("[dry-run] No se escribe nada.")
        return 0

    # Liberar los cuerpos de los docs SIN cambios: solo hacen falta los
    # nuevos/modificados (que siguen referenciados en sus listas). Con 4.176
    # documentos el listado completo retenía el vault entero en RAM durante
    # el embedding y la escritura (15-oct-2026).
    del docs
    import gc
    gc.collect()

    # Construir filas de los que cambian
    filas_sum, filas_q = [], []
    for rpath, meta, body, fpath, tipo, estado, h in nuevos + modificados:
        s, q = construir_filas(rpath, meta, body, fpath, tipo, estado)
        filas_sum.extend(s)
        filas_q.extend(q)

    print(f"[*] Embebiendo {len(filas_sum)} summaries + {len(filas_q)} queries...")
    textos_sum = [f["text"] for f in filas_sum]
    textos_q = [f["text"] for f in filas_q]
    if textos_sum:
        vecs = _embeder(textos_sum, dev)
        for f, v in zip(filas_sum, vecs):
            f["vector"] = v.tolist() if hasattr(v, "tolist") else list(v)
    if textos_q:
        vecs = _embeder(textos_q, dev)
        for f, v in zip(filas_q, vecs):
            f["vector"] = v.tolist() if hasattr(v, "tolist") else list(v)

    # Conservar filas de docs sin cambios: se filtra en ARROW (buffers), sin
    # materializar objetos Python (ver _write_table).
    import lancedb
    import pyarrow as pa
    import pyarrow.compute as pc
    db = lancedb.connect(str(DB_PATH))

    def _write_table(name: str, filas_nuevas: list, paths_sin_cambios: list):
        """Reescribe la tabla = filas de docs sin cambios + filas nuevas.

        Bajo consumo (15-oct-2026): la version anterior hacia
        to_pandas() + df[mask].to_dict(orient="records") + create_table(dicts),
        que con 72.394 filas x 1024 floats materializaba ~2 GB en listas Python
        y daba un pico medido de 4,65 GiB (roza el tope de 4 GiB del scope de
        ejecucion: un dia se lo llevo el OOM-killer a mitad de fase B). Ahora
        el filtro y la concatenacion son operaciones Arrow (memcpy de buffers)
        y la tabla se escribe ya como Arrow: mismo esquema, misma semantica
        (se descartan las filas de docs cambiados/borrados, se anaden las
        nuevas y se conservan las de los sin cambios), mucho menos pico.
        """
        vieja = None
        if name in db.table_names():
            t = db.open_table(name).to_arrow()
            if t.num_rows:
                if paths_sin_cambios:
                    mask = pc.is_in(t["path"], value_set=pa.array(paths_sin_cambios, type=pa.string()))
                    vieja = t.filter(mask)
                else:
                    vieja = t.slice(0, 0)

        nueva = None
        if filas_nuevas:
            esquema = vieja.schema if vieja is not None else None
            nueva = pa.Table.from_pylist(filas_nuevas, schema=esquema)

        if vieja is not None and nueva is not None:
            todas = pa.concat_tables([vieja, nueva])
        else:
            todas = vieja if vieja is not None else nueva

        if todas is not None and todas.num_rows:
            db.create_table(name, data=todas, mode="overwrite")
            print(f"[✓] {name}: {todas.num_rows} filas ({len(filas_nuevas)} nuevas, {todas.num_rows - len(filas_nuevas)} conservadas).")

    _write_table(SUMMARY_TABLE, filas_sum, sin_cambios)
    _write_table(QUERY_TABLE, filas_q, sin_cambios)

    # Actualizar sidecar QS (solo los docs procesados/confirmados)
    hashes_nuevos = dict(sidecar_previo)
    for rpath, meta, body, fpath, tipo, estado, h in nuevos + modificados:
        hashes_nuevos[rpath] = h
    guardar_sidecar(hashes_nuevos)
    print("[✓] Sidecar QS actualizado.")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query+Summary Indexing (A1)")
    parser.add_argument("--force", action="store_true", help="Regenera TODO")
    parser.add_argument("--dry-run", action="store_true", help="Muestra sin escribir")
    parser.add_argument("--limit", type=int, default=None, help="Procesa solo N documentos (prueba)")
    parser.add_argument("--device", choices=["cuda", "cpu"], default=None)
    args = parser.parse_args()
    sys.exit(build_qs(force=args.force, dry_run=args.dry_run, limit=args.limit, device=args.device))
