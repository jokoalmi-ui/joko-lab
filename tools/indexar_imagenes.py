#!/usr/bin/env python3
"""indexar_imagenes.py — Indexa imágenes del lab en LanceDB con CLIP (RAG multimodal).

Implementación del GAP detectado en analisis-multi-modal-rag.md (10-ago):
el lab analiza imágenes (capturas, fotos de perfumes, infografías) pero NO
las indexa — se pierden. Este script las indexa con CLIP (ViT-B/32) en la
tabla `joko_images` del LanceDB existente (junto a joko_notes de texto).

Arquitectura (validada 12-ago-2026):
- Embeddings de imagen: CLIP ViT-B/32 (transformers) → 512 dims, GPU
- Vector DB: LanceDB (tabla joko_images, misma DB que el RAG de texto)
- Consulta: búsqueda por imagen (query CLIP) o por texto (CLIP text encoder)
  → ambas comparten el mismo espacio vectorial CLIP
- Razonamiento: GLM (VLM local) para describir la imagen recuperada

Uso:
  python3 indexar_imagenes.py                      # indexa todo (incremental por hash)
  python3 indexar_imagenes.py --dry-run            # muestra qué haría
  python3 indexar_imagenes.py --query "perfume"    # busca por texto
  python3 indexar_imagenes.py --imagen foto.jpg    # busca por imagen

Fuentes indexadas (por defecto):
  ~/.hermes/image_cache/           (capturas de Telegram analizadas)
  ~/perfume-ia/data/fotos/         (fotos de perfumes)
  ~/joko-lab/research/**/img*      (imágenes en research)

Backup: no toca la BD de texto (joko_notes); crea tabla nueva (joko_images).
"""
import argparse
import glob
import hashlib
import json
import os
import sys
import time
from pathlib import Path

import lancedb
import pyarrow as pa
import torch
from PIL import Image
from transformers import CLIPModel, CLIPProcessor

DB_PATH = Path(os.path.expanduser("~/joko-lab/.lancedb"))
TABLE_NAME = "joko_images"
MODEL_NAME = "openai/clip-vit-base-patch32"
HASH_SIDECAR = DB_PATH / "index_images_hashes.json"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

FUENTES = [
    Path(os.path.expanduser("~/.hermes/image_cache")),
    Path(os.path.expanduser("~/perfume-ia/data/fotos")),
    Path(os.path.expanduser("~/joko-lab/research")),
]

EXT = (".jpg", ".jpeg", ".png", ".webp", ".heic")


def _cargar_modelo():
    t0 = time.time()
    print(f"[*] Cargando CLIP ({MODEL_NAME}) en {DEVICE}...")
    model = CLIPModel.from_pretrained(MODEL_NAME).to(DEVICE).eval()
    processor = CLIPProcessor.from_pretrained(MODEL_NAME)
    print(f"    Modelo listo en {time.time()-t0:.1f}s")
    return model, processor


def _hash_archivo(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _escanear_imagenes() -> list[Path]:
    encontradas = []
    for fuente in FUENTES:
        if not fuente.exists():
            continue
        for ext in EXT:
            encontradas.extend(fuente.rglob(f"*{ext}"))
    # dedup por ruta
    return sorted(set(encontradas))


def _embed_imagen(model, processor, path: Path) -> list[float]:
    image = Image.open(path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt").to(DEVICE)
    with torch.no_grad():
        out = model.get_image_features(**inputs)
    emb = out.pooler_output if hasattr(out, "pooler_output") else out
    emb = emb / emb.norm(dim=-1, keepdim=True)
    return emb[0].cpu().tolist()


def _embed_texto(model, processor, texto: str) -> list[float]:
    inputs = processor(text=[texto], return_tensors="pt", padding=True).to(DEVICE)
    with torch.no_grad():
        out = model.get_text_features(**inputs)
    emb = out.pooler_output if hasattr(out, "pooler_output") else out
    emb = emb / emb.norm(dim=-1, keepdim=True)
    return emb[0].cpu().tolist()


def _crear_tabla(db, nombre):
    schema = pa.schema([
        pa.field("path", pa.string()),
        pa.field("nombre", pa.string()),
        pa.field("fuente", pa.string()),
        pa.field("size", pa.int64()),
        pa.field("vector", pa.list_(pa.float32(), 512)),
    ])
    if nombre in db.table_names():
        return db.open_table(nombre)
    return db.create_table(nombre, schema=schema)


def _indexar(model, processor, db, force=False, dry=False):
    imagenes = _escanear_imagenes()
    print(f"[*] Imágenes encontradas: {len(imagenes)}")

    sidecar = {}
    if HASH_SIDECAR.exists() and not force:
        sidecar = json.loads(HASH_SIDECAR.read_text())

    tabla = _crear_tabla(db, TABLE_NAME)
    existentes = set()
    try:
        for row in tabla.to_pandas().to_dict("records"):
            existentes.add(row["path"])
    except Exception:
        pass

    nuevos = []
    for p in imagenes:
        h = _hash_archivo(p)
        if force or sidecar.get(str(p)) != h:
            nuevos.append(p)

    print(f"[*] A indexar: {len(nuevos)} (sidecar {len(sidecar)} previos, {len(existentes)} en tabla)")
    if dry:
        for p in nuevos[:10]:
            print(f"    [dry-run] {p}")
        return

    t0 = time.time()
    registros = []
    for i, p in enumerate(nuevos, 1):
        try:
            vec = _embed_imagen(model, processor, p)
            registros.append({
                "path": str(p),
                "nombre": p.stem,
                "fuente": p.parent.name,
                "size": p.stat().st_size,
                "vector": vec,
            })
            sidecar[str(p)] = _hash_archivo(p)
        except Exception as e:
            print(f"    [aviso] {p.name}: {str(e)[:60]}")
        if i % 20 == 0:
            print(f"    {i}/{len(nuevos)} ({time.time()-t0:.0f}s)")
    if registros:
        tabla.add(registros)
    HASH_SIDECAR.write_text(json.dumps(sidecar, indent=1))
    print(f"[✓] Indexadas {len(registros)} imágenes en {time.time()-t0:.0f}s | tabla: {TABLE_NAME} | total en tabla: {len(existentes)+len(registros)}")


def _buscar(model, processor, db, query_text=None, query_imagen=None, k=5):
    tabla = db.open_table(TABLE_NAME)
    if query_imagen:
        vec = _embed_imagen(model, processor, Path(query_imagen))
    else:
        vec = _embed_texto(model, processor, query_text)
    # búsqueda vectorial
    resultados = tabla.search(vec).limit(k).to_pandas()
    print(f"\n=== Resultados ({'texto: '+query_text if query_text else 'imagen: '+query_imagen}) ===")
    for _, r in resultados.iterrows():
        print(f"  {r['path']}")
    return resultados


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--query", type=str, default=None)
    ap.add_argument("--imagen", type=str, default=None)
    args = ap.parse_args()

    db = lancedb.connect(str(DB_PATH))

    if args.query or args.imagen:
        model, processor = _cargar_modelo()
        _buscar(model, processor, db, args.query, args.imagen)
        return

    model, processor = _cargar_modelo()
    _indexar(model, processor, db, force=args.force, dry=args.dry_run)


if __name__ == "__main__":
    main()
