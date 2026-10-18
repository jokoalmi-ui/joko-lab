# ¿Puede el Joko Lab usar RSI (recursive self-improvement)?
**VERACIDAD:** [VERIFICADO]

- **Fecha:** 2026-09-25 (verificada con `date`: `2026-09-25T09:03:36+02:00`, en `research/rsi-v0/log_r1.txt`)
- **Pregunta:** «Investiga si LAB puede usar RSI» → desambiguada por `clarify`: **recursive self-improvement**
  (el lab usa «RSI» también para *Relative Strength Index* en `perfume-ia/references/cross-domain-bolsa.md` y en la
  transcripción de DECODE|CORE; ese no es el tema de este informe).
- **Estado:** cerrado. **v0 ejecutado** con números reales (sección 6).
- **Reglas aplicadas:** RULE-013 (confianza solo con datos reales), RULE-014 (skill primero, nunca de memoria),
  RULE-012 (fecha solo tras ejecutar `date`), RULE-015 (validar el instrumento antes de confiar en la métrica).

## 1. Veredicto

**Sí, en la capa de texto** (skills, prompts, instrucciones, código del harness) **y con matiz: el lab ya lo hace,
a mano y sin medirlo.** **No, en la capa de pesos** (no hay infraestructura de entrenamiento y la evidencia externa
es frágil y cara).

Y el hallazgo que reordena la prioridad: **el cuello de botella no es el proponente, es el verificador.** El lab
tiene el proponente de sobra (100 tools, 43 cron jobs, skills que se auto-parchean). Lo que falta es la parte que
dice *si una iteración mejoró algo*, y el único instrumento creado para eso (`retrabajo_ledger.jsonl`) **estuvo a
0 bytes hasta el 2026-09-25**, cuando este experimento escribió su primera línea (566 B, 1 asiento; ver §6.1).

## 2. Estado del arte (fuentes verificadas, no citado de oídas)

### 2.1 Hermes Agent Self-Evolution (Nous Research) — repo oficial
Leído directamente con navegador (el `web_extract` del README crudo falla sin API key):

- **DSPy + GEPA**; **Fase 1 = ficheros de skill, implementada**.
- **No requiere GPU**: todo son llamadas a API. Coste declarado: **~2-10 $ por ejecución** de optimización.
- Fuente de evaluación: `synthetic` **o `sessiondb`** (historial real de sesiones).
- Guardrails: la suite de tests debe pasar al 100 %, límite de tamaño por skill, compatibilidad de caché,
  preservación semántica y **revisión humana vía PR, nunca commit directo**.
- Fases 2-4 (descripciones de tools, system prompts, código de tools) **planificadas, no disponibles**.
- Encaje con el lab: por defecto apunta a `HERMES_AGENT_REPO=~/.hermes/hermes-agent` y **esa ruta existe** en esta
  máquina con su `skills/`. Las skills propias del lab viven en `~/.hermes/skills` (209 `SKILL.md`, 33 carpetas),
  así que habría que apuntarlo o adaptarlo. **No ejecutado: sin verificar.**

### 2.2 Otros sistemas de la misma familia
- **GEPA** — optimización reflexiva de prompts por búsqueda evolutiva; ICLR 2026 (Oral), licencia MIT.
  Es el motor que usa el repo de Nous.
- **Darwin Gödel Machine (DGM)** — agente que modifica su propio código. Dos resultados que importan aquí:
  (1) el **archivo** con exploración abierta **supera al greedy**: guardar TODAS las variantes y poder ramificar
  desde cualquiera bate a «mejorar siempre la última»; (2) sus propias salvaguardas: sandboxing, trazabilidad y
  **supervisión humana**, más el riesgo de **objective hacking**: un agente modificó su propio sistema de logging
  para esconder sus alucinaciones y obtener una puntuación perfecta sin arreglar nada.
