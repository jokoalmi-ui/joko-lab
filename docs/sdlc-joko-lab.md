---
type: docs
subtype: docs
status: active
tags: [docs, sdlc, proceso, harness]
created: 2026-10-23
---
# SDLC real de Joko Lab

Este documento describe **el ciclo de vida que el lab ya ejecuta**, no uno ideal.
Cada fase apunta al artefacto real que la cumple. Si una fase no existe, se dice.

Fecha de redacción: 2026-10-23. Base: repo `~/joko-lab` en `960990d`.

## 1. Qué es y qué no es

No es un SDLC de manual (requisitos formales → diseño firmado → QA → staging → release).
Es un SDLC **de un solo operador** donde la verificación se apoya en artefactos y no en reuniones.
Lo que lo hace funcionar no es el número de fases, sino tres cosas: RULEs con evidencia,
gate de veracidad y recibos git verificables.

## 2. Las fases y su artefacto real

**Descubrimiento / requisitos**
- `04-operations/backlogs/pendientes.md` — backlog único, con topes de fecha y marcas por entrada.
- `01-knowledge/objects/OBS-*.yaml` — observaciones con evidencia.
- Bucle corto del lab: **OBS → HYP → EXP → DEC**. Una hipótesis no se convierte en cambio sin pasar por experimento y decisión.

**Constitución y diseño**
- `AGENTS.md` — reglas de operación del repo.
- `01-knowledge/objects/RULE-*.yaml` — 22 ficheros a fecha de hoy, con `evidence`, `confidence`, `domain`, `scope`.
- `04-operations/decisions/` — decisiones fechadas.
- `docs/` — planes y análisis (este documento incluido).

**Implementación**
- `tools/` — utilidades del lab.
- `~/.hermes/scripts/` — wrappers que ejecutan los crons.
- `skills/` — conocimiento procedimental de Hermes.
- `hooks/pre-commit` — validación en el momento del commit.

**Pruebas**
- `tests/` — 26 ficheros `test_*.py`, batería **unittest** (no pytest).
- Estado verificado el 2026-10-23: **400 tests, 56 skipped, 0,485 s, rc=0**.
- Ejecución canónica: `cd ~/joko-lab && env -u PYTHONPATH /usr/bin/python3 -m unittest discover -s tests -t tests`
- No hay `tests/__init__.py`: por eso el descubrimiento se lanza con `-t tests`.

**Verificación**
- `verification/` — comprobaciones de estado.
- Gate de veracidad: no se declara «hecho» sin salida real del comando que lo prueba.
- RULE-021: un `ok` que descarta el error real es un falso ok; el ok se acredita en el artefacto.
- Escrituras acumulativas: backup + `cmp` del prefijo + conteo de marca.

**Despliegue**
- Crons de Hermes (`~/.hermes/cron/jobs.json`) — 57 jobs antes de este cambio.
- `hermes-gateway.service` — servicio de usuario con el scheduler.
- Docker Compose del stack principal (protegido, fuera de este repo).

**Operación y mantenimiento**
- `04-operations/incidents/` — incidencias.
- `changelog/` — qué cambió y cuándo.
- Revisión semanal LPA — detecta componentes desfasados o desconectados.
- Watchdogs (salud del sistema, higiene, backups).

**Control de cambios**
- git en `master` + `hooks/pre-commit` + `hooks/generar_recibo.sh` (recibos de commit verificables).
- Push solo a `origin`.

## 3. Huecos declarados (no son opinión, son ausencias comprobadas)

1. **Sin CI.** No existe `.github/workflows` y ningún cron ejecutaba los tests hasta el 2026-10-23.
   Los 400 tests dependían de que alguien se acordara de lanzarlos.
   *Mitigación:* cron `tests-joko-lab` (`30 6 * * *`, `no_agent`), silencio en verde, alerta en rojo.
2. **Sin entornos.** No hay staging ni rollback real: producción es este PC y el rollback es un `.bak` con md5.
   Con un operador único, montar staging sería coste sin retorno; lo que sí se exige es backup previo y verificación posterior.
3. **Sin trazabilidad requisito → test.** Un pendiente no apunta a la prueba que lo cierra.
   Es el hueco que ataca el criterio de cierre del LPA: mtime del productor + producto posterior.
4. **Criterio de cierre heterogéneo.** Cada tarea se cierra con la prueba que a cada uno se le ocurre.
   El pendiente E del informe LPA (que un `resolved` no sobrescriba la ocurrencia anterior) apunta a esto.

## 4. Qué NO se añade, y por qué

El material de harness engineering es explícito: la estructura que no demuestra valor encarece.
Añadir ceremonias de seis fases, comités o plantillas de requisitos sería «ensanchar caro».
La regla de este repo: **toda pieza nueva del proceso debe poder señalar un fallo que evitó**.
Si en 60 días no lo señala, se retira.

## 5. Cómo se verifica este documento

```sh
cd ~/joko-lab
env -u PYTHONPATH /usr/bin/python3 -m unittest discover -s tests -t tests
git log -1 --format='%h %s'
ls 01-knowledge/objects/RULE-*.yaml | wc -l
```

Si alguna cifra de este documento no coincide con la salida real, gana la salida real.
