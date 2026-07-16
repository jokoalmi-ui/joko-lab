# Watchdog de Versiones Hermes Agent (2026-07-16)

## Decisión

Se crea un watchdog automatizado para detectar nuevas versiones de Hermes
Agent, analizar su impacto en Joko Lab y decidir si actualizar o esperar.

## Mecanismo

### Watchdog automático (cron, no_agent=True)

- **Script**: `~/.hermes/scripts/hermes-version-watchdog.sh`
- **Frecuencia**: cada 7 días (10080 minutos)
- **Ejecuta**: `bash ~/.hermes/scripts/hermes-version-watchdog.sh`
- **Coste**: 0 tokens cuando no hay novedades (no_agent=True, stdout vacío = silencio)
- **Estado notificado**: `~/.hermes/.version-watchdog-notified` (contiene el tag ya notificado)

### Flujo

1. El script obtiene la versión actual vía `hermes --version`
2. Obtiene la última release vía API de GitHub (`releases/latest`)
3. Compara segmentos numéricos con Python (soporta 3 y 4 segmentos con padding a cero)
4. Si la nueva versión es distinta a la última ya notificada y es más reciente → notifica
5. Si es la misma o anterior → silencio

### Skill de análisis

- **Skill**: `hermes-lab/hermes-upgrade-analysis`
- **Ruta**: `~/.hermes/skills/hermes-lab/hermes-upgrade-analysis/SKILL.md`
- Se carga cuando el usuario pide "analiza la nueva version de Hermes"
- Metodología de 7 pasos: versión actual → changelog → bugs de migración → impacto
  por componente → informe .txt → recomendación
- El informe se guarda en `/home/jokoalmi/informes-joko-lab/` con nombre
  `YYYY-MM-DD-hermes-upgrade-analysis.txt`

## Pruebas de comparación de versiones (2026-07-16)

Contra API real de GitHub (`api.github.com/repos/NousResearch/hermes-agent/releases/latest`):

| Caso | current | latest | Segmentos | Padding | Resultado |
|---|---|---|---|---|---|
| v0.17.0 → v2026.7.7.2 | `[0,17,0]` | `[2026,7,7,2]` | 3 vs 4 | `[0,17,0,0]` vs `[2026,7,7,2]` | NEWER ✅ |
| Misma versión | `[0,17,0]` | `[0,17,0]` | 3 vs 3 | igual | SAME ✅ |
| v0.17.1 → v0.18.2 | `[0,17,1]` | `[0,18,2]` | 3 vs 3 | igual | NEWER ✅ |
| v2026.7.7.2 → v2026.7.7.3 | `[2026,7,7,2]` | `[2026,7,7,3]` | 4 vs 4 | igual | NEWER ✅ |
| v0.16.0 → v0.17.0 | `[0,16,0]` | `[0,17,0]` | 3 vs 3 | igual | NEWER ✅ |

**Código de comparación (Python, dentro del script):**

```python
import re
c = '$CURRENT'.lstrip('v')
l = '$LATEST_TAG'.lstrip('v')
c_parts = [int(x) for x in re.findall(r'\d+', c)]
l_parts = [int(x) for x in re.findall(r'\d+', l)]
while len(c_parts) < len(l_parts): c_parts.append(0)
while len(l_parts) < len(c_parts): l_parts.append(0)
if l_parts > c_parts:
    print('NEWER')
elif l_parts == c_parts:
    print('SAME')
else:
    print('OLDER')
```

**Formato de tags del repo Hermes Agent (verificado contra API):**

| tag | nombre semántico |
|---|---|
| `v2026.7.7.2` | Hermes Agent v0.18.2 |
| `v2026.7.7` | Hermes Agent v0.18.1 |
| `v2026.7.1` | Hermes Agent v0.18.0 |
| `v2026.6.19` | Hermes Agent v0.17.0 |
| `v2026.6.5` | Hermes Agent v0.16.0 |

## Bug conocido (motivo para no actualizar aún)

Bug #62723 (fix #64606, NO incluido en v0.18.2): la migración de config
v30→v32 borra silenciosamente las secciones `platforms` de perfiles con
configuración mínima. Esperar a v0.18.3 o v0.19.0 que incluya el fix.

## Componentes afectados en una futura actualización

| Componente | Riesgo | Detalle |
|---|---|---|
| Config principal (~/.hermes/config.yaml) | ALTO | Migración v30→v32 puede borrar secciones |
| Display platforms (telegram, discord) | ALTO | Bug #62723: se borran silenciosamente |
| Personality | MEDIO | Puede perderse en migración |
| Auxiliary models | MEDIO | Depende de la migración |
| Proveedor principal (DeepSeek) | BAJO | Sin cambios en interfaz |
| Delegación a Ollama | BAJO | Sin cambios en subagentes |
| Cron jobs | BAJO | No afectados |
| Skills locales | BAJO | No afectadas |
| Memory | BAJO | Sin cambios de esquema |

## Archivos involucrados (fuera del repo)

- `~/.hermes/scripts/hermes-version-watchdog.sh` — script del watchdog
- `~/.hermes/.version-watchdog-notified` — estado de última notificación
- `~/.hermes/skills/hermes-lab/hermes-upgrade-analysis/SKILL.md` — skill de análisis
