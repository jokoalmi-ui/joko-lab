# evolution — COMMANDS

## Diagnóstico

| Comando | Qué hace |
|---------|----------|
| `evolution --version` | Versión instalada |
| `evolution --force-shutdown --quit` | Forzar cierre limpio |
| `evolution &` | Abrir Evolution en segundo plano |
| `ls ~/.config/evolution/` | Ver carpetas de configuración |
| `ls ~/.local/share/evolution/` | Ver carpetas de datos |
| `du -sh ~/.config/evolution/` | Tamaño de configuración |
| `du -sh ~/.local/share/evolution/` | Tamaño de datos de correo |

## Backup

| Comando | Qué hace |
|---------|----------|
| `tar czf ~/backups/evolution-config-$(date +%F).tar.gz -C ~ .config/evolution` | Backup de configuración |
| `tar czf ~/backups/evolution-data-$(date +%F).tar.gz -C ~ .local/share/evolution` | Backup de datos |
| `tar czf ~/backups/evolution-completo-$(date +%F).tar.gz -C ~ .config/evolution .local/share/evolution` | Backup completo |
