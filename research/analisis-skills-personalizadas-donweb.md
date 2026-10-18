---
title: "Análisis — Skills personalizadas para Claude (Donweb Cloud / Triple A, 15-ago-2026)"
type: research
---

# Análisis — Skills personalizadas para Claude (Donweb Cloud / Triple A, 15-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://www.youtube.com/live/qc8hQ6teb9U (taller ~1h20m, Donweb Cloud, instructor Ezequiel)
**Transcripción:** completa (es)

## Qué enseña el taller
Cómo crear y aplicar skills de Claude en proyectos reales. Lo relevante NO es Claude — es la METODOLOGÍA de crear skills (aplicable a Hermes, que es el harness del lab).

## Concepto central
- **Skill vs prompt**: un prompt sirve una sola vez (ventana de contexto); una skill es conocimiento empaquetado y reutilizable que el modelo activa SOLO cuando la descripción "matchea" la petición.
- **Una skill = UNA habilidad** (específica y general a la vez: específica en qué hace, general en que se reutiliza en N proyectos).

## Anatomía de una skill bien armada (el núcleo)
1. **Descripción de activación MUY específica**: "Usar cuando el usuario pida crear, editar o analizar archivos .docx" — si leyendo SOLO la descripción no puedes adivinar cuándo se activa, el modelo tampoco. Descripción ambigua = skill muerta (nunca matchea).
2. **Reglas**: el proceso paso a paso (como receta de cocina): qué, cuándo, dónde, cómo.
3. **Límites (más importantes que las reglas)**: qué NO debe hacer NUNCA. La IA no tiene contexto humano (agua caliente → la traes en algo térmico; la IA haría lo literal). Explicitar límites = evitar alucinación y errores.
4. **Ejemplos (lo más valioso)**: casos reales de cómo se hizo antes (cliente enfadado/feliz/dudoso...). "Los ejemplos son la mejor manera de entrenar cualquier modelo/herramienta."

## Errores comunes (checklist de lo que NO hacer)
- Descripción genérica ("ayúdame con X" no sirve — no le dice nada)
- Skills que se pisan (descripciones parecidas compiten por el mismo caso → unificar o diferenciar)
- Meter demasiado en una skill (deja de ser skill y pasa a ser prompt)
- No probarla en conversación NUEVA (crear y asumir que funciona sin verificar)

## Cómo detectar una skill muerta
- Mirar los **logs**: si el modelo intenta buscar la skill y aparece en rojo → no funciona
- Si "corrige" algo sin la skill → puede estar **alucinando** (cuidado)

## Aplicación práctica mostrada
Skill "curador de paleta tinta negra" para una landing de estudio de tatuajes: revisa el copy contra el tono de marca, propone cambios (con explicación y permiso previo, no aplica directo), corrige textos ambiguos ("no tatuamos menores" → "tampoco con autorización"), boilerplates legales.

## Casos de uso propuestos (ideas aplicables)
- **Revisor de tono de marca** (chequea cualquier texto contra la voz de la empresa — web, post, mail, carta)
- Generador de reportes con estructura fija
- Checklist de calidad antes de dar por terminado
- Seguridad básica (revisa archivo por archivo vulnerabilidades)
- **Criterio del rubro** (reglas específicas de tu industria que el modelo debe respetar siempre, en cada proyecto nuevo)

## Veredicto para el lab
**VALIDA DIRECTAMENTE el sistema de skills de Hermes/Joko Lab — el lab ya sigue exactamente esta metodología:**
- Descripciones específicas de activación = frontmatter `description` de las 136 skills del lab ✅
- Reglas + límites = secciones "Cuándo usar" / "Pitfalls" de las skills del lab ✅
- Ejemplos = las skills del lab incluyen casos reales verificados ✅
- Detectar skill muerta = el lab YA tiene `detectar-sin-uso` (watchdog semanal) ✅
- "No meter demasiado en una skill" = la regla del límite de 100K chars (skill_manage lo avisa) ✅

**Aportes concretos (2 ideas menores, no urgentes):**
1. **Checklist "14 preguntas base"** para crear skills formalmente — el lab tiene `hermes-agent-skill-authoring` pero un checklist de preguntas (¿cuándo se activa? ¿qué reglas? ¿qué límites? ¿ejemplos?) puede formalizar aún más la creación.
2. **Skill "revisor de tono de marca"** aplicable al lab: el estilo de contenido YA está decidido (texto+gráficos en español tipo maurys) — una skill que revise cualquier contenido público contra ese estilo (como hace formato-carrusel-maurys.md pero como skill ejecutable).

**NO accionable técnicamente**: el lab no usa Claude; el patrón ya está implementado en Hermes. El taller confirma la metodología, no aporta nada nuevo estructural.

## Registro
- Guardado: research/analisis-skills-personalizadas-donweb.md
- Futuribles: (1) checklist formal de creación de skills; (2) skill de revisión de tono de marca/estilo para contenido del lab.
