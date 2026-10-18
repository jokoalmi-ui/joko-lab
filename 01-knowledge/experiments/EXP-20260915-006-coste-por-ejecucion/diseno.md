---
title: "EXP-20260915-006 — Coste por ejecución del pipeline LLM (reconstrucción, validación y baseline)"
type: EXP
---

# EXP-20260915-006 — Coste por ejecución del pipeline LLM

**Estado:** DISEÑO — redactado 2026-09-15. NO iniciado (F0 y F2 requieren acción externa; ver Fases).
**Tipo:** EXP-20260915-006 (sexto experimento secuencial del lab; abre el eje "coste por ejecución" del HYP-002).
**Método:** Reconstrucción desde ledgers ya existentes (solo lectura) + validación contra facturación oficial. No modifica el router ni ningún servicio.
**Origen:** OBS-104 (`observations/OBS-104-coste-no-unido-al-escalado-2026-09-15.md`) + HYP-002 (`hypotheses/HYP-002-coste-por-ejecucion-y-escalado-local-cloud.md`).

## Hipótesis

> **H-EXP-006:** Es posible reconstruir el coste real por ejecución del pipeline LLM del lab a partir de los ledgers existentes (`pipeline_obs.jsonl` + tabla de precios oficial) con desviación aceptable respecto a la facturación oficial de DeepSeek, de forma que el coste pueda atribuirse después a la decisión del router (local vs cloud).

Estado: **NO VALIDADA** todavía. El reconocimiento previo (abajo) deja la reconstrucción en **−76,5%** frente a la factura → la hipótesis NO se sostiene con el instrumento actual tal como está. Este EXP mide exactamente cuánto falta y por qué.

## Reconocimiento previo (medido 2026-09-15, solo lectura)

### R1. Precios oficiales (fuente: export oficial DeepSeek, `USAGE/extraido/amount-2026-07-12_2026-08-10.csv`, columna `price` por tipo de token)

| Modelo | cache hit (USD/1M) | cache miss (USD/1M) | output (USD/1M) |
|---|---|---|---|
| deepseek-v4-flash | 0,0028 | 0,14 | 0,28 |
| deepseek-v4-pro | 0,003625 | 0,435 | 0,87 |

### R2. Discrepancia interna SIN RESOLVER (bloqueante para calcular €)

`04-operations/metrics/precios-ia/2026-09-14.md`, sección "Gasto real del lab (CSVs oficiales DeepSeek)", da para v4-flash off-peak: **miss 0,22 / output 0,66 / cache hit 0,007** USD/1M.

Son **~1,57x / 2,36x / 2,5x** los valores del CSV oficial de jul-ago (R1). Dos fuentes del propio lab dan precios distintos del mismo modelo. **No se resuelve por inferencia**: hay que contrastar con la fuente oficial vigente y fecharla. Mientras no se resuelva, cualquier cifra en € que produzca el lab es dudosa → afecta también a los informes de coste ya emitidos.

### R3. El campo de cache existe solo desde 2026-09-01 17:38:57

- `prompt_cache_hit_tokens` es **null** en todas las líneas anteriores a esa fecha (3.149 nulls de 31.659 líneas).
- Confirmado en el código: `hermes-lab/observability/pipeline_proxy.py` (líneas 177-178) emite los campos; el backup `pipeline_proxy.py.bak-20260901-cachehit` NO contiene `cache_hit` (grep = 0) → la instrumentación es del 01-sep.
- Consecuencia: **cualquier € reconstruido con datos anteriores al 01-sep es inválido** (no es que el cache fuera 0: es que no se registraba).

### R4. El ledger NO es la factura (cobertura parcial + ruido)

- Cobertura de `completion_tokens` observado vs facturado, días completos del solape: 07-ago **90,6%**, 08-ago **89,5%**, 09-ago **94,5%**, 10-ago **171,8%** (¡observado > facturado!).
- Hay `status` no-200 registrados: 58 (404) el 31-ago, 154 el 01-sep, 216 el 02-sep, 146 el 03-sep, 8 (400) el 03-sep → **peticiones fallidas no facturables** contadas como si lo fueran.
- **21 líneas duplicadas exactas** (misma ts+prompt+completion+status) de 31.665.
- `path=/api/show`: 2.919 líneas (model=null) → **no son inferencias**, no generan coste.
- 3.154 líneas sin `prompt_tokens` (~10%).
- Modelos reales: deepseek-v4-flash 28.716; v4-pro 16; r1-distill-qwen-14b 2.