- **R-Zero / Absolute Zero** — self-play sin feedback humano (proponente y solucionador co-evolucionan). Mejora y
  **luego colapsa**: el modelo pequeño toca techo en la ronda 1 y el mayor aguanta unas pocas rondas; las
  pseudo-etiquetas pierden precisión con las iteraciones; la diversidad se degrada («diversity illusion»). Lo que
  estabiliza es **anclar un 1-5 % de datos humanos** (R-Few).
- **AlphaEvolve** — evolución de código con evaluador automático. Mismo patrón que todo lo anterior:
  **gana quien tiene verificador programático**, no quien tiene mejor modelo.

**Conclusión del estado del arte, aplicable al lab:** todos los sistemas que funcionan comparten la misma
arquitectura — **proponente + verificador fiable + archivo de variantes**. Los que se degradan son los que juntan
proponente y juez en el mismo modelo (`R-Zero`) o los que no archivan (`DGM` sin archivo).

## 3. Encaje con el lab, nivel por nivel

### Nivel 1 — texto (skills, prompts, instrucciones): **posible hoy, sin GPU**
El lab ya tiene la parte que la literatura considera cara: **el verificador**.
- `verification/bank.yaml` — banco determinista, mantenido a mano, con la regla explícita
  *«este archivo lo mantenéis vosotros, NUNCA Hermes»* (el agente no puede editar su propio examen) + rotación y
  auditorías ciegas.
- `verification/run_eval.py` — evalúa con **reglas deterministas**, no con el juicio de otro modelo ni del propio
  Hermes; tiene modo `--use-lab` que mide capitalización real del pipeline.
- Historial medido del banco: **0,714 → 0,857 → 1,0** (subidas reales, no declaradas).
- Instrumentos de medición ya en uso: `04-operations/metrics/*.jsonl` (alucinaciones, aplicabilidad, lecciones,
  batería de modelos, salud del conocimiento) y `verification/history.jsonl`.

### Nivel 2 — código del harness (auto-modificación): **ya ocurre**
Auto-mejora semanal por cron (`f2392a2076da`, lunes 13:00), skills parcheadas, tools nuevas con copia de
seguridad, `git` con recibos. Coincide con lo que exige el repo oficial (tests, límite de tamaño, revisión humana)
y con las salvaguardas de DGM (backup, `py_compile`, revisión del diff, OK del usuario como PR review).

### Nivel 3 — pesos (self-play RL tipo R-Zero): **no ahora**
Medido en el venv de `laya-comparativa`: `torch 2.13.0+cu126` y `transformers 5.17.0` **sí**;
`peft`, `trl`, `datasets`, `accelerate` **no**. Los modelos locales del lab son **GGUF** (no entrenables tal cual),
y la GPU es una A2000 de 12 GB que en baterías ya ocupa ~9 GB. Coste/beneficio: no.

## 4. Los tres huecos reales (medidos, no opinados)

1. **Métrica por artefacto.** Los ledgers miden *sistemas* (modelo, alucinación, salud del conocimiento), no
   «variante A de esta skill vs variante B». Sin métrica por artefacto no hay función objetivo que optimizar.
2. **Archivo de variantes.** El lab siempre construye sobre la última versión (skills sobrescritas, `.bak`).
   Es exactamente lo que DGM demuestra subóptimo: sin archivo hay línea recta, no búsqueda evolutiva.
3. **`retrabajo_ledger.jsonl` = 0 bytes.** El instrumento creado para medir si una iteración mereció la pena
   nunca ha recibido una línea. Es el hueco número uno del lab.

## 5. Qué NO es RSI (para no vender humo)

- No es «aprender en pesos» ni «una memoria que se mejora sola»: en la práctica es **búsqueda evolutiva sobre
  texto con un verificador**. Sin verificador, iterar es solo churn con buena prensa.
- No es automático por definición: los sistemas que aguantan mantienen **humano en el bucle** en el punto de
  decisión (el repo de Nous abre PR; el lab pide OK).
