---
title: "Análisis — Reel \"4 Estrategias de Indexación RAG\" (Daily Dose of Data Science, 11-ago)"
type: research
---

# Análisis — Reel "4 Estrategias de Indexación RAG" (Daily Dose of Data Science, 11-ago)
**VERACIDAD:** [VERIFICADO]

**Fecha:** 11-ago-2026
**Fuente:** https://www.instagram.com/reel/Db5zoMiDhX9/ — dailydoseofds_ (4h, 10s)
**Método:** Descarga MP4 + 5 frames + GLM. Nota: el alt del post mostraba también
"Prefill & Decode" (contenido del feed) — los frames del vídeo son de RAG Indexing.

---

## El contenido — 4 estrategias de indexación RAG

| Estrategia | Qué hace | Cuándo usarla |
|---|---|---|
| **Chunk Indexing** | Indexa el documento completo en trozos | La base — simple, la más común |
| **Sub-chunks Indexing** | Indexa subconjuntos de los chunks (granularidad fina) | Cuando los chunks grandes pierden detalle |
| **Query Indexing** | Indexa según las preguntas posibles sobre el dato | Cuando sabes qué preguntarán los usuarios |
| **Summary Indexing** | Indexa por resumen del documento (además o en vez del texto completo) | Cuando el contexto es limitado o hay muchos docs |

Diagramas: documentos → chunks/subchunks/resúmenes → base vectorial → consulta → contexto recuperado.

---

## 🎯 Aplicación al LAB — RELEVANTE (el RAG es un pilar del lab)

### Qué hace el lab hoy
- **Chunk Indexing** con BGE-M3 + LanceDB (19.569 filas, compactado hoy a 311 MB)
- Chunking simple de documentos (indexer.py)

### Lo que podríamos extraer (honesto)

| Estrategia | Lab | Aprovechable |
|---|---|---|
| Chunk Indexing | ✅ Ya lo hace | — |
| **Sub-chunks** | ❌ No (chunks planos) | 🟡 Mejoraría granularidad en docs largos (GUIA, skills) |
| **Query Indexing** | 🟡 Parcial (los ledgers se consultan por tipo) | 🟢 Futurible: indexar las preguntas típicas (estado, pendientes, perfumes) |
| **Summary Indexing** | ❌ No | 🟢 Futurible: indexar resúmenes de GUIA/skills para búsquedas rápidas de contexto |

### 💡 El hallazgo más valioso
**Summary Indexing + Query Indexing son baratos de probar** con el stack actual
(BGE-M3 ya genera embeddings; solo hay que indexar un resumen por documento o
las preguntas frecuentes). Con el LanceDB ahora compactado (311 MB), hay
margen para añadir estas estrategias sin inflar el índice.

**Pero la regla del lab:** el RAG actual ya cumple (búsquedas 0.08s, 19.5K filas).
Las 2 estrategias nuevas son **futurible** — se implementan si un caso real lo
pide (p.ej. las búsquedas de "estado del lab" fallan en recuperar contexto).

## Conclusión
Reel educativo (10s) que valida el enfoque de chunking del lab y añade 2
futuribles concretos (Query + Summary Indexing). Sin urgencia — el RAG actual
funciona bien. Guardado + backlog.

## Nota técnica
- GLM tardó ~10s/frame (rápido tras matar el huérfano de VRAM)
- El problema de carga de GLM era un llama-server huérfano (8.6 GB VRAM) — matado
  (autorizado), VRAM liberada, GLM cargado en 11.5s
- Patrón: tras reinicio o carga fallida, comprobar `nvidia-smi --query-compute-apps`
  por huérfanos antes de reintentar carga de modelo
