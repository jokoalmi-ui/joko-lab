# F1 — Coste en tokens del CONTEXTO FIJO del lab

**Preparado:** 2026-09-16 (noche). **Estado:** PREPARADO, NO EJECUTADO.
**Origen:** vídeo Gentleman Programming «ventana de contexto» (research/analisis-gentleman-programming-ventana-contexto.md), hallazgo NUEVO nº 1.

## Pregunta

¿Cuántos tokens cuesta, por request, el contexto que Hermes manda SIEMPRE en el perfil `default`
(SOUL + memorias + índice de skills + definiciones de herramientas + los 3 MCP), y qué bloque
justifica pasar a carga bajo demanda?

## Por qué (evidencia del vídeo, no opinión)

El directo sostiene que el system prompt (355 tok) + 4 tools (1.183 tok) se pagan en CADA request
y que una memoria inflada (428 líneas ≈ 91 $/mes) se paga entera aunque no se use. El lab tiene
3 MCP en producción con 25 herramientas y **no tiene medido ese coste**. Contabilidad, no concepto.

## Hipótesis

H1: el contexto fijo supera los 10.000 tokens por request y al menos un bloque (MCP o índice de
skills) es >20% del total → existe palanca real de poda.
H0: el fijo es pequeño (<5.000 tok) → la palanca no está aquí y el coste viene del contexto
ACUMULADO de conversación (lo que dice la skill `skill-compaction`).

## Instrumento declarado (y su límite)

- Medida: campo `usage.prompt_tokens` de `POST http://127.0.0.1:1234/v1/chat/completions`
  con `max_tokens=1`, `temperature=0`.
- Tokenizador: el del modelo cargado en LM Studio. Es el **mismo endpoint** que usa
  `delegation` (`openai/gpt-oss-20b`, :1234). NO es el tokenizador de DeepSeek.
  → Las cifras son «tokens según tokenizador de gpt-oss-20b», no tokens «universales».
  → El valor absoluto es un ORDEN DE MAGNITUD para el pipeline cloud; la FRACCIÓN por bloque
  (lo que decide la poda) es válida sin esa salvedad.
- Contraste independiente (patrón oro parcial): `pipeline_obs.jsonl` (33.247 líneas) guarda el
  `prompt_tokens` REAL de las llamadas de Hermes al pipeline cloud. Suelo del prompt real =
  mínimo observado en arranques de sesión. Sirve para detectar que la reconstrucción no omite
  ni inventa bloques grandes (si reconstruyo 40K y el real es 25K, sobra algo).

## Fases (una por comando, en este orden)

- **F1.0 Recolección** — `recolectar.py` (solo lectura de `~/.hermes`). Salida: `piezas.json` + inventario. Coste 0.
- **F1.1 Validación del instrumento (RULE-015, BLOQUEANTE)** — `validar_instrumento.py`. Sin esto, ninguna cifra vale.
  - V1 determinismo: mismo payload ×3 → varianza debe ser 0.
  - V2 linealidad: unidad ×1, ×2, ×3 → los incrementos deben ser constantes (si no, no se pueden restar bloques).
  - V3 suelo: prompt de 1 char → offset fijo (demuestra que no hay término oculto).
  - V4 ratio chars/token por tipo (prosa vs JSON de tools) → si el ratio baila, la reconstrucción del formato está mal.
  - V5 contraste: ratio medido aplicado al ledger vs `prompt_tokens` real del ledger.
- **F1.2 Medición por bloques** — `medir_bloques.py`. Cada bloque aislado (diferencia contra offset) y acumulado
  (para detectar no-linealidad). Salida: `mediciones.json` + `RESULTADOS.md`.
- **F1.3 Contraste con el ledger** — `leer_ledger.py` (solo lectura del JSONL). Salida: `ledger_baseline.json`.
  Límite conocido: el ledger no identifica la sesión ni el cliente → da DISTRIBUCIÓN, no aislamiento del fijo.
- **F1.4 MCP real (SEPARADA, requiere OK explícito)** — `medir_bloques.py --con-mcp`: lanza cada servidor MCP,
  pide `tools/list` (JSON-RPC stdio), mide el JSON y CIERRA el proceso. Es la única fase que crea procesos.
- **F1.5 Decisión** — el umbral NO se fija a priori (RULE-015). Se decide DESPUÉS del baseline, mirando
  fracción por bloque y coste € del bloque con la tarifa vigente del modelo cloud.

