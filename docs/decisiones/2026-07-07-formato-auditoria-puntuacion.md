# Formato de auditoría ejecutiva con puntuación global

**Fecha:** 2026-07-07

## Contexto

La primera auditoría ejecutiva produjo un texto plano con secciones descriptivas. El usuario sugirió añadir una **puntuación global** y **barras visuales** por categoría para poder ver la evolución del laboratorio de un vistazo entre auditorías.

## Problema

Sin un número global, dos auditorías con el mismo "Estado general: OPERATIVO" son indistinguibles. No hay forma de saber si el laboratorio ha mejorado, empeorado o se ha estancado sin leer el informe completo.

## Alternativas consideradas

1. **Solo texto descriptivo** — como estaba originalmente.
2. **Puntuación global sin desglose** — un número rápido pero sin diagnóstico.
3. **Puntuación + barras por categoría** — la propuesta del usuario.

## Decisión

Las auditorías ejecutivas incluirán:

- **Puntuación global** (X.X / 10)
- **Desglose por categoría** con barra visual y puntuación:
  - Arquitectura
  - Documentación
  - Skills
  - Automatización
  - Seguridad
- **Bloque de comparativa** con la auditoría anterior (vacío en la primera)

## Motivos

- Un vistazo de 5 segundos basta para ver la tendencia.
- Las barras por categoría indican dónde actuar.
- La comparativa entre auditorías incentiva la mejora continua.

## Consecuencias

- Cada auditoría debe incluir una sección de comparativa con la anterior.
- Si es la primera auditoría, el bloque queda como "sin datos anteriores".
- El formato se incluirá como plantilla dentro de lab-manager.

## Estado

Aprobada.
