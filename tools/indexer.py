#!/usr/bin/env python3
"""indexer.py - Indexa archivos .md/.yaml de Joko Lab en LanceDB usando BGE-M3.

v2 (2026-08-05): INDEXADO INCREMENTAL por hash sha256.
  - Sidecar de hashes: <DB_PATH>/index_hashes.json
  - Solo re-embebe documentos nuevos o modificados; conserva vectores de los
    que no cambiaron; elimina chunks de archivos borrados.
  - --force: reindexa TODO (ignora el sidecar).
  - --dry-run: muestra qué haría sin escribir nada.
Backup previo: indexer.py.bak-20260805 (RULE-008).
"""
import os, re, sys, json, hashlib, argparse, yaml, lancedb, torch, pyarrow as pa
from pathlib import Path
from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

VAULT_PATH = Path(os.path.expanduser("~/joko-lab"))
# Fuente extra: el proyecto biohacking (Prueba 1, entrenador, protocolos) —
# estaba FUERA del RAG (fallo detectado por evaluar_rag.py, OP-20260812-007).
# El prefijo "biohacking/" distingue sus rutas de las de ~/joko-lab.
VAULT_EXTRA = [
    (Path(os.path.expanduser("~/proyectos/biohacking-cerebral")), "biohacking/"),
]
DB_PATH = VAULT_PATH / ".lancedb"
COLLECTION_NAME = "joko_notes"
MODEL_NAME = "BAAI/bge-m3"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
HASH_SIDECAR = DB_PATH / "index_hashes.json"


def parse_frontmatter(content: str) -> tuple[Dict[str, Any], str]:
    pattern = r"^---\s*\n(.*?)\n---\s*\n"
    match = re.match(pattern, content, re.DOTALL)
    if match:
        try:
            metadata = yaml.safe_load(match.group(1)) or {}
        except Exception:
            metadata = {}
        return metadata, content[match.end():]
    return {}, content


def _campos_presentes(data, claves) -> list:
    """Devuelve ['k: v', ...] para claves con valor truthy en data."""
    return [f"{k}: {data[k]}" for k in claves if data.get(k)]


def yaml_to_text(fpath: Path) -> str:
    """Convierte un Knowledge Object YAML a texto plano buscable."""
    raw = fpath.read_text(encoding="utf-8")
    try:
        data = yaml.safe_load(raw)
    except Exception:
        return raw
    if not isinstance(data, dict):
        return raw
    parts = _campos_presentes(data, ("id", "type", "status", "domain", "scope", "body"))
    lf = data.get("legacy_fields") or {}
    if not isinstance(lf, dict):
        lf = {}
    parts += _campos_presentes(lf, ("condicion", "accion", "prioridad", "nota"))
    accion = lf.get("accion") or {}
    params = accion.get("params") if isinstance(accion, dict) else None
    if isinstance(params, dict):
        for key, val in params.items():
            if val is not None:
                parts.append(f"param_{key}: {val}")
    return "\n".join(parts)


def hash_documento(meta: Dict[str, Any], body: str, fpath: Path) -> str:
    """sha256 de todo lo que afecta a los chunks indexados (metadatos + cuerpo)."""
    titulo = str(meta.get("title", fpath.stem))
    tags = meta.get("tags", "")
    if isinstance(tags, list):
        # Tags YAML de terceros pueden ser numericos (p.ej. 802.11 sin comillas
        # -> float). str() evita "sequence item N: expected str instance, float found".
        tags = ",".join(str(t) for t in tags)
    fuente = f"{fpath}\n{titulo}\n{tags}\n{body}"
    return hashlib.sha256(fuente.encode("utf-8")).hexdigest()


def cargar_sidecar() -> Dict[str, str]:
    if HASH_SIDECAR.exists():
        try:
            return json.loads(HASH_SIDECAR.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def guardar_sidecar(hashes: Dict[str, str]) -> None:
    HASH_SIDECAR.parent.mkdir(parents=True, exist_ok=True)
    tmp = HASH_SIDECAR.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(hashes, ensure_ascii=False, indent=1), encoding="utf-8")
    tmp.replace(HASH_SIDECAR)


def _excluir_directorio(root: str, d: str) -> bool:
    return (d.startswith(".") or d == "node_modules" or
            (root.endswith("04-operations") and d == "decisions") or
            d == "verification" or
            d.endswith(".BACKUP") or
            ".bak" in d)


def _parsear_archivo(file: str, fpath: Path, raw: str) -> tuple:
    if file.endswith(".yaml") or file.endswith(".yml"):
        meta, body = {}, yaml_to_text(fpath)
        try:
            ko = yaml.safe_load(raw) or {}
            tipo = str(ko.get("type", ""))
            estado = str(ko.get("status", ""))
        except Exception:
            tipo, estado = "", ""
    else:
        meta, body = parse_frontmatter(raw)
        tipo = str(meta.get("type", ""))
        estado = str(meta.get("status", ""))
    return meta, body, tipo, estado


