# scripts/ — Automatización

Scripts independientes y herramientas operativas del laboratorio.

---

## ¿Qué va aquí?

Scripts que se ejecutan sin intervención directa de Hermes:

- **`backup.sh`** — Copias de seguridad del stack Docker o documentación.
- **`healthcheck.sh`** — Verificación periódica de servicios activos.
- **`update-changelogs.sh`** — Mantenimiento de changelogs.
- Cualquier script que un cron, systemd timer o GitHub Action pueda ejecutar.

## ¿Qué NO va aquí?

- **Scripts específicos de una skill** — van en `skills/<nombre>/scripts/`.
- **El script del knowledge-governor** — ya está en `skills/knowledge-governor/scripts/`.
- **Archivos de documentación** — van en `docs/`.

## Convención

- Todos los scripts deben tener shebang (`#!/usr/bin/env bash`).
- Deben ser ejecutables (`chmod +x`).
- Deben tener un comentario de cabecera con propósito y autor.
- Si pueden destruir datos, deben pedir confirmación antes de actuar.
