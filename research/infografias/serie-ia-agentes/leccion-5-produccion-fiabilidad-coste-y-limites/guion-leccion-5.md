# Lección 5 · «Producción: fiabilidad, coste y límites»

Serie **«IA y agentes, de cero a producción»** — pieza 8 (nivel 5, **última del plan de
niveles**). Formato: documento PDF (7 slides 1080×1350) + texto para LinkedIn. Cadencia
lunes / miércoles / viernes.

- Contenido del nivel: `research/analisis-techyybanda-ai-agents-20260914.md`, bloque
  «NIVEL 5 · PRODUCCIÓN: FIABILIDAD, COSTE Y LÍMITES» (subniveles 5.1 a 5.5). No se
  inventa contenido: se desarrolla lo que fija el plan y se mide la métrica que fija el plan.
- Estado: `seguimiento.json` → pieza `L5`.
- Fecha de trabajo: 2026-09-30 (publicación prevista: viernes 2026-10-02).

## 1. Qué dice el plan

- **5.1 Qué es.** Mantener agentes fiables: medir, verificar, limitar permisos y controlar el gasto.
- **5.2 Cómo funciona.** Evals con golden set, verificación de salidas (citas, JSON válido),
  permisos mínimos, observabilidad (traza) y límites de coste.
- **5.3 Confusión típica.** «Si funciona en la demo, funciona»; y creer que alucinar es cosa de
  modelos malos: es estadística, se mide.
- **5.4 Ejemplo real.** La batería de casos trampa (preguntas cuya respuesta correcta es no inventar).
- **5.5 Dato medible.** **Tasa de alucinación (%)**; el plan añade también coste por 1.000 consultas
  y latencia percentil 95. ← Aquí se publica la **tasa de alucinación**, que es la métrica que el
  plan declara como ya medida.

### Corrección al plan (dato del plan ≠ dato del crudo)

El plan dice: «batería de **81 casos** trampa» y «**0 de 81** alucinaciones en modo directo
(14-sep-2026; con razonamiento la tasa bruta fue 9,9 % y real 1,2 %)». Comprobado contra el
instrumento y el ledger:

- `tools/golden_set_alucinaciones.json` tiene **27 casos**, no 81 (6 de contexto, 2 de contexto
  ausente, 6 de memoria, 8 de trampa, 4 de ficha y 1 de ficha ausente).
- El ledger `04-operations/metrics/alucinaciones_ledger.jsonl` registra el 14-sep-2026 con
  `ibm/granite4.2:8b-q4_K_M`: **3 pasadas con el razonamiento desactivado a 0,0 %** de alucinación
  global y honestidad 1,0 (seeds 42/43/44); y 4 pasadas con razonamiento a **3,7 % / 11,1 % /
  14,8 % / 3,7 %**.
- La cifra «81» coincide con 27 casos × 3 pasadas = **81 respuestas**: lo más probable es que el
  plan confundiera respuestas con casos. El par «9,9 % / 1,2 %» **no aparece** en el crudo.

→ **No se publican ni el 81 ni el 9,9 %/1,2 %.** El fichero del plan queda pendiente de corrección
(es escritura en `research/`: necesita OK aparte).

## 2. Hipótesis (escrita antes de leer el crudo)

«Con la misma batería, el modelo que acierta en las preguntas normales no inventará en las
trampas: la tasa de alucinación será 0 en el modo directo. Con el razonamiento largo activado
espero una tasa algo peor —razona más, escribe más, tiene más ocasiones de rellenar huecos— pero
pequeña.»

## 3. Diseño de la medición (lo que existe, no lo que me gustaría)

- **Instrumento:** `tools/evaluar_alucinaciones.py` (batería) + `tools/juez_alucinaciones.py` (recuento).
- **Batería:** `tools/golden_set_alucinaciones.json`, 27 casos con respuesta conocida, trampas incluidas.
- **Condiciones:** `ibm/granite4.2:8b-q4_K_M` en Ollama (local), temperatura 0,2, `num_ctx` 8192,
  `max_tokens` 2000; **dos condiciones** (razonamiento desactivado / por defecto) × 3 seeds (42/43/44).
- **Métrica:** tasa de alucinación global = casos etiquetados ALUCINACION / total; y tasa de
  honestidad = abstención correcta en los casos que no tienen respuesta.
