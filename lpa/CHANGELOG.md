---
type: lpa
subtype: lpa
status: active
tags: [lpa]
created: 2026-07-19
---
# LPA Changelog

Registro de cambios en los niveles de evidencia de las afirmaciones sobre LPA.

---

## 2026-07-19 — Fundación del programa de investigación

### Creados

- `EPISTEMOLOGY.md` — Sistema de niveles E0-E4, criterio de falsabilidad P000, estructura del programa.
- `KNOWN.md` — 15 afirmaciones con nivel de evidencia asignado (0 E4, 2 E3, 4 E2, 6 E1, 3 E0).
- `HYPOTHESIS.md` — 8 hipótesis activas no verificadas.
- `UNKNOWN.md` — 20 preguntas sin respuesta.
- `experiments/TEMPLATE.md` — Plantilla para futuros experimentos.

### Movidos (conceptual)

- Perfume IA pasa de ser "el proyecto" a ser "Experimento 001".
- Biblioteca Personal pasa de ser "validación cross-domain" a ser "Experimento 002 (parcial, sin prototipo)".

### Niveles asignados (primera pasada)

Ver `KNOWN.md` para la asignación completa. Esta primera pasada es provisional — todas las afirmaciones deben ser re-auditadas contra los criterios formales de EPISTEMOLOGY.md.

### Pendiente

- Re-auditar cada afirmación en KNOWN.md contra los criterios exactos de EPISTEMOLOGY.md.
- Responder P000 (criterio de falsabilidad) antes de diseñar el próximo experimento.
- Crear `experiments/perfume-ia/` con el registro formal del Experimento 001.
- Migrar artifacts/ desde experience/ (STRESS_TEST, CROSS_DOMAIN_AUDIT, etc.).

---

## 2026-10-02 — Revisión mensual del incubator (ciclo semanal LPA)

### Añadidos

- `KNOWN.md` **E1-007**: «Un instrumento sin disparador no se usa: el que depende de que alguien se acuerde se degrada» — ascenso de **CP-009** con 9 ocurrencias / 7 dominios (joko-lab). Falsación citada de CP-009.
- `KNOWN.md` **E1-008**: «Un instrumento no validado miente en silencio» — ascenso de **CP-010** con 6 ocurrencias / 4 dominios, el último sostenido 8 días (`curator status: PAUSED` frente a 703 operaciones reales). Falsación citada de CP-010.

### Niveles actualizados

- E1 pasa de 6 a 8 afirmaciones (total del documento: 17).

### Limitación declarada en los ascensos

- Los dos ascensos se apoyan **solo** en el Experimento 004 (joko-lab): se asignan como **E1 «patrón observado»** y **no habilitan reglas estructurales** hasta que exista un segundo experimento. Las condiciones de falsación quedan copiadas en `KNOWN.md` para poder caer.

### Sin cambios

- `CP-008` (12→13 ocurrencias), `CP-011` (2 ocurrencias + 1 reforzada) y `CP-001`…`CP-007` siguen en incubación. **Ninguna fusión y ningún descarte** en esta revisión (antídotos distintos: muestreo periódico / etiqueta de validez / comprobación de tamaño y cola).
- `HYPOTHESIS.md` y `UNKNOWN.md` sin cambios.

### Nuevo candidato

- `pattern-incubator/CP-012-estado-unknown-se-resuelve-en-el-artefacto.md` — 5 ejecuciones `unknown` en 5 jobs distintos (01-10).

### Contexto

- Acta: `incidentes/revision-fallos-2026-10-02.md` (decisiones D0..D12). Ventana: 2026-09-25 → 2026-10-02. Backups RULE-008 `.bak-20261002` de los ficheros tocados.

---

## 2026-11-06 — Revisión MENSUAL del incubator (primer ciclo mensual; deuda del 02-11 cerrada)

Ejecutada el 2026-11-06 17:40 CET (nominal 02-11 13:30, catch-up de 4 días; el job `b2c498369692` existía sin ejecuciones previas). Acta: `incidentes/revision-mensual-2026-11.md`.

### Añadidos

- `KNOWN.md` **E1-009**: «El estado documentado diverge del estado real, y la divergencia no se detecta sin muestreo» — ascenso de **CP-008** con 13 ocurrencias en 8+ dominios y 3 fechas (02-09, 18-09, 25-09). Falsación citada de CP-008.
- `KNOWN.md` **E1-010**: «El estado `unknown` no se resuelve en el motor: se resuelve en el artefacto» — ascenso de **CP-012** con 5 ocurrencias en 5 jobs y 3 reexámenes sin disparo (09-10, 16-10 con OOM real, 20-10). Falsación citada de CP-012.
- `KNOWN.md` **E1-011**: «`resolved` mide la corrida siguiente, no la reparación» — ascenso de **CP-017** con 3 ocurrencias en 2 jobs y 2 contraejemplos declarados. Falsación citada de CP-017.

### Niveles actualizados

- E1 pasa de 8 a **11** afirmaciones (total del documento: **20**).

### Limitación declarada en los ascensos

- Los tres se apoyan **solo** en el Experimento 004 (joko-lab) o en un único registro (`cron_incidents`) → **E1 «patrón observado»**, sin reglas estructurales hasta el segundo experimento. Las condiciones de falsación quedan copiadas para poder caer.

### Sin cambios (15 fichas mantenidas, ninguna fusión, ningún descarte)

- **CP-001, CP-002, CP-003, CP-00X**: nunca reexaminados desde julio (revisión 2026-08-01 sin ejecutar); **tope 2026-12-02**, y CP-00X a renumerar como CP-020.
- **CP-004, CP-005**: su propia condición de ascenso no se cumple (2+ dominios / >20 DECs con conflictos).
- **CP-006, CP-007**: 3 ocurrencias cada uno, pero todas en un mismo día (24 h) → contextos distintos, no ocasiones distintas. **Tope 2026-12-02**.
- **CP-011**: 2 ocurrencias pero sin denominador (hueco de instrumento).
- **CP-013, CP-014, CP-015**: un solo host / un solo evento raíz / un solo vigía.
- **CP-016**: antídoto aplicado y 0 reinicios en 7 días, pero su falsación pide 10 noches y los artefactos del vigilante retienen ~21 h.
- **CP-018**: un solo registro; el antídoto exige tocar el núcleo de Hermes (RULE-016).
- **CP-019** (creado hoy): 9 noches de fallo de entrega, causa raíz no asignada.

### Contexto de instrumentos (medido)

- `executions`: 1.001 filas, 2026-11-05T16:15 → 2026-11-06T17:55 (**~1 día**). Artefactos del vigilante `264c02dae003`: 50 ficheros, 05-11 20:57 → 06-11 17:55 (**~21 h**). Ninguna revisión puede reconstruir el mes con esas dos fuentes.
- Deudas: cerrada la verificación de B (`rag-reindex`, 0 `timed out` posteriores al 16-10 en 50 artefactos) y D (CP-016). Vencidas: revisión mensual del 02-11 (se cierra con esta acta), asiento del `retrabajo_ledger` (llegó el 03-11 07:39, 7 h 40 min tarde) y el vigía de informes (sigue sin leer la cabecera declarativa).

### Backups

- RULE-008 `.bak-20261106` de `KNOWN.md`, `CHANGELOG.md`, `CP-008`, `CP-012` y `CP-017`. Sin commit.

---

FIN DEL CHANGELOG
