---
title: "Curso IA y agentes — Lección 2: El modelo conectado al mundo (datos y herramientas)"
type: guion-infografia
serie: ia-agentes (6 niveles · de lo básico a lo avanzado)
leccion: 2 (primera pieza del nivel 2 · pieza 5 de la serie)
estado: guion v2 (medición ejecutada el 22-sep-2026; pendiente arte y render)
created: 2026-09-22
---

# LECCIÓN 2 — El modelo conectado al mundo: datos y herramientas

**Serie:** curso divulgativo de IA y agentes (NO del LAB). Cada pieza termina con un gancho a la siguiente.
**Plan completo:** `research/analisis-techyybanda-ai-agents-20260914.md` (secciones «CLASIFICACIÓN POR NIVELES» y «SUBNIVELES POR NIVEL», nivel 2).
**Escalera didáctica:** qué es → cómo funciona → confusión típica → ejemplo real → dato medible → cierre con gancho.
**Regla de la pieza (corregida por la medición):** conectar el modelo son **dos cosas distintas** (tus datos por RAG / tus acciones por herramientas). Y la confusión típica es mezclar cuatro nombres para tres cosas y un estándar. El dato medible **no** dice que el modelo no sepa calcular: dice que **acierta cuando le das los datos, y cuando no los tiene responde «0» sin avisar**; con la herramienta declarada el número sale de tu código.

## TEXTO DE LAS SLIDES (exacto, para maquetar)

**S1 · Portada**
- Título: `CONECTADO AL MUNDO`
- Subtítulo: `Tus datos y tus acciones: dos formas de que deje de adivinar`
- Pie: `6 LECCIONES · DE LO BÁSICO A LO AVANZADO` / `LECCIÓN 2 · PIEZA 5`
- Arte: `arte/s1-puente.png` (puente pequeño de madera salvando un hueco)

**S2 · Qué es (1/5)** — dos formas de conectar
- Titular: `DOS FORMAS, NO UNA`
- Arte: `arte/s2-libro-llave.png` (libro abierto con una llave pequeña encima)
- Dos fichas:
  - `TUS DATOS (RAG) — el modelo consulta antes de responder: tus documentos, tus facturas, tus notas.`
  - `TUS ACCIONES (HERRAMIENTAS) — el modelo pide que ejecutes algo: una búsqueda, una suma, crear un evento.`
- Caja: `En los dos casos el modelo deja de adivinar: en uno porque lee, en el otro porque delega. Lo que NO hace en ninguno de los dos es aprender: eso es otra cosa (fine-tuning).`

**S3 · Cómo funciona (2/5)** — los dos caminos, paso a paso
- Titular: `DOS CAMINOS DISTINTOS`
- Camino 1 (RAG):
  - `1. Trocear tus documentos en fragmentos pequeños.`
  - `2. Convertir cada fragmento en vectores (embeddings) y guardarlos.`
  - `3. Buscar por similitud los fragmentos que encajan con la pregunta.`
  - `4. Meter esos fragmentos en el prompt: el modelo responde leyéndolos.`
- Camino 2 (herramientas):
  - `1. Le declaras qué funciones existen y qué necesitan.`
  - `2. El modelo devuelve una llamada estructurada: nombre + argumentos.`
  - `3. Tu código la ejecuta de verdad (aquí sí se calcula).`
  - `4. El resultado vuelve al modelo, que redacta la respuesta final.`
- Caja: `El modelo no ejecuta nada: pide. El que ejecuta es tu código, y por eso el resultado es verificable. El «razonar antes de responder» (CoT) es un tercer truco, pero no conecta con nada: solo ordena el razonamiento.`

**S4 · Confusión típica (3/5)** — cuatro nombres, tres cosas y un estándar
- Titular: `CUATRO NOMBRES, TRES COSAS`
- Tabla:
  - `HERRAMIENTAS (tools)` = la capacidad: funciones que le declaras.
  - `TOOL CALLING / FUNCTION CALLING` = el mecanismo: cómo las pide (dos nombres, lo mismo).
  - `MCP` = el estándar: un enchufe común para no reescribir la integración en cada sitio.
- Columna ✗: `«RAG es lo mismo que fine-tuning.»` / `«Si le doy mis datos, el modelo los aprende.»`
- Columna ✓: `RAG = memoria consultable: se actualiza sin reentrenar y se puede citar la fuente.` / `Fine-tuning = cambia cómo se comporta (tono, formato, tarea), no es una base de datos.`
- Caja: `La prueba rápida: si te importa qué fuente lo dice y que esté al día, es RAG. Si te importa que responda con tu formato y tu tono, es fine-tuning.`

**S5 · Ejemplo real (4/5)** — corregido por el dato
- Titular: `NO SABE, Y NO TE LO DICE`
- Arte: `arte/s5-calculadora-recibos.png` (calculadora pequeña junto a un taco de recibos)
- Dos columnas:
  - `✗ SIN LOS DATOS (6/6) → se le pide el total de luz sin darle la tabla. Respuesta literal, las seis veces: 0. Ni un «no lo sé»: un cero con el mismo tono seguro.`
  - `✓ CON LOS DATOS (6/6) → con la tabla delante acierta los seis totales (1302,25 el de luz), pero el número sale de su aritmética: no hay nada que auditar.`
