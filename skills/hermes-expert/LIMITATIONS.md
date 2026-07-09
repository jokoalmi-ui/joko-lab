# hermes-expert — Limitaciones

> Registro vivo de límites reales encontrados.
> Fecha de última actualización: 2026-07-05

## Límites confirmados

### 1. No existe ~/.hermes/profiles/

**Verificado:** 2026-07-05
**Impacto:** Hermes usa un perfil único plano. No hay múltiples perfiles.
**Documentación afectada:** La documentación oficial de Hermes menciona profiles/ pero no existe en esta instalación.

### 2. Skills de hermes-lab/ no están en ~/.hermes/skills/

**Verificado:** 2026-07-05
**Impacto:** Las skills documentadas en `~/hermes-lab/skills/` no son cargadas por Hermes. Son archivos markdown independientes. Para que Hermes las reconozca, habría que copiarlas o enlazarlas a `~/.hermes/skills/`.

### 3. cron/ y hooks/ están vacíos

**Verificado:** 2026-07-05
**Impacto:** No hay tareas programadas ni hooks activos. Si se necesitan, hay que crearlos desde cero.

### 4. No puede asumir rutas

**Verificado:** Múltiples sesiones
**Impacto:** Hermes no puede afirmar que una ruta existe sin verificarla con comandos de solo lectura o `read_file`. Aplica a rutas de Docker, archivos de configuración, volúmenes, etc.

### 5. No recuerda conversaciones antiguas sin memoria explícita

**Verificado:** Múltiples sesiones
**Impacto:** Hermes solo recuerda lo que está en MEMORY.md, USER.md y la sesión actual. La base de datos state.db almacena sesiones pero no se inyectan automáticamente.

### 6. No ejecuta comandos sin permiso

**Verificado:** Múltiples sesiones
**Impacto:** Por diseño, Hermes no ejecuta comandos automáticamente. Siempre propone y espera confirmación.

### 7. state.db usa SQLite sin poda automática

**Verificado:** 2026-07-05
**Impacto:** `auto_prune: false`. La base de datos crece sin límite hasta llegar a 90 días de retención.

### 8. Auxiliary clients (Nous, OpenRouter) sin autenticar

**Verificado:** 2026-07-06
**Impacto:** `errors.log` muestra WARNINGs repetitivos de `auxiliary_client` marcando Nous y OpenRouter como unhealthy por falta de autenticación. No afecta al funcionamiento con DeepSeek (el proveedor principal). Son solo ruido en los logs.

### 9. Curator nunca ha consolidado skills

**Verificado:** 2026-07-06
**Impacto:** La única ejecución de curator (2026-06-30) reporta 71 skills, 0 transiciones, 0 consolidaciones. `consolidation off`. El curator está operativo pero no hace nada porque no está configurado para consolidar.

## Límites pendientes de verificar

- Número máximo de skills activas simultáneas
- Comportamiento con DESCRIPTION.md vs SKILL.md
- Si se pueden cargar skills desde fuera de ~/.hermes/skills/
- Límite de tamaño de MEMORY.md y USER.md
- Comportamiento del gateway timeout con tareas largas
