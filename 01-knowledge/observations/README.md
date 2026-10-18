---
type: OBS
subtype: observation
status: index
tags: [knowledge, observation]
created: 2026-07-29
---
# Flujo de conocimiento — Joko Lab
====================================

No se salta de observacion a decision. El flujo correcto es:

  OBS (Observacion)
    ↓
  HYP (Hipotesis)
    ↓
  EXP (Experimento)
    ↓
  DEC (Decision)

Cada nivel requiere mas evidencia que el anterior.

═══════════════════════════════════════════
NIVELES
═══════════════════════════════════════════

OBS — Observacion
  Se ha visto algo N veces de forma informal o en una sesion.
  No es reproducible necesariamente. No se toma ninguna accion.

  Archivo: 01-knowledge/observations/OBS-NNN.md

HYP — Hipotesis
  Hay una explicacion para la observacion. Se ha visto en al
  menos 2 contextos distintos. Pendiente de validar formalmente.

  Archivo: 01-knowledge/hypotheses/HYP-NNN.md

EXP — Experimento
  Validacion formal en condiciones controladas. Produce datos
  que confirman o refutan la hipotesis.

  Archivo: 01-knowledge/experiments/EXP-YYYYMMDD-NNN/

DEC — Decision
  Conocimiento lo suficientemente consolidado como para
  aplicarlo automaticamente. No se toma sin pasar por EXP.

  Archivo: 04-operations/decisions/DEC-NNN.md

═══════════════════════════════════════════
REGLA DE ORO
═══════════════════════════════════════════

No se puede crear una DEC sin un EXP que la respalde.
No se puede crear un EXP sin una HYP que lo motive.
No se puede crear una HYP sin una OBS que la origine.

Excepcion: experimentos exploratorios (EXP sin HYP previa)
que surgen de una pregunta, no de una observacion.

═══════════════════════════════════════════
EJEMPLO REAL
═══════════════════════════════════════════

OBS-001: "El router tiene tabla hardcodeada y consulta RAG.
          Son dos fuentes de verdad distintas."

HYP-001: "Si las dos fuentes divergen, el router tomara
          decisiones inconsistentes."

EXP-20260730-001: Comparar 20 consultas con tabla hardcodeada
                  vs RAG y medir cuantas divergen.

DEC-00X: "Eliminar la tabla hardcodeada. Unica fuente: RAG."

═══════════════════════════════════════════
FIN
═══════════════════════════════════════════
