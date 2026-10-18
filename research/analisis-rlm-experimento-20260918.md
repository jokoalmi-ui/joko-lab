# Experimento RLM-lite — ¿iterar en código bate a recuperar fragmentos?
**VERACIDAD:** [ALCANCE INTERNO]

- **Fecha:** 2026-09-18, ejecución 16:29:42 → 16:34 CEST (hora medida con `date`, RULE-012)
- **Autorización:** usuario, «Autorizado» (tras proponer el experimento mínimo en el análisis de RLM)
- **Diseño derivado de:** *Recursive Language Models* (arXiv 2512.24601v1) — ver `analisis-rlm-20260918.md`
- **Raíz:** `deepseek-v4-flash` vía API DeepSeek. Credencial leída del entorno del lab **dentro del proceso**; nunca impresa, nunca registrada.
- **Estado:** EXPERIMENTO EJECUTADO Y MEDIDO. Nada de esto está integrado en el lab.

## 1. Hipótesis y diseño

**Hipótesis:** en preguntas de **agregación global** («¿en cuántos ficheros aparece X?») sobre un corpus
que no cabe en la ventana, un bucle que **itera en código** (RLM-lite: el modelo no ve el contexto,
solo su tamaño; escribe código para inspeccionarlo) acierta más que un pipeline de **fragmentos top-k**.

**Corpus:** 115 SKILL.md de `/home/jokoalmi/.hermes/skills` (1.693.144 B, 1.664.825 caracteres).
Se excluyeron **49 ficheros** por contener marcas sensibles (`sk-`, `password`, `api_key`, `MEMORY.md`,
`USER.md`, `system_prompt`…). El corpus resultante es ~3× la ventana de 131k tokens (estimación por
caracteres; **no se midió con tokenizer**, así que la cifra es aproximada).

**Brazos (3), misma pregunta, `temperature=0`:**

| brazo | qué recibe el modelo | fidelidad al paper |
|---|---|---|
| `rlm` | **solo el tamaño del corpus** + funciones de código: `list_files`, `grep`, `count`, `peek`, `meta`, `sizes` | RLM con ablación **sin sub-llamadas** (Observación 2) |
| `rag_fragmentos` | **top-10 fragmentos** de 900 chars (1.849 chunks) por BM25 + permiso explícito de decir `INSUFICIENTE` | baseline «Summary/retrieval» del paper |
| `indice` | las 115 rutas + primera línea + bytes, sin contenido | baseline de truncado/índice |

**Sandbox:** el código del modelo se ejecuta con `exec` sobre builtins vacías y **whitelist AST**
(prohibidos `Import`, `open`, `exec`, `eval`, `getattr`, dunders…), con alarma de 5 s por bloque y
salida truncada a 3.000 caracteres. Las rutas se resuelven siempre dentro del corpus.

**Verdad de referencia: contada con Python/grep, NUNCA por el modelo.** Además se audita cada texto
enviado al modelo contra la lista de marcas sensibles.

## 2. Resultados

Verdad (Python) · resultado por brazo:

| # | pregunta | verdad | `rlm` | `rag_fragmentos` | `indice` |
|---|---|---|---|---|---|
| q1 | ¿en cuántos ficheros aparece «LanceDB»? | **5** | ✅ 5 (7 it · 12,2 s · 5.350 tok) | ❌ INSUFICIENTE | ❌ INSUFICIENTE |
| q2 | ¿cuántos con «n8n» y cuántos con «Docker»? | **24 / 11** | ✅ n8n=24, Docker=11 (4 it · 5,5 s · 2.540 tok) | ❌ INSUFICIENTE | ❌ INSUFICIENTE |
| q3 | ¿el SKILL.md más grande y cuántas líneas? | **media/instagram-carruseles-analisis/SKILL.md, 101.355 B, 1.419 líneas** | ✅ exacto (4 it · 5,4 s · 2.825 tok) | ❌ INSUFICIENTE | ❌ INSUFICIENTE |
| q4 | ¿cuántos con `description` que **empieza por** «Use when»? | **11** | ❌ dijo 27 (8 it · 12,7 s · 16.353 tok) | ❌ INSUFICIENTE | ❌ INSUFICIENTE |

**Marcador:** RLM-lite **3/4**; fragmentos **0/4**; índice **0/4**. Diez de las doce salidas de los
baselines fueron literalmente `INSUFICIENTE` (la excepción: q4-fragmentos devolvió vacío).

**Tokens totales:** `rlm` 27.068 · `rag_fragmentos` 14.146 · `indice` 10.811.
El RLM gasta ~1,9× y ~2,5× más tokens, pero en las preguntas que acierta el coste es de 500–2.900 tokens
y 1–6 s. No se da cifra en euros: no hay precio unitario verificado para este modelo.

### 2.1 Variante v2 — el protocolo de cierre importaba

