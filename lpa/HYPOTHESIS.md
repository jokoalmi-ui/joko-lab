---
type: lpa
subtype: lpa
status: active
tags: [lpa]
created: 2026-07-19
---
# LPA HYPOTHESIS — Lo que creemos pero no está verificado

## Propósito

Este documento contiene hipótesis activas sobre LPA. Son afirmaciones que nos parecen plausibles, que tienen cierta evidencia circunstancial, pero que **no han sido sometidas a intentos formales de falsificación.**

La diferencia con KNOWN.md: aquí las afirmaciones son especulativas. No deben usarse para justificar decisiones estructurales sin advertir que son hipótesis.

La diferencia con UNKNOWN.md: aquí hay una intuición formada. En UNKNOWN.md hay preguntas sin respuesta ni siquiera tentativa.

---

## Hipótesis sobre la naturaleza de LPA

### H001 — LPA es un sistema de preservación de identidad, no una metodología de diseño

- **Formulada:** 2026-07-19
- **Evidencia circunstancial:** Todos los conceptos que han emergido (trazabilidad, gobernanza, capas, leyes) apuntan a preservar coherencia, no a crear cosas nuevas. La pregunta que generó LPA no fue "¿cómo diseñar?" sino "¿cómo evitar que esto se descontrole?"
- **Qué la falsearía:** Si LPA resulta ser igual de útil para diseñar desde cero que para preservar sistemas existentes, entonces no es específicamente un sistema de preservación — es algo más general.
- **Experimento propuesto:** Aplicar LPA a diseñar algo completamente nuevo (sin legado que preservar) y medir si añade valor o sobre-ingeniería.

### H002 — La unidad mínima de LPA es el concepto, no la decisión

- **Formulada:** 2026-07-19
- **Evidencia circunstancial:** Los conceptos (Identidad, Silencio, Respiración) aparecen antes que las decisiones en la cadena causal. Las decisiones se derivan de conceptos. Los conceptos emergen de principios perceptivos o axiomas.
- **Cadena propuesta:** Axioma → Concepto → Ley → Decisión → Implementación
- **Qué la falsearía:** Si se demuestra que en dominios sin "conceptos" previos (ej: un producto diseñado empíricamente), las decisiones trazables son la unidad real que persiste.
- **Experimento propuesto:** Testear LPA en un dominio donde no existan "conceptos de diseño" previos y ver qué unidad persiste.

### H003 — Las 5 capas son contingentes, no necesarias

- **Formulada:** 2026-07-19
- **Evidencia circunstancial:** Emergieron en 2 experimentos, pero ambos son productos software con interfaz. No sabemos si un restaurante necesita 5 capas o 3. No sabemos si una empresa necesita 5 o 7.
- **Qué la falsearía:** Si 3+ experimentos en categorías distintas a "colección personal" muestran consistentemente 5 capas, la hipótesis se debilita y la necesidad se fortalece.
- **Experimento propuesto:** Aplicar LPA a un servicio físico (restaurante, museo) y documentar cuántas capas emergen naturalmente.

---

## Hipótesis sobre el alcance de LPA

### H004 — LPA funciona para sistemas complejos, no para sistemas simples

- **Formulada:** 2026-07-19
- **Evidencia circunstancial:** Perfume IA (44 archivos, ~14,500 líneas) y Biblioteca Personal justificaron la complejidad de LPA. Un script de 50 líneas probablemente no.
- **Qué la falsearía:** Si LPA añade valor medible a un proyecto de menos de 500 líneas de código o menos de 5 pantallas.
- **Experimento propuesto:** Aplicar LPA a un proyecto pequeño deliberadamente y medir si el overhead se justifica.

### H005 — LPA aplica a cualquier sistema que tenga "identidad", no solo software

