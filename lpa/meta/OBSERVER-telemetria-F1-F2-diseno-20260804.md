---
title: "OBSERVER — Telemetría del proceso de decisión (F1/F2/F2.5)"
type: lpa
---

# OBSERVER — Telemetría del proceso de decisión (F1/F2/F2.5)

**Estado:** DISEÑO — 2026-08-04
**Autor:** Joseba + Hermes
**Relación:** fase observacional de Loop Engineering / alimenta MEL.

## 1. Principio

El lab produce pocos eventos medibles. Antes de optimizar ciclos (vigencia,
revalidación), hay que saber QUÉ se usa de verdad. Esto NO es Loop
Engineering: es telemetría. Produce OBS (E0) y respeta LPA: nada se cambia,
nada se propone. Solo se observa.

## 2. Arquitectura

```
Ledger ──▶ Observer (F1) ──▶ Metrics (F2) ──▶ Evidence (F2.5)
                                                      │
                                                      ▼
                                                  PARAR
                                              2-3 semanas
                                              de datos reales
                                                      │
                                                      ▼
                                                 Analizar
                                                      │
                                                      ▼
                                               Proposer (NO construir aún)
```

## 3. Fuentes de datos (verificadas 2026-08-04)

| Ledger | Estado | Contenido | Mide |
|---|---|---|---|
| decision-ledger.jsonl | ✅ EXISTE (337 decisiones, lab-state/) | timestamp, provider, model, reason, nivel, temp, max_tokens | % decisiones por política, fallback rate, uso por franja |
| activation-ledger.jsonl | ❌ NO EXISTE | (a instrumentar) timestamp, rule_id, tipo_tarea, activa | qué RULE se usa, cuál nunca, peso por RULE |
| rag-query-ledger.jsonl | ❌ NO EXISTE | (a instrumentar) timestamp, query, top_k, ids_recuperados | qué KO se consulta siempre, cuál jamás, latencia |

**Medible YA con el ledger existente** (decisión real 04-ago, 337 entradas):
- Horario: 281 (83.4%)
- GPU: 44 (13.1%)
- Privacidad: 11 (3.3%)
- Disponibilidad (fallback): 1 (0.3%)

## 4. F1 — Observer

Script diario (cron 22:00 o bajo demanda) que LEE los ledgers y agrega.
NO modifica nada. Sin umbrales.

## 5. F2 — Metrics

Salida JSON + markdown en `04-operations/metrics/telemetria/YYYY-MM-DD.md`.
Números sin interpretar:
- decisiones por política (%) y por día
- RULE activadas por día (top + nunca activadas)
- KOs recuperados por día (top + nunca recuperados)
- fallback rate
- latencia media RAG

## 6. F2.5 — Evidence

Convierte patrones en OBS-XXX. SOLO observaciones, sin propuestas:

```
OBS-NNN: RULE-008 participa en el 81% de las decisiones.
```

No dice "hay que cambiar RULE-008". Después vendrán HIP → EXP → DEC por el
proceso normal con aprobación humana.

## 7. Respeto LPA

- Solo lectura + instrumentación de registro (no cambia comportamiento).
- Salida = observaciones (E0). Nada se promueve sin HIP/EXP/DEC.
- Ninguna modificación se aplica automáticamente.

## 8. Orden (decidido)

F1 → F2 → F2.5 → PARAR → 2-3 semanas de datos → analizar → Proposer.
Proposer NO se construye ahora: con una semana de datos propondría sobre
ruido.

## 9. Implementación (EJECUTADA 2026-08-04)

1. ✅ Instrumentado `activation_engine.py` → activation-ledger.jsonl
   (defensivo, try/except; de paso fix bug preexistente RULE-007 `condicion: null`).
2. ✅ Instrumentado `search.py` → rag-query-ledger.jsonl (1 línea por consulta,
   paths recuperados).
3. ✅ Creados `tools/observer.py` (F1+F2) y `tools/evidence.py` (F2.5, dedupe
   por día para no duplicar OBS).
4. ✅ Cron diario 22:00 `telemetria-observer-diario` (no_agent) vía
   `~/.hermes/scripts/observer-daily.sh`.
5. ✅ Primera salida 04-ago: informe metrics + OBS-005/006/007 (decisiones por
   política, fallback rate, uso RAG). Backups: tools/*.bak-20260804.

## 10. Lo que MEL consume de aquí

- Plasticidad: necesita "cuántas reglas cambian" → antes "cuántas se usan"
  (F1/F2).
- Calibración: confianza vs resultado → el "resultado" sale de Evidence.
- Coste cognitivo: decisiones/consultas por día.
