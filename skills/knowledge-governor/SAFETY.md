# knowledge-governor — Seguridad

## Reglas obligatorias

1. **Solo lectura por defecto.** Las 7 comprobaciones del governor son de solo lectura. No ejecutan cambios.
2. **No modificar documentación automáticamente.** El governor diagnostica y reporta; los cambios los decide el usuario.
3. **Los informes se escriben en `/tmp/`**, nunca sobre los archivos originales.
4. **Los hallazgos falsos positivos se corrigen en el script**, no silenciando las alertas.

## Riesgos conocidos

- El script `governor-check.sh` usa `grep -oP` con Perl regex. Si un archivo contiene patrones maliciosos, podría producir falsos negativos. No hay riesgo de ejecución de código.
- La comprobación de enlaces rotos depende del patrón regex. Si un enlace usa una sintaxis markdown no estándar, puede pasar desapercibido.
- La comprobación de changelogs usa `stat -c %Y` que es específico de Linux. En otros sistemas fallaría silenciosamente.

## Comandos prohibidos sin confirmación explícita

- `rm -f /tmp/knowledge-governor/*` — los informes pueden contener información útil para depuración
- Modificar archivos en `docs/`, `skills/` o `certification/` basándose solo en un reporte del governor — primero verificar manualmente cada hallazgo

## Límites

- knowledge-governor **no es fuente de verdad**. La fuente de verdad es `docs/`.
- Los reportes de governor son diagnósticos, no órdenes. Cada hallazgo debe verificarse antes de actuar.
- No superponerse con lab-manager: lab-manager prioriza y decide; knowledge-governor solo reporta.
