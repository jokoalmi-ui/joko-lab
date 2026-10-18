---
title: "Análisis crítico — Infografía 'Traditional AI vs Agentic AI vs Agentic RAG'"
type: research
---

# Análisis crítico — Infografía "Traditional AI vs Agentic AI vs Agentic RAG"
**VERACIDAD:** [ALCANCE INTERNO]

**Fecha:** 04-ago-2026
**Fuente:** Post de Instagram de intellibooks.io (imagen recibida por Telegram)
**Imagen:** `~/.hermes/image_cache/img_57c85baa9f69.jpg` (infografía de 3 paneles)

---

## Lo que la infografía presenta

| Paradigma | Flujo | Nota de la imagen |
|---|---|---|
| Traditional AI | Define → Data → Clean → Features → Train → Deploy → Predict → Evaluate | "One-way flow, minimal adaptability" |
| Agentic AI | Understand → Objectives → LLM → Tools → Action → (loop: Evaluate → Plan → Iterate → Refine) | "Continuous learning and adaptive decision-making" |
| Agentic RAG | Goal → Retrieve → Vector Search → Context → Update KB → (loop: APIs → Reason → Memory → Generate → Adapt) | "Memory-enhanced, context-aware, evolving" |

---

## Veredicto global: parcialmente verdadero (6/10 precisión)

Es material de **divulgación con fines comerciales** (intellibooks.io vende libros).
Válido como resumen conceptual, pero simplifica en exceso y presenta como
jerarquía lo que son ejes complementarios.

---

## ✅ Lo correcto

1. Tradicional = pipeline menos autónomo (dirección correcta)
2. Agentic AI = bucle dentro de una tarea (conceptualmente cierto)
3. Agentic RAG = añade memoria/contexto externo (cierto en general)
4. Evolución estático → dinámico → contextual (tendencia real)

## ⚠️ Lo simplificado/exagerado

1. **"Traditional AI" como unidireccional puro** — falso: los modelos clásicos
   también iteran (retraining, evaluación, CV). Solo son menos autónomos.
2. **"Continuous learning" en Agentic AI** — EXAGERADO: la mayoría de agentes
   2026 ejecutan el bucle DENTRO de una tarea, pero NO persisten aprendizaje
   entre tareas. "Continuous learning" es aspiracional, no la realidad.
3. **"Agentic RAG" como cima de la escalera** — FALSO como jerarquía: RAG y
   agentic son complementarios (un agente sin RAG razona; un RAG sin agente
   no actúa). Son ejes ortogonales, no fases.
4. **Línea temporal implícita** — falsa: el RAG existe desde antes que el
   agentic comercial. La evolución no es lineal.

## 🎯 El punto más discutible

"Store in Long-term Memory... Adapt & Learn Over Time" — casi nadie lo hace
bien. La mayoría de "Agentic RAG" comerciales usan memoria de SESIÓN (contexto),
no memoria a LARGO PLAZO persistente. "Adapt & Learn" suele ser marketing sin
re-entrenamiento real.

**Nota relevante para el lab:** Joko Lab SÍ tiene memoria a largo plazo real
(LanceDB + knowledge objects + decision-ledger). El infográfico describe la
arquitectura del lab como ideal — pero la mayoría del mercado no la tiene.

## ❌ Lo que NO dice (y es crítico)

- Coste real de implementar memoria persistente
- Complejidad del "Agentic RAG" de verdad (lo más difícil de los tres)
- Que la evolución no es consecuencia automática, requiere diseño explícito

---

## Conexión con el lab

El paso de "Agentic AI" a "Agentic RAG" (bucle + memoria) es exactamente la
arquitectura de **Loop Engineering (L2)** diseñada el 04-ago
(`research/loop-engineering-diseno.md`):

- "Evaluate & Get Feedback" → decision-ledger.jsonl (326 entradas)
- "Iterate & Improve" → LPA: OBS→HYP→EXP→DEC
- "Store in Long-term Memory" → 01-knowledge/objects/ + wikilinks
- "Update Knowledge Base" → RAG re-index diario

La infografía sirve como **referencia visual** del patrón L2, con la salvedad
de que describe el ideal, no la práctica común del mercado.
