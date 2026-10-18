---
title: "Plantilla del prompt del puente (LAB -> Gemini web)"
type: operations
---

# Plantilla del prompt del puente

> La rellena el LAB. Un fichero por tarea en `outbox/`. El bloque marcado
> `PROMPT` es lo único que se copia y se pega en Gemini web.

## Ficha de la tarea

- **Tema:**
- **Preparado:** (fecha y hora reales)
- **Herramienta prevista:** 3.1 Pro / Deep Research / NotebookLM / Gem / Workspace
- **Por qué aquí y no en local:**
- **Contexto incluido (origen y tamaño):**
- **[NO PEGAR] (excluido a propósito):**

## PROMPT

```
<rol + objetivo + formato de salida + puntos obligatorios 1..N, en imperativo>

CONTEXTO:
<extracto mínimo necesario, ya redactado; nada de volcar ficheros enteros>

SALIDA: <estructura pedida>. Si un dato no está en el contexto, escribe
"no aparece en el contexto" en vez de inventarlo.
```

## Cómo devolver la respuesta

Guardar la respuesta completa, sin editar, como
`inbox/AAAA-MM-DD-HHMM-<tema>-respuesta.txt` y avisar por Telegram:
«trae el inbox» → el LAB la verifica y la archiva.

## Criterio de valor (para el registro)

- **5** = no replicable en local y ha cambiado una decisión o un entregable
- **4** = no replicable y ha ahorrado trabajo real
- **3** = útil, pero replicable con esfuerzo en local
- **2** = relleno
- **1** = lo cubría el local
