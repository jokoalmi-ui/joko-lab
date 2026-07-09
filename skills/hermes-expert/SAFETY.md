# hermes-expert — Seguridad

## Reglas obligatorias

1. **No modificar perfiles de Hermes** sin explicar el impacto y recibir confirmación.
2. **No borrar skills** sin autorización explícita.
3. **No modificar archivos de configuración de Hermes** sin copia de seguridad previa.

## Comandos prohibidos sin confirmación explícita

- `rm -rf ~/.hermes/profiles/<perfil>` — borraría toda la configuración del perfil
- `rm -rf ~/hermes-lab/skills/<nombre>` — borraría la skill completa
- Modificar `~/.hermes/config.yaml` sin respaldo