### R5. Reconstrucción vs facturado (solape 06→10 ago, únicos 5 días con cache… inexistente)

| Día | n | reconstruido USD | facturado USD | desviación |
|---|---|---|---|---|
| 2026-08-06 | 48 | 0,0262 | 2,7421 | −99,0% |
| 2026-08-07 | 1242 | 0,7680 | 2,1464 | −64,2% |
| 2026-08-08 | 919 | 0,4567 | 1,1439 | −60,1% |
| 2026-08-09 | 858 | 0,3014 | 1,4337 | −79,0% |
| 2026-08-10 | 1117 | 0,4842 | 1,1892 | −59,3% |
| **TOTAL** | | **2,0365** | **8,6554** | **−76,5%** |

Causa doble identificada: (a) cero cache capturado antes del 01-sep (grueso de la desviación), (b) cobertura/deduplicación (R4).

### R6. Dato de magnitud relevante

Facturación real del lab **06→10 ago: 8,66 USD en 5 días ≈ 1,73 USD/día**, frente a los **~0,92 USD/día** del ciclo 27-jun→10-ago documentado en la skill `ai-router`. El gasto diario está aproximadamente **duplicado** en agosto respecto a la media de junio-julio. (Nota: el prompt masivo — 224-530M tokens prompt/día — vive en el cache hit a 0,0028 USD/1M; el coste está dominado por el RATIO de cache.)

### R7. Huecos de datos

Días sin ninguna línea entre 06-ago y 15-sep: **27, 28, 29, 30-ago** y **10, 11, 12, 13-sep** (huecos de 4 días, patrón compatible con PC apagado). Días con cache ya instrumentado: 31-ago (parcial), 01→09-sep, 14-sep, 15-sep.

### R8. Atribución por decisión del router: sin base

`04-operations/metrics/local_cloud_ledger.jsonl` = **5 líneas** (10-ago ×2, 22-ago ×2, 06-sep ×1) y **ningún campo de coste**.

## Diseño

### F0 — Fijar la tabla de precios vigente (BLOQUEANTE, sin coste)

Resolver R2 con la fuente oficial de DeepSeek (pantalla de precios / api-docs) **con fecha**. Salida: `04-operations/metrics/precios-ia/precios-vigentes-2026-09-15.md` indicando cuál de los dos juegos es el correcto y desde cuándo. Si el precio cambió entre jul y sep: la validación de F2 se hace con el precio del periodo del patrón oro.

### F1 — Calculador de coste por ejecución (solo lectura)

Reglas obligatorias derivadas del reconocimiento:
1. Filtrar `status == 200` (excluir 404/400/0).
2. Excluir `path == /api/show` y `model == null`.
3. Deduplicar por (timestamp, prompt_tokens, completion_tokens, status).
4. Separar por modelo (flash / pro) — el pro es ~3,1x el flash en miss.
5. `prompt_cache_hit_tokens` null → marcar la fila como `coste_no_calculable` (NO imputar 0: imputar 0 es lo que produjo el −76,5%).
6. Aplicar la tabla de F0. Franja peak ×2 (3-6h y 8-12h España) solo si F0 confirma que aplica al modelo y hora.

Salida por ejecución: `modelo`, `prompt_tokens`, `cache_hit`, `cache_miss`, `completion_tokens`, `coste_usd`, `franja`. Agregados: €/día, €/1.000 consultas, mediana y p90 €/consulta, mix por buckets de contexto (<5k / 5-30k / 30-100k / >100k).

Ubicación: primero `/tmp` como prototipo; si pasa F2 y se quiere permanente → `tools/coste_ejecucion.py` **con Gate de código** (backup + verifier ad-hoc + SVP-diff). Script del lab: NO tocar el router.

### F2 — Validación del instrumento contra patrón oro (BLOQUEANTE para el veredicto)

- **Patrón oro**: export oficial de facturación de DeepSeek del periodo (mismo procedimiento que produjo `USAGE/extraido/cost-*.csv` el 10-ago). Requiere descarga desde la plataforma → **acción del usuario**.
- Periodo a validar: **septiembre** (el único con cache instrumentado, R3). El export de jul-ago no sirve para validar la reconstrucción con cache: no hay cache que reconstruir en el ledger.
- Test de reproducibilidad del método: reproducir el −76,5% del solape 06-10 ago **con las reglas nuevas** (sin cache) → si sale distinto, el método cambió de definición y hay que explicarlo antes de seguir.
- **Sin patrón oro de septiembre, la métrica queda NO VALIDADA** y el EXP no pasa a baseline publicable (RULE-015: no confiar en una métrica sin validar).

