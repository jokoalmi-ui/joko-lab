---
title: "Análisis — Multi-Modal RAG Pipeline (Aman Kharwal, 9 slides)"
type: research
---

# Análisis — Multi-Modal RAG Pipeline (Aman Kharwal, 9 slides)
**VERACIDAD:** [VERIFICADO]

**Fecha:** 09-ago-2026 (retomado; descargado originalmente 06-ago)
**Fuente:** https://www.instagram.com/p/DbF4g39moKL/ — amankharwal.official
**Método:** Descarga carrusel (9 slides) + GLM 4.6V local
**Tutorial completo:** https://amanxai.com/2026/07/22/build-a-multi-modal-rag-pipeline/

---

## Qué es

Tutorial práctico para construir RAG que recupera y razona sobre **texto E
imágenes** (PDFs con figuras/diagramas). Stack 100% open-source y local.

### Arquitectura (5 pasos)

1. **Extraer texto + imágenes** del PDF (pymupdf/fitz + pillow)
2. **Embeddings por separado**: texto con `BAAI/bge-small-en-v1.5`
   (SentenceTransformers), imágenes con **CLIP** (transformers/torch)
3. **Almacenar ambos** en una base vectorial (ChromaDB)
4. **Recuperar** texto + imagen coincidentes (top-k)
5. **Enviar a un VLM** (modelo de lenguaje con visión) para responder

### Stack
| Componente | Herramienta |
|---|---|
| Extracción PDF | pymupdf, pillow |
| Embeddings texto | sentence-transformers (BGE-small) |
| Embeddings imagen | CLIP (transformers+torch) |
| Vector DB | ChromaDB |
| Razonamiento | VLM (visión) |

---

## 🎯 Aplicación al LAB

### El lab YA cubre el 80% del pipeline

| Paso | Lab | Estado |
|---|---|---|
| Extracción texto | indexer (markdown/yaml) | ✅ |
| Embeddings texto | **BGE-M3** (mejor que BGE-small del tutorial) | ✅ |
| Vector DB | **LanceDB** (mejor que ChromaDB: híbrido FTS+vectorial) | ✅ |
| Razonamiento | Hermes + GLM 4.6V (visión) | ✅ |
| **Embeddings de imagen** | ❌ **NO existe** — el lab no indexa imágenes | **GAP** |
| Extracción imagen de PDF | ❌ NO existe | **GAP** |

### El GAP real: indexar imágenes

**El lab analiza muchas imágenes** (fotos de perfumes, infografías IG, capturas
de sueño) pero **no las indexa en el RAG** — se pierden. Un RAG multi-modal
permitiría:

- Indexar **fotos de etiquetas/decants** → búsqueda por imagen de perfume
- Indexar **infografías/capturas** (los cientos analizados por Telegram)
- Indexar **gráficos de la Band** (sueño) → consultas sobre tendencias visuales
- Consultas tipo "¿qué infografía hablaba de X?"

### Coste de implementación (estimado honesto)

| Componente | Coste en el lab |
|---|---|
| CLIP embeddings (imagen) | ~1-2 GB VRAM (CLIP ViT-B/32) — cabe en la A2000 junto a GLM |
| Pipeline de extracción | Script nuevo (adaptar indexer) — 2-4h |
| Indexación retroactiva | Re-correr sobre image_cache + capturas |

**Decisión pendiente:** ¿merece la pena el esfuerzo? El lab ya tiene GLM (VLM)
para ANALIZAR imágenes puntuales; la diferencia es poder BUSCARLAS después.

## Veredicto honesto

**Tutorial válido y ejecutable** (stack open-source, mismo estilo que el lab).
El lab cubre 4/5 pasos con herramientas superiores (BGE-M3, LanceDB). El único
gap real: **embeddings de imagen para indexar capturas/fotos**.

**Recomendación:** NO implementar ahora (el lab no tiene backlog urgente de
búsqueda de imágenes). Anotar como estudio para cuando el RAG lo pida — el
pipeline del tutorial sirve de plantilla (CLIP + LanceDB ya compatible).

## Nota

Aman Kharwal (amanxai.com) — autor de libros de ciencia de datos y ML.
El tutorial completo con código está en su web.
