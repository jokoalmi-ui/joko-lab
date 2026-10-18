---
type: research
fecha: 2026-09-25
hora: "21:51 CEST"
canal: "@jokioki (Joaquín Ruiz — IA para Desarrolladores)"
videos_revisados: 59
metodo: "yt-dlp (catálogo + descripciones) + GitHub API + fuentes primarias (SPEC OKF v0.2, blog oficial LiteLLM, NVD/GHSA/Kaspersky)"
estado: "investigación cerrada — 0 instalaciones, 0 cuentas, 0 €; propuestas pendientes de OK"
peticion_usuario: "Este canal es bastante técnico. Investiga el canal por si encuentras alguna tecnología útil para LAB"
---

# Investigación del canal `@jokioki` — tecnología aprovechable para Joko Lab
**VERACIDAD:** [VERIFICADO]

## 1. Objeto y pregunta

Determinar si el canal **@jokioki** (Joaquín Ruiz — IA para Desarrolladores), ya conocido en el lab por
el análisis del 08-sep («11 trucos para ahorrar tokens») y del 25-sep (vídeo de Jev/TypeSafe),
aporta **tecnología concreta y aprovechable** para el LAB, no solo divulgación.

## 2. Método (reproducible)

1. Catálogo completo del canal con `yt-dlp --flat-playlist` → **59 vídeos**.
2. Descripción + URLs citadas de **los 59** (`yt-dlp --dump-json`) → caché `/tmp/chan_clean.json`.
3. Triage por título/descripción → candidatos que tocan el stack del lab (MCP, RAG, evals, agentes,
   modelos locales, seguridad, n8n/Ollama).
4. **Verificación externa de cada candidato**: `api.github.com` (estrellas, licencia, último push,
   creación, archivado) y fuentes primarias (SPEC.md de OKF, blog oficial de LiteLLM, NVD/GHSA).
5. Comprobación en el propio equipo de lo que afecta al lab (solo lectura: venvs, `.pth`, compose).

Regla aplicada: **nada se da por bueno porque lo diga el vídeo**; las cifras de esta ficha son de la
comprobación externa, y cuando el vídeo y la fuente difieren se dice cuál es cuál.

## 3. Ficha del canal

- **59 vídeos**. Era antigua (2020-2023): WordPress/frontend. **Era IA: desde oct-2025 hasta hoy (25-09-2026)**.
- Vistas modestas (mayoría 200-12.000) con 4 picos: **61k** (Kimi K3 en 8 GB sin GPU), **39k** (RAG),
  **31k** (Google Antigravity), **23k** (Gemma 4).
- Patrón de valor: **divulgación + medición propia + repositorio reproducible**. Publica scripts y
  resultados, e incluso publica los resultados que le dejan mal (RAG 2/6 · OKF 3/6 · OKF+RAG 4/6
  «ninguno aprueba»). Es el rasgo que lo hace útil para el lab.
- Repos propios relevantes: `JoaquinRuiz/rag-vs-okf` (6★, jul-2026), `JoaquinRuiz/SpecJudge`
  (53★, MIT, push 24-09-2026), `JoaquinRuiz/graphrag-neo4j-ollama` (36★), `JoaquinRuiz/soportebot` (2★).
- Ruido estructural: varios vídeos de VPS llevan **enlace de afiliado** (Hostinger) en su descripción.

## 4. Hallazgos verificados (Tier 1)

### 4.1 OKF — Open Knowledge Format v0.2 (el hallazgo más aplicable)

- **Qué es**: formato abierto de Google Cloud publicado el **12-jun-2026** (según el canal y prensa;
  el propio SPEC se identifica como **v0.2**). Repo: `GoogleCloudPlatform/open-knowledge-format`
  (**603★, Apache-2.0, último push 2026-08-21**). Leído el `SPEC.md`, no solo el vídeo.
- **Definición real (SPEC)**: «un directorio de ficheros markdown con frontmatter YAML». Sin registro
  de esquemas, sin autoridad central, sin tooling obligatorio. Hace de **primera clase**:
  procedencia (`sources`), confianza (`generated`, `verified`, niveles de confianza), ciclo de vida
  (`status`, `stale_after`) y **atestación** (§10, computaciones atestadas). Convenciones `references/`,
  `index.md`, `log.md`. Única clave siempre obligatoria: **`type`**.
