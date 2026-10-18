---
title: "Diseño — Capa Metacognitiva (Metacognitive Engine)"
type: research
---

# Diseño — Capa Metacognitiva (Metacognitive Engine)
**VERACIDAD:** [ALCANCE INTERNO]

**Fecha:** 04-ago-2026
**Estado:** ESPECIFICACIÓN DE DISEÑO — NO implementar todavía (decisión Joseba 04-ago)
**Origen:** propuesta de Joseba tras cerrar la iteración de Loop Engineering (F1-F2)

---

## 1. Separación de niveles (no mezclar conceptos)

| Nivel | Nombre | Objeto de observación | Estado |
|---|---|---|---|
| 1 | Operación | El sistema ejecuta (pregunta → retriever → LLM → decisión) | Implementado |
| 2 | Loop Engineering (F1-F6) | CÓMO decide el sistema (reglas, umbrales, frecuencia, fallos) | F1-F2 implementados; F3-F6 bloqueados hasta 1 semana de datos |
| 3 | Metacognición | EL PROPIO RAZONAMIENTO (suposiciones, evidencia, confianza, alternativas, info faltante) | DISEÑO — este documento |

Loop Engineering es ingeniería del comportamiento. Metacognición es razonamiento
sobre el razonamiento. No son lo mismo y no deben acoplarse.

## 2. Arquitectura de 4 capas desacopladas

```
Usuario
   ↓
Metacognitive Engine   ← evalúa la calidad del razonamiento
   ↓
Decision Engine        ← decide
   ↓
Knowledge Engine       ← almacena/conocimiento (KO, RAG)
   ↓
Ledger
   ↓
Loop Engineering       ← aprende de las decisiones
```

Cuatro responsabilidades distintas. Desacopladas para poder medir si cada una
aporta valor por separado.

## 3. Señales metacognitivas a registrar (por decisión)

Durante esta semana NO se cambia ninguna regla. SOLO se registra (ampliación
de la observación de F1, sin tocar el ledger actual):

```yaml
decision_id: 20260804-091255-b8d5280a
confidence: 0.7              # confianza declarada
evidence_count: 3            # piezas de evidencia usadas
knowledge_sources:           # qué se consultó
  - KO/RULE-002
  - ledger
  - bank.yaml
assumptions:                 # suposiciones no verificadas
  - "state.json disponible"
alternatives_considered:     # alternativas evaluadas
  - provider local
missing_information:         # qué faltaba
  - estado de costes del día
```

Regla: registrar, no decidir. La observación metacognitiva NO cambia el
comportamiento del sistema.

## 3b. MEL como función transversal (clarificación 06-ago-2026)

La metacognición NO es una etapa final (KAP → KVC → KEL → MEL). Es una
**función transversal** que observa a todos los demás ciclos. Responde siempre
a la misma pregunta: **¿cómo sé que estoy aprendiendo correctamente?**

```
            MEL
             │
 ┌───────────┼────────────┐
 │           │            │
KAP         KVC          KEL
 │           │            │
 ├───────────┼────────────┤
 │        Gates           │
 └───────────┼────────────┘
             │
            EVF
```

MEL observa todos los ciclos. No ejecuta ninguno.

### Tres niveles de MEL

| Nivel | Observa | Ejemplo de pregunta |
|---|---|---|
| **MEL-1 operativo** | Una decisión | ¿La confianza declarada coincidió con el resultado? |
| **MEL-2 procedimental** | Un procedimiento | ¿SVP encontró defectos? ¿Gate-005 evitó respuestas obsoletas? ¿KVC reabrió decisiones equivocadas? |
| **MEL-3 arquitectónico** | El propio LAB | ¿Las últimas 5 evoluciones redujeron incidentes? ¿Ha aumentado el coste? ¿Estamos añadiendo demasiada complejidad? ¿Qué componentes nunca producen valor? |

MEL-1 estaba planteado; MEL-2 acaba de aparecer con el EVF (Detection Yield,
fichas de evolución); MEL-3 queda DECLARADO como siguiente paso natural, SIN
implementar (coherente con Architecture Freeze: se documenta, no se construye).

### Metacognitive Ledger

Materialización de la metacognición: un ledger de aprendizajes sobre el propio
proceso (NO de decisiones del dominio). Registro en
`04-operations/metrics/mel_ledger.jsonl`:

