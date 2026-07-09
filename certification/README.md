# Certificación de Arquitectura de Joko Lab

Este directorio contiene el sistema de certificación del laboratorio.

## ¿Qué es?

Un conjunto de casos de prueba que verifican que un agente (IA o humano)
comprende, mantiene y puede evolucionar Joko Lab utilizando únicamente la
documentación oficial en `docs/`.

## ¿Qué contiene?

| Archivo | Propósito |
|---------|-----------|
| `CERTIFICATION_SPEC.md` | Especificación completa: propósito, principios, competencias, niveles, ciclo de vida |
| `CERTIFICATION.md` | Resumen ejecutivo con casos activos y estado actual |
| `RUBRIC.md` | Criterios de evaluación detallados (5 criterios, 5 niveles) |
| `CHANGELOG.md` | Historial de cambios de la certificación |
| `tests/` | Casos de certificación organizados por competencia |

## ¿Qué NO es?

- No es documentación del laboratorio (la documentación está en `docs/`).
- No es una skill de Hermes (las skills están en `skills/`).
- No es una fuente de verdad. Si hay conflicto, la fuente de verdad es `docs/`.

## ¿Cómo se usa?

1. Lee `CERTIFICATION_SPEC.md` para entender el sistema.
2. Elige un caso de `tests/`.
3. Responde el caso usando exclusivamente la documentación en `docs/`.
4. Evalúa la respuesta con `RUBRIC.md`.

## Primeros casos

| ID | Título | Competencia |
|----|--------|-------------|
| C-001 | Detección de contradicciones | Comprensión |
| C-002 | Onboarding simulado | Mentoría |
| C-003 | Evolución de la arquitectura | Evolución |
