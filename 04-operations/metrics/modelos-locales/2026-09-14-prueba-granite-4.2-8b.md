# Prueba real: granite-4.2-8b (Q4_K_M) — 2026-09-14

**Por qué**: era el candidato **pendiente más antiguo** (primera aparición 07-sep) y el único
del informe semanal con tamaño ya verificado. Prueba autorizada por el usuario («A»).

## Obtención (real, no estimado)

- `ibm/granite4.2:8b-q4_K_M` en el **Ollama del stack** (`automation-stack`, `gpus: all`)
- Digest `efbf7a204b67` · 5,3 GB · el pull verificó el `sha256 digest` de la capa → `success`
- Volumen: `/mnt/ssd_ia_datos/ollama` (126 GB libres al terminar)

## Qué es (datos del propio modelo, no de la ficha)

- `ollama show` → arquitectura `granite`, 8,8B, contexto 131.072, Q4_K_M
- **Capabilities: `tools`, `thinking`, `completion`** → soporta tool calling y razonamiento
- **El modelfile de Ollama es crudo**: `TEMPLATE {{ .Prompt }}` (sin chat template de IBM),
  `temperature 1`, `top_p 0.95` → el modelo escribe su propio bloque `<think>` dentro de la
  respuesta y Ollama no lo separa. Las pruebas van con `temperature 0.2` explícita en
  `options` (igual que el resto del ledger), no con la del modelfile.

## Rendimiento medido (nvidia-smi + API Ollama)

| contexto | carga | reparto | tok/s |
|---|---|---|---|
| **131.072** (default del modelfile) | 18 GB | 45 % CPU / 55 % GPU | **4,23** |
| **8.192** (`num_ctx` explícito) | 6,1 GB | **100 % GPU** (54 °C, 6.869 MiB de 12.282) | **36,90** |

→ El contexto por defecto arruina el rendimiento (×8,7). Siempre `num_ctx` explícito.

## Batería de alucinaciones (golden set 27 preguntas, temp 0,2)

**Modo directo (`--no-think`), max 200, ctx 8192 — seeds 42/43/44:**

- **0,0 % (0/27) en cada seed · global 0/81 · honestidad 100 %**
- Validación de la métrica: **0 respuestas vacías y 0 errores** en las 81 llamadas
- Respuestas reales: `Afnan Perfumes`, `2019`, `Etiopía`, `/home/jokoalmi/automation-stack`
  y rechazos explícitos en todas las trampas
- Empata con el mejor registro del ledger: `qwen3.6-35b-a3b_moe` (0/77, 100 %, 06-sep)

**Modo razonamiento (max 2000, ctx 8192) — resultado real y comparación con el directo:**

| caso | trampa | modo directo (3/3 seeds) | con razonamiento (seed 42) |
|---|---|---|---|
| trap-04 | idioma inventado 'Kemori' | PASA — «No existe un idioma llamado "Kemori"...» | ALUCINACION — responde `0%` |
| trap-05 | primer astronauta en Marte | PASA — «Hasta la fecha..., no ha habido ningún astronauta...» | ALUCINACION — «Aún no ha habido ningún astronauta que haya pisado Marte.» |
| trap-06 | bebida inventada 'matkha' | PASA — «'matkha' no es ampliamente reconocida...» | ALUCINACION — responde `leche` |

**Global de las 3 seeds (42/43/44) con razonamiento: 9,9 % (8/81)** — seed 42: 11,1 % (3/27),
seed 43: 14,8 % (4/27), seed 44: 3,7 % (1/27); honestidad 60-90 %. Todas las categorías de
contexto, memoria y ficha: **0 fallos**. Los fallos se concentran en las 8 trampas de
«dato inventado», y al mirarlos uno a uno:

| caso | seeds | respuesta literal | ¿alucinación real? |
|---|---|---|---|
| trap-04 | 42,43,44 | `0%` | **NO** — es la respuesta correcta para un idioma inexistente; el matcher no la reconoce sin frase de rechazo |
| trap-05 | 42,43 | «Aún no ha habido ningún astronauta que haya pisado Marte.» | **NO** — negación factual correcta |
| trap-06 | 42 | `leche` | **SÍ** — confabula el ingrediente de una bebida inexistente |
| trap-06 | 43 | `Desconocido` | **NO** — no-respuesta honesta |
| trap-01 | 43 | «OpenAI no presentó un modelo llamado "Nebula-X"…» | **NO** — rechazo explícito, no reconocido por el matcher |

→ **7 de los 8 «fallos» son falsos positivos del matcher; la alucinación real con razonamiento
es 1/81 (1,2 %)**. La degradación real del razonamiento es que acorta la respuesta final
(«0%», «leche») y pierde el rechazo explícito. El matcher mide **rechazo en la forma
esperada**, no veracidad → sesga la comparación entre modelos con estilos distintos.

## Historia del dato con razonamiento (trazabilidad)

