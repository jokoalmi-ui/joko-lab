# Bibliotecas de referencia externas (skills de agentes)

Directorio para **bibliotecas de skills externas clonadas** que NO se instalan
como skills activas en `~/.hermes/skills` (instalar cientos saturaría el
contexto de skills de cada sesión). Se consultan **bajo demanda**: primero el
índice/descripción, luego se lee solo la `SKILL.md` concreta que encaje.

## anthropic-cybersecurity-skills/

- **Fuente**: https://github.com/mukul975/Anthropic-Cybersecurity-Skills
  (32.143⭐, Apache-2.0, verificado 04-sep-2026)
- **Contenido**: 818 skills de ciberseguridad profesional en formato
  agentskills.io / Hermes (`skills/<nombre>/SKILL.md`, frontmatter YAML
  idéntico al de Hermes). Nivel profesional: SOC, DFIR, threat hunting,
  pentest, compliance, malware analysis, cloud, network.
- **Mapeos incluidos**: `mappings/mitre-attack/`, `mappings/nist-csf/`,
  `mappings/owasp/`, `mappings/attack-navigator-layer.json` (MITRE Navigator).
- **Índice**: `index.json` (818 skills, generado — NO editar a mano).
- **Versión local**: índice 1.1.0 (2026-08-24); clon shallow con `.git`.

### Cómo consultar (patrón del lab)

Buscar por descripción o tags en los frontmatter:

```bash
# ¿Hay skill para X? (busca en descripciones)
grep -ril "dns tunneling" ~/joko-lab/01-knowledge/references/anthropic-cybersecurity-skills/skills/*/SKILL.md
# alternativa con patrón de nombre
ls ~/joko-lab/01-knowledge/references/anthropic-cybersecurity-skills/skills/ | grep -i "<tema>"
```

Leer la skill concreta cuando la descripción encaje:

```bash
cat ~/joko-lab/01-knowledge/references/anthropic-cybersecurity-skills/skills/<skill>/SKILL.md
```

### Reglas

1. NO copiar skills de aquí a `~/.hermes/skills` salvo decisión explícita de
   instalar un subconjunto curado (y entonces con revisión de duplicados).
2. NO editar nada dentro de la biblioteca (es copia de upstream; actualizar
   con `git -C <ruta> pull`).
3. El cuerpo de cada skill puede citar APIs/CVEs: verificar contra fuente
   antes de afirmar (RULE-013/015 — las skills externas no están validadas
   por el lab salvo la consulta puntual).
4. Útil previsto: unidad FP de ciberseguridad, bootcamp BBK (inicio
   05/10/2026), tirith fail-closed, y práctica forense/SOC del lab.

### Registro

- 2026-09-04 — Añadida por auditoría de ZeroPointRepo/awesome-hermes-skills
  (decisión usuario: biblioteca bajo demanda, NO instalar 818 activas).
  Backup/verificación: clon shallow, 818 SKILL.md contados en destino.

## mattpocock-skills/

- **Fuente**: https://github.com/mattpocock/skills
  (248.639⭐, MIT, verificado 04-sep-2026)
- **Contenido**: paquete de ingeniería de Matt Pocock (agentskills.io).
  **37 SKILL.md reales** en el paquete (la auditoría del awesome-list decía
  23; el conteo real en destino incluye `skills/productivity/` +
  `skills/engineering/`). Formato: SKILL.md con frontmatter
  (`name`/`description`/`disable-model-invocation`) — compatible con Hermes,
  aunque su mecánica interna asume "Skill tool" (ecosistema Claude) y su
  tracker de issues.
- **Importante — no portadas como activas**: la mayoría duplica skills del lab
  (tdd, code-review, diagnosing-bugs ≈ systematic-debugging, grill-me ≈
  grill-idea, plan ≈ plan, to-tickets ≈ kanban, wayfinder está relacionado con
  cross-session-awareness). La auditoría recomendó solo 3 sin equivalente:
  1. `skills/productivity/writing-for-agents/SKILL.md` (+ `SKILL-MECHANICS.md`)
     — cómo escribir docs que los agentes siguen (meta-skill para redactar
     skills/SOUL.md/AGENTS.md con "leading words", sin duplicación, sin no-ops).
  2. `skills/engineering/wayfinder/SKILL.md` — planes demasiado grandes para una
     sesión → mapa de "decision tickets" en el tracker; resolver 1 por sesión.
  3. `skills/engineering/grill-with-docs/SKILL.md` — **router de 7 líneas** que
     delega en `skills/productivity/grilling/SKILL.md` (la entrevista real) +
     `skills/engineering/domain-modeling/SKILL.md` (+ `ADR-FORMAT.md` +
     `CONTEXT-FORMAT.md`) (escribe ADR/glosario). Para usar
     grill-with-docs hay que leer esas 2 dependencias.