- **Dato medido por el canal** (repo reproducible `JoaquinRuiz/rag-vs-okf`): sobre el mismo corpus de 60
  ficheros y 7 preguntas → **RAG 2/6 · OKF 3/6 · RAG+OKF 4/6**. Ninguno aprueba; él lista los 5 peros.
- **DÓNDE beneficia al LAB**: el lab **ya es OKF de facto**. `01-knowledge/objects/RULE-*.yaml` tiene
  `status`, `confidence`, `confidence_label`, `evidence`, `last_validated`, `next_review`, `expires`,
  `superseded_by` (≈ ciclo de vida + confianza + frescura); los `research/*.md` ya usan frontmatter
  `type:`; las skills ya usan `references/`. Alinearse con OKF = nombres estándar, interoperabilidad y
  una semántica ya pensada para corpus **mantenidos por agentes** (que es exactamente el caso del lab).
- **Qué NO es**: no arregla el RAG por sí solo; el propio autor documenta 5 limitaciones y su medición
  no aprueba. No sustituye el RAG: lo complementa (él enruta entre capas con un tipo `Corpus`).

### 4.2 codebase-memory-mcp — grafo de código servido por MCP

- Repo `DeusData/codebase-memory-mcp`: **44.910★, MIT, C puro (sin runtime), push hoy 2026-09-25**.
  Indexa el código en un **grafo de conocimiento** (tree-sitter + LSP híbrido en 10 lenguajes,
  162 lenguajes soportados) y responde preguntas de arquitectura sin leer fichero a fichero.
- **Paper (arXiv 2603.27277)**: «83% answer quality, **10× fewer tokens**, 2.1× fewer tool calls»
  en **31 repositorios reales**. README: 8.050 tests, 45 superficies de agente, SLSA 3, VirusTotal por release.
- **Soporta Hermes explícitamente**: en su tabla de clientes aparece `Hermes | Detected |
  $HERMES_HOME/config.yaml | Skill + fail-open pre_llm_call context augmentation`. Linux soportado;
  instalación de una línea vía `install.sh`.
- **Discrepancia importante**: el vídeo titula «99% de tokens» (su medición con `/context` sobre un
  proyecto propio); el paper dice **10×**. Para el lab vale el paper.
- **Riesgo**: `curl … | bash`. Mitigación propuesta: clonar el repo y leer `install.sh` antes de ejecutar.
- **DÓNDE beneficia**: el lab vive con el contexto al límite (MEMORY al 98%, sesiones que se compactan).
  Indexar `~/joko-lab` permitiría consultas estructurales (grafo de llamadas, dependencias, impacto)
  sin quemar contexto leyendo ficheros.

### 4.3 promptfoo — arnés de evals y red teaming (proveedor Ollama nativo)

- Repo `promptfoo/promptfoo`: **25.458★, MIT, TypeScript, push hoy 2026-09-25**.
- Docs verificadas: proveedor **`ollama`** (`/api/chat`, `/api/completion`, `/api/embed`) con
  `OLLAMA_BASE_URL`; lista `gemma4` (visión), `qwen3.5`, `gpt-oss` (razonamiento); aserciones con
  modelo juez. Aviso textual de su doc: Ollama moderno emite `thinking` por defecto.
- Caso del canal: conectó promptfoo a un **modelo local (coste 0)**, generó **140 ataques** de red
  teaming contra su propio agente y encontró un fallo real; además descubrió que **sus propios tests
  estaban mal escritos**.
- **DÓNDE beneficia**: es el arnés que le falta al **cuello de botella declarado del lab (el
  verificador / RSI)** y a la medición de alucinaciones. El detalle del `thinking` por defecto es
  justo el fallo de instrumento ya registrado en el arnés v1 del RSI.

### 4.4 Seguridad: incidente LiteLLM/Trivy — comprobado en este equipo