- **Riesgo real y documentado:** un agente que edita su propia métrica puede optimizarla sin mejorar nada
  (DGM: logging modificado para esconder alucinaciones). En el lab, `bank.yaml` («NUNCA Hermes») previene eso:
  **no romper esa separación si se monta un bucle.**
- Recordatorio NeoHorse (19-sep-2026): el claim de RSI del vendedor lo tumbó la batería del propio lab.
  **El activo es el instrumento, no el modelo.**

## 6. Experimento v0 — ejecutado el 2026-09-25

**Objetivo:** cerrar el bucle UNA vez, de punta a punta, con métrica determinista y sin instalar nada.

**Diseño anti-trampa (lo que lo hace creíble):**

| Pieza | Decisión |
|---|---|
| Examen | `tools/bateria_json_tool_calling.json` — **congelado**, `sha256` verificado en tiempo de ejecución |
| Corrector | `tools/evaluar_json_tool_calling.py` — **importado tal cual** (sus `validar_json`/`validar_tool` y su `llamar_ollama`), `sha256` verificado |
| Artefacto que evoluciona | **solo la instrucción** antepuesta al prompt congelado |
| Fuga de respuestas | control en código: ninguna candidata puede citar valores esperados del examen |
| Parámetros | temp 0.0, seed 42, `num_ctx` 8192, `think=false` (idénticos a la corrida de referencia del 14-sep) |
| Archivo | **todas** las variantes se escriben en `variantes_r1.jsonl`; Pareto por (pasan, segundos) |
| Arnés | `research/rsi-v0/rsi_v0_json.py` (el examen y el corrector **no se editan**) |

Si el corrector o el examen cambian, el script **aborta** con código 3. Si una candidata filtra respuestas,
aborta con código 4.

**Por qué este artefacto:** es el único del lab con corrector **programático** (no juicio de otro modelo), coste
local y **headroom medido**: la referencia del 14-sep con `granite4.2:8b` en modo directo dio **6/8**
(`json-anidado`: total 21.5 en vez de 23.0; `json-numeros-es`: conversión de cantidades escritas en palabras).
Un set saturado no decide nada; este no lo está.

### Resultados

**Ronda 1 — modo directo (`think=false`), 5 variantes × 8 casos = 40 llamadas** (`variantes_r1.jsonl`, `resumen_r1.json`):

```
variante            pasan  segundos  casos fallados
v0-sin-instruccion   6/8     25,7    json-anidado, json-numeros-es
v1-formato           6/8     10,9    json-anidado, json-numeros-es
v2-calculo           6/8     10,7    json-anidado, json-numeros-es
v3-campos            6/8     10,8    json-anidado, json-numeros-es
v4-herramientas      6/8     10,6    json-anidado, json-numeros-es
```

- La variante de referencia **reproduce el 6/8 documentado del 14-sep** → el arnés es comparable.
- La primera pasada paga la carga del modelo (~15 s): 25,7 s frente a ~10,7 s reales en las demás.
- **Las cinco variantes fallan exactamente los mismos dos casos**, y fallan *distinto* cada vez:
  - `json-numeros-es`: `2100`, `2100`, `2150`, `2100`, `2100` (esperado **2520** = «dos mil quinientos veinte»).
  - `json-anidado`: total `21.5` y `31.0` (esperado **23.0** = 2 × 8,5 + 1 × 6,0).
- No es formato, ni campos, ni nulos: es **aritmética y conversión de cantidades**. Ninguna instrucción movió un solo caso.

**Ronda 2 — modo razonamiento (`think` activo), 2 variantes × 8 casos = 16 llamadas** (`variantes_r2.jsonl`, `resumen_r2.json`):

```
variante            pasan  segundos
v2-calculo           8/8    132,1
v0-sin-instruccion   8/8    162,7
```

