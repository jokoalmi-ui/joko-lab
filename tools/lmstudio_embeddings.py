"""lmstudio_embeddings.py — Usa el endpoint de embeddings de LM Studio en vez de cargar BGE-M3.

Ventajas:
- No compite por GPU con el modelo principal (Dolphin, Gemma, etc.)
- Elimina el CUDA Out of Memory cuando LM Studio está cargado
- Latencia similar (~1-2s vs ~3-5s de BGE-M3 en CPU)

Uso:
    from lmstudio_embeddings import encode
    vector = encode("texto a codificar")
    vectores = encode(["texto1", "texto2"])  # batch
"""

import requests
import numpy as np

LMSTUDIO_URL = "http://localhost:1234/api/v0/embeddings"
MODEL = "text-embedding-bge-m3"
DIM = 1024


def _is_available():
    """Verifica si LM Studio está respondiendo."""
    try:
        r = requests.get("http://localhost:1234/api/v0/models", timeout=2)
        return r.status_code == 200
    except Exception:
        return False


def encode(texts, model=MODEL):
    """Codifica texto(s) usando LM Studio API.

    Args:
        texts: str o list[str]
        model: nombre del modelo de embedding (default: text-embedding-bge-m3)

    Returns:
        numpy array de shape (n, 1024)
    """
    if isinstance(texts, str):
        texts = [texts]

    embeddings = []
    for text in texts:
        try:
            r = requests.post(
                LMSTUDIO_URL,
                json={"model": model, "input": text},
                timeout=30,
            )
            r.raise_for_status()
            data = r.json()
            emb = data["data"][0]["embedding"]
            embeddings.append(emb)
        except Exception as e:
            raise RuntimeError(f"LM Studio embedding failed: {e}")

    return np.array(embeddings, dtype=np.float32)


def is_available():
    """Verifica disponibilidad (para que el llamante decida si usar fallback)."""
    return _is_available()