- **Formulada:** 2026-07-19
- **Evidencia circunstancial:** Los conceptos de LPA (identidad, trazabilidad, gobernanza, experiencia, evolución) no contienen la palabra "código", "interfaz" ni "usuario". Son conceptos de sistemas, no de software.
- **Qué la falsearía:** Si al aplicar LPA a un restaurante o museo, los conceptos no mapean o requieren adaptación forzada.
- **Experimento propuesto:** Experimento Museo o Restaurante.

---

## Hipótesis sobre mecanismos internos

### H006 — LPA tiene un mecanismo de auto-descubrimiento (EMERGENT_CONCEPTS)

- **Formulada:** 2026-07-19
- **Evidencia circunstancial:** STATES, METABOLISM y AXIOMS emergieron durante la construcción de pantallas, no durante el diseño teórico. Esto sugiere que LPA genera conceptos por fricción con la realidad, no por especulación.
- **Qué la falsearía:** Si en un nuevo dominio no emerge ningún concepto nuevo durante la construcción de pantallas — sugeriría que el mecanismo es específico de Perfume IA.
- **Experimento propuesto:** En el próximo experimento, documentar si emergen conceptos nuevos no previstos.

### H007 — La trazabilidad es la columna vertebral de LPA; sin ella, LPA colapsa

- **Formulada:** 2026-07-19
- **Evidencia circunstancial:** La trazabilidad aparece en TODOS los documentos: CROSS_DOMAIN_AUDIT, FALSIFICATION_AUDIT, REFERENCE_SCREEN, EMERGENT_CONCEPTS. Es el único concepto que atraviesa las 5 capas.
- **Qué la falsearía:** Si se construye un producto consistente con principios LPA pero sin trazabilidad documental explícita, la trazabilidad sería un artefacto, no una necesidad.
- **Experimento propuesto:** Diseñar una pantalla sin referencias documentales explícitas y verificar si un tercero puede juzgar su consistencia con el producto.

---

## Hipótesis sobre falsabilidad

### H008 — Si LPA no puede falsearse, no es una teoría sino una creencia

- **Formulada:** 2026-07-19
- **Evidencia circunstancial:** P000 sigue sin respuesta. Mientras no sepamos qué falsearía LPA, todo el edificio es especulación organizada, no conocimiento verificable.
- **Qué la falsearía:** Si encontramos un criterio de falsabilidad claro y LPA lo sobrevive.
- **Experimento propuesto:** Dedicar una sesión completa a responder P000 antes de cualquier nuevo experimento.

---

## Hipótesis sobre el proceso cognitivo del lab

### H-HEL-001 — La activación deliberada del razonamiento antes de responder reduce los errores de primera respuesta

- **Formulada:** 2026-08-07. Reformulada el mismo día tras análisis externo:
  el fallo no es de conocimiento ni de divergencia, es de ACTIVACIÓN — el lab
  gobierna la validación pero no la generación de la respuesta. E0 en
  patterns-observed.md ("Divergencia deliberada antes de validar",
  actualizada a activación del razonamiento).
  ORIGEN REAL ANTERIOR: research/reasoning-gate-diseno.md (06-ago, Joseba) —
  RULE-PROC-001..005, State Question Detector y Evidence Arbitration Layer.
  H-HEL-001 es la formalización EVF de esa propuesta, no una idea nueva.
  FORMULACIÓN CANÓNICA (07-ago, sesión imagen LangGraph): la DECISIÓN de
  activar deliberadamente una fase previa de construcción de contexto y
  razonamiento, cuando la naturaleza de la pregunta lo requiere, reduce los
  errores de primera respuesta respecto a responder directamente desde la
  memoria paramétrica. Independiente del mecanismo (leer el LAB, RAG,
  herramientas, subagente, generar alternativas).