- **Fuente primaria** (blog oficial de LiteLLM, 24-mar-2026, ampliado 30-mar): paquetes PyPI
  comprometidos **`litellm==1.82.7`** (payload en `proxy_server.py`) y **`1.82.8`** (incluye
  `litellm_init.pth`, que se ejecuta al arrancar Python sin importar nada), publicados el 24-mar a las
  10:39 UTC durante ~40 minutos antes de ser puestos en cuarentena por PyPI. Origen creído:
  la dependencia **Trivy** de su flujo de escaneo CI. **La imagen Docker oficial del proxy NO se vio
  afectada**; versión limpia publicada: **1.83.0**.
- **Estado del lab (solo lectura)**: `pip show litellm` **vacío** en los dos venvs de Hermes
  (`~/.hermes/hermes-agent/venv`, `~/.hermes/.venv`); **no aparece** `litellm_init.pth` en
  `/home/jokoalmi` ni en `/usr/lib/python3` (búsqueda acotada); el stack Docker solo declara
  `n8n`, `stirling-pdf`, `pdf-cleaner`, `ollama` — **sin servicio litellm**. Las menciones a «litellm»
  dentro de `joko-lab` son backlogs/documentos antiguos (texto, no dependencia).
- **Conclusión**: **el lab no está afectado por esa vía**. Lo aprovechable es la clase de riesgo
  (cadena de suministro en CI/instaladores): fijar versiones y no ejecutar instaladores sin leerlos.

### 4.5 OpenClaw — CVE-2026-25253 (aviso de exposición de gateways de agente)

- `openclaw/openclaw`: **390.499★**, muy activo. Vulnerabilidad verificada en fuentes externas al canal:
  **CVE-2026-25253** / GHSA-g8p2-7wf7-98mq, «1-Click RCE via Authentication Token Exfiltration from
  gatewayUrl» (afecta a versiones anteriores a 2026.1.29); cubierto por Kaspersky y por análisis de
  instancias expuestas a Internet (hunt.io).
- **Relevancia para el lab**: no se usa OpenClaw, pero el patrón de riesgo es idéntico al de
  **cualquier gateway de agente con acceso a shell expuesto** (Hermes incluido). Vale como checklist
  (exposición de puertos, sandbox, acceso por red privada), no como instalación.

## 5. Tier 2 (anotado, no prioritario)

| tecnología | dato verificado | encaje en el lab |
|---|---|---|
| `JoaquinRuiz/SpecJudge` | 53★, MIT, push 24-09-2026, Python | juez **local** vía Ollama + catálogo de modelos/precios; mismo patrón que `ai-router`/`llm_as_judge` |
| `github/spec-kit` | 138.891★, MIT | metodología Spec-Driven Development; encaja con `plan`/`grill-idea` |
| `coddingtonbear/obsidian-local-rest-api` | 2.958★, MIT, push 25-09-2026 | MCP para el vault de Obsidian del lab |
| `agent0ai/agent-zero` | 19.264★, licencia NOASSERTION | framework de agentes alternativo a Hermes |
| cuantización (GGUF/EXL2/AWQ/GPTQ) | vídeo del 28-may | **confirma** la práctica actual del lab (GGUF, `num_ctx` explícito) |
| `FareedKhan-dev/kimi-k3-in-c` + `gavamedia/deltafin` | 8.645★ Apache-2.0 (C) y 823★ (Rust, servidor OpenAI-compatible) | técnica de inferencia de un modelo gigante en un solo equipo; curiosidad técnica |
| `qhjqhj00/MemoRAG` | 2.266★, Apache-2.0, **último push 2025-09-11** | descartable por abandono |
| Gemma 4 (E2B/E4B) | **no verificado** (solo visto en el vídeo y en la doc de promptfoo) | candidato a evaluar en el banco de modelos |

## 6. Descartado (no aporta al lab)

Era WordPress/frontend (2020-2023), debates «ChatGPT Atlas vs Chrome», selfies IA con Google Flow,
LoRA en Colab, «adiós Siri en 100 líneas», `miscoshorts-ai`, `graphrag-neo4j-ollama` (2026-03, sin
licencia) y los vídeos de VPS (embudo de afiliado Hostinger en la propia descripción).

