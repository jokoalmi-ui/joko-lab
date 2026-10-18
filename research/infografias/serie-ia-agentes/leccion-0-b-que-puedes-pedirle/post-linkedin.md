# TEXTO DEL POST — Lección 0-B (carrusel «Qué puedes pedirle y qué no: usos y tamaño del modelo»)

**Título del documento (lo pide LinkedIn, se indexa):**
Qué puedes pedirle a la IA y qué no: usos y tamaño del modelo

**Texto de la publicación (pegar tal cual):**

«Es que el modelo que uso es pequeño.» «Para eso necesitas uno grande.» Se dice mucho. Lo medí.

Misma tarea, mismo texto, tres modelos en mi ordenador (2,6B, 8B y 35B), temperatura 0:

· Clasificar 5 reseñas (positiva/negativa): los tres, 5 de 5. El de 2,6B tardó 18,2 s; el de 8B, 13,8 s; el de 35B, 119,6 s.
· Sacar el importe del transporte de una factura: el de 2,6B no llegó a contestar (se quedó razonando); el de 8B lo dio en 0,3 s; el de 35B, en 48,8 s.
· Calcular el total (4 × 89,50 − 10,00 + 12,00 = 360,00 €): el de 2,6B acertó; el de 8B contestó 342,00; el de 35B acertó.

Lo que saco en claro:

1. Reescribir texto que le das —resumir, redactar, clasificar, traducir— lo hace hasta un modelo que cabe en un portátil.
2. Para exactitud no sirve ninguno, tampoco el grande: dale el dato o calcula tú.
3. El tamaño se paga en tiempo y en recursos: el mismo importe costó unas 160 veces más al de 35B que al de 8B.
4. Más grande no es más fiable: el que falló la cuenta fue el mediano, no el pequeño.

Los cuatro usos que sí resuelve: resumir, redactar, clasificar y traducir/extraer. Y los cuatro tienen lo mismo en común: el material se lo das tú. El modelo no busca fuera; reescribe lo que le entregas.

Y los tres pasos de cómo funciona, para no pedirle lo imposible: le das la instrucción y el material (no le pidas que busque lo que no le has dado), predice la siguiente pieza de texto (no le pidas cuentas exactas ni datos de hoy) y devuelve el formato que pediste (no le pidas que sepa si lo que dice es verdad). El que lee, corrige y decide eres tú.

Pieza 3 de una serie para entender la IA y los agentes desde cero, en orden y con datos medidos, sin humo.

En el carrusel: los cuatro usos que sí, los tres pasos con lo que NO le puedes pedir en cada uno, la confusión típica («cuanto más grande, mejor») y la prueba completa con los tres modelos.

¿Qué le pides tú a la IA que no deberías? Te leo.

#IA #InteligenciaArtificial #LLM #ModelosLocales #Productividad

---

## Notas para publicar (no se publican)

- Archivo a subir: `carrusel-leccion-0-b.pdf` (7 páginas, 1080x1350) como **documento**, NO los PNG sueltos.
- Título del documento (literal, para el campo de LinkedIn): "Qué puedes pedirle a la IA y qué no: usos y tamaño del modelo"
- Dato de la slide 6: **medición propia** (18-sep-2026) en LM Studio (`localhost:1234`, temperatura 0), la misma tanda de tareas a `lfm2.5-2.6b` (2,6B), `granite-4.1-8b` (8B) y `qwen3.6-35b-a3b-mtp` (35B). Registro consolidado: `medicion-tamano-consolidado.json` (+ crudos y `medicion-tamano-2,6b-repeticion.json`).
- Hallazgo bruto que NO va al post: con el VLM residente, los modelos 8B y 35B no cargaban (`llama-server exited before becoming healthy`); se arregló con `lms unload`. Queda como nota operativa.
- Corrección metodológica ya aplicada: el "esperado" del cálculo estaba mal en la primera pasada (370); el total correcto es **360,00** (4×89,50=358; −10=348; +12=360). Los veredictos salen de recalcular sobre la salida literal de cada modelo.
- Verificación: QA objetivo 7/7 (1080x1350, bordes crema limpios) + transcripción literal por visión de las 7 slides. Corregido un corte en S4 («35B pide una GPU d…»).
- Registro: `python3 serie_estado.py publicar L0-B --url <url-del-post>` cuando esté arriba.
- Gancho de la siguiente pieza: **Lección 1** «Instrucciones: el prompt».
