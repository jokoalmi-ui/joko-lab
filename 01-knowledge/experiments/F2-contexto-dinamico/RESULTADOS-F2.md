# RESULTADOS-F2 · Desglose del contexto dinámico de una sesión Hermes

Experimento: **F2-contexto-dinamico** (predecesor: F1-contexto-fijo, cerrado 16-sep-2026).
Medición: **26-sep-2026**, 17:57–18:32 CEST. Coste: **0 €**. Todo solo-lectura.

## 1. Pregunta

F1 midió el prompt **fijo** (23.292 tok netos, 16-sep). Lo que quedaba sin desglosar es el
resto: **¿cuánto del prompt real es fijo, cuánto es dinámico y en qué bloque está la palanca?**

## 2. Estado de las fases

| Fase | Qué es | Estado |
|---|---|---|
| F2.0 | Recolección (prompt-size + esquema de dumps + ledger) | ✅ hecha |
| F2.1 | Validación del instrumento (suelo, aditividad, determinismo, límites) | ✅ hecha |
| F2.2 | Desglose por bloque en tokens | ✅ hecha (1 dump) |
| F2.3 | Prueba A/B de la palanca con umbral post-hoc | ⛔ **NO lanzada** (requiere OK) |

## 3. F2.1 · El instrumento, validado antes de usarlo

Instrumento: `POST http://127.0.0.1:1234/v1/chat/completions`, `max_tokens=1`,
modelo **openai/gpt-oss-20b** (el mismo que usó F1, para que las cifras sean comparables).
Se lee `usage.prompt_tokens`. No hay tiktoken ni transformers en ningún venv del lab:
el tokenizador **solo** puede venir del endpoint.

- **Suelo/offset = 68 tok.** Contenido `x` → 68. En dos procesos distintos → 68 y 68
  (determinismo). `x`, `y` y `xy` → 68 los tres: no hay término oculto.
- **Incertidumbre del framing: ±3 tok.** F1 midió el 16-sep **71 (A) / 67 (B)** con el mismo
  modelo: el offset **no es perfectamente estable** entre arranques. Se declara, no se esconde.
- **Aditividad medida**: tramos de 746 + 685 + 721 tok → suma 2.152; medidos juntos 2.154.
  Desviación **+2 tok = +0,09%**. Los bloques se pueden sumar.
- **Framing por mensaje ≈ 6,8 tok** (F(k) = 0 / 10 / 12 / 22 / 24 / 34 para k = 1…6;
  con 5 mensajes extra → 34/5 = 6,8). No lo captura la medición por bloques: hay que sumarlo.
- **Límite real encontrado (no estaba en el diseño)**: el modelo se cargó con
  **contexto 8.192 tok, no 131.072**. Medido: 25.000 chars pasan; 50.000 chars → HTTP 400
  del motor; un array con el `system` del dump (10.470 tok) → *«exceeds the available context
  size (8192)»*. **Consecuencia**: el tokenizado se hace **por trozos de 20.000 chars con
  reintento adaptativo**. El instrumento mide bloques, no peticiones completas de 300k.

## 4. F2.2 · Composición real de una petición (en tokens)

Dump medido: `request_dump_20260803_154237_873858_20260803_231400_835197.json`
(1,40 MiB de fichero · **1.154 mensajes** · 30 tools · destino api.deepseek.com · era semana-32).

Tokens de **contenido** (offset descontado, medidos bloque a bloque):

| Bloque | tokens | % tok | bytes contenido | bytes JSON crudo | mensajes | tok/kB |
|---|---|---|---|---|---|---|
| assistant | **168.845** | **51,0%** | 516.591 | 714.959 | 567 | 334,7 |
| tool | **123.305** | **37,3%** | 389.781 | 438.014 | 466 | 323,9 |
| user | 14.564 | 4,4% | 56.343 | 60.193 | 120 | 264,7 |
| tools_json (schemas) | 13.688 | 4,1% | 58.295 | 63.289 | 30 | 240,4 |
| system | 10.369 | 3,1% | 42.780 | 43.166 | 1 | 248,2 |
| **contenido total** | **330.771** | 100% | 1.063.790 | 1.319.621 | 1.154 | |

Framing de los 1.153 mensajes extra: 1.153 × 6,8 ≈ **7.840 tok**
→ **petición real ≈ 338.611 tok**.

- **Dinámico** (assistant + tool + user) = 306.714 tok = **92,7%**
- **Fijo por petición** (schemas + system) = 24.057 tok = **7,3%**

Dos avisos de etiqueta (importante): «bytes contenido» es el texto de los mensajes;
«bytes JSON crudo» incluye claves, `role`, `tool_call_id` y escapes — por eso las cifras
del fichero de mediciones son mayores. Las dos bases son válidas; **no se mezclan**.

Las salidas de herramienta son **el bloque más denso en tokens por byte** (324–335 tok/kB
frente a 240–265 del resto). El peso no está en un monstruo suelto, sino en la acumulación:
**460 llamadas** en ese dump — `terminal` **284**, write_file 50, web_search 33, patch 30,
skill_manage 17, read_file 13, cronjob 8, skill_view 7, process 6, browser_navigate 5,
memory 4, todo 3.