- **Evidencia circunstancial (solo casos verificados):** Cadena causal única
  documentada en research/reasoning-gate-diseno.md (sección 9.5): los tres
  incidentes (0.19?, 0.20.1, V003) — memoria → parece coherente → no se
  consulta la fuente → se responde → contradicción posterior. Fuentes:
  analisis-hermes-quicksilver.md (marcador "0.19? — verificar versión" sin
  contrastar, origen del SVP); reasoning-gate-diseno.md 9.1 (caso A2A);
  VERIFIER (falso negativo sistemático). El caso "Granite" NO está localizado
  como incidente de activación (solo existe el banco de evaluación
  history.jsonl): PENDIENTE DE VERIFICAR. Forma común: respuesta emitida antes
  de activar el contraste; todos los gates posteriores habrían pasado (no
  había marcador, estado declarado ni revisión).
  EVIDENCIA VERIFICADA 07-ago (sesión imagen LangGraph): con activación
  deliberada forzada (analizar el estado real del LAB antes de responder), la
  misma capacidad produjo un gap analysis específico en vez de la respuesta
  genérica de memoria — la capacidad existía, faltaba el disparador. Primera
  evidencia directa del mecanismo.
- **Naturaleza:** POLÍTICA de activación, no componente ni capa. No razona por
  sí misma: decide cuándo el sistema debe abandonar la respuesta inmediata y
  entrar en razonamiento profundo. La decide RULE-PROC-005 (State Question
  Detector) y la ejecuta el mecanismo existente tools/activation_engine.py
  (busca RULEs activas por task_type); PIL verifica que ocurrió; MEL mide si
  mejora. Sin sigla nueva, sin motor nuevo.
- **Qué la falsearía:** Si la activación deliberada (consultar fuente, generar
  ≥1 alternativa o contrastar memoria antes de responder, según el tipo de
  pregunta) no reduce la tasa de errores de primera respuesta respecto a
  baseline, o si el coste medido (tokens y latencia) supera el beneficio
  medido con la distribución real.
  PREDICCIÓN SECUNDARIA (07-ago): la activación del razonamiento no solo
  reduce errores — aumenta la PROBABILIDAD de que el conocimiento gobernado
  participe en la respuesta (más RULEs activas, más recuperación RAG, más
  fuentes consultadas y verificadas). Efecto observable del mismo mecanismo,
  medible en la EXP vía C con el execution path (HEL OFF path A vs HEL ON
  path B). Pregunta de la EXP en 2 pasos: (1) ¿la activación modifica
  sistemáticamente el path? (2) si sí, ¿ese path produce menos errores?
- **Métricas de activación (por tipo de pregunta):** factual → ¿se consultó
  fuente?; estado → ¿se contrastó memoria?; estratégica → ¿existieron ≥2
  alternativas?; diseño → ¿hubo síntesis? Cada una con distinción DECLARADA
  (auto-reporte del agente) vs VERIFICADA (evidencia de ejecución real en el
  Operations Ledger: comando lanzado, archivo abierto, fuente citada). La
  declarada sin verificación no es métrica (lección KVC-001: confidence
  auto-reportado = defecto; patrón SVP-A/SVP-B contra Goodhart). Equivalentes
  ya propuestos en reasoning-gate-diseno.md: MOR (Memory Override Rate) y MTE
  (Memory Trust Error), extensión de MEL-2.
  MÉTRICA ADICIONAL (07-ago): no solo ¿se activó?, sino ¿POR QUÉ se activó? —
  registrar el tipo de pregunta disparadora (estado/imagen/código/documento/
  arquitectura/factual) en el ledger. Permite calibrar el Router y detectar
  tipos que disparan sin necesidad (falsos positivos de activación).
