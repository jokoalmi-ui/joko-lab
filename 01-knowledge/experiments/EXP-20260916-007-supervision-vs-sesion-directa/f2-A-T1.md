# EXP-20260916-007 — F2 celda A(T1): precios y límites oficiales de la API DeepSeek (sesión directa)

- **Fecha**: 2026-09-16, ventana **16:09:30 → 16:10:16 CEST** (0,77 min de reloj).
- **Modo**: A — sesión directa (`deepseek-v4-flash` cloud) con `web_search` + `web_extract` + verificación por `curl`. Sin delegar, sin cards.
- **Tarea T1**: precios y límites oficiales vigentes de la API DeepSeek (cierra además la F2 del EXP-20260915-006).

## Coste y latencia (medidor `/tmp/exp007_coste.py`, tarifa oficial)

| métrica | valor |
|---|---|
| llamadas en la ventana | **4** |
| prompt tokens | 329.484 |
| **coste** | **0,007316 USD** |
| franja | 4/4 off-peak |
| ttfb_total | 3,6 s (medio 906 ms) |
| total_ms_total | 35,2 s (medio 8,8 s) |
| líneas sin desglose de caché | 0 |
| status ≠ 200 | 0 |

## Calidad (instrumento objetivo: `curl` + cita literal)

- **8 claims reales → 8/8 PASS** (todas por vía **exacta**).
- **1 control negativo** (cita inventada): correctamente **no encontrada**.
- **Fallo propio detectado y corregido en la propia celda**: el claim 5 llevaba la **URL equivocada** (la cita estaba en `rate_limit`, no en `pricing` — la página de precios tiene **0 ocurrencias** de `extra_body`). Re-verificado con la URL correcta → **PASS**. Se deja registrado como error de construcción de la cita, no como dato falso.
- Artefactos de instrumento detectados en la celda: `curl` sin `-L` devolvía **302** (la URL redirige a `pricing/`); el medidor de coste usa `--json`, no `--salida`.

## Hallazgos (la página oficial ha cambiado)

1. **El modelo es ahora `deepseek-flash` = DeepSeek-V4.1-Flash**. Los nombres legacy `deepseek-v4-flash` y `deepseek-v4-flash-vision-exp` se aceptan, pero **sus modelos están retirados**: las peticiones las sirve **V4.1-Flash** y se facturan a precio Flash.
2. **Tabla oficial vigente** (USD/1M): cache hit **0,003** (peak 0,006) · cache miss **0,15** (peak 0,3) · output **0,6** (peak 1,2) para Flash; Pro 0,022 / 0,66 / 1,98 (peak 0,044 / 1,32 / 3,96).
3. **Off-peak = mitad de peak**. Peak: **01:00-04:00 y 06:00-10:00 UTC, lunes a viernes** (= 03:00-06:00 y 08:00-12:00 CEST).
4. **`deepseek-v4-pro` se retira**: desde el **14-sep-2026 12:00 (hora de Pekín)** las peticiones a `deepseek-v4-pro` se enrutan a **V4.1 Flash** y se facturan a **precio Flash**. V4.1 Flash supera a V4 Pro en rendimiento, coste, velocidad y tiempo total (texto oficial).
5. **Límites**: concurrencia por cuenta **2.500** (flash) / **500** (pro) / 2.500 (vision-exp); al exceder → **HTTP 429**. Se cuentan **por cuenta**, no por API key. **`user_id`** da aislamiento de contenido, de **KVCache** y de planificación.
6. **Keep-alive**: el servidor devuelve líneas vacías (no-stream) o comentarios SSE `: keep-alive`; **si la petición no ha empezado a inferir en 10 minutos, el servidor cierra la conexión**.

## Impacto para el lab

- El **medidor de coste v2 ya usaba esta tabla** (0,003/0,006 · 0,15/0,3 · 0,6/1,2) → las medidas del EXP-007 están en tarifa correcta.
- La tabla del **F0 del EXP-006** (0,0028/0,14/0,28) está **obsoleta**; se confirma que infravaloraba el output a la mitad.
- El ledger registra el nombre de modelo `deepseek-v4-flash` (legacy): conviene saber que **hoy eso es V4.1-Flash**, no V4-Flash.