def _construir_documentos(splitter, rpath, fpath, meta, body, tipo, estado) -> list:
    chunks = splitter.split_text(body)
    docs = []
    for idx, chunk in enumerate(chunks):
        docs.append({
            "id": f"{rpath}#{idx}",
            "path": rpath,
            "title": meta.get("title", fpath.stem),
            "tags": ",".join(str(t) for t in meta.get("tags", [])) if isinstance(meta.get("tags"), list) else str(meta.get("tags", "")),
            "type": tipo,
            "status": estado,
            "text": chunk
        })
    return docs


def load_notes_con_hash() -> tuple[List[Dict[str, Any]], Dict[str, str]]:
    """Devuelve (documents, {rpath: hash}) para TODOS los archivos indexables."""
    documents: List[Dict[str, Any]] = []
    hashes: Dict[str, str] = {}
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=150,
        separators=["\n## ", "\n### ", "\n\n", "\n", " "]
    )
    for root, dirs, files in os.walk(VAULT_PATH):
        dirs[:] = [d for d in dirs if not _excluir_directorio(root, d)]
        for file in files:
            if not (file.endswith(".md") or file.endswith(".yaml") or file.endswith(".yml")):
                continue
            # Excluir backups sueltos (*.bak-*, *.BACKUP) — se cuelan como "nuevos"
            # y obligan al watchdog a re-embebrer cientos de backups en cada cambio
            # (timeout 600s + contaminación del RAG). Fix 07-ago-2026.
            if ".bak" in file or file.endswith(".BACKUP"):
                continue
            fpath = Path(root) / file
            rpath = str(fpath.relative_to(VAULT_PATH))
            try:
                raw = fpath.read_text(encoding="utf-8")
                meta, body, tipo, estado = _parsear_archivo(file, fpath, raw)
                hashes[rpath] = hash_documento(meta, body, fpath)
                documents.extend(_construir_documentos(splitter, rpath, fpath, meta, body, tipo, estado))
            except Exception as e:
                print(f"  Error en {rpath}: {e}")
    # Fuentes extra (biohacking) — con prefijo en la ruta para distinguirlas
    for extra_path, prefijo in VAULT_EXTRA:
        if not extra_path.exists():
            continue
        for root, dirs, files in os.walk(extra_path):
            dirs[:] = [d for d in dirs if not _excluir_directorio(root, d)]
            for file in files:
                if not (file.endswith(".md") or file.endswith(".yaml") or file.endswith(".yml")):
                    continue
                if ".bak" in file or file.endswith(".BACKUP"):
                    continue
                fpath = Path(root) / file
                rpath = prefijo + str(fpath.relative_to(extra_path))
                try:
                    raw = fpath.read_text(encoding="utf-8")
                    meta, body, tipo, estado = _parsear_archivo(file, fpath, raw)
                    hashes[rpath] = hash_documento(meta, body, fpath)
                    documents.extend(_construir_documentos(splitter, rpath, fpath, meta, body, tipo, estado))
                except Exception as e:
                    print(f"  Error en {rpath}: {e}")
    return documents, hashes


def leer_tabla_existente(db) -> Optional[Any]:
    """Devuelve DataFrame de la tabla existente, o None si no existe."""
    if COLLECTION_NAME not in db.table_names():
        return None
    try:
        return db.open_table(COLLECTION_NAME).to_pandas()
    except Exception:
        return None


def _clasificar_cambios(sidecar_previo: dict, hashes_nuevos: dict) -> tuple[set, set, set, set]:
    rpaths_actuales = set(hashes_nuevos.keys())
    rpaths_previos = set(sidecar_previo.keys())
    eliminados = rpaths_previos - rpaths_actuales
    modificados = {r for r in rpaths_actuales if r in sidecar_previo and sidecar_previo[r] != hashes_nuevos[r]}
    nuevos = rpaths_actuales - rpaths_previos
    sin_cambios = (rpaths_actuales & rpaths_previos) - modificados
    return (nuevos, modificados, eliminados, sin_cambios)


def _cargar_modelo(dev: str) -> tuple[SentenceTransformer, str]:
    print(f"[*] Cargando {MODEL_NAME} en {dev}...")
    try:
        model = SentenceTransformer(MODEL_NAME, device=dev)
        if dev == "cuda":
            model.half()
    except torch.cuda.OutOfMemoryError:
        if dev == "cuda":
            print("[!] OOM en GPU — cayendo a CPU (GLM u otro modelo ocupa la VRAM).")
            dev = "cpu"
            model = SentenceTransformer(MODEL_NAME, device=dev)
        else:
            raise
    return (model, dev)


