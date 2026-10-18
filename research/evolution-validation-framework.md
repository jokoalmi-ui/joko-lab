---
title: "Evolution Validation Framework (EVF)"
type: research
---

# Evolution Validation Framework (EVF)
**VERACIDAD:** [ALCANCE INTERNO]

**Estado:** DISEÑADO 06-ago-2026. Primer uso con las evoluciones SVP, KVC y KCR.
**Propósito:** evaluar cada evolución del laboratorio con evidencia, no con impresiones. Cada evolución es un experimento falsable.

**state_sources (SVP Fase 2):**
- verification/bank.yaml
- verification/history.jsonl
- 04-operations/metrics/evolution.jsonl
- 04-operations/metrics/svp_exp.jsonl
**last_state_check:** 2026-08-06

---

## 0. Visión: los ciclos como Knowledge Learning Cycles

KAP → KVC → KEL → MEL no son módulos independientes: son la lógica de aprendizaje del sistema, cuatro ciclos con la misma estructura:

```
Observación → Hipótesis → Contraste → Decisión → Registro → Métrica
```

Lo único que cambia es qué objeto manipulan:

| Ciclo | Objeto | Produce |
|---|---|---|
| KAP (Acquisition) | conocimiento nuevo | EXP / DEC / RULE |
| KVC (Validation) | conocimiento existente | validado / rechazado / reabierto |
| KEL (Evolution) | conocimiento histórico | superseded / retired / merged / split |
| MEL (Meta-Evaluation) | el proceso de aprender | hipótesis / deudas / sesgos / propuestas |

**Decisión de nomenclatura (06-ago):** se mantienen KAP/KVC/KEL/MEL como nombres propios y se habla de "Knowledge Learning Cycles". NO se reutiliza el acrónimo LPA: en el lab LPA ya significa Living Product Architect (perfume-ia es su primer espécimen vivo) y cambiar ese significado tiene un coste conceptual alto. Un hipotético ciclo de "Decision Execution" (¿se aplica la RULE? ¿dónde falla?) NO está formalizado: existen piezas sueltas (Gate-005, SVP, Verifier, retrieval con vigencia) que aún no forman un algoritmo único. Se esperará a que aparezca de forma natural.

**Contrato común de validación de todo ciclo:**

```
Entrada → Proceso → Salida → Evidencia → Métrica → Acción
```

Un **LPA Verifier genérico** valida que cualquier nuevo ciclo cumple este contrato, en vez de escribir verificadores específicos por capa. La arquitectura crece por incorporación de LPAs que satisfacen un contrato común, no añadiendo componentes aislados.

---

## 1. Los 5 niveles de validación

Cada nivel responde una pregunta distinta:

| Nivel | Nombre | Pregunta | Mecanismo |
|---|---|---|---|
| 1 | Gate Unit Test | ¿Funciona el gate? | Casos PASS/FAIL mínimos por gate |
| 2 | Regression Tests | ¿Vuelve a aparecer el incidente? | verification/bank.yaml (incidentes convertidos en items permanentes) |
| 3 | Behaviour Benchmark | ¿El sistema responde mejor? | run_eval.py + comparador.py + history.jsonl (antes/después) |
| 4 | MEL Metrics | ¿Mejoró el proceso de aprendizaje? | Métricas longitudinales (MEL) |
| 5 | Adoption Review | ¿Mereció la pena introducir esta evolución? | Ficha EVF con evidencia |

### Nivel 1 — Gate Unit Test

Conjunto mínimo de casos PASS/FAIL por gate. Ejemplo SVP:

```
Documento sin estado → PASS (no ejecuta SVP)
Documento con estado sin state_sources → FAIL
Documento con estado con "?" sin SVP REPORT → FAIL
Documento con estado, 3 marcadores, 3 resueltos, SVP REPORT → PASS
```

Valida únicamente que el gate hace lo que promete.

