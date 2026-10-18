---
type: knowledge
subtype: experiment
status: active
tags: [knowledge, experiment]
created: 2026-07-28
---
# Runtime Feedback Loop — Propuesta de investigación

**Estado:** CONCEPTO EMERGENTE
**Fecha:** 2026-07-20
**Autor:** Derivado de conversación con Hermes
**Nivel de evidencia:** E0 (observación única, aún no aplicado)
**Revisión:** Corregido 2026-07-20 — de flujo directo a proceso epistemológico con tres niveles de mutabilidad en Governance

## Qué es

Un proceso por el que la evidencia obtenida del uso real de un producto puede modificar las reglas que lo gobiernan, **sin comprometer su identidad**.

No es una flecha. Es un proceso con filtros.

## El modelo corregido

La versión anterior proponía:

```
Runtime → Governance
```

Eso era incorrecto. Otorgaba al dato bruto autoridad para modificar principios, violando la regla más repetida del laboratorio: *la metodología no debe adelantarse a la evidencia.*

El modelo correcto incorpora el mismo proceso epistemológico que LPA ya exige para cualquier afirmación (niveles E0-E4, definidos en `lpa/EPISTEMOLOGY.md`):

```
Runtime (producto en uso)
    ↓
Observación (E0) — "El 80% ignora las recomendaciones matutinas"
    ↓
Patrón (E1) — misma observación semanas distintas, usuarios distintos
    ↓
Hipótesis (E2) — "Quizá el sistema habla demasiado pronto"
    ↓
Validación (E3) — experimento A/B, o patrón repetido en otro dominio
    ↓
Nuevo principio (E4) — la regla en Governance cambia
    ↓
Governance (actualizado)
```

Si un dato no alcanza al menos E2, no tiene derecho a modificar nada. Si alcanza E2 pero falla en E3, la hipótesis se descarta. Solo lo que sobrevive al proceso completo puede tocar Governance.

## Por qué este filtro es indispensable

Sin él, el producto se desintegra en optimizaciones locales: un A/B test aquí, un ajuste allá, y en seis meses nadie recuerda por qué existe. Cada experimento exitoso empuja en una dirección distinta, y la identidad se diluye sin que nadie lo note.

Con él, el producto mejora sin dejar de ser él mismo.

## Los tres niveles de mutabilidad en Governance

No todo en Governance puede cambiar con la misma facilidad. Sin esta distinción, un experimento exitoso podría acabar modificando la identidad del producto.

| Nivel | Qué contiene | Mutabilidad | Autoridad | Ejemplo en Perfume IA |
|-------|-------------|-------------|-----------|----------------------|
| **Identidad** | Propósito fundacional, lo que el producto ES | 0 (casi inmutable) | Fundador. Solo revisión humana extraordinaria | "El perfume es el protagonista", "No es una tienda", "La persona está en el centro" |
| **Constitución** | Reglas estructurales del producto, promesas fundacionales | 1 (muy baja) | Consejo humano. La IA puede asesorar, nunca decidir | "Nunca publicidad", "Nunca venta de datos", "Privacidad por defecto" |
| **Principios** | Reglas de diseño, experiencia, arquitectura | 4 (media) | Investigación validada. Evidencia E4 + revisión humana | "Silence", "Object First", "Presence precedes conversation" |
| **Estrategias** | Tácticas de implementación, algoritmos, parámetros | 10 (alta) | Runtime + IA. Aprendizaje automático con supervisión | "Retrasar 2 segundos la recomendación", "Usar temperatura como factor", "Cambiar una animación" |

La Identidad y la Constitución existen en un plano anterior al aprendizaje: no cambian porque el producto aprenda algo. Cambian, si acaso, porque el mundo ha cambiado tanto que el propósito original ya no responde a la realidad. Los Principios evolucionan con evidencia sólida. Las Estrategias se adaptan continuamente.

La columna de **Autoridad** es esencial: no basta con que un dato alcance E4. Hace falta que quien propone el cambio tenga legitimidad para hacerlo. Una IA puede proponer un cambio de Estrategia. No puede reescribir la Constitución, aunque el p-valor sea 0.001. La trazabilidad sin legitimidad es registro, no gobierno.

## Candidate Principle — el estado intermedio

Entre E3 (Validación) y E4 (Principio) existe un vacío. Una hipótesis validada no debería convertirse automáticamente en principio. Necesita un período de observación donde demuestre que no es un artefacto del experimento, ni una moda, ni una coincidencia.

Este estado intermedio —Candidate Principle— tiene tres propiedades:

1. **Ha superado E3** — existe evidencia sólida a su favor
2. **No ha alcanzado E4** — todavía no tiene autoridad para modificar Governance
3. **Acumula evidencia longitudinal** — observación continua mientras se buscan activamente contraejemplos

### Ciclo de vida: no solo asciende, también muere

Un Candidate Principle sin mecanismo de muerte se convierte en un vertedero epistemológico: candidatos acumulados que nadie revisa, algunos contradictorios entre sí, otros obsoletos porque el producto evolucionó por otro lado. Para evitarlo, cada Candidate Principle debe tener un destino definido. No solo Accepted.

