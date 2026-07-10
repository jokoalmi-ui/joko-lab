# Decisión Técnica: Remoto Git local en SSD secundario

**Fecha**: 2026-07-10
**Estado**: Aceptada
**Área**: Infraestructura / Backups

## Contexto

El repositorio de Joko Lab (24 commits, 156 archivos) solo existía en el disco
principal (`/`). El auditor reportaba: "No hay remoto Git configurado. Solo existe
en este disco." El backup a GDrive mediante bundle git cubría el offsite pero
no protegía contra pérdida del disco principal entre backups.

## Problema

Un fallo del SSD principal entre las 3:00 y las 23:00 (ventana sin backup GDrive)
perdería todo el trabajo del día. No había un remoto local para push frecuente.

## Decisión

1. Crear un bare repo en el SSD secundario (`/mnt/ssd_ia_datos/hermes-lab.git`)
   como remoto `origin`.
2. Configurar upstream `origin/master` para tracking.
3. Añadir `git push origin master` como `ExecStartPost` en `joko-backup.service`,
   para que el push ocurra automáticamente tras cada backup diario.
4. GitHub queda pendiente como segundo remoto futuro (`github`).

## Motivos

- `/mnt/ssd_ia_datos` es un SSD independiente con 170 GB libres.
- El push automático tras backup garantiza que el remoto local esté siempre
  al día sin intervención manual.
- No requiere internet, autenticación ni servicios externos.
- El bundle a GDrive sigue cubriendo el offsite.

## Consecuencias

- Cada backup diario hará también `git push` al SSD secundario.
- Se elimina la ventana de pérdida de datos entre backups GDrive.
- El remoto local puede servir como fuente para clonar en otras máquinas
  de la red local.

## Referencias

- `scripts/auditor-completo.py` (sección 1.3: Remoto Git)
- `/etc/systemd/system/joko-backup.service`
- `docs/decisiones/2026-07-10-backups-systemd-timer.md`
