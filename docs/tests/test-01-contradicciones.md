# Test 01 — Detección de contradicciones

**Fecha:** 2026-07-07
**Alcance:** HERMES.md, skills/joko-lab, skills/lab-manager, skills/docker-admin,
            skills/hermes-expert, skills/n8n-admin, skills/ai-router,
            skills/betterbird, skills/perfumes, skills/evolution,
            docs/estado-real.md, docs/arquitectura.md, docs/roadmap.md,
            docs/hermes-notes.md, docs/hermes-internals.md, docs/decisiones/

**Método:** Lectura cruzada de todos los documentos, comparando:
- Nombres de roles
- Etapas y versiones
- Estado de skills (vacía/poblada)
- Existencia de archivos referenciados
- Fechas de decisiones
- Datos concretos (versiones, puertos, rutas)

---

## Resultado: 8 contradicciones detectadas

### CONTRADICCIÓN 1 — lab-manager: "Arquitecto Permanente" vs "Arquitecto Técnico" (ALTA)

| Documento | Texto |
|---|---|
| lab-manager/SKILL.md (línea 3 y 11) | "Arquitecto **Permanente**" |
| lab-manager/COMMANDS.md (título, §115) | "Arquitecto **Técnico**" |
| estado-real.md (línea 100, 128) | "Arquitecto **técnico**" |
| joko-lab/SKILL.md (línea 83) | "lab-manager (nivel 2) — **Arquitecto técnico**" |

**Impacto:** Quien consulte lab-manager/SKILL.md pensará que el rol es "Arquitecto Permanente". Quien consulte COMMANDS.md o estado-real.md pensará que es "Arquitecto Técnico". Son dos nombres distintos para el mismo rol.

---

### CONTRADICCIÓN 2 — lab-manager: etapa 3 vs etapa 1 (ALTA)

| Documento | Dice |
|---|---|
| lab-manager/SKILL.md (línea 15) | Etapa **3 — Razonar** |
| estado-real.md (línea 149) | Etapa **3 — Razonar** |
| arquitectura.md (línea 134) | Etapa **1 — Comprender**, versión v0.1.0 |
| roadmap.md (línea 40) | "En desarrollo (etapa 1)" |

**Impacto:** arquitectura.md dice v0.1.0 cuando el SKILL.md dice v0.3.0. Roadmap lo clasifica como "en desarrollo (etapa 1)" cuando su propio SKILL.md y estado-real.md lo tienen en etapa 3. Un documento dice que lab-manager está empezando, otro dice que ya razona y audita.

---

### CONTRADICCIÓN 3 — betterbird, perfumes, evolution: "vacías" vs con SKILL.md (MEDIA)

| Documento | betterbird | perfumes | evolution |
|---|---|---|---|
| roadmap.md (línea 41) | Vacía | Vacía | Vacía |
| estado-real.md (línea 150-152) | Madurez 3 | Madurez 2 | Madurez 3 |
| arquitectura.md (línea 135-137) | Vacía | Vacía | Vacía |
| Sus propios SKILL.md | Etapa 2 | Etapa 1 | Etapa 1 |

**Impacto:** Las tres tienen SKILL.md con propósito, contexto y etapa definida. No están vacías. Roadmap y arquitectura.md no se actualizaron después de poblarlas.

---

### CONTRADICCIÓN 4 — docs/joko-lab-principles.md: "pendiente" vs "eliminado" (MEDIA)

| Documento | Dice |
|---|---|
| roadmap.md (línea 17) | Tarea #3: "Redactar docs/joko-lab-principles.md" — pendiente |
| estado-real.md (línea 175) | "Vacío" |
| arquitectura.md (línea 147) | "(vacío)" |
| Realidad en disco | El archivo **no existe** (fue eliminado) |

**Impacto:** Tres documentos hacen referencia a un archivo que ya no existe. roadmap.md lo marca como tarea pendiente cuando la decisión real fue eliminar el archivo porque su contenido se migró a HERMES.md.

---

### CONTRADICCIÓN 5 — docs/hermes-notes.md y docs/hermes-internals.md: "con contenido" vs esqueletos (BAJA)

| Documento | Dice |
|---|---|
| estado-real.md (línea 173-174) | "Con contenido" y "Con contenido antiguo" |
| arquitectura.md (línea 143-144) | Los lista como documentación relacionada |
| Realidad en disco | 7 líneas y 15 líneas, información desactualizada de julio |

**Impacto:** estado-real.md los presenta como si fueran documentos útiles. En realidad son esqueletos con notas antiguas. No hay contradicción entre documentos, pero sí entre lo que los documentos dicen y lo que contienen realmente.

---

### CONTRADICCIÓN 6 — ai-router.md con fecha 2026-07-08 en sesión 2026-07-07 (BAJA)

| Documento / Realidad | Fecha |
|---|---|
| estado-real.md (línea 188) | 2026-07-08-ai-router.md — Activa |
| Archivo en disco | 2026-07-08-ai-router.md |
| Sesión actual | 2026-07-07 |

**Impacto:** El archivo de decisión `2026-07-08-ai-router.md` existe en disco pero la sesión actual es 2026-07-07. Un archivo con fecha del día siguiente. Puede ser un error de fecha al crear el archivo o una decisión registrada antes de tiempo.

---

### CONTRADICCIÓN 7 — ai-router: v0.3.0 vs v0.4.0 (BAJA)

| Documento | Versión |
|---|---|
| ai-router/SKILL.md (línea 4) | v0.3.0 |
| estado-real.md (línea 148) | v0.4.0 |
| arquitectura.md (línea 133) | v0.4.0 |

**Impacto:** No se sabe cuál es la versión real. Puede que el SKILL.md no se haya actualizado tras el cambio de versión, o que estado-real.md y arquitectura.md estén adelantados.

---

### CONTRADICCIÓN 8 — Git: pendiente pero no comprobado (BAJA)

| Documento | Dice |
|---|---|
| estado-real.md (línea 20) | Git: ✗ Pendiente comprobar |
| roadmap.md (línea 18) | Tarea #4: "Comprobar Git" |
| Realidad | No se ha ejecutado ninguna comprobación |

**Impacto:** No hay contradicción entre documentos, pero sí entre lo que dicen que hay que hacer y el hecho de que no se ha hecho. Es una tarea pendiente que aparece en dos sitios sin avanzar.

---

## Lo que NO es contradicción

- **HERMES.md vs skills:** HERMES.md define principios generales. Ninguna skill los viola.
- **estado-real.md vs SKILL.md en stages:** La mayoría coincide. Solo lab-manager y ai-router tienen diferencias (ya listadas arriba).
- **docs/decisiones/ vs skills:** Las decisiones están registradas correctamente. No hay decisiones que contradigan lo que las skills hacen.

## Conclusión

**8 contradicciones detectadas.** 2 altas, 2 medias, 4 bajas.

Las dos altas afectan a lab-manager, la skill más importante del laboratorio.
Tener dos nombres distintos para su rol y dos etapas distintas en documentos
diferentes significa que cualquiera que consulte la documentación obtendrá
información contradictoria sobre qué hace lab-manager y en qué punto está.

**Corrección prioritaria:** unificar el nombre del rol en lab-manager/SKILL.md
y unificar la etapa en arquitectura.md y roadmap.md.
