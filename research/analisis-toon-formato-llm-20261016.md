# Análisis — TOON (Token-Oriented Object Notation): ¿conviene adoptarlo en el lab?

**VERACIDAD:** [ALCANCE INTERNO]
**Fecha del análisis:** 2026-10-16 07:1x CEST (medida con `date` → `2026-10-16 07:17:35 CEST`)
**Fuente primaria:** especificación oficial `toon-format/spec` — **v4.1 (26-jul-2026)**, estado *Working Draft*, licencia **MIT**, © 2025-present **Johann Schopplich**, leída vía `web_extract` el 16-oct-2026 (3.681 B devueltos entre spec y README).
**Repositorio de referencia:** `toon-format/toon`, metadatos por API de GitHub el 16-oct-2026 07:1x → **creado 2025-10-22**, último push **2026-10-09**, **25.505 ★**, **1.138 forks**, **MIT**, descripción literal «Token-Oriented Object Notation: a compact, human-readable encoding of the JSON data model». La organización `toon-format` agrupa **12 repos** (SDK TypeScript oficial + implementaciones de terceros en Python, Java, Go, Rust, …).
**Implementación usada en el lab:** PyPI `toon-format` (paquete oficial de Python) → **1.1.0 (2026-10-06)**; la **1.0.0 es del 2026-10-03** y la 0.1.0 del **2025-11-01**. Módulo `toon_format`. Instalada en `/home/jokoalmi/venvs/toon-vs-json` (instalación previa; el primer intento con el nombre `toon` falló porque **el paquete real se llama `toon-format`**).
**Método:** metadatos por API (GitHub/PyPI) + lectura de README/spec con `web_extract`; literatura por `web_search` (títulos y resúmenes del índice de búsqueda — **NO se ha leído el texto completo de los arXiv**, por eso las cifras de terceros van marcadas como tales); y la **medición propia** de la tanda anterior del lab (script `~/.hermes/scripts/toon-vs-json-qwen36.py`, 208 líneas; job de cron `f9615035320a`).

## Qué es
**TOON** es una **codificación del modelo de datos JSON**, línea a línea, pensada para prompts de LLM: indentación tipo YAML para objetos y **arrays uniformes en forma tabular**, con la longitud declarada en la propia cabecera. Ejemplo del formato:

```
users[2]{id,name,role}:
  1,Ana,admin
  2,Luis,user
```

Frente a JSON, elimina llaves, comillas repetidas y el `{"clave": valor}` de cada fila: el nombre de los campos se escribe **una vez** en la cabecera y los valores van en CSV por fila. No es un formato binario ni un compresor: es texto legible, y el proyecto lo presenta como **alternativa a JSON en la entrada de prompts** (no como formato de almacenamiento ni de API).

## Lo que promete el proyecto (benchmarks del propio autor)
- 72,2 % de acierto frente a 71,4 % de JSON con **−42,6 % de tokens** (244 preguntas, 4 modelos).
- 76,4 % frente a 75,0 % en una suite propia de 209 preguntas con **−39,9 % de tokens**.
- Los propios resultados por modelo no son uniformes: en Gemini **TOON queda por debajo** (96,7 % vs 97,1 %), y el propio material reconoce que **JSON-compact gana en datos anidados** y CSV en tablas planas.
- Conclusión honesta de un análisis de la comunidad (`context-compression/RESEARCH.md`): TOON es **un candidato, no la respuesta**; optimiza datos estructurados, no instrucciones.

## Evidencia independiente (lo que rompe el relato)
- **Ensayo propio de improvingagents.com** (GPT-4.1-nano y GPT-5-nano): TOON **47,5 %** de acierto, por debajo de Markdown-KV (60,7 %), JSON (52,3 %) y YAML; en datos anidados **43,1 % vs 62,1 % de YAML**. Su conclusión: **no encontraron ningún caso donde TOON fuera el mejor formato**.
- **arXiv 2605.29676** («Notation Matters», evaluación agéntica: BFCL, MCPToolBenchPP, MCP-Universe, StableToolBench; 5 LLM de pesos abiertos): TOON ahorra **−18 % de tokens** pero **pierde ≈9 puntos de acierto**; en multi-turno aparecen **fallos de parseo en cascada** y la salida de **llamadas a herramienta en paralelo se colapsa** en casi todos los modelos (Mistral en BFCL: 89 % → 53 %).
- **arXiv 2601.12014** («Are LLMs Ready for TOON?»): TOON **no está en el preentrenamiento** de los modelos → hay que especificar la sintaxis en el prompt y la corrección estructural se degrada.
- **IEEE Access 2026** (5.016 evaluaciones): −39,6 % de tokens y ligera ventaja de acierto (73,9 % vs 69,7 %), pero **pierde contra JSON-compact en datos anidados** y da **0 % en detección de truncado** pese a incluir el metadato de longitud.
- **F5 / blog técnico**: lo llama el «efficiency trap» — mucha promoción y parodias, poco uso real; recuerda que datos estructurados **no** son instrucciones.
- **McMillan 2026**: en generación de SQL el formato **no cambia el acierto agregado** de forma significativa (χ²=2,45; p=0,484).

