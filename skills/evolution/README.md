# evolution — README

## Descripción

Evolution (3.56.2-9) es el cliente de correo, calendario y contactos del laboratorio. Corre en Ubuntu de forma nativa (no Docker). Almacena los datos localmente en el home del usuario.

## Datos del sistema

| Elemento | Ruta | Tamaño |
|----------|------|--------|
| Binario | /usr/bin/evolution | — |
| Configuración | ~/.config/evolution/ | 260 K |
| Datos (correo, calendarios) | ~/.local/share/evolution/ | 4.2 GB |
| Libretas de direcciones | ~/.config/evolution/addressbook/ | — |
| Calendarios | ~/.config/evolution/calendar/ | — |
| Configuración de correo | ~/.config/evolution/mail/ | — |
| Fuentes IMAP/POP | ~/.config/evolution/sources/ | — |

## Comandos básicos

- `evolution &` — abrir Evolution en segundo plano
- `evolution --force-shutdown --quit` — forzar cierre de Evolution
- `evolution --help` — ayuda general
