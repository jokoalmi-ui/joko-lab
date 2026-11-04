# EXP — GLiNER2.5-base en el triaje de canales (02-nov-2026)

**Estado:** ejecutada. Datos reales, no estimaciones.
**Máquina:** RTX A2000 12 GB · torch 2.15.0 (CUDA 13) · venv `~/joko-lab/.venv-gliner2` (Python 3.14.4).
**Checkpoint:** `fastino/gliner2.5-base-v1` (apache-2.0, 194M, **English**), 749 MB en `~/joko-lab/models/gliner2.5-base-v1`.
**Carga:** `AutoExtractor.from_pretrained(..., map_location="cuda", quantize=True)` → `BoundaryExtractor`, 4,4 s, 386 MiB de VRAM.
**Banco:** `04-operations/metrics/triaje_canales.jsonl` — 972 títulos con etiqueta humana `senal`.
**Reproducir:** `HF_HUB_OFFLINE=1 ./.venv-gliner2/bin/python gliner2_exp.py` (script en `~/.hermes/cache/scratch/`, resultados en esta carpeta).

## Resultados

| config | accuracy | F1 macro | F1 prometedor | F1 dudoso | F1 ruido |
|---|---|---|---|---|---|
| A — etiquetas simples | 0,3467 | 0,2241 | 0,1145 | 0,5344 | 0,0235 |
| B — etiquetas con descripción | **0,5206** | **0,2676** | **0,0000** | 0,6890 | 0,1139 |

**Línea base trivial (predecir siempre `dudoso`): 0,5700.**

El modelo **no supera la línea base** en ninguna configuración.

## Matriz de confusión B (fila = humano, columna = predicho)

```
prometedor:  prom 0   dudoso 75   ruido 12
dudoso:      prom 33  dudoso 483  ruido 38
ruido:       prom 18  dudoso 290  ruido 23
```

Con descripciones, el modelo **no predijo `prometedor` ni una sola vez** en 972 títulos: colapsa hacia la clase mayoritaria. Con etiquetas simples sobrepredice `prometedor` (367 predicciones para 87 casos reales).

## Coste (esto sí es imbatible)

- Latencia: **25,2 ms/título** (p95 27,5 ms) → **39,6 títulos/s**.
- VRAM pico: **928 MiB**.
- Los 972 títulos en **~25 s** por configuración.
- Sin facturación por token, sin red.

## Lectura

1. **HYP rechazada para esta tarea.** GLiNER2.5-base no extrae la señal de triaje con ≥ el acierto actual: empata con la clase mayoritaria y falla justo en la clase que importa (`prometedor`, 87 casos, F1 = 0).
2. **Causa probable nº1: idioma.** El checkpoint es English y parte del corpus está en español. La variante `multi-v1` (mDeBERTa, 1,1 GB) es la prueba justa pendiente.
3. **Causa probable nº2: la tarea no encaja.** Clasificar un titular de 6 palabras en tres categorías donde una es un juicio del anotador (`dudoso` = "ni fu ni fa") es el peor caso para un encoder de boundaries. La ventaja declarada de GLiNER2 es **extracción de esquema sobre texto largo**, no clasificación de titulares.
4. **No se cierra la puerta a GLiNER2.** Se cierra esta aplicación. La siguiente EXP útil es extracción de campos reales (entidades y atributos) sobre textos largos del lab, donde el modelo compite en su terreno.

## Segunda pasada: `multi-v1` (mDeBERTa, multilingüe) — 1,1 GB

Mismo banco, mismo script, mismo hardware. Resultados en `../exp-gliner2-multi-triaje-20261102/`.

| config | accuracy | F1 macro | F1 prometedor | F1 ruido |
|---|---|---|---|---|
| base A | 0,3467 | 0,2241 | 0,1145 | 0,0235 |
| base B | 0,5206 | 0,2676 | 0,0000 | 0,1139 |
| multi A | 0,5031 | 0,2506 | 0,0561 | 0,0060 |
| multi B | **0,5617** | 0,2406 | 0,0000 | 0,0000 |
| **baseline trivial** | **0,5700** | — | — | — |

`multi-v1` mejora 4 puntos sobre `base-v1`, pero **sigue por debajo de predecir siempre `dudoso`**. En la mejor configuración predijo `dudoso` en **959 de 972** títulos: no es que clasifique mal, es que no discrimina.

Coste de `multi-v1`: 565 MiB al cargar, **1.464 MiB pico**, 23,5 ms/título.

**El idioma no era la causa.** Con dos checkpoints y cuatro configuraciones, ninguno supera el suelo trivial. El problema está en la tarea: un titular de 6 palabras no da señal suficiente para tres clases donde una (`dudoso`) es un juicio del anotador y no una categoría semántica del texto. El anotador humano usa contexto que el título no contiene (canal, histórico, pieza completa).

## DEC

**GLiNER2.5 no entra en el triaje de canales.** Cerrado con evidencia: dos checkpoints, cuatro configuraciones, 972 casos, ninguna supera la línea base trivial. No es un problema de instalación, ni de GPU, ni de idioma.

Lo que esta EXP **sí** deja medido y aprovechable: el coste de GLiNER2 en esta máquina (25 ms/título, 928 MiB pico con `base`, 1.464 MiB con `multi`, 39-42 títulos/s). Ese número sirve para la siguiente prueba, donde el modelo juega en su terreno: **extracción de esquema sobre texto largo**.

Siguiente paso si se quiere seguir: exp de extracción de entidades/campos sobre textos reales del lab (descripciones largas, no titulares). Si ahí tampoco gana, GLiNER2 se archiva como candidato.

