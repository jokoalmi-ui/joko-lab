# Post LinkedIn — Lección 1 · «Instrucciones: el prompt»

## Título del documento (campo de LinkedIn, se indexa)

Cómo escribir instrucciones para la IA: tarea, formato y rol

## Texto del post

Le pedí lo mismo dos veces al mismo modelo. Las dos veces acertó las seis reseñas. Solo una de las dos respuestas se podía usar.

La diferencia no fue el modelo: fue lo que escribí.

1.600 caracteres frente a 228. Misma tarea, misma tanda de reseñas, temperatura 0:

· Sin decir el formato: seis clasificaciones correctas envueltas en un párrafo con explicación por ítem. Perfecta para leerla yo, imposible de procesar.
· Con el formato exigido: un JSON válido tal cual, listo para pegar en cualquier sitio. Y 22 segundos más rápido.

En el carrusel de esta semana:

· Las tres piezas de una instrucción útil: la tarea, el formato y el rol. Y por qué el rol es la única que no es obligatoria.
· Los dos mitos: la «frase mágica» y el «cuanto más largo, mejor». El rol cambia el tono, no los datos.
· La misma petición en dos formas, con las dos respuestas literales.
· Una trampa de al lado: subir la temperatura no hace al modelo más listo. En la prueba cambió la respuesta —205 frente a 228 caracteres— pero mantuvo el formato.

La regla que me llevo: el formato no arregla los aciertos, arregla el uso. Si la salida la lees tú, la prosa vale; si la lee un programa, exige el formato.

¿Tú le pides el formato a la IA, o le dejas que elija?

Esta es la pieza 4 de una serie donde estoy aprendiendo IA y agentes de lo básico a lo avanzado, con pruebas hechas en mi propio ordenador. Lección 1: la instrucción.

#IA #InteligenciaArtificial #LLM #Productividad #Automatizacion

## Datos de la medición (para el pie de la slide 6, verificado)

- Modelo: ibm/granite4.2:8b-q4_K_M en Ollama (local).
- Tanda: 6 reseñas, misma entrada exacta.
- Condición A (instrucción sin formato exigido, temperatura 0): 6/6 correctas, 1.600 caracteres, 52,8 s, salida no parseable con código.
- Condición B (misma instrucción + «devuelve solo JSON con este esquema», temperatura 0): 6/6 correctas, 228 caracteres, 30,0 s, JSON válido tal cual.
- Condición C (control con la temperatura a 0,8): 6/6 correctas, 205 caracteres, 37,1 s, JSON válido tal cual.
- Fichero de la prueba: `medicion-formato-20260920.json` (respuestas literales), `medicion-prompt.py` (script).
- Fecha: 20-sep-2026.

---

## Notas para publicar (no se publican)

- Texto listo para pegar: `post-linkedin.txt` (solo el bloque publicable, sin cabecera ni notas). Se genera y se verifica con `python3 extraer_post.py .` desde la carpeta de la pieza: extrae el bloque del .md, escribe el .txt y comprueba que los dos llevan el mismo texto (sha256). NO pegar este .md entero.
- Archivo a subir: `carrusel-leccion-1.pdf` (7 páginas, 1080x1350) como **documento**, NO los PNG sueltos.
- Título del documento (literal, para el campo de LinkedIn): "Cómo escribir instrucciones para la IA: tarea, formato y rol".
- Campo a pegar: el texto de la publicación del bloque de arriba (mismo contenido que `post-linkedin.txt`).
- Dato de la slide 6: **medición propia** (20-sep-2026, 21:11) con `ibm/granite4.2:8b-q4_K_M` en Ollama (`num_ctx` 8192, seed 42), la misma tanda de 6 reseñas en tres condiciones: A sin formato y temperatura 0 → 1.600 caracteres, 52,8 s, no parseable; B formato JSON exigido y temperatura 0 → 228 caracteres, 30,0 s, JSON válido; C formato exigido con temperatura 0,8 → 205 caracteres, 37,1 s, JSON válido. Aciertos 6/6 en las tres: el formato no cambia los aciertos, cambia el uso. Crudo: `medicion-formato-20260920.json`; script: `medicion-prompt.py`.
- Límite declarado (va en la slide): una sola ejecución por condición (N=1); no es una ley, es una prueba.
- Verificación visual: hecha, con fecha 2026-09-20 en `seguimiento.json` (`verificado_visual: true`).
- Registro: `python3 serie_estado.py publicar L1 --url <url-del-post>` cuando el post esté arriba. Si el enlace no se puede copiar (falla el compartir de la app móvil), se registra con la fecha real y url nula, mismo criterio que L0-A y L0-B, y el hueco se declara.
- Gancho de la siguiente pieza: **L2** «El modelo conectado al mundo: datos y herramientas».
