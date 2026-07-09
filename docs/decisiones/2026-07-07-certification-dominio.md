# 2026-07-07 — Creación del dominio certification/

**Estado:** Vigente

---

## Contexto

Hasta ahora, las pruebas de validación del conocimiento del laboratorio
(`docs/tests/`) estaban dentro de `docs/`. Esto mezclaba dos funciones distintas:
documentar el laboratorio y evaluar si alguien lo entiende.

Durante la sesión del 2026-07-07, se discutió la creación de un sistema formal
de certificación con casos normalizados, criterios de evaluación y ciclo de vida
propio.

## Problema

- `docs/` contiene documentación técnica. Mezclarla con material de evaluación
  rompe la separación de responsabilidades.
- No existía un mecanismo para validar que un agente (IA o humano) comprende
  el laboratorio.
- Las pruebas existentes (`test-01-contradicciones.md`, `onboarding-simulado.txt`,
  `3-evolucion-arquitectura-30-skills.txt`) eran documentos independientes sin
  formato común ni criterios de evaluación.

## Alternativas consideradas

1. **Mantener las pruebas dentro de docs/tests/**. Descartado porque mezcla
   documentación con evaluación y la certificación debe ser independiente de la
   fuente de verdad.

2. **Crear certification/ como dominio separado**. Elegido. La certificación
   es un subsistema con vida propia: especificación, casos, rúbrica y changelog.

3. **Mover las pruebas originales a certification/**. Descartado. Los originales
   son parte de la historia del laboratorio. La certificación contiene versiones
   normalizadas (C-001, C-002, C-003).

## Decisión

Crear `certification/` como quinto dominio del laboratorio, con la siguiente
estructura:

```
certification/
├── CERTIFICATION_SPEC.md   — especificación completa
├── CERTIFICATION.md        — resumen ejecutivo
├── RUBRIC.md               — criterios de evaluación
├── CHANGELOG.md            — historial de cambios
├── README.md               — guía de inicio
└── tests/
    ├── 01-comprension/     — C-001
    ├── 02-auditoria/
    ├── 03-arquitectura/
    ├── 04-evolucion/       — C-003
    ├── 05-operacion/
    ├── 06-recuperacion/
    ├── 07-seguridad/
    ├── 08-gobierno/
    └── 09-mentoria/        — C-002
```

Reglas fundamentales:

- La certificación **nunca será fuente de verdad**. La fuente de verdad es `docs/`.
- Los casos se identifican con formato `C-XXX` (no por nombre de archivo).
- Cada caso evalúa una competencia principal (C1-C9) y puede requerir habilidades
  secundarias.
- La certificación se actualiza siguiendo el ciclo definido en HERMES.md §13.

## Motivos

- Separa responsabilidades: documentación vs validación.
- Permite versionado independiente de la certificación.
- Los casos C-XXX son referenciables desde otros documentos (changelogs,
  decisiones, informes de auditoría).
- La rúbrica (5 criterios, 5 niveles) es simple, medible y suficiente.

## Consecuencias

**Positivas:**

- La documentación en `docs/` ya no contiene material de evaluación.
- Cualquier agente puede certificarse siguiendo la especificación.
- La certificación puede evolucionar sin contaminar la documentación técnica.

**Negativas:**

- Un dominio más que mantener. Pero su estructura es ligera (5 archivos + casos)
  y su ciclo de vida está definido.

## Archivos relacionados

- `certification/CERTIFICATION_SPEC.md` — especificación
- `certification/CERTIFICATION.md` — resumen ejecutivo
- `certification/RUBRIC.md` — rúbrica de evaluación
- `certification/CHANGELOG.md` — historial
- `certification/README.md` — guía de inicio
- `certification/tests/01-comprension/C-001-contradicciones.md`
- `certification/tests/04-evolucion/C-003-evolucion.md`
- `certification/tests/09-mentoria/C-002-onboarding.md`
- `docs/tests/test-01-contradicciones.md` (original conservado)
- `docs/onboarding-simulado.txt` (original conservado)
- `docs/3-evolucion-arquitectura-30-skills.txt` (original conservado)
