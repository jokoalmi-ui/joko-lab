---
title: "Curso IA y agentes — Lección 3: El agente (el bucle)"
type: guion-infografia
serie: ia-agentes (6 niveles · de lo básico a lo avanzado)
leccion: 3 (primera pieza del nivel 3 · pieza 6 de la serie)
estado: guion v1 (medición en curso; pendiente arte y render)
created: 2026-09-24
---

# LECCIÓN 3 — El agente: el bucle

**Serie:** curso divulgativo de IA y agentes (NO del LAB). Cada pieza termina con un gancho a la siguiente.
**Plan completo:** `research/analisis-techyybanda-ai-agents-20260914.md` (secciones «CLASIFICACIÓN POR NIVELES» y «SUBNIVELES POR NIVEL», nivel 3).
**Escalera didáctica:** qué es → cómo funciona → confusión típica → ejemplo real → dato medible → cierre con gancho.
**Regla de la pieza:** lo que separa un chatbot de un agente no es el modelo, es **el bucle**. Y el bucle solo sirve si en cada vuelta entra algo de fuera (una herramienta, un dato): pensar más sin mirar el entorno no trae el dato que falta. Eso es lo que se mide aquí.

## TEXTO DE LAS SLIDES (exacto, para maquetar)

**S1 · Portada**
- Título: `EL AGENTE: EL BUCLE`
- Subtítulo: `No le dictas los pasos: le das un objetivo y las llaves`
- Pie: `6 LECCIONES · DE LO BÁSICO A LO AVANZADO` / `LECCIÓN 3 · PIEZA 6`
- Arte: `arte/s1-noria.png` (noria pequeña de feria: da vueltas y vuelve a subir)

**S2 · Qué es (1/5)** — un objetivo, no una lista
- Titular: `UN OBJETIVO, NO UNA LISTA`
- Arte: `arte/s2-caja-herramientas.png` (caja de herramientas pequeña junto a un cuaderno abierto)
- Cuatro fichas:
  - `EL BUCLE — pensar → actuar → observar, y otra vez, hasta cerrar la tarea.`
  - `HERRAMIENTAS — lo que puede hacer de verdad: buscar, sumar, escribir.`
  - `MEMORIA — lo que lleva encima de una vuelta a la siguiente.`
  - `UN OBJETIVO — qué quieres conseguir, no cómo conseguirlo.`
- Caja: `La diferencia con un chatbot no es el modelo: es el bucle. El mismo modelo, en bucle y con herramientas, deja de ser una máquina de respuestas y pasa a intentar una tarea hasta cerrarla… o hasta agotar los pasos que le has dado.`

**S3 · Cómo funciona (2/5)** — los cuatro pasos
- Titular: `CUATRO PASOS, EN BUCLE`
- Pasos:
  - `1. PENSAR — el modelo dice qué necesita; muchas veces, pedir una herramienta.`
  - `2. ACTUAR — tu código ejecuta la acción de verdad: la búsqueda, la suma, el envío.`
  - `3. OBSERVAR — el resultado vuelve al modelo como texto: el dato real, no su recuerdo.`
  - `4. REPETIR — con el dato nuevo vuelve al paso 1; si ya tiene la respuesta, cierra.`
- Caja: `Quién decide cuándo parar es el bucle: un máximo de pasos o el modelo diciendo que ha terminado. Y por eso importa la memoria: en cada vuelta lleva encima lo que ha pasado. Corto plazo = la conversación de esa tarea; largo plazo = lo que se guarda fuera (un fichero, una base de datos) y se vuelve a leer.`

**S4 · Confusión típica (3/5)** — bucle sí, bucle no
- Titular: `BUCLE SÍ, BUCLE NO`
- Tabla:
  - `CoT (cadena de pensamiento) = pensar antes de responder. Una vuelta, sin tocar nada.`
  - `ReAct = pensar, actuar sobre el entorno y mirar el resultado. Varias vueltas.`
  - `CHATBOT vs AGENTE = el chatbot contesta; el agente intenta cerrar una tarea (y puede fallar).`
