---
title: "Análisis reel notfound404.es — ECC (everything-claude-code) de Affaan Mustafa"
type: research
source: "https://www.instagram.com/reel/DeH6T4FDLa3/"
account: notfound404.es
published: 2026-10-05
analyzed: 2026-10-09
tags: [agentes, skills, claude-code, hermes, contexto]
---

# Reel «ECC / everything-claude-code» (IG notfound404.es, DeH6T4FDLa3)

## 0. Fuente y extracción completa
- Cuenta: **notfound404.es** · publicado **5-oct-2026** (el 09-oct aparece «hace 3 días») · **258 likes, 3 comentarios**.
- Vídeo: 59,0 s · 720x1280 · h264 + aac · 5.156.223 B (descargado y transcrito localmente).
- Método: `og:title`/`og:description` + transcripción (whisper) + 12 frames por escena analizados con GLM-4.6V local.
- Comentarios (2 de 3): `cristianrdr76` «Y?????» · `abrahamluque89` «¿Cuál es el motivo de compartir algo que te puede hacer destacar?».

## 1. Qué dice el reel (transcripción literal, resumida sin alterar cifras)
- Affaan Mustafa **ganó un hackathon de Anthropic en Nueva York** (>100 participantes) y lo construyó todo con Claude Code; después subió **su configuración entera a GitHub**.
- El repo se llama **ECC** (antes *everything-claude-code*): **68 agentes** (uno planifica, otro diseña arquitectura, otro revisa seguridad, otro arregla errores de compilación) y **casi 300 skills**.
- «Lo mejor: **aprende de ti**. Observa cómo trabajas y convierte tus costumbres en skills nuevas».
- Se instala con **dos comandos** dentro de Claude Code, es gratis y hoy tiene **más de 270.000 estrellas**; «**está entre los 20 repositorios con más estrellas de todo GitHub**».
- Opinión del autor del reel: «**no lo instales entero** y te olvides; 300 skills son demasiadas, todo lo que cargas ocupa memoria de Claude. Ábrelo, mira cómo trabaja alguien que gana hackathones y quédate solo con lo que vayas a usar».

## 2. Contraste con la fuente real (GitHub API + README, 09-oct-2026)
| Afirmación del reel | Dato medido | Veredicto |
|---|---|---|
| «más de 270.000 estrellas» | **275.713** ⭐ (41.150 forks) | **CIERTO** |
| «entre los 20 repos con más estrellas de GitHub» | 15 repos por encima → **posición ≈16** (el nº1 tiene 552k) | **CIERTO** (top-20) |
| «68 agentes» | **68** entradas en `/agents` | **CIERTO** exacto |
| «casi 300 skills» | **293** entradas en `/skills` | **CIERTO** |
| «se instala con dos comandos» | `/plugin marketplace add https://github.com/affaan-m/ECC` + `/plugin install ecc@ecc` | **CIERTO** (vía Claude Code) |
| «ganó el hackathon de Anthropic en NY» | Anthropic x Forum Ventures, NYC, **sep-2025**, 1º de 100+, 15.000 $ en créditos | **CIERTO** (matiz de fecha) |

- Repo: `affaan-m/ECC` · MIT · creado **2026-01-18** · último push **2026-10-05** · web `ecc.tools` · descripción oficial: «The agent harness performance optimization system. Skills, instincts, memory, security, and research-first development…».
- **Matiz de fecha**: el hackathon fue **sep-2025**; el repo nació **ene-2026**. El reel lo presenta como un «esto lo hice y lo regalé» continuo.
- Estructura real: **94 comandos**, 23 packs de reglas por lenguaje, 5 hooks (incl. `memory-persistence`), 3 *contexts* (dev/research/review), 7 manifests, 2 plugins. README v2.0.0 citaba «281 skills, 67 agents, 94 command shims» (la cifra del reel = versión actual).

