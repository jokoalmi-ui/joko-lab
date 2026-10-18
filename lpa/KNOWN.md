---
type: lpa
subtype: lpa
status: active
tags: [lpa]
created: 2026-07-19
---
# LPA KNOWN — Afirmaciones con nivel de evidencia asignado

Este documento lista afirmaciones sobre LPA que tienen evidencia. No contiene hipótesis ni preguntas. Cada entrada tiene su nivel E0-E4 y los experimentos que la respaldan.

**Regla:** Si una afirmación no está aquí, no puede usarse para justificar decisiones estructurales sobre LPA.

---

## Nivel E4 — Principios

*Ninguno todavía. LPA no tiene la madurez suficiente para afirmar principios E4.*

---

## Nivel E3 — Validación

### E3-001: ANATOMY no es necesaria para una pantalla, pero sí para consistencia cross-pantalla

- **Experimentos:** Perfume IA (Falsification Audit)
- **Qué se intentó:** Construir la ficha de perfume sin ANATOMY, solo con EXPERIENCE_OS + LAWS + VISUAL_LANGUAGE
- **Resultado:** La pantalla salió consistente, pero sin vocabulario compartido ni reglas de composición. Para una pantalla aislada, ANATOMY sobra. Para consistencia entre múltiples pantallas, es necesaria.
- **Última revisión:** 2026-07-18

### E3-002: Al menos 3 de las 12 leyes no son universales

- **Experimentos:** Perfume IA (Falsification Audit)
- **Qué se intentó:** Violar leyes produciendo buena UX
- **Resultado:** Ley 03 (Silencio) violada con dashboards de trading. Ley 11 (Umbral) violada con Settings estándar. Ley 06 (Gravedad Emocional) violada con timelines narrativos.
- **Implicación:** LPA no es un conjunto de leyes inviolables. Es un sistema que reduce variabilidad sin eliminarla.
- **Última revisión:** 2026-07-18

---

## Nivel E2 — Hipótesis

### E2-001: "El código es la última capa"

- **Experimentos:** Perfume IA, Biblioteca
- **Explicación:** El producto no nace del código. Las decisiones de significado preceden a las de implementación. Si la aplicación se reescribe en otra tecnología, el producto sobrevive si conserva su identidad en las capas superiores.
- **Intentos de falsificación:** Ninguno formal. No se ha testeado en un producto donde el código SÍ sea la primera capa (ej: un videojuego donde la mecánica es el significado).

### E2-002: "La ausencia comunica"

- **Experimentos:** Perfume IA, Biblioteca
- **Explicación:** Cuando un dato no existe, el producto debe comunicar potencial ("aún no has añadido notas") en lugar de carencia ("no hay datos"). Pero el stress-test sugiere que esto falla en dominios de necesidad (médico).
- **Intentos de falsificación:** Stress-test sugiere ruptura en dominio médico. No verificado con prototipo real.

### E2-003: "La IA no es un órgano universal de LPA"

- **Experimentos:** Stress-test Perfume IA
- **Explicación:** En el stress-test contra dominio médico, la IA resultó innecesaria en varios productos (calculadora, editor markdown). La IA debería ser una capacidad transversal opcional, no un órgano fijo.
- **Intentos de falsificación:** No se ha testeado si hay productos donde la IA SÍ es estructuralmente necesaria.

### E2-004: "EXPERIENCE_OS es ~60% universal, ~40% extensión de dominio"

- **Experimentos:** Stress-test, Cross-domain audit
- **Explicación:** Las secciones 02 (Arquitectura Emocional) y 06 (Voz) contienen valores concretos que no sobreviven al dominio médico. El resto (principios, tiempo, presencia, ritmo, etc.) es universal.
- **Intentos de falsificación:** Pendiente prototipo real en dominio médico.

---

## Nivel E1 — Patrón

### E1-001: Las 5 capas emergen al organizar documentación de producto

- **Experimentos:** Perfume IA, Biblioteca
- **Observación:** En ambos casos, al organizar documentos sobre un producto, emergieron 5 niveles: significado (producto), reglas (governance), percepción (experience), ejecución (implementation), aprendizaje (runtime).
- **No sabemos:** Si esto es necesario (siempre ocurre) o contingente (ocurrió en estos dos casos por su naturaleza).

### E1-002: Las 12 leyes de percepción son verificables en dominios de colección

- **Experimentos:** Perfume IA
- **Observación:** Las 12 leyes pudieron verificarse contra la ficha de perfume. Cada ley produjo una decisión de diseño concreta.
- **No sabemos:** Si sobreviven a dominios que no son de colección.

### E1-003: Los 10 órganos funcionales son reutilizables en dominios de colección

- **Experimentos:** Perfume IA, Biblioteca
- **Observación:** Los 10 órganos (Hero, Identidad, Contexto, etc.) se mapearon directamente a fichas de libros sin cambiar su definición.
- **No sabemos:** Si sobreviven a dominios sin "objetos con ficha" (médico, finanzas).

### E1-004: La trazabilidad documental reduce la deriva del producto

- **Experimentos:** Perfume IA
- **Observación:** Cuando se construyó REFERENCE_SCREEN con 39 referencias a documentos fuente, las decisiones de diseño no improvisadas fueron 0.
- **No sabemos:** Si esto se mantiene en productos con equipos grandes o múltiples diseñadores.

### E1-005: Las 5 cadenas fisiológicas describen patrones de interacción genéricos

