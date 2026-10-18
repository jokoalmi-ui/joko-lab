# TEXTO DEL POST — Lección 0 (carrusel «Qué es un LLM»)

**Título del documento (lo pide LinkedIn) — el que se publicó el 14-sep-2026:**
¿ que es un llm? La máquina que no busca , genera.

**Texto de la publicación (pegar tal cual):**

Un modelo de lenguaje no busca información. La genera.

Es la confusión que más veces veo: se piensa que ChatGPT u otra IA «consulta» algo parecido a internet o a una enciclopedia.

No funciona así.

Un modelo de lenguaje ha leído muchísimo texto, y de ahí aprende un patrón estadístico del idioma. Cuando le escribes, no recupera una frase guardada: predice el fragmento siguiente (el token), lo añade y repite. Palabra a palabra.

Eso explica dos cosas que cambian por completo cómo lo usas:

1. Cuando te responde con total seguridad algo que no sabe, no te está mintiendo: está generando lo más plausible. Eso es una alucinación.

2. Por eso funciona tan bien cuando tú le das el texto (tus documentos, tus notas) y tan mal cuando le preguntas por algo que no ha visto.

Un dato para que se vea la escala real: en español una palabra se convierte en unas 1,4 piezas (tokens). Un texto de 141 palabras son 195 tokens — medido con un modelo de 8B instalado en local, no copiado de un blog. Y todo lo que el modelo «ve» de golpe (tu pregunta + historial + documentos) tiene que caber en su ventana de contexto: el que uso aquí declara 131.072.

Empiezo una serie para explicar la IA y los agentes desde cero, en orden y con datos comprobados, sin humo. Esta es la pieza 0: los fundamentos.

En el carrusel: qué es un LLM, cómo funciona por dentro, la confusión típica y qué puedes esperar (y qué no) de él.

¿Cuál es el mito sobre IA que más has escuchado? Te leo.

#IA #InteligenciaArtificial #LLM #IAgenerativa #AprendizajeAutomatico

---

## Notas para publicar (no se publican)

- Archivo a subir: `carrusel-leccion-0.pdf` (7 páginas, 1080x1350) como **documento**, NO los PNG sueltos.
- Título del documento (el publicado, literal): "¿ que es un llm? La máquina que no busca , genera."
- Los datos de tokens y ventana son **medición propia** (14-sep-2026) con granite 4.2 8B sobre Ollama local; no hay URL que citar. Si se quiere fuente externa, hay que buscarla antes.
- Registro: `python3 serie_estado.py publicar L0 --url <url-del-post>` cuando esté arriba.
