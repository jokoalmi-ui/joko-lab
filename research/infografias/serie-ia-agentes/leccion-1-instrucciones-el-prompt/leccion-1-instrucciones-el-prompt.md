---
title: "Curso IA y agentes — Lección 1: Instrucciones: el prompt"
type: guion-infografia
serie: ia-agentes (6 niveles · de lo básico a lo avanzado)
leccion: 1 (primera pieza del nivel 1 · pieza 4 de la serie)
estado: guion (v2, con la medición hecha)
created: 2026-09-20
---

# LECCIÓN 1 — Instrucciones: el prompt

**Serie:** curso divulgativo de IA y agentes (NO del LAB). Cada pieza termina con un gancho a la siguiente.
**Plan completo:** `research/analisis-techyybanda-ai-agents-20260914.md` (secciones «CLASIFICACIÓN POR NIVELES» y «SUBNIVELES POR NIVEL», nivel 1).
**Escalera didáctica:** qué es → cómo funciona → confusión típica → ejemplo real → dato medible → cierre con gancho.
**Regla de la pieza:** el prompt se presenta como **tres cosas concretas** (tarea, formato, rol), no como una fórmula mágica. El dato medible es propio y **corrige el mito**: el formato no mejora los aciertos, mejora el uso.

## TEXTO DE LAS SLIDES (exacto, para maquetar)

**S1 · Portada**
- Título: `LA INSTRUCCIÓN`
- Subtítulo: `Tarea, formato y rol: las tres cosas que cambian la respuesta`
- Pie: `6 LECCIONES · DE LO BÁSICO A LO AVANZADO` / `LECCIÓN 1 · PIEZA 4`
- Arte: `arte/s1-cartel-flecha.png` (cartel de madera con flecha, panel en blanco)

**S2 · Qué es (1/5)** — las tres piezas de una instrucción
- Titular: `TRES COSAS, NO UNA`
- Arte: `arte/s2-tres-piezas.png` (tres piezas de madera encajando, como un puzle)
- Tres fichas:
  - `TAREA — qué quieres que haga: «clasifica estas reseñas».`
  - `FORMATO — cómo quieres la salida: «una línea por reseña: POSITIVA o NEGATIVA».`
  - `ROL — desde dónde lo hace: «eres un revisor de producto».`
- Caja: `Si falta la tarea, no sabe qué hacer. Si falta el formato, acierta pero no te sirve para pegarlo en otro sitio. El rol no es obligatorio: cambia el tono, no los datos.`

**S3 · Cómo funciona (2/5)** — la instrucción como contexto
- Titular: `LO QUE ESCRIBES CONDICIONA LO QUE SIGUE`
- Pasos:
  - `1. Tu instrucción entra junto al texto y condiciona cada palabra siguiente.` → `NO le pides: que adivine lo que no le has dicho.`
  - `2. Un ejemplo pesa más que una explicación larga.` → `NO le pides: que deduzca un formato que no le has enseñado ni con un ejemplo.`
  - `3. El formato exigido convierte su salida en algo que otro programa puede leer.` → `NO le pides: que sepa qué vas a hacer tú con esa salida.`
  - `4. La temperatura cambia cuánto varía la respuesta, no lo que sabe.` → `NO le pides: que la variedad y el contenido sean lo mismo.`
- Caja: `Casi todo lo que se llama «prompt engineering» es esto: escribir la tarea y el formato. No hay frase mágica; hay instrucción concreta.`

**S4 · Confusión típica (3/5)** — los dos mitos
- SVG de barras: `SIN DECIR EL FORMATO` vs `FORMATO EXIGIDO` → `caracteres de respuesta para la misma tarea: 1.600 vs 228` (medición de esta pieza).
- Columna ✗:
  - `«El truco está en una frase mágica: "eres un experto en…".»`
  - `«Cuanto más larga, mejor.»`
- Columna ✓:
  - `El rol cambia el tono, no los datos: lo que arregla la salida es la tarea y el formato.`
  - `Más texto no es más precisión: cada frase de más diluye la instrucción.`
- Caja: `Y una trampa de al lado: subir la temperatura no hace al modelo «más listo». En nuestra prueba cambió la respuesta —205 caracteres frente a 228— pero mantuvo el formato. La variedad no es conocimiento.`

**S5 · Ejemplo real (4/5)**
- Titular: `LA MISMA PETICIÓN, DOS FORMAS`
- Arte: `arte/s5-dos-formas.png` (una hoja arrugada junto a una tarjeta plana)
- Dos columnas:
  - `SIN DECIR EL FORMATO → «1. POSITIVA, 2. NEGATIVA… Explicación breve (por ítem): la primera reseña habla de…»` · se lee, no se procesa.
  - `FORMATO EXIGIDO → [{"id":1,"sentimiento":"positiva"}, {"id":2,"sentimiento":"negativa"}, …]` · se pega en cualquier sitio y otro programa lo lee.
