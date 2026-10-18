---
title: "Análisis — Alternativas open source a Lovable (19-ago-2026)"
type: research
---

# Análisis — Alternativas open source a Lovable (19-ago-2026)

**Origen:** recordatorio de investigación del cron (f79aecba29b4) — tema mencionado en julio 2026, pendiente de verificar.
**Método:** web_search + browser (OpenAlternative, actualizado 19-ago-2026) + **GitHub API verificada HOY 19-ago-2026** (stars, licencia, último push).
**VERACIDAD:** [VERIFICADO]

## Contexto: ¿qué es Lovable?

Hosted AI app builder: describes un producto en lenguaje natural y genera/despliega una web app full-stack (frontend + backend + BD) con un click. Genuino en "prompt → app funcionando" (fuente: open-design.ai). El ecosistema open source busca lo mismo pero self-hosted y con control del código.

## Ranking verificado (GitHub API, 19-ago-2026)

| Proyecto | Stars | Licencia | Último push | Lenguaje | Nota |
|---|---|---|---|---|---|
| **OpenHands** | 84.486 | MIT | **hoy** (19-ago) | Python | El más grande y activo. Agente de desarrollo IA |
| **Reflex** | 28.833 | Apache-2.0 | **hoy** (19-ago) | Python | Web apps en Python puro + AI builder + deploy |
| **Onlook** | 26.514 | Apache-2.0 | 22-jul | TypeScript | "El Cursor para diseñadores" — diseño visual AI-first |
| **Dyad** | 21.279 | NOASSERTION (fair-source FSL 1.1, NO 100% open) | **hoy** (19-ago) | TypeScript | App builder local "v0/Lovable/Replit/Bolt alternative" |
| **bolt.diy** | 19.767 | MIT | **07-feb-2026** (5 meses sin push ⚠️) | TypeScript | Fork open de Bolt.new — "usa cualquier LLM" |
| **Frontman** | 664 | NOASSERTION | **hoy** (19-ago) | ? | Joven (creado sep-2025), lo recomienda OpenAlternative |

## Notas importantes (honestas)

1. **OpenHands es el que manda por actividad** (84K stars, push HOY, MIT): es un agente de desarrollo autónomo (antes OpenDevin) — más "Claude Code/Codex open" que "Lovable clone", pero cubre el caso de uso "describe → el agente construye".

2. **Dyad es "fair-source", NO 100% open source**: su repo declara "all code within src/pro is fair-source licensed under Functional Source License 1.1 + Apache 2.0" — NOASSERTION en SPDX significa que NO tiene una licencia OSI estándar. Ojo: se vende como "open-source" en su propio README pero la parte pro no lo es. No llamarlo open source sin matiz.

3. **bolt.diy lleva 5 meses sin actualización** (07-feb-2026): el fork que "usa cualquier LLM" fue el más popular en 2025 pero puede estar estancado. A verificar si vuelve a actividad antes de recomendarlo.

4. **Reflex es el más alineado con el lab** (Python puro, Apache-2.0, activo): si el lab quisiera construir una app interna (ej. dashboard del lab, monitor), Reflex sería la vía natural sin salir de Python.

5. **Onlook es diseño visual** (26K stars): no es "generar la app completa" como Lovable, es editar UI visualmente con IA — otro caso de uso distinto (afinar el frontend, no crearlo desde prompt).

## 🎯 Aplicación al lab — ¿merece la pena?

**Veredicto honesto: NO urgente para el lab.**
- El lab NO desarrolla apps web comerciales — su producto es infraestructura de agentes (Hermes, n8n, RAG, LM Studio). El caso de uso "prompt → app completa" no encaja con lo que el lab produce hoy.
- Si mañana hiciera falta una app interna (dashboard de métricas, UI para el monitor LM Studio), la vía natural sería **Reflex** (Python, Apache, activo) — no Lovable ni sus clones.
- **OpenHands** sí es interesante como herramienta de desarrollo asistido (84K stars, MIT, activo) — el equivalente open del agente de código, para cuando el lab delegue desarrollo a subagentes de verdad (futurible ya mapeado en graph-lab).
- **No recomendar Dyad ni bolt.diy sin matices**: Dyad no es 100% open; bolt.diy está estancado desde febrero.

## Fuentes
- https://openalternative.co/alternatives/lovable (actualizado 19-ago-2026, lista 3: Reflex, Dyad, Frontman)
- GitHub API: repos reflex-dev/reflex, dyad-sh/dyad, openhands/openhands, stackblitz-labs/bolt.diy, onlook-dev/onlook, frontman-ai/frontman (19-ago-2026)
- https://open-design.ai/alternatives/lovable (definición de Lovable)

## Veredicto
**INFORMATIVO / NO ACCIONABLE AHORA.** Alternativas open source a Lovable existen y son sólidas (OpenHands 84K, Reflex 28K, ambos activos y con licencia limpia), pero el caso de uso no encaja con el lab actual. Guardar como referencia para: (a) app interna futura → Reflex; (b) desarrollo asistido → OpenHands. No implementar nada ahora.
