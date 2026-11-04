---
title: "Análisis — Eric Risco: Software Factory / AI Factory y el clasificador de riesgo (26-oct-2026)"
type: research
---

# Análisis — «Programar con agentes ya no basta: monta tu Software Factory»

**VERACIDAD:** [VERIFICADO] contra transcripción íntegra de auto-subtítulos.

**Fuente**: https://youtu.be/p6nnqerea7w · canal **Eric Risco | Inteligencia Artificial** · publicado **2026-10-23** · **17:21** · **105.788 vistas** (leído 26-10-2026 22:26 con `yt-dlp --skip-download --print`, exit 0).
**ID**: `p6nnqerea7w` · **Transcripción**: `vid.es-orig.vtt` (169.220 B) → `clean.txt` (**18.136 chars / 483 frases**) tras quitar timestamps, etiquetas y duplicados solapados del VTT.
Rutas locales: `~/.hermes/cache/scratch/yt_factory/`.

**Cobertura previa**: 0 rastros de «Eric Risco», «AI Factory» ni el ID en `~/joko-lab` (el término solo aparece en los volcados de `metrics/sesiones/*.jsonl`, que no cuentan como analizado). Canal sin precedente.

---

## Qué propone (5 piezas encadenadas)

1. **Entrada única**: error de producción (Sentry), issue de GitHub o tarea del usuario.
2. **spec writer** (Opus) que consulta el «brain» —memoria de contexto persistente— **antes** de escribir la spec; justificado para evitar duplicar código y romper arquitectura.
3. **builder** (Opus) en worktree y rama nueva, con **TDD por cada tarea** de la spec (test primero, falla, luego código hasta pasar).
4. **Cuatro revisores en paralelo**, contexto limpio cada uno y **modelo de familia distinta** al que escribe: seguridad, UX, UI y código. El argumento central es explícito: *«quizá el modelo Opus se sesgaría de utilizarse a sí mismo para revisar la seguridad»*.
5. **approver** (Opus) que recoge los 4 feedbacks y devuelve al builder en bucle hasta que pasen; después **un clasificador de riesgo** decide si el cambio va directo a main o exige aprobación humana por PR. El autor insiste en que ese paso **exige hooks o código, no confianza en el prompt**, y en que el modelo clasificador no puede ser pequeño.

Añade dos extensiones: **Content Factory** (bruto de audio → corta silencios y errores → transiciones → miniatura → subida a YouTube, con revisión humana final) y **RSC Factory**, que anuncia como open source **sin repositorio público todavía** (es un CTA de comentarios, no un entregable).

## Cifras del vídeo, contrastadas en fuente primaria

- OpenAI: ~1 M de líneas con **0 % de código escrito a mano** → `openai.com/index/harness-engineering` (harness engineering con Codex).
- Stripe: **1.000+ PRs por semana** producidos por agentes → `stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2` (cobertura: InfoQ, 2026-03).

Ambas se sostienen. El vídeo **no inventa** las cifras de la industria.

## Medición propia del lab (26-10-2026)

- **162** `SKILL.md` · **152** ficheros en `tools/` · **22** `RULE-*.yaml` · **57** crons (**54 activos**) · `~/.hermes/hooks` sin contenido → **0 hooks**.

## Qué ya está cubierto en casa (confirmación, no novedad)

| Pieza del vídeo | Equivalente medido en el lab |
|---|---|
| spec antes de codificar | skill `plan` |
| builder con TDD | skill `test-driven-development` |
| revisión previa | skill `requesting-code-review` |
| brain / contexto persistente | RAG LanceDB + `RULE-*.yaml` + memoria episódica |
| verificación de subagentes | skill `delegacion-subagentes` + RULE-021 |

## Qué es nuevo de verdad (3 huecos)

1. **Disparo por evento**: los 54 crons activos son por tiempo; no hay entrada por webhook (Sentry/issue).
2. **Revisor ≠ modelo que escribe**, formalizado como regla anti-sesgo. Hoy hay heterogeneidad de hecho (DeepSeek habla, gpt-oss ejecuta) pero no está escrita.
3. **Clasificador de riesgo que decide humano sí / humano no**. Los gates actuales son binarios fail-closed (RULE-021), no un juicio de tamaño o impacto.

## Límite real en este hardware

Cuatro revisores en paralelo con modelos distintos **no caben en 12 GB de VRAM**; en local sería secuencial y con uno o dos modelos. El paralelismo es de su stack cloud.

## Experimentación propia: ¿sirve el clasificador de riesgo en este lab?

Caso elegido: **las escrituras del lab** (la decisión que el usuario toma a mano). Rúbrica propuesta en 4 niveles: R0 solo lectura · R1 aditivo (backlog/research) · R2 código propio no protegido · R3 zona protegida (n8n, `coleccion.db`, compose, servicios, crons, skills).

**Intento 1 — `git log` (30 días):** 9 commits, 18 ficheros, **0 en R3**; se excluyó el commit `21dcc98` (2.347 ficheros, snapshot de importación). Resultado **inválido como censo**: las escrituras sensibles del lab no se commitean (`coleccion.db`, `~/.hermes/scripts`, `SKILL.md`, crons), así que git no contiene la materia del riesgo.

**Intento 2 — `mtime` por ruta (26-09 a 26-10):**

- R3: **87 vivos** + 77 backups · R2: **78 vivos** + 85 backups · R1: **1.581**.

Resultado **también inválido**: los 87 de R3 incluyen los informes diarios de empleo de joseba/esti/carmen (`2026-10-20-esti.txt`, `-joseba.html`…), que **se generan solos cada día**. La rúbrica por ruta mete el **producto normal de un cron** en la misma categoría que un cambio de código protegido. **No distingue escritura automática de decisión humana.**

**Hallazgo (lo que sobrevive a los dos fallos):** el clasificador necesita un eje que el vídeo no explicita — **¿cambia el comportamiento o produce la salida?** Un informe diario es producto; tocar `rag-reindex.sh`, `informe-diario-local.sh`, un cron, una skill o `coleccion.db` cambia comportamiento. Con ese eje, el universo real de decisiones es del orden de **20-30 ficheros de código/config al mes**, no 1.900 escrituras.

Regla candidata derivada: **R3 solo cuando cambia el comportamiento de un circuito protegido; producir su salida normal nunca pide OK.** Contraste empírico del mismo día: se pidió OK explícito para `rag-reindex.sh` y `informe-diario-local.sh`, y **no** se pidió para regenerar los 87 ficheros de salida de empleo.

## No verificado / límites

- Nombres de modelo («Sol», «Astra», «Opus 5.5») proceden de **auto-subtítulos**: pueden estar deformados. **No se citan como dato.**
- «RSC Factory» **no existe** como repositorio público a 26-10-2026; es una promesa con CTA.
- El autor afirma que su propia factory edita su vídeo; **no hay artefacto verificable**, solo el vídeo como demo de sí mismo.
- El paralelismo de 4 revisores no se ha probado aquí y no cabe en 12 GB de VRAM.

## Qué NO es y qué no autoriza

- **No es adopción de nada**: ni Sentry, ni webhooks, ni multi-revisor, ni RSC Factory.
- **No autoriza** tocar crons, servicios, `coleccion.db` ni skills.
- **No es un cambio de las RULE**: la regla candidata queda como **propuesta** en `pendientes.md`; crear un `RULE-*.yaml` exige OK aparte.
- El veredicto del post es **MEDIO-ALTO como arquitectura, sin entrada como herramienta** (no hay entregable inspeccionable).

_Anotado 2026-10-26 22:39 CET. Sin commit._