- Columna ✗: `«Más autonomía = mejor modelo.»` / `«Si el agente piensa más vueltas, acierta más.»`
- Columna ✓: `La autonomía se la da el acceso: sin herramientas el bucle gira sin traer el dato.` / `El bucle con herramientas es lo que cierra tareas de varios pasos… y lo que se puede auditar.`
- Caja: `La prueba rápida: si para terminar hay que mirar algo de fuera (un fichero, una web, una cuenta exacta), necesitas bucle con herramientas. Si solo hay que redactar mejor lo que ya sabes, basta con una vuelta.`

**S5 · Ejemplo real (4/5)** — el precio en tres tiendas
- Titular: `[PENDIENTE: se fija con el dato medido]`
- Arte: `arte/s5-etiquetas-precio.png` (tres etiquetas de precio pequeñas y una libreta)
- Dos columnas:
  - `✗ UNA VUELTA — «busca el precio de este producto en 3 tiendas y hazme una tabla». Sin acceso a las tiendas no tiene los precios: contesta igual de seguro, con números que no son.`
  - `✓ EN BUCLE — consulta la primera tienda, guarda el precio, consulta la segunda, la tercera, y solo entonces monta la tabla. Varias vueltas, y cada número viene de donde se ha leído.`
- Caja: `El bucle no lo hace más listo: lo hace capaz de ir a mirar. Y deja rastro: se puede ver qué preguntó, en qué orden y con qué resultado.`
- [PENDIENTE: cifras exactas de la medición]

**S6 · Dato medible (5/5)** — [PENDIENTE DE MEDIR]
- Titular: `[PENDIENTE]`
- Dato grande: `[PENDIENTE]`
- Sub: `[PENDIENTE]`
- Caja: `[PENDIENTE]`
- Pie de método: `MEDICIÓN PROPIA · IBM/GRANITE4.2:8B EN OLLAMA (LOCAL) · N=6 POR CONDICIÓN, UNA PASADA · 24-SEP-2026`

**S7 · Cierre**
- `En 1 minuto: (1) Un agente es un modelo con un objetivo dentro de un bucle: pensar, actuar, observar, repetir. (2) Lo que lo cambia todo no es el modelo, son las herramientas: el bucle sin acceso no trae el dato que falta. (3) CoT da una vuelta y responde; ReAct da varias y actúa.`
- Arte: `arte/s7-llave-etiqueta.png` (llave pequeña con una etiqueta colgando)
- Gancho: `Siguiente · Lección 4 — De uno a muchos: agentes que colaboran.`

## DATOS (medición de esta pieza — EN CURSO)

- **Fecha:** 24-sep-2026 (estampa del JSON al terminar).
- **Modelo:** `ibm/granite4.2:8b-q4_K_M` en Ollama (local), `num_ctx` 8192, seed 42.
- **Diseño:** 6 tareas que exigen varios pasos y una decisión (comparar, restar, sacar un porcentaje) sobre una tabla de pedidos de ejemplo (8 filas), con los valores de referencia **calculados aparte en Python**. Cuatro condiciones, mismo modelo y mismas tareas:
  - **A · una vuelta, sin herramientas:** se le pide el número final directamente.
  - **D · varias vueltas, sin herramientas:** puede pensar en varios turnos, pero no tiene nada que consultar.
  - **B · bucle + herramientas (ReAct):** 4 herramientas (`listar`, `buscar`, `sumar`, `detalle`); los datos solo llegan por ahí, no están en el prompt.
  - **C · control:** B con la temperatura a 0,8.
- **Lo que se mide (subnivel 3.5 del plan):** % de tareas completadas, pasos por tarea y coste en tokens por tarea resuelta.
- **Crudo:** `medicion-bucle-20260924.json`. **Script:** `medicion-bucle.py`.
- **Sin verificar (no se publica):** ninguna cifra de mercado, ningún modelo comercial, ninguna comparación con servicios de pago.

## FORMATO
Estilo fijado de la serie (L0 / L0-A / L0-B / L1 / L2): paneles claros estilo MAURYS, 1080×1350, 7 slides, PDF como documento en LinkedIn. Arte SDXL para escenas; diagramas en SVG dentro del HTML.

## HISTORIAL
- 2026-09-24 · v1: guion base de la lección 3 (subniveles 3.1–3.4 del plan del nivel 3); medición del bucle en curso, arte pendiente.
