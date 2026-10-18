---
title: "Análisis — Agent with Episodic, Semantic and Procedural Memory (Deepak Jose, 20 slides)"
type: research
---

# Análisis — Agent with Episodic, Semantic and Procedural Memory (Deepak Jose, 20 slides)
**VERACIDAD:** [VERIFICADO]

**Fecha:** 13-ago-2026 (11:15 CEST)
**Fuente:** https://www.instagram.com/p/Db9xNeMmJ5g/ — datasciencebrain (Deepak Jose)
**Método:** 20 imágenes (HEIC→JPG), GLM 4.6V-Flash, 162s (8.1s/img).

---

## Qué dice el carrusel (tutorial técnico real con código Python)

**Objetivo:** construir en 60 minutos un agente de soporte con los 3 tipos de
memoria a largo plazo (sistema de ejemplo: agente de soporte de "PaySetta").

### Arquitectura (slide 2-3)
- Agente de soporte con 3 memorias: semántica, episódica, procedimental
- Módulo de recall: recupera contexto al llegar un ticket desde 3 fuentes
- Stack: Python 3.12+, `uv`, `langgraph`, `sentence-transformers`, SQLite

### Las 3 memorias (slide 5 — comparación en 5 ejes)
| Memoria | Qué guarda | Alcance | Trigger |
|---|---|---|---|
| **Semántica** | Hechos duraderos ("el cliente X tiene plan Y") | General/global | Actualización de hechos |
| **Episódica** | Eventos vividos ("intenté X y falló por Y") | Personal/histórica | Experiencias pasadas |
| **Procedural** | Cómo hacer las cosas (reglas, pasos) | Habilidades | Ejecución de tareas |

### Implementación (slides 6-19)
- **Semántica**: `SQLiteStore` + embeddings `sentence-transformers` (384 dims)
  + `Extractor` que lee mensajes y extrae solo "hechos durables" (plan, región)
  — evitando síntomas transitorios. Política: si el mismo hecho se actualiza →
  "colisión en lugar de conflicto" (modelo de datos lo resuelve).
- **Episódica**: modelo `Episode` con campos: texto, descripción,
  **tried_list (intentos fallidos)**, causa raíz, solución (`fix`). Se
  guarda "lo que funcionó y no funcionó" para aprender lecciones.
- **Procedural**: sistema de reglas EXTRACT_SYSTEM (cómo extraer hechos).
- **Ablaciones** (slide 8): configuraciones ablativas (sin componente X) para
  medir el impacto de cada memoria.

---

## 🎯 Veredicto — VALIDA el lab (los 3 tipos YA existen aquí)

| Memoria del carrusel | Lab equivalente | Estado |
|---|---|---|
| **Semántica** (hechos duraderos, embeddings, búsqueda) | **RAG LanceDB** (BGE-M3, 19.900 filas) + memoria de Hermes | ✅ Superior (más potente que SQLite+384dims) |
| **Episódica** (eventos, intentos fallidos, causa raíz, fix) | **Ledgers** (decisiones, OPs, activaciones) + file bus + session_search | 🟡 **Parcial — GAP de estructura** |
| **Procedural** (reglas de cómo hacer) | **Skills** (procedimientos + pitfalls) | ✅ Superior |
| **Ablaciones** (medir impacto de cada pieza) | Tests + evaluaciones | ✅ |

### 🟡 El único GAP real: memoria episódica sin estructura formal

El lab REGISTRA episodios (ledgers: qué pasó, decisiones tomadas), pero **no
con la estructura `tried_list / causa_raiz / fix`** que el carrusel usa:

- El lab documenta fallos en los **pitfalls de las skills** (informal)
- El carrusel estructura el episodio como: intentos fallidos + causa raíz +
  solución → **buscable y reutilizable**

**Futurible (bajo coste):** añadir a los ledgers o a un nuevo "ledger de
lecciones" el patrón episódico estructurado (tried_list, causa_raíz, fix) —
esto haría que los fallos pasados fueran **buscables** (como los pitfalls pero
en BD).

### Nota honesta
- El ejemplo (PaySetta, tickets de pago) es un caso de negocio distinto al
  lab — pero el PATRÓN de las 3 memorias es exactamente la arquitectura que el
  lab ya tiene (RAG + ledgers + skills).
- El stack del carrusel (langgraph + SQLite + sentence-transformers) es
  inferior a lo que el lab tiene (Hermes + LanceDB + BGE-M3) — no es un modelo
  a copiar, es una validación.
- La slide 20 es promoción de suscripción (ignorar).

---

## Conclusión

**VALIDA — el lab ya implementa las 3 memorias de agentes** (semántica=RAG,
episódica=ledgers, procedural=skills) con mejor stack. El único gap: la
memoria episódica del lab no tiene la estructura formal (tried_list, causa
raíz, fix) que haría los fallos pasados buscables. Futurible anotado.
