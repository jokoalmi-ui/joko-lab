---
type: lpa
subtype: lpa
status: active
tags: [lpa]
created: 2026-07-19
---
# LPA Epistemology — Cómo sabemos lo que creemos saber

## Propósito

Este documento no describe qué es LPA. Describe **cómo determinamos si algo que creemos sobre LPA es cierto, probable, especulativo o falso.**

Es la constitución epistemológica del programa de investigación LPA.

---

## Principio fundacional

> La evidencia debe ir siempre por delante de la metodología.

Traducción operativa: **ningún concepto entra en el núcleo de LPA sin un nivel de evidencia asignado. Ningún nivel se asigna sin un experimento que lo respalde.**

---

## Niveles de evidencia

Cada afirmación sobre LPA debe tener un nivel asignado. El nivel puede subir, bajar o ser revocado por nueva evidencia.

### E0 — Observación

**Definición:** Algo ocurrió una vez, en un contexto, y lo registramos.

**Criterio de asignación:**
- Ocurrió en exactamente 1 experimento.
- No hay evidencia de que ocurra en otro dominio.
- No hay explicación causal. Solo constatación.

**Derechos:** Ninguno. No puede usarse para justificar decisiones estructurales.

**Ejemplo:** "En Perfume IA, las 5 capas emergieron espontáneamente al organizar 16 documentos."

---

### E1 — Patrón

**Definición:** Algo ocurrió al menos 2 veces en contextos distintos.

**Criterio de asignación:**
- Ocurrió en 2+ experimentos.
- Los contextos son significativamente distintos (no dos colecciones).
- Hay una hipótesis de por qué ocurre, pero no está verificada.

**Derechos:** Puede mencionarse como "patrón observado". No como regla.

**Ejemplo:** "La separación Product → Governance → Experience apareció en Perfume IA y en Biblioteca Personal."

---

### E2 — Hipótesis

**Definición:** Creemos que esto es generalizable, pero solo ha sido testeado en un subconjunto limitado de dominios.

**Criterio de asignación:**
- Patrón observado en 2+ experimentos.
- Se ha formulado una explicación causal.
- Se ha intentado falsear al menos una vez sin éxito.
- No ha sido validado en un dominio radicalmente distinto.

**Derechos:** Puede usarse como guía de diseño. Debe etiquetarse como [E2] y citar los experimentos que lo respaldan.

**Ejemplo:** "La ausencia comunica. [E2] — Perfume IA, Biblioteca."

---

### E3 — Validación

**Definición:** Ha sobrevivido a intentos de falsificación en dominios radicalmente distintos.

**Criterio de asignación:**
- Testeado en 3+ dominios de categorías distintas (no 3 colecciones).
- Ha pasado al menos un intento deliberado de falsificación.
- No se ha encontrado un contraejemplo convincente.
- El patrón se mantiene sin modificar la estructura del concepto.

**Derechos:** Puede enseñarse como parte del núcleo. Debe seguir etiquetándose como [E3].

**Ejemplo:** "Los 10 órganos funcionales sobreviven en cualquier producto centrado en objetos. [E3] — Perfume IA, Biblioteca, Vinos."

---

### E4 — Principio

**Definición:** No recordamos ningún caso que lo contradiga. Es tan estable que lo tratamos como verdad operativa.

**Criterio de asignación:**
- 5+ dominios de al menos 3 categorías radicalmente distintas.
- Múltiples intentos de falsificación fallidos.
- Ningún contraejemplo documentado en al menos 6 meses.
- La comunidad de práctica (si existe) no reporta violaciones válidas.

**Derechos:** Puede usarse como fundamento para derivar otras afirmaciones.

**Atención:** E4 no significa "verdad absoluta". Significa "no hemos encontrado cómo romperlo todavía". Un E4 puede bajar a E3 o E2 si aparece nueva evidencia.

---

## Nivel especial: E∅ — Revocado

Una afirmación que fue E1/E2/E3 y fue falseada.

No se elimina. Se marca como E∅ con la fecha de revocación y el experimento que la rompió.

**Ejemplo hipotético:** "Las 5 capas son necesarias. [E2 → E∅ 2026-08-15] — El experimento Restaurante mostró que 3 capas bastan para servicios físicos."

---

## La pregunta fundacional

### P000 — Criterio de falsabilidad

> **¿Qué tendría que ocurrir para demostrar que LPA es falsa?**

Mientras esta pregunta no tenga respuesta, no sabemos qué significa "validar LPA".

**Estado actual:** Sin respuesta. Esta es la primera pregunta que el programa de investigación debe responder.

Posibles criterios candidatos (ninguno verificado):

- Si las 5 capas colapsan a 3 o menos en más del 50% de los experimentos, la estructura de capas no es universal.
- Si un dominio radicalmente distinto produce resultados consistentes sin trazabilidad documental, la trazabilidad no es necesaria.
- Si 3+ leyes se rompen con buena UX en dominios de necesidad (médico, finanzas), LPA es específico de productos de disfrute.

---

## Categorías de dominios para experimentos

Para que un experimento cuente como "radicalmente distinto", debe pertenecer a una categoría diferente:

| Categoría | Ejemplos | Propósito de testeo |
|---|---|---|
| **A — Colección personal** | Perfumes, libros, vinos, discos | Origen de LPA. No añade evidencia nueva. |
| **B — Necesidad** | Gestor médico, finanzas personales, trámites | Testea emociones, tono, urgencia. |
| **C — Alta densidad** | Trading, monitorización, control industrial | Testea Silencio, Umbral, Respiración. |
| **D — Progreso** | Educación, habilidades, fitness | Testea "colección" vs "progreso". |
| **E — Servicio físico** | Restaurante, museo, hospital | Testea si LPA funciona sin software. |
| **F — Organización** | Empresa, laboratorio, ayuntamiento | Testea si LPA aplica a estructuras humanas. |
| **G — Narrativa** | Libro, curso, exposición | Testea si LPA aplica a objetos sin estado. |