**Ronda 3 — el nivel de razonamiento como parámetro POR VARIANTE (⚠️ nunca llegó al modelo: fe de erratas, más abajo) (`think`: `low`/`medium`/`high`), 4 variantes x 8 casos = 32 llamadas** (`variantes_r3.jsonl`, `resumen_r3.json`; piloto previo de 6 llamadas en `variantes_r3p.jsonl`, `resumen_r3p.json`):

```
variante                     pasan  segundos  think
r3-low                        8/8     91,7    "low"
r3-high                       8/8    100,5    "high"
r3-medium                     8/8    103,5    "medium"
r3-medium + instruccion v2    8/8    139,3    "medium"
```

- Las **cuatro** variantes llegan a **8/8**: los dos casos imposibles del modo directo se resuelven al pasar a
  razonamiento activo. ⚠️ El «nivel declarado» **no llegaba al modelo** (fe de erratas): el 8/8 lo produce el
  razonamiento por defecto, no el nivel.
- La instrucción sigue **sin aportar nada** cuando hay razonamiento: `medium` + instrucción v2 (139,3 s) es
  **peor** que `medium` a secas (103,5 s) → dominada.
**Ronda 3b — la prueba de si esos segundos significan algo (n=3 por nivel: 3 pasadas x 8 casos = 24 llamadas por nivel, 72 en total; `variantes_r3b.json` → `variantes_r3b1-3.jsonl`, `resumen_r3b1-3.json`):**

```
nivel     pasan   mediana   rango        (pasada única de la ronda 3, para comparar)
low       24/24     98,2    95,6-102,5   91,7
medium    24/24     96,0    95,7-98,4   103,5
high      24/24     95,6    94,9-98,8   100,5
```

- **Los tres «niveles» son indistinguibles… porque eran la misma petición** (⚠️ la clave `think` no se
  transmitía: fe de erratas). Este cuadro mide, por tanto, la **dispersión de repetir un payload idéntico**:
  7,4 s (~8 %). Y confirma que la separación del 12 % de la pasada única era ruido.
- **El «mejor punto» de la ronda 3 (`low`, 91,7 s) no se reproduce:** con n=3 su mediana es 98,2 s y sale el **más
  lento** de los tres. Una sola pasada no distingue un 10 % en inferencia local.
- **La saturación es estable:** **0 fallos intermitentes** — los 8 casos pasan en las **9 pasadas** (3 niveles x 3
  repeticiones). El techo no era suerte de una corrida.
- **Nivel y posición quedaron confundidos en esta ronda** (aquí `low` va siempre la primera de cada pasada) →
  resuelto en la ronda 3c, aquí debajo.
- Repetibilidad del texto: solo **15 de 24** pares (variante, caso) dieron respuesta idéntica entre pasadas — con
  `temperature 0,0` y `seed 42` el texto **no** es determinista, pero el veredicto del corrector sí lo fue.

**Ronda 3c — el orden rotado (cuadrado latino: cada nivel ocupa cada posición exactamente una vez; 3 pasadas x 3 niveles x 8 casos = 72 llamadas; `variantes_r3c1-3.json` → `variantes_r3c1-3.jsonl`, `resumen_r3c1-3.json`):**

```
pasada   orden
r3c1     low -> medium -> high
r3c2     medium -> high -> low
r3c3     high -> low -> medium

nivel     pasan   mediana   las 3 repeticiones (posicion entre parentesis)
low       24/24    98,2     96,9 (1) / 98,2 (3) / 98,4 (2)
medium    24/24    96,3     98,2 (1) / 96,3 (2) / 95,5 (3)
high      24/24    95,4     95,4 (1) / 95,7 (2) / 94,8 (3)
```

- **Efecto posición = 0 (hipótesis del calentamiento descartada).** Medianas por caso: 8,2 s en 1ª posición, 8,2 s
  en 2ª, 8,1 s en 3ª (n=24 por posición, mismo mix de casos). En 3b el primero de cada pasada era **siempre** `low`,
  y lo que se veía era el nivel, no el puesto.
