---
type: lpa
subtype: pattern
status: incubating
tags: [lpa, pattern]
created: 2026-09-02
---
# CP-006: Verification by Evidence, not by Declaration

**ID:** CP-006
**Fecha:** 2026-09-02
**Estado:** E0 — Candidate Pattern
**Origen:** Revisión de fallos 2026-09-01 (INC-001/A1, INC-005-B1, A4) — primera promoción del ciclo LPA reactivado (D0)

---

## 1. Qué ocurrió

El 01-09 tres fallos en dominios distintos compartieron el mismo error de fondo: se aceptó una DECLARACIÓN de éxito como si fuera EVIDENCIA.

- **Render de carrusel (INC-001/A1):** el pipeline dio por "verificada" una salida cuando el PNG era la página de error de Chrome (33 KB, `file://` relativa → ERR_INVALID_URL). El comando había "salido bien"; nadie miró el artefacto.
- **Subagente local (B1):** un nodo investigador auto-reportó ÉXITO ("archivo creado") cuando `/tmp/graph_piloto1/investigacion.json` NO existía en disco.
- **Detector de outliers (A4):** el detector declaraba outlier a casi TODOS los vídeos de canales pequeños sanos porque la condición ("views > suscriptores") no estaba calibrada contra la distribución real.

Además, al descubrirse el bug del carrusel, se extrapoló a la F1 del 20-ago ("también era error") SIN verificarla — inferencia no verificada que resultó FALSA (la F1 era correcta: 53-82 KB, perfil de píxeles beige, GLM confirmó contenido real).

## 2. Evidencia que lo respalda

- 3 ocurrencias en 24 h en dominios distintos (render visual, delegación, detección/métricas).
- Regla ya vigente en el lab: "no concluir que algo está caído sin salida real" (filosofía Hermes/sistema) y "no concluir que un servicio falla si el comando falló por otra causa".
- Backlog 2026-07-31, entradas 1487-1548 (registro del día).

## 3. Contradicciones o limitaciones

- Comprobar evidencia cuesta tiempo; no toda tarea tiene evidencia objetiva disponible (criterio subjetivo: estilo, redacción).
- Riesgo opuesto: sobre-verificación/parálisis en tareas triviales.
- No define QUÉ evidencia es suficiente en cada dominio — depende del tipo de tarea (tamaño/píxeles para renders, archivo en disco para escrituras, distribución real para umbrales).

## 4. Principio que parece emerger

> La verificación debe comprobar la EVIDENCIA objetiva del artefacto (tamaño, píxeles, archivo en disco, salida real, distribución de datos), NO la declaración de éxito del proceso que lo produjo. Y un fallo detectado en una salida NO se extrapola a otras salidas sin verificarlas una a una.

## 5. ¿En qué otros proyectos podría aplicarse?

- Todo pipeline con verificación visual (infografías, carruseles, renders).
- Delegación a subagentes: los self-reports no son verificables; el estado debe ir a un archivo/SQLite auditado.
- Detectores con umbrales (outliers, watchdogs): calibrar contra datos reales antes de emitir alertas.
- Despliegues para clientes (entregar solo lo verificado por evidencia).

## 6. ¿Qué tendría que ocurrir para demostrar que este patrón es falso?

Sería FALSO si: una verificación por declaración (sin mirar evidencia) detecta el mismo porcentaje de fallos reales que una verificación por evidencia, medido sobre N=20 casos con fallos inyectados en al menos 3 dominios.

## 7. Decisión

Incubar (E0). Primera revisión en la revisión periódica del ciclo LPA (mensual).

- [ ] Asciende a KNOWN.md como E1
- [ ] Asciende a procedures/ como procedimiento LPA
- [ ] Sigue en incubación (falta evidencia)
- [ ] Se descarta (no sobrevive a otro dominio / fue falseado)
- [ ] Se fusiona con otro patrón

**Fecha de revisión:** 2026-11-02 (próxima mensual)
**Última revisión:** 2026-10-02 — sin evidencia nueva en la ventana 25-09→02-10; sigue incubando (D10 del acta `revision-fallos-2026-10-02.md`).
**Justificación:** 3 ocurrencias en 24 h + regla previa del lab; requiere validación en más dominios y definir evidencia mínima por tipo de tarea.
