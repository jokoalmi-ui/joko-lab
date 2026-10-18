# Post LinkedIn — Lección 2 · «El modelo conectado al mundo»

## Título del documento (campo de LinkedIn, se indexa)

Cómo conectar la IA a tus datos y a tus acciones: RAG y herramientas

## Texto del post

Le pregunté por unos gastos que no le había dado. Seis preguntas, seis veces la misma respuesta: «0». Ni una sola vez dijo «no lo sé».

Con esa misma tabla delante, acertó los seis totales. Y las dos respuestas —el cero y el acierto— sonaban exactamente igual de seguras.

Después le declaré una sola función, la de sumar gastos, y en las seis preguntas devolvió la llamada bien formada: `{"herramienta": "sumar_gastos", "argumentos": {"filtro": "concepto", "valor": "luz"}}`. El número lo puso mi código, no su memoria.

En el carrusel de esta semana:

· Las dos formas de conectar un modelo: tus datos (RAG) y tus acciones (herramientas). En una consulta antes de responder; en la otra pide que ejecutes tú.
· Los dos caminos por dentro: trocear → vectores → buscar por similitud → responder citando la fuente; y declarar funciones → recibir la llamada → ejecutar → devolver el resultado.
· Cuatro nombres que se mezclan y no son lo mismo: herramientas (la capacidad), tool calling (el mecanismo) y MCP (el estándar).
· RAG frente a fine-tuning: memoria consultable frente a cambio de comportamiento. No son lo mismo y no se sustituyen.
· La prueba: 6 preguntas al mismo modelo local en 4 condiciones —sin los datos, con los datos, con la herramienta a temperatura 0 y el control a 0,8—.

La regla que me llevo: la pregunta no es si el modelo sabe o no sabe, sino de dónde sale el número. Si sale de su memoria, no hay nada que auditar. Si sale de tu código, puedes comprobarlo.

¿Tú le das tus datos a la IA, o le pides que ejecute algo?

Esta es la pieza 5 de una serie donde estoy aprendiendo IA y agentes de lo básico a lo avanzado, con pruebas hechas en mi propio ordenador. Lección 2: el modelo conectado al mundo.

#IA #InteligenciaArtificial #LLM #RAG #AgentesIA

## Datos de la medición (para el pie de la slide 6, verificado)

- Modelo: ibm/granite4.2:8b-q4_K_M en Ollama (local), num_ctx 8192, seed 42.
- Tanda: 6 preguntas sobre un fichero de 8 gastos de ejemplo, con los totales calculados aparte en Python.
- Condición A (los datos en el prompt, sin herramienta, temperatura 0): 6/6 números exactos.
- Condición S (la misma pregunta sin los datos y sin herramienta): 0/6 exactos y 6/6 respondió con un número; literal, las seis veces: `0`.
- Condición B (los datos + la función declarada, temperatura 0): 6/6 llamadas bien formadas y 6/6 con argumentos correctos.
- Condición C (control con la temperatura a 0,8): 6/6 bien formadas y correctas.
- Límites declarados: n=6 por condición y una sola pasada; en S la instrucción pedía responder solo con el número (el modelo no tuvo la opción de explicarse).
- Fichero de la prueba: `medicion-herramientas-20260922.json` (respuestas literales), `medicion-herramientas.py` (script).
- Fecha: 22-sep-2026.

---

## Notas para publicar (no se publican)

- Texto listo para pegar: `post-linkedin.txt` (solo el bloque publicable, sin cabecera ni notas). Se genera y se verifica con `python3 extraer_post.py .` desde la carpeta de la pieza: extrae el bloque del .md, escribe el .txt y comprueba que los dos llevan el mismo texto (sha256). NO pegar este .md entero.
- Archivo a subir: `carrusel-leccion-2.pdf` (7 páginas, 1080x1350) como **documento**, NO los PNG sueltos.
- Título del documento (literal, para el campo de LinkedIn): "Cómo conectar la IA a tus datos y a tus acciones: RAG y herramientas".
- Campo a pegar: el texto de la publicación del bloque de arriba (mismo contenido que `post-linkedin.txt`).
- Dato de la slide 6: **medición propia** (22-sep-2026) con `ibm/granite4.2:8b-q4_K_M` en Ollama (`num_ctx` 8192, seed 42), 6 preguntas sobre 8 gastos de ejemplo en cuatro condiciones: A con los datos en el prompt → 6/6 exactos; S sin los datos → 6/6 respuestas «0» (ninguna vez «no lo sé»); B con la función declarada, temperatura 0 → 6/6 llamadas bien formadas y correctas; C control a 0,8 → 6/6 igual. Crudo: `medicion-herramientas-20260922.json`; script: `medicion-herramientas.py`.
- Límite declarado (va en la slide): una sola ejecución por condición (N=6); no es una ley, es una prueba. En S la instrucción pedía solo el número, así que el 0 también es efecto del formato exigido.
- Verificación visual: ver `seguimiento.json` (`verificado_visual`).
- Registro: `python3 serie_estado.py publicar L2 --url <url-del-post>` cuando el post esté arriba. Si el enlace no se puede copiar (falla el compartir de la app móvil), se registra con la fecha real y url nula, mismo criterio que L0-A y L0-B, y el hueco se declara.
- Gancho de la siguiente pieza: **L3** «El agente: el bucle».
