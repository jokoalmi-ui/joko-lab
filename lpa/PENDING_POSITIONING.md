---
type: lpa
subtype: lpa
status: active
tags: [lpa]
created: 2026-07-19
---
# LPA — Posicionamientos pendientes

Este documento registra comparaciones de LPA con otros enfoques. Cada entrada es una hipótesis, no una verdad establecida. Ninguna entra en el core hasta que tenga evidencia en 3+ dominios.

---

## LPA vs LLM Wiki (Karpathy)

**Estado:** Hipótesis fuerte [E2]

**Definición propuesta de LPA:** Sistema de trazabilidad causal para la evolución de productos.

**Diferencias clave:**

| Karpathy | LPA |
|----------|-----|
| Organiza conocimiento | Organiza decisiones |
| Optimiza contexto para LLM | Optimiza coherencia del producto |
| Navegación ("¿dónde está?") | Justificación ("¿por qué existe?") |
| Grafo asociativo | Cadena causal |
| La wiki es el artefacto | La trazabilidad es el artefacto |

**Relación propuesta:** La wiki de Karpathy puede ser el soporte de conocimiento sobre el que LPA opera. La wiki responde "¿qué sabemos del dominio?". LPA responde "dadas esas restricciones, ¿qué decisiones son coherentes con la identidad del producto?".

**Evidencia:**
- Perfume IA: la cadena THE_BOOK → VISION → ... → HTML funcionó como trazabilidad causal, no como grafo de conocimiento.
- Biblioteca Personal: mismo patrón.

**Pendiente:** Validar en un tercer dominio radicalmente distinto.

---

## LPA vs DDD (Domain-Driven Design)

**Estado:** Sin explorar.

---

## LPA vs Shape Up (Basecamp)

**Estado:** Sin explorar.

---

FIN
