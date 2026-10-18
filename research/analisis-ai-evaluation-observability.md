---
title: "Análisis — AI Evaluation & Observability Notes (Ketan Sagare, 10 slides)"
type: research
---

# Análisis — AI Evaluation & Observability Notes (Ketan Sagare, 10 slides)
**VERACIDAD:** [VERIFICADO]

**Fecha:** 12-ago-2026 (15:15 CEST)
**Fuente:** https://www.instagram.com/p/Db7OGHOEsVV/ — ds_ai_ketan (Ketan Sagare)
**Método:** 10 imágenes (webp→jpg, efg truncado OK — lección validada), GLM
4.6V-Flash, 90s total (9.0s/img)

---

## Contenido del carrusel (10 slides)

1. **Portada**: AI Evaluation & Observability — por qué importa (respuestas
   incorrectas/irrelevantes/inseguras + coste)
2. **Framework de evaluación en 3 capas**: Modelo (accuracy, reasoning, task
   success) → Aplicación (relevance, latency) → Sistema (cost, errors)
3. **Métricas de LLM en 3 categorías**: Calidad (correctitud, relevancia,
   fiabilidad) + Seguridad (toxicidad, PII leakage, violaciones de política)
   + Producción (latencia, coste, tasa de error). "Evaluación completa =
   Calidad + Seguridad + Rendimiento"
4. **Evaluación de RAG**: Calidad de Recuperación (Recall@K, Precision@K) +
   Calidad de Generación (fiabilidad/relevancia de la respuesta) + Flujo RAG
   (consulta → recuperación → generación)
5. **Dataset de evaluación**: por qué un set FIJO (comparar versiones, detectar
   problemas, rastrear mejoras); estructura de cada caso (pregunta, respuesta
   esperada, texto recuperado, respuesta AI); tipos de casos (fáciles,
   complejos, borde, falla)
6. **Observabilidad y tracing**: flujo (usuario → API → recuperación → LLM →
   respuesta); qué capturar (ID, latencia, info modelo, tokens, errores);
   para qué (encontrar causas raíz, depurar, analizar atascos, reducir coste)
7. **Detección de fallos de IA** (parcialmente extraído — GLM dio REASONING)
8. **Detección de fallos** (continuación — GLM dio REASONING)
9. **Ciclo de mejora continua**: consulta → respuesta → evaluar (tracing) →
   identificar debilidades → mejorar (prompt, modelo, recuperación, tools).
   Principio: **"No puedes mejorar lo que no mides"**
10. **Guía rápida / checklist**: medir lo importante, observar continuamente,
    detectar problemas temprano, mejorar cada día; pilares de observabilidad
    (métricas, logs, trazas)

---

## 🎯 Mapeo al LAB — VEREDICTO: VALIDA + 1 GAP REAL

### Lo que el lab YA tiene (validación)

| Capa del carrusel | Lab |
|---|---|
| **Evaluación de RAG** (slide 4) | ✅ **`evaluar_rag.py` — creado HOY (recall@K, 8 consultas, 100%)**. El carrusel valida exactamente lo que hicimos hoy |
| **Dataset fijo** (slide 5) | ✅ **`evaluar_rag.py` tiene 8 consultas con esperado** — el set fijo del lab |
| **Métricas de Producción** (slide 3) | ✅ Ledgers (latencia, coste, errores) + pipeline_obs |
| **Observabilidad/tracing** (slide 6) | ✅ Ledgers de decisiones/RAG/activaciones + file bus + watchdog |
| **Ciclo de mejora** (slide 9) | ✅ "No puedes mejorar lo que no mides" = el OBS→HYP→EXP→DEC del lab |
| **Checklist** (slide 10) | ✅ Crons de salud + umbrales del watchdog |

### El GAP real (lo único que falta)

**Seguridad (slide 3): toxicidad, PII leakage, violaciones de política**
- El lab NO tiene métricas de seguridad sobre sus respuestas
- La evaluación actual cubre Calidad + Rendimiento, pero no la capa Seguridad
- Es el único tercio del framework sin cubrir

### 🟡 Futuribles anotados
1. **Métricas de seguridad** (PII leakage, toxicidad) en el evaluador — bajo
   prioridad (el lab es local y personal, el riesgo de PII es bajo, pero la
   evaluación sería completa)
2. **Ampliar el dataset de evaluación** de 8 a más casos (incluyendo "borde" y
   "falla" como sugiere el carrusel) — barato y aumenta la confianza

---

## Conclusión

El carrusel **valida la arquitectura de evaluación del lab** (recall@K + set
fijo + observabilidad por ledgers + ciclo OBS→EXP→DEC). El lab cubre 2 de las
3 capas del framework (Calidad + Rendimiento); falta la de **Seguridad** (PII,
toxicidad) — un futurible menor dado el uso local y personal del lab.
El principio central del carrusel ("no puedes mejorar lo que no mides") es
exactamente la razón por la que hoy creamos `evaluar_rag.py` y por la que la
evaluación reveló el fallo de cobertura de biohacking.

## Nota técnica
- Descarga 10/10 (webp, efg truncado no afectó — lección validada otra vez)
- Slides 7-8 (detección de fallos) quedaron parciales (GLM dio REASONING en
  el prompt de resumen largo) — contenido general capturado, detalle menor
