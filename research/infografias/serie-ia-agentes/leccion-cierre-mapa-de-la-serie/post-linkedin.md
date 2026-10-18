# Pieza 9 — «El mapa de la serie» (cierre)

- Serie: «IA y agentes, de cero a producción»
- Pieza 9 de 9 · id `CIERRE` · **no es una lección** (la serie tiene 6 niveles, 0-5): es el mapa que cierra el arco
- Formato: documento PDF, 7 páginas 1080x1350 (estilo de la serie, crema #F5EFE6)
- Objetivo de publicación: lunes 2026-10-05 (cadencia lunes/miércoles/viernes)
- Título del documento (campo de LinkedIn): «El mapa de la serie: 6 niveles y 8 piezas»
- Sin enlaces: en el registro solo L0 tiene URL (la app móvil no deja copiar el enlace) → el texto remite al perfil

## Texto del post

Después de ocho piezas, esta es la que faltaba: el mapa.

«IA y agentes, de cero a producción» está completa. Ocho entregas, seis niveles, una idea por pieza. Y como ya son muchas, he hecho lo que hago con todo lo que crece: un índice.

Cada nivel resuelve un atasco concreto:

· Nivel 0 — Qué es un LLM y qué se le puede pedir. La máquina no busca: genera.
· Nivel 1 — Instrucciones: el prompt. La misma pregunta, pedida de otra forma, da otra respuesta.
· Nivel 2 — El modelo conectado al mundo: tus documentos y tus herramientas.
· Nivel 3 — El agente: el bucle. Contestar no es lo mismo que hacer.
· Nivel 4 — De uno a muchos: varios agentes colaborando. Cuesta ×3,90 en tokens y ×4,68 en tiempo para el mismo acierto (medido, no estimado).
· Nivel 5 — Producción: fiabilidad, coste y límites. El listón lo pone una batería de casos, no una demo.

Tres cosas que me llevo de haberlo escrito:

1. El orden no es decorativo. Casi todos los atascos que veo son una pieza usada sin la anterior.
2. Medir cambia la conversación. La última medición de la serie: 0 invenciones en 81 respuestas (27 casos × 3 pasadas). Y el fallo estaba en mi medidor, no en el modelo.
3. Ninguna pieza pide programar. Piden leerlas en orden.

¿Y por dónde entras tú?

· ¿Aún no sabes qué es un LLM? Nivel 0.
· ¿Ya lo usas y quieres que haga cosas? Niveles 1 y 2.
· ¿Quieres que trabaje solo y sin sustos? Niveles 3, 4 y 5.

La serie queda completa en mi perfil: ocho piezas, de cero a producción.

¿Cuál te falta?

---

## Notas para publicar (no se publican)

- Texto listo para pegar: `post-linkedin.txt` (solo el bloque publicable), generado con `extraer_post.py` (vive en la carpeta de la serie). NO pegar este .md entero.
- Archivo a subir: `carrusel-cierre.pdf` (7 páginas, 1080x1350) como **documento**, NO los PNG sueltos.
- Título del documento (literal, para el campo de LinkedIn): «El mapa de la serie: 6 niveles y 8 piezas».
- Dato de la slide 6: **no hay medición nueva**. Se citan dos mediciones propias ya publicadas y se recalculan del crudo con `verificar_cifras.py`:
  - multiagente 27-sep-2026 (`medicion-multiagente-20260927.json`): 6 tareas × 2 condiciones → x3,90 tokens, x4,68 tiempo, 1 reintento (0 útiles).
  - alucinaciones 14-sep-2026 (`medicion-alucinaciones-20260914.json`): 27 casos × 3 pasadas con razonamiento desactivado → 0 invenciones en 81 respuestas (16 aciertos + 11 abstenciones por pasada).
  - el «1,4 tokens por palabra» es de la pieza 1 (su crudo no está en esta carpeta; se cita la pieza).
- Límite declarado (va en la slide): el contador automático de la última medición marcaba rechazos honestos como «invención»; una pasada quedó invalidada en el crudo por ese artefacto.
- Verificación visual: hecha el 2026-09-30 con GLM-4.6V-Flash (7/7 SIN DEFECTOS + control de lectura del titular en cada slide) en `revision-visual-20260930.json`.
- Registro: `python3 serie_estado.py publicar CIERRE --url <url-del-post>`; si el enlace no se puede copiar, se registra con fecha y url nula.
- Gancho de la siguiente pieza: **ninguna** — es la última de la serie.