## 5. Hallazgo 2 (no buscado) · El régimen cambió: el ledger no es plano

El p50 agregado de todo el ledger (154.309 tok) **no describe el hoy**: mezcla eras.
P50 por semana ISO, filas con `prompt_tokens ≥ 1.000` (`/v1/chat/completions`):

| Semana | n | p50 | p90 | >131k | >200k | >300k | caché hit% |
|---|---|---|---|---|---|---|---|
| 2026-W32 | 2.719 | **316.775** | 451.399 | 86,6% | 79,6% | 55,1% | — |
| 2026-W33 | 6.787 | 278.271 | 444.877 | 91,4% | 76,3% | 40,4% | — |
| 2026-W34 | 7.496 | 213.900 | 286.303 | 84,3% | 57,0% | 3,5% | — |
| 2026-W35 | 1.808 | 218.551 | 287.681 | 82,1% | 60,5% | 4,4% | — |
| 2026-W36 | 5.404 | 121.001 | 273.347 | 47,2% | 31,2% | 1,9% | 97,4% |
| 2026-W37 | 1.863 | 78.299 | 119.836 | 8,7% | 1,8% | 0,0% | 94,9% |
| 2026-W38 | 5.985 | 76.467 | 94.961 | 0,4% | 0,0% | 0,0% | 93,7% |
| 2026-W39 | 4.343 | **80.293** | 98.253 | 4,5% | 0,2% | 0,0% | 93,9% |

- La mediana ha caído de **316.775 → 80.293 tok**: factor **≈4** en 7 semanas.
- Desde W36 el ledger trae `prompt_cache_hit_tokens`: **93,7–97,4% de hit**.
  El coste real de un prompt grande NO es proporcional a `prompt_tokens`.
- **Régimen actual (últimos 7 días, n = 5.343)**: min 1.000 · p25 67.581 ·
  **p50 79.964** · p75 91.324 · **p90 97.732** · max 209.050 · media 80.343 ·
  `>131k` **4,0%** · `>200k` **0,1%**.

**Recálculo del reparto con el régimen de hoy** (fijo F1 = 23.292 tok sobre p50 79.964):
**fijo ≈ 29,1% · dinámico ≈ 70,9%**.

Esto **corrige** la lectura del diseño (que decía fijo ≈15% / dinámico ≈85%): aquel 15%
salía del agregado de todo el ledger, no de una semana real de hoy. La palanca sigue
estando en el dinámico, pero **más pequeña de lo que parecía y ya reducida 4×**.

## 6. Limitaciones (declaradas, no resueltas)

1. El tokenizador es **gpt-oss-20b**, no DeepSeek: los tokens del ledger y los de aquí
   **no son directamente comparables**. Cuenta el orden de magnitud y la fracción.
2. El dump medido es de la **semana 32** (era de peticiones de 300k) y es un **volcado de
   fallo** (`max_retries_exhausted`) — precisamente porque superaba el contexto.
   **La composición de una sesión media de hoy (~80k) NO está medida**: es la siguiente
   medición pendiente si se quiere atribuir la palanca en el régimen actual.
3. `usage` en **0/27** dumps: no hay patrón oro por petición. El ledger no tiene campo de
   sesión (es distribución, no patrón oro).
4. Caché de prompt medida solo **desde W36** (antes el proxy no la registraba).
5. Offset ±3 tok y framing ±0,2 tok/mensaje: despreciable en bloques de miles de tokens.

## 7. F2.3 · La palanca: qué se propone y qué NO se decide

Evidencia acumulada: el dinámico pesa ~71% hoy, y dentro de él las **salidas de herramienta**
son el bloque más denso (`terminal` = 284 de 460 llamadas en el dump medido).

Propuesta (reversible, sin tocar `config.yaml`, 0 €): durante N sesiones, acotar el volumen
de las salidas largas de `terminal` (volcar a fichero y leer solo lo necesario) y comparar la
distribución de `prompt_tokens` contra esta **línea base congelada**:

> últimos 7 días · n = 5.343 · p50 79.964 · p90 97.732 · p75 91.324

**El umbral NO se fija ahora.** RULE-015: se fija **después** de ver la variabilidad natural
de la línea base (la dispersión diaria de los últimos 14 días ya está medida en
`linea_base_f2.py`). Sin ese paso, cualquier «mejora» sería a ojo.

## 8. Reproducción

```
# instrumentos del experimento (solo lectura)
python3 linea_base_f2.py            # régimen del ledger: semanal + día + caché
python3 leer_ledger_f2.py           # distribución agregada (instrumento D)
python3 analizar_dumps.py <dump>    # composición en bytes de un dump (instrumento C)

# tokenizado por bloque (necesita LM Studio levantado con un modelo cargado)
#   offset = tokens de un mensaje de 1 char; trozos de 20.000 chars
#   contexto cargado 8.192 tok -> NO sirve para medir peticiones completas de 300k
```

## 9. Efecto colateral registrado

La pasada de `tools/verificar_research.py` **sin `--archivo`** (18:01–18:04) normalizó la
línea `**VERACIDAD**` en 35 ficheros `.md` de `research/` (+38 / −17 líneas). Lección:
**usar siempre `--archivo <ruta>`**. Revertible con `git checkout --`; pendiente de decisión.
