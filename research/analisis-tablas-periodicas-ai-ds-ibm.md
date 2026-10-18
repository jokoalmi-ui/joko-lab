---
title: "Análisis — AI & Data Science Periodic Tables (IBM Technology, 15-ago-2026)"
type: research
---

# Análisis — AI & Data Science Periodic Tables (IBM Technology, 15-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://youtu.be/jAkB_qeATag (13:18, IBM Technology, inglés)
**Transcripción:** completa (en, 190 líneas — sin rate-limit)
**Fecha:** 2026-08-15 09:58 CEST (verificado con date)

---

## Qué propone el vídeo

**Concepto:** dos "tablas periódicas" (Data Science + AI) como **herramienta de
aprendizaje** (no oficiales — los autores Martin Keen y Aaron lo aclaran: "no
hay tabla periódica oficial ni para DS ni para IA, las creamos como ayuda
didáctica") y un **caso de uso real (Document Q&A)** que recorre los
"elementos" como un pipeline.

### Tabla de Data Science (Aaron)
- **Filas = madurez del dato:** fila 1 raw data (ETL, cleansing) → fila 2
  prepared (data engineering, data coding) → fila 3 model data (clustering,
  aggregation) → fila 4 validated insight (data governance, audit)
- **Columnas (grupos):** acquisition → preparation → modeling → generation →
  evaluation
- **Quantum addendum:** 5 elementos extra (quantum encoding, quantum metrics)

### Tabla de AI (Martin) — 5 grupos × 4 filas
- **Grupos:**
  1. **Reactive** — toman input y actúan (agentes)
  2. **Retrieval** — la memoria de la IA (embeddings, vector database)
  3. **Orchestration** — coordina piezas (RAG)
  4. **Validation** — mantiene el sistema honesto (guardrails, red teaming)
  5. **Models** — LLMs, thinking models (razonan antes de responder)
- **Filas:** primitives (prompt, embed, LLM) → composition (function calling) →
  deployment (framework) → emerging (multi-agent systems)

### El caso real: Document Q&A (chat con tus documentos)
**Reacción lineal (pipeline):**
1. **Rg (RAG)** — la pregunta se embeddea, se consulta la vector DB, top-chunks
2. **Go (guardrails/GO)** — decide qué chunks puede ver el analista (filtro de
   permisos)
3. **Pr (prompt template)** — chunks + pregunta → prompt (grounding)
4. **LG (LLM)** — genera respuesta anclada en los chunks
5. **GR (guardrails final)** — ¿la cita aparece en la fuente? ¿PII a redactar?

**De reacción lineal a LOOP (mejora continua):**
1. **DR (data drift)** — vigila la distribución (queries que se agrupan raro,
   feedback bajando) y dispara cuando se aleja del baseline
2. **Synthetic data** — la IA genera pares Q&A sintéticos cubriendo los
   patrones que fallan
3. **Ft (fine-tune)** — los pares sintéticos entrenan al modelo de embeddings
   ("esta pregunta debe caer cerca de este chunk")
4. → el embedding mejorado vuelve a **EM (embeddings)** — el sistema mejora
   solo, sin intervención manual

**Mensaje central:** *"As important as AI pipelines are, real-world AI runs on
good data science"* — el bucle de mejora (drift→synthetic→fine-tune) es lo
que hace que el sistema aprenda de la operación.

---

## Veredicto para el lab

### ✅ VALIDA + 2 GAPS REALES DETECTADOS

| Elemento del vídeo | Equivalente REAL en el lab | Estado |
|---|---|---|
| RAG (Rg) | **RAG LanceDB híbrido (20.237 filas, recall@5 100%)** | ✅ Implementado |
| Guardrails (Go/GR) | **Gates SVP + evidence_contract (F4) + KVC + KCR** | ✅ Implementado |
| Prompt grounding (Pr) | **Contexto estructurado + SVP** | ✅ Implementado |
| LLM (LG) | R1 local + DeepSeek cloud (router) | ✅ Implementado |
| **Data drift (DR)** | **Telemetría observa (MEL, ledgers) pero NO dispara acciones automáticas** | 🔴 **GAP REAL** |
| **Synthetic data + fine-tune embeddings (Ft)** | **NO existe — el lab no fine-tunea (decisión 05-ago)** | 🔴 **GAP (por decisión, no descuido)** |

### 🎯 El GAP más interesante: el LOOP de mejora automática

El vídeo describe el bucle: **drift detectado → datos sintéticos → fine-tune de
embeddings → vuelve al sistema**. El lab tiene la PRIMERA mitad (telemetría
observa: ledgers, MEL, evidence) pero **NO cierra el bucle**:
- La telemetría registra fallos (queries con recall malo) pero **no genera
  acciones correctivas automáticas**
- El lab NO puede fine-tunear embeddings en la A2000 (VRAM 12 GB) — el
  fine-tune de BGE-M3 es inviable en este hardware

**PERO la parte del bucle SÍ viable en el lab:**
- **Detectar drift de queries reales** (qué preguntas fallan en el RAG) → ya
  tenemos evaluar_rag.py (OP-007) y telemetría
- **Generar pares sintéticos Q&A con GLM local** (datos sintéticos con el LLM
  local = viable, es solo generación de texto)
- **Inyectar esos pares en el indexer** (como documentos de conocimiento) —
  sin fine-tune de pesos, el lab puede "cerrar el bucle" añadiendo al RAG lo
  que aprende de los fallos

**Es decir:** el lab puede implementar la MITAD viable del loop (drift →
síntesis → inyección en RAG) sin tocar el fine-tune. Eso es un **futurible
concreto y alineado con local-first.**

### 📌 También aprovechable (conceptual)

- **La tabla periódica de AI como material didáctico** — con el estilo decidido
  (texto + gráficos bonitos + español) sería un carrusel LinkedIn/TFM perfecto:
  "5 grupos × 4 filas" de la IA organizados como tabla → conecta con el lab
  (cada elemento del lab tiene su celda)
- **La distinción "reaction vs loop"** — explica por qué el lab mide (MEL,
  ledgers, gates): para convertir reacción en bucle de mejora

---

## Registro

- Guardado: research/analisis-tablas-periodicas-ai-ds-ibm.md
- Veredicto: **VALIDA + GAP REAL del loop de mejora (drift→síntesis→inyección
  RAG) viable sin fine-tune + material didáctico para LinkedIn/TFM**
- Relacionado: research/analisis-multi-modal-rag.md, RAG pipeline 12 etapas,
  evaluar_rag.py (OP-007)