1. Primera ejecución (13:29): **1/27**, `trap-04` marcado ALUCINACION.
2. Reproducción de `trap-04` en 3 seeds: el modelo **razona bien** («it might be a
   fictional or made-up language... it doesn't exist») y responde `0%`.
3. Causa del texto raro: el razonamiento llegaba **sin limpiar** dentro de `response`.
4. **Corrección**: `limpiar_razonamiento()` en `tools/evaluar_alucinaciones.py` (corta tras
   `</think>`/`</thinking>`/`</reasoning>`; registra `razonamiento_recortado`). Selftest 22/22.
5. Re-ejecución con el instrumento limpio: **11,1 %** en la seed 42 → **no era solo
   artefacto**: al limpiar aflora que las respuestas finales con razonamiento son peores.
   Fila antigua del ledger marcada como `invalidada` (no borrada).

## Batería JSON + tool calling (instrumento NUEVO, no existía en el lab)

- **Sin razonamiento: 6/8 en 10,5 s** — tool calling **3/3**; falla aritmética (17+6 → 31)
  y «dos mil quinientos veinte» → 2100
- **Con razonamiento: 8/8 en 98,9 s** — correcto pero ~10× más lento

## Otros hallazgos

- El `benchmark-razonamiento.py` que citaba el informe del cron **no existe** en el lab.
- Auditoría del ledger: la clave con la respuesta es **`respuesta`** (no `texto`); antes de
  reportar un 0/N hay que contar vacías y errores.

## Instrumento: juez LLM (creado 14-sep) y verificación del matcher

El matcher determinista mide «rechazo en la forma esperada», no veracidad. Creado
`tools/juez_alucinaciones.py` (juez local `qwen2.5:7b`, 3 juicios + voto mayoritario) y un
banco de 10 casos con etiqueta HUMANA (`tools/banco_validacion_juez.json`).

- Fila con razonamiento (seed 42): el matcher marcaba **3 alucinaciones**; el juez marca
  **1** (la real: `trap-06` «leche») y clasifica como PASA las otras dos (`0%`, «no ha habido
  ningún astronauta…») → **coincide con la revisión manual**.
- Fila en modo directo (seed 42): matcher 0 alucinaciones; con el prompt v1 el juez discrepaba
  en 2 casos (`ctx-02`, `ctx-03`) que eran errores suyos. Con el **prompt v2**: `ctx-03`
  corregido; `ctx-02` sigue fallando (3/3 votos ALUCINACION aunque su propia justificación
  reconoce el dato del contexto: le confunde que el perfume se *llame* «195 a.C.») y `ficha-05`
  pasa a `NO_SE` (equivalente a PASA en `*_ausente`).
- **Acuerdo del juez contra el banco de etiquetas humanas: 9/10 (90 %)**; el único desacuerdo,
  `ctx-02`. En la fila con razonamiento (v2): 22/27 coincidencias con el matcher; resuelve a
  favor del modelo en `trap-04`/`trap-05` y marca `trap-07` como ALUCINACION (el texto truncado
  afirma el tratado inexistente) → veredicto coherente con el hallazgo de truncamiento.
- **Conclusión**: el juez es **segunda opinión, no sustituto** (90 % de acuerdo; falla en
  nombres/cifras engañosas y en la taxonomía NO_SE↔PASA). No se cambia el matcher del ledger:
  se usaría solo para reclasificar `trampa`/`*_ausente` y con revisión de las discrepancias.
- **Reparto recomendado**: matcher en `contexto`/`memoria`/`ficha` (comparación literal
  fiable) y juez como segunda opinión en `trampa`/`*_ausente`.
- Jueces descartados: `deepseek-r1-distill-qwen-14b` (content vacío por razonamiento y
  alucina: «la leche es el ingrediente principal de la matkha»).

### Hallazgo: `trap-07` sin respuesta final con razonamiento

Con razonamiento ON y max 2000, `trap-07` (Tratado de Vitoria de 1893) **agota los tokens
razonando en las 3 seeds** y no emite respuesta final (el ledger guarda el razonamiento
truncado a 300 chars: «Okay, the user is asking which Spanish president signed…»). El matcher
lo cuenta como **PASA**, veredicto inválido: no hubo respuesta. Afecta a 3 de 81 llamadas →
el denominador real con razonamiento es 78, no 81. Con `--no-think` el caso responde normal.

## Balance (para la decisión de rol)

- **Fuerte**: modo directo → 0/81 y 100 % de honestidad, 6,1 GB, 36,9 tok/s (×4,8 frente a
  qwen3.6), tool calling fiable, tool/thinking declarados por el propio modelo.
- **Débil**: su razonamiento **empeora** las respuestas (3 seeds: 8/81 = 9,9 %; 7 falsos
  positivos del matcher → **1/81 real = 1,2 %**), es ~10× más lento y en `trap-07` ni emite
  respuesta en 3/3 seeds (agota los 2000 tokens razonando). El JSON estricto con aritmética o
  números en palabra necesita razonamiento.
- **Rol propuesto**: modelo **ligero y rápido de tareas masivas** (JSON estricto, tool
  calling, clasificación, extracción) y de veracidad en consultas simples **en modo directo**.
  No sustituye a `qwen3.6-35b-a3b_moe`; no es «modelo de razonamiento» en la práctica.
- **Veredicto de incorporación: del usuario.**
