# EXP 3 — GLiNER2.5 extrayendo entidades de textos reales del lab (02-nov-2026)

**Pregunta:** en su terreno declarado (extracción de entidades sobre texto largo), ¿aporta algo?
**Modelo:** `fastino/gliner2.5-multi-v1`, etiquetas `herramienta` / `modelo_ia` / `organizacion` con descripción.
**Muestra:** 15 documentos reales de `research/` y `04-operations/` (1.800 caracteres cada uno, sin bloques de código).
**Script:** `~/.hermes/cache/scratch/gliner2_exp_ner.py`.

## Cómo se midió (y por qué hay tres cifras)

La verdad de referencia son las menciones de una lista cerrada de 36 entidades del lab (n8n, ollama, hermes, qwen, deepseek, nvidia…). Es determinista y reproducible, pero **depende de cómo se defina "mención"**, y ahí salen tres números distintos:

| medida | qué cuenta | resultado |
|---|---|---|
| recall estricto | entidad de la lista como palabra exacta | **8/25 = 0,32** |
| recall flexible | también variantes con versión (`qwen` en `qwen3-14b`) | 14/122 = 0,115 (gt inflado) |
| precisión estricta | predicha ∈ lista cerrada | **16/157 = 0,10** |

Ninguna de las tres es la buena, y conviene decir por qué:

- El recall estricto **subestima**: en un documento extrajo `qwen3-14b`, `llama-3.1-8b`, `gemma-4-e4b` (correctas) pero mi lista dice `qwen`, `llama`, `gemma` y el regex no las empareja.
- El recall flexible **sobrestima el denominador**: `meta` aparece dentro de "metadatos" y `git` dentro de otras palabras, así que infla el ground truth a 122.
- La precisión estricta **castiga lo correcto**: si extrae `guia-joko-lab.md` o `mel_ledger` y no están en mi lista, cuenta como fallo.

## Juicio sobre la precisión real

Muestra aleatoria de 25 de las 157 entidades extraídas:

```
thepracticai · nichonauta · shiva.bytes · telegram      (canales y servicios reales)
gemma-4-e4b · llama-3.1-8b · gemini api · hermes        (modelos y herramientas reales)
guia-joko-lab.md · mel_ledger · scratchpad · watchdog   (archivos y componentes reales)
lora · delta-lora · kos · strategy controller · mcps    (términos técnicos del dominio)
```

**21 de 25 son entidades correctas** = precisión ≈ 0,84. Las cuatro flojas: `genai`, `spec first`, `tot`, `mcps` (genéricas o etiquetas sueltas).

Este 0,84 es **mi juicio sobre 25 casos**, no una métrica automática. Es el único número de este informe que no se puede reproducir con un comando.

## Coste

- Latencia: **131,8 ms/documento** (5 veces más que clasificar: aquí procesa el texto entero).
- VRAM pico: 1.464 MiB.
- 15 documentos en ~2 s.

## Lectura

1. **En NER el modelo sí funciona.** Extrae nombres técnicos reales con precisión alta y sin inventar apenas. Es la primera tarea de las tres donde el resultado es utilizable.
2. **El recall es parcial.** No encuentra todas las menciones: con la medida más benévola se queda entre un octavo y un tercio. Sirve para **enriquecer**, no para inventariar.
3. **La clasificación de 3 y 7 clases está descartada** con evidencia de EXP 1 y EXP 2. Esta EXP no la rescata: es otra tarea.

## DEC

**Sí hay un uso para GLiNER2.5 en el lab, y es estrecho: extracción de entidades para enriquecer índices.** Ejemplo concreto: al reindexar los 3.000 documentos del lab, sacar de cada uno los modelos, herramientas y canales que menciona, y guardar eso como metadato de búsqueda. Precisión suficiente para que el metadato sea útil; recall insuficiente para decir "esto es todo lo que menciona".

**No sustituye** a un LLM generativo en clasificación, ni en extracción exhaustiva de campos con formato estricto.

Decisión operativa pendiente: si se adopta para el índice del RAG, se queda el venv (5,6 GB) y los pesos (1,9 GB); si no hay hueco en el plan, se archiva y se recuperan 7,5 GB.
