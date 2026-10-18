# EXP-20260916-007 — F0: contrato de medida y gate de instrumentación

- **Fecha F0**: 2026-09-16, 15:2x CEST (autorización del usuario: «Si, a las 2» → aclarado por formulario: *ahora mismo*; y las 3 tareas de prueba *tal cual*).
- **Hipótesis (H-EXP-007)**: el modo supervisado (swarm multi-agente) **no mejora la calidad verificada** del entregable y **sube el coste y/o la latencia**, con el **mismo modelo** en ambos modos.
- **Diseño completo**: `diseno.md` (8.762 B, md5 `c382b0c2…`).

## Modos

- **A — sesión directa**: yo (esta sesión, `deepseek-v4-flash` cloud) hago la tarea con `web_search` + `web_extract` + verificación por `curl`, sin delegar ni lanzar cards.
- **B — supervisado**: `hermes kanban swarm` (workers en paralelo con perfil `default` → verifier → synthesizer). Mismo modelo (`deepseek-v4-flash`).

## Tareas (confirmadas por el usuario, 16-sep 15:2x)

- **T1** — precios y límites oficiales vigentes de la API DeepSeek (cierra además la F2 del EXP-20260915-006).
- **T2** — MTP en `llama.cpp` 2.38 y en LM Studio según fuentes oficiales.
- **T3** — servir un MoE de 22,6 GB en 12 GB de VRAM por offload de capas, con fuentes.

## Instrumentos (reales, verificados en F0)

### Coste — `/tmp/exp007_coste.py`

- Fuente: **`/home/jokoalmi/joko-lab/04-operations/metrics/pipeline_obs.jsonl`** — 32.416 líneas al 16-sep 15:27; rango `2026-08-06T23:35:45` → `2026-09-16T15:27:40`.
- Esquema real por línea: `timestamp, path, model, provider, stream, ttfb_ms, total_ms, status, prompt_tokens, completion_tokens, prompt_cache_hit_tokens, prompt_cache_miss_tokens, error`. El desglose de caché aparece en 9.781/32.415 líneas (en las recientes sí).
- Ventana de medida: `[desde, hasta]` sobre `timestamp` ISO local; el script escribe resultado en `/tmp/exp007/`.
- Tarifas (F0 del EXP-006, validadas por inversión 98,93 %): **flash** hit `0,0028` / miss `0,14` / output `0,28` USD por 1M tokens.
- **Regla de honestidad**: si una línea no trae desglose de caché, TODO su prompt se cuenta como **miss** → el coste sale como **cota superior** y el JSON lo declara (`sin_desglose_cache`, `aviso`).

### Calidad — `/tmp/exp007_calidad.py`

- Entrada: `[{url, cita}]` extraídos del informe.
- Criterio **objetivo, sin opinión de LLM**: `PASS` = `curl` HTTP 200 **y** cita literal presente en la página (comparación normalizada: sin acentos, comillas unificadas, espacios colapsados; fragmentos ≥25 caracteres).
- `403/429` → `ANTIBOT_NO_VERIFICABLE_POR_CURL` (no se cuenta como PASS, pero se declara). `200` sin cita → `URL_OK_CITA_NO_ENCONTRADA`.
- Salidas: `tasa_pass`, `tasa_url_viva`, detalle por claim.

## Gate F1 (fail-closed)

Antes de gastar en F2 hay que comprobar que **el tráfico del swarm entra en `pipeline_obs.jsonl`**.

- Método: marca previa (timestamp + nº de líneas) → lanzar **1 swarm pequeño** (1 worker) → esperar sin generar tráfico propio → medir el delta de la ventana.
- El ledger **no** etiqueta la card/tenant (no hay `session_id` ni `task_id` en el esquema real): la atribución es **por orden de magnitud** — si el delta de llamadas en la ventana supera claramente las llamadas que pueda haber hecho mi propia sesión, el swarm entra. Se declara como atribución aproximada, no exacta.
- **Si el swarm NO entra en el ledger**: el coste del modo B se marca **NO MEDIBLE** (jamás `0`), igual que se hizo con el −76,5 % del EXP-006.

## Criterio de decisión (RULE-015: umbral NO a priori)

- La F2 mide 3 tareas × 2 modos **intercaladas** (A,B,A,B,A,B) y devuelve 6 pares (coste, latencia, tasa_pass).
- El **umbral** de "mejora relevante" **no se fija aquí**: se fija tras ver el baseline, con los datos delante, y se anota. n=3 es baseline, no significación estadística.
- Veredicto esperado si H-EXP-007 se sostiene: `tasa_pass(B) ≈ tasa_pass(A)` **y** (`coste(B) > coste(A)` **o** `latencia(B) > latencia(A)`).

## Riesgos declarados

- El **dispatcher** tiene intervalo de 60 s → infla la latencia de B por diseño; se declara y no se interpreta como "el swarm es lento pensando".
- Workspaces **efímeros** → los informes se pierden al completar la card; para conservarlos, `--workspace dir:/abs/path` o copiar antes de completar (pitfall verificado 01-sep). El blackboard de la card sí persiste (`hermes kanban show`).
- Pitfall de assignee: `--verifier`/`--synthesizer` no se despachan con `perfil:titulo` → `hermes kanban reassign <task_id> default`.
- La web devuelve **fuentes distintas** en cada ejecución → el criterio es *verificable y citable*, no *las mismas fuentes*.
- El coste de mi propia sesión entra en la misma ventana del ledger y se declara.

## Fases

- **F0** — este contrato + los 2 medidores. ✅
- **F1** — gate de instrumentación (1 swarm pequeño). ⏳
- **F2** — 3 tareas × 2 modos intercaladas. ⏳
- **F3** — veredicto con umbral post-baseline. ⏳
