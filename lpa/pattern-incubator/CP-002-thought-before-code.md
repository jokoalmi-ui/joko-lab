---
type: lpa
subtype: pattern
status: incubating
tags: [lpa, pattern]
created: 2026-07-25
---
# Separar el pensamiento del código

> **Estado:** Incubación (E0→E1)
> **Fecha:** 2026-07-25
> **Origen:** Análisis de alternativas open source a Lovable.dev — Joseba detecta que la pregunta correcta no es "qué herramienta" sino "qué capacidad"
> **Nivel de confianza:** Alto

---

## 1. Qué ocurrió

Al investigar alternativas open source a Lovable.dev, Joseba señaló que el análisis se había centrado en "qué herramienta instalar" cuando la pregunta relevante era "qué capacidad queremos adquirir en Joko Lab". Las herramientas de vibe coding (Lovable, Bolt, v0) no son valiosas porque escriban mejor HTML, sino porque tienen un **motor de proyecto**: un pipeline que va de objetivo → plan → arquitectura → archivos → código → correcciones → preview → iteración.

Este mismo patrón ya aparecía en Joko Lab: Hermes primero diseña la arquitectura, luego implementa, luego valida. Pero no está explicitado como capacidad diferenciada.

---

## 2. Evidencia que lo respalda

| # | Contexto | Descripción | Rol del patrón |
|---|----------|-------------|----------------|
| 1 | **Pipeline GLM→Gemma→Hermes** | GLM analiza (visión), Gemma extrae parámetros, Hermes razona y genera código | Análisis previo separado de generación |
| 2 | **KAP (M-001)** | Fase A extrae, Fase B critica, Fase C asimila | Separación explícita en fases con roles distintos |
| 3 | **Perfume IA** | Hipótesis → diseño → implementación → validación con personas reales | Ciclo completo con separación de pensamiento y ejecución |
| 4 | **Joko Lab runtime** | ai-router decide proveedor, luego Hermes ejecuta | Decisión separada de acción |
| 5 | **Análisis Graph Engineering** | El informe identifica que la industria está redescubriendo que un solo loop no basta — se necesita un sistema donde cada nodo tiene una responsabilidad única | Confirmación externa |

---

## 3. Contradicciones o limitaciones

1. **Para tareas simples, separar fases añade latencia innecesaria.** No todo necesita un plan antes de ejecutar.
2. **El coste de token aumenta** al tener fases separadas (plan + ejecución + validación).
3. **No hemos medido** cuánto mejora la calidad al separar pensamiento de código. Es una intuición, no un dato.
4. **Herramientas como Lovable/Bolt integran todo en una sola interfaz** — la separación es estructural, no de UX. No sabemos si la separación estructural es suficiente o si necesita también separación de interfaz.

---

## 4. Principio que parece emerger

> **Un agente debe diseñar la arquitectura antes de escribir código. La implementación y la validación son fases separadas con criterios distintos.**

### Corolarios operativos:
- Una tarea de construcción de software tiene al menos 3 fases: plan, ejecución, validación.
- Ninguna fase debe ser ejecutada por el mismo agente que la valida (ver CP-001).
- El plan debe ser explícito y verificable antes de empezar la implementación.
- La iteración no es un fallo del plan — es parte del proceso.

---

## 5. ¿En qué otros proyectos podría aplicarse?

| Proyecto/Dominio | Aplicación potencial |
|------------------|---------------------|
| **Perfume IA** | Ya lo aplica (hipótesis → diseño → implementación). Explicitarlo como patrón formal. |
| **Compan-IA** | Diseñar el sistema con fases separadas antes de codificar. |
| **N8n workflows** | Cada workflow complejo debería tener una fase de diseño antes de implementar nodos. |
| **Cualquier proyecto de software** | Aplicable universalmente a tareas de construcción que requieran más de un archivo. |

---

## 6. ¿Qué tendría que ocurrir para demostrar que este patrón es falso?

**Condición de falsación:**

> Que una tarea de construcción de software en Joko Lab (3+ archivos, lógica no trivial) ejecutada por Hermes en un solo paso (sin plan explícito previo) produzca un resultado de calidad igual o superior (evaluado por Joseba) que la misma tarea ejecutada con fases separadas (plan → código → validación), medida en 3 pruebas consecutivas.

**Criterio concreto:** Si en 3 tareas distintas, el resultado sin planificación explícita es funcionalmente equivalente y requiere menos tiempo total, el patrón se debilita.

---

## 7. Decisión

*[Se rellena en la revisión periódica, no al crear el documento.]*

- [ ] Asciende a KNOWN.md como E1
- [ ] Asciende a procedures/ como procedimiento LPA
- [ ] Sigue en incubación (falta evidencia)
- [ ] Se descarta (no sobrevive a otro dominio / fue falseado)
- [ ] Se fusiona con otro patrón

**Fecha de revisión:** 2026-08-01 (próxima revisión semanal)
**Justificación:** [Pendiente]
