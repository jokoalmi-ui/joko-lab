---
title: "Análisis — Carrusel datastreakofficial \"AI Agents Overview and Types\" (25-ago-2026)"
type: research
---

# Análisis — Carrusel datastreakofficial "AI Agents Overview and Types" (25-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://www.instagram.com/p/DceFm8kgXd2/ (datastreakofficial, 25-ago, 14 likes, 0 comentarios)
**Método:** pipelina IG — caption mínimo ("AI Agents Overview and Types" + hashtags) → contenido en las imágenes; el DOM expone 2 (portada + SLIDE 5/8 con texto completo en el alt). Las slides 1-4, 6-8 NO accesibles sin login (límite del lab validado).

## Contenido accesible: SLIDE 5/8 — UTILITY-BASED AGENTS

**Concepto**: agentes que van más allá de alcanzar metas: **evalúan cuán beneficiosa es cada acción** con una función de utilidad y eligen la mejor opción.

**Cómo funciona** (flujo):
Percepts → PREDICT OUTCOMES → CALCULATE UTILITY → CHOOSE BEST ACTION → Execute → Observe result → Update beliefs

**Características**: considera múltiples resultados, maneja incertidumbre, recomendaciones de decisión compleja.

**Ejemplo**: opciones de vuelo (3h20m vs 7h45m) — el agente compara y elige por utilidad.

**Casos reales**: Investment Agents · E-commerce Agents (optimizar producto) · Healthcare Agents · Autonomous Driving.

**Key takeaway**: evalúa la condición de cada acción, elige la acción con **mayor utilidad esperada**.

## 🔴 Aplicación al LAB — VALOR BAJO-MEDIO (material entrevistas, sin futuribles)

| Ángulo | Veredicto |
|---|---|
| **Tipología de agentes** | 🟡 Material de estudio/entrevistas (BBK/empleo): reflex, model-based, goal-based, utility-based, learning — el carrusel repasa la taxonomía clásica de Russell & Norvig |
| **¿El lab tiene utility agents?** | 🟢 Parcialmente: el **router (llvm-router.sh)** decide qué modelo usar por coste/VRAM = función de utilidad; el **LLM-as-judge** puntúa respuestas (utilidad); Hermes elige herramientas por objetivo |
| **Accionable** | ❌ Nada nuevo — es teoría educativa, no herramienta |

**Nota honesta**: solo la slide 5/8 es accesible (el usuario la envió con img_index=5). Las demás slides (tipos 1-4, 6-8) no se vieron — no se inventan. El patrón del carrusel es "taxonomía de agentes", contenido estándar de system design.

## Conclusión
VALOR BAJO-MEDIO: contenido educativo clásico de agentes. Valida que el lab ya implementa conceptos de "utility" (router, juez) sin llamarlos así. Útil como repaso para entrevistas, sin futuribles.
