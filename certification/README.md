# Certification — Joko Lab

## Qué es

El dominio `certification/` contiene casos de validación diseñados para
comprobar que un agente (Humano o IA) comprende la fuente de verdad del
laboratorio: `docs/`.

Cada caso de certificación es un conjunto de preguntas, ejercicios o
escenarios que verifican:

- Conocimiento de la arquitectura y los servicios.
- Comprensión de las decisiones registradas.
- Capacidad de aplicar los principios del laboratorio.
- Habilidad para navegar la documentación existente.

## Reglas

1. **Nunca es fuente de verdad.** La fuente de verdad es `docs/`.
   Certification solo verifica que esa fuente se ha comprendido.

2. **Se adapta a los cambios.** Cuando se registra una nueva decisión o
   se modifica la documentación, certification se revisa y actualiza
   (ver HERMES.md §13).

3. **No hay nota eliminatoria.** Fallar un caso no es un error; es una
   señal de que la documentación necesita mejorar o el agente necesita
   más contexto.

4. **Los casos se numeran.** `001-tema.md`, `002-tema.md`, etc. para
   mantener un orden claro.

## Estructura de un caso

```markdown
# Título del caso

**Dominio:** [Gobierno | Operación | Conocimiento | Certificación | IA]
**Habilidades evaluadas:** [lista de skills necesarias]
**Dependencias:** [casos que deben haberse aprobado antes]

## Contexto

Explicación breve del escenario.

## Preguntas / Ejercicios

1. Pregunta o tarea concreta.
2. ...
3. ...

## Criterios de aprobación

- Criterio 1
- Criterio 2

## Referencias

- Enlaces a docs/ relevantes.
```

## Índice de casos

| # | Caso | Dominio | Estado |
|---|------|---------|--------|
| 001 | Constitución del laboratorio | Gobierno | Activo |
| 002 | Arquitectura y servicios | Operación | Activo |