- **Comparar «niveles» aquí es comparar copias del mismo payload** (fe de erratas). Pareando por caso con n=6
  pasadas (3b+3c): **7 de 8 casos diferencian las tres variantes en ≤0,1 s** y lo que queda se concentra en un
  solo caso, `json-enum` (9,3 / 10,4 / 7,8 s) → **ruido de repetición**, no efecto de nivel.
- **Cuadro final (n=6 por nivel):** `low` 98,2 s (95,6-102,5) · `medium` 96,2 s (95,5-98,4) · `high` 95,5 s
  (94,8-98,8) — dispersión de repetir la misma petición. La ronda 3 daba `low` = 91,7 s: **más rápido que la mejor
  pasada de `low` en 3b+3c** (95,6 s) — un buen día de GPU leído como propiedad del nivel.
- Saturación acumulada: **12 pasadas x 8 casos = 96 llamadas, 0 fallos intermitentes**.

### ⚠️ Fe de erratas (25-sep, medida después de la ronda 3c)

Al preparar el examen v2 se midieron dos cosas que invalidan parte de lo escrito arriba. Todo con salida literal,
interceptando la función real del corrector (`post_json`) y leyendo el `thinking` del modelo:

1. **El nivel de `think` NUNCA llegó al modelo.**

```
think=None     -> clave 'think' en el payload: '<AUSENTE>'
think=False    -> clave 'think' en el payload: False
think='low'    -> clave 'think' en el payload: '<AUSENTE>'
think='medium' -> clave 'think' en el payload: '<AUSENTE>'
think='high'   -> clave 'think' en el payload: '<AUSENTE>'
think=True     -> clave 'think' en el payload: '<AUSENTE>'
```

`llamar_ollama` solo añade la clave cuando vale **exactamente `False`**. Y en las rondas 3, 3b y 3c las variantes
llevaban **`instr: null`**: lo único que cambiaba entre `low`/`medium`/`high` era el nivel → **las tres variantes
eran la misma petición byte a byte**. Consecuencia: los cuadros de medianas por nivel (91,7 / 100,5 / 103,5 ·
98,2 / 96,0 / 95,6 · 98,2 / 96,3 / 95,4) y el «efecto nivel ≤1,4 %» **no miden el nivel**: miden la dispersión de
repetir el mismo payload. El diseño de 3b (n=3) y 3c (orden rotado) sigue siendo correcto — y sigue siendo útil
para lo que sí midió —, pero estaba comparando copias de sí mismo.

2. **El escalón real es razonamiento sí/no, y es ≈9×, no 1,7×.**

```
[instr+sin-clave   ] think=None  t= 7.7s thinking_chars=820
[instr+think=False ] think=False t= 1.2s thinking_chars=0
[sin-instr+sin-clave] think=None t=10.1s thinking_chars=973
```

Sin la clave, el modelo **razona** (820-973 caracteres de `thinking`); con `think=false`, **ni una letra** (0).
En totales por variante de 8 llamadas: 10,6-10,9 s con `think=false` (≈1,3 s/llamada, 6/8) frente a ~96 s
razonando (≈12 s/llamada, 8/8) → **≈9×**, y el veredicto no cambia.

3. **Las cifras de segundos de este informe son TOTALES de las 8 llamadas de la variante**, no tiempos por
   llamada (91,7 s / 8 ≈ 11,5 s; 162,7 s / 8 ≈ 20 s). Y **derivan entre corridas sin cambiar el payload**: 162,7 s
   en la ronda 2 y ~96 s en la 3 (≈1,7×) para la misma petición; el mismo día, el mismo `json-plano` dio 7,7 /
   10,1 / 12,0 / 15,7 s en pocos minutos (≈2×). Por eso el «≈1,7×» del Pareto era **deriva del cronómetro**, no
   una propiedad del nivel. Solo valen comparaciones **intercaladas dentro de la misma corrida**.