## 7. No verificado

- Gemma 4: no se comprobaron pesos, tamaños ni ficha en la librería de Ollama.
- Incidente Trivy: leído en el blog de **LiteLLM**, no en una fuente de Trivy.
- Claims de un solo equipo para Kimi K3 (8.645★/823★): no reproducidos aquí.
- Los «99% de tokens» del vídeo frente al **10×** del paper: no reproducidos; se cita el paper.

## 8. Relevancia para el LAB (dónde beneficia / qué NO es)

- **(A) OKF**: beneficia a la gobernanza del conocimiento (RULEs, `01-knowledge/objects`, informes con
  frontmatter). **NO es** un motor de búsqueda ni arregla el RAG por sí solo.
- **(B) codebase-memory-mcp**: beneficia al consumo de contexto sobre el propio `joko-lab`.
  **NO es** un modelo ni una mejora de inferencia; es una capa de consulta estructural.
- **(C) promptfoo**: beneficia a la **verificación** (RSI, alucinaciones, red teaming propio).
  **NO es** un framework de agentes ni sustituye al banco de casos del lab.
- **(D) seguridad**: beneficia como constancia documentada (LiteLLM no afecta al lab) y como checklist
  de exposición de gateways. **NO implica** cambiar nada hoy.

## 9. Propuestas (ninguna en marcha; requieren OK)

- **(a)** este informe ← **elegida y ejecutada** (opción «a» del mensaje de 25-09).
- **(b)** lectura de conformidad OKF v0.2 de los objetos de conocimiento del lab (solo análisis, sin escribir).
- **(c)** prueba de `codebase-memory-mcp` sobre una copia de `joko-lab` en directorio aislado
  (requiere OK de instalación; antes, leer `install.sh`).
- **(d)** `promptfoo` en venv aparte con 2-3 casos del banco de alucinaciones (requiere OK).
- **(e)** añadir `@jokioki` a `tools/monitor_yt.py` (opción pendiente heredada del 25-09).

## 10. Estado de esta investigación

- **0 ficheros escritos fuera de este informe**, **0 instalaciones**, **0 cuentas**, **0 gasto**.
- Cachés de trabajo (volátiles) en `/tmp`: `chan_clean.json` (59 vídeos), `okf.md` (SPEC), `cbm.md` (README).
- Ningún servicio tocado: ni n8n, ni Ollama, ni el stack de `automation-stack`.

## 11. Fuentes primarias consultadas

- `https://github.com/GoogleCloudPlatform/open-knowledge-format` (SPEC.md v0.2)
- `https://arxiv.org/abs/2603.27277` + `https://github.com/DeusData/codebase-memory-mcp` (README)
- `https://www.promptfoo.dev/docs/providers/ollama/` + `https://github.com/promptfoo/promptfoo`
- `https://docs.litellm.ai/blog/security-update-march-2026` (incidente de cadena de suministro)
- `https://nvd.nist.gov/vuln/detail/CVE-2026-25253` + GHSA-g8p2-7wf7-98mq + Kaspersky + hunt.io
- `https://github.com/JoaquinRuiz/rag-vs-okf` (comparativa medida RAG vs OKF)
- `api.github.com/repos/<owner>/<repo>` (ficha de cada repositorio citado)

## Anexo A — Catálogo completo del canal (59 vídeos, datos de yt-dlp)