Patrón: **el ahorro de tokens es real y reproducible; la ganancia de acierto no lo es**, y en modelos pequeños —o cuando el formato se usa para orquestar herramientas— el acierto **cae**.

## Medición propia del lab (tanda 15–16 oct, tokens vs acierto)
Tokens (gana siempre):
- Ollama: **3.143 → 2.474** (−21,3 %)
- LM Studio: **4.848 → 3.764** (−22,4 %)
- Tokenizer Qwen3.6: **−23,1 %**

Acierto (pierde):
- `granite4.2:8b`: JSON **24/26/24** vs TOON **11/13/11**
- `qwen2.5:7b`: JSON **12/15** vs TOON **3/15**
- variante `tab`: **2/15**
- `deepseek-r1-distill-14b`: **0/15 en AMBOS formatos** → prueba **descartada** (no mide)
- Causa identificada: **desalineación posicional** (el encoder sí cita las comas; el problema no es el separador sino que el modelo no respeta la alineación campo↔valor en la forma tabular).

La dirección de estos números **coincide exactamente** con la literatura independiente: ahorro de tokens real, acierto dependiente del modelo y en regresión en modelos pequeños sin exposición a TOON.

## Encaje en el lab
- **Aporta**: (a) una cifra de ahorro de contexto reproducible si algún día el problema fuera la ventana de contexto — hoy **no lo es** (el cuello es el acierto y la disciplina de formato); (b) material y cifras propias para contenido (LinkedIn), con experimento hecho y contraste externo.
- **NO aporta**: ventaja de precisión en modelos locales pequeños/medianos, ni madurez (el binding de Python tiene **13 días** de vida en su 1.0), ni reduce el trabajo de disciplina de formato — lo aumenta (hay que explicar TOON en el prompt).
- **Cambio de criterio necesario**: que un modelo grande local (p. ej. **qwen3.6-35b**) dé acierto **≥ JSON** con ahorro claro de tokens. La prueba está agendada y **todavía no ha corrido**.

## Veredicto
**No adoptar TOON** para el pipeline del lab. El formato cambia tokens por acierto en el rango de modelos que el lab usa a diario, y el resultado no es un fallo aislado del lab: **tres evaluaciones independientes** describen el mismo patrón. Se mantiene el criterio ya fijado: **medir precisión además de tokens antes de adoptar un formato**.
Se reconsideraría **solo** si la corrida con el modelo grande (35b) invierte la relación (acierto ≥ JSON con ahorro ≥ ~20 %), y aun así quedaría como opción **por tarea**, nunca global.

## Lo que NO se puede afirmar
- **No se ha leído el texto completo** de arXiv 2605.29676 / 2601.12014 ni del paper de IEEE Access: las cifras de terceros son las que devolvió el índice de búsqueda (título/resumen), **no una lectura verificada línea a línea**.
- **No se ha ejecutado la prueba con `qwen3.6-35b`**: al cerrar este análisis el job `f9615035320a` figura **agendado a las 08:00 del 16-oct y sin ejecutar**; la corrida previa (23:49) dejó `NO MEDIDO: el API Server de LM Studio no responde`.
- Las cifras propias provienen de la tanda anterior: **los artefactos en `/tmp` se borraron** con el resto de temporales redundantes, así que las cifras quedan registradas aquí y en el backlog, **sin el volcado original** para re-auditar.
- Los **25.505 ★** y demás metadatos del repo son los que devolvió la API de GitHub a las 07:1x del 16-oct: **foto de ese instante**, no una serie temporal.
- No se ha evaluado el **rendimiento del propio encoder/decoder** en Python (solo se comprobó round-trip exacto en la validación del instrumento).

## Estado del lab devuelto
- Sin tocar: `n8n`, Docker, `automation-stack`, `/mnt/ssd_ia_datos/`, LM Studio, `~/.hermes/config.yaml`. Sin commit ni push.
- No se ha arrancado ningún servicio; la prueba de las 08:00 arrancaría LM Studio por sí misma si el API está apagado (salvaguarda `TOON_NO_ARRANQUE=1` disponible) — **decisión del usuario, sin cambios en este análisis**.
- **Registro de la escritura**: ver entrada del 16-oct en `04-operations/backlogs/pendientes.md` (marca `toon-analisis-20261016`), con bytes/md5 antes y después y backup del backlog.