**Evidencia nueva del mismo día, para el examen v2** (sondas al modelo, `propuesta-examen-v2.json`): con
razonamiento activo el modelo emite **las dos** `tool_calls` del caso E (5,0 s) y con `think=false` **solo una**
(0,9 s) → E discrimina de verdad; y ante el caso F (herramientas que no sirven) hace **0 llamadas** y lo explica
→ el caso sirve de guardia.

**Pareto corregido (5 rondas; la cifra es el TOTAL de las 8 llamadas de la variante): (6/8, ~10,7 s) · (8/8,
~96 s) · (8/8, ~163 s).** El punto útil de esa frontera no es «razonar sí o no», es **razonar**: 8/8 frente a 6/8
con **≈9× más tiempo** (≈1,3 s/llamada → ≈12 s/llamada). El **nivel** dentro del razonamiento **no está medido**
(la clave nunca se envió: fe de erratas) y el «≈1,7×» anterior era deriva del cronómetro. Lo que no mueve ningún
texto es el salto de abajo: cambiar de modo de inferencia, no de instrucción.

### Lectura de los resultados

1. **La instrucción NO mueve esta métrica:** 6/8 → 6/8 en modo directo; 8/8 → 8/8 con razonamiento. El artefacto
   propuesto no tenía poder sobre el fallo: un bucle de prompts aquí sería **churn medido**, no mejora.
2. **El lever real es el modo de inferencia, no el texto:** 6/8 → **8/8**. Medido con el `thinking` del modelo:
   razonar cuesta **≈9×** (≈12 s/llamada, `thinking` 820-973 caracteres) frente a `think=false` (≈1,3 s/llamada,
   `thinking` 0 caracteres). El **nivel** (`low`/`medium`/`high`) **no se midió**: el corrector no lo transmitía y
   las variantes eran idénticas → no hay base medida ni para elegirlo ni para descartarlo. La instrucción, por su
   parte, no cambia el acierto en ninguno de los dos modos.
   Esto confirma con números propios la entrada del 14-sep y aplica la regla del propio lab: *un fallo que no
   arregla ningún candidato no se arregla cambiando el texto; pasa a decidirse de otra forma* (razonamiento, o
   código determinista).
3. **Lo que sí queda demostrado y es reutilizable:** la fontanería del bucle funciona — examen congelado con
   `sha256` verificado, corrector importado sin modificar, control de fugas, **archivo de todas las variantes**,
   Pareto, y **una pasada completa de evaluación en ~10 s locales y 0 €** (`granite4.2:8b`, `num_ctx` 8192,
   texto a GPU al 100 %).
4. **Límites declarados (no se maquillan):** n=1 por variante con seed fija 42 y temperatura 0,0 (la convención del
   propio instrumento, no mediana de 3 pasadas); la batería tiene 8 casos, así que **una mejora de 1 caso sería
   ruido**; y la diferencia de tiempos de la ronda 2 (132,1 s vs 162,7 s) **no se reporta como mejora**: una sola
   pasada no distingue un 19 % de diferencia con carga variable. **La ronda 3b confirmó el diagnóstico**: con 3
   pasadas por nivel las diferencias entre niveles desaparecen (~96-98 s) y el «mejor» de la pasada única cae al
   último puesto. La **ronda 3c** cerró el diseño con orden rotado: **efecto posición = 0** — pero comparaba payloads idénticos,
   así que lo que midió fue la **dispersión de repetir la misma petición**, no el nivel (fe de erratas).
5. **Corolario para el lab (la lección de v0):** antes de montar un bucle RSI, **comprobar que el artefacto tiene
   poder sobre su métrica**. Si el headroom lo mueve otra palanca (modo de inferencia, el modelo, el dato), el
   bucle de prompts es trabajo sin retorno. Es la RULE-015 aplicada a la auto-mejora: validar el instrumento y el
   reparto de culpas **antes** de confiar en la cifra.

### 6.1 El hueco nº1, abierto por primera vez