def _recrear_indices(table) -> None:
    try:
        table.create_fts_index("text", language="Spanish", replace=True)
        table.create_index(metric="cosine", index_type="IVF_HNSW_FLAT",
                           num_partitions=16, m=20, ef_construction=300, replace=True)
        print("[✓] Indices FTS + vectorial recreados.")
    except Exception as e:
        print(f"[!] No se pudieron recrear los indices ({e}) — busqueda solo vectorial hasta el proximo reindex.")


def _conservar_sin_cambios(db, sin_cambios) -> list:
    """Reutiliza los vectores de archivos sin cambios desde la tabla existente."""
    df_existente = leer_tabla_existente(db)
    conservados = []
    if df_existente is not None and not df_existente.empty:
        mask = df_existente["path"].isin(sin_cambios)
        conservados = df_existente[mask].to_dict(orient="records")
        print(f"[*] Conservando {len(conservados)} fragmentos sin cambios (vectores reutilizados).")
    return conservados


def _embedear_docs(docs_a_embedear, dev):
    """Embebe los fragmentos que cambiaron o son nuevos. Devuelve (docs_con_vector, modelo_dev)."""
    model = None
    if docs_a_embedear:
        model, dev = _cargar_modelo(dev)
        texts = [d["text"] for d in docs_a_embedear]
        embeddings = model.encode(texts, batch_size=16, show_progress_bar=True, normalize_embeddings=True)
        for i, doc in enumerate(docs_a_embedear):
            doc["vector"] = embeddings[i].tolist()
    return docs_a_embedear, (model, dev)


def _clasificar_y_reportar(sidecar_previo, hashes_nuevos, docs, force, dry_run) -> tuple:
    """Clasifica cambios y maneja early-returns. Devuelve
    (nuevos, modificados, eliminados, sin_cambios) o None si hay return temprano."""
    nuevos, modificados, eliminados, sin_cambios = _clasificar_cambios(sidecar_previo, hashes_nuevos)

    if not force and not nuevos and not modificados and not eliminados:
        print(f"[✓] Sin cambios: {len(docs)} fragmentos ya indexados (sidecar al día).")
        return None

    print(f"[*] Cambios detectados: {len(nuevos)} nuevos, {len(modificados)} modificados, "
          f"{len(eliminados)} eliminados, {len(sin_cambios)} sin cambios.")

    if dry_run:
        print("[dry-run] No se escribe nada. Sidecar: "
              f"{len(hashes_nuevos)} entradas previstas.")
        return None

    return nuevos, modificados, eliminados, sin_cambios


def build_index(force: bool = False, dry_run: bool = False, device: Optional[str] = None) -> int:
    sidecar_previo = {} if force else cargar_sidecar()
    dev = device or DEVICE

    print("[*] Leyendo archivos Markdown/YAML...")
    docs, hashes_nuevos = load_notes_con_hash()
    if not docs:
        print("[!] No se encontraron archivos .md")
        return 1

    # Clasificar: nuevos / modificados / sin cambios / eliminados
    clasif = _clasificar_y_reportar(sidecar_previo, hashes_nuevos, docs, force, dry_run)
    if clasif is None:
        return 0
    nuevos, modificados, eliminados, sin_cambios = clasif

    # Conservar vectores de archivos sin cambios
    db = lancedb.connect(str(DB_PATH))
    conservados = _conservar_sin_cambios(db, sin_cambios)

    # Solo re-embeder los que cambiaron o son nuevos
    docs_a_embedear = [d for d in docs if d["path"] in (nuevos | modificados)]
    print(f"[*] Re-embebiendo {len(docs_a_embedear)} fragmentos ({len(nuevos) + len(modificados)} archivos)...")

    docs_a_embedear, (model, dev) = _embedear_docs(docs_a_embedear, dev)

    # Unir: conservados (ya con vector) + nuevos
    todos = conservados + docs_a_embedear
    if not todos:
        print("[!] Nada que escribir.")
        return 1

    print("[*] Guardando en LanceDB...")
    table = db.create_table(COLLECTION_NAME, data=todos, mode="overwrite")
    guardar_sidecar(hashes_nuevos)
    print(f"[✓] Indexacion completada. {len(table)} registros en {DB_PATH} "
          f"({len(docs_a_embedear)} re-embebidos, {len(conservados)} conservados).")

    _recrear_indices(table)
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Indexer incremental Joko Lab (BGE-M3 + LanceDB)")
    parser.add_argument("--force", action="store_true", help="Reindexa TODO ignorando el sidecar")
    parser.add_argument("--dry-run", action="store_true", help="Muestra cambios sin escribir")
    parser.add_argument("--device", choices=["cuda", "cpu"], default=None,
                        help="Fuerza dispositivo (por defecto: cuda si disponible)")
    args = parser.parse_args()
    sys.exit(build_index(force=args.force, dry_run=args.dry_run, device=args.device))