- **Mecánica**: varias skills se auto-invocan ("Call the Skill tool twice"),
  asumen tracker de issues de GitHub y config `/setup-matt-pocock-skills`.
  En Hermes eso no aplica literalmente: consultar la SKILL.md concreta como
  referencia de procedimiento y adaptar a kanban local / herramientas del lab.

### Cómo consultar (patrón del lab)

```bash
ls ~/joko-lab/01-knowledge/references/mattpocock-skills/skills/*/   # ver paquetes
cat ~/joko-lab/01-knowledge/references/mattpocock-skills/skills/productivity/writing-for-agents/SKILL.md
cat ~/joko-lab/01-knowledge/references/mattpocock-skills/skills/engineering/wayfinder/SKILL.md
cat ~/joko-lab/01-knowledge/references/mattpocock-skills/skills/engineering/grill-with-docs/SKILL.md
cat ~/joko-lab/01-knowledge/references/mattpocock-skills/skills/productivity/grilling/SKILL.md
cat ~/joko-lab/01-knowledge/references/mattpocock-skills/skills/engineering/domain-modeling/SKILL.md
```

### Reglas

1. Igual que anthropic-cybersecurity-skills: NO copiar a `~/.hermes/skills`
   sin decisión explícita y sin revisión de duplicados (RULE-008).
2. NO editar dentro del clon (actualizar con `git -C <ruta> pull`).
3. Las referencias a "Skill tool"/setup de terceros NO aplican a Hermes:
   adaptar el procedimiento al lab (skill_view / kanban nativo / tools).

### Registro