En v1 se detectó un fallo **del harness, no del modelo**: el modelo intentó `FINAL(...)` *dentro* del
bloque de código y recibió `name 'FINAL' is not defined` (q1: 2 veces; q4: 1 vez). Se añadió `FINAL()`
como función real del sandbox y se repitieron q1 y q4:

- **q1: de 7 iteraciones / 5.350 tokens a 1 iteración / 495 tokens** (mismo acierto). **10,8× menos coste.**
- q4: sigue fallando (8 iteraciones, 20.482 tokens, sin cerrar).

## 3. Hallazgos

1. **Los conteos globales son estructuralmente imposibles para el patrón fragmentos.** El top-k no puede
   saber cuántos de los 1.849 chunks contienen algo, y el índice no tiene contenido. Coincide con el paper
   (que en contexto largo da por muertos a los baselines), pero aquí la razón es más simple y más rotunda:
   *no es que fallen, es que la pregunta les es inaccesible*.
2. **El fallo de q4 es de criterio, no de acceso.** Conteo desglosado con Python: 115 ficheros tienen
   `description`, **31** contienen «Use when» en cualquier parte y **11** lo tienen al principio del campo.
   El modelo dijo 27 en v1: aplicó un criterio intermedio. Agotó las 8 iteraciones sin verificar.
   → **Lección de lab:** un bucle así necesita el criterio **operacional y verificable**; si el criterio
   es difuso, el agente no falla al buscar, falla al definir qué cuenta.
3. **El sandbox funcionó en producción**: 1 bloqueo real de `Import` (q4 v2, iteración 5) + 3/3 bloqueos
   en prueba (`import os`, `open("/etc/passwd")`, `__import__("os")`). El código del modelo nunca tocó
   el sistema de ficheros fuera del corpus.
4. **El «negative result» #3 del paper, observado en vivo:** con `max_tokens=8` la primera llamada
   devolvió **contenido vacío** con `reasoning_tokens: 8` — todos los tokens de salida se fueron en
   razonamiento. La raíz del lab es un modelo de razonamiento, que es exactamente el perfil que el paper
   documenta como frágil (trayectorias truncadas).
5. **Cero incidencias de sensibilidad:** el audit de todo lo enviado al modelo (18 brazos × iteraciones)
   dio **0 marcas sensibles**, y 49 ficheros quedaron fuera preventivamente.

## 4. Límites de este experimento (declarados)

- **n=4 preguntas**, una sola pasada, `temperature=0`, un solo modelo raíz. No hay significación estadística.
- El baseline `rag_fragmentos` es un **BM25 reconstruido**, NO el pipeline RAG de producción del lab.
  Por tanto **el 0/4 no dice «el RAG del lab no sirve»**: dice que «top-k fragmentos + responder» no
  contesta preguntas globales. Son cosas distintas.
- **Sin sub-llamadas** (ablación deliberada; el paper dice que en contexto largo rinde casi igual).
- Corpus pequeño (115 ficheros, 1,69 MB) comparado con los 6–11M tokens de BrowseComp.
- Latencia medida con **raíz cloud**; los modelos locales del lab (7,7 tok/s) multiplicarían el tiempo
  por un factor enorme — el mismo bucle en local sería inviable de forma interactiva.
- La estimación «0,9×chars» que imprimió el harness era **un error de cálculo mío** (mezclaba bytes y
  tokens). La referencia buena es ~4 caracteres por token → **~416k tokens**, sin medir.

## 5. Lectura para Joko Lab

- **Dónde tiene ventaja real:** contabilidad y auditoría sobre corpus propios que no caben en la ventana
  (`backlog` de 760 KB, corpus de SKILL.md, `research/`, exports). Preguntas tipo «¿cuántas entradas hay
  sobre X?», «¿qué ficheros cubren Y?», «¿el corpus mantiene Z en el 100 % de los casos?».
- **Dónde NO:** preguntas donde basta un dato localizado (ahí el RAG por similitud es más barato y más
  rápido), y criterios difusos sin definición operacional (q4).
- **Condición de uso:** sandbox (ya probado) + criterio explícito + verificación con Python/grep al final.
- **En local, hoy, no:** requiere muchos tokens de salida y un modelo con buena capacidad de código;
  los dos fallos del paper que ya se ven en el lab (modelos pequeños y modelos que razonan) apuntan a que
  la raíz debe ser cloud y, si acaso, las sub-llamadas locales.

## 6. Qué NO se ha hecho

0 uso de GPU · 0 modelos descargados o cargados · 0 servicios tocados (n8n, Docker, Ollama, LM Studio,
ComfyUI intactos) · 0 cambios en el lab más allá de este informe y su registro en el backlog ·
0 integración en producción · 0 escrituras en bases de datos.

## 7. Artefactos

- Harness: `/tmp/rlm-exp/rlm_exp.py` (temporal; si se adopta, se mueve a `tools/` con OK)
- Resultados crudos: `/tmp/rlm-exp/resultados.json` (v1) y `/tmp/rlm-exp/resultados_v2.json` (protocolo corregido)
- Log de ejecución: `/tmp/rlm-exp/run.log`
