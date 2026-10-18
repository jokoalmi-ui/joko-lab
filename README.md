---
type: index
subtype: index
status: index
tags: [joko-lab]
created: 2026-07-28
---
# Joko Lab — Laboratorio de Ingenieria de IA
==============================================

Joko Lab es un laboratorio reproducible para estudiar,
comparar y mejorar agentes de IA. No es un "agente".
Es un sistema operativo para trabajar con IA.

## Pilares

```
01-knowledge/       Lo que sabemos (modelos, experimentos, datos)
02-infrastructure/  Lo que sostiene el lab (docker, recovery, inicio/fin)
03-automation/      Lo que se ejecuta solo (scripts, cron, tests)
04-operations/      Lo que registramos (informes, metricas, incidencias)
05-inference/       Lo que hacemos con lo que sabemos (router, compiler)
```

## Empezar una sesion

```bash
~/joko-lab/02-infrastructure/inicio/inicio.sh
```

Esto ejecuta los checks, genera estado-inicial.json,
compara con el ultimo cierre y reporta anomalias.

## Mapa de capacidades del lab

Antes de valorar cualquier novedad externa (video, post, herramienta),
consultar el mapa: si el dominio ya esta cubierto, es validacion;
si no, es futurible con senal.

- `research/mapa-capacidades-lab-20260824.md` — plano central: 7 dominios,
  164 skills, 317 research, 80 tools, 3 MCPs, RAG 21.975 fragmentos,
  modelos locales, crons, futuribles con senales de activacion.


## Cerrar una sesion

```bash
~/joko-lab/02-infrastructure/fin/fin.sh
```

Esto captura el estado, compara con el inicio,
hace backup si hay cambios y guarda estado-final.json.

## Incidentes documentados

`02-infrastructure/recovery/procedures/`

## Documentacion

`docs/`

## Estado

Este laboratorio esta en construccion activa (Fase 1 de 5).
Ver `informes-joko-lab/2026-07-28-estructura-joko-lab-5-pilares.txt`
para el diseno completo.