### F3 — Baseline 7 días (solo si F2 pasa)

Ventana candidata: **03→09-sep** (7 días naturales, con cache instrumentado, sin huecos). Se publica: € total, €/día, €/1.000 consultas, mediana/p90 €/consulta, mix por buckets, y ratio de cache real (`hit/(hit+miss)`) por día.

### F4 — Atribución por decisión del router (NO en este EXP sin OK explícito)

Unir €/ejecución con `local_cloud_ledger.jsonl` exige que el orquestador escriba `coste_usd` y `tokens` al ledger (`tools/local_cloud_orchestrator.py`). Eso es **modificación de código del router** → OK explícito, y con el ledger a 5 líneas no hay base estadística todavía. Se deja preparado, no se ejecuta.

## Criterios de éxito

- **Ningún umbral a priori** (RULE-015). Primero baseline; la tolerancia de F2 se fija DESPUÉS de ver los datos y entendida la cobertura.
- Gate de validez: reconstruido ≈ facturado en el mismo periodo, con la desviación explicada (no un número mágico). Si la desviación no es explicable → el instrumento no sirve y se declara así.

## Riesgos y límites

- **Cobertura parcial del proxy**: si no ve todo el tráfico, la reconstrucción subestima estructuralmente. Hay que acotar qué tráfico ve (¿todo Hermes? ¿crons con agente? ¿scripts directos a la API?).
- **Precios**: si el precio cambió con el tiempo (R2), reconstruir hacia atrás exige el precio de cada periodo.
- **Franja peak** (×2 en 3-6h y 8-12h España): el export oficial da el día, no la hora → el factor solo se puede aplicar si F0 lo confirma.
- **Huecos** (R7): un "baseline de 7 días" debe ser "7 días con datos", no 7 días naturales si hay apagones.
- **Lo que este EXP NO mide**: latencia (otro eje; hay `total_ms`/`ttfb_ms` en el ledger), calidad de respuesta, ni el ahorro de mover tareas a local (exige además el mix de tareas por tipo).

## Pendiente / dependencias externas

1. **F0**: precio oficial vigente con fuente y fecha (descarga o consulta a la plataforma).
2. **F2**: export oficial de facturación de septiembre (descarga desde platform.deepseek.com → acción del usuario).
3. Decidir si el calculador pasa a `tools/` (Gate de código) o se queda en `/tmp`.

## Trazabilidad

- OBS: `01-knowledge/observations/OBS-104-coste-no-unido-al-escalado-2026-09-15.md`
- HYP: `01-knowledge/hypotheses/HYP-002-coste-por-ejecucion-y-escalado-local-cloud.md`
- Instrumento: `hermes-lab/observability/pipeline_proxy.py` (cache hit/miss desde 01-sep-2026)
- Patrón oro: `USAGE/extraido/cost-2026-07-12_2026-08-10.csv`, `amount-2026-07-12_2026-08-10.csv`
- Precios internos: `04-operations/metrics/precios-ia/2026-09-14.md`
- Referencias de coste ya emitidas: skill `ai-router` (`references/medicion-coste-cloud.md`, `references/analisis-coste-por-tipo.md`)


## Resultado

F1 ejecutado 2026-09-15 -> `resultados-preliminares-f1.md` (NO VALIDADO: 5,7427 USD con precio A / 11,6018 USD con precio B en 03->09-sep; ratio de cache 96,09%). Salida: `04-operations/metrics/coste-ejecucion-20260915.json`; prototipo `/tmp/coste_ejecucion.py`.


## Cierre de F0 (2026-09-15)

F0 CERRADO. Precio fijado en `04-operations/metrics/precios-ia/precios-vigentes-2026-09-15.md`:
hit 0,0028 / miss 0,14 / out 0,28 USD/1M (escenario A). B refutado (minimo 10,4204 USD > 5,9132 USD facturados).
Resultado consolidado de F1: **5,7427 USD / 7 dias (0,8204 USD/dia)**. F2 sigue pendiente del export oficial
de septiembre. Detalle en `resultados-preliminares-f1.md` (anexo) y OBS-106.
