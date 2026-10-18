# Cierre de evaluación — terna `outcome` + `trayectoria` + `constraints`

**Fecha:** 2026-10-11, 14:02–14:07 CEST (domingo).
**Plantilla aplicada:** `04-operations/reports/PLANTILLA-cierre-outcome-trayectoria-constraints.md` (v1.0).
**Qué es:** primer cierre REAL del lab con la terna completa. Cierra el ítem **(B)** de
`04-operations/backlogs/pendientes.md:626` («Adoptar la terna outcome + trayectoria + constraints
como plantilla de cierre de evaluaciones y EXP»). No reescribe ningún cierre anterior.

---

## 1. OUTCOME — ¿qué salió?

- **Instrumento:** `tools/evaluar_json_tool_calling_v2.py` (9.896 B; comentario de versión `v2`).
- **Set de casos:** `tools/bateria_json_tool_calling.json` v1.0.1 (7.706 B, creado 14-sep-2026);
  sha256 declarado por la propia corrida = `30557a9df6ee2fca82f3a823ed8e5dea20baa56ebc21d00c7b6f51f011493080`.
  8 casos: 5 `json` + 3 `tool_calling`.
- **Modelo / backend:** `qwen2.5:7b` servido por **Ollama** (`127.0.0.1:11434`).
- **Parámetros que afectan a la comparabilidad:** `num_ctx = 8192` (explícito),
  `think_pedido = omit`, `think_payload = <AUSENTE>`. Temperatura/seed: **no aparecen en la salida**
  (el resultado no las reporta) → no se afirman aquí.
- **Resultado:** **7/8 (87,5 %)**; `segundos_total = 98,8`.
- **Fallo único:** `json-numeros-es` → `a: esperado 2520, obtenido 2512` (`b = 30.5`, correcto).
  El caso pide convertir a número «dos mil quinientos veinte» y «treinta coma cinco».
  La respuesta emitida fue JSON válido, sin fences y sin texto extra → **es un fallo de contenido
  (lectura del número en palabras), no de formato**.

## 2. TRAYECTORIA — ¿cómo llegó?

Datos por caso (los 5 `json` no usan herramientas; los 3 `tool_calling` sí):

- **5 casos `json`:** `n_tool_calls = 0`, `thinking_chars = 0` en todos.
- **3 casos `tool_calling`:** exactamente **1 tool call** cada uno, nombre correcto en los 3 (3/3),
  **0 reintentos**, **0 chars de razonamiento**:
  - `tool-eleccion` → `consultar_clima` con `{ciudad: "Getxo", unidad: "celsius"}`.
  - `tool-args` → `enviar_email` con `{asunto: "Cena del sábado", destinatario: "maite@ejemplo.com"}`.
  - `tool-dos-pasos` → `contar_cafes` con `{especialidad: true}`.

Hallazgos que el resultado final NO muestra:

- **(A) Argumento inventado que el corrector no comprueba.** En `tool-dos-pasos` el modelo emitió
  `contar_cafes` con `{"especialidad": true}`, pero esa herramienta declara `parameters.properties = {}`
  (sin parámetros). El banco solo comprueba `herramienta: contar_cafes` → `pasa = true`.
  La trayectoria caza un fallo de esquema que el outcome da por bueno.
- **(B) «Dos pasos» fueron uno.** `tool-dos-pasos` pide contar cafés y luego dar el precio del último.
  El modelo hizo 1 tool call y devolvió texto («Primero, vamos a contar los cafés de especialidad…»)
  sin completar el segundo paso. El banco lo declara explícitamente aceptable
  («la segunda llamada se comprobaría en un turno siguiente (no exigido aquí)») → la limitación
  es del banco, y la terna la hace visible en lugar de dejarla implícita.
- **(C) Acierto de formato con fallo de contenido.** `json-numeros-es` tiene 0 tool calls y JSON limpio:
  sin el eje de contenido, el 87,5 % se leería como «fallo de JSON», que no es el caso.

## 3. CONSTRAINTS — ¿dentro de qué límites?

- **Latencia por caso (s):** `[90,81, 2,35, 0,72, 1,05, 0,58, 1,00, 1,09, 1,21]`.
  El primer caso (`json-plano`, 90,81 s) **incluye la carga del modelo en frío**; los 7 siguientes
  van de 0,58 a 2,35 s. Sin el arranque (n=7): media **1,14 s**, p50 **1,05 s**, máximo **2,35 s**.
- **Coste:** **0 €** — inferencia 100 % local (Ollama en la propia máquina), 0 llamadas a la nube.
  El coste marginal aquí es energía, no dinero.
