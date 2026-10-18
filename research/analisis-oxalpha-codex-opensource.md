---
title: "Análisis — \"Esta nueva IA supera a los mejores modelos... ¡pero nadie sabe quién la creó!\" (AI Revolution en Español, 25-ago-2026)"
type: research
---

# Análisis — "Esta nueva IA supera a los mejores modelos... ¡pero nadie sabe quién la creó!" (AI Revolution en Español, 25-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://youtu.be/_UZ5kW1YYPg (17 min, 2.694 views)
**Método:** metadatos + subtítulos ES (168 KB → 18.6K chars limpios, lectura completa en 4 pasadas)

## Los 3 temas del vídeo

### 1. 🕵️ OxAlpha — el modelo misterioso de OpenRouter (20-ago)
- Modelo "stealth" sin ficha técnica ni laboratorio atribuido: **Stealth Ox Alpha**, razonamiento para programación + trabajo agéntico + multimodal (texto/imagen/vídeo), ventana de **1M tokens**, salida 128K.
- **80% en DeepSWE** (10 tareas de Ben Davis) — supera a GPT-5.6 Sol, Claude Fable, GLM 5.3 Max (62%) y Grok 4.6 — pero **muestra pequeña**: otras ejecuciones dan 63% (no es comparación justa con SWE-bench Verified ~96).
- Forense (por qué se cree que es GLM 5.x de Zhipu sin lanzar): tokenizador de vídeo idéntico a GLM 5B Turbo, desfase fijo de 75 tokens en 25 prompts (vocabulario compartido), rechazo de audio como GLM 5, 1.3 emojis/1000 chars (igual que GLM/Qwen), censura china (respuestas cortadas a mitad en temas sensibles).
- **~744.000M parámetros MoE con ~40.000M activos** (huella digital) — lo que hace viable los 100 billones de tokens/día gratis.
- **100 billones de tokens/día gratis** (~100× el consumo mensual de Visa según el vídeo); ventana gratuita hasta ~27-ago.
- Cronología de "stealth models" chinos: Oni Alpha (Zhipu, feb) · Pantera (B2 Pro, mar) · Elephant (Qwen/Lingchi, abr) · Ogw (Meituan Longcat 2.0, jun) · **OxAlpha (20-ago, sin atribuir)**.
- Perplejidad adicional: otro "Corin" en Codearena (¿Kimi? ¿Moonshot? ¿Qwen? — sin confirmar).
- **Ya en producción real**: agentes de Nous Research (Hermes) lo usan como modelo seleccionable en OpenRouter/OpenCode.

### 2. 🛡️ Anthropic Glasswing + "Mito 5" (21-ago)
- Anthropic distribuye capacidad cibernética de vanguardia SOLO a defensores: preview de "Mito 5" a organizaciones que protegen software crítico; acceso amplio pero con trabajo ciber de doble uso bloqueado.
- Integración en herramientas existentes de socios (solo salidas específicas: parches, alertas — nunca un cuadro de texto para pedir exploits).
- **0xDAF (Defender Advantage Fund)**: $35M en créditos para vulnerabilidades activas.
- Cloud Security ahora escanea con Mito 5 en beta pública (CWE, confianza, severidad, solución sugerida, facturado como tokens estándar).

### 3. 🎁 OpenAI libera el runtime de Codex como open source (Apache 2.0) — LO MÁS RELEVANTE
- No el modelo: **el entorno de ejecución** (capa de ejecución de agentes).
- Demostración de que la capa de ejecución importa: en ARC-AGI 3, dos cambios (conservar razonamiento + comprimir contexto) llevaron a GPT-5.6 Sol de **13.3% → 38.3%** reduciendo tokens de salida a 1/6.
- Componentes: **Codex Exec** (CLI, salida estructurada) · **SDK** (TypeScript/Python, ciclo de vida de tareas) · **Servidor de apps** (protocolo **JSON-RPC** documentado: estado persistente, eventos, interrupción, aprobar por humano).
- Casos reales: Drive/Creed → 7.000 declaraciones de impuestos, tiempo -1/3; Disco → App Builder sobre el SDK; demo "Relay" (panel logístico sin chat: contexto en la interfaz, herramientas MCP propias, aprobación humana antes de actuar).
- Filosofía: **el contexto del usuario vive en sus herramientas (colas, registros, paneles)**, no en un chatbot genérico.

## 🔴 Aplicación al LAB — VALOR MEDIO

### ✅ Futurible anotado: evaluar el runtime open source de Codex
- El lab tiene el skill `codex` (delegar a Codex CLI). El runtime open source (Apache 2.0) con JSON-RPC + aprobación humana + estado persistente es **una referencia de arquitectura de capa de ejecución**.
- **Señal de activación**: si el lab integra un agente de código en un panel/herramienta propia (p.ej. automatizar PRs, CI, revisión de código) con control humano.
- No es urgente: Hermes YA implementa ese ciclo (memoria, herramientas, aprobación, salida estructurada).

### ✅ Validación del diseño de Hermes/agentes del lab
- El vídeo describe la capa de ejecución ideal de un agente: memoria a lo largo de conversaciones largas, recuperación de contexto, llamada de herramientas, streaming, sobrevivir a bloqueos, aprobar momentos peligrosos, salida estructurada — **exactamente lo que Hermes hace** (skills, memoria persistente, MCPs, approvals, terminal).
- Validación externa del patrón "agente incrustado en las herramientas del usuario" (el lab vive en Telegram + terminal + cron, no en un chatbot genérico).

### ⚪ Contexto (no accionable)
- **OxAlpha/GLM 5.x**: el lab usa modelos locales (gpt-oss, GLM 4.6V, LFM). Un "GLM 5.3 sin lanzar de 40B activos" es interesante para el roadmap de hardware (¿cabría en 12 GB? 40B activos con 744B total NO cabe sin cuantización agresiva — confirmar cuando salga). Anotado como vigilancia.
- **Anthropic Mito 5/Glasswing**: ciberseguridad defensiva — contexto de la industria, no aplica al lab (no es SOC).

## Conclusión
VALOR MEDIO: 1 futurible ligero (runtime Codex open source como referencia de capa de ejecución si se integra un agente en panel propio) + validación del diseño de Hermes. El resto (OxAlpha, Glasswing) es contexto de la industria. Ningún cambio de stack hoy.