- Caja: `Con datos acierta y sin datos se lo inventa, y las dos respuestas suenan igual de firmes. Eso es lo que resuelve la herramienta: el número sale de tu código, no de su memoria.`

**S6 · Dato medible (5/5)** — MEDICIÓN HECHA (22-sep-2026)
- Titular: `6/6 LLAMADAS BIEN FORMADAS`
- Dato grande: `6/6`
- Sub: `Mismo modelo, mismas 6 preguntas, temperatura 0. Sin los datos: 6/6 respuestas «0». Con la tabla delante: 6/6 aciertos calculando él. Con la función declarada: 6/6 llamadas bien formadas y ejecutables, y el número lo devuelve el código. Control con la temperatura a 0,8: 6/6 también.`
- Caja: `Lo que separa una respuesta plausible de una verificable no es el acierto: es de dónde sale el número. Declararle la herramienta no lo hace más listo; lo hace auditable.`
- Pie de método: `MEDICIÓN PROPIA · IBM/GRANITE4.2:8B EN OLLAMA (LOCAL) · N=6 POR CONDICIÓN, UNA PASADA · 22-SEP-2026`

**S7 · Cierre**
- `En 1 minuto: (1) Conectar el modelo son dos cosas: tus datos (RAG) y tus acciones (herramientas). (2) Con datos consulta; con herramientas delega: el que calcula es tu código. (3) Herramientas, tool calling y MCP no son lo mismo: capacidad, mecanismo y estándar.`
- Arte: `arte/s7-candado.png` (candado abierto con una llave al lado)
- Gancho: `Siguiente · Lección 3 — El agente: el bucle.`

## DATOS (medición de esta pieza — EJECUTADA)

- **Fecha de la medición:** 22-sep-2026, 19:22 CEST (estampa del JSON).
- **Modelo:** `ibm/granite4.2:8b-q4_K_M` en Ollama (local), `num_ctx` 8192, seed 42.
- **Tanda:** 6 preguntas sobre un fichero de gastos de ejemplo (8 filas, importes con céntimos), **calculadas de forma independiente en Python** (tareas esperadas: marzo 2091,40 · abril 3417,80 · mayo 3360,95 · luz 1302,25 · material 7152,10 · transporte 415,80).
- **Condición A** (los datos en el prompt, sin herramienta; se le pide el número): **6/6 números exactos**. Literal de la primera: `1302.25`.
- **Condición S** (la misma pregunta **sin los datos** y sin herramienta): **0/6 exactos y 6/6 respondió con un número**. Literal, las seis veces: `0`. No dijo «no lo sé» en ningún caso.
- **Condición B** (los datos + la función `sumar_gastos` declarada, temperatura 0; se le pide la llamada): **6/6 llamadas bien formadas y 6/6 con argumentos correctos**. Literal de la primera: `{"herramienta": "sumar_gastos", "argumentos": {"filtro": "concepto", "valor": "luz"}}` → la ejecuta el código → `1302.25`.
- **Condición C** (control: B con la temperatura a 0,8): **6/6 bien formadas y correctas**. El formato aguanta la temperatura.
- **LÍMITES DECLARADOS (van en la pieza):** n=6 por condición y **una sola pasada** (no es una ley, es una prueba); en S la instrucción pedía «responde SOLO con el número», así que el 0 es también un efecto del formato exigido (el modelo no tuvo la opción de explicarse) — se declara en la slide; A acierta con esta tanda de 8 filas (no se ha medido con volúmenes mayores y **no se afirma** nada sobre ellos).
- **Crudo:** `medicion-herramientas-20260922.json` (24 filas con las respuestas literales). **Script:** `medicion-herramientas.py`.
- **Dato de apoyo ya medido (14-sep-2026):** batería de JSON estricto + tool calling `tools/evaluar_json_tool_calling.py` sobre el mismo modelo: **6/8 sin razonamiento en 10,5 s** y **8/8 con razonamiento en 98,9 s**; tool calling **3/3**. Fuente: `04-operations/metrics/modelos-locales/2026-09-14-prueba-granite-4.2-8b.md`. Es apoyo: la slide 6 va con la medición de ESTA pieza.
- **Sin verificar (no se publica):** ninguna cifra de mercado, ningún modelo comercial, ninguna comparación con servicios de pago.

## FORMATO
Estilo fijado de la serie (L0 / L0-A / L0-B / L1): paneles claros estilo MAURYS, 1080×1350, 7 slides, PDF como documento en LinkedIn. Arte SDXL para escenas; diagramas en SVG dentro del HTML.

## HISTORIAL
- 2026-09-22 · v1: guion base de la lección 2 (los 5 subniveles del plan del nivel 2); medición diseñada y pendiente, arte pendiente.
- 2026-09-22 · v2: medición ejecutada (24 llamadas, 4 condiciones). Se **corrige el titular** de la pieza: el dato no respalda «el modelo no suma» (A acertó 6/6 con los datos delante); el eje real medido es «con datos acierta / sin datos inventa un 0 / con la herramienta el número sale del código». Titulares de S5 y S6 reescritos con el dato.