- **Recursos GPU** (RTX A2000 12 GB, `power.limit` 70,00 W, medido con `nvidia-smi`):
  reposo **1404 MiB / 8,78 W** → durante la corrida **6221 MiB / 68,84 W**.
  Deltas: **VRAM +4.817 MiB (4,70 GB)**, **potencia +60,06 W**, pico al **98,3 % del límite**.
- **Energía:** ≈**1,89 Wh** en los 98,8 s de cómputo a 68,84 W; reposo ≈0,24 Wh →
  **≈1,65 Wh por corrida completa**.
- **Presupuesto de contexto:** `num_ctx = 8192` explícito (en Ollama, no fijarlo lleva a 131072 →
  desborda a CPU).
- **Seguridad:** el instrumento **no ejecuta herramientas ni escribe ficheros** (verificado por grep:
  sin `subprocess`/`os.system`/`eval`/`exec`/escritura); solo habla con `127.0.0.1:11434`.
- **Límites de la medición (RULE-015):** la potencia se muestreó con `nvidia-smi` **antes y después**,
  no integrada durante la corrida → 68,84 W es una **muestra puntual**, no la media; la energía es
  una **estimación** a potencia constante; **no** cubre CPU, RAM, discos, ventiladores ni pérdidas
  de la fuente. Los contadores `intel-rapl` existen pero `energy_uj` es 0400 root → **no leídos**
  (frontera de privilegios, pendiente del hueco 3).

## 4. VEREDICTO

`outcome` 7/8 con trayectoria limpia donde se midió (3/3 nombres correctos, 0 reintentos) **y** un
argumento de esquema inválido que el corrector no comprueba; `constraints` medidos en GPU/latencia y
**no medidos** en CPU/disco/pared. La evaluación queda cerrada **con la terna**, sin declarar bueno
lo que solo lo es en el eje del resultado.

## 5. Anexo para el ledger (propuesta, NO aplicada)

```json
"trayectoria": {"casos": 8, "tool_calls_total": 3, "nombres_correctos": 3,
                "argumentos_con_claves_invalidas": 1, "reintentos": 0, "thinking_chars": 0},
"constraints": {"latencia_s": {"total": 98.8, "p50_sin_arranque": 1.05, "max_sin_arranque": 2.35},
                "coste_eur": 0.0, "vram_delta_mib": 4817, "potencia_pico_w": 68.84,
                "energia_wh_estimada": 1.65, "contexto_tokens": 8192,
                "límites_de_medicion": "potencia muestreada antes/después, no integrada; sin CPU/disco/pared"}
```

**No aplicado**: añadir campos al esquema de `aplicabilidad_ledger.jsonl` es la decisión siguiente
(generalizar o limitar a evaluaciones de agentes). El ledger no se ha tocado.

## 6. Reproducir

```bash
cd /home/jokoalmi/joko-lab
/usr/bin/python3 tools/evaluar_json_tool_calling_v2.py \
  --bateria tools/bateria_json_tool_calling.json \
  --modelo qwen2.5:7b --backend ollama --num-ctx 8192 --json
```

Evidencia cruda de esta corrida: `/tmp/h2_eval.json`, `/tmp/h2_eval.err`, `/tmp/h2_gpu_pre.txt`,
`/tmp/h2_gpu_post.txt` (temporales; el contenido está transcrito arriba).

---

## Anexo (2026-10-11, 14:14:07–14:17:32 CEST) — corridas de confirmación

El mismo instrumento con el mismo set (sha256 `30557a9df6ee2fca82f3a823ed8e5dea20baa56ebc21d00c7b6f51f011493080`)
se volvió a ejecutar 3 veces (modelo `qwen2.5:7b` ya cargado en Ollama, `num_ctx=8192`):

- **Outcome estable: 7/8 las tres veces**, y el mismo fallo: `json-numeros-es`, esperado **2520**,
  obtenido **2512** las tres veces → **fallo determinista de contenido**, no ruido de muestreo.
- **Duración:** 7,6 s / 7,5 s / 7,6 s, frente a **98,8 s** de la primera corrida → el arranque en
  frío cuesta **~13×** la duración; el eje de constraints debe declarar siempre el régimen.
- **Trayectoria NO estable:** en `tool-dos-pasos` la 1ª corrida hizo **1** tool call; las tres de
  confirmación hicieron **2** (`contar_cafes`, `ultimo_cafe`) → la trayectoria se declara **por
  corrida**, nunca como propiedad fija del modelo.
- Latencias en caliente: `[0.69, 2.21, 0.60, 0.96, 0.46, 0.79, 0.95, 0.88]` s → media **0,94 s**,
  máximo 2,21 s.
- Energía GPU de una pasada en caliente (2 pasadas medidas por el instrumento `consumo-electrico`):
  **≈0,13–0,14 Wh**; en régimen sostenido la GPU va a **65,94 W de media / 68,75 W de pico**.
