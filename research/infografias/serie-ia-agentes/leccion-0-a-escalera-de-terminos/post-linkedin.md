# TEXTO DEL POST — Lección 0-A (carrusel «IA, ML, Deep Learning y LLM: la escalera de términos»)

**Título del documento (lo pide LinkedIn, se indexa):**
IA, machine learning, deep learning y LLM: en qué se diferencian

**Texto de la publicación (pegar tal cual):**

«IA», «machine learning», «deep learning» y «LLM». Se usan como sinónimos toda la semana. No lo son.

Son cajas dentro de cajas:

· IA: el paraguas. Cualquier máquina que hace algo que llamamos «inteligente».
· Machine learning (ML): programas que aprenden de ejemplos en vez de seguir reglas escritas a mano.
· Deep learning (DL): redes neuronales con muchas capas.
· LLM: deep learning especializado en lenguaje. La caja más pequeña de las cuatro.

El orden importa: un LLM es un caso de DL, que es un caso de ML, que es un caso de IA. Al revés no funciona. Un filtro de spam es ML y no es deep learning. Un rival de ajedrez con reglas fijas es IA y no aprende de nada.

Por qué te conviene tenerlo claro: cada peldaño hace una cosa y te conviene pedirle esa. A la IA de reglas, que cumpla lo escrito. Al machine learning, que acierte una predicción. Al LLM, texto. Y al LLM no le pidas exactitud ni datos que no le has dado.

Lo probé antes de escribir esto. Le pregunté a un modelo local tres cosas que no puede saber: cuántos modelos de IA tengo instalados, cuántas piezas tiene esta serie y el total de un albarán que no existe.

· Sin darle el dato: 0 de 3. No dijo «no lo sé». Contestó 1, 45 y 1234.56.
· Dándole el dato en la pregunta: 3 de 3. Contestó 15, 8 y 30.50.

Un LLM no consulta tu ordenador: predice texto. Si el dato no está en lo que le escribes, se lo inventa con toda la seguridad del mundo.

Pieza 2 de una serie para entender la IA y los agentes desde cero, en orden y con datos medidos, sin humo.

En el carrusel: los cuatro peldaños con un ejemplo y con lo que NO le puedes pedir a cada uno, la confusión típica («son lo mismo») y la prueba con y sin el dato.

¿Cuál de las cuatro palabras usas peor? Te leo.

#IA #InteligenciaArtificial #MachineLearning #DeepLearning #LLM

---

## Notas para publicar (no se publican)

- Archivo a subir: `carrusel-leccion-0-a.pdf` (7 páginas, 1080x1350) como **documento**, NO los PNG sueltos.
- Título del documento (literal, para el campo de LinkedIn): "IA, machine learning, deep learning y LLM: en qué se diferencian"
- Dato de la slide 6: **medición propia** (16-sep-2026) contra `qwen2.5:7b` en local (Ollama, CPU, temperatura 0). Registro crudo: `medicion-contexto-20260916.json`. Respuestas literales sin el dato: 1 / 45 / 1234.56. Con el dato: 15 / 8 / 30.50.
- Inventario del equipo (15 modelos, 112 GB, medido hoy): queda como origen de la primera pregunta, no como dato de portada.
- Verificación: QA objetivo 7/7 + transcripción literal por visión de todas las slides (sin cortes ni solapes).
- Registro: `python3 serie_estado.py publicar L0-A --url <url-del-post>` cuando esté arriba.
- Gancho de la siguiente pieza: **L0-B** «Qué puedes pedirle y qué no».
