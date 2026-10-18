---
title: "EXP-20260915-006 / F1 — Resultado preliminar del calculador de coste por ejecución"
type: EXP
---

# EXP-20260915-006 — F1: resultado preliminar

**ETIQUETA: NO VALIDADO.** Falta F0 (precios vigentes con fuente y fecha) y F2 (export oficial de facturación de septiembre). Estas cifras son un orden de magnitud, no una medición acreditada.
**Ejecutado:** 2026-09-15 18:2x CEST. **Herramienta:** prototipo `/tmp/coste_ejecucion.py` (solo lectura). **Salida:** `04-operations/metrics/coste-ejecucion-20260915.json`.
**Ventana:** 2026-09-03 → 2026-09-09 (7 días naturales con datos y con cache ya instrumentado).

## Reglas aplicadas (las de F1 del diseño)

- `path == /v1/chat/completions` (excluye `/api/show`).
- `status == 200`.
- modelo normalizado a `flash`/`pro` (excluye `r1-distill` y `model=null`).
- deduplicación por (timestamp, prompt_tokens, completion_tokens, status).
- cache hit/miss null → **no calculable** (NO se imputa 0).
- **No se aplica el factor ×2 de franja peak**: F0 no ha confirmado si aplica (pendiente).

## Filtrado de la ventana

| Concepto | Líneas |
|---|---|
| Válidas y calculables | **5.102** |
| No calculables (cache null) | 53 |
| Excluidas: `path` no inferencia (`/api/show`) | 182 |
| Excluidas: `status` 400 | 20 |
| Excluidas: JSON inválido | 1 |

## Resultado por día

| Día | n | cache hit | cache miss | output | ratio cache | USD (A) | USD (B) |
|---|---|---|---|---|---|---|---|
| 2026-09-03 | 885 | 143.014.528 | 3.989.699 | 1.238.262 | 97,29% | 1,3057 | 2,6961 |
| 2026-09-04 | 1.015 | 105.154.944 | 2.785.930 | 948.705 | 97,42% | 0,9501 | 1,9751 |
| 2026-09-05 | 291 | 18.710.528 | 1.389.665 | 435.472 | 93,09% | 0,3689 | 0,7241 |
| 2026-09-06 | 857 | 59.916.032 | 3.172.256 | 921.993 | 94,97% | 0,8700 | 1,7258 |
| 2026-09-07 | 861 | 65.032.448 | 2.987.848 | 1.033.987 | 95,61% | 0,8899 | 1,7950 |
| 2026-09-08 | 607 | 38.091.008 | 2.820.642 | 838.863 | 93,11% | 0,7364 | 1,4408 |
| 2026-09-09 | 586 | 44.445.440 | 2.165.941 | 692.774 | 95,35% | 0,6217 | 1,2449 |

## Agregados (los dos escenarios de precio, R2 sin resolver)

| Escenario | Fuente | Total 7 días | USD/día | USD/1.000 consultas | p50 consulta | p90 consulta |
|---|---|---|---|---|---|---|
| A | CSV oficial jul-ago (hit 0,0028 / miss 0,14 / out 0,28) | **5,7427 USD** | 0,8204 | 1,1374 | 689 micro-USD | 2.271 micro-USD |
| B | Informe `precios-ia/2026-09-14.md` (hit 0,007 / miss 0,22 / out 0,66) | **11,6018 USD** | 1,6574 | 2,2978 | 1.558 micro-USD | 4.635 micro-USD |

- Tokens de la ventana: **474.364.928 cache hit / 19.311.981 cache miss / 6.110.056 output**.
- **Ratio de cache hit real: 96,09%.**
- Reparto del coste (escenario A): cache miss **2,7037 USD (47,1%)** · output **1,7108 USD (29,8%)** · cache hit **1,3282 USD (23,1%)**.
- Mix de contexto (prompt_tokens): `>100k` 1.278 · `30-100k` 3.356 · `5-30k` 71 · `<5k` 397.

## Lectura (qué se puede y qué no se puede decir)

1. **El coste está dominado por el cache miss**, no por el volumen: 19,3M de tokens miss cuestan 2,7 USD mientras 474M de hit cuestan 1,33 USD. Cualquier optimización de coste pasa por el ratio de cache, no por "usar menos el modelo".
2. **La ventana con datos (0,82–1,66 USD/día) es del mismo orden que la facturación real 06-10 ago (1,73 USD/día)** con el escenario B prácticamente idéntico (1,6574) y el A por debajo (0,8204). **Esto es una pista, NO una prueba** a favor de B: el ratio de cache de agosto pudo ser distinto y el ledger subcuenta (cobertura 90-95%). No se usa para decidir el precio. Lo decide F0 con la fuente oficial.
3. **Micro-coste por consulta**: del orden de **1,1–2,3 milésimas de USD** por ejecución (p90: 2,3–4,6 milésimas). Es la cifra que faltaba para poder atribuir coste a la decisión del router (F4).
4. El 05-sep tiene la mitad de líneas (291) y el peor ratio de cache (93,09%): la bajada de coste de ese día es por volumen, no por eficiencia.

## Qué falta para levantar la etiqueta NO VALIDADO

- **F0**: precio oficial vigente con fuente y fecha → resuelve A vs B (diferencia de ×2 en el resultado).
- **F2**: export oficial de facturación de **septiembre** → comparación reconstruido vs facturado del mismo periodo. Sin él, no hay validación posible: el export jul-ago no contiene cache.


## Anexo 2026-09-15 — F0 CERRADO y validacion por inversion

**F0 cerrado.** Precio oficial fijado en `04-operations/metrics/precios-ia/precios-vigentes-2026-09-15.md`:
hit 0,0028 / miss 0,14 / output 0,28 USD por 1M tokens (escenario A). El escenario B queda REFUTADO:
su minimo teorico con las cantidades reales de 07->10 ago (10,4204 USD) ya supera la factura (5,9132 USD).
Evidencia primaria: price x amount = cost al sexto decimal en dos periodos oficiales independientes
(14,406802 = 14,406802 y 35,900597 = 35,900597), con el mismo precio unitario en ambos.

**Consecuencia para este resultado:** A es el unico escenario valido, asi que el coste de la ventana
03->09 sep queda en **5,7427 USD** (0,8204 USD/dia; 1,1374 USD por 1.000 consultas; p50 689 / p90 2.271 micro-USD).
Las cifras del escenario B (11,6018 USD) se retiran como referencia.

**F2-bis — validacion por inversion (NO es prueba directa):** con A, la factura de 07->10 ago se reproduce
si el ratio de cache hit de esos dias fue del **98,93%** (banda 98,93-99,53% segun la cobertura de tokens
del proxy), plausible frente al 96,09% medido en septiembre. Confirma el metodo y el orden de magnitud,
pero NO sustituye a la comparacion directa contra el export oficial de septiembre (F2), que sigue pendiente:
en agosto el campo de cache no existia, asi que el ratio implicito no se puede comprobar.
