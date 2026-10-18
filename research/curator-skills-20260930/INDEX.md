---
title: "Evidencia de la sesión del 30-sep-2026 — triaje de los 4 posts de IG y forense del curador de skills"
type: research
---

# Evidencia de la sesión del 30-sep-2026

**VERACIDAD:** [ALCANCE INTERNO]
**Origen:** `/tmp/ig-4posts` (directorio de trabajo de la sesión del 30-sep-2026, volátil: se
pierde al reiniciar). Copiado al lab con `keeper_traslado.py` el 30-09-2026 20:30 CEST:
**27 ficheros, 238.114 B**, verificados byte a byte contra el origen (`cmp`, además de tamaño
y md5 en la propia copia). Medidas fichero a fichero en `MANIFEST.txt`.
**Ámbito:** este paquete cubre DOS líneas de trabajo de la misma sesión. El slug nombra la
principal (el curador); la otra es el triaje de los 4 posts de Instagram del vigilante.
Si en el futuro molesta el nombre, el paquete no cambia de contenido (renombrar es `mv`: exige OK).

## Qué hay aquí

| Subcarpeta | Ficheros | Qué es |
|---|---|---|
| `evidencia/` | 17 | Productos de **medida cruda** de la sesión: volcados de los 4 posts (`raw1-3.json`), estado previo del registro de uso, trazas del RAG/chunking, menciones de skills en los logs, actores del ledger del curador, recuentos reales (RULE/OBS), blobs del curador y el diff de los volcados intermedios |
| `scripts-de-la-sesion/` | 10 | Los scripts que **produjeron** los cambios: forense del curador, rectificaciones de RULE-018 (dos pases), anexo de OBS-154, altas de OBS/pendiente y los tres scripts de commit con recibo |

## Qué respalda (y qué NO)

**Sí respalda los hechos que quedaron en los documentos durables:**
- La medida de la que salieron las cifras del addendum de `OBS-154` (`medir_ko.txt`,
  `medidas2.txt`, `counts.txt`): ledger con **1754 filas** a las 16:41 (`agent` 416 /
  `curator` 1338), **2716 blobs** en `.curator_backups/blobs/`.
- El cómputo rectificado de `RULE-018` (32→**30** nombres en la lista de supresión;
  2713→**2716** blobs): el error y su re-medida con instrumento directo.
- El material que el curador **generalizó después como plantillas de skill**
  (`templates/edicion-anclas.py` desde `fix_rule018_figs.py`; `diff` de 247 líneas) y la
  procedencia de `references/edicion-correctiva-y-cifras.md`.

**NO respalda (dicho aquí para que nadie lo cite de más):**
- **No es prueba de la autoría**: la autoría se lee en `~/.hermes/skills/.curator_ledger.jsonl`
  (campo `actor`), que es durable y sigue creciendo. Este paquete es la **traza de derivación**
  de la sesión, no el registro oficial.
- **No es un corte congelado de los documentos citados**: `OBS-154` y `RULE-018` viven en
  `01-knowledge/` con sus propios backups (`.bak-obs154-addendum-drift-20260930`,
  `.bak-20260930-figs`) y sus commits (`2cda2aa`, `1a2421a`); aquí no se duplican.
- Las cifras de los volcados son **fotos con su hora**, no valores actuales.

## Qué NO se ha copiado (y por qué)

Del directorio original de 64 ficheros / 512 K:
- **Logs de dry-run y apply** (`dry_*`, `apply_*`, `verif*`, `final*`, `commit*.log`, `alta.log`):
  el laboratorio no versiona logs de ejecución intermedios y son regenerables ejecutando el script.
- **5 duplicados exactos** (pares `<x>_read`/`<x>` idénticos por md5): se conservó una copia.
- **Volcados de recon intermedios** (`recon*.txt`, `obs_recon*.txt`): superados por
  `medir_ko.txt` / `counts.txt`, y re-derivables del ledger.
- **`OBS-154.draft.md`**: ocupa exactamente lo que el backup pre-addendum del OBS versionado.

## Cómo se usa

- Forense en vivo: `python3 tools/auditar_curador_skills.py --horas 48`
  (solo lectura; resume el ledger por actor/skill/sesión, lista los volcados intermedios y
  mide el estado en disco de lo tocado).
- Commit con recibo: `bash 03-automation/scripts/commit-con-recibo.sh --fichero <ruta>
  --mensaje "<msg>"` (dry-run por defecto; `--apply` y `--push` son explícitos).
