---
title: "Análisis — Carrusel ds_ai_ketan: MLOps → LLMOps + Experiment Tracking (17-ago-2026)"
type: research
---

# Análisis — Carrusel ds_ai_ketan: MLOps → LLMOps + Experiment Tracking (17-ago-2026)

**Fuente:** https://www.instagram.com/p/DcKmOpfEux4/ (ds_ai_ketan — Ketan Sagare, carrusel, img_index=1)
**Método:** browser_get_images → descarga 2 slides (1440×1799, webp, sin efg — 120+133 KB) → GLM + browser_vision
**VERACIDAD:** [VERIFICADO]

## CONTENIDO (lo que dice)

### Slide 1 — "MLOps → LLMOps AT A GLANCE"

| MLOps (Model → Deploy → Monitor) | LLMOps (Model + Prompts + Data + Eval) |
|---|---|
| MODELS · DATA · FEATURES · INFRASTRUCTURE | LLMs · PROMPTS · RAG & Knowledge · AGENTS & TOOLS · EVALUATION & SAFETY |

**Simple View**: "Fewer components / More predictable / Traditional ML" → "More
components / More variability / LLM based systems"

**Key Idea**: "LLMOps extends MLOps to handle the unique challenges of LLMs,
Prompts, RAG, Agents and Evaluation in production." — Ketan Sagare

### Slide 2 — "EXPERIMENT TRACKING"

1. **¿Por qué rastrear?** Los sistemas AI cambian frecuentemente; rastrea todo
   para reproducir y mejorar; compara ideas con datos, no con memoria.
2. **MLOps vs LLMOps experiments**: Modelo→Métricas→Experimento vs
   Prompt→Búsqueda→Evaluación→Experimento
3. **¿Qué rastrear?**
   - Performance: precisión, latencia, throughput, tasa de error
   - Costo: tokens usados, costo API, cómputo, almacenamiento
   - Calidad: relevancia, tasa de alucinación, fundamentación, rating usuario
   - Otro: versión, entorno, etiquetas/notas, métricas personalizadas
4. **Recordar**: "Si no puedes reproducirlo, no puedes mejorarlo de manera confiable."
5. **Resumen**: "El seguimiento de experimentos es la base de sistemas AI
   confiables y repetibles."

## 🎯 APLICACIÓN AL LAB — MUY RELEVANTE (valida la observabilidad)

| Concepto | En el lab (real, verificado) |
|---|---|
| **"LLMOps = más componentes"** | El lab ES un sistema LLMOps: LLM + prompts + RAG (LanceDB) + agentes + evaluación |
| **Experiment Tracking** | **Prueba 1 biohacking = experiment tracking real** (hipótesis → medición diaria → decisión con datos, no memoria) |
| **"Compara ideas con datos, no memoria"** | **La regla #1 del lab** ("verificar > asumir", "no inventar") |
| **Rastrear: calidad (alucinación)** | Gate de veracidad + etiquetas [VERIFICADO]/[ALCANCE INTERNO] |
| **Rastrear: rendimiento/coste** | Monitor (localhost:5000) + política de costes + watchdogs |
| **Rastrear: versión/entorno** | GUIA v1.6.3 + backups .bak-* con fecha |

**"Si no puedes reproducirlo, no puedes mejorarlo"** = el principio del lab:
todo con salida real verificable, backups con fecha, decisiones documentadas.

## FORMATO (aislable)

- Estructura comparativa (2 columnas + simple view + key idea)
- Estructura "¿qué rastrear?" con 4 categorías (performance/coste/calidad/otro)
- Atribución al autor al final ("— Ketan Sagare") — patrón de autoría que
  encaja con la marca del lab

## Veredicto
**MUY RELEVANTE / VALIDA LA OBSERVABILIDAD DEL LAB.** El carrusel explica
LLMOps (extensión de MLOps con prompts/RAG/agentes/evaluación) y Experiment
Tracking — y el lab ya implementa ambos sin llamarlos así: Prueba 1 es un
experimento rastreado con datos (no memoria), el gate de veracidad mide
calidad/alucinación, y el monitor mide rendimiento/coste. "Si no puedes
reproducirlo, no puedes mejorarlo" = filosofía del lab. Material directo
para TFM/LinkedIn sobre observabilidad.
**Nota proceso**: descarga sin efg funcionó de nuevo (3º post consecutivo).
