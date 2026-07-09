# Especificación de la Certificación de Arquitectura de Joko Lab

Versión: 1.0
Estado: Vigente
Responsable: Joko Lab

---

# 1. Propósito

Verificar que un agente (IA o humano) es capaz de comprender, mantener, evolucionar
y gobernar el laboratorio Joko Lab utilizando exclusivamente la documentación
disponible.

No evalúa conocimientos teóricos aislados. Evalúa capacidades aplicadas sobre un
sistema real.

---

# 2. Principios

La certificación debe ser:

- **Objetiva** — las respuestas se evalúan contra criterios publicados.
- **Repetible** — el mismo agente obtiene el mismo resultado en condiciones equivalentes.
- **Independiente del modelo utilizado** — no favorece a un proveedor de IA sobre otro.
- **Basada en documentación real** — las respuestas se justifican con docs/ existentes.
- **Evolutiva** — se actualiza cuando el laboratorio cambia.
- **Versionable** — cada versión de la certificación es un snapshot evaluable.

**Regla fundamental:**

> La certificación nunca será considerada fuente de verdad del laboratorio.

La fuente de verdad es `docs/`. La certificación verifica que el agente comprende
esa fuente de verdad. Si un dato cambia, el cambio ocurre en `docs/`. La certificación
se adapta después.

---

# 3. ¿Quién puede certificarse?

La certificación está diseñada para:

- Hermes Agent
- Otros asistentes IA
- Colaboradores humanos
- El propio propietario del laboratorio

Todos realizan las mismas pruebas con los mismos criterios.

---

# 4. Competencias evaluadas

Cada caso de certificación pertenece a una única competencia principal.
Puede requerir habilidades secundarias de otras competencias.

## C1 — Comprensión

Capacidad para interpretar correctamente la documentación.
Debe demostrar que distingue hechos de suposiciones.

## C2 — Auditoría

Capacidad para inspeccionar el estado del laboratorio.
Debe detectar incoherencias, documentación obsoleta, redundancias y riesgos.

## C3 — Arquitectura

Capacidad para diseñar estructuras mantenibles.
Debe justificar las decisiones y evaluar ventajas e inconvenientes.

## C4 — Evolución

Capacidad para prever el impacto de cambios futuros.
Ejemplos: añadir nuevas skills, sustituir componentes, crecimiento del laboratorio.

## C5 — Operación

Capacidad para comprender cómo funciona el laboratorio.
Debe conocer Docker, n8n, IA, skills y el flujo operativo.

## C6 — Recuperación

Capacidad para actuar ante errores.
Debe identificar documentación necesaria, procedimientos, riesgos y pasos de
recuperación.

## C7 — Seguridad

Capacidad para proteger el laboratorio.
Debe priorizar integridad, seguridad y reproducibilidad.

## C8 — Gobierno

Capacidad para mantener el conocimiento del laboratorio.
Incluye documentación, decisiones, roles, redundancias y fuentes de verdad.

## C9 — Mentoría

Capacidad para explicar el laboratorio.
Debe adaptar la explicación al nivel del interlocutor.

---

# 5. Niveles de madurez

Las respuestas se clasifican en cinco niveles.

| Nivel | Nombre | Qué demuestra |
|-------|--------|---------------|
| 1 | Comprende | Responde correctamente. No aporta análisis. |
| 2 | Diagnostica | Detecta problemas. Explica causas. |
| 3 | Diseña | Propone soluciones. Justifica decisiones. |
| 4 | Optimiza | Compara alternativas. Prioriza mejoras. Analiza impacto. |
| 5 | Gobierna | Comprende el laboratorio como un sistema completo. Relaciona documentación. Detecta inconsistencias. Propone evolución. Mantiene coherencia global. |

---

# 6. Estructura de los casos de certificación

Cada caso debe contener:

- **Identificador único** — C-XXX (ej. C-001, C-002)
- **Competencia evaluada** — una competencia principal (C1-C9)
- **Nivel esperado** — nivel de madurez que se espera alcanzar
- **Objetivo** — qué se quiere comprobar
- **Contexto** — situación simulada
- **Pregunta** — enunciado concreto
- **Criterios de evaluación** — qué hace que una respuesta sea aceptable
- **Resultado esperado** — qué debería contener la respuesta

---

# 7. Criterios de evaluación

Cada respuesta se valora de 1 a 5 en:

| Criterio | Descripción |
|----------|-------------|
| Comprensión | Entiende correctamente el problema |
| Razonamiento | Justifica sus conclusiones |
| Coherencia | No contradice la documentación |
| Priorización | Ordena correctamente las acciones |
| Visión global | Relaciona distintas partes del laboratorio |

Puntuación máxima: 25 puntos.

---

# 8. Organización

```
certification/
│
├── CERTIFICATION_SPEC.md   ← este documento
├── CERTIFICATION.md        ← resumen ejecutivo y estado actual
├── RUBRIC.md               ← guía de evaluación detallada
├── CHANGELOG.md            ← historial de cambios de la certificación
├── README.md               ← explicación para quien llega nuevo
│
└── tests/
    │
    ├── 01-comprension/
    ├── 02-auditoria/
    ├── 03-arquitectura/
    ├── 04-evolucion/
    ├── 05-operacion/
    ├── 06-recuperacion/
    ├── 07-seguridad/
    ├── 08-gobierno/
    └── 09-mentoria/
```

Cada carpeta contiene uno o varios casos de certificación en formato
`C-XXX-descripcion.md`.

---

# 9. Reglas

- Un caso debe evaluar una única competencia principal.
- Puede requerir varias habilidades secundarias.
- No debe depender de conversaciones anteriores.
- Debe poder ejecutarse únicamente con la documentación del laboratorio (`docs/`).

---

# 10. Ciclo de vida

La certificación es un elemento vivo que evoluciona con el laboratorio.

```
Cambio en el laboratorio (arquitectura, servicio, decisión)
        │
        ▼
Registrar decisión en docs/decisiones/
        │
        ▼
Actualizar documentación en docs/
        │
        ▼
Revisar skills afectadas
        │
        ▼
Revisar certificación (¿algún caso queda obsoleto? ¿hace falta uno nuevo?)
        │
        ▼
Actualizar CERTIFICATION_CHANGELOG.md
```

Cada nueva capacidad importante del laboratorio debe reflejarse mediante:

- Nuevos casos de certificación.
- Actualización de competencias.
- Revisión de niveles de madurez.

---

# 11. Objetivo final

No obtener una puntuación.

Comprobar que cualquier arquitecto (IA o humano) puede mantener, evolucionar y
comprender Joko Lab utilizando únicamente la documentación oficial del proyecto.

La certificación debe convertirse en el mecanismo de validación continua del
conocimiento arquitectónico del laboratorio.
