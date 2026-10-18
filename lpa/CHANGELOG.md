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

FIN DEL CHANGELOG
