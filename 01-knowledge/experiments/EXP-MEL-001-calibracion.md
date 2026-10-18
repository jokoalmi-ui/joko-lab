---
title: "EXP-MEL-001 — Estudio de calibración del proceso de decisión"
type: EXP
---

# EXP-MEL-001 — Estudio de calibración del proceso de decisión

**Estado:** COMPLETADO (fase 1, observacional, solo lectura) — 2026-08-04
**Tipo:** EXP-MEL-001 (primer experimento de la capa MEL)
**Método:** Observacional sobre datos históricos reales. No intervino en el sistema.

## Hipótesis

> **H1:** La confianza registrada contiene información predictiva sobre la
> fiabilidad futura de una decisión.

## Método

- Fuentes: 17 Knowledge Objects (`01-knowledge/objects/`, excluido template),
  evidencia de `evidence`/`history`, y registros de reapertura en el lab.
- Variables: `confidence_label`, `evidence_level` (evidencia real citada),
  `reopened` (KVC), `superseded_by`, `age_days` (desde created a 2026-08-04),
  `decision_origin` (inferido de evidence/history).
- No se fijó ningún umbral.

## Datos (corte 2026-08-04)

| ID | TIPO | STATUS | CONF_LABEL | AGE | SUPERSEDED | ORIGEN (inferido) |
|---|---|---|---|---|---|---|
| DEC-001 | DEC | activo | NO_EVALUADA | 9 | - | experimento (EXP-20260726-001) |
| DEC-002 | DEC | activo | NO_EVALUADA | 7 | - | experimento (EXP-20260728-003) |
| DEC-003 | DEC | activo | ALTA | 6 | - | experimento (EXP-20260729-004 + 3 validaciones) |
| DEC-GAIPRO-001 | DEC | active | MEDIA | 1 | - | auditoría (verificación directa web) |
| POLICY-001 | POLICY | activo | NO_EVALUADA | 4 | - | revisión de diseño |
| POLICY-002 | POLICY | activo | NO_EVALUADA | 4 | - | revisión de diseño |
| POLICY-003 | POLICY | activo | NO_EVALUADA | 0 | - | revisión de diseño |
| PRED-001 | PRED | pendiente | SIN_LABEL | 0 | - | - |
| PRED-002 | PRED | pendiente | SIN_LABEL | 0 | - | - |
| RULE-001 | RULE | activo | ALTA | 6 | - | herencia (DEC-003) |
| RULE-002 | RULE | activo | ALTA | 7 | - | herencia (DEC-002) |
| RULE-003 | RULE | activo | ALTA | 6 | - | herencia (DEC-002) |
| RULE-004 | RULE | activo | ALTA | 6 | - | herencia (DEC-001) |
| RULE-005 | RULE | activo | ALTA | 3 | - | norma (JL-013) |
| RULE-006 | RULE | draft | BAJA | 1 | - | vídeo (RDD) |
| RULE-007 | RULE | activo | ALTA | 1 | - | norma (JL-014) |
| RULE-008 | RULE | activo | ALTA | 0 | - | incidente/verificación |

## Hallazgos

**F1 — H1 no es falsable hoy (resultado esperado de un KEL joven).**
Edad máxima 9 días, 0 KOs con `superseded_by`, 0 reaperturas registradas
(búsqueda de reabiert|reopened|reapertura: solo menciones conceptuales en
GUIA/CP-003, ningún evento real). La dimensión temporal que H1 necesita
(confianza → resultado futuro) aún no tiene datos.

**F2 — Patrón de proceso utilizable: la confianza no se actualiza con la evidencia.**
DEC-001 y DEC-002 tienen experimento asociado (EXP-20260726-001,
EXP-20260728-003) y siguen en `NO_EVALUADA`. El label se asigna al crear,
no al validar. Transición accionable: al registrar evidencia nueva, re-evaluar
`confidence_label` (primera aplicación práctica de RULE-MEL-001).

**F3 — Consistencia interna estado/label (patrón débil pero coherente).**
activo→ALTA, draft→BAJA, pendiente→SIN_LABEL. Las 7 RULE activas tienen
ALTA y todas tienen origen (norma/herencia/incidente). El único draft
(RULE-006) tiene BAJA. El etiquetado actual es internamente consistente.

**F4 — `decision_origin` no está registrado; solo inferible.**
Se deduce de evidence/history (experimento, norma, vídeo, auditoría,
incidente, herencia). Sin campo explícito no se podrá medir "las DEC de
vídeos se reabren un X%" de forma fiable. Acción: añadir el campo.

**F5 — Dimensión Evolución sin datos todavía.**
0 `superseded_by` en todo el corpus → plasticidad (tiempo DEC→superseded,
DEC→pruning) no medible hasta que el KEL complete ciclos reales.

## Caso de estudio: VERIFIER (separado de las DEC)

No es un fallo de conocimiento: es un fallo del proceso de verificación
(falso negativo sistemático del detector, TD-001). El proceso lo detectó y
generó RULE-008 con evidencia de verificación real (backup .bak-* verificado
con find/ls, 04-ago). Evidencia persistente: /tmp/hermes-verify-*.log
(NO re-ejecutar: bloqueo documentado).

Lectura: el lab SÍ detecta sus propios errores de proceso, pero la detección
fue manual/ad-hoc (Joseba/Hermes), no sistemática. Eso es exactamente el
hueco que MEL cubre: convertir la detección de errores del proceso en
métrica continua, no en episodio.

## Conclusión (criterio de éxito no binario)

- **Éxito parcial:** aparece al menos un patrón estable utilizable para
  mejorar el proceso (F2: incoherencia label/evidencia) y un caso real de
  metacognición (VERIFIER → RULE-008).
- **H1 SIN DECIDIR:** ni confirmada ni falsada. La muestra es demasiado joven
  (edad ≤9 días, sin reaperturas ni obsolescencia). No es resultado negativo:
  las métricas discriminan (F3), pero la dimensión temporal aún no existe.
- Conclusión operativa: MEL no queda validada ni descartada; queda con una
  primera señal accionable y un plazo de re-medición.

## Limitaciones

- n=17, edad máxima 9 días.
- `decision_origin` inferido, no registrado.
- Sin reaperturas/superseded en el periodo.
- El grep de reaperturas buscó términos concretos; puede haber trazas con
  otra terminología.

## Acciones derivadas (transiciones, sin umbrales)

- A1: ✅ EJECUTADA 2026-08-04 — `confidence_label` de DEC-001 y DEC-002
  re-evaluado a MEDIA (ambos tienen EXP asociado) + campo `label_updated`.
  Primer test real de RULE-MEL-001: métrica (label incoherente con evidencia)
  → transición (re-etiquetar). Backups: objects/*.bak-20260804.
- A2: ✅ EJECUTADA 2026-08-04 — campo `decision_origin` añadido a los 17 KOs
  (valores: experimento, auditoria, revision, herencia, norma, video,
  incidente, desconocido). Backups: objects/*.bak-20260804.
- A3: ✅ CONVENCIÓN REGISTRADA — reaperturas se registrarán como evento
  explícito `reopened` en `history` del KO (hoy no hay ninguna: el grep de
  reabiert|reopened|reapertura solo encuentra menciones conceptuales).

## Próximo ciclo

EXP-MEL-002 tras 30-60 días de operación: re-medir con reaperturas y
superseded reales → H1 falsable. Medir plasticidad (OBS→DEC, DEC→superseded)
cuando existan datos longitudinales.
