---
type: knowledge
subtype: knowledge
status: active
tags: [knowledge]
created: 2026-07-29
---
# Jerarquia autoridad

JERARQUIA DE AUTORIDAD — Joko Lab
=====================================
Fecha: 2026-07-29
Estado: ACTIVA

Cuando dos fuentes del laboratorio entran en conflicto,
la de mayor jerarquia prevalece.

═══════════════════════════════════════════
NIVELES (de mayor a menor autoridad)
═══════════════════════════════════════════

1. EXPERIMENTOS REPRODUCIBLES
   Archivo: 01-knowledge/experiments/EXP-YYYYMMDD-NNN/
   Autoridad: MAXIMA
   Por que: Datos objetivos en condiciones controladas.
            La evidencia empirica siempre prevalece.
   Ejemplo: EXP-20260726-001 (35 tests, 7 modelos)

2. DECISIONES APROBADAS
   Archivo: 04-operations/decisions/DEC-NNN.md
   Autoridad: MUY ALTA
   Por que: Basadas en experimentos. Decisiones operativas
            que afectan al funcionamiento del laboratorio.
            Solo se modifican con nueva evidencia de nivel 1.
   Ejemplo: DEC-001 (Qwen 3.5 descartado)

3. PATRONES CONSOLIDADOS
   Archivo: 01-knowledge/patterns/
   Autoridad: ALTA
   Por que: Validados en multiples experimentos (E3).
            Representan conocimiento recurrente.
   Ejemplo: large-creative-model.md (E3 en 3+ condiciones)

4. FICHAS DE MODELO
   Archivo: 01-knowledge/models/*.md
   Autoridad: MEDIA-ALTA
   Por que: Describen un modelo especifico. Los datos de
            benchmarks en la ficha pueden quedar desactualizados
            si un experimento mas reciente los contradice.
   Ejemplo: granite-4.1-8b.md

5. OBSERVACIONES
   Archivo: 01-knowledge/observations/OBS-NNN.md
   Autoridad: MEDIA
   Por que: Dato puntual, no necesariamente reproducible.
            Puede ser un falso positivo. Necesita validacion.
   Ejemplo: observacion puntual (el router no bloquea modelos descartados)

6. HIPOTESIS
   Archivo: 01-knowledge/hypotheses/HYP-NNN.md
   Autoridad: BAJA
   Por que: No validada. Es una explicacion propuesta,
            no un hecho confirmado.
   Ejemplo: "Qwen 3.5 falla en cualquier configuracion"

7. DOCUMENTACION GENERAL
   Archivos: docs/, README.md, etc.
   Autoridad: MINIMA
   Por que: Puede estar desactualizada. Es referencia,
            no fuente de verdad.

═══════════════════════════════════════════
REGLA DE ORO
═══════════════════════════════════════════

Si un nivel superior contradice a uno inferior, el superior
prevalece. Si dos fuentes del MISMO nivel se contradicen,
prevalece la mas reciente.

Si una decision (nivel 2) contradice un experimento (nivel 1),
la decision debe actualizarse para reflejar el experimento.

═══════════════════════════════════════════
EJEMPLO REAL
═══════════════════════════════════════════

Conflicto detectado en Problema 5:

  Ficha Granite 4.1 dice: "JSON correcto" (E2)
  EXP-20260728-002 dice: "JSON valido pero envuelto en markdown"

  Jerarquia: Nivel 1 (experimento) > Nivel 4 (ficha)
  Resolucion: Prevalece el experimento. La ficha debe actualizarse
              para reflejar que el JSON es correcto pero requiere
              post-procesado a temp=0.7, o puro a temp=0.3.

═══════════════════════════════════════════
FIN
═══════════════════════════════════════════