---

## Estructura del programa de investigación

```
lpa/
├── EPISTEMOLOGY.md              ← Este documento
├── KNOWN.md                     ← Afirmaciones con nivel de evidencia asignado
├── HYPOTHESIS.md                ← Hipótesis activas, pendientes de verificación
├── UNKNOWN.md                   ← Preguntas sin respuesta (P001, P002...)
├── experiments/
│   ├── perfume-ia/              ← Experimento 001
│   ├── biblioteca-personal/     ← Experimento 002
│   └── TEMPLATE.md              ← Plantilla para nuevos experimentos
├── artifacts/
│   ├── STRESS_TEST.md           ← Del experimento Perfume IA (existente)
│   ├── CROSS_DOMAIN_AUDIT.md    ← Del experimento Biblioteca (existente)
│   ├── FALSIFICATION_AUDIT.md   ← Del experimento Perfume IA (existente)
│   └── MATURITY_MODEL.md        ← Marco de madurez (existente)
└── CHANGELOG.md                 ← Registro de cambios en niveles de evidencia
```

---

## Reglas del programa de investigación

1. **Ninguna afirmación sin nivel.** Todo lo que se afirme sobre LPA debe tener un nivel E0-E4 asignado.

2. **Los niveles pueden bajar.** Nueva evidencia puede degradar una afirmación. No es un fracaso — es refinamiento.

3. **Un experimento no confirma. Intenta falsear.** Cada experimento debe diseñarse para ROMPER una afirmación, no para confirmarla.

4. **La falsificación exitosa es un resultado valioso.** Si un experimento rompe una afirmación E2, no es un fallo del experimento — es un avance del conocimiento.

5. **Las afirmaciones revocadas no se eliminan.** Se marcan como E∅ con trazabilidad de cuándo y por qué.

6. **El core solo crece por evidencia, no por acumulación.** Un documento no entra en el núcleo hasta que sus afirmaciones alcanzan E3.

7. **El programa de investigación es más importante que cualquier producto.** Perfume IA es el Experimento 001. No es el centro.

---

## Preguntas abiertas iniciales

Estas preguntas no tienen respuesta. Son el punto de partida del programa.

| ID | Pregunta | Estado |
|----|----------|--------|
| P000 | ¿Qué tendría que ocurrir para demostrar que LPA es falsa? | Abierta |
| P001 | ¿Qué tipo de cosa es LPA? (metodología, lenguaje, marco, teoría, disciplina?) | Abierta |
| P002 | ¿Cuál es la unidad mínima de LPA? (decisión, concepto, axioma?) | Abierta |
| P003 | ¿Puede existir LPA sin documentos? | Abierta |
| P004 | ¿Las 5 capas son necesarias o contingentes? | Abierta |
| P005 | ¿Por qué emergen siempre 5 capas? ¿Es casualidad? | Abierta |
| P006 | ¿Puede una IA aplicar LPA sin conocer LPA? | Abierta |
| P007 | ¿Puede una persona aplicar LPA intuitivamente? | Abierta |
| P008 | ¿LPA describe cómo se construye o cómo se preserva algo? | Abierta |
| P009 | ¿LPA prescribe (debes hacer) o describe (cuando funciona, ocurre esto)? | Abierta |

---

## Estado actual del conocimiento (resumen)

### Afirmaciones con nivel asignado

*Pendiente de auditoría completa. Esto es una primera pasada.*

| Afirmación | Nivel actual | Experimentos |
|------------|-------------|-------------|
| "La estructura de capas organiza el conocimiento del producto" | E1 | Perfume IA, Biblioteca |
| "Las 12 leyes de percepción son verificables" | E1 | Perfume IA |
| "Los 10 órganos funcionales son universales" | E1 | Perfume IA, Biblioteca |
| "Las 5 cadenas fisiológicas describen patrones de interacción" | E1 | Perfume IA |
| "La trazabilidad documental reduce la deriva del producto" | E1 | Perfume IA |
| "El código es la última capa" | E2 | Perfume IA, Biblioteca |
| "La ausencia comunica" | E2 | Perfume IA, Biblioteca |
| "3 de las 12 leyes se rompen con buena UX en contextos específicos" | E3 | Perfume IA (Falsification Audit) |
| "ANATOMY no es necesaria para 1 pantalla, sí para consistencia" | E3 | Perfume IA (Falsification Audit) |
| "La IA no es un órgano universal" | E2 | Stress-test |
| "EXPERIENCE_OS es ~60% universal, ~40% extensión de dominio" | E2 | Stress-test, Cross-domain |

---

## Cómo usar este documento

Al hacer cualquier afirmación sobre LPA:

1. Asignar un nivel E0-E4.
2. Citar los experimentos que lo respaldan.
3. Si no hay experimentos, es E0 como máximo.
4. Si es una hipótesis sin evidencia, va a HYPOTHESIS.md, no a KNOWN.md.

Al diseñar un experimento:

1. Especificar qué afirmación(es) intenta falsear.
2. Elegir una categoría de dominio distinta a las ya testeadas.
3. Documentar el resultado: ¿la afirmación sobrevive, se debilita o se rompe?
4. Actualizar el nivel en KNOWN.md.

---

FIN DEL DOCUMENTO EPISTEMOLOGY.md
