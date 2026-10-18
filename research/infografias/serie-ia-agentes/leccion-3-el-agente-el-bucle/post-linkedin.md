# Post LinkedIn — Lección 3 · «El agente: el bucle»

## Título del documento (campo de LinkedIn, se indexa)

Qué es un agente de IA: el bucle de pensar, actuar y observar

## Texto del post

Le pedí el importe del pedido más caro sin darle la tabla. Contestó «0». En las seis tareas, las seis veces un dato inventado, y con el mismo tono seguro que usa cuando acierta.

En la misma tanda, el mismo modelo en bucle pidió la tabla, la recibió, comparó y contestó con los números exactos: 5 de las 6 tareas cerradas, con 3 pasos y 2 herramientas por tarea. El número salió de mi código, no de su memoria.

La diferencia entre las dos respuestas no era el modelo: era el bucle.

En el carrusel de esta semana:

· Qué es un agente: bucle (pensar → actuar → observar) + herramientas + memoria + un objetivo. La diferencia con un chatbot no es el modelo, es el bucle.
· Cómo funciona por dentro, paso a paso: pensar qué necesita, ejecutar la acción en tu código, devolver el resultado como texto, repetir hasta cerrar (o hasta agotar los pasos).
· Memoria a corto y a largo plazo: la conversación de la tarea frente a lo que se guarda fuera y se vuelve a leer.
· La confusión típica: CoT (una vuelta, sin tocar nada) frente a ReAct (bucle sobre el entorno) y agente frente a chatbot. Y la frase que se oye siempre —«más autonomía = mejor modelo»— que la medición de esta semana no respalda.
· La prueba: 6 tareas de varios pasos en 4 condiciones con el mismo modelo local —una vuelta sin herramientas, varias vueltas sin herramientas, bucle con herramientas a temperatura 0 y el control a 0,8—.

La regla que me llevo: la autonomía no la da el modelo, la da el acceso. Sin entorno no llega el dato que no tiene, y las vueltas de más solo cuestan tokens; con herramientas, el bucle cierra la tarea y el número se puede comprobar.

¿Tú has montado un bucle con herramientas, o usas la IA a una pregunta por vez?

Esta es la pieza 6 de una serie donde estoy aprendiendo IA y agentes de lo básico a lo avanzado, con pruebas hechas en mi propio ordenador. Lección 3: el agente, el bucle.

#IA #InteligenciaArtificial #LLM #AgentesIA #Automatización

## Datos de la medición (para el pie de la slide 6, verificado)

- Modelo: ibm/granite4.2:8b-q4_K_M en Ollama (local), num_ctx 8192, seed 42.
- Tanda: 6 tareas de varios pasos (traer datos, sumar, comparar, calcular un porcentaje) sobre una tabla de 8 pedidos de ejemplo, con el resultado esperado calculado aparte en Python.
- Condición A (una vuelta, sin herramientas, temperatura 0): 0/6 cerradas; 6/6 respondió con un número inventado (cinco «0» y un «25.0»).
- Condición D (bucle de hasta 4 vueltas, sin herramientas): 0/6 cerradas, pero 5 de 6 cerró diciendo «desconocido» o «no se puede determinar» en vez de inventar el dato; 2,33 pasos de media y 25.407 tokens, frente a 5.703 de A (4,5 veces más).
- Condición B (bucle con herramientas, temperatura 0): 5/6 cerradas; 3,0 pasos y 2 herramientas por tarea; 6.660 tokens por tarea resuelta.
- Condición C (control con la temperatura a 0,8): 5/6 cerradas; 2,33 pasos y 1,33 herramientas por tarea; 5.602 tokens por tarea resuelta.
- La tarea que se escapa (T1) pide dos cosas —importe y cliente— y el modelo devuelve solo el nombre: fallo de completitud, no de cálculo.
- Límites declarados: n=6 tareas por condición y una sola pasada; el coste se mide en tokens, no en euros (el modelo es local: no hay factura de API); en A y D el formato de respuesta estaba acotado (un valor, o un JSON con las claves «pensar»/«fin»).
- Ficheros: `medicion-bucle-20260924.json` (respuestas literales) y `medicion-bucle.py` (script).
- Fecha: 24-sep-2026.

---

## Notas para publicar (no se publican)

- Texto listo para pegar: `post-linkedin.txt` (solo el bloque publicable, sin cabecera ni notas). Se genera y se verifica con `python3 extraer_post.py .` desde la carpeta de la pieza: extrae el bloque del .md, escribe el .txt y comprueba que los dos llevan el mismo texto (sha256). NO pegar este .md entero.
- Archivo a subir: `carrusel-leccion-3.pdf` (7 páginas, 1080x1350) como **documento**, NO los PNG sueltos.
- Título del documento (literal, para el campo de LinkedIn): "Qué es un agente de IA: el bucle de pensar, actuar y observar".
- Dato de la slide 6: **medición propia** (24-sep-2026) con `ibm/granite4.2:8b-q4_K_M` en Ollama (`num_ctx` 8192, seed 42), 6 tareas de varios pasos en cuatro condiciones: A una vuelta sin herramientas → 0/6 y 6 números inventados; D bucle sin herramientas → 0/6 (5 de 6 dijo «desconocido») y 4,5× más tokens; B bucle con herramientas, temperatura 0 → 5/6 cerradas, 3 pasos y 2 herramientas por tarea; C control a 0,8 → 5/6. Crudo: `medicion-bucle-20260924.json`; script: `medicion-bucle.py`.
- Límite declarado (va en la slide): una sola ejecución por condición (n=6 tareas); no es una ley, es una prueba.
- Verificación visual: ver `seguimiento.json` (`verificado_visual`).
- Registro: `python3 serie_estado.py publicar L3 --url <url-del-post>` cuando el post esté arriba. Si el enlace no se puede copiar (falla el compartir de la app móvil), se registra con la fecha real y url nula, mismo criterio que L0-A, L0-B, L1 y L2, y el hueco se declara.
- Gancho de la siguiente pieza: **L4** «De uno a muchos: agentes que colaboran».
