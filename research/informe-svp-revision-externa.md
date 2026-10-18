---
title: "Informe técnico: Incidente de incumplimiento del procedimiento de revisión (SVP)"
type: research
---

# Informe técnico: Incidente de incumplimiento del procedimiento de revisión (SVP)
**VERACIDAD:** [ALCANCE INTERNO]

**Fecha:** 06-ago-2026
**Estado:** para revisión externa. Documento de referencia del patrón: research/state-verification-pattern.md
**Origen del incidente:** revisión de research/analisis-hermes-quicksilver.md aprobada con marcador `0.19? — verificar versión` sin contrastar contra la fuente oficial (hermes-lab/docs/pendientes.txt)

**state_sources (SVP Fase 2):**
- research/state-verification-pattern.md
- hermes-lab/docs/pendientes.txt
- 04-operations/metrics/evolution.jsonl
**last_state_check:** 2026-08-06

---

## 1. Resumen ejecutivo

Durante la revisión de un documento del laboratorio se aprobó un análisis que contenía un marcador explícito de incertidumbre (`0.19? — verificar versión`) sin contrastarlo contra la fuente oficial del sistema.

El dato correcto existía. La fuente oficial existía. La herramienta para consultarla existía. El procedimiento no obligaba a hacerlo.

**No es un fallo de memoria. No es un fallo del modelo. Es un fallo del procedimiento de revisión.**

Ese mismo patrón ya había aparecido anteriormente en el laboratorio bajo formas distintas.

## 2. Causa raíz

Proceso actual aproximado: leer documento → revisar contenido → aprobar.

Para documentos con estado el flujo correcto: leer → clasificar → ¿contiene estado? (NO → revisión normal; SI → consultar fuentes oficiales → resolver incertidumbres → documentar evidencia → aprobar).

La diferencia es enorme. Consultar la fuente es hoy una buena práctica; debe convertirse en un requisito verificable.

## 3. Patrón observado

| Caso | Capa | Problema |
|---|---|---|
| 1 | RAG | Documento antiguo recuperado antes que el vigente. La vigencia estaba registrada, no participaba en el retrieval |
| 2 | Knowledge Objects | Los campos expires / superseded_by / status existían. El pipeline no los utilizaba (filtro opcional, expires ausente) |
| 3 | Revisión documental | Existía "0.19? verificar". Existía pendientes.txt. No se consultó |

Los tres casos comparten exactamente el mismo patrón: **la información de estado existe pero no participa obligatoriamente en la decisión.**

## 4. Hipótesis

La hipótesis deja de ser "el modelo olvidó consultar" y pasa a ser "el procedimiento no obliga a consultar". Eso cambia completamente el tipo de solución.

## 5. Solución propuesta

No añadir memoria. No añadir IA. No añadir otro agente. Añadir un **Gate Procedimental obligatorio**:

```
Operación → Clasificación → Gate obligatorio → Ejecución → Verificación → MEL
```

SVP sería el primer Procedural Gate. Mapa de gates:

| Gate | Disparo | Puerta | Estado |
|---|---|---|---|
| Gate-001 SVP | Documento con conocimiento de estado | SVP REPORT obligatorio | PROPUESTO (este informe + research/state-verification-pattern.md) |
| Gate-002 Evidence Contract | Se modifica un KO | Evidence contract | YA EXISTE en el lab |
| Gate-003 KVC | Se crea una DEC | KVC REPORT obligatorio (research/gate-003-kvc.md) | ESPECIFICADO 06-ago (sin implementar) |
| Gate-004 RULE | Se declara una RULE | EXP validado | YA EXISTE de facto (OBS→HIP→EXP→DEC→RULE) |
| Gate-005 KCR | Consulta RAG | Vigencia participa por defecto (research/gate-005-knowledge-context-resolution.md) | DISEÑADO 06-ago (sin implementar; EXP con banco de evaluación) |

## 6. Diseño del State Verification Pattern (SVP)

Fases (detalle completo en research/state-verification-pattern.md):
1. Clasificación: ¿contiene estado? NO → revisión normal; SI → SVP obligatorio.
2. Declaración explícita de fuentes (state_sources + last_state_check en frontmatter). No depende de la memoria del revisor.
3. Detección: buscar automáticamente marcadores (?, TODO, FIXME, verificar, confirmar, pendiente, sin confirmar...). Si aparece cualquiera: no existe revisión, existe tarea de resolución.
4. Resolución obligatoria con trazabilidad (marcador / fuente / resultado / acción).
5. SVP REPORT: sin el bloque final, SVP FAIL.

