---
title: "Prospective Memory — Joko Lab"
type: operations
status: active
created: 2026-08-07
description: "Índice de intenciones activas con plazo (metas planificadas a futuro). El detalle vive en la fuente; aquí solo el puntero + deadline. Gestionado por ~/.hermes/scripts/prospective.sh"
---

# Prospective Memory — Joko Lab

Memoria de intenciones/metas planificadas SIN ejecutar todavía (tipo 7 de
memoria de agentes — el que faltaba formalizar). Cada intención es una línea
con plazo; la fuente apunta a donde vive el detalle. NO duplica el backlog:
esto es lo que debe estar PRESENTE al inicio de cada sesión para no olvidar
lo planificado.

Formato de línea:
`- [ ] INT-NNN | descripción | deadline: YYYY-MM-DD | fuente: <ruta>`

## Activas

- [x] INT-001 | ~~EXP-HEL-001 baseline corte (vía C, activación)~~ **CERRADO 14-ago**: informe `04-operations/reports/2026-08-14-exp-hel-001-corte.md` (103 entradas, 6.7% memoria, 0.0% en 11-13; recomendación: sostener). Fase 2 (intervención acotada, skill intervencion-hel-fase2) ACTIVA desde 14-ago, 62 entradas al 19-ago; corte fase 2 ≈ 28-ago (EVF). | deadline: 2026-08-14 (cumplido) | fuente: joko-lab/01-knowledge/experiments/EXP-HEL-001-via-c-baseline.md
- [x] INT-002 | ~~Prueba 1 cafeína: corte 14:00, seguimiento diario energía/foco/sueño~~ **CERRADA 17-ago**: decisión "MANTENER corte de café a las 14:00 como regla permanente" (seguimiento-prueba1.md, sección "🏁 Decisión"); seguimiento post-decisión 18-19 ago activo. | deadline: 2026-08-17 (cumplido) | fuente: proyectos/biohacking-cerebral/04-medicion/seguimiento-prueba1.md
- [ ] INT-003 | Revisar uso Gemini (DEC-GAIPRO-001 next_review) | deadline: 2026-09-03 | fuente: joko-lab/01-knowledge/objects/DEC-GAIPRO-001.yaml
- [x] INT-004 | ~~Copiar formato cuaderno DBMS (espiral negra wire-o)~~ **CERRADO 09-ago**: la plantilla-cuaderno-block.html (creada 09-ago, validada 8/8 GLM) cubre el propósito (formato cuaderno para Founderz). El render DBMS se archiva como referencia. | deadline: 2026-08-08 (vencida, cerrada) | fuente: joko-lab/research/infografias/formato-cuaderno-dbms.html

## Completadas / caducadas

(historial — no se borra)
