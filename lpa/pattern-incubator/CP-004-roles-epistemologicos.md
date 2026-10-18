---
type: lpa
subtype: pattern
status: incubating
tags: [lpa, pattern]
created: 2026-07-31
---
# CP-004: Roles Epistemológicos

**ID:** CP-004
**Fecha:** 2026-07-31
**Estado:** E0 — Candidate Pattern
**Origen:** ChatGPT (Fase B KAP — crítica adversarial)

---

## Qué ocurrió

ChatGPT señaló que el laboratorio es "Hermes-centrista": Hermes analiza, propone, clasifica, prioriza, escribe DEC y actualiza conocimiento. Falta diversidad cognitiva aunque todos los roles los ejecute el mismo agente.

---

## Principio que emerge

> La calidad del conocimiento no depende de cuántos agentes intervienen, sino de cuántas funciones cognitivas distintas se ejecutan antes de que una afirmación se convierta en decisión.

---

## Los 5 roles

| Rol | Función | Pregunta que responde |
|-----|---------|----------------------|
| **Investigador** | Formula hipótesis a partir de observaciones | ¿Qué podría ser cierto? |
| **Crítico** | Intenta destruir la hipótesis | ¿Cómo sé que es falso? |
| **Experimentalista** | Diseña experimento para validar/refutar | ¿Qué prueba lo decide? |
| **Juez** | Evalúa si la evidencia es suficiente | ¿Cumple el Evidence Contract? |
| **Archivista** | Convierte en Knowledge Object | ¿Dónde vive y cuándo caduca? |

---

## Aplicación al pipeline actual

```
Fase A (KAP)        → Investigador
Fase B (ChatGPT)    → Crítico
P1/P2/P3            → Experimentalista
Evidence Contract   → Juez
Knowledge Object    → Archivista
```

Ya existen todos los roles. Solo falta nombrarlos y tratarlos como funciones separadas.

---

## Condición de falsación

Este patrón sería FALSO si:
1. Separar roles no mejora la calidad de las DEC respecto a no separarlos.
2. El overhead de cambiar de "rol" entre pasos degrada la fluidez del análisis.

---

## Decisión

Incubar. No implementar como sistema formal hasta tener evidencia en 2+ dominios.