- **Experimento propuesto:** Baseline primero sobre operaciones reales
  (OBSERVER / Operations Ledger), después intervención con activación
  deliberada: medir antes/después tasa de errores de primera respuesta, nº de
  alternativas generadas, coste en tokens y latencia, % de veces que la
  respuesta final no coincide con la primera, ratio activación
  declarada/verificada. Umbrales derivados de la distribución, nunca a priori.
  Diseño según disciplina EVF (ficha + EXP + informe). Si no aporta mejora
  medible, descartar. Si se confirma en varios casos, candidata a familia de
  patrones de razonamiento en thinking-patterns — no capa ni componente
  (choca con FREEZE, JL-005 y la dirección proyecto→LPA), y sin sigla nueva
  (RAL/CAP añade nombre sin definición operativa nueva).
  DECISIÓN DE JOSEBA (07-ago): vía C — instrumentar MOR/MTE primero (OBSERVER /
  Operations Ledger, baseline ≥1 semana), sin componente nuevo. Las vías (a)
  gate nuevo EVF, (b) ampliación de SVP y (d) Evidence Arbitration Layer
  quedan congeladas hasta que la EXP demuestre mejora medible. El selector
  previo ya está diseñado (RULE-PROC-005 + Evidence Arbitration Layer): falta
  la evidencia, no el diseño.
  RELACIÓN CON SESIÓN 2 (07-ago): research/mission-contract-diseno.md +
  lpa/contracts/mission.schema.json (ejecución de misiones, CAPA 2/3) — plano
  distinto (orquestación vs cognición) pero mismo principio: activación
  deliberada antes de ejecutar. No duplican; se instrumentan por separado.
  RESULTADO DEL CORTE DE FASE OBSERVACIONAL (14-ago-2026):
  - Informe: 04-operations/reports/2026-08-14-exp-hel-001-corte.md.
  - Ledger: respuestas_hel.jsonl (103 entradas, 07→13-ago, sin huecos,
    0 errores) actualizado con clasificacion (genuina/dudosa/ruido,
    validada por Joseba) y 51 activacion_verificada nuevas.
    Backup: respuestas_hel.jsonl.bak-20260814.
  - Datos: tasa de memoria entre GENUINAS 4/60 = 6.7%; periodo 07-10 =
    10.8% (4/37); periodo 11-13 = 0.0% (0/23). MOR/MTE n/a (0 overrides,
    0 errores). activacion_declarada inservible: 103/103 true por diseño
    del script (defecto del instrumento confirmado).
  - Las 4 respuestas de memoria son TODAS de la familia de preguntas
    cortas "¿cuánto queda / qué hay urgente?" (08-08, 09-08, 10-08 x2).
  - Veredicto: H-HEL-001 se SOSTIENE (señal >0, consistente en una familia
    identificable; el baseline discrimina). Matiz: 10.8% → 0.0% no
    distingue entre "el agente corrigió el patrón" y "cambió el tipo de
    pregunta" — la fase 2 debe controlarlo.
  - Decisión (14-ago): pasar a FASE 2 (activación deliberada) con criterio
    falsable — familia "¿cuánto queda" a 0 en 14 días, o tasa global de
    memoria < 6.7% con N ≥ 60. Mejoras de instrumento previas (registro de
    universo completo, golden set de ruido, verificación automática)
    diseñadas en research/exp-hel-001-fase2-instrumento-diseno.md. NO se
    implementa ToT/GoT/scratchpad/controller/debate permanente (freeze,
    sin evidencia, contaminarían la fase 2).

---

## Resumen

| ID | Hipótesis | Prioridad para testear |
|----|-----------|----------------------|
| H001 | LPA es sistema de preservación, no metodología de diseño | Alta |
| H002 | Unidad mínima = concepto, no decisión | Alta |
| H003 | 5 capas son contingentes, no necesarias | Alta |
| H004 | LPA funciona para sistemas complejos, no simples | Media |
| H005 | LPA aplica a cualquier sistema con identidad | Alta |
| H006 | LPA tiene mecanismo de auto-descubrimiento | Media |
| H007 | Trazabilidad es la columna vertebral | Alta |
| H008 | Si LPA no es falseable, no es teoría | Crítica |
| H-HEL-001 | Activación deliberada del razonamiento antes de responder reduce errores de primera respuesta | Alta (para estudio) |

---

FIN DEL DOCUMENTO HYPOTHESIS.md