### Nivel 2 — Regression Tests

Regla del laboratorio (a adoptar explícitamente):

> **Every bug becomes a test.**

Cada incidente real se convierte en un item permanente de verification/bank.yaml y nunca desaparece. NO se crean estructuras paralelas (tests/, incidents/) — el banco es el único repositorio.

Ejemplos ya presentes en el banco (verificado 06-ago):
- EXP1-001: prueba de vigencia (doc viejo vs vigente)
- EXP4-001: conflicto de vigencia Qwen 3.5 (04-ago) — coincide con el Caso 1 del informe SVP

Tras cada evolución del lab: run_eval.py ejecuta TODO el banco. Si un incidente vuelve a aparecer → regresión.

### Nivel 3 — Behaviour Benchmark

No mide PASS/FAIL: mide antes/después. El mecanismo ya existe (run_eval.py + history.jsonl con precision). Ejemplo:

```
Antes de Gate-005: EXP1 respuesta correcta 4/6
Después: 6/6
```

### Nivel 4 — MEL Metrics

Métricas longitudinales del proceso: tiempo medio hasta detectar obsolescencia, tiempo hasta reapertura, número de DEC revertidas, confianza alta con resultado malo, coste por decisión.

**Registro:** Metacognitive Ledger en 04-operations/metrics/mel_ledger.jsonl (aprendizajes sobre el propio proceso, no decisiones del dominio). Diseño completo en research/metacognitive-layer-diseno.md (MEL como función transversal; MEL-1 operativo, MEL-2 procedimental, MEL-3 arquitectónico). MEL-3 queda DECLARADO sin implementar (Architecture Freeze).

### Nivel 5 — Adoption Review (Evolution Benchmark)

La ficha de evolución. Seis preguntas obligatorias:

1. ¿Qué problema resolvía este cambio?
2. ¿Cómo se medía antes?
3. ¿Cómo se mide ahora?
4. ¿Cuál ha sido el coste (tokens, complejidad, mantenimiento, tiempo)?
5. ¿Qué evidencia demuestra que realmente mejoró? (OBLIGATORIA — enlaza con bank.yaml, history.jsonl o svp_exp.jsonl; sin evidencia, la ficha es una hipótesis documentada, no una evolución respaldada)
6. ¿Se adopta, se modifica o se retira?

Ejemplos de conclusión: ADOPTAR (evidencia positiva), MODIFICAR (evidencia parcial), RETIRAR (sin cambio medible).

**Métrica transversal de utilidad — Detection Yield (DY):**

```
DY = defectos descubiertos (clases únicas) / ítems revisados
```

**Definición explícita del denominador (fijada 06-ago):** "ítems revisados" = unidades de revisión sobre las que se aplicó el gate (documentos para SVP, DECs para KVC, consultas para KCR). Numerador = clases ÚNICAS de defecto (no instancias): si el mismo defecto aparece en 5 documentos, cuenta 1.

**Advertencia de comparabilidad (no comparar DY entre gates sin contexto):**
- DY es comparable INTRA-gate a lo largo del tiempo (¿el gate sigue encontrando defectos o se satura?)
- NO es directamente comparable INTER-gate: SVP (10 docs) y KVC (4 DECs) tienen denominadores de distinta naturaleza; un DY más alto no implica "mejor gate", puede reflejar solo que la población revisada era distinta o más defectuosa
- Para comparar gates entre sí, usar métricas complementarias: clases únicas encontradas, tasa de instancias (instancias/ítems), y DY normalizado por tipo de ítem

No mide si el procedimiento funciona (estabilidad), mide cuánto valor aporta (descubrimiento). Un procedimiento que nunca encuentra un defecto puede ser innecesario.

### Informe final de evolución (plantilla EVF)

Cuando una EXP termina (revisiones completas o plazo cumplido), se genera un informe con estructura fija — este es el primer caso completo del EVF y sirve como plantilla para todas las evoluciones futuras:

