# Decisión Técnica: GitHub como remoto externo de hermes-lab

**Fecha**: 2026-07-14
**Estado**: Aceptada
**Área**: Infraestructura / Control de versiones

## Contexto
El repositorio `hermes-lab` solo tenía un remoto (`origin`) apuntando a
`/mnt/ssd_ia_datos/hermes-lab.git`, dentro de la misma torre física. Esto
protegía contra fallo del SSD principal, pero no contra incendio, robo o
fallo catastrófico de la torre completa.

## Decisión
Se añade un segundo remoto (`github`) apuntando a un repositorio privado
en GitHub: `git@github.com:jokoalmi-ui/joko-lab.git`.

Antes del primer push se verificó el historial completo de Git en busca de
secretos con un patrón estricto (palabra clave + valor alfanumérico de 20+
caracteres), con resultado de 0 coincidencias reales — confirmando que los
hallazgos previos del auditor eran falsos positivos.

## Motivos
- Cierra el riesgo de punto único de fallo físico sobre el historial de Git.
- El repo es privado; no expone la arquitectura del laboratorio públicamente.

## Consecuencias
- A partir de ahora, tras cualquier commit relevante, hacer también
  `git push github master` además del push a `origin`.
- Pendiente: automatizar este segundo push (cron o hook post-commit) para
  no depender de acordarse manualmente.

## Referencias
- `docs/decisiones/2026-07-13-...` (verificación de secretos, precedente)