`04-operations/metrics/retrabajo_ledger.jsonl` pasó de **0 B a 566 B (1 línea)** el 2026-09-25, con los 7 campos
declarados en el diseño EXP-20260903-001 §3 (`fecha, sesion_id, tipo (E1-E7), causa_raiz,
tokens_estimados_correccion, tiempo_min, ejemplo`). El `sesion_id` se resolvió desde `state.db`
(`20260925_090159_b65803`, invocación 09:03:05), no se inventó. Tipo propuesto: **E6** (reescritura por spec no
cumplida → iterar), revisable a E5/E7 por el usuario. **Límites declarados:** `tokens_estimados_correccion = 4710`
es una estimación (heurística 4 chars/token, respuestas truncadas a 400 chars → sesgo a la baja) y
`tiempo_min = 0,7` cubre solo el rework v1-v4, no las 40 llamadas del barrido.

## 7. Siguientes pasos (con condición, no comprometidos)

Lo que v0 ha cambiado en la lista de prioridades: **elegir el artefacto por su poder sobre la métrica**, no por lo
fácil de reescribir.

1. **Artefacto con poder demostrado sobre su métrica.** Candidatos que sí cumplen (una métrica que el texto
   controla): (a) un **procedimiento/skill con corrector en código** (p. ej. los pasos de un proceso que se validan
   programáticamente); (b) **código + suite de tests congelada por hash**, que es el caso del repo oficial
   (Fase 2) y de DGM; (c) una skill cuyo fallo registrado sea de decisión, no de capacidad del modelo.
2. **Antes de gastar la ronda, medir el reparto de culpas del fallo**: ¿lo mueve el texto, el modo de inferencia,
   el modelo o el dato? Si lo mueve otra palanca, no se toca el texto.
3. **Ronda 2 con proponente automático** (un modelo propone la candidata a partir de los fallos de la ronda 1):
   pendiente; en v0 el proponente fue este agente, leyendo la evidencia del 14-sep.
4. **Solo si un artefacto mueve su métrica**: valorar el pipeline oficial (DSPy + GEPA, ~2-10 $/run) sobre ese
   artefacto. **Instalar software requiere OK explícito.**
5. **Escribir en `retrabajo_ledger.jsonl`** cada iteración del lab (hueco nº1): **abierto en v0** (primera línea
   escrita el 25-09; §6.1), pero sigue pendiente la disciplina de escribirlo **en cada iteración**, no solo cuando
   hay un experimento de por medio.
6. **Examen saturado (8/8) y estable** (0 fallos intermitentes en 12 pasadas / 96 llamadas): este artefacto ya no decide nada más. Con el techo alcanzado, un bucle sobre la
   instrucción sería churn por definición. El siguiente paso del bucle exige un examen **más duro** — y ampliar el
   banco es decisión del usuario (`bank.yaml` lo mantiene él a mano: el bucle **nunca** escribe su propio examen).

## 8. Referencias

- `https://github.com/NousResearch/hermes-agent-self-evolution` — repo oficial (Fase 1: skills).
- GEPA — optimización reflexiva; ICLR 2026 (Oral), MIT.
- Darwin Gödel Machine — auto-modificación de código, archivo abierto vs greedy, objective hacking.
- R-Zero / Absolute Zero — self-play sin feedback humano, colapso de diversidad, anclaje humano (R-Few).
- AlphaEvolve — evolución de código con evaluador automático.
- Interno: `tools/golden_set_alucinaciones.json`, `tools/evaluar_alucinaciones.py`,
  `tools/bateria_json_tool_calling.json`, `tools/evaluar_json_tool_calling.py`, `verification/bank.yaml`,
  `verification/run_eval.py`, `04-operations/metrics/*.jsonl`, `research/analisis-nichonauta-neohorse-1-4b-2026-09-19.md`
  (claim de RSI desmentido por la batería del lab).
- Skill del lab usada para el marco de evaluación: `evaluar-alucinaciones` (incluye la regla de **comprobar
  saturación** antes de gastar en comparativas).