```
<evolution_id>

Problema original
↓
Incidente que lo motivó
↓
Diseño
↓
Resultados de la EXP
↓
Defectos encontrados
    - missing_state_sources
    - ...
↓
Coste
    - tiempo medio por revisión
    - pasos añadidos
↓
Detection Yield
↓
Recomendación
    ADOPTAR / MODIFICAR / RETIRAR
```

El informe se guarda en 04-operations/reports/ con el evolution_id (p. ej. 2026-08-XX-svp-001-evf.md). Cuando la plantilla funcione, el EVF deja de ser documento de diseño y pasa a ser proceso operativo repetible.

---

## 2. Ciclo de vida de una evolución

```
Diseño
  ↓
EXP
  ↓
BENCHMARK PASS        ← estado nuevo: la evolución funciona pero aún no merece RULE
  ↓
ADOPTADO
  ↓
RULE                  ← solo tras periodo de funcionamiento demostrado
```

Puede darse: EXP PASS → se adopta → funciona meses → aún no es RULE. Evita promover reglas demasiado pronto.

---

## 3. Identificador común (evolution_id)

Ficha y banco se enlazan por el mismo identificador; son dos vistas del mismo cambio, no dos mecanismos:

```
verification/bank.yaml   (comportamiento, items con evolution_id)
04-operations/metrics/evolution.jsonl   (ficha de evolución)
```

Ejemplo: SVP-001 existe en ambos con `evolution_id: SVP-001`.

---

## 4. Registro de fichas

04-operations/metrics/evolution.jsonl — una línea JSON por ficha, esquema:

```
{"evolution_id": "...", "fecha": "YYYY-MM-DD", "cambio": "...",
 "problema": "...", "media_antes": "...", "media_ahora": "...",
 "coste": "...", "evidencia": ["<ruta o id>"], "conclusion": "EXP|BENCHMARK PASS|ADOPTAR|MODIFICAR|RETIRAR|RULE"}
```

---

## 5. Fichas abiertas (06-ago-2026)

| evolution_id | Cambio | Estado | Evidencia |
|---|---|---|---|
| SVP-001 | Gate-001 State Verification Pattern | EXP (10 revisiones) | 04-operations/metrics/svp_exp.jsonl (baseline 06-ago: 1 FAIL + 1 PASS) |
| KVC-001 | Gate-003 Knowledge Validation Check | Diseño especificado, sin EXP | research/gate-003-kvc.md |
| KCR-001 | Gate-005 Knowledge Context Resolution | Diseñado, sin EXP | research/gate-005-knowledge-context-resolution.md |

Regla: sin ficha con evidencia, una evolución no se adopta como RULE.

---

## 6. Architecture Freeze (regla arquitectónica, 06-ago-2026)

**Decisión del responsable del lab.** El objetivo deja de ser diseñar y pasa a ser demostrar.

```
No puede incorporarse un nuevo componente
hasta que al menos DOS evoluciones anteriores
hayan completado su EVF (EXP → Benchmark → Adoptado).
```

Durante el freeze solo se permite:
- **validar** (aplicar los gates existentes)
- **medir** (recoger métricas de las EXP en curso)
- **retirar** (eliminar lo que no aporta)
- **simplificar** (reducir complejidad)

Motivo: el lab creció resolviendo problemas reales; a partir de cierto tamaño puede empezar a crecer porque es capaz de inventar nuevas abstracciones — el punto exacto donde los proyectos de arquitectura se vuelven excesivamente complejos. El freeze lo impide.

Evoluciones en curso bajo el freeze (las únicas permitidas): SVP-001, KVC-001, KCR-001. Hasta que dos de ellas completen EVF, no se diseñan nuevos componentes. La promoción de "every bug becomes a test" a RULE queda pendiente de ese ciclo (no es un componente nuevo: es formalizar lo que el banco ya hace).
