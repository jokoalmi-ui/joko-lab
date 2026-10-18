---
title: "Análisis — \"Alucinaciones de IA durante el desarrollo: por qué pasan y la solución\" (Gentleman Programming, 01-sep-2026)"
type: research
---

# Análisis — "Alucinaciones de IA durante el desarrollo: por qué pasan y la solución" (Gentleman Programming, 01-sep-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://youtu.be/38Y1JWU-mdE (@gentlemanprogramming, stream ~26 min, transcripción completa 30 KB)
**Fecha:** 2026-09-01 22:40 CEST (verificada con `date`)

## Contenido — los problemas de la auto-revisión con IA y su stack de solución

**Premisa**: los agentes hacen el código muy bien, pero **a la hora de revisar alucinan** — "si el agente es autor, revisor y juez de su propio trabajo, es lo mismo que autoaprobarte en el trabajo".

### Los 4 problemas que detecta (del propio stream)

1. **Loops infinitos de review**: el agente revisa, encuentra algo NUEVO aparte de lo que debía revisar, lo arregla, y entra en bucle eterno.
2. **Findings persuasivos pero FALSOS** (la alucinación central): el revisor reporta un "crítico" que en realidad **no existe**.
3. **Autoaprobación / psicología de confirmación**: dentro de su propio contexto, lo que hizo "está bien"; el big picture externo lo desmiente.
4. **Findings que desaparecen**: encuentra un problema, lo "soluciona", y en la siguiente iteración ya no aparece.

### La solución (su stack, herramienta propia "Gentel")

| Pieza | Qué hace | Equivalente en el lab |
|---|---|---|
| **Refutador** (subagente) | Revisa el finding en SU PROPIA sesión: recibe el target inmutable (JSON: "esta es la problemática con este código"), **busca evidencias y TRATA DE REPLICARLO** → devuelve **Corroborado / Refutado / Inconcluso** | Verifier independiente del kanban + gates fail-closed (el lab verifica con curl + web_search, no con un subagente que replica) |
| **Clasificación del finding** | Determinista (un test que falla → no hay que refutar, ir a arreglarlo) · Inferencia (se infiere problema futuro) · Insuficiente (no hay pruebas → warning/suggestion, se guarda) | Fail-closed del lab (si no hay evidencia, no pasa) |
| **Corrección acotada** | "Arregla SOLO esto, código mínimo, una transacción" — evita el loop infinito | Mejora A del PRD graph (encadenar por señal) |
| **Juez con modelo propio + máx 2 rondas** | Cada juez puede usar un modelo distinto; máximo 2 iteraciones, luego **se escala al orquestador** | "2 vueltas máx" del graph-lab (bucle revisor→redactor máx 2) |
| **Gates** (pre-commit, pre-push, pre-release, post-apply) | Cada compuerta valida el "recipt" (huella digital del fix) | **Gates de commit del lab: `joko-git-recibos`** (recibos git verificables) + RULE-008 backups + gate de código PIL |
| **Recipt** (recibo) | Al terminar, el sistema emite un recibo: "está todo perfecto" con evidencia (tests, runtime) o rollback; **el orquestador NO deja commitear sin recipt** | **Recibos git del lab** (joko-git-recibos) + verificación ad-hoc con evidencia persistente |
| **Validador del delta** | Tras el fix, valida SOLO las líneas que tocó el fix (no todo el código) | SVP-diff del refactor gobernado (revisar alcance del diff vs backup) |
| **Hash/huella digital por unidad de trabajo** | Evidencia de cada unidad: "arreglé, hice tests, runtime OK, o rollback" | State-verification-pattern (SVP) del lab |

## 🔴 Aplicación al LAB — VALOR MEDIO-ALTO (validación fuerte + 1 idea parcialmente nueva)

| Ángulo | Veredicto |
|---|---|
| **"Autor, revisor y juez del propio trabajo = alucina"** | 🟢🟢 **Es la tesis central del lab**: el verifier del kanban es independiente (maker-checker), el revisor del graph-lab es SIEMPRE en sesión y nunca el mismo agente que redactó. Validación externa directa de la regla F4/delegación |
| **Findings persuasivos pero falsos** | 🟢🟢 = el patrón "autoinforme de subagente" del lab (deleg_92baa5c2: "éxito" con archivo inexistente; 3 subagentes con tablas fabricadas). El lab ya lo mitiga con verificación de artefacto en disco + gate fail-closed |
| **Loops infinitos de review** | 🟢 El lab lo evita con "máx 2 vueltas" del graph + Mejora A (encadenar por señal); el vídeo lo resuelve con corrección ACOTADA (arregla solo lo dicho) — matiz útil |
| **Refutador que REPLICA el finding** | 🟡 **Idea parcialmente nueva**: el lab verifica con curl/web_search/artefacto-en-disco, pero NO tiene un subagente que intente REPLICAR el problema reportado en su propia sesión (corroborado/refutado/inconcluso). Es el paso natural del verifier del kanban hacia "verificación activa" en vez de "inspección pasiva". Futurible DÉBIL (el lab ya cubre la función con sus gates; el refutador añadiría coste cloud sin mejora clara hoy) |
| **Recipt = recibos git del lab** | 🟢🟢 **Validación directa**: el lab ya implementa el concepto (joko-git-recibos: no commitear sin recibo verificable) — el vídeo describe exactamente eso como "recipt" |
| **Corrección acotada (solo las líneas del fix)** | 🟢 = SVP-diff del refactor gobernado (revisar alcance del diff, no el código entero) |
| **Ahorro de tokens por hacerlo bien** | 🟢 Coincide con la medición del lab (99,6% del coste es prompt; no romper cache; los errores corregidos tarde cuestan más) |

**Conclusión**: validación fuerte del diseño de verificación del lab (verifier independiente, gates, recibos). El único matiz nuevo es el **refutador que replica** (verificación activa vs pasiva) — futurible débil, no implementar hoy (el lab ya cubre la función; coste cloud sin mejora clara).

## Notas de honestidad

- **Stream sin edición** (el autor lo dice explícitamente: "este video va a ir sin edición") — hay ruido, bromas y divagaciones; el contenido técnico real son ~10-12 min.
- El autor promociona su **herramienta propia "Gentel"** (stack completo que hace "todo esto sola") — no es sponsor externo; el cierre pide **donaciones GitHub (22 sponsors, para pagar la suscripción de Codex)**. La herramienta NO se evaluó (no es el objetivo del análisis).
- ASR de stream en argentino: "gentel" = Gentel (herramienta), "recipt" = receipt (recibo), "resist/recift" = recipt (el mismo), "engram" = Engram (donde guarda estado). Marcados como aproximaciones del ASR.
- El vídeo confirma el patrón del canal: contenido de diseño avanzado + componente de comunidad/donaciones (la skill ya lo anotó el 15-ago: "la lección de diseño vale, la herramienta de pago no").
