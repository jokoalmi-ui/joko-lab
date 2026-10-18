---
title: "MEL — Metacognitive Evaluation Layer (diseño)"
type: lpa
---

# MEL — Metacognitive Evaluation Layer (diseño)

**Estado:** DISEÑO (no consolidado) — 2026-08-04
**Autor:** Joseba + Hermes (síntesis de la conversación de 2026-08-04)
**Ubicación:** lpa/meta/ (documento de diseño; NO en GUIA-JOKO-LAB.md todavía)

## 1. Motivación

El laboratorio ha pasado por dos etapas:
1. Construir herramientas.
2. Construir conocimiento (KAP → KVC → KEL).

Ahora empieza la tercera: **medir la calidad del propio proceso de
construcción del conocimiento**. El siguiente salto no vendrá de añadir más
agentes o modelos, sino de que el laboratorio pueda demostrar con datos
cuándo aprende, cuándo se equivoca y cuándo debe olvidar.

## 2. Qué es MEL

Capa que evalúa la calidad del proceso cognitivo del lab (KAP, KVC, KEL).

- NO genera conocimiento.
- NO decide.
- NO modifica reglas.
- SOLO evalúa cómo han funcionado KAP/KVC/KEL.

### Pregunta central (reformulada)

> ¿Qué evidencia tengo de que mi proceso de razonamiento produce decisiones
> fiables?

("¿Estoy razonando bien?" NO es observable; lo observable es la evidencia de
que el proceso produce decisiones fiables. Evita convertir MEL en un
evaluador subjetivo del LLM.)

### Posición

```
KAP
 ↓
KVC
 ↓
KEL
 ↓
─────────────── MEL ───────────────
Evalúa cómo han funcionado KAP/KVC/KEL
```

El MEL NO pertenece al flujo operativo. Pertenece al flujo de evaluación.

## 3. Regla arquitectónica

```
RULE-MEL-001 (PROPUESTA — pendiente de validación)

Ninguna métrica puede existir
si no tiene asociada
una transición del sistema.
```

Ejemplos métrica → acción:

| Métrica              | Acción                |
| -------------------- | --------------------- |
| Sobreconfianza       | Reabrir DEC           |
| Baja trazabilidad    | Solicitar evidencia   |
| Confianza envejecida | Ejecutar revalidación |
| Alta reapertura      | Revisar proceso KVC   |
| KO sin revisar       | Lanzar pruning        |

Si una métrica nunca provoca ninguna transición → no pertenece al MEL.

NOTA: se marca como propuesta (no RULE activa) porque en el lab las RULE
derivan de DECs validadas. Hasta que MEL pase sus ciclos de validación, no
puede crear reglas activas.

## 4. Dimensiones del MEL

### 1. Calibración
Confianza declarada → resultado real.
Una DEC con confianza ALTA que produce resultado MALO = sobreconfianza o sesgo.

### 2. Calidad epistemológica
¿Qué porcentaje de DEC proviene de evidencia suficiente?
(Medible con trazabilidad: % de DECs que citan EXP/evidencia real al crearse.)

### 3. Evolución
¿Cuánto tarda el sistema en detectar que una DEC ya no vale?
(Tiempo DEC → superseded_by / retirada.)

### 4. Coste cognitivo
¿Cuánto cuesta mantener todo el mecanismo?
Riesgo real: un lab puede acabar dedicando más recursos a validar
conocimiento que a generar valor.

### 5. Plasticidad (nueva, añadida por Joseba)
¿Con qué facilidad cambia el laboratorio cuando aparece evidencia nueva?

Métricas de plasticidad:
- tiempo medio OBS → DEC
- tiempo DEC → superseded
- tiempo DEC → pruning
- % de DEC modificadas
- % de DEC nunca revisadas

Conecta directamente con el objetivo del KEL: capacidad adaptativa del sistema.

## 5. Piezas que YA existen en el lab (no partir de cero)

- thinking-patterns (skill) — patrones de razonamiento (materia prima)
- Pre-Flight Checklist — 6 verificaciones pre-respuesta
- Knowledge Resolver — confianza global + boundaries
- Confidence Decay — envejecimiento de confianza
- Evidence Contract — umbrales EXP → DEC (0/9 KOs cumplen: deuda señalada)
- Debt Detector — 6 checks de deuda del conocimiento
- VERIFIER — detector de falsos negativos (ejemplo real de metacognición:
  el proceso de verificación razonaba mal y se convirtió en hipótesis a falsar)

MEL = orquestación de estas piezas, no creación desde cero.

## 6. Reglas de diseño

1. Cada métrica dispara UNA transición concreta (RULE-MEL-001). Si no dispara
   nada → es ruido, fuera del MEL.
2. Umbrales NUNCA a priori: primero medir, después fijar umbrales
   (precedente: LoopEng F3 bloqueado hasta datos).
3. Riesgo a vigilar: que MEL derive hacia capa de evaluación meramente
   descriptiva. La salida de MEL debe ser accionable, no un informe.
4. Coste cognitivo como dimensión de primera clase: la metacognición sin
   control de coste se convierte en burocracia.

## 7. Orden de implementación (decidido por Joseba)

1. ✅ Documento de diseño en lpa/meta/ (este archivo)
2. 🔄 Validación mediante ciclos reales — EXP-MEL-001 EJECUTADO 2026-08-04
   (resultado: `01-knowledge/experiments/EXP-MEL-001-calibracion.md`)
3. ⏳ Incorporación a GUIA-JOKO-LAB.md (solo tras validación)
4. ⏳ Integración parcial en thinking-patterns

Razón: estamos en fase de diseño, no de conocimiento consolidado. La propia
epistemología del lab exige evidencia antes de promocionar.

## 8. Primer ciclo de validación (EJECUTADO 2026-08-04)

EXP-MEL-001 — estudio observacional de calibración sobre 17 KOs reales.
Resultado: éxito parcial (patrón F2: label no se actualiza con evidencia →
transición A1; caso VERIFIER como metacognición real), H1 SIN DECIDIR
(muestra joven: edad ≤9 días, 0 superseded, 0 reaperturas). Próximo:
EXP-MEL-002 tras 30-60 días.
