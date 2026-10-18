---
type: lpa
subtype: pattern
status: incubating
tags: [lpa, pattern]
created: 2026-07-24
---
# H-001: Obsidian como Knowledge Layer de Joko Lab

**Tipo:** Hipótesis LPA
**Fecha formulación:** 24 julio 2026
**Origen:** Conversación sobre Obsidian (vídeo de Marcos) + acumulación de conocimiento en semanas recientes
**Estado:** Formulada — pendiente de experimento

---

## Contexto

Hace unos días surgió la idea de usar Obsidian tras un vídeo de Marcos. La conclusión entonces fue: **no instalar todavía**. No había suficiente evidencia de que una herramienta de PKM aportase algo real al laboratorio. Era una hipótesis sin datos.

Desde entonces han pasado cosas:

- Hermes se ha consolidado como agente principal
- LPA ha generado patrones, candidate patterns, KNOWN, Patterns Observed
- Perfume IA ha producido iteraciones de diseño, sesiones documentadas, conversaciones con múltiples IAs
- Cada día aparecen ideas que luego cuesta localizar

**El problema que antes imaginábamos ahora existe de verdad.**

---

## Hipótesis

> Un sistema de conocimiento basado en archivos Markdown enlazados (Obsidian) puede convertirse en la **Knowledge Layer (KL)** de Joko Lab: una memoria navegable a largo plazo que sirva de soporte documental para Hermes y futuros agentes, sin sustituir a Hermes, ChatGPT ni al propio LPA.

---

## Lo que NO es

- NO es un sustituto de Hermes
- NO es un sustituto del LPA
- NO es "otra herramienta más que mantener"
- NO es una migración completa de todo el conocimiento existente

---

## Lo que SÍ aspira a ser

- Una capa de conocimiento persistente y navegable
- Un grafo de ideas interconectadas (aprovechando `[[wikilinks]]`)
- Un complemento a la memoria de Hermes (que es limitada y efímera)
- Un formato nativo que ya usa todo el ecosistema: **Markdown**

---

## Diseño del experimento

### Alcance inicial (mínimo viable)

Importar **solo el conocimiento LPA**:

- `/home/jokoalmi/perfume-ia/lpa/patterns-observed.md`
- `/home/jokoalmi/perfume-ia/lpa/pattern-incubator/`
- Principios LPA documentados
- KNOWN
- Candidate Patterns

### Duración

1-2 semanas de trabajo real con el vault como referencia.

### Criterios de éxito (falsables)

| Criterio | ¿Cómo se mide? |
|---|---|
| Recuperación de conocimiento más rápida | ¿Encuentro una idea antigua en < 30 segundos sin tener que preguntarle a Hermes? |
| Se forman relaciones nuevas | ¿Aparecen conexiones entre notas que no había visto antes? (backlinks, graph view) |
| Hermes puede usarlo como fuente | ¿Puedo decir "mira en el vault" y Hermes encuentra información relevante? |
| No añade fricción | ¿Mantener el vault cuesta menos de 5 minutos al día? |
| El conocimiento sobrevive a sesiones | ¿Una idea documentada hace 2 semanas se recupera sin esfuerzo? |

### Criterios de fracaso (para descartar)

- Mantener el vault se convierte en una carga
- La información está más dispersa, no menos
- Hermes no puede interactuar útilmente con el vault
- No se forman relaciones nuevas que justifiquen el grafo

---

## Decisión al final del experimento

- **Si ≥ 3 criterios de éxito se cumplen:** la hipótesis asciende a **patrón LPA**. Obsidian se adopta como Knowledge Layer oficial de Joko Lab. Se planifica migración gradual del resto del conocimiento.
- **Si ≤ 2 criterios se cumplen:** se descarta. Obsidian no es la herramienta adecuada para este rol. Se documenta por qué.
- **Si es ambiguo:** se amplía el experimento otras 2 semanas con ajustes.

---

## Principios LPA aplicados aquí

- **Experience Before Interface:** no se instala por el vídeo de Marcos, sino porque la experiencia real lo pide
- **Falsabilidad:** criterios claros para aceptar o descartar
- **Pattern over Tool:** no se decide sobre "Obsidian", se decide sobre "Knowledge Layer"
- **Minimum Viable Experiment:** solo LPA al principio, no todo el laboratorio

---

## Notas

- El skill `obsidian` ya existe en Hermes (`/home/jokoalmi/.hermes/skills/note-taking/obsidian/`)
- Obsidian no está instalado todavía en el sistema
- Todo el ecosistema Joko Lab ya trabaja en Markdown → compatibilidad nativa
- La variable `OBSIDIAN_VAULT_PATH` está sin definir — habrá que configurarla
- El graph view de Obsidian podría revelar conexiones no obvias entre patrones LPA
