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

### E1-009: El estado documentado diverge del estado real, y la divergencia no se detecta sin muestreo

- **Experimentos:** joko-lab (Experimento 004)
- **Origen:** CP-008 (`pattern-incubator/CP-008-estado-real-vs-documentado.md`) → E1 en la revisión mensual del **2026-11-06** (acta `incidentes/revision-mensual-2026-11.md`).
- **Observación:** **13 ocurrencias** (12 del recuento original de la ficha + 1 en la ventana 25-09→02-10) en 8+ dominios del lab, en 3 fechas distintas: 8 el **2026-09-02** (systemd, kanban, docs canónicos, salud del conocimiento, repo git, memoria, config, logs), 2 el **2026-09-18** (cadencia doc↔motor y BD↔registro) y 2 el **2026-09-25** (registro de lecciones declarado vs real; resumen del curador vs su ledger de 703 operaciones), más 4 correcciones ya anotadas en el backlog. En todos los casos el documento afirmaba un estado que la fuente desmentía, y la divergencia solo apareció al muestrear: nadie la había detectado leyendo el documento.
- **No sabemos:** con qué frecuencia la divergencia es inocua frente a la que induce una acción incorrecta; ni si un muestreo periódico doc↔fuente la mantiene a raya (el antídoto está propuesto, no medido). **Limitación declarada:** las 13 ocurrencias son del mismo experimento (joko-lab) → E1 «patrón observado»; no habilita reglas estructurales hasta tener un segundo experimento.
- **Falsación (citada de CP-008, 2026-11-06):** «Sería FALSO si: durante 2 ciclos LPA consecutivos (2 meses), un muestreo de 10 afirmaciones de estado extraídas de documentos del lab contra su fuente real NO encuentra ninguna divergencia relevante (que hubiera llevado a una acción incorrecta de haber actuado sobre el documento).»
- **Última revisión:** 2026-11-06

### E1-010: El estado `unknown` no se resuelve en el motor: se resuelve en el artefacto

- **Experimentos:** joko-lab (Experimento 004)
- **Origen:** CP-012 (`pattern-incubator/CP-012-estado-unknown-se-resuelve-en-el-artefacto.md`) → E1 en la revisión mensual del **2026-11-06**.
- **Observación:** 5 ocurrencias en 5 jobs distintos (**2026-10-02**) y tres reexámenes posteriores que **no dispararon la falsación**: 09-10 (dos `unknown` resueltos en las dos direcciones: producto presente y producto ausente), 16-10 (el `unknown` del consolidador tapaba un **OOM real** del worker en su cgroup de 4 GiB, no un reinicio) y 20-10 (incidencia cerrada en el mismo segundo en que apareció el producto, 79.753 B). La serie empezó con `unknown` por reinicio del planificador (incertidumbre benigna) y ganó un segundo mecanismo con el OOM.
- **No sabemos:** cuántos `unknown` quedan sin resolver porque el artefacto tarda más que la ventana de revisión; y el antídoto decide **efectos**, no **causa** (límite compartido con CP-015). **Limitación declarada:** un solo experimento (joko-lab) → E1 «patrón observado».
- **Falsación (citada de CP-012, 2026-11-06):** «Sería FALSO si, sobre N=10 ejecuciones que terminan en `unknown` en el lab y durante 2 ciclos LPA consecutivos, 8 o más se resuelven consultando únicamente el estado del motor (sin ir al artefacto) con un veredicto correcto (efectos sí / efectos no) verificado después contra el producto.»
- **Última revisión:** 2026-11-06

### E1-011: `resolved` mide la corrida siguiente, no la reparación

- **Experimentos:** joko-lab (Experimento 004)
- **Origen:** CP-017 (`pattern-incubator/CP-017-resolved-mide-la-corrida-siguiente-no-la-reparacion.md`) → E1 en la revisión mensual del **2026-11-06**.
- **Observación:** 3 ocurrencias en 2 jobs distintos y 4 fechas: dos cierres sin reparación (23-10); el historial sobrescrito de la fila `264c02_761c7f27bcb0` (leída el 13-10, el 23-10 y el 26-10 con tres estados distintos de la misma incidencia); y la reapertura del 01-11 que volvió a cerrar el 02-11 **sobrescribiendo** el `closed_at` del 28-10. Con **2 contraejemplos** declarados, cierres sí respaldados por reparación verificable: `bbc1d8` (28-10, OAuth renovado) y `da39a2` (26-10, mtime del productor + 10 salidas limpias).
- **No sabemos:** cuántas incidencias del histórico tienen `resolved` sin reparación detrás, porque la tabla no conserva ocurrencias (el borrado es parte del defecto). **Limitación declarada:** un solo registro (`cron_incidents`) → E1 «patrón observado».
- **Falsación (citada de CP-017, 2026-11-06):** «Sería FALSO si, sobre 10 incidencias cerradas del lab en 2 ciclos consecutivos, en 8 o más el cierre coincidiera con un cambio verificable en el productor (script/config con mtime posterior al `first_seen_at` y producto generado después) y el registro conservara el histórico de ocurrencias (reabrir no borra el cierre anterior). También lo falsaría que el lab no usara nunca `resolved` como prueba de reparación.»
- **Última revisión:** 2026-11-06

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
| E1 — Patrón | 11 |
| E0 — Observación | 3 |
| E∅ — Revocado | 0 |
| **Total** | **20** |

*Actualizado en la revisión mensual del 2026-11-06 (acta `incidentes/revision-mensual-2026-11.md`): E1-009 (ex CP-008), E1-010 (ex CP-012), E1-011 (ex CP-017).*

---

FIN DEL DOCUMENTO KNOWN.md
