---
type: lpa
subtype: lpa
status: active
tags: [lpa]
created: 2026-07-19
---
# LPA — Definición y alcance

## Definición actual (2026-07-19)

> **LPA es un sistema para construir sistemas complejos sin perder coherencia cuando intervienen humanos, IA y el paso del tiempo.**

### Evolución de la definición

| Fecha | Definición | Problema |
|-------|-----------|---------|
| 2026-07-17 | "Metodología de diseño de productos" | Demasiado amplio |
| 2026-07-19 (mañana) | "Sistema de trazabilidad causal para la evolución de productos" | Demasiado específico — "trazabilidad" es el mecanismo, no el propósito; "productos" excluye aprendizaje, gobierno, organizaciones |
| 2026-07-19 (tarde) | "Sistema para construir sistemas complejos sin perder coherencia cuando intervienen humanos, IA y el paso del tiempo" | Describe el propósito, no el método. "Sistemas complejos" incluye software, organizaciones, aprendizaje, gobierno. Nombra los tres agentes de cambio. |

---

## Mecanismo (no está en la definición, pero la implementa)

La **trazabilidad causal** es el mecanismo principal de LPA: cada decisión debe poder justificarse subiendo por las capas hasta el propósito. La **separación en 5 capas** (Product → Governance → Experience → Implementation → Runtime) es el modelo de organización que ha emergido hasta ahora.

Ambos son hipótesis [E1-E2], no principios. Pueden evolucionar sin que la definición cambie.

---

## Los tres agentes de cambio

| Agente | Qué introduce | Ejemplo |
|--------|--------------|---------|
| Humanos | Decisiones, emociones, sesgos, cambios de opinión | Un usuario cambia de gusto en perfumes |
| IA | Automatización, patrones, escala, deriva | Un agente optimiza sin entender el propósito |
| Tiempo | Obsolescencia, evolución, acumulación | Un producto sobrevive 10 años |

LPA existe porque estos tres agentes, combinados, tienden a degenerar cualquier sistema complejo. Sin humanos, no hay propósito. Sin IA, no hay escala. Sin tiempo, no hay evolución. Sin coherencia, el sistema se desintegra.

---

## Alcance

### Lo que LPA puede gobernar (hipótesis [E2])

- Productos software (Perfume IA)
- Sistemas de aprendizaje asistido por IA (Joko Lab)
- Asistentes de decisión bajo incertidumbre (Bolsa)
- Gobierno de agentes IA (Hermes + Skills + Auditorías)
- Relaciones humano-sistema (Psicología)

### Lo que probablemente NO gobierna (hipótesis sin evidencia)

- Sistemas caóticos sin identidad (prototipos desechables)
- Sistemas donde la coherencia no es deseable (experimentos artísticos)
- Sistemas de menos de ~500 líneas de código o equivalente

### Lo que no sabemos todavía

- Si funciona en organizaciones humanas (empresas, equipos)
- Si funciona en servicios físicos (restaurante, museo)
- Si escala a sistemas con cientos de agentes

---

## Casos de evidencia (no "productos")

LPA no mide cuántos productos tiene. Mide cuántos casos de evidencia ha acumulado.

| Caso | Dominio | Qué estresa | Estado | IE último caso |
|------|---------|------------|--------|---------------|
| Perfume IA | Producto de colección | Experience, coherencia, evolución | ✅ 4 pantallas | 14.3% |
| Biblioteca | Gestión de conocimiento | Trazabilidad, anatomía | 🧪 1 pantalla (sin HTML) | — |
| Bolsa | Decisión bajo incertidumbre | Tiempo real, síntesis, riesgo | 🔵 Construyendo | — |
| Joko Lab | Aprendizaje humano-IA | Verificación, evidencia, iteración | 🧪 Parcial | — |
| Hermes | Gobierno de agentes IA | Auditoría, no-invención, contexto | 🧪 Parcial | — |
| Psicología | Relación y confianza | Seguridad emocional, empatía | ⏳ Pendiente | — |

---

## Principio operativo

> LPA nunca debe adelantarse a una necesidad real de un caso de evidencia.

Los conceptos no se diseñan. Emergen cuando un caso real los necesita. Si no emerge nada en tres casos, no falta nada.

---

FIN