- Caja: `La diferencia no es que entienda mejor: es que le has dicho dónde cortar. Exigir el formato es la frontera entre un texto que se lee y una salida que se procesa.`

**S6 · Dato medible (5/5)** — PRUEBA REAL (medida 20-sep-2026)
- Titular: `ACERTÓ IGUAL; SIRVIÓ DISTINTO`
- Dato grande: `6/6` · `reseñas clasificadas bien en las tres condiciones — la instrucción vaga acertó tanto como la que exigía JSON`
- Dos columnas (respuesta literal de la misma tanda):
  - ✗ `SIN DECIR EL FORMATO` — `1.600 caracteres · 52,8 s · no se puede leer con código`
  - ✓ `FORMATO EXIGIDO` — `228 caracteres · 30,0 s · JSON válido, listo para usar`
- Caja: regla que se lee → `El formato no arregla los aciertos: arregla el uso. Si la salida la vas a leer tú, la prosa vale. Si la va a leer un programa, exige el formato: es una línea de instrucción.`
- Pie de método: `Medición propia · 20-sep-2026 · ibm/granite4.2:8b-q4_K_M en Ollama · 6 reseñas · temperatura 0 (control a 0,8) · crudo: medicion-formato-20260920.json`

**S7 · Cierre**
- `En 1 minuto: (1) Toda instrucción útil dice la tarea y el formato. (2) Lo que se llama «truco» casi siempre es haber escrito lo que querías. (3) El formato no mejora la respuesta: la hace usable.`
- Arte: `arte/s7-cuaderno.png`
- Gancho: `Siguiente · Lección 2 — El modelo conectado al mundo: datos y herramientas.`

## DATOS
- **Medición de esta pieza (hecha el 20-sep-2026, 21:11):** `medicion-formato-20260920.json`. Modelo `ibm/granite4.2:8b-q4_K_M` (Ollama, `num_ctx` 8192, seed 42), 6 reseñas, misma tanda en las tres condiciones:
  - **A · sin decir el formato** (temp 0): 1.600 caracteres, 52,8 s, **no parseable** — 6 clasificaciones correctas + una explicación por ítem.
  - **B · formato JSON exigido** (temp 0): 228 caracteres, 30,0 s, **JSON válido tal cual** (`json.loads` sin limpiar nada) — 6/6 correctas.
  - **C · formato JSON exigido con temperatura 0,8** (control): 205 caracteres, 37,1 s, **JSON válido** — 6/6 correctas.
  - Lecturas admitidas por el dato: el formato exigido **no cambió los aciertos** (6/6 en las tres) y **sí la usabilidad** (1.600 → 228 caracteres; 0 de 1 frente a 2 de 2 salidas parseables); el formato **aguantó la temperatura alta** en esta única prueba.
  - **Límite declarado:** una sola ejecución por condición (N=1); no es una ley, es una prueba. La condición A se midió una vez.
- **Dato de apoyo (ya medido, 14-sep-2026):** batería JSON estricto + tool calling `tools/evaluar_json_tool_calling.py` sobre `granite4.2:8b-q4_K_M` (Ollama, temperatura 0): **6/8 sin razonamiento en 10,5 s** y **8/8 con razonamiento en 98,9 s**; tool calling **3/3**. Los dos fallos en modo directo fueron de exactitud (una suma y un número escrito en palabras), no de formato. Fuente: `04-operations/metrics/modelos-locales/2026-09-14-prueba-granite-4.2-8b.md`, línea del backlog 1821.
- **Sin verificar (no se publica):** ninguna cifra de mercado, ningún modelo comercial, ninguna comparación con servicios de pago.

## FORMATO
Estilo fijado de la serie (L0 / L0-A / L0-B): paneles claros estilo MAURYS, 1080×1350, 7 slides, PDF como documento en LinkedIn. Arte SDXL para escenas; diagramas en SVG dentro del HTML.

## HISTORIAL
- 2026-09-20 · v1: guion base de la lección 1 (escalera de 5 subniveles del plan del nivel 1); medición diseñada, arte pendiente.
- 2026-09-20 · v2: **medición ejecutada** (`medicion-formato-20260920.json`, tres condiciones) y guion corregido con lo que el dato dice de verdad: aciertos iguales, uso distinto, y el formato **no** se rompió con temperatura alta (el mito original del borrador queda descartado por la prueba propia).