- **Experimentos:** Perfume IA
- **Observación:** Las cadenas (Registrar, IA→Descubrimiento, Retorno, Nota, Sin Datos) describen flujos que aparecen en cualquier producto con objetos persistentes.
- **No sabemos:** Si aparecen en productos sin objetos persistentes.

### E1-006: Los conceptos emergen por necesidad, no por diseño

- **Experimentos:** Perfume IA
- **Observación:** STATES, METABOLISM y AXIOMS aparecieron como gaps detectados durante la construcción de pantallas. No fueron diseñados a priori. Esto sugiere que LPA tiene un mecanismo de auto-descubrimiento.
- **No sabemos:** Si este mecanismo funciona en otros dominios o es específico de Perfume IA.

### E1-007: Un instrumento sin disparador no se usa: el que depende de que alguien se acuerde se degrada

- **Experimentos:** joko-lab (Experimento 004)
- **Origen:** CP-009 (`pattern-incubator/CP-009-instrumento-sin-forzado-se-degrada.md`) → E1 en la revisión mensual del **2026-10-02**.
- **Observación:** 9 ocurrencias medidas en disco, en 7 dominios distintos del lab, todas con el mismo mecanismo: el instrumento existe, funciona cuando alguien lo dispara, y nadie lo dispara. Casos: `lecciones_ledger.jsonl` congelado 7 días (mtime 2026-09-25) y `retrabajo_ledger.jsonl` con 1 entrada el mismo día; `lpa/incidentes/*-incidentes.md` (único fichero del 01-09 → **31 días sin escrituras**) frente a `~/.hermes/cron/executions.db`, que registró **13 incidencias** en ese mismo periodo; dos bloques `[truncated]` en skills sin reparar desde el 24-09 (**3 semanas**, D8 del acta 25-09); `resumen-dia` parado en el 29-09; el scan del Experimento 002 perdido el 01-10 sin anotarse en el `retrabajo_ledger`.
- **No sabemos:** si un instrumento con disparador automático + dueño declarado deja de degradarse. **Limitación declarada:** las 9 ocurrencias son del mismo experimento (joko-lab) → E1 «patrón observado»; no habilita reglas estructurales hasta tener un segundo experimento.
- **Falsación (citada de CP-009, 2026-10-02):** «Sería **FALSO** si, medido sobre **N=10 instrumentos nuevos** del lab (ledger/registro/ciclo creados sin disparador automático ni comprobación periódica) durante **2 ciclos consecutivos**, al menos 8 de ellos acumulan registros reales en su primer periodo de uso **sin** que nadie los verifique ni los dispare desde fuera.»
- **Última revisión:** 2026-10-02

### E1-008: Un instrumento no validado miente en silencio

- **Experimentos:** joko-lab (Experimento 004)
- **Origen:** CP-010 (`pattern-incubator/CP-010-instrumento-no-validado-miente.md`) → E1 en la revisión mensual del **2026-10-02**.
- **Observación:** 6 ocurrencias en 4 dominios (copias a disco, salud del conocimiento, transcripción por VLM y gobernanza), el último **sostenido 8 días**: `hermes curator status` devuelve `PAUSED` / `last run: 8d ago` mientras `.curator_ledger.jsonl` acumula **703 operaciones** con fecha ≥ 2026-09-25 (171/80/74/57/90/112/83/36; última 2026-10-02T12:16:38Z). El número que se lee para decidir no coincide con la actividad real, y nadie lo había contrastado.
- **No sabemos:** qué instrumentos del lab devuelven una cifra correcta **sin** haber sido validados, ni si la validación puntual caduca. **Limitación declarada:** todas las ocurrencias son del Experimento 004 → E1 «patrón observado».
- **Falsación (citada de CP-010, 2026-10-02):** «Sería **FALSO** si, sobre **N=10 instrumentos** del lab usados para decidir durante **2 ciclos LPA consecutivos**, comparados contra su patrón oro, **al menos 9** devuelven la cifra correcta (dentro de la tolerancia declarada) **sin** validación previa ni etiqueta de validez.»
- **Última revisión:** 2026-10-02

---

## Nivel E0 — Observación

### E0-001: EMERGENT_CONCEPTS.md captura conceptos antes de formalizarlos

- **Experimento:** Perfume IA
- **Observación:** STATES.md se escribió tras 3 gaps en una pantalla. Fue rebajado a EMERGENT_CONCEPTS.md. El patrón de "tracking de candidatos" funcionó.

### E0-002: IE (Índice de Emergencia) mide convergencia de la metodología

- **Experimento:** Perfume IA
- **Observación:** IE = decisiones nuevas / decisiones totales. Tres casos: 16.7% → 17.6% → 0%. Tendencia a 0% sugiere convergencia.
- **No sabemos:** Si IE funciona como métrica en otros dominios.

### E0-003: Creative References ≠ Design Rules

- **Experimento:** Perfume IA
- **Observación:** Las referencias de dirección artística no son reglas de diseño. Tratarlas como reglas crea un nuevo "Bootstrap". Dos diseñadores con las mismas referencias pueden llegar a soluciones distintas, ambas válidas.

---

## Afirmaciones revocadas (E∅)

*Ninguna todavía.*

---

## Resumen estadístico

| Nivel | Cantidad |
|-------|----------|
| E4 — Principio | 0 |
| E3 — Validación | 2 |
| E2 — Hipótesis | 4 |
| E1 — Patrón | 8 |
| E0 — Observación | 3 |
| E∅ — Revocado | 0 |

---

FIN DEL DOCUMENTO KNOWN.md
