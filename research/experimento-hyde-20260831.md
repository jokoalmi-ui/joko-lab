---
title: "Experimento HyDE vs RAG clásico — Joko Lab (31-ago-2026)"
type: research
---

# Experimento HyDE vs RAG clásico — Joko Lab (31-ago-2026)

**VERACIDAD:** [ALCANCE INTERNO]

**Fuente:** post dailydoseofds_ "RAG vs. HyDE, visually explained" (DctTkAciGWr, 31-ago) → señal del mapa de niveles RAG (niveles-rag-20260817.md: HyDE = nivel 7, futurible con señal "cuando queries vagas den recall pobre").
**Método:** script `tools/experimento_hyde.py` (solo lectura del índice; emb: text-embedding-bge-m3 vía LM Studio API; hipótesis: glm-4.6v-flash local 0€; comparación top-5 con las 8 consultas REALES del evaluador del lab). Ejecutado 31-ago 21:35 (LM Studio iniciado sin preguntar — tarea hablada; GPU 8.4 GiB).

## Resultado (salida real, top-5)

| Consulta | Clásico | HyDE | Cambio |
|---|---|---|---|
| estado refactorización complejidad | ✅ HIT | miss | ↓ |
| horario China UTC | ✅ HIT | ✅ HIT | = |
| prueba 1 cafeína | ✅ HIT | ✅ HIT | = |
| entrenador kettlebell | ✅ HIT | ✅ HIT | = |
| modelos locales LM Studio VRAM | ✅ HIT | ✅ HIT | = |
| decisiones arquitectura líderes | ✅ HIT | miss | ↓ |
| EXP-HEL respuestas herramientas | ✅ HIT | miss | ↓ |
| compactación LanceDB | ✅ HIT | ✅ HIT | = |

**Resumen:**
- **RAG clásico: 8/8 (100%)** · **HyDE: 5/8 (62.5%)**
- Mejoras: **0** · Empeora: **3** · Iguales: 5
- Latencia media: clásico **0.1s** · HyDE **47.8s** (generación hipótesis GLM + 2 embeddings)

## Veredicto: NO IMPLEMENTAR HyDE en el lab (resultado negativo honesto)

**Por qué empeora aquí (análisis honesto):**
1. **El lab ya tiene recall@5 = 100%** con retrieval clásico (BGE-M3 + reranker + consultas del evaluador). La señal de activación de HyDE era "queries vagas con recall pobre" — **esa señal NO se da**: las consultas del evaluador ya son razonablemente descriptivas y el pipeline ya las resuelve.
2. **Las hipótesis de GLM "inventan" el documento** (fechas 2023, nombres de experimentos que no existen en el corpus) → el embedding de un documento ficticio queda desplazado del espacio real de los chunks del lab → recupera peor.
3. **Coste enorme**: 47.8s vs 0.1s por consulta (la generación de la hipótesis en local). Para un RAG con recall 100%, ese coste no aporta nada.

**Cuándo SÍ valdría HyDE (señal reforzada):** si el lab consultara con queries MUY vagas/cortas (1-3 palabras) o sobre un corpus ajeno/ruidoso donde el recall bajara del 90%. Hasta entonces, el retrieval clásico es la elección correcta — y el experimento lo demuestra con datos.

**Valor del experimento:** validación negativa con evidencia (8/8 vs 5/8, latencia 470x) — exactamente el tipo de resultado que un TFM pide (no todo futurible técnico mejora un pipeline real). El script queda en tools/ para re-ejecutar si cambia la señal.

## Lección de proceso (para la skill local-rag)
- El path de LanceDB es el DIRECTORIO `.lancedb` (conectar + open_table("joko_notes")), NO la ruta de la tabla `.lance` — error inicial del experimento corregido.
- Re-ejecutar el experimento: `cd ~/joko-lab && ~/.venv/hermes-rag/bin/python3 tools/experimento_hyde.py -k 5` (requiere LM Studio con bge-m3 + GLM cargados).
- Resultado actualizado en backlog con backup RULE-008.
