# EXP 2 — GLiNER2.5 clasificando el tipo de documento del lab (02-nov-2026)

**Pregunta:** ¿sirve el modelo en su terreno declarado —texto largo— para clasificar el tipo de documento?
**Modelo:** `fastino/gliner2.5-multi-v1` (mDeBERTa, multilingüe).
**Banco:** 1.789 `.md` de `~/joko-lab` con `type` en el frontmatter y cuerpo > 500 caracteres. El texto que ve el modelo es **solo el cuerpo**, limpiado (sin imágenes, enlaces ni bloques de código) y cortado a 1.200 caracteres. El frontmatter, que contiene la respuesta, se elimina.
**Etiqueta:** el `type` real del frontmatter.
**Reproducir:** `HF_HUB_OFFLINE=1 ./.venv-gliner2/bin/python gliner2_exp_docs.py` (script en `~/.hermes/cache/scratch/`).

## Distribución del banco

```
session    1160   (64,8 %)
research    431   (24,1 %)
operations   76
knowledge    55
lpa          43
EXP          14
docs         10
```

**Baseline trivial (predecir siempre `session`): 0,6484.**

## Resultados

| config | accuracy | F1 macro | ¿supera baseline? |
|---|---|---|---|
| A — etiquetas simples | 0,6221 | 0,2966 | No |
| B — con descripciones | **0,6814** | **0,3760** | Sí, +3,3 puntos |
| baseline trivial | 0,6484 | — | — |

Latencia: 28,9 ms/doc (A), 38,1 ms/doc (B). VRAM pico 1.464 MiB.

**Por primera vez el modelo supera el suelo trivial.** La mejora es real pero pequeña.

## Dónde está ese acierto

```
session     n=1160   acierta 970   (predice research 124, knowledge 29)
research    n= 431   acierta 194   (predice knowledge 194)
knowledge   n=  55   acierta  20   (predice operations 21)
operations  n=  76   acierta   3   (predice research 33, knowledge 27)
lpa         n=  43   acierta  22
EXP         n=  14   acierta   9
docs        n=  10   acierta   1
```

- El **54,2 % de todos los aciertos** son `session` acertados.
- `research` acierta 194 y falla otras 194 confundiéndolas con `knowledge`.
- `operations` acierta **3 de 76**. `docs`, **1 de 10**.
- F1 macro 0,376: la mitad de las clases están por debajo de 0,12.

## Lectura

1. El modelo funciona como **discriminador binario `session` / `no-session`** (83,6 % de recall en session, 970/1160). Ahí sí aporta.
2. Como clasificador de 7 tipos documentales **no sirve**: las clases minoritarias —justo las que interesan— caen a F1 0,05-0,11.
3. La ventaja de +3,3 puntos sobre el baseline es demasiado estrecha para justificar sustituir nada. Un `grep` de encabezados (`## Fuentes`, `## Hallazgos`, `Sesión \``) probablemente iguala ese 0,68 sin GPU.
4. Sesgo del banco: `session` es el 64,8 % porque son tarjetas auto-generadas por el consolidador. El banco está desbalanceado a favor de la clase fácil.

## DEC

**GLiNER2.5 no sustituye la clasificación documental del lab.** Dos tareas distintas (titulares y documentos largos), dos checkpoints y cuatro combinaciones checkpoint-configuración: el modelo solo gana donde la tarea es casi binaria.

Queda una hipótesis sin probar y es la última que merece la pena: **extracción de entidades** (nombres de herramientas, modelos, fechas, personas) sobre texto largo, que es literalmente para lo que está entrenado. No se puede medir con un banco automático como los anteriores; requiere una muestra pequeña anotada a mano.

Si esa prueba tampoco da ventaja clara, GLiNER2 se archiva como candidato y el venv (`5,6 GB`) y los pesos (`1,9 GB`) se pueden borrar.