```yaml
mel_id: MEL-2026-08-06-001
trigger: Incidente 0.19 (revisión analisis-hermes-quicksilver.md)
procedure: Revisión documental
root_cause: No se consultó la fuente de verdad (estado tratado como descriptivo)
systemic_change: Se crea SVP (Gate-001)
validated: en curso
evidence: EVF SVP-001 + svp_exp.jsonl
status: adoptado
```

Un DEC registra una decisión del laboratorio. Un MEL Ledger registra **cómo
cambia la forma de pensar del laboratorio**. Permite responder: ¿qué tipos de
errores procedimentales aparecen más? ¿qué cambios metodológicos tuvieron mayor
impacto? ¿qué hipótesis sobre nuestro propio proceso fueron refutadas? ¿cómo ha
evolucionado la calidad del razonamiento?

### Métrica MEL-Integrity (06-ago-2026, decisión DEC-004)

La metacognición también mide la **calidad del sistema de conocimiento**, no
solo la de las decisiones. Métrica:

```
MEL-Integrity

DEC totales.............N
confidence presente.....N
confidence legacy.......N   (null declarado, histórico no medido)
confidence ausente......N   (null sin declarar = defecto)
integridad..............%    (evaluables / totales)
```

Una DEC solo es completamente evaluable si tiene: evidencia, confidence (o
legacy declarado), rationale, provenance, history, estado — **Epistemic
Completeness**. Si falta algo sin declarar:

```
epistemic_completeness = false
```

Valor: permite responder "no puedo evaluar correctamente esta decisión porque
nació antes del modelo actual" — sin inventar el pasado. Aplicado 06-ago:
DEC-001/DEC-002 pasaron de "confidence ausente sin declarar" (defecto) a
"legacy declarado" (estado válido, contabilizado en MEL). La integridad pasó de
50% a 100% de DECs evaluables (DEC-004 como decisión de gobierno).

## 4. Qué NO hacer

- NO dejar que el modelo escriba "Creo que debería cambiar la RULE-008" — eso
  es opinión del LLM, no evidencia.
- Las propuestas deben emerger de datos observados, con forma:
  ```
  RULE-008 | Usos: 148 | Fallos: 2 | Último uso: hace 6d | Tendencia: +34% | Propuesta: revisar umbral | Confianza: 0.63
  ```

## 5. Relación con lo existente (real, no inventada)

- **Prediction Log (PRED-001/002, integrado 04-ago)** ya es metacognición
  incipiente: el sistema predice resultados y mide calibración por autor
  (quien_predice ≠ resuelto_por, anti-Goodhart). La capa metacognitiva lo
  EXTENDERÁ del nivel "predicción" al nivel "decisión".
- **thinking-patterns** (skill, patrón 15 Prediction Log) documenta el patrón.
- El ledger actual NO registra señales de razonamiento: solo
  timestamp/provider/model/reason/nivel/temperature/max_tokens. La capa
  metacognitiva necesitará instrumentación propia (no tocar el ledger hoy).

## 6. Hoja de ruta (decisión Joseba 04-ago)

1. Mantener F1-F2 EXACTAMENTE como están durante 1 semana (sin modificar reglas). ✅ alineado con el estado actual.
2. En paralelo: DISEÑAR esta especificación (hecho — este documento). NO implementar todavía.
3. Definir qué señales registrar (sección 3 — suposiciones, evidencia, confianza, alternativas, info faltante).
4. Al finalizar la semana: cruzar los datos del ledger (Loop Engineering) con las señales metacognitivas para decidir si una F3 debe ajustar no solo reglas sino también la calidad del razonamiento.

## 7. Preguntas que la capa metacognitiva responderá (tras 1 semana de datos)

- ¿Las decisiones con confianza >90% fallan más o menos?
- ¿Qué % de decisiones usan una sola fuente?
- ¿Cuántas decisiones contienen suposiciones no verificadas?
- ¿Cuántas veces se responde con evidencia insuficiente?
- ¿Qué tipo de KO se usa realmente?
- ¿Qué reglas jamás intervienen?

Metacognición basada en evidencia, no introspección simulada.

## 8. Verificación del diseño

- [x] Separa explícitamente Loop Engineering de Metacognición
- [x] No implementa nada (solo especificación)
- [x] Define señales observables (no opiniones)
- [x] Conecta con PRED existente (calibración por autor)
- [x] Hoja de ruta con corte semanal y criterio de cruce