| Destino | Motivo | ¿Puede reabrirse? |
|---------|--------|-------------------|
| **Accepted** | Evidencia suficiente acumulada. Ha sobrevivido a intentos razonables de refutación | No. Ya es un Principio (E4) |
| **Rejected** | Se encontró evidencia que lo contradice activamente | Sí, si aparece nueva evidencia independiente no contemplada en la refutación original |
| **Expired** | No apareció evidencia suficiente durante el horizonte de revisión definido | Sí, pero empieza un ciclo nuevo. No continúa el anterior |
| **Archived** | El conocimiento es válido pero dejó de ser relevante para el producto actual (ej: un principio sobre Home ya no aplica porque el producto eliminó Home) | Normalmente no. Pertenece a otra época del producto |

La diferencia entre Expired y Rejected es esencial. Rejected significa que sabemos que era falso. Expired significa que nunca llegamos a saberlo: simplemente no consiguió mantenerse vivo.

### Reglas del ciclo de vida

**Horizonte de revisión explícito.** Todo Candidate Principle debe tener un horizonte de revisión definido en el momento de su creación. No existe un N fijo universal. Un principio visual puede resolverse en tres semanas. Uno sobre evolución del gusto puede necesitar un año. Lo importante es que el horizonte se declare, no cuál sea el número.

**Refutación activa obligatoria.** El sistema no debe limitarse a esperar confirmaciones. Debe intentar refutar activamente el Candidate Principle antes de aceptarlo: buscar contraejemplos, probarlo en contextos adversos, exponerlo a condiciones donde sería más probable que fallara. Un principio no se acepta porque haya muchas pruebas a su favor. Se acepta porque ha sobrevivido a los intentos razonables de demostrar que era incorrecto.

### Flujo completo

```
Observación (E0)
    ↓
Patrón (E1)
    ↓
Hipótesis (E2)
    ↓
Validación (E3)
    ↓
Candidate Principle ← horizonte de revisión definido aquí
    ↓
    ├── Accepted (E4) → Governance
    ├── Rejected     → evidencia en contra
    ├── Expired      → sin evidencia suficiente en el plazo
    └── Archived     → conocimiento histórico, ya no relevante
```

La mayoría de los Candidate Principles nunca alcanzarán E4. Se descartarán porque el patrón era temporal, porque el experimento tenía un sesgo no detectado, porque una observación posterior los contradice, o porque simplemente dejaron de recibir atención. Esa tasa de descarte no es un fallo del sistema — es su mecanismo de defensa.

Sin este estado intermedio y su ciclo de vida completo, cualquier experimento bien diseñado tiene un camino directo a modificar las reglas del producto. Con él, solo lo que sobrevive a un escrutinio prolongado —y a intentos activos de refutación— gana ese derecho. Es la diferencia entre un sistema que aprende y un sistema que reacciona.

## La pregunta central de investigación

> ¿Cuál es el mecanismo legítimo por el que la evidencia obtenida en Runtime puede modificar las reglas de Governance sin comprometer la identidad definida en Product?

Responder esta pregunta con evidencia procedente de varios dominios (Perfume IA, psicología, bolsa, aprendizaje) es la condición necesaria para que el Runtime Feedback Loop ascienda de concepto emergente a componente verificado de LPA.

## Relación con LPA

LPA nació como un sistema de trazabilidad unidireccional:

```
Product → Governance → Experience → Implementation → Runtime
```

Ese es el **ciclo de construcción**. Responde a: ¿estamos siendo coherentes?

El Runtime Feedback Loop añade el **ciclo de aprendizaje**. Responde a: ¿qué hemos aprendido?

Juntos forman un sistema que no solo preserva la coherencia sino que la hace evolucionar:

```
                    CICLO DE CONSTRUCCIÓN
        Product → Governance → Experience → Implementation
            ↑                                         ↓
            │                                    Runtime
            │                                         ↓
            └── Principios ← E4 ← E3 ← E2 ← E1 ← E0 (Observación)
                    CICLO DE APRENDIZAJE
```

La implementación nunca aprende directamente. Aprenden los principios. Y después los principios vuelven a generar implementación. Esa es la diferencia entre un producto que reacciona y uno que aprende.

## Preguntas abiertas

1. ¿Quién decide qué evidencia es suficiente para cambiar una regla?
2. ¿Cómo se distingue una corrección de rumbo de una desviación oportunista?
3. ¿El ciclo debe ser automático o requiere intervención humana (L2 Loop Engineering)?
4. ¿Qué umbral de uso justifica activar el bucle? ¿Un usuario? ¿Cien? ¿Mil?
5. ¿El bucle pertenece a LPA core o es un patrón específico de productos con telemetría?
6. ¿Qué partes de Governance son Identidad, cuáles Principios y cuáles Estrategias? ¿Quién traza esa frontera y con qué criterio?
7. ¿Puede un cambio en Estrategias, acumulado durante meses, forzar un cambio en Principios sin pasar por el proceso E0-E4? (Riesgo de deriva por goteo)

## Estado

Concepto emergente. Corregido respecto a la versión anterior. No diseñado. No implementado. No planificado.

Documentado porque es la primera vez que aparece explícitamente la necesidad de un proceso epistemológico —no una simple flecha— para cerrar el ciclo de aprendizaje de un producto LPA.

## Conexiones

- [[OBS-001]] — OBS-001: observación del router