| fecha | vistas | dur | título |
|---|---|---|---|
| 2026-09-25 | 62 | 14:40 | Jev NO es un LLM (por ESTO es casi GRATIS) |
| 2026-09-20 | 4226 | 15:44 | Estudiar programación en 2026? Mi respuesta honesta |
| 2026-09-17 | 1252 | 14:40 | OpenAI dice que GPT-6 es AGI. Lo he medido. |
| 2026-09-12 | 2472 | 18:14 | La IA que sustituye a tu jefe, no a ti ¿funciona? |
| 2026-09-08 | 3547 | 18:37 | Deja de ver “vuelve en 5 horas”: 11 trucos para ahorrar tokens |
| 2026-08-11 | 61105 | 16:48 | Kimi K3 con SOLO 8GB de RAM y sin GPU: sí funciona, pero... |
| 2026-08-07 | 1747 | 11:16 | El modelo barato ganó al caro: mejor código y menos gasto |
| 2026-07-31 | 4487 | 13:20 | ¿OKF soluciona el GRAN PROBLEMA del RAG? Medido + código |
| 2026-07-28 | 924 | 8:23 | Deja de usar el modelo más CARO para todo | SpecJudge |
| 2026-07-21 | 525 | 6:59 | IA local en WordPress 7 con Ollama, GRATIS y sin API key |
| 2026-07-13 | 746 | 15:27 | Seguridad en IA: ataqué mi propio agente (y falló) |
| 2026-07-01 | 8264 | 9:16 | Ahorra tokens en Claude Code con Codebase Memory MCP (gratis) |
| 2026-06-25 | 2846 | 12:38 | Los 6 NIVELES de programar con IA (el 90% NO pasáis del 3) |
| 2026-06-18 | 1648 | 14:29 | SDD en producción: añade una feature con IA sin romper nada |
| 2026-06-11 | 969 | 13:20 | Probé Claude Fable 5 en código real (no vale el doble) |
| 2026-06-08 | 511 | 7:33 | Claude Code: ¿qué está haciendo cuando ves "Cogitating..."? |
| 2026-06-04 | 2248 | 21:31 | La IA encontró un BUG en mi código ANTES de que yo lo escribiera | Spec-Driven Developme |
| 2026-05-28 | 11179 | 17:43 | De 140 GB a 40 GB: corre modelos de IA gigantes en tu PC con CUANTIZACIÓN |
| 2026-05-15 | 29971 | 15:22 | Vibe coding está MUERTO: Construí una app con Spec Driven Development |
| 2026-04-13 | 1431 | 5:50 | El PROBLEMA INVISIBLE de la IA que Hace que Se Olvide de Todo (y la Solución GRATIS) |
| 2026-04-10 | 626 | 11:42 | CLAUDE MYTHOS: La IA que Anthropic ESCONDE y NO te deja usar ¿MARKETING o ciberseguridad |
| 2026-04-07 | 23554 | 8:40 | Gemma 4: IA local en tu MÓVIL y PC sin Internet (privacidad total) |
| 2026-03-30 | 910 | 16:07 | Trivy y LiteLLM INFECTADOS | El mayor HACKEO que ha asustado a TODOS este 2026 |
| 2026-03-28 | 6603 | 14:48 | GraphRAG LOCAL: Soluciona PARA SIEMPRE los problemas de tu RAG (Python + Neo4j + Ollama) |
| 2026-03-23 | 6890 | 10:33 | SE ACABÓ el Autocompletado: Crea Agentes IA Locales Gratis con OpenCode + MCP + Ollama |
| 2026-03-13 | 1823 | 9:36 | Tu ChatGPT privado en la Nube sin tarjetas graficas (tutorial e integración Python) |
| 2026-03-05 | 8715 | 10:59 | RAG 2.0: Olvida las alucinaciones de tu IA para SIEMPRE (tutorial Python) |
| 2026-02-25 | 1285 | 9:19 | Gemini 3.1 Pro es un GENIO... ¿seguiré programando con Claude? |
| 2026-02-23 | 1324 | 8:47 | NO subas tus PDFs a ChatGPT: Crea tu IA PRIVADA casi GRATIS (RAG VPS) |
| 2026-02-17 | 3792 | 9:52 | Cuidado con el Vibe Coding: Tu IA te está HACKEANDO |
| 2026-02-13 | 660 | 14:16 | Ahorra cientos de dólares al mes: La mejor alternativa GRATIS a Zapier (n8n) |
| 2026-02-08 | 1532 | 7:29 | Adiós SIRI: hice una IA MEJOR en menos de 100 líneas de Python |
| 2026-02-03 | 4932 | 10:11 | memorIA INFINITA: Procesa 2GB+ de Documentos con RAG y Python (Sin Alucinaciones) |
| 2026-01-31 | 2056 | 7:43 | BORRA OpenClaw (Clawdbot) AHORA MISMO si no activas esto |
| 2026-01-27 | 2752 | 9:08 | Le di Acceso ROOT a una IA (y pasó esto...) - Tutorial Agent Zero |
| 2026-01-17 | 10305 | 8:34 | Deja de usar tu Terminal. Instala ESTO (IA Local Gratis) |
| 2026-01-13 | 7128 | 10:39 | Dejé CURSOR por la TERMINAL (Guía transición a Claude Code) |
| 2026-01-05 | 8000 | 8:55 | DEJA DE PAGAR a OpenAI: Tu propia IA Ilimitada con n8n |
| 2026-01-02 | 1698 | 9:32 | Deja de pagar $30/mes: Crea tu propia IA de Shorts GRATIS (Python) |
| 2025-12-26 | 11613 | 9:56 | Si no usas MCP, tu IA está incompleta (Docker Toolkit + Python) |
| 2025-12-23 | 4453 | 4:35 | Cómo hacer el Celebrity Selfie Viral en Hollywood con IA (Tutorial Google Flow) |
| 2025-12-18 | 5099 | 6:30 | El Fin de los Fotógrafos: Crea tu propio LoRA en la Nube |
| 2025-12-12 | 39502 | 9:37 | Adiós Prompt Engineering: Por qué RAG es el único futuro (Tutorial Python) |
| 2025-12-02 | 5147 | 7:21 | Hackear la IA es DEMASIADO FÁCIL (Debería ser ilegal) |
| 2025-11-26 | 1286 | 7:29 | Dejé de programar Agentes IA: n8n vs Código |
| 2025-11-21 | 31152 | 6:34 | Google Antigravity lo cambia TODO: Tu propio equipo de Agentes IA Gratis |
| 2025-11-03 | 669 | 9:08 | Automatización con IA para Principiantes: Tu primer Bot con n8n (Sin Código) |
| 2025-10-28 | 7986 | 4:24 | Crea tu Propia IA Personalizada GRATIS en 5 Minutos (El Método FÁCIL) |
| 2025-10-24 | 457 | 5:27 | Por QUÉ ChatGPT es tan inteligente (La Revolución de la "T" en 5 Minutos) |
| 2025-10-23 | 159 | 49:13 | ¿Tu trabajo está OBSOLETO? La IA Cambia las Reglas del Juego #wordcamp #ia #inteligencia |
| 2025-10-22 | 393 | 19:16 | ChatGPT Atlas vs. Google Chrome: El Debate Definitivo | ¿El Fin de una Era? |
| 2025-10-22 | 187 | 13:42 | VIBE CODING: ¿Tu Aliado 😇 o tu Enemigo 👿? (El Debate Definitivo) |
| 2025-10-20 | 393 | 22:19 | No programes con IA hasta que veas esto (El método AI-First) | Podcast "Programar con IA |
| 2025-10-20 | 206 | 6:39 | Deja el Vibe Coding: Programa con IA como un Profesional |
| 2023-02-14 | 903 | 39:38 | Programando un bloque Gutenberg de WordPress en React desde cero |
| 2020-11-09 | 122 | 24:48 | El Futuro de las tecnologías Frontend y su impacto en la conversión: El WebAssembly. |
| 2020-06-30 | 81 | 30:16 | El UI Component… Aliado o Enemigo? |
| 2020-01-23 | 59 | 37:19 | ¿Tengo una buena página web, o me están estafando? |
| 2020-01-23 | 197 | 35:41 | WordPress desacoplado. Mueve tu WordPress al (futuro) presente |

