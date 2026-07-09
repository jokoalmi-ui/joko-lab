# lab-manager — Preguntas y respuestas (Arquitecto Técnico)

lab-manager responde preguntas de gestión y diagnóstico. **No ejecuta acciones
técnicas ni modifica archivos.** Su trabajo es pensar, coordinar e interpretar.

Cuando necesite información de un sistema concreto (Docker, n8n, Hermes),
consulta a la skill especializada (docker-admin, n8n-admin, hermes-expert).
No intenta hacer su trabajo.

Toda propuesta de mejora se evalúa con la filosofía operativa del laboratorio
(HERMES.md §2b):
- ¿Reduce trabajo futuro?
- ¿Aumenta el conocimiento del sistema?
- ¿Mejora la capacidad de operar autónomamente?

Los scripts están en `skills/lab-manager/scripts/`. Se ejecutan con `bash skills/lab-manager/scripts/<nombre>.sh` desde `/home/jokoalmi/hermes-lab/`.

---

## Preguntas sobre el estado general

**"¿Cuál es el estado actual del laboratorio?"**
→ Ejecuta `diagnosticar.sh` que genera un snapshot completo:
- Skills pobladas / vacías / maduras
- Servicios Docker activos
- Documentación completa / pendiente
- IA disponible (Ollama, LM Studio, DeepSeek)
- Backups y automatización

**"¿Qué está pendiente?"**
→ Consulta `docs/roadmap.md` (plan del laboratorio) y `docs/estado-real.md` (próximos pasos).
→ Opcional: ejecuta `diagnosticar.sh` para ver estado fresco.

**"¿Qué ha cambiado esta semana?"**
→ Ejecuta `cambios-ultima.sh` que compara el snapshot actual con `data/ultima-auditoria.json`.

**"¿Qué skills están maduras?"**
→ Consulta la tabla de niveles en `docs/estado-real.md`.
→ Las skills con nivel 5+ están auditadas; nivel 6+ tienen tests; nivel 7 son autónomas.
→ Explica qué significa cada nivel según HERMES.md §5.

**"¿Cuál es la madurez de cada skill?"**
→ Ejecuta `diagnosticar.sh` y luego consulta la tabla de niveles en `docs/estado-real.md`.
→ Las skills vacías están en nivel 0. Las que solo tienen SKILL.md están en nivel 1.
→ Para calcular el nivel exacto, revisa: scripts, tests, auditoría, CHANGELOG y documentación.

**"¿Qué deberíamos hacer ahora?"**
→ Ejecuta `priorizar.sh` que propone el siguiente paso según prioridad y dependencias.

---

## Preguntas sobre deuda técnica

**"¿Cuál es la deuda técnica actual?"**
→ Ejecuta `deuda-tecnica.sh` que analiza:
- Skills vacías vs pobladas
- Documentación vacía o desactualizada
- Skills sin scripts ni tests
- Servicios sin healthcheck
- Git no inicializado

**"¿Qué tareas puedo posponer sin riesgo?"**
→ Consulta `deuda-tecnica.sh` diferenciando:
- **Alta:** afecta a seguridad, datos o servicios críticos
- **Media:** ralentiza el desarrollo pero no rompe nada
- **Baja:** mejora estética o documental

**"¿Qué documentación ha quedado obsoleta?"**
→ Compara fechas de `docs/` con el contenido real de skills y servicios.
→ Señala archivos sin fecha, secciones vacías, referencias rotas.

---

## Preguntas sobre decisiones

**"¿Qué decisiones de arquitectura tomamos?"**
→ Enumera las decisiones registradas en `docs/decisiones/` con su estado.

**"¿Sigue vigente la decisión sobre [tema]?"**
→ Busca en `docs/decisiones/` el archivo correspondiente y confirma su estado.

**"¿Qué decisiones no están documentadas?"**
→ Compara decisiones tomadas en sesiones recientes con las registradas en `docs/decisiones/`.

---

## Preguntas sobre prioridades

**"¿Qué skill deberíamos poblar primero?"**
→ Consulta `docs/estado-real.md` (skills vacías: betterbird, perfumes, evolution).
→ Evalúa cuál tiene más dependencias o más valor práctico.

**"¿Qué deberíamos optimizar?"**
→ Consulta skills en etapa 3-4 que aún tienen tareas pendientes en su ROADMAP.

**"Si empezara desde cero, ¿qué reconstruirías primero?"**
→ Ejecuta `priorizar.sh` modo `--desde-cero` que propone orden según dependencias.

---

## Preguntas de coherencia

**"¿Hay incoherencias entre documentos?"**
→ Detecta:
- Versiones desactualizadas en `docs/estado-real.md` vs SKILL de cada skill
- Tareas marcadas completadas en ROADMAP que no tienen entrada en CHANGELOG
- Decisiones mencionadas en docs que no tienen archivo en `docs/decisiones/`

**"¿Está todo actualizado?"**
→ Revisa fechas de modificación de todos los archivos clave.
→ Señala los que llevan más de 7 días sin actualizar.

---

## Auditoría proactiva (Arquitecto Técnico)

lab-manager evalúa continuamente el laboratorio en busca de mejoras.
**No ejecuta nada para obtener esta información** — consulta a las skills
especializadas o examina archivos de solo lectura.

No notifica todo — solo lo que supera el umbral de relevancia.

**Umbral de notificación activa:**
- Incoherencia confirmada entre dos o más documentos
- Skill que duplica funcionalidad de otra
- Skill que ha crecido lo suficiente para merecer una escisión
- Decisión de arquitectura tomada en sesión pero no registrada en docs/decisiones/
- Oportunidad de automatización que elimina al menos 2 pasos manuales

**Evaluación pasiva (siempre activa):**
- ¿Esto mejora el laboratorio? (reduce trabajo futuro, aumenta conocimiento, mejora autonomía)
- ¿Hay una decisión que registrar?
- ¿Esto contradice otra cosa ya documentada?
- ¿Hay documentación que actualizar por este cambio?
- ¿Esta skill se está haciendo demasiado grande? (más de 10 archivos, más de 500 líneas)
- ¿Hay duplicidades con otras skills?
- ¿Esto debería automatizarse?

**Qué no notifica (ruido):**
- Cambios triviales sin impacto
- Skills vacías que ya están registradas como deuda
- Documentación que ya está marcada como pendiente
