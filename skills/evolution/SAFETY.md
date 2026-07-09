# evolution — Seguridad

## Reglas obligatorias

1. **No acceder a credenciales de correo** sin autorización explícita.
2. **No modificar configuraciones de cuentas** sin confirmación.
3. **No leer contenido de correos** sin autorización explícita del usuario.
4. **No enviar correos** sin confirmación explícita.
5. **No modificar ni borrar archivos del buzón** sin confirmación.
6. **No compartir información de correos** fuera del laboratorio.

## Riesgos conocidos

- Las credenciales de correo son información sensible
- Modificar configuraciones de cuentas (sources/*.source) puede romper el acceso al correo
- Borrar archivos del buzón local puede provocar pérdida de correos
- La búsqueda con `grep` es solo lectura y segura
- Leer el contenido de un correo con `cat` expone su contenido completo en terminal

## Zonas protegidas

- `~/.config/evolution/sources/` — configuraciones de cuentas (contienen credenciales)
- `~/.local/share/evolution/mail/` — buzón local (datos de correo)
