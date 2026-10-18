---
type: lpa
subtype: pattern
status: incubating
tags: [lpa, pattern]
created: 2026-09-02
---
# CP-007: Audit before Acting (Paso 0)

**ID:** CP-007
**Fecha:** 2026-09-02
**Estado:** E0 — Candidate Pattern
**Origen:** Revisión de fallos 2026-09-01 (B2, B3/INC-004, B4) — primera promoción del ciclo LPA reactivado (D0)

---

## 1. Qué ocurrió

El 01-09 tres fallos de proceso por producir o analizar sin auditar primero el estado real:

- **Análisis de vídeo Emowe (B2):** se analizó una herramienta externa (kanban) sin comprobar que el lab YA tenía kanban nativo integrado (kanban.db desde 21-jul, VACÍO — nunca usado).
- **Piloto de infografía (B3/INC-004):** se produjo un piloto 16:9 SIN pedir referencia visual; el usuario lo rechazó ("los mismos cuadros con texto de antes"). Faltó auditar los requisitos de composición antes de montar nada.
- **max_tokens GLM (B4):** se usó el valor por defecto cuando estaba documentado usar SIEMPRE max_tokens=4000 (backlog 26-ago + 3 skills). Lección YA documentada que se ignoró — no se consultó la skill antes de actuar.

La regla "Paso 0: consultar skill + backlog 48h antes de actuar" existía desde 26-ago; los fallos muestran que el patrón es más general: auditar el estado real (skills, capacidades del lab, requisitos, referencias) antes de cualquier producción con salida visible.

## 2. Evidencia que lo respalda

- 3 ocurrencias en 24 h, dos de ellas correcciones explícitas del USUARIO (B2, B3).
- Regla Paso 0 vigente en el lab (26-ago) + INC-004 lección integrada en skill infographic-production F1: "si existe referencia posible, PEDIRLA antes de producir".

## 3. Contradicciones o limitaciones

- Auditar TODO antes de TODO puede volverse burocracia; hay tareas triviales donde el coste de auditar supera al beneficio.
- Falta definir cuándo el Paso 0 es obligatorio (salidas visibles/reutilizables: infografías, análisis publicados, código, veredictos) vs cuándo se puede obviar.
- Auditar capacidades del lab exige un mapa de capacidades mínimamente actualizado; si no existe, el propio audit falla (dependencia).

## 4. Principio que parece emerger

> Antes de producir una salida (análisis, infografía, código, veredicto), auditar: (1) qué existe ya en el lab (capacidades, kanban, herramientas propias); (2) qué documenta la skill/backlog relevante; (3) si hay referencia visual o requisitos explícitos que pedir. El coste de auditar/preguntar antes es siempre menor que el de rehacer tras una corrección.

## 5. ¿En qué otros proyectos podría aplicarse?

- Análisis de contenido externo (IG/YT/podcasts): auditar capacidades internas antes de comparar con herramientas externas.
- Producción visual (infografías, carruseles): pedir referencia antes de la primera iteración.
- Cualquier tarea con skill asociada: cargar la skill antes de actuar (regla de skills del sistema).
- Despliegues para clientes: auditar el entorno real antes de prometer soluciones.

## 6. ¿Qué tendría que ocurrir para demostrar que este patrón es falso?

Sería FALSO si: tareas de producción realizadas con Paso 0 sistemático no reducen el número de iteraciones/correcciones frente a las realizadas sin él, medido durante 4 semanas (N correcciones por tipo de tarea con y sin audit previo).

## 7. Decisión

Incubar (E0). Primera revisión en la revisión periódica del ciclo LPA (mensual).

- [ ] Asciende a KNOWN.md como E1
- [ ] Asciende a procedures/ como procedimiento LPA
- [ ] Sigue en incubación (falta evidencia)
- [ ] Se descarta (no sobrevive a otro dominio / fue falseado)
- [ ] Se fusiona con otro patrón

**Fecha de revisión:** 2026-11-02 (próxima mensual)
**Última revisión:** 2026-10-02 — sin evidencia nueva en la ventana 25-09→02-10; sigue incubando (D10 del acta `revision-fallos-2026-10-02.md`).
**Justificación:** 3 ocurrencias en 24 h con 2 correcciones de usuario; requiere definir umbral de obligatoriedad del Paso 0 y validar reducción de iteraciones.
