---
title: "Análisis — Infografía: 7 Types of AI Agent Memory (shiva.bytes)"
type: research
data_as_of: 2026-08-06
last_validated: 2026-11-05
next_review: 2027-02-05
superseded_by: []
invalidated:
  - claim: "Memoria prospective sin formalizar (fila 7 de la tabla)"
    since: 2026-08-07
    evidence: "04-operations/prospective-memory.md"
---

# Análisis — Infografía: 7 Types of AI Agent Memory (shiva.bytes)
**VERACIDAD:** [ALCANCE INTERNO]

**Fecha:** 06-ago-2026
**Fuente:** Telegram (imagen) — shiva.bytes
**Método:** GLM 4.6V local (LM Studio)

---

## Los 7 tipos de memoria

| # | Tipo | Ventana | Qué es |
|---|---|---|---|
| 1 | **In-Context / Working** | Corto | Lo que el modelo ve en su ventana de contexto (system prompt, mensajes recientes, tool outputs) |
| 2 | **Semantic** | Largo | Hechos/preferencias/conocimiento de dominio persistentes, desacoplados del momento |
| 3 | **Episodic** | Largo | Eventos pasados, conversaciones completas, ejecuciones |
| 4 | **Procedural** | Largo | Cómo hacer cosas: skills, patrones de uso de herramientas, workflows, reglas |
| 5 | **External / Retrieval** | Corto+Largo | Conocimiento fuera del modelo en vector DB, traído por similitud |
| 6 | **Parametric** | Largo | Conocimiento en los pesos del modelo (entrenamiento) |
| 7 | **Prospective** | Corto+Largo | Recordar intenciones futuras y metas planificadas sin ejecutar (long-horizon planning) |

## 🔗 Mapeo al LAB (lo importante)

| Tipo | Qué usa el lab | Estado |
|---|---|---|
| 1. Working | Contexto de sesión de Hermes | ✅ |
| 2. Semantic | **Memoria persistente de Hermes (MEMORY.md)** | ✅ |
| 3. Episodic | **Decision ledger + activation ledger + uso_diario** | ✅ |
| 4. Procedural | **Skills (perfume-ia, diagnostico, etc.)** | ✅ |
| 5. External | **RAG LanceDB + BGE-M3** | ✅ |
| 6. Parametric | Modelos locales (GLM, Dolphin) | ✅ |
| 7. **Prospective** | ❌ **NO lo tiene formalizado** | 🟡 |

## 🎯 Hallazgo: el gap del lab

**El lab cubre 6 de 7 tipos.** El que falta es **Prospective Memory** — recordar
intenciones futuras/metas planificadas. El lab tiene esto de forma implícita:
- Crons (informe diario, heartbeat, sueño 09:00)
- Backlog de pendientes
- Prueba 1 de cafeína (hasta ~17-ago)

**Pero no está formalizado como "memoria de intenciones"** — los crons son
mecánicos y el backlog no alimenta al agente en cada sesión.

## Veredicto

Infografía de 1 imagen que **valida el diseño de memoria del lab al 90%** — el
lab ya implementa los 7 tipos excepto Prospective formal. La conclusión práctica
de la infografía ("empieza con working, añade semantic cuando el usuario espera
que le recuerdes, añade el resto cuando necesite planear") coincide exactamente
con el camino recorrido del lab.

**Candidato a estudio:** formalizar Prospective Memory (intenciones/sprints
activos inyectados al inicio de cada sesión — el file bus de team-context podría
ser el vehículo).

---

## 🔄 ACTUALIZACIÓN 05-11-2026 — el gap del tipo 7 está cerrado

La fila 7 de la tabla («Prospective: ❌ NO lo tiene formalizado») **ya no es cierta**.
Medido en disco el 05-11-2026:

- `04-operations/prospective-memory.md` — creado **07-08-2026**, `status: active`,
  formato `- [ ] INT-NNN | descripción | deadline: YYYY-MM-DD | fuente: <ruta>`.
- Lo gestiona `~/.hermes/scripts/prospective.sh`.
- Su propio encabezado lo dice: «tipo 7 de memoria de agentes — el que faltaba formalizar».

Cobertura real del lab a fecha de hoy: **7 de 7**, no 6 de 7.

### Por qué se anota

El 05-11 llegó un reel de `codewithbrij` (04-11-2026, shortcode `DfWO9ZMuoQI`) repitiendo
la misma lista de siete, atribuyendo la idea a Neo Kim. **No aporta nada nuevo**: esta
infografía del 06-08 ya cubría la taxonomía completa, y `analisis-memoria-agentes-3-tipos.md`
(13-08) la superaba en profundidad al traer implementación real (langgraph + SQLite +
sentence-transformers + ablaciones). Veredicto del reel: reempaquetado, sin entrada.

**Lo que sí quedó demostrado** es que este análisis estaba desfasado: el futurible que
proponía («formalizar Prospective Memory») se ejecutó al día siguiente de escribirse.
Lección de proceso: un futurible registrado aquí caduca y hay que re-medirlo antes de
volver a citarlo (misma regla que `triaje-contenido-externo`).

**Fuente:** disco (`04-operations/prospective-memory.md`, `mtime` 2026-08-19 18:44, 2.191 B).
