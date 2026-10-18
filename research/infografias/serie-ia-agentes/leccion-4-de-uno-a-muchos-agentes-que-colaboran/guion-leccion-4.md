# Lección 4 · «De uno a muchos: agentes que colaboran»

Serie **«IA y agentes, de cero a producción»** — pieza 7 (nivel 4). Formato: documento PDF
(7 slides 1080×1350) + texto para LinkedIn. Cadencia lunes / miércoles / viernes.

- Contenido del nivel: `research/analisis-techyybanda-ai-agents-20260914.md`, bloque
  «NIVEL 4 · DE UNO A MUCHOS» (subniveles 4.1 a 4.5). No se inventa contenido: se
  desarrolla lo que fija el plan y se mide la métrica que fija el plan.
- Estado: `seguimiento.json` → pieza `L4`.
- Fecha de trabajo: 2026-09-27 (publicación prevista: lunes 2026-09-28).

## 1. Qué dice el plan

- **4.1 Qué es.** Varios agentes con roles (o un workflow con pasos fijos) repartiéndose el trabajo.
- **4.2 Cómo funciona.** Patrones: secuencial, paralelo (fan-out / fan-in), supervisor.
  Mensajes entre agentes + estado compartido. Agentic RAG: el que reformula y vuelve a buscar.
- **4.3 Confusión típica.** Workflow con pasos fijos vs multi-agente real; «varios prompts en
  cadena» vs agentes con estado y decisión; RAG vs RAG agéntico.
- **4.4 Ejemplo real.** El que escribe + el que revisa + el que verifica.
- **4.5 Dato medible.** **Coste y latencia multi-agente vs un solo agente; número de reintentos;
  mejora de precisión al añadir el crítico.** ← la métrica que se mide aquí.

## 2. Hipótesis (escrita antes de medir)

«Añadir un crítico independiente al agente que ya trabaja solo hace que el conjunto cierre más
tareas. El precio se paga en tokens y en tiempo: más llamadas, más latencia y algún reintento.»

Lo que se va a comprobar es el INTERCAMBIO: si la precisión sube y cuánto cuesta. Si el crítico no
rescata ninguna tarea, el eje de la pieza no será «colaborar mejora» sino «colaborar cuesta», y el
guion se reescribe con eso.

## 3. Diseño de la medición

- Instrumento: `medicion-multiagente.py` (mismo mundo y mismas 6 tareas que la lección 3, para que
  la cifra sea comparable con la pieza anterior).
- Modelo: **ibm/granite4.2:8b-q4_K_M** en Ollama local (`http://127.0.0.1:11434`), temperatura 0,
  `num_ctx` 8192, seed 42. Una pasada por celda.
- Mundo: 12 pedidos ficticios con herramientas (`listar`, `buscar`, `sumar`, `detalle`).
  **No son datos del LAB**: es un mundo de juguete reproducible.
- **A · un solo agente**: un agente con herramientas (ReAct) hasta 6 pasos. Cierra cuando dice `fin`.
- **B · multi-agente con crítico**: el mismo agente, y después un **crítico independiente** que
  recibe la tarea y la respuesta (no el razonamiento), tiene las mismas herramientas para comprobar
  el dato real y devuelve veredicto + motivo. Si el veredicto es «incorrecto», el agente recibe el
  motivo y dispone de **un** reintento.
- **B incluye el coste de A** (el crítico trabaja sobre la respuesta de A): así se mide el añadido,
  no dos experimentos distintos.
- Juez objetivo: acierto de número y de texto contra el dato calculado del mundo.
- Métricas: tareas cerradas, tokens (prompt + generados), segundos, pasos, llamadas a herramienta,
  reintentos disparados y veredicto del crítico.

**Lectura del instrumento (RULE-015, antes de dar la cifra por buena):** el eje «precisión» solo
se sostiene si B rescata tareas que A falla. Si B no rescata nada y solo añade coste, se publica el
intercambio real. Se declaran los límites: una sola pasada por celda; 6 tareas; un solo modelo.

## 4. Resultado

Medición ejecutada el 27-sep-2026 (22:32 – 23:08). Crudo: `medicion-multiagente-20260927.json`.

- **A · un solo agente:** 6/6 cerradas · **22.121 tokens** · **537 s** (8,9 min) · 2,33 llamadas al
  modelo por tarea · 1,33 llamadas a herramienta por tarea.
- **B · mismo agente + crítico** (su coste incluye el de A): 6/6 · **86.256 tokens** · **2.515 s**
  (41,9 min) · 5,00 llamadas por tarea · 2,67 herramientas por tarea · 1 reintento disparado.
- **Diferencia: ×3,90 en tokens y ×4,68 en tiempo. Tareas rescatadas por el crítico: 0.**
  Veredictos del crítico: 5 «ok» + 1 «incorrecto».
- **El único reintento (T6):** el crítico marcó «incorrecto» una respuesta **correcta** (falso
  negativo). A: 6.530 tokens / 163 s → B: 35.633 tokens / 1.114 s (8 pasos). **La misma respuesta**,
  ×5,5 de coste y ×6,8 de tiempo.
- **Lectura del instrumento (RULE-015):** la hipótesis escrita en §2 («el crítico cierra más tareas»)
  **no se sostiene** con estos datos. El eje de la pieza es **«colaborar cuesta»**: mismo resultado,
  la factura multiplicada. Se declara que con tareas más duras —o con un modelo que falle— la
  pregunta vuelve a estar abierta.

Crudo: `medicion-multiagente-20260927.json`.

## 5. Escalera de las 7 slides

1. Portada — «De uno a muchos» (pieza 7).
2. Qué es (4.1) — varios roles, un trabajo.
3. Cómo funciona (4.2) — secuencial, paralelo, supervisor; mensajes y estado compartido.
4. Confusión típica (4.3) — workflow ≠ multi-agente; cadena ≠ agentes; RAG ≠ RAG agéntico.
5. Ejemplo real (4.4) — el que escribe + el que revisa, con la medición.
6. Dato medible (4.5) — coste y latencia de A vs B, con pie de método y fecha.
7. Cierre — resumen en 3 puntos + gancho a la lección 5 («Producción: fiabilidad, coste y límites»).

## 6. Límites declarados

- Una sola pasada por tarea y condición (no es una ley del modelo, es una medición con fecha).
- 6 tareas sintéticas de varios pasos, un único modelo local de 8B.
- El coste se publica en **tokens**, no en euros: es un modelo local y no hay factura de API.
- El crítico es un rol de prompt, no un modelo distinto: se dice tal cual en la pieza.
