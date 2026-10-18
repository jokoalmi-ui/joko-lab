---
title: "REVISIÓN DE FALLOS — 2026-09-14 (ciclo semanal LPA, D0/INC-005)"
type: knowledge
---

# REVISIÓN DE FALLOS — 2026-09-14 (ciclo semanal LPA)

> Ciclo semanal reactivado el 02-09-2026 (decisión D0/INC-005). Ejecutado por el cron «Ciclo semanal LPA».
> Fecha real verificada con `date`: **2026-09-14 07:14 CEST (lunes)**.
> Revisión anterior: `revision-fallos-2026-09-01.md` (D0..D5) + ciclo del 04-09 (sin promociones).
> Ventana cubierta: **02-09-2026 → 14-09-2026**.

---

## 0. Incidentes de la ventana

**No hay ningún fichero de incidentes nuevo desde el 01-09-2026.** Verificado (solo lectura):

| Comprobación | Resultado real |
|---|---|
| `ls -la lpa/incidentes/` (sin .bak) | Solo `2026-09-01-incidentes.md` (mtime 03-09 13:38), `2026-09-02-auditoria-estado-lab.md` (02-09 14:02), `revision-fallos-2026-09-01.md` (03-09 13:38) |
| `find . -iname '*-incidentes.md'` | Únicamente el del 01-09 (más copia en `.BACKUP-frontmatter-20260817`) |

→ **No se promueve nada desde incidentes nuevos: esta semana no hay FALLO/ACIERTO/DUDOSO/HIPOTESIS que leer.**
El registro diario `YYYY-MM-DD-incidentes.md` no se ha materializado ni un solo día desde el 01-09 (**12 días**).

---

## 1. Actividad de la ventana (contexto, sin interpretar)

- Sesiones/día (`04-operations/metrics/sesiones/resumen-dia-*.md`): 04-09=28, 05-09=18, 06-09=35, 07-09=43, 08-09=37, 09-09=32 → **193 sesiones en 6 días**.
- 10-09..13-09: **0 sesiones** (LAB apagado, ausencia del usuario).
- 14-09 07:10: el observador diario ha reanudado (OBS-101/102/103 + `telemetria/2026-09-14.json|.md`).

---

## 2. C. INSTRUMENTOS SIN ALIMENTAR (hallazgo de la semana)

### C1. El ledger del EXP-20260903-001 se creó y nunca se alimentó

- **03-09 14:56** — el usuario **APRUEBA** el experimento (backlog grande, líneas 1631-1635): fase 1 activa 04-09→10-09, informe 11-09, ledger `04-operations/metrics/retrabajo_ledger.jsonl`.
- **03-09 15:06** — pasa a **MODO PAUSA FLEXIBLE** (backlog 1643-1647): la fase 1 mide **7 días de actividad real**, no de calendario; LAB apagado = pausa y se reanuda al volver. El registro sigue vigente («Registro empieza 04-09 si hay sesiones»).
- **14-09 (hoy)** — `stat` + `wc -l` sobre el ledger: **0 bytes, 0 líneas** (mtime 2026-09-03 14:56).
- **Evidencia de que algo había que registrar:** 6 días de actividad real (193 sesiones) y al menos 1 evento de la taxonomía cerrada E1-E7 documentado el primer día de la ventana en `pendientes.md`:
  - `2026-09-04 ~14:15 — ... GPU ocupada con Ollama al cargar glm-4.6v-flash (LM Studio) → llama-server 'exited before becoming healthy' (VRAM insuficiente, no bug)` → **E4 (debug de servicio/infra)**.
- **Entregable previsto** (11-09): `research/exp-20260903-roi-metacognicion-resultados.md` → **no existe** (`ls research/ | grep exp-` solo devuelve el diseño `exp-20260903-roi-metacognicion.md`, 03-09 14:54).
- **Divergencia documento/realidad:** el diseño sigue con `Estado: DISEÑO — pendiente de aprobación` aunque fue aprobado y arrancado el 03-09 (mismo patrón que CP-008). La memoria de sesión mantiene el ancla «EXP retrabajo ACTIVO 04-10/09».

→ **Conclusión honesta:** NO se puede afirmar «no hubo incidentes E1-E7». Lo que consta es **0 registros** y ≥1 evento E4 documentado en otro fichero el primer día de la ventana. El instrumento no se alimentó.

### C2. Registro diario de incidentes (2ª observación del mismo síntoma)

- Reactivado el 02-09 como remedio de INC-005 con la hipótesis «el problema no es el documento, es el hábito» → 0 ficheros diarios en 12 días con actividad continua.
- Es la **2ª observación consecutiva** (la 1ª la anotó el ciclo del 04-09). La hipótesis «es el hábito» no se sostiene sin un disparador.

### C3. Contraste verificado: lo que SÍ produce ficheros (tiene disparador automático)

| Mecanismo | Evidencia real |
|---|---|
| Observador diario (cron) | OBS-098/099/100 (09-09 22:00) y OBS-101/102/103 (14-09 07:10) |
| Telemetría diaria | `telemetria/2026-09-08|09|14.json` + `.md` |
| Backups hermes-state | cron diario 22:20 (job `5119c2e881ad`) |
| Backlog grande (por disciplina, SIN cron) | entradas 01-09=35, 02-09=14, 03-09=17, 06-09=3, 08-09=7, 09-09=1 → **huecos en 04, 05 y 07-09** |

