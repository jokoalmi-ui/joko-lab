# Decisión: lab-manager pasa a Arquitecto Permanente

**Fecha:** 2026-07-07
**Estado:** Activa

## Contexto

El usuario identificó que Joko Lab ha superado la fase de "aprender Hermes" y necesita entrar en una fase de diseño de sistema que pueda evolucionar con mínimo esfuerzo manual. Propuso cinco niveles de madurez del proyecto y cinco pasos de evolución: Hermes como Arquitecto Permanente, lab-manager como cerebro, generación automática de documentación, indicadores medibles y niveles de madurez de skills.

## Problema

lab-manager estaba en etapa 2 (Diagnosticar) como Director Técnico. Ejecutaba diagnósticos predefinidos pero no tenía capacidad de evaluar proactivamente el laboratorio ni emitir juicios técnicos basados en datos. No había una escala objetiva para medir la madurez de las skills.

## Alternativas consideradas

1. **Dejarlo como estaba** — mantener solo scripts predefinidos sin capacidad de razonamiento. Descartado porque no resuelve la necesidad de evolución autónoma.

2. **Hacer un script de evaluación proactiva** — programar detección automática de incoherencias. Incompleto porque la evaluación humana (umbral de relevancia) no es programable.

3. **Evolucionar lab-manager a Arquitecto Permanente** — añadir capacidad de razonamiento al agente, no al script. La evaluación proactiva la hace Hermes en cada sesión usando un filtro de relevancia documentado. Esta es la opción elegida.

## Decisión

lab-manager pasa a v0.3.0 con el rol de **Arquitecto Permanente**. Esto implica:

- **Escala de madurez 0-7** implementada en `deuda-tecnica.sh`
- **Evaluación proactiva** en cada sesión, con filtro de relevancia (COMMANDS.md)
- **Filosofía operativa** como principio 2b de HERMES.md
- **Etapa 3 (Razonar)** — ya no solo diagnosticar, sino emitir juicios técnicos

## Motivos

- El usuario pidió explícitamente que Hermes evalúe continuamente el laboratorio
- La escala 0-7 da una métrica objetiva para medir progreso real
- El filtro de relevancia evita ruido y mantiene la atención en lo importante
- No se añade complejidad técnica — solo documentación y scripts que ya existían

## Consecuencias

- La deuda técnica del laboratorio se recalcula usando la nueva escala (resultado: 48% de salud)
- Las skills que antes se consideraban "vacías" ahora tienen niveles concretos (betterbird nivel 3, evolution nivel 3 — tenían documentación pero sin scripts)
- La documentación de lab-manager crece pero se mantiene en skills/, no en docs/
- Este cambio no afecta a n8n, Docker, ni servicios externos