- **Crudo:** `medicion-alucinaciones-20260914.json` (literal, 7 pasadas con sus 27 respuestas cada una).
- **No se ejecuta medición nueva** (decisión del usuario, 30-sep-2026): se cita la medición propia
  del 14-sep-2026 con su crudo literal. No se gasta GPU en medir.

## 4. Resultado (leído del crudo, respuesta a respuesta)

- **Modo directo (razonamiento desactivado): 0 de 27 invenciones en las 3 pasadas** (seeds 42/43/44),
  con 16 aciertos + 11 abstenciones correctas en cada pasada y honestidad 1,0. La primera parte de la
  hipótesis se sostiene.
- **Modo con razonamiento: 3,7 % / 11,1 % / 14,8 % (y 3,7 %)** según la pasada. La segunda parte
  también… **pero al leer las respuestas literales una a una, las «alucinaciones» que cuenta el
  contador son rechazos honestos mal etiquetados**: «Aún no ha habido ningún astronauta que haya
  pisado Marte» aparece contada como invención, igual que «OpenAI no presentó un modelo llamado
  Nebula-X». La pasada de las 13:29 ya está marcada como `invalidada` en el ledger con ese motivo.
- **Consecuencia:** la tasa bruta del modo con razonamiento **no se publica como fallo del modelo**
  (sería publicar un artefacto del medidor). Lo que se publica es **0/27 en directo** + el **límite
  del medidor**, que pasa a ser el contenido de la slide 6 — y encaja con el nivel: fiabilidad y límites.
- **Hallazgo secundario (límite de diseño del caso):** en las trampas que exigen «responde solo con el
  número», el propio formato **impide abstenerse**: el modelo devuelve «0 %» en vez de decir que no lo
  sabe. Se declara como límite del caso, no como fallo del modelo.

## 5. Escalera de las 7 slides

1. **Portada.** «A PRODUCCIÓN» · Fiabilidad, coste y límites: la demo no es la prueba. Pie: 6 LECCIONES · LECCIÓN 5 · PIEZA 8. Arte: balanza de hojalata.
2. **Qué es (5.1).** «MEDIR, VERIFICAR, LIMITAR» — cuatro piezas: la medida, la comprobación, los permisos, el techo de gasto. Arte: fichero de fichas.
3. **Cómo funciona (5.2).** «CINCO PIEZAS, UN SISTEMA» — casos de prueba, salida verificable, permisos mínimos, traza, techo de gasto. Caja: son controles, no inteligencia.
4. **Confusión típica (5.3).** «SI FUNCIONA EN LA DEMO, FUNCIONA» — tabla de tres frases hechas vs lo que pasa + par ✗/✓ + caja: la pregunta útil es cuánto falla y cuánto cuesta cada fallo.
5. **Ejemplo real (5.4).** «LA PREGUNTA QUE NO TIENE RESPUESTA» — caso normal vs caso trampa; la trampa se elige a mano. Arte: imán.
6. **Dato medible (5.5).** «0 VECES SE LO INVENTÓ» — **0/27** en 3 pasadas (16 aciertos + 11 abstenciones por pasada) + caja con el límite del medidor + pie de método (modelo, condiciones, fecha).
7. **Cierre.** «EN 1 MINUTO» — tres ideas, arte (candado) y bloque final: **FIN DEL RECORRIDO · 5 LECCIONES** (no se anuncia nivel siguiente: no existe).

## 6. Límites declarados

- Vale para **este modelo, estas condiciones y esta batería de 27 casos**: no dice «el modelo no alucina».
- El **contador automático no es neutral** (arriba, con ejemplos literales): quien mide tiene que auditar su medida.
- `n` = 27 casos por pasada × 3 pasadas por condición.
- **No medido y por tanto NO publicado:** coste por 1.000 consultas y latencia p95, que el plan menciona en 5.5.
- El contenido de los casos de la batería (que cita el catálogo interno) **no se publica**: solo la tasa y el método.

## 7. Pendientes de esta pieza

- Corregir el bloque del nivel 5 en `research/analisis-techyybanda-ai-agents-20260914.md` (81 → 27 casos; quitar 9,9 %/1,2 %) → requiere OK, es escritura.
- Decidir la continuación de la serie: el plan de niveles se agota en esta pieza (desglose de subniveles 5.x o etapa nueva).
- Medir coste por 1.000 consultas y latencia p95 si se quieren publicar en una pieza futura.