Diferencia medida: lo que tiene cron escribe cada día; lo que depende de recordar, no.

---

## 3. Aciertos de la ventana (verificables, sin promoción)

- **Experimento HyDE cerrado CON DATO** (05-09 19:52, spike ejecutado, no integrado) — `pendientes.md`.
- **Herramienta nueva `tools/mapa_conocimiento.py` + `tools/mapa_conocimiento.sh`** (04-09 19:30) que resuelve el gap visual del RAG.
- **Verificación uno a uno de repos de skills comunitarios** (04-09 12:57, `ZeroPointRepo/awesome-hermes-skills`) → la regla «no dar por bueno lo declarado» se aplicó sin excepción.

---

## 4. Patrón promovido (2+ ocurrencias en contextos distintos)

**CP-009 — «Instrumento sin disparador no se usa»** → `lpa/pattern-incubator/CP-009-instrumento-sin-forzado-se-degrada.md` (E0, con condición de falsación).

Ocurrencias: (1) ficheros de conocimiento LPA dormidos 31-07→01-09 (INC-005); (2) registro diario de incidentes, 0 ficheros en 12 días tras reactivarse; (3) ledger del EXP-20260903-001, 0 líneas tras 6 días de actividad.

Solape parcial con **CP-008** («una métrica en 0 que nadie mira equivale a no tener métrica») → anotado como candidato de fusión en ambos ficheros, para la revisión mensual del 01-10.

---

## DECISIONES (14-09)

- [x] **D0 (INC-005 — vigilancia):** no hay incidentes nuevos → **NO se fuerza ninguna promoción desde incidentes**. INC-005 pasa de «remedio por hábito» a «remedio sin verificar»: 2ª observación del mismo síntoma (C2). Sin acción unilateral.
- [x] **D1 (hallazgo C1, registro):** el ledger del EXP-20260903-001 queda **documentado como no alimentado** (0 líneas, 0 días de registro útiles, ≥1 evento E4 fuera del ledger). No se rellena a posteriori: el diseño prohíbe registrar «de memoria días después» y hacerlo contaminaría el baseline. Estado: **bloqueado esperando decisión del usuario**.
- [ ] **D2 (EXP-20260903-001 — decisión del usuario, 3 opciones):** (a) **reanudar** la fase 1 con disparador (registro retrospectivo declarado desde `pendientes.md`/backlog de la semana, no de memoria) hasta completar 7 días de actividad; (b) **cerrar** la fase 1 como «sin datos» y dejar congelada la capa metacognitiva (no se puede decidir H1/H0 sin medida); (c) **retirar** el experimento y su ancla de memoria. Requiere fechas confirmadas por el usuario (LAB reanudado hoy 14-09).
- [x] **D3 (patrón):** promovido **CP-009** a incubadora + enlace cruzado con CP-008 (backups `.bak-20260914` de los ficheros tocados, RULE-008).
- [x] **D4 (lección de proceso):** registrada en `04-operations/metrics/lecciones_ledger.jsonl` (dominio `proceso`) y añadida como comprobación manual en la skill `detectar-sin-uso`.
- [ ] **D5 (propuesta, NO ejecutada):** dar al registro de incidentes un disparador real, colgándolo de un cron que ya funciona (p. ej. el ciclo semanal rellena la semana desde `pendientes.md`/backlog; el registro diario lo genera el observador diario de las 07:10 junto a los OBS). Cambia infraestructura de crons → **requiere confirmación explícita del usuario**.

---

## 5. Cadena incidente → lección → mejora

| Eslabón | Estado 14-09 |
|---|---|
| **Incidente** | INC-005 (01-09, conocimiento LPA dormido) + hallazgos C1/C2 (14-09, instrumentos sin alimentar) |
| **Lección** | `LEC-…` dominio `proceso` («instrumento sin disparador no se usa») — registrada hoy |
| **Patrón** | **CP-009** (E0, incubando; falsación definida) |
| **Mejora** | **PROPUESTA, no ejecutada** (D5): disparador automático para el registro. Sin confirmación del usuario no se toca ningún cron |

---

## 6. Próxima revisión

- **Semanal:** 2026-09-21 (lunes).
- **Mensual (la 1ª del mes):** 2026-10-01 → revisar incubadora completa (CP-001..CP-009) y decidir promoción a `KNOWN.md`/`HYPOTHESIS.md` o descarte; incluye la fusión CP-008/CP-009 si se confirma el solape.

Documento generado: 2026-09-14 07:14 CEST (fecha verificada con `date`) · fuentes: `lpa/incidentes/` (ls), `retrabajo_ledger.jsonl` (stat+wc), `lecciones_ledger.jsonl`, `04-operations/backlogs/pendientes.md` y `2026-07-31-backlog.md` (líneas 1624-1647), `01-knowledge/observations/`, `04-operations/metrics/telemetria/`, `research/exp-20260903-roi-metacognicion.md`.