## 3. Lo que el reel NO dice y sí importa al lab
- **ECC soporta Hermes de forma nativa**: `./install.sh --profile minimal --target hermes` + `docs/HERMES-SETUP.md`; `npx ecc-universal@2.2.3 doctor --target hermes`. `.hermes/README.md` afirma que **NO toca `config.yaml` ni `.env`**.
- Otros targets: Codex, OpenCode, Cursor, Gemini, Zed, Antigravity, Qwen, OpenClaw, Kimi, CodeBuddy, JoyCode.
- **Memory Vault** compartida entre harnesses (markdown local e inspeccionable) con handoff explícito: `ecc memory ... --from hermes --target codex`.
- **Control de contexto para modelos locales**: `ECC_SESSION_START_MAX_CHARS` (por defecto 8000), cap de instintos inyectados (6), y `ECC_SESSION_START_CONTEXT=off` «para setups de bajo contexto / modelos locales».
- Escala de ingeniería declarada: 1282 tests, 98 % cobertura, 102 reglas de análisis estático, `.gitleaksignore`, hooks `beforeShellExecution`/`beforeMCPExecution`.

## 4. Aplicabilidad al Joko Lab (OBS → HYP)
- **CONFIRMA reglas ya vigentes del lab**:
  - «No activar en masa» (biblioteca externa de 873 `SKILL.md` en `references/`) ↔ el propio consejo del reel: 300 skills son demasiadas y ocupan contexto.
  - El lab ya gobierna esto con `skill-compaction` y la regla «lección nueva → editar/consolidar sección, NUNCA bloque aditivo». ECC llega a las mismas conclusiones con **variables medidas** (cap 8000 chars, cap 6 instintos).
- **NUEVO / candidato a experimento**:
  1. **«Instincts»**: observa trabajo real (ediciones, comandos bash como `npm test`/`git commit`) y **propone una skill nueva** si detecta un patrón (ejemplo de la slide 08: crea «tests-antes-del-commit»). En el lab existe `auto-mejora-lab` (a petición) y `detectar-sin-uso` (higiene semanal), pero **no un detector de hábitos recurrentes** en sesiones/tools. → HYP: un cron semanal que lea el histórico de sesiones y proponga 1 skill por patrón repetido.
  2. **Memoria/contexto compartido entre harnesses**: el lab tiene el problema inverso documentado («sin puente agente→WebUI/CLI»; `hermes send` acusa ok sin llegar al DM). El patrón de ECC (fichero markdown local + handoff por target) es el que el lab ya usa con `memoria-episodica.sh` (RULE-011) → **CONFIRMA el enfoque**, no aporta mecanismo nuevo.
  3. **Empaquetado/distribución**: `marketplace.json` + `plugin.json` + `manifests/` como canal de distribución de skills. El lab no tiene canal propio (las skills no están versionadas en git). → dato para una eventual DEC sobre publicar la biblioteca del lab.
- **RIESGO / NO HACER ahora**: `install.sh --target hermes` escribiría en `~/.hermes` (rules, skills, commands, AGENTS.md) → choca con **RULE-016** (no tocar Hermes con menos de 5 días de incidencias tras la publicación) y con la política de no activar skills en masa.
- **DEC (propuesta)**: **no instalar**; tratar ECC como biblioteca de referencia de solo lectura. Pendiente opcional y barato: leer `docs/HERMES-SETUP.md` y revisar 2-3 skills concretas (tests/seguridad) para robar ideas al lab.

## 5. Verificación y artefactos
- Todo dato de §2 proviene de `api.github.com/repos/affaan-m/ECC` + `raw.githubusercontent.com/.../README.md`, consultados **2026-10-09** (no hay cifras tomadas de la transcripción sin contrastar).
- Artefactos locales: `reel_transcripcion.txt` (1.061 B), `reel_metadatos.json`, 12 `frame_NN.jpg`, `reel.mp4` (5.156.223 B).
- Herramientas usadas: descarga directa del MP4, `tools/transcribir_reel.sh`, `tools/extraer_frames_escenas.py`, `tools/analizar_carrusel_rapido.py` (GLM-4.6V, 8,4 s/img).
