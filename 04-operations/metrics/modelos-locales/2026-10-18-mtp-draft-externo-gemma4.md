# MTP con draft externo — Gemma 4 12B QAT en la RTX A2000 (12 GB)

Medido el 2026-10-18, 14:32–14:59 CEST. Datos crudos en esta misma carpeta (`*.json`).

## Qué se ha medido

Speculative decoding MTP con **draft externo** (`llama-server -md <asistente>` + `--spec-type draft-mtp`
+ `--spec-draft-n-max N`) sobre `gemma-4-12B-it-QAT-Q4_0.gguf`, comparado contra el mismo fichero sin
spec decoding. No es el MTP embebido del GGUF (ver «Por qué el draft va aparte»).

- Hardware: NVIDIA RTX A2000 12 GB (12.282 MiB).
- Motor: `llama.cpp` build **2.60.0** (`~/.lmstudio/extensions/backends/llama.cpp-linux-x86_64-nvidia-cuda12-avx2-2.60.0`), `-ngl 99`, `LD_LIBRARY_PATH` con `vendor/linux-llama-cuda12-vendor-v1`.
- Modelo: `/mnt/ssd_ia_datos/LM STUDIO/lmstudio-community/gemma-4-12B-it-QAT-GGUF/gemma-4-12B-it-QAT-Q4_0.gguf`
- Draft: `~/joko-lab/05-inference/models/gemma-4-12B-it-qat-assistant-MTP-Q8_0.gguf` (465.127.040 B, origen `Janvitos/gemma-4-12B-it-qat-assistant-MTP-Q8_0-GGUF`; **no** está en el repo de Google — allí da 404).
- Ventana aislada: puerto **8099**, `temperature 0`, `cache_prompt off`, `--jinja` + `/v1/chat/completions`, prompts fijos, rondas intercaladas baseline→modos. LM Studio (`:1234`) parado durante todo el banco.
- Banco: `~/.hermes/cache/scratch/banco_gemma.py`.

## Resultado — `n_predict 96`, ctx 4096, 2 rondas intercaladas

### Prompt LISTA (6 pasos de diagnóstico Docker)

| modo | tok/s (mediana) | ganancia | aceptación | VRAM |
|---|---|---|---|---|
| `none` | 27,95 | — | — | 9.267–9.423 MiB |
| n1 | 45,99 | +64,6 % | 86,3 % | 9.753–9.821 |
| n2 | 49,27 | +76,3 % | 76,0 % | 9.759–9.787 |
| n3 | 48,89 | +74,9 % | 68,8 % | 9.775–9.785 |
| **n4** | **51,11** | **+82,9 %** | 65,4 % | 9.798–9.789 |

### Prompt PROSA (por qué el cielo es azul)

| modo | tok/s (mediana) | ganancia | aceptación | VRAM |
|---|---|---|---|---|
| `none` | 28,12 | — | — | 9.285–9.255 MiB |
| n1 | 44,20 | +57,2 % | 80,8 % | 9.788–9.765 |
| n2 | 45,24 | +60,9 % | 72,7 % | 9.785–10.508 |
| n3 | 46,08 | +63,9 % | 67,7 % | 9.781–10.535 |
| **n4** | **47,46** | **+68,8 %** | 59,8 % | 9.781–10.507 |

Lectura: la ganancia es grande en las dos clases (+69 % a +83 %) y **el óptimo medido es n4**, no n1-n2:
la aceptación baja con n (86 → 60 %) pero el coste de verificar no se come la ganancia hasta más allá de 4.
Con la cabeza MTP **embebida** la curva del lab era la contraria (óptimo n1, n4 negativo); el draft externo
Q8_0 se comporta distinto y las dos curvas no se heredan.

## Contexto largo (n4, prompt lista)

| ctx | `none` | n4 | ganancia | VRAM n4 |
|---|---|---|---|---|
| 16.384 | 27,37 | 49,21 | +79,8 % | 10.921 MiB |
| 32.768 | 26,88 | 50,55 | +88,1 % | 11.184 MiB |

Cabe en 12 GB a 32k con ~1,1 GB de margen. Referencia del lab: `qwen3.6-35b` va a 7,7 tok/s.

## Verificación de texto (la buena, y la que estaba mal)

- Las pasadas de 96 tokens guardaron `content` **vacío**: Gemma 4 12B emite el razonamiento en
  `reasoning_content` y deja `content` en `""` mientras no termina de pensar (con `max_tokens` corto,
  `finish_reason: "length"`). Ese banco comparó dos cadenas vacías → la «coincidencia 1,0» que se anotó
  antes **era un artefacto**: no probaba nada.
- Repetido con la extracción corregida (`content or reasoning_content`), `n_predict 200`, prosa:
  `none` 28,67 tok/s (842 chars) vs n4 46,85 tok/s (+63,4 %, aceptación 55,2 %, 137/248; 844 chars) →
  **coincidencia 0,993**, no 1,0. Divergen en 2 puntos a partir del carácter 582 (`The l` → `L`) y por el
  corte a 200 tokens. Es divergencia de redacción al final, no de contenido: el spec decoding no cambia la
  respuesta, pero **tampoco es bit a bit idéntica** y publicar 1,0 exige comparar texto real.

## Por qué el draft va aparte y por qué no entra en LM Studio

- El QAT Q4_0 tiene **0 tensores `blk.N.nextn.*`** (inspección con `head -c 200M | strings`; el parser
  completo de cabecera muere con exit 137). El MTP no está embebido.
- LM Studio 0.4.20: `lms load … --speculative-draft-mtp` → error literal
  `MTP speculative decoding requires a GGUF model with a bundled supported MTP head.`
- `--speculative-draft-simple` + este asistente → **SIGABRT**:
  `Gemma4Assistant requires ctx_other to be set` y `GGML_ASSERT(ubatch->embd_state …)`.
- No existe GGUF fusionado (modelo+cabeza) en HF con `nextn`: `magnitudedev/…MTP` publica solo la cabeza
  (0,25 GB), `OliviaRossi/…Q5_K_L-MTP` el mtp aparte (0,47 GB) y `ravenx-…-MTP-Q4_K_M` (7,38 GB) da 0
  coincidencias en 120 MB de cabecera.
- Conclusión: la vía operativa es el servidor propio, no LM Studio.

## Vía operativa

`~/joko-lab/05-inference/executors/local/gemma-mtp-server.sh` (`start|status|stop`, `--ctx/--nmax/--port`,
pidfile `~/.cache/gemma-mtp.pid`, log `~/.cache/gemma-mtp.log`, default ctx 32768 / nmax 4 / puerto 8099).
Bajo demanda: arrancado ocupa ~11 GB y **hay que pararlo** antes de cargar otro modelo en `:1234`.

Verificado el 2026-10-18 con la ruta nueva del draft: arranque OK, petición real vía
`/v1/chat/completions` a **52,93 tok/s** (127 borradores, 86 aceptados), parada y VRAM de vuelta a
1.657 MiB.

## Lo que NO se ha medido

- Dosis de prompts largos reales (RAG, código): solo 2 prompts fijos y `n_predict` 96/200.
- Calidad del contenido (el banco mide velocidad y solape de texto, no corrección).
- `--spec-draft-n-max` > 4 con draft externo, ni n-max distinto por clase.
- Tool calling / formato JSON con el canal `reasoning_content` activo.
- El efecto de `reasoning_content` sobre la latencia percibida: `content` vacío con `max_tokens` bajo deja
  al cliente sin respuesta visible aunque el modelo haya trabajado 200 tokens.
