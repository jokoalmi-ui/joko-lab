# TEXTO DEL POST — LECCIÓN 5 (nivel 5, pieza 8 de la serie)

Título del documento (propuesta, ver notas): Cómo saber si tu IA se inventa las cosas

---

**Texto de la publicación (pegar tal cual):**

Le pedí a mi IA local que me contara cuándo presentó OpenAI su modelo «Nebula-X». No existe. Y contestó bien: que no lo sabía. Cero invenciones en 27 preguntas, once de ellas imposibles de contestar.

Lo interesante no es eso.

Lo interesante es lo que pasó cuando fui a contarlas automáticamente: mi propio contador había marcado como «alucinación» frases que eran rechazos honestos. «Aún no ha habido ningún astronauta que haya pisado Marte» contaba como invención. El fallo no estaba en el modelo: estaba en mi forma de medirlo.

Esta es la lección 5 y última de la serie «IA y agentes, de cero a producción». Sacar un agente de la demo no es hacerlo más listo: es medirlo, verificarlo y ponerle límites. Cuatro cosas lo sostienen:

· Una batería de casos con respuesta conocida, trampas incluidas. Tres pruebas sueltas no son una muestra.
· Salidas que se verifiquen solas: una cita, un JSON que valida, un número que se recalcula. Lo que no se comprueba, no se sabe.
· Permisos mínimos: que el agente haga solo lo que necesita. Un borrado no se deshace.
· Un techo de gasto por tarea y por día: al llegar, el agente para en vez de seguir.

Y la regla que me llevo de esta medición: desconfía de tu propio medidor. El fallo lo encontré en mi contador, no en el modelo.

Un agente fiable no es el que nunca falla. Es el que falla donde tú lo puedes ver, y a un precio que aceptaste antes.

¿Tú cómo compruebas que tu IA no se inventa lo que te dice?

#IA #AgentesIA #IAenProducción #LLM #Automatización
---

## Notas para publicar (no se publican)

- Texto listo para pegar: `post-linkedin.txt` (solo el bloque publicable), generado con `extraer_post.py`. NO pegar este .md entero.
- Archivo a subir: `carrusel-leccion-5.pdf` (7 páginas, 1080x1350) como **documento**, NO los PNG sueltos.
- Título del documento: **no consta** en `seguimiento.json` para esta pieza. Propuesta: «Cómo saber si tu IA se inventa las cosas» (elegida por lo que la gente teclea). Alternativa literal: «Producción: fiabilidad, coste y límites».
- Dato de la slide 6: medición propia (14-sep-2026) con granite4.2:8b-q4_K_M en Ollama (local), num_ctx 8192, temperatura 0,2, razonamiento desactivado, 27 casos x 3 pasadas (seeds 42/43/44): 0 de 27 invenciones. Crudo: `medicion-alucinaciones-20260914.json` (84 KB, 7 pasadas literales).
- Límite declarado (va en la slide): el contador automático del propio instrumento marcó rechazos honestos como invenciones, así que la tasa bruta de las pasadas con razonamiento (3,7 %–14,8 %) es artefacto del medidor y NO se publica como fallo del modelo; una de esas pasadas quedó invalidada en el registro. Coste por 1.000 consultas y latencia p95: no medidos, no se publican.
- Verificación visual: hecha con glm-4.6v-flash (LM Studio, contexto 8192), 7/7 SIN DEFECTOS y control de lectura transcrito (portada, método de la slide 6 y cierre), 30-sep-2026 en `seguimiento.json`.
- Registro: `python3 serie_estado.py publicar L5 --url <url-del-post>`; si el enlace no se puede copiar, se registra con fecha y url nula.
- Gancho de la siguiente pieza: **no hay**. El plan de niveles se agota en L5; la continuación (desglose de los subniveles 5.x o etapa nueva) está pendiente de decisión.