## Bloques a medir (perfil `default`, sesión Telegram)

| id | bloque | fuente real |
|----|--------|-------------|
| B0 | offset/suelo (framing del chat) | payload mínimo |
| B1 | SOUL.md | `/home/jokoalmi/.hermes/SOUL.md` (20.478 B) |
| B2 | memorias inyectadas | `~/.hermes/memories/MEMORY.md` (3.110 B) + `USER.md` (1.408 B) |
| B3 | índice de skills (name+description) | frontmatter de las SKILL.md activas (reconstruido) |
| B4 | herramientas del toolset `hermes-cli` | `toolsets: [hermes-cli]` en config.yaml |
| B5 | MCP: lab-db + lancedb + animation-server | `mcp_servers:` en config.yaml (fase F1.4) |
| B6 | contexto de plataforma/sesión (Telegram, home channel) | texto fijo del runtime |

## Qué NO es este experimento

- NO toca `~/.hermes` (solo lectura). NO modifica config, ni skills, ni memorias.
- NO toca n8n, Docker, ComfyUI, GLM ni el perfil `investigador`.
- NO publica nada. NO descarga ni carga modelos: usa el que ya está en VRAM.
- NO decide la poda: mide. La decisión es del usuario (RULE-013).
- NO afirma que el resultado del vídeo aplique al lab: mide el lab.

## Riesgos y control

- **TTL del modelo**: `lms ps` → `openai/gpt-oss-20b` IDLE con TTL 2h (quedaban ~52 min a las 22:59).
  Si expira durante la medición, F1.1/F1.2 fallan con error de modelo no cargado → se PARA y se
  pregunta (recargar es una acción con OK). No se recarga en automático.
- **Contexto**: suma de bloques ≈ 120 KB ≈ 30K tokens, justo en el borde de ctx 32768. El script mide
  bloque a bloque y NO envía la suma completa si excede; los bloques que no quepan se marcan
  `no_medido_por_contexto` (cero imputación, se reportan aparte).
- **Artefacto de reconstrucción**: el bloque B3 se reconstruye con el formato observado del prompt
  (categoría → `name: description`), no con el string literal del runtime. Se etiqueta como
  **orden de magnitud** para ese bloque; B1/B2/B5 sí son el texto exacto de la fuente.
- **Tokenizador distinto** al del modelo cloud → ver «Instrumento declarado».
- **⚠️ El ledger NO tiene campo de sesión ni de cliente** (comprobado en la preparación: solo
  timestamp, path, model, provider, stream, ttfb_ms, total_ms, status, prompt_tokens,
  completion_tokens, error). Por tanto NO permite aislar las llamadas de una sesión de Hermes
  frente a llamadas de scripts/cron del lab: hay prompts no-sonda de ~1.009 tok con salida de
  90-508 tok que no pueden ser una sesión de Hermes con skills cargadas. Uso correcto del ledger:
  **distribución de referencia** (p10 54.532 / mediana 192.799 tok), NO patrón oro del fijo.
  El patrón oro del FIJO es F1.2 (medición directa), no el ledger.
- **Coste**: 0 € (todo local). Sin llamadas a DeepSeek ni a ninguna API externa.

## Entregable

`RESULTADOS.md` con: tabla bloque → tokens → % del fijo → € por 1.000 requests con la tarifa vigente
(fechada), etiqueta de validez por cifra, y la comparación H1/H0. Sin recomendación de poda hasta que
el usuario vea el baseline.

## Estado de partida (medido, no supuesto)

- `SOUL.md` 20.478 B · `config.yaml` 14.571 B · `MEMORY.md` 3.110 B · `USER.md` 1.408 B
- `.skills_prompt_snapshot.json` 95.353 B (= manifiesto de 164 SKILL.md, NO el prompt: contiene
  `[mtime_ns, size]`, no las descripciones)
- `pipeline_obs.jsonl` 9.244.423 B / 33.247 líneas (claves: timestamp, path, model, provider, stream,
  ttfb_ms, total_ms, status, prompt_tokens, completion_tokens, error)
- `toolsets: [hermes-cli]` · 3 MCP enabled · `delegation` → `openai/gpt-oss-20b` en :1234
- LM Studio :1234 (pid 5481) · proxy :9911 (pid 2421) · Ollama :11434.
  El headless de visión (:1235) NO aparece en la salida de `ss` de esta comprobación.
- No hay `tiktoken` ni `transformers` instalados → el tokenizador solo puede venir del endpoint.