## Anexo B — Repos y enlaces citados por el canal (era IA)

- **Jev NO es un LLM (por ESTO es casi GRATIS)** (`FIOXJXRfsZQ`) → https://docs.typesafe.ai/introduction · https://typesafe.ai/blog/introducing-system-one-models-and-jev · https://wavect.io/es/blog/jev-ai-decision-model-review/
- **Estudiar programación en 2026? Mi respuesta honesta** (`7qIyJzxLEf0`) → https://gist.github.com/JoaquinRuiz/2a800e24ffeb8ec7c03d7c81b3c32a11
- **OpenAI dice que GPT-6 es AGI. Lo he medido.** (`n5QAvo1QeOI`) → https://github.com/JoaquinRuiz/agi-tests
- **La IA que sustituye a tu jefe, no a ti ¿funciona?** (`fSmJYsyz6kU`) → https://github.com/SenteLabsAI/OpenExecutive · https://news.ycombinator.com/item?id=49458418 · https://www.amazon.es/dp/B0GLNFW5TC · https://www.amazon.es/dp/B0H9Z2MRZT · https://www.challengergray.com/wp-content/uploads/2026/08/Challenger-Report-July-2026.pdf
- **Deja de ver “vuelve en 5 horas”: 11 trucos para ahorrar tokens** (`yWx7TrhZTxg`) → https://github.com/JoaquinRuiz/SpecJudge · https://www.amazon.es/dp/B0GT566CCL
- **Kimi K3 con SOLO 8GB de RAM y sin GPU: sí funciona, pero...** (`1o_JvhCk-gw`) → https://github.com/FareedKhan-dev/kimi-k3-in-c · https://github.com/gavamedia/deltafin · https://github.com/sqliteai/waste · https://huggingface.co/moonshotai/Kimi-K3
- **El modelo barato ganó al caro: mejor código y menos gasto** (`EOiv7RywtQM`) → https://github.com/JoaquinRuiz/SpecJudge
- **¿OKF soluciona el GRAN PROBLEMA del RAG? Medido + código** (`rtlDbb-q1pU`) → https://github.com/GoogleCloudPlatform/knowledge-catalog · https://github.com/JoaquinRuiz/rag-vs-okf · https://github.com/JoaquinRuiz/rag-vs-okf.git · https://www.trychroma.com
- **Deja de usar el modelo más CARO para todo | SpecJudge** (`T53zvm08zUg`) → https://github.com/JoaquinRuiz · https://github.com/JoaquinRuiz/SpecJudge · https://pypi.org/project/specjudge/
- **IA local en WordPress 7 con Ollama, GRATIS y sin API key** (`zMJRMnjdt6s`) → https://wordpress.org/plugins/jokiruiz-local-model-connector/
- **Seguridad en IA: ataqué mi propio agente (y falló)** (`3H68LLYNNvs`) → https://github.com/JoaquinRuiz/soportebot · https://github.com/promptfoo/promptfoo · https://www.promptfoo.dev/docs/red-team/quickstart/
- **Ahorra tokens en Claude Code con Codebase Memory MCP (gratis)** (`5_5yik4Y0cw`) → https://arxiv.org/abs/2603.27277 · https://deusdata.github.io/codebase-memory-mcp/ · https://github.com/DeusData/codebase-memory-mcp · https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/install.sh · https://www.russ.cloud/2026/05/10/codebase-memory-mcp-giving-claude-code-and-codex-a-map/
- **Los 6 NIVELES de programar con IA (el 90% NO pasáis del 3)** (`acpGOnJ-iAk`) → https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/ · https://techcrunch.com/2026/02/12/spotify-says-its-best-developers-havent-written-a-line-of-code-since-december-thanks-to-ai/ · https://www.anthropic.com/engineering/building-c-compiler
- **SDD en producción: añade una feature con IA sin romper nada** (`vGNvixq2ybk`) → https://github.com/JoaquinRuiz/spec-driven-development-produccion · https://github.com/github/spec-kit · https://github.com/github/spec-kit.git
- **Probé Claude Fable 5 en código real (no vale el doble)** (`NQiA1UC4OdQ`) → https://benchlm.ai/compare/claude-fable-vs-gpt-5-5 · https://www.anthropic.com/news/claude-fable-5-mythos-5 · https://www.coderabbit.ai/blog/fable-5-model-review
- **La IA encontró un BUG en mi código ANTES de que yo lo escribiera | Spe** (`oSA84NDvlJg`) → https://github.com/JoaquinRuiz/roboadvisor-sdd
- **De 140 GB a 40 GB: corre modelos de IA gigantes en tu PC con CUANTIZAC** (`MR4bNspc_rY`) → https://github.com/ggml-org/llama.cpp · https://huggingface.co · https://lmstudio.ai
- **Vibe coding está MUERTO: Construí una app con Spec Driven Development** (`uV5Q7d5M3XM`) → https://claude.com/claude-code · https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/ · https://github.com/github/spec-kit
- **El PROBLEMA INVISIBLE de la IA que Hace que Se Olvide de Todo (y la So** (`Vbj2mXImJCQ`) → https://chromewebstore.google.com/detail/obnlfngfhhdllmpkpbgfoiknekgmnflg?utm_source=item-share-cb
- **Trivy y LiteLLM INFECTADOS | El mayor HACKEO que ha asustado a TODOS e** (`0o3uvlpGnV4`) → https://blog.dreamfactory.com/the-litellm-supply-chain-attack-a-complete-technical-breakdown-of-what-happened-who-is-affected-and-what-comes-next · https://docs.litellm.ai/blog/security-update-march-2026 · https://medium.com/@tahirbalarabe2/the-litellm-pypi-supply-chain-attack-what-you-need-to-know-6ab536d4aeb3 · https://snyk.io/articles/trivy-github-actions-supply-chain-compromise/ · https://www.aquasec.com/blog/trivy-supply-chain-attack-what-you-need-to-know/
- **GraphRAG LOCAL: Soluciona PARA SIEMPRE los problemas de tu RAG (Python** (`dJ6D_krxpX0`) → https://github.com/JoaquinRuiz/graphrag-neo4j-ollama
- **Tu ChatGPT privado en la Nube sin tarjetas graficas (tutorial e integr** (`gp9R0JXNlRM`) → https://openwebui.com/
- **RAG 2.0: Olvida las alucinaciones de tu IA para SIEMPRE (tutorial Pyth** (`gvzibu9-OUc`) → https://github.com/ContextualAI/examples · https://github.com/qhjqhj00/MemoRAG
- **BORRA OpenClaw (Clawdbot) AHORA MISMO si no activas esto** (`swQi3C8uD3A`) → https://github.com/openclaw/openclaw
- **Le di Acceso ROOT a una IA (y pasó esto...) - Tutorial Agent Zero** (`bZ7OgeyhVGI`) → https://github.com/agent0ai/agent-zero
- **Deja de usar tu Terminal. Instala ESTO (IA Local Gratis)** (`-nJdU5CR91k`) → https://gist.github.com/JoaquinRuiz/19c1d9f374bb6b05c291bf44c4fae9b5
- **Dejé CURSOR por la TERMINAL (Guía transición a Claude Code)** (`siaR1aRQShM`) → https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code · https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- **Deja de pagar $30/mes: Crea tu propia IA de Shorts GRATIS (Python)** (`zukJLVUwMxA`) → https://aistudio.google.com/api-keys · https://github.com/JoaquinRuiz/miscoshorts-ai
- **Si no usas MCP, tu IA está incompleta (Docker Toolkit + Python)** (`fsyJK6KngXk`) → https://docs.docker.com/ai/mcp-catalog-and-toolkit/toolkit/ · https://github.com/JoaquinRuiz/mcp-docker-tutorial · https://github.com/coddingtonbear/obsidian-local-rest-api
- **Cómo hacer el Celebrity Selfie Viral en Hollywood con IA (Tutorial Goo** (`zV71eJpURIc`) → https://labs.google/flow
- **¿Tu trabajo está OBSOLETO? La IA Cambia las Reglas del Juego #wordcamp** (`B9X3vV8VI0s`) → https://zaragoza.wordcamp.org/2025/ · https://zaragoza.wordcamp.org/2025/files/2025/02/WCZGZ-25-IA_-Las-Reglas-del-Juego-han-Cambiado.pdf
- **VIBE CODING: ¿Tu Aliado 😇 o tu Enemigo 👿? (El Debate Definitivo)** (`CnX0VxFcVA4`) → https://www.amazon.es/dp/B0FNJXS5WH
- **No programes con IA hasta que veas esto (El método AI-First) | Podcast** (`_n0HsFqz6v8`) → https://www.amazon.es/dp/B0FNJXS5WH
