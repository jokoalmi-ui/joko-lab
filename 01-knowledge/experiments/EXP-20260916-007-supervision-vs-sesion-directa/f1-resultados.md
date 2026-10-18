# EXP-20260916-007 — F1: gate de instrumentación (RESULTADO: PASA)

Fecha: **2026-09-16, 15:31 → 15:34:54 CEST**. Autorización del usuario: «Si, a las 2» → aclarado por formulario: *ahora mismo*, y las 3 tareas tal cual.

## 1. Qué se probó

Si el tráfico de un swarm de kanban **entra en el ledger de observabilidad** `04-operations/metrics/pipeline_obs.jsonl`. Sin esto, el coste del modo B (supervisado) sería *no medible* y el experimento no podría comparar nada: nunca se registraría como 0.

## 2. Cómo

- Swarm real `exp007-f1`: root `t_9a04acbb`, worker `t_f595660a` (`default:investigador-precios-deepseek`), verifier `t_3a8fc399`, synthesizer `t_a3c346cc`. Los tres assignees quedaron en `default` (existe en disco): el pitfall de reasignación no aplicó.
- Tarea real y útil, no de relleno: precios y límites oficiales vigentes de la API DeepSeek.
- Marca antes: **32.418 líneas** (15:31). Marca después: **32.484 líneas** (15:34:54). Delta: **+66 líneas**.
- Ventana medida: `2026-09-16T15:31:00 → 2026-09-16T15:35:00`.

## 3. Resultado del gate

| Métrica | Valor |
|---|---|
| Llamadas en la ventana | **33** |
| Llamadas propias de esta sesión en la ventana | 1 (el turno de lanzamiento) |
| Prompt tokens | 1.339.710 (hit 1.252.864 / miss 86.846) |
| Completion tokens | 23.457 |
| Coste, tarifa oficial vigente | **0,030860 USD** |
| Coste, tarifa del F0 del EXP-006 | 0,022234 USD |
| Peak / off-peak | 0 peak / 33 off-peak |
| Llamadas sin desglose de caché | 4 → contadas como *miss* (cota superior) |

**33 llamadas frente a 1 mía → el tráfico del swarm entra en el ledger. GATE F1: PASA.** El modo B es medible.

## 4. Hallazgo de tarifas (afecta a la medición de coste del lab)

La doc oficial verificada hoy dice, por 1M tokens (USD):

- `deepseek-flash`: input cache HIT 0,003 off-peak / 0,006 peak; cache MISS 0,15 / 0,30; OUTPUT 0,60 / 1,20.
- `deepseek-v4-pro`: 0,022 / 0,044; 0,66 / 1,32; 1,98 / 3,96.
- Off-peak = mitad del peak. **Peak = 01:00-04:00 y 06:00-10:00 UTC, lun-vie** (= 03:00-06:00 y 08:00-12:00 CEST).

Discrepancia con las tarifas del F0 del EXP-20260915-006 (validadas allí por inversión al 98,93 %): hit 0,0028 vs 0,003 (−6,7 %), miss 0,14 vs 0,15 (−6,7 %), **output 0,28 vs 0,60 (−53,3 %)**. El medidor soporta las dos tablas (`--tarifa oficial|exp006`) y declara en el JSON cuál usa; por defecto usa la oficial vigente. **Anotado como pendiente para el EXP-006: revisar de dónde salió el 0,28 de output.**

## 5. Verificación independiente de la evidencia del swarm

No me fío del autoinforme: lo compruebo yo.

| Fichero adjunto | sha256 declarado y **recalculado (coincide)** |
|---|---|
| `informe-precios-deepseek.md` | `dec0c69e6d25ca093b850ee37900e31e34acf1a95b4f01f98ff31b4c1e30fdd3` |
| `pricing.html` | `755aa9b488d1185cba016ca4de3b3b6b8f593f5e13e5f9f961305289a5c8d242` |
| `rate_limit.html` | `a8bb7e5c48b65336ca10759b1f3a3f5d3001bbad8b58577d775c74db2decb2da` |

- Fetch en vivo de las 2 URLs: **HTTP 200**, **23.359 B** y **35.133 B** — los mismos bytes que los adjuntos.
- Las cifras de precio aparecen literalmente en el HTML vivo (comprobado con extracción propia, no con el informe).
- Medidor de calidad sobre 3 citas reales del informe: **3/3 PASS** (2 por coincidencia exacta, 1 por la vía tolerante a tags inline). Control negativo con 2 citas inventadas: **0 falsos positivos**.
- Dato colateral: `python.org` sirve a `curl` una página distinta de la del navegador → el criterio «cita literal en lo servido por HTTP» es el correcto y objetivo; no se puede exigir «lo mismo que ve el humano».

## 6. Avisos y limitaciones

- Los adjuntos del kanban **persisten** (`~/.hermes/kanban/attachments/<task_id>/`); el workspace del worker no.
- El kanban **no registra tokens por card** (`runs` solo da tiempos) → la atribución es por ventana temporal + número de llamadas, no por tarea. Declarado.
- 4 de 33 llamadas sin desglose de caché → coste declarado como cota superior.
