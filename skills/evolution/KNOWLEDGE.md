# evolution — Conocimiento

## Evolution

Evolution es el cliente de correo, calendario y contactos del escritorio GNOME.

- **Versión instalada:** 3.56.2
- **Ruta del binario:** `/usr/bin/evolution`
- **Proceso activo:** sí (confirmado)

## Almacenamiento

Evolution usa **Maildir** como formato de almacenamiento local.

- **Buzón local:** `~/.local/share/evolution/mail/local/`
- **Configuración:** `~/.config/evolution/mail/`
- **Fuentes/cuentas:** `~/.config/evolution/sources/`

### Estructura del buzón local

Cada carpeta visible en Evolution es un directorio **Maildir** dentro de `~/.local/share/evolution/mail/local/`:

- `cur/` — correos ya leídos
- `new/` — correos nuevos
- `tmp/` — correos en proceso

### Indexación

Evolution genera índices **ibex** (`.ibex.index` y `.ibex.index.data`) por carpeta para búsqueda rápida.

## Cuentas configuradas

| Cuenta | Tipo |
|--------|------|
| jokoalmi@gmail.com | IMAP + SMTP + Google |

## Carpetas locales relevantes

| Carpeta | Contenido |
|---------|-----------|
| ABANCA_A_MI | Correos recibidos de ABANCA |
| PRUEBAS_JUICIO | Correos de pruebas de juicio |
| PRUEBAS_JUICIO_CATEGORIA_PUESTO | Subtipo de juicio |
| PRUEBAS_JUICIO_ESPECIALISTA_RECICLADOR | Subtipo de juicio |
| PRUEBAS_JUICIO_GESTOR_HP | Subtipo de juicio |
| SEGUIMIENTOS | Correos de seguimiento |

## Diferencia con Betterbird/Thunderbird

- Evolution usa Maildir nativo (Betterbird/Thunderbird usa mbox por defecto)
- Evolution se integra con GNOME (calendario, contactos, online accounts)
- Betterbird/Thunderbird usa perfiles en `~/.thunderbird/`

## Búsqueda desde terminal

Los correos en Maildir son archivos de texto plano (formato RFC 822). Se pueden buscar con herramientas UNIX estándar:

- `grep -ril "texto" ~/.local/share/evolution/mail/local/*/cur/`
- Búsqueda por remitente: `grep -ril "^From:.*usuario" ~/.local/share/evolution/mail/local/*/cur/`
- Búsqueda por asunto: `grep -ril "^Subject:.*texto" ~/.local/share/evolution/mail/local/*/cur/`
