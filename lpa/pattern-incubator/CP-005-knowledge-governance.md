---
type: lpa
subtype: pattern
status: incubating
tags: [lpa, pattern]
created: 2026-07-31
---
# CP-005: Knowledge Governance

**ID:** CP-005
**Fecha:** 2026-07-31
**Estado:** E0 — Candidate Pattern
**Origen:** ChatGPT (Fase B KAP — crítica adversarial)

---

## Qué ocurrió

ChatGPT señaló que el laboratorio tiene procesos para crear conocimiento pero no tiene reglas explícitas sobre quién tiene permiso para modificar cada nivel.

---

## Principio que emerge

> Un sistema de conocimiento sin reglas de gobernanza es un sistema donde cualquier afirmación puede convertirse en decisión sin pasar por los filtros adecuados.

---

## Matriz de permisos

| Nivel | ¿Quién crea? | Requisito mínimo | ¿Quién modifica? | ¿Quién retira? |
|-------|-------------|------------------|------------------|----------------|
| OBS | Cualquiera | Ninguno | Cualquiera | Cualquiera |
| HIPÓTESIS | Investigador | 2+ observaciones | Investigador + Crítico | Crítico |
| EXP | Experimentalista | Diseño reproducible | Experimentalista | Juez |
| DEC | Juez | Evidence Contract cumplido | Solo Juez | Juez + monitorización |
| PATTERN | Juez | 3+ dominios + falsación | Solo Juez | Juez + revisión |
| POLICY | Humano | Doble validación externa | Solo humano | Solo humano |

---

## Reglas clave

1. **Nadie puede promocionar su propio hallazgo.** El que formula la hipótesis no puede ser quien la valida.
2. **POLICY solo la modifica un humano.** Es la capa constitucional.
3. **Retirar una DEC requiere más evidencia que crearla.** Monitorización + intento de falsación fallido.
4. **El Evidence Contract es el guardián del paso EXP→DEC.** No se negocia.

---

## Condición de falsación

Este patrón sería FALSO si:
1. Las DEC creadas con governance no son mejores que las creadas sin ella.
2. El sistema de permisos bloquea más conocimiento válido del que filtra inválido.

---

## Decisión

Incubar. No implementar formalmente hasta que haya >20 DECs y aparezcan los primeros conflictos de autoridad.
