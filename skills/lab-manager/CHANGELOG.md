# lab-manager — Changelog

## 2026-07-07 — v0.3.0 — Arquitecto Permanente

### Madurez de skills (niveles 0-7)
- Escala de madurez implementada en `deuda-tecnica.sh`
- Cada skill se evalúa automáticamente de nivel 0 (vacía) a nivel 7 (autónoma)
- Deuda técnica ahora se calcula en función del nivel real, no de categorías genéricas

### Auditoría proactiva
- lab-manager ahora evalúa continuamente el laboratorio en busca de mejoras
- Umbral de relevancia: solo notifica incoherencias, duplicidades, oportunidades de automatización y decisiones no registradas
- No notifica ruido (skills vacías ya registradas como deuda, cambios triviales)

### Documentación
- HERMES.md: escala de madurez añadida a sección 5
- HERMES.md: filosofía operativa añadida como principio 2b (toda mejora debe: reducir trabajo futuro, aumentar conocimiento, mejorar autonomía)
- docs/estado-real.md: tabla de skills ahora muestra niveles 0-7 en lugar de estados genéricos
- COMMANDS.md: nuevas preguntas de madurez y auditoría proactiva, filtro de relevancia documentado

### Filosofía operativa
- Nueva regla de filtro para toda propuesta de mejora en COMMANDS.md
- Aplicable a cualquier skill del laboratorio

## 2026-07-07 — v0.2.0 — Director Técnico

### Rol evolucionado
- lab-manager pasa de skill de gestión pasiva a **Director Técnico** del laboratorio
- Ahora diagnostica, audita, prioriza y responde preguntas complejas

### Nuevos scripts (etapa 2 — Diagnosticar)
- `scripts/diagnosticar.sh` — snapshot completo de estado del laboratorio
- `scripts/deuda-tecnica.sh` — calcula y cuantifica la deuda técnica
- `scripts/cambios-ultima.sh` — diff entre el estado actual y la última auditoría
- `scripts/priorizar.sh` — propone orden de reconstrucción (modo normal y --desde-cero)

### Infraestructura
- `data/ultima-auditoria.json` — primer snapshot de referencia para comparativas

### Documentación actualizada
- `SKILL.md` — nuevo propósito, capacidades, reglas y relación con otras skills
- `COMMANDS.md` — rutas corregidas a `docs/`, nuevos scripts, preguntas expandidas
- `CHANGELOG.md` — este archivo

### Incoherencias corregidas
- `docs/estado-real.md`: fecha actualizada, docs/arquitectura marcado como completo, cuenta de decisiones corregida (8 archivos, 2 activas)
- `docs/arquitectura.md`: cuenta de decisiones corregida, roadmap añadido a docs relacionados, pendiente "3 huecos" eliminado

## 2026-07-07 — v0.1.0

### Creación de la skill
- SKILL.md: propósito, alcance, relación con otras skills, regla de 4 criterios para propuestas de mejora
- COMMANDS.md: preguntas que responde (estado, documentación, decisiones, prioridades, coherencia)
- README.md: explicación para humanos
- docs/decisiones/2026-07-07-regla-justificacion-mejoras.md: registro de la decisión

### Refactor por principio de propiedad documentación
- Inventario global movido de KNOWLEDGE.md a docs/estado-real.md (fusionado)
- Roadmap general movido de ROADMAP.md a docs/roadmap.md
- KNOWLEDGE.md convertido en enlace a docs centralizados
- ROADMAP.md convertido en enlace a docs/roadmap.md
- docs/decisiones/2026-07-07-formato-auditoria-puntuacion.md: registro del formato de auditoria con puntuacion global y barras visuales
