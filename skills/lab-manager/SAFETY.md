# lab-manager — Seguridad

## Reglas obligatorias

1. **No ejecutar acciones sobre el stack de Docker** sin explicar el impacto y recibir confirmación explícita.
2. **No modificar servicios en producción** (n8n, ollama) sin autorización.
3. **No borrar scripts ni skills** sin autorización explícita.
4. **Los comandos de solo lectura son seguros**; los comandos destructivos requieren confirmación paso a paso.

## Comandos prohibidos sin confirmación explícita

- `docker compose ... stop/restart/down` — afecta servicios activos
- `docker system prune` — borra recursos no usados de Docker
- `rm -rf ...` — borrado irreversible
- `kill / pkill` — mata procesos sin limpieza
- `sudo ...` — permisos elevados, requiere autorización

## Skills que lab-manager coordina

- **n8n-admin** — n8n es zona protegida. No reiniciar ni modificar sin confirmación.
- **ai-router** — Puede usar Ollama o LM Studio. No cambiar modelo activo sin consultar.
- **docker-admin** — Comandos de solo lectura primero; acciones requieren confirmación.
- **knowledge-governor** — Solo diagnóstico; cambios en documentación requieren consulta.

## Protección de datos

- No exponer credenciales, tokens, API keys ni secretos.
- Las rutas protegidas de n8n son: `/mnt/ssd_ia_datos/n8n`, `/mnt/ssd_ia_datos/exports`, `/mnt/ssd_ia_datos/backups`.
- No modificar backups ni datos persistentes sin autorización.
