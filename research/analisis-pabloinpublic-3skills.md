---
title: "Análisis — Reel pabloinpublic: \"3 skills que le meten oficio a tu agente\" (25-ago-2026)"
type: research
---

# Análisis — Reel pabloinpublic: "3 skills que le meten oficio a tu agente" (25-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://www.instagram.com/reel/DcbvvzNuSQ6/ (pabloinpublic, 24-ago, 461 likes, 807 comentarios)
**Método:** caption completo + verificación web de los 3 repos GitHub (web_search)

## El post
"Tu agente escribe como una IA. Y programa a lo loco. 3 skills que le meten oficio:
- Humanizer — 37.597★ — textos que suenan a persona
- mattpocock/skills — 235.130★ — ingeniería, no vibe coding
- addyosmani/agent-skills — 89.445★ — hábitos de senior
Comenta 17 y te paso las 17" → **bait** (DM para la lista), pero los recursos son reales.

## Verificación de los 3 repos (web_search, no inventado)

### 1. Humanizer (blader/humanizer + Aboudjem/humanizer-skill)
- **blader/humanizer**: "Agent skill that removes signs of AI-generated writing from text". Plugin `/humanizer:humanizer`, se instala como ZIP/skill en Claude Desktop/Code/Cursor/Codex/opencode.
- **Aboudjem/humanizer-skill**: "53 patterns, 5 voices, 0-100 AI-tell score. Pure Markdown, zero dependencies. Works in Claude Code, Cursor, Codex, opencode y 70+ editores."
- El número 37.597★ no coincide exactamente con un repo concreto en los resultados, pero la categoría "humanizer" es real y hay varios repos con miles de estrellas.

### 2. mattpocock/skills — ✅ VERIFICADO (235.0k★, GitTrend)
- "Skills for Real Engineers. Straight from my .agents directory." — 21-53 skills que incorporan disciplina de ingeniería real (no vibe coding): enfoque crítico con GSD/BMAD/Spec-Kit ("te quitan el control y hacen los bugs difíciles de resolver").
- Publicado también como plugin oficial en Claude (claude.com/plugins/mattpocock-skills).
- Matt Pocock = referente de TypeScript (Total TypeScript, 300k+ en YouTube).

### 3. addyosmani/agent-skills — ✅ VERIFICADO (89.2k★, GitStarClub)
- "Production-grade engineering skills for AI coding agents. Skills encode the workflows, quality gates, and best practices that senior engineers use."
- 19-32 skills, MIT License.
- Addy Osmani = ex-Google Chrome, autor de "Learning JavaScript Design Patterns", referente senior de ingeniería web.

## 🔴 Aplicación al LAB

| Recurso | Estado en el lab | Veredicto |
|---|---|---|
| **Humanizer** | ✅ **YA INSTALADO**: skill `humanizer` en Hermes ("strip AI-isms and add real voice") | 🟢 Validación — ya lo tienes |
| **mattpocock/skills** | 🟡 El lab YA sigue el patrón: verificación > asumir, gates, TDD, systematic-debugging, refactor-seguro, revisar-decisiones | 🟢 VALIDACIÓN del enfoque "no vibe coding" |
| **addyosmani/agent-skills** | 🟡 El lab YA tiene gates propios: tirith fail-closed, RULE-008 backups, joko-git-recibos, gate veracidad, estado-verificación | 🟢 VALIDACIÓN de los quality gates |

**Veredicto: VALOR MEDIO — validación, sin futuribles nuevos.**
- Los 3 recursos son reales (verificados) y el post los presenta bien, pero el contenido está detrás del DM (bait).
- **El lab ya tiene los 3 conceptos**: humanizer instalado, disciplina de ingeniería (skills de proceso), y gates de calidad propios.
- La señal interesante: **los referentes de la industria (Matt Pocock, Addy Osmani) usan exactamente el mismo patrón que el lab** — skills de proceso + gates + verificación. Es validación externa del diseño del lab (como IBM Digital Librarian el 24-ago).

## Opcional (si el usuario quiere profundizar)
Revisar `mattpocock/skills` y `addyosmani/agent-skills` por si alguna skill concreta (p.ej. code-review, debugging, testing) añade algo a las 164 del lab. Coste: ~30-60 min de lectura de los .agents. No urgente.

## Sin futuribles nuevos — registro como validación
El lab ya cubre los 3 patrones. No se instala nada (el lab no usa Claude Code como agente principal; Hermes ya tiene la skill humanizer).
