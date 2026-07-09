# ⚠ OBSOLETO — Anotaciones iniciales (2026-07-05)

Este archivo contenía observaciones tempranas sobre el funcionamiento interno de Hermes Agent.
Toda la información está verificada o documentada formalmente en otros lugares.

## Estado actual de cada punto

| Nota original | Estado hoy |
|---|---|
| Skills en ~/.hermes/skills/ | ✓ Confirmado |
| Perfil activo "default" | ✓ Confirmado |
| Memoria usa proveedor built-in | ✓ Confirmado |
| Sistema de perfiles (pendiente) | ✓ Verificado: `hermes profile list` |
| skill_view (pendiente) | ✓ Verificado y en uso |
| Carga automática HERMES.md (pendiente) | ✓ Verificado |
| Prioridad USER/MEMORY/SKILL (pendiente) | ✓ Resuelto: memoria > project context > skill |
| Descubrimiento skills (pendiente) | ✓ Automático desde ~/.hermes/skills/ |

## Dónde está esta información hoy

- **Arquitectura de Hermes**: `docs/hermes-expert/SKILL.md` y `docs/hermes-expert/KNOWLEDGE.md`
- **Perfiles**: `hermes profile list`
- **Skills**: `skill_view()`, `hermes skills list`
- **Memoria**: `memory` tool
- **Documentación completa**: `docs/`, `skills/hermes-expert/`

*Archivo mantenido por compatibilidad. No actualizar.*
*Reemplazado por: docs/estado-real.md, skills/hermes-expert/*

--- 

## Verificado

- Las Skills instaladas están en ~/.hermes/skills/
- El perfil activo es "default" (hermes dump).
- La memoria usa el proveedor built-in.

## Pendiente de verificar

- Sistema de perfiles.
- skill_view.
- Carga automática de HERMES.md.
- Prioridad entre USER.md, MEMORY.md y SKILL.md.
- Descubrimiento automático de Skills.