## 7. Observación importante (Goodhart)

Si el experimento mide únicamente "marcadores pendientes = 0", el sistema puede optimizar la métrica dejando de escribir marcadores: la incertidumbre desaparece del documento, no del razonamiento. Se miden dos variables independientes:

- A) Número de marcadores declarados (caída brusca = posible ocultación)
- B) Número de marcadores resueltos (objetivo: 100% de los declarados)

## 8. Relación con MEL

Este incidente es candidato natural para validación metacognitiva. MEL puede medir: revisiones con estado, revisiones con marcadores, revisiones con contraste documentado, tiempo hasta resolver un marcador, revisiones aprobadas sin evidencia, reaperturas posteriores. Así MEL evalúa la calidad del procedimiento, no la calidad del contenido.

## 9. Posicionamiento respecto al estado del arte

Precedentes parciales: detección obligatoria de marcadores (TODO/FIXME) en pipelines de integración y gobernanza de agentes; declaración explícita de fuentes y vigencia en contratos de datos. La aportación específica del laboratorio: integrar ambos conceptos dentro del ciclo de revisión de conocimiento gobernado (Knowledge Objects), con evidencia persistente y transición posterior hacia reglas del laboratorio.

## 10. Preguntas para revisión externa y respuestas (06-ago)

1. ¿La distinción descriptivo/estado justifica un gate específico? — SI. Los 3 casos comparten el mismo mecanismo: dato de estado presente pero no vinculante. La clasificación al inicio separa los dos caminos desde el primer paso.

2. ¿Existen patrones equivalentes? — Parciales: linters/CI que fallan ante TODO/FIXME; data contracts con vigencia. No se ha visto la combinación completa (clasificación + fuentes + detección + evidencia + métrica) integrada en un ciclo de conocimiento gobernado. Esa es la aportación específica.

3. ¿Procedural Gates es útil como capa independiente? — SI. El lab ya tiene 2 de 4 de facto (Evidence Contract, EXP para RULE). La capa formaliza lo que existe por costumbre. Riesgo: burocratización — cada gate debe dispararse por tipo de operación, no por voluntad del operador.

4. ¿state_sources obligatorio es carga excesiva? — Carga baja, beneficio alto: las fuentes canónicas son pocas y estables (3-5 rutas en frontmatter). El revisor deja de depender de recordar. Si la carga molesta, plantilla pre-cargada.

5. ¿Cubre los fallos observados? — Cubre los 3 casos. Escenario fuera: el filtro opcional de search.py muestra que un gate sobre DOCUMENTOS no cubre gates sobre CONSULTAS. El Caso 1 no es un documento con marcador: es una consulta que ignora vigencia → Gate-005 de retrieval (diseño pendiente).

6. ¿Mecanismos para que la vigencia participe obligatoriamente? — Dos niveles complementarios: (a) retrieval: estado/expires como filtro por defecto en search.py (pendiente "OKF Fase B"); (b) revisión: SVP REPORT. Uno evita recuperar datos muertos; el otro evita aprobar documentos sin contrastar.

**Matiz operativo (añadido en revisión):** el SVP REPORT no puede depender del detector de verificación actual (TD-001 da falsos negativos). La evidencia debe ser el bloque escrito por el revisor.

## Conclusión

La evolución del laboratorio pasa de mejorar modelos a mejorar el proceso que gobierna a los modelos. El incidente no revela una carencia de capacidad del LLM, sino una ausencia de un punto de control procedimental. Si la hipótesis se confirma mediante el experimento (OBS→HIP→EXP→DEC→RULE), el SVP dejaría de ser una recomendación y pasaría a ser un mecanismo de gobernanza verificable.

## Anexo (06-ago): marco de validación

Este incidente dio lugar al **Evolution Validation Framework (EVF)** — research/evolution-validation-framework.md — que formaliza los 5 niveles de validación de cualquier evolución del lab:

1. Gate Unit Test (¿funciona el gate?)
2. Regression Tests (¿vuelve a aparecer el incidente? — banco = único repositorio, "every bug becomes a test")
3. Behaviour Benchmark (¿el sistema responde mejor? — run_eval.py + history.jsonl)
4. MEL Metrics (¿mejoró el proceso de aprendizaje?)
5. Adoption Review (¿mereció la pena? — ficha con 6 preguntas, evidencia obligatoria)

Fichas registradas en 04-operations/metrics/evolution.jsonl: SVP-001, KVC-001, KCR-001. Ciclo de vida con estado intermedio BENCHMARK PASS (la evolución funciona pero aún no merece RULE).
