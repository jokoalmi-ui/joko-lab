# hermes-expert — Conocimiento

> Cómo funciona Hermes internamente.
> Para estructura del sistema, ver STRUCTURE.md.
> Para configuración, ver CONFIG.md.

## Modelo de funcionamiento

1. **Entrada:** El usuario envía un mensaje.
2. **Contexto:** Hermes inyecta SOUL.md (personalidad + reglas) + MEMORY.md + USER.md.
3. **Razonamiento:** El modelo (deepseek-v4-flash) procesa el contexto y decide acciones.
4. **Herramientas:** Si necesita ejecutar algo, usa las toolsets disponibles (CLI, web, etc.).
5. **Memoria:** Al finalizar, puede guardar datos en MEMORY.md o USER.md mediante la herramienta memory().

## Skills

Las skills están en `~/.hermes/skills/`. Cada skill es un directorio que puede contener:

- **SKILL.md** — metadatos y propósito (se carga como skill activa)
- **DESCRIPTION.md** — descripción textual (posiblemente también se carga, pendiente de verificar)
- **Subdirectorios** — subskills especializadas

De 18 skills instaladas, solo 4 tienen SKILL.md propio. Las 14 restantes usan DESCRIPTION.md.

## Memoria persistente

Archivos en `~/.hermes/memories/`:

| Archivo | Propósito | Límite conocido |
|---|---|---|
| MEMORY.md | Notas personales de Hermes | ~2200 chars |
| USER.md | Perfil del usuario | ~1375 chars |

Ambos archivos se inyectan en el contexto de cada conversación. Si se llenan, hay que consolidar o limpiar.

## Sesiones

- Almacenadas en state.db (SQLite, 12 MB actualmente)
- Sin poda automática (auto_prune: false)
- Retención máxima: 90 días
- No se guardan snapshots JSON (write_json_snapshots: false)

## Configuración

Ver CONFIG.md para detalle completo.

## Logs

Archivos en `~/.hermes/logs/`:

| Archivo | Líneas | Propósito |
|---|---|---|
| agent.log | 7708 | Log principal del agente |
| errors.log | 749 | Errores y advertencias (mayoría: WARNINGs de auxiliary clients sin autenticar) |
| update.log | 147 | Log de actualizaciones |

También existe `~/.hermes/logs/curator/` con una ejecución del 2026-06-30.

## Skills con DESCRIPTION.md

De las 18 skills instaladas en `~/.hermes/skills/`, 13 usan DESCRIPTION.md en lugar de SKILL.md. Todas tienen un formato YAML simple con `description:`. Las 4 restantes (computer-use, diagnostico-stack-local, dogfood, yuanbao) tienen SKILL.md propio.

## Proveedores

| Proveedor | Tipo | URL | Estado |
|---|---|---|---|
| DeepSeek | Externo | https://api.deepseek.com/v1 | Principal activo |
| Ollama | Local | http://localhost:11434/v1 | Custom provider, GPU habilitada |

## Personalidades

14 personalidades disponibles. Se activan con `/personality <nombre>`.
La personalidad se inyecta en el prompt del sistema, modificando el tono de la respuesta.

## Flujo de decisión

Según orden de consulta definido en HERMES.md del laboratorio:
1. HERMES.md (filosofía)
2. docs/arquitectura.md (entorno)
3. docs/decisiones/ (porqués)
4. Skill especializada
5. Notificar incoherencias
6. No duplicar información