- 2026-09-04 — Añadida (portado #2 de la auditoría; usuario: "Si, y explica
  que mejoras aportan"). Clon shallow, 37 SKILL.md contados en destino.

## planning-with-files/

- **Fuente**: https://github.com/OthmanAdi/planning-with-files
  (26.621⭐, MIT, verificado 04-sep-2026)
- **Contenido**: skill de planificación persistente en archivos (estilo
  Manus) + adaptador nativo Hermes. 18 SKILL.md en el repo (la canonical +
  i18n es/zh/de/ar + copias por agente). La versión que importa para el lab:
  - `.hermes/skills/planning-with-files/SKILL.md` — bundle Hermes nativo
    (237 líneas, escaneado SAFE por skills-guard; la canonical lleva hooks
    de Claude Code que Hermes clasifica como peligrosos — NO usar esa).
  - `.hermes/plugins/planning-with-files/` — plugin Python oficial Hermes
    (tools `planning_with_files_init/status/check_complete`, slash `/pwf`,
    hooks `pre_llm_call`/`post_tool_call`/`pre_verify`).
  - `docs/hermes.md` — guía de instalación/uso verificada contra Hermes
    v0.19.1 (el lab corre v0.21.0; hooks presentes en el código fuente).
- **Mecánica**: `task_plan.md` + `findings.md` + `progress.md` en el
  directorio del proyecto (NO en la skill); inyección del plan activo al
  inicio de cada turno; recuperación tras /clear/crash/compactación; gate
  opcional de completado (`pre_verify`, `agent.max_verify_nudges`).
- **Decisión del lab (04-sep)**: portado como BIBLIOTECA bajo demanda (NO
  instalado activo). Requisitos de una futura instalación activa: backup de
  `~/.hermes/skills` + `plugins/` + `config.yaml`, `hermes plugins install`,
  `plugins.enabled`, reinicio de gateway; coste ~330 tokens/turno con plan
  activo. No hay colisión con skills activas del lab (plan nativa no se
  sombrea: usa /pwf).

### Cómo consultar (patrón del lab)

```bash
# La skill nativa Hermes (leer esta, NO la canonical con hooks de Claude)
cat ~/joko-lab/01-knowledge/references/planning-with-files/.hermes/skills/planning-with-files/SKILL.md
# Guía de integración con Hermes + plantillas de plan
cat ~/joko-lab/01-knowledge/references/planning-with-files/docs/hermes.md
ls ~/joko-lab/01-knowledge/references/planning-with-files/.hermes/skills/planning-with-files/templates/
```

### Reglas

1. NO instalar como skill/plugin activo sin decisión explícita (toca
   `~/.hermes/skills`, `plugins/`, `config.yaml`, requiere reinicio).
2. Usar SIEMPRE el bundle `.hermes/` — la canonical
   (`skills/planning-with-files/SKILL.md`) lleva hooks de Claude Code con
   command substitution que el skills-guard de Hermes clasifica peligrosos.
3. NO editar dentro del clon (actualizar con `git -C <ruta> pull`).
4. Contenido de plan/plantillas: aplicar como patrón de procedimiento al
   kanban nativo / todo del lab (no duplicar herramientas).

### Registro

- 2026-09-04 — Añadida (portado #4 de la auditoría; usuario eligió opción B:
  biblioteca bajo demanda, NO instalar activo). Clon shallow, bundle `.hermes`
  verificado en destino.


## ai-slop-detector/

- **Fuente**: https://github.com/FeedHive/ai-slop-detector
  (71⭐, MIT, verificado 14-oct-2026 con la API de GitHub; último push
  2026-10-12T09:38:49Z, rama `main`).
- **Contenido**: 120 patrones que hacen que un texto suene a «AI slop», en 9
  categorías, cada uno con explicación, ejemplo malo y reescritura. Los 120
  están también como DATOS estructurados en `patterns.json` (`AI Slop
  Detector`, `version: 1.0.0`). Ficheros del clon (5 sin `.git`, medidos en
  destino el 14-oct-2026):
  - `patterns.json` (36992 B) — la lista completa por categoría: Vocabulary 20
    (V-01…), Stock phrases 15 (P-01…), Sentence patterns 22 (S-01…),
    Structure and rhythm 12 (R-01…), Imagery and metaphor 6 (M-01…),
    Substance 12 (C-01…), Formatting and punctuation 10 (F-01…), Chatbot
    residue 8 (B-01…), Social media and LinkedIn 15 (L-01…).
  - `skills/ai-slop-detector/SKILL.md` (22494 B) — el paquete como agent skill
    para Claude Code / Codex.
  - `README.md` (29129 B) — la misma lista en prosa, con los ejemplos.
  - `scripts/build.mjs` (4438 B) — regenera README + skill desde
    `patterns.json`; `LICENSE` (MIT, 1065 B).
- **Qué aporta al lab**: NO vocabulario nuevo (el skill `humanizer` ya cubre 34
  patrones de base Wikipedia y solapa en Vocabulary y Stock phrases); aporta
  las tres categorías que `humanizer` no tiene —Social media y LinkedIn 15,
  Formato y puntuación 10, Sustancia 12— y, sobre todo, un chequeo como DATOS:
  pasar un borrador por `patterns.json` y contar coincidencias, en vez de
  fiarse de la memoria del modelo.
- **Decisión del lab (14-oct-2026)**: portado como BIBLIOTECA bajo demanda
  (opción A del usuario: clon con `.git` + registro aquí). NO se instala como
  skill activa: no inyecta contexto en las sesiones.

### Cómo consultar (patrón del lab)

```bash
# Cuántos patrones tiene (control rápido del dato: 120)
python3 -c "import json;d=json.load(open('/home/jokoalmi/joko-lab/01-knowledge/references/ai-slop-detector/patterns.json'));print(sum(len(c['patterns']) for c in d['categories']))"
# La categoría que NO cubre humanizer (social media y LinkedIn: L-01 a L-15)
python3 -c "import json;d=json.load(open('/home/jokoalmi/joko-lab/01-knowledge/references/ai-slop-detector/patterns.json'));[print(p['id'],p['name'],'-',p['description']) for c in d['categories'] if c['id']=='social-media-and-linkedin' for p in c['patterns']]"
# La lista en prosa con ejemplos, y la skill empaquetada
less /home/jokoalmi/joko-lab/01-knowledge/references/ai-slop-detector/README.md
less /home/jokoalmi/joko-lab/01-knowledge/references/ai-slop-detector/skills/ai-slop-detector/SKILL.md
# Actualizar la biblioteca
git -C /home/jokoalmi/joko-lab/01-knowledge/references/ai-slop-detector pull
```

### Reglas

1. NO copiar a `~/.hermes/skills` ni instalar como skill activa sin decisión
   explícita (duplicaría lo que ya cubre `humanizer` y pagaría contexto en
   cada sesión).
2. NO editar dentro del clon (es copia de upstream; actualizar con
   `git -C <ruta> pull`).
3. Los 120 patrones están en INGLÉS: aplican mejor a vocabulario y estructura
   que a muletillas del castellano. Un patrón suelto es normal en escritura
   humana; lo que suena a slop es la acumulación en un mismo párrafo (criterio
   del propio repo).
4. Uso previsto: chequeo de borradores antes de enviarlos (serie editorial de
   LinkedIn, mensajes de presentación de ofertas).

### Registro

- 2026-10-14 — Añadida como biblioteca bajo demanda (el usuario eligió la
  opción A: clon con `.git` + registro en este README). Clon `--depth 1` en
  destino; HEAD `95d5507` (12-oct-2026 10:45:39 +0200); recuento real en el
  clon: 5 ficheros sin `.git`, 1 `SKILL.md`, 120 patrones en `patterns.json`.
  La ruta queda ignorada en git (`01-knowledge/references/ai-slop-detector/`
  en `.gitignore`), igual que las otras tres bibliotecas.
