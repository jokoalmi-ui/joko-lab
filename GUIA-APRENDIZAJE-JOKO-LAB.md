---
title: "GUIA DE APRENDIZAJE DE JOKO LAB"
type: guia
---

# GUIA DE APRENDIZAJE DE JOKO LAB

**Para:** Joseba
**Objetivo:** entender Joko Lab de principio a fin, SIN perderte, leyendo en orden.
**Formato:** progresivo — cada capítulo explica los términos que usa (no asume que los conoces), qué hace cada pieza y POR QUÉ existe.
**Versión:** 1.3 — 2026-09-04 (revisión: cifras reales 04-sep — skills 119→185, RAG 15,200→42,931, LM Studio 11 modelos por API, 16 RULEs, delegación gpt-oss-20b validada, mapa del conocimiento como tool; el resto de estructura de 1.2 intacto)
**Relación con la otra guía:** esta es para APRENDER. `GUIA-JOKO-LAB.md` es para CONSULTAR (datos, comandos, rutas). Cuando termines esta, la de consulta te sonará familiar.

---

## Cómo usar esta guía

- Léela EN ORDEN. Cada capítulo construye sobre el anterior.
- Los términos en **negrita** se explican la primera vez que aparecen.
- Al final de cada capítulo hay un "Repaso" con las ideas clave.
- Si algo no te cuadra, vuelve al repaso del capítulo anterior — no sigas arrastrando dudas.

---

# PARTE 1 — EL CONTEXTO

## Capítulo 1: ¿Qué es Joko Lab y por qué existe?

Joko Lab es un **laboratorio personal de IA** que funciona 100% en tu casa (Erandio), sobre un PC con GPU NVIDIA RTX A2000 de 12 GB.

**¿Por qué existe?** La idea de fondo es esta: la IA no debería ser solo una herramienta que responde — debería ser un sistema que **aprende de cada sesión de trabajo** y acumula conocimiento verificable que mejora decisiones futuras.

El objetivo concreto se resume en un mapa:

```
[Tu] → [Hermes Agent] → [DeepSeek cloud / LM Studio local] → [Conocimiento LPA] → [Mejores decisiones]
```

Desglosemos cada pieza (se explican en detalle más adelante):

- **Hermes Agent** — el agente que te asiste. Es "el cerebro que ejecuta": te lee, decide, ejecuta y documenta.
- **DeepSeek** — un modelo de IA en la nube (el principal del lab).
- **LM Studio** — un motor de IA LOCAL (en tu GPU, sin internet).
- **Conocimiento LPA** — el sistema de conocimiento del lab (LPA = Living Product Architecture). Es donde se acumula lo aprendido.
- **Mejores decisiones** — el fin último: que cada respuesta, cada experimento, cada regla del lab te haga decidir mejor.

**La frase que resume todo:** Joko Lab es un sistema para construir sistemas complejos (humanos + IA + tiempo) sin perder coherencia.

### Repaso capítulo 1
- Joko Lab = laboratorio personal de IA en casa, con GPU NVIDIA RTX A2000 12 GB.
- Objetivo: que la IA aprenda de cada sesión y mejore decisiones futuras.
- Piezas: Hermes (agente) + DeepSeek (cloud) + LM Studio (local) + LPA (conocimiento).

---

## Capítulo 2: El hardware — la restricción central

Todo el lab está condicionado por UNA pieza de hardware:

**GPU NVIDIA RTX A2000 de 12 GB de VRAM.**

**VRAM** = memoria de video. Es donde se cargan los modelos de IA para que funcionen rápido. 12 GB es "poco" para los estándares actuales (muchos modelos grandes piden 20+ GB).

**¿Por qué es la restricción central?** Porque decide qué cabe y qué no:

- **No caben modelos > 12 GB** (ej: Granite 4.0 H Small de 19.5 GB NO cabe).
- **Solo cabe UN modelo grande cargado a la vez** — hay que rotar.
- **Un modelo grande típico usa 7-9 GB**, dejando 3-5 GB libres para lo demás.
- **Los embeddings (otra pieza, capítulo 6) compiten por la misma GPU** — este fue un problema real que se resolvió (lo verás en el capítulo 6).

**El PC actual (dato importante, 2026):** un Intel i5-9500 (6 núcleos, sin hyperthreading). El i9-9900K está comprado pero pendiente de montar. Esto importa para el RAG (capítulo 6): el reranker en CPU es lento porque el i5 tiene pocos hilos.

**Regla del driver:** el driver NVIDIA 595.84 está confirmado como óptimo. No actualizarlo sin motivo.

**Sistema:** Ubuntu (derivado), kernel 7.0.0-28, zona horaria Europe/Madrid.

**Rutina del PC:** se apaga de madrugada (~1:00-9:00). No programar tareas nocturnas. Los cron diarios se ponen a las 22:00.

### Dónde vive cada cosa (rutas críticas)

| Ruta | Qué contiene |
|------|-------------|
| /home/jokoalmi/automation-stack/ | Stack Docker (n8n, ollama, stirling-pdf, pdf-cleaner) |
| /home/jokoalmi/joko-lab/ | Conocimiento, herramientas, protocolos (el corazón) |
| /home/jokoalmi/hermes-lab/ | Scripts de sesión, informes, git |
| /mnt/ssd_ia_datos/ | Datos persistentes (n8n, modelos, backups) |
| /home/jokoalmi/lmstudio_real_monitor/ | Monitor Flask de LM Studio |
| /home/jokoalmi/lm-studio-benchmarks/ | Resultados de benchmarks de modelos |
| /home/jokoalmi/perfume-ia/ | PRODUCTO: Perfume IA (Experimento 001) |

### Zonas protegidas (regla dura)
```
/mnt/ssd_ia_datos/n8n        → datos de n8n (NO TOCAR sin confirmación)
/mnt/ssd_ia_datos/exports    → exportaciones
/mnt/ssd_ia_datos/backups    → backups
```

### Repaso capítulo 2
- La GPU A2000 12 GB es la restricción central: define qué modelos caben.
- PC actual: i5-9500 (6 núcleos); i9-9900K pendiente de montar.
- Hay rutas críticas y zonas protegidas que nunca se tocan sin confirmación.

---

## Capítulo 3: Los "4 cerebros" — cómo se reparten el trabajo

El lab tiene UNA idea de fondo: no usar un solo modelo para todo. En su lugar, reparte el trabajo entre "cerebros" con roles distintos:

| Cerebro | Rol | Dónde | Qué responde |
|---------|-----|-------|--------------|
| **DeepSeek** | Piensa, decide, coordina | Cloud | Qué tiene sentido hacer |
| **LM Studio** | Ve, evalúa, critica | Local GPU | Es correcto visualmente |
| **Ollama** | Simula, genera, explica | Local | Qué pasaría si... |
| **Telemetría/Runtime** | Mide, observa, contrasta | El sistema | Qué ocurre realmente |

**Las reglas duras (por qué existen):**
- DeepSeek no ve (no tiene visión) → delega en LM Studio para imágenes.
- LM Studio no decide → evalúa, y DeepSeek decide.
- Ollama no critica → genera escenarios.
- Telemetría no opina → solo mide.

**¿Por qué esta separación?** Porque cada modelo es bueno en algo distinto. Y porque delegar evita que un modelo "haga todo mal": el que decide no es el que ve, el que ve no es el que decide.

### Repaso capítulo 3
- 4 cerebros con roles separados: DeepSeek (decide), LM Studio (ve), Ollama (simula), Telemetría (mide).
- Regla: quien decide no ve, quien ve no decide, quien mide no opina.

---

# PARTE 2 — LA INFRAESTRUCTURA

## Capítulo 4: Docker y los servicios del stack

**Docker** es un sistema de contenedores: paquetes de software que incluyen TODO lo necesario para ejecutarse (código + dependencias), aislados del resto del sistema.

**Docker Compose** es la herramienta que define varios contenedores juntos en un archivo (`docker-compose.yml`) y los levanta/para como un grupo.

**¿Por qué Docker en el lab?** Porque servicios como n8n o un PDF-server necesitan entornos completos, y Docker permite tenerlos aislados, reproducibles y fáciles de gestionar.

**El stack actual (en /home/jokoalmi/automation-stack/):**

| Servicio | Puerto | Qué es | Para qué se usa en el lab |
|----------|--------|--------|---------------------------|
| **n8n** | 5678 | Plataforma de automatización visual (nodos conectados) | Automatizaciones (ej: workflow ENVIO WHATSAPP) — ZONA PROTEGIDA |
| **stirling-pdf** | 8081 | Suite de utilidades PDF (convertir, dividir, OCR...) | Tratar PDFs |
| **pdf-cleaner** | 8000 | Servicio propio para limpiar PDFs | Limpiar PDFs |
| **ollama** | 11434 | Motor de inferencia local secundario | Modelos locales alternativos; en este lab es secundario (LM Studio es el principal) |

**Regla crítica de Docker:**
- SIEMPRE usar `docker compose` (v2), NUNCA `docker-compose` (v1, obsoleto).
- `docker compose ps` muestra el estado real de los contenedores. NO usar `docker compose ls -a` para concluir si están activos.
- stop/restart/down/up -d/prune requieren confirmación explícita (el stack es zona sensible).
- **n8n es zona protegida**: no reiniciar, parar, recrear ni actualizar sin confirmación explícita.

### Servicios systemd (sobreviven a la sesión)

Además de Docker, hay servicios del sistema (systemd) que corren siempre:

| Servicio | Función |
|----------|---------|
| lmstudio-headless.service | Arranque headless LM Studio + carga GLM (visión) |
| lmstudio-monitor.service | Monitor web en :5000 (dashboard de observabilidad) |
| joko-indexer.service | Watchdog de re-indexación RAG (incremental v2) |
| joko-reranker.service | Daemon del reranker (CPU, --max-seq 256, Nice=-10) |
| team-bus-watch.service | File bus multi-sesión (polling 5s, snapshot README) |
| hermes-gateway.service | Gateway de Telegram (Hermes) |
| hermes-pipeline-proxy.service | Proxy de observabilidad del pipeline LLM (TTFB, tokens) en :9911 → DeepSeek |
| chrome-lab.service | Chrome headless para browser-use (:9224) |
| comfyui.service | Servidor de generación de imágenes (SDXL/ComfyUI, GPU) |

(9 unit files propios del lab verificados 04-sep-2026; 8 enabled —comfyui bajo demanda—. Los demás servicios de usuario activos son de GNOME/escritorio, no del lab.)

**systemd** = el sistema de arranque y gestión de servicios de Linux. "Servicio de usuario" = corre bajo tu usuario, no como root.

### Protocolos de sesión (por qué existen)

- **inicio.sh** — al abrir sesión: ejecuta checks (git, docker, GPU...), genera estado-inicial.json y lo compara con el último cierre para detectar cambios.
- **fin.sh** — al cerrar: snapshot final, diff, backup git, informe, y PARA el stack Docker (comportamiento por diseño: ahorro de energía nocturno). Al día siguiente hay que levantarlo con inicio.sh o `docker compose up -d`.
- **checkpoint.sh** — durante la sesión: punto de recuperación sin cerrar.

**¿Por qué estos protocolos?** Para que ninguna sesión "pierda" el estado: sabes qué cambió entre una sesión y otra, y puedes recuperarte a mitad de camino.

### Repaso capítulo 4
- Docker = contenedores; Docker Compose = varios contenedores definidos juntos.
- Stack: n8n (automatización), stirling-pdf, pdf-cleaner, ollama.
- n8n es zona protegida. Siempre `docker compose` (v2).
- Servicios systemd (9 unit files): LM Studio, monitor, indexer, reranker, file bus, gateway, proxy, chrome-lab, comfyui.
- inicio.sh / fin.sh / checkpoint.sh = protocolos para no perder estado entre sesiones.

---

## Capítulo 5: LM Studio — el motor de inferencia local

**LM Studio** es el motor que ejecuta modelos de IA EN TU GPU (sin internet). Expone una API compatible con OpenAI en `http://localhost:1234/v1`.

**¿Por qué existe?** Porque no todo debe ir a la nube: los modelos locales son gratis, privados (tus datos no salen del equipo) y funcionan sin conexión. DeepSeek (cloud) es el que "piensa y decide"; LM Studio es el que "ve y evalúa".

**Abstracción importante:** la herramienta actual es LM Studio, pero el conocimiento (parámetros, metodología, modelos) está abstraído. Si mañana se sustituye por vLLM u Ollama, las capacidades permanecen. (Principio JL-011: el flujo del conocimiento tiene prioridad sobre la optimización de herramientas.)

### Cómo funciona por dentro

```
Proceso lm-studio (daemon, se inicia con la GUI o autostart)
    └── hijo llama-server → atiende :1234 (API OpenAI-compatible)
```

**Daemon** = proceso que corre en segundo plano de forma continua.
**API** = interfaz que permite a otros programas pedirle cosas (en este caso, generar texto).

### Los modelos (inventario real, 04-sep-2026 — 11 modelos verificados por API)

**Modelos "no-reasoning"** (responden directamente):

| Modelo | Cuant. | VRAM | Velocidad | Resultado |
|--------|--------|------|-----------|-----------|
| dolphin3.0-llama3.1-8b | Q4_K_M | 4.58 GiB | 5.6s | 5/5 ✅ |
| granite-4.1-8b | Q4_K_S | 4.74 GiB | 15.6s | 5/5 ✅ (mejor T2 no-reasoning) |
| granite-4.0-h-tiny | Q4_K_S | 3.72 GiB | 23.7s | 5/5 ✅ (mínima VRAM) |
| lfm2.5-2.6b | Q4_K_M | 1.67 GiB | 55 tok/s | 7/7 ✅ (batería 06-ago, tool calling) |

**Modelos "reasoning"** (piensan antes de responder, con cadena de pensamiento):

| Modelo | Cuant. | VRAM | Velocidad | Resultado |
|--------|--------|------|-----------|-----------|
| deepseek-r1-distill-qwen-14b | Q4_K_M | 8.37 GiB | 73.4s | 5/5 ✅ |
| gemma-4-12b-qat | Q4_0 | 6.66 GiB | 88.4s | 5/5 ✅ |
| glm-4.6v-flash | Q4_K_M | 7.41 GiB | 54.2s | 4/5 ⚠️ (rol=visión) |
| openai/gpt-oss-20b | MXFP4 | — (no medido) | — (no medido) | Delegación validada 6/6 ✅ (04-sep); sustituye a r1-14b/llama31 en delegation.model |
| lfm2.5-vl-3b | — (no medido) | — (no medido) | — (no medido) | Respaldo visión VLM (04-sep): cuando vision_analyze/GLM cae |

**Términos que necesitas para leer la tabla:**
- **Cuantización (Q4_K_M, Q4_0...)** = técnica para reducir el tamaño del modelo (y su uso de VRAM) perdiendo un poco de calidad. 4 bits = equilibrio calidad/precio.
- **GiB** = gigabyte binario (unidad de memoria). Aquí, VRAM que ocupa el modelo.
- **5/5** = pasó los 5 tests del protocolo de evaluación (JL-010).

**Modelos de embeddings** (para el RAG, capítulo 6 — NO para chat):
- text-embedding-bge-m3 (1024 dimensiones, ganador por soportar español)
- text-embedding-nomic-embed-text-v1.5 (768 dimensiones, alternativa)

### La regla del max_tokens (por qué existe)

Los modelos reasoning separan su salida en dos canales:
- `reasoning_content` → la cadena de pensamiento interna (invisible para ti)
- `content` → la respuesta real

**El problema:** los tokens de razonamiento CUENTAN contra el máximo. Si el presupuesto (max_tokens) es bajo, el modelo se gasta todo en pensar y la respuesta sale VACÍA.

**Regla práctica:**
- max_tokens mínimo: 400 (solo prompts triviales)
- max_tokens recomendado: 1024-2048 (uso real)
- max_tokens con visión: 2000 mínimo
- Ratio razonamiento:respuesta ≈ 10:1

**Síntoma de max_tokens insuficiente:** `content` vacío con `finish_reason: "length"`, mientras `reasoning_content` tiene texto coherente.

### Cómo se elige el modelo por rol

| Necesidad | Modelo | Por qué |
|-----------|--------|---------|
| Chat rápido | Dolphin Cyber LoRA | 5.6s, 5/5 |
| Tool use / agentes | LFM 2.5 2.6B | 55 tok/s, tool calling nativo, 7/7 (06-ago) |
| JSON estructurado | Dolphin o Granite 4.1 | rápidos y fiables |
| Razonamiento ligero | Granite 4.1 8B | mejor T2 no-reasoning |
| Mínima VRAM | Granite 4.0 h-tiny | 3.72 GiB |
| Razonamiento pesado | DeepSeek R1 14B | 5/5, equilibrado |
| Razonamiento profundo | Gemma 4 12B | 5/5, calidad máxima |
| Visión rápida | GLM 4.6V Flash | único VLM rápido (15-30s) |
| Visión precisa | Gemma 4 12B | análisis detallado |
| Visión respaldo (si GLM/vision_analyze cae) | LFM 2.5 VL 3B | VLM ligero en LM Studio (:1234) |
| Delegación de tareas (subagentes) | gpt-oss-20b | validado 6/6 tareas reales (04-sep) |

**Retirados del catálogo (no existen en disco):** llama-3.1-8b, qwen3-14b,
gemma-4-e4b — sustituidos por LFM 2.5 2.6B y la rotación granite/deepseek/gemma.

**VLM** = Vision Language Model (ve imágenes y las describe).

### Monitor de observabilidad (:5000)

Hay un dashboard web (proyecto `/home/jokoalmi/lmstudio_real_monitor`, Flask + psutil + nvidia-smi) que muestra en vivo: VRAM, temperatura, CPU/RAM, modelos cargados y uso de API. Es "ver el corazón del motor latiendo".

### Repaso capítulo 5
- LM Studio = motor local en :1234, API OpenAI-compatible.
- Modelos: no-reasoning (responden) vs reasoning (piensan); embeddings (para RAG).
- Cuantización = reducir tamaño del modelo; VRAM = memoria de video (12 GB tope).
- max_tokens bajo = respuesta vacía en modelos reasoning.
- Cada rol tiene su modelo; el monitor (:5000) lo vigila.

---

## Capítulo 6: Hermes Agent — el cerebro que ejecuta

**Hermes Agent** (de Nous Research) es el agente que ejecuta las instrucciones del laboratorio. Es quien te lee, decide, ejecuta y documenta. Vive en `~/.hermes/` y se usa desde CLI, Telegram (gateway) o cron.

**¿Por qué existe?** Porque alguien tiene que orquestar todo: interpretar lo que pides, decidir qué modelo usar, ejecutar comandos, documentar resultados y mantener el conocimiento. Ese "alguien" es Hermes.

### Componentes principales

| Componente | Ruta | Función |
|------------|------|---------|
| config.yaml | ~/.hermes/config.yaml | Configuración (modelo, proveedor, gateway) |
| Skills | ~/.hermes/skills/ | Conocimiento procedimental (185 skills, 04-sep-2026) |
| Memoria | ~/.hermes/memories/ | Datos persistentes entre sesiones |
| Sesiones | ~/.hermes/ (DB) | Historial de conversaciones (session_search) |
| Cron | ~/.hermes/cron/ | Tareas programadas |
| Scripts | ~/.hermes/scripts/ | shared-events, session-state, consolidador... |

**Skill** = un procedimiento reutilizable que Hermes carga cuando lo necesita (como un "manual de instrucciones" para una tarea concreta). Ej: local-rag (cómo usar el RAG), lm-studio (cómo operar LM Studio).

**Memoria** = datos que se inyectan en CADA turno (quién eres tú, preferencias, entorno). La regla: lo que cambia en una semana NO va a memoria; los procedimientos reutilizables van a skills.

**Cron** = tareas programadas (a cierta hora o cada X minutos). Ej: informe diario a las 9:00 (script informe-diario-local.sh; el cron lista model=deepseek-v4-flash — mecanismo interno del script no verificado 04-sep), reindex RAG a las 8:00, consolidador a las 22:30.

### El modelo principal

```yaml
model:
  provider: deepseek
  default: deepseek-v4-flash
```

**DeepSeek** = el proveedor cloud principal (deepseek-v4-flash). Desde el 04-ago-2026, el lab decidió usar deepseek SIEMPRE (coste mínimo) y el modo PRO solo manualmente (comando /model).

### Gateway de Telegram

Permite hablar con Hermes desde el móvil. El canal_prompt inyecta el file bus (capítulo 9) + shared-events antes de responder, para que Telegram sepa el estado en vivo de todas las sesiones.

**Pitfall:** tras cambiar config del gateway hay que reiniciarlo desde OTRA shell (`hermes gateway restart`), nunca desde dentro del gateway.

**Integración Gemini API (06-ago-2026):** el lab tiene una key de Google AI Studio (proyecto "Hermes Agent") para usar Gemini programáticamente — visión fina, análisis de capturas con especificación técnica (paleta hex, tipografías, espiral). Modelo usable: `gemini-3-flash-preview`. La suscripción Google AI Pro NO da créditos de API. Detalle: skill google-ai-pro.

### Reglas de seguridad del agente (importantes)

1. NO ejecutar comandos automáticamente — proponer, esperar salida real.
2. n8n es zona protegida — no reiniciar/parar/modificar sin confirmación.
3. No inventar datos — si no aparece en la salida, decir "no aparece".
4. Comandos de solo lectura primero (ps, ss, df, free, nvidia-smi, curl).
5. sudo solo con autorización explícita.
6. No borrar/mover/modificar archivos sin autorización.
7. Formato de diagnóstico: salida cruda + resumen en español.

**¿Por qué estas reglas?** Porque el lab contiene datos valiosos (n8n, backups, conocimiento) y un agente que ejecuta comandos sin permiso podría romperlos. La seguridad es por diseño.

### Repaso capítulo 6
- Hermes = el agente que orquesta todo (CLI, Telegram, cron).
- Skills = procedimientos; Memoria = datos persistentes; Cron = tareas programadas.
- Modelo principal: deepseek-v4-flash (cloud, coste mínimo).
- Reglas de seguridad: no ejecutar sin permiso, no tocar n8n, no inventar datos.

---

# PARTE 3 — EL CONOCIMIENTO (el corazón del lab)

## Capítulo 7: LPA — el sistema de conocimiento

**LPA (Living Product Architecture)** es el programa de investigación del lab. La definición oficial:

> LPA es un sistema para construir sistemas complejos sin perder coherencia cuando intervienen humanos, IA y el paso del tiempo.

**¿Por qué existe LPA?** Porque cuando humanos + IA + tiempo colaboran en un sistema complejo, ese sistema tiende a DEGENERAR (perder coherencia). LPA es la respuesta: un sistema para que el conocimiento se acumule, se valide, evolucione y se retire de forma ordenada.

No es una metodología ni un framework. Es una **hipótesis fuerte [E2]** — un nivel de evidencia que verás a continuación.

### Los niveles de evidencia (E0-E4) — por qué existen

Todo conocimiento del lab pasa por niveles de evidencia:

| Nivel | Definición | Requisito | Derechos |
|-------|-----------|-----------|----------|
| E0 | Observación única | 1 experimento, 1 dominio | Ninguno |
| E1 | Patrón | 2+ experimentos, contextos distintos | Mencionable |
| E2 | Hipótesis | 2+ experimentos + falsificación fallida | Usable como guía |
| E3 | Validación | 3+ dominios distintos + falsificación fallida | Enseñable |
| E4 | Principio | 5+ dominios, 3+ categorías, 6 meses sin contraejemplos | Fundacional |

**E∅ — Revocado:** una afirmación que fue E1+ y fue falseada. NO se elimina: se marca con fecha y experimento.

**¿Por qué esta escala?** Para que una idea no se considere "cierta" por decirlo una vez. La evidencia va SIEMPRE por delante de la metodología. Un experimento no confirma: intenta falsear.

### El proceso epistemológico

```
Observación (E0) → Patrón (E1) → Hipótesis (E2) → Validación (E3) → Principio (E4)
```

**Candidate Principle:** estado intermedio entre E3 y E4 donde la hipótesis validada acumula evidencia longitudinal. La mayoría NUNCA alcanzan E4 — esa tasa de descarte es el mecanismo de defensa del sistema.

### Repaso capítulo 7
- LPA = sistema para construir sistemas complejos sin perder coherencia.
- Niveles de evidencia E0-E4: de observación única a principio fundacional.
- Un experimento no confirma: intenta falsear.

---

## Capítulo 8: Knowledge Objects (los KOs) — las piezas del conocimiento

Los **Knowledge Objects (KOs)** son las entidades con las que el lab almacena conocimiento: decisiones, reglas y políticas en archivos YAML con ciclo de vida, en `01-knowledge/objects/`.

**YAML** = formato de texto legible por humanos para datos estructurados (clave: valor).

| Tipo | Significado | Ejemplos reales |
|------|-------------|-----------------|
| **DEC** | Decisión | DEC-001, DEC-002, DEC-003, DEC-004, DEC-GAIPRO-001 |
| **RULE** | Regla activa derivada de DEC | RULE-001..009 |
| **POLICY** | Restricción global | POLICY-001, POLICY-002, POLICY-003 |
| **PRED** | Predicción con veredicto | PRED-001, PRED-002 |
| **PATTERN** | Patrón de conocimiento | PATTERN-001 |
| **OBS** | Observación factual | OBS-005/006/007 |
| **HYP** | Hipótesis | HYP-001 |

**Total a 5-ago-2026: 20 KOs.**

**¿Por qué existen los KOs?** Porque antes las decisiones/reglas vivían en archivos sueltos sin estructura. Ahora tienen un ciclo de vida: nacen, se validan, caducan, se revisan, se sustituyen. Eso es lo que permite que el conocimiento no se quede obsoleto.

### Esquema real de un KO (DEC-002)

```yaml
id: DEC-002
type: DEC
status: activo
created: '2026-07-28'
last_validated: '2026-07-31'
next_review: '2026-10-26'
expires: '2027-01-24'
confidence_label: NO_EVALUADA
evidence:
- 'EXP-20260728-003: Superior en razonamiento logico multi-paso'
domain: ai-architecture
scope: todo_joko_lab
body: "DeepSeek R1 destilado en Qwen 14B para tareas de razonamiento paso a paso. Límite de tokens: max_tokens 2048 (nunca menos)."
```

**Campos clave del ciclo de vida:**
- `expires` — cuándo caduca la validez
- `next_review` — cuándo hay que revisarlo
- `last_validated` — última validación
- `confidence_label` — NO_EVALUADA / BAJA / MEDIA / ALTA
- `dependencies` — de qué otros KOs depende
- `contradicts` — qué KO contradice
- `superseded_by` — qué KO lo sustituye

### Los ciclos del conocimiento (KAP, KVC, KEL, Pruning)

Estos son los "motores" que hacen vivir al conocimiento:

**KAP — Knowledge Assimilation Pipeline (M-001):** cómo entra CONOCIMIENTO EXTERNO al lab (videos, artículos, libros). Tres fases: Extracción → Revisión adversarial → Asimilación. Con 6 preguntas obligatorias (¿ya lo sabíamos? ¿cambia cómo trabaja el lab? ¿qué experimento podremos hacer mañana?...).

**KVC — Knowledge Validation Cycle (CP-003):** el ciclo de validar una decisión:
```
Observación → Análisis → Crítica adversarial → Falsación → DEC → Aplicación → Monitorización → ¿Mejoró? → conservar / reabrir
```
**Principio emergente:** la unidad de progreso no es el componente, es la DECISIÓN VALIDADA. "Una decisión sin monitorización no es una decisión — es una apuesta."

**KEL — Knowledge Evolution Loop:** la máquina de estados del conocimiento:
```
OBS → HIPOTESIS → EXP → EVIDENCIA → DEC → MONITORIZACION → REVALIDACION → (conservar | retirar)
```
Propiedad clave: incorpora el OLVIDO como operación de primer orden. Un sistema que solo acumula se degrada.

**Knowledge Pruning (poda):** 7 operaciones (VALIDAR, DEGRADAR, RETIRAR, DIVIDIR, FUSIONAR, VERSIONAR, ARCHIVAR). Regla: un sistema que solo añade sin retirar lo obsoleto se degrada por acumulación.

### Knowledge Health Auditor

Script `tools/knowledge_health.py` que mide la salud del conocimiento 0-100. **Progresión real: 31 → 43 → 67 → 70 → 76 → 88/100.** KHI < 50 requiere intervención.

### Evidence Contract

Umbrales verificables para promocionar EXP → DEC. Convierte el paso de "juicio" a "contrato verificable". Estado real: 0/9 KOs cumplen = deuda señalada (es un dato, no un fallo oculto).

### Normas constitucionales (JL)

Son las "leyes" del lab (JL-001..014). Algunas destacadas:
- JL-011: el flujo del conocimiento tiene prioridad sobre la optimización de herramientas.
- JL-013: la guía del lab se actualiza ante cada cambio estructural.
- JL-014: copia de seguridad antes de cambios grandes (creada 03-ago).

**RULE-008** (4-ago): backups dentro del árbol antes de tocar nada (`.bak-YYYYMMDD`).
**RULE-009** (5-ago): toda sesión que complete una tarea DEBE registrarla en el file bus + shared-events ANTES de declararla cerrada.

### Repaso capítulo 8
- KOs = piezas de conocimiento (DEC/RULE/POLICY/PRED/OBS/HYP) con ciclo de vida.
- KAP (asimilar externo), KVC (validar), KEL (evolucionar), Pruning (podar).
- Health Auditor mide la salud (88/100). Evidence Contract: EXP→DEC verificable.
- Normas JL = leyes del lab. RULE-008 (backups), RULE-009 (registrar al completar).

---

## Capítulo 9: Multi-sesión — cómo se sincronizan las sesiones

**El problema que resuelve:** Hermes ejecuta sesiones separadas por canal (CLI, Telegram gateway, cron). Cada una arranca con contexto VACÍO. Si trabajas en CLI y luego sigues por Telegram, la sesión de Telegram no sabe que estabas a mitad de algo.

**La solución:** un sistema de estado y eventos compartidos que todas las sesiones leen y escriben. Tres niveles:

| Canal | Archivo | Contenido |
|-------|---------|-----------|
| shared-state.json | ~/.hermes/shared-state.json | Estado vivo de cada sesión (activa/inactiva, temas) |
| shared-events.jsonl | ~/.hermes/shared-events.jsonl | Eventos relevantes (decisión, pendiente, completado...) |
| **file bus por dominio** | ~/.hermes/team-context/ | 1 archivo .md por dominio (cli, telegram, lab, biohacking, perfume, founderz...) |

**El file bus** (la capa principal desde 5-ago): cada sesión escribe SOLO en su dominio y todas leen todos. Un daemon (team-bus-watch.service) hace polling cada 5s y regenera el snapshot consolidado (README.md).

**RULE-009 (regla fija):** toda sesión que complete una tarea DEBE registrar ANTES de cerrarla: (1) evento en shared-events, (2) su dominio en el file bus. El bus NO se llena solo — es lectura bajo demanda. Sin registro, las otras sesiones ven info congelada aunque el trabajo se haya hecho (incidente real: Telegram no veía el trabajo del día).

**¿Por qué "por dominio"?** Para que cada sesión escriba donde le corresponde (la CLI en cli.md, Telegram en telegram.md, el lab en lab.md...) y no se pisen entre sí. Claim/release = advisory lock para recursos compartidos.

### Scripts útiles

```bash
# Eventos
bash ~/.hermes/scripts/shared-events.sh write cli completado "Resumen del evento"
bash ~/.hermes/scripts/shared-events.sh read --limit 10

# File bus
bash ~/.hermes/scripts/domain-bus.sh read [dominio]
bash ~/.hermes/scripts/domain-bus.sh write <dominio> "..."
bash ~/.hermes/scripts/domain-bus.sh claim "recurso" "motivo"
bash ~/.hermes/scripts/domain-bus.sh release "recurso"
```

### Repaso capítulo 9
- Sesiones separadas = contexto vacío; el file bus las sincroniza.
- File bus: 1 archivo .md por dominio; RULE-009 obliga a registrar al completar.
- El bus no se llena solo: hay que escribirlo.

---

# PARTE 4 — EL RAG (la memoria recuperable)

## Capítulo 10: ¿Qué es el RAG y por qué existe?

**RAG (Retrieval-Augmented Generation)** = generar respuestas usando información RECUPERADA de una base de conocimiento, en vez de solo el conocimiento interno del modelo.

**¿Por qué existe en el lab?** Porque un modelo de IA tiene un "conocimiento interno" (lo que aprendió al entrenarse), pero NO sabe lo que ha pasado en JOKO LAB (tus sesiones, decisiones, experimentos). El RAG le da acceso a esa memoria: cuando preguntas algo del lab, Hermes busca en la base los documentos relevantes y usa ese contexto para responder con datos reales.

**100% local, sin cloud** — tus datos no salen del equipo.

### Términos que necesitas (explicados desde cero)

- **Embeddings** = vectores numéricos que representan el significado de un texto. Dos textos parecidos tienen vectores parecidos (cercanos en el espacio). El modelo de embeddings del lab es BGE-M3 (multilingüe, 1024 dimensiones).
- **Base vectorial (LanceDB)** = base de datos especializada en guardar y buscar vectores. En lugar de buscar "palabras exactas" busca "significados cercanos".
- **Índice** = estructura que acelera las búsquedas. Dos tipos aquí: vectorial (por significado) y FTS (por palabras exactas).
- **Chunk** = fragmento de un documento (el indexador parte cada documento en trozos de ~1000 tokens con solapamiento de 150).
- **Reranker** = modelo que REORDENA los resultados por relevancia (un segundo filtro más preciso tras la búsqueda inicial).
- **Token** = unidad básica de texto (una palabra o parte de ella). Los modelos "cuentan" tokens.
- **Daemon** = proceso persistente que carga un modelo UNA vez y sirve peticiones (evita recargar cada vez).

### Los componentes del stack

| Componente | Qué es | Detalle |
|-----------|--------|---------|
| BGE-M3 | Modelo de embeddings | 1024 dimensiones, español nativo |
| LanceDB | Base vectorial | daemonless, zero-copy (Arrow) |
| indexer.py | Indexa documentos .md y .yaml | v2 INCREMENTAL (5-ago): hash sha256 + sidecar → solo re-embebe cambios |
| search.py | Búsqueda HÍBRIDA | FTS + vectorial + RRF (5-ago), filtros --type/--status |
| context_builder.py | Inyecta contexto al LLM | detecta tipo + busca + formatea ESTRUCTURADO |
| knowledge_resolver.py | Sintetiza conocimiento | hechos, conflictos, decisiones, confianza |
| lmstudio_embeddings.py | Embeddings via LM Studio API | evita competencia por VRAM |
| reranker_daemon.py | Daemon del reranker | carga CrossEncoder UNA vez, sirve /rerank en :8765 |

### El flujo completo (cómo funciona de punta a punta)

```
Documentos .md/.yaml → indexer.py v2 (hash incremental) → embeddings BGE-M3 → LanceDB
                                                          ↓
Pregunta → search.py (HÍBRIDA: FTS + vectorial + RRF → filtros type/status → reranker)
              ↓
context_builder.py (contexto inyectado al prompt + índice OKF vigencia)
              ↓
knowledge_resolver.py (conocimiento estructurado)
              ↓
LLM responde con contexto real
```

### La evolución del RAG (por qué es como es hoy)

**1. El cuello de botella de GPU (resuelto 31-jul):** BGE-M3 cargado independientemente competía con LM Studio por la misma GPU → 75% de queries devolvían contexto vacío. **Solución:** usar el endpoint de embeddings de LM Studio (localhost:1234/api/v0/embeddings) → 59ms, sin VRAM extra.

**2. El daemon del reranker (2-ago):** search.py tardaba ~15s por consulta porque cada ejecución importaba sentence_transformers (~8s) y cargaba el CrossEncoder a CUDA (~11s). **Solución:** daemon persistente que carga el modelo UNA vez + lazy import. Resultado: 14.8s → 2.6s.

**3. El indexador incremental (5-ago):** re-indexar TODO el vault tardaba ~2h. **Solución:** hash sha256 por documento + sidecar → solo re-embebe lo que cambió. Resultado: ~30s por pocos archivos. Y si la GPU está ocupada (GLM cargado), cae a CPU automáticamente (fallback OOM→CPU).

**4. El cuello del reranker en CPU (5-ago):** con 10 pares a puntuar, el rerank costaba ~6s (97% del tiempo). **Causa:** bge-reranker-v2-m3 en CPU cuesta ~0.6s/par, y el coste escala con la longitud. **Fix en 3 capas:** TOP_K_RETRIEVE 10→5 (el top-3 resultante es IDÉNTICO, verificado), max-seq 256 (limita tokens por fragmento), Nice=-10 (prioridad del daemon). Resultado: 6.24s → **3.23s**, calidad idéntica.

**5. Búsqueda híbrida FTS + vectorial (5-ago):** antes solo buscaba por significado (vectorial). Ahora busca por significado Y por palabras exactas (FTS, BM25) y fusiona por RANGO con **RRF (Reciprocal Rank Fusion)** — porque los scores BM25 y las distancias NO son comparables entre sí, así que se fusiona por posición, no por puntuación. El indexer recrea los índices tras cada re-index (si no, el watchdog los destruiría en silencio).

**6. Filtros por frontmatter (5-ago):** search.py acepta `--type` y `--status` (pre-filtro por frontmatter del documento). Ejemplo real: `-q "reglas" --type RULE` devuelve SOLO reglas RULE.

### Métricas reales (para que veas la escala)

| Operación | Volumen | Tiempo |
|-----------|---------|--------|
| Indexación completa | 42,931 filas | ~90s (GPU) / ~4h (CPU, no usar) |
| Re-index incremental v2 | solo cambios | ~30s por pocos archivos |
| Búsqueda híbrida (5-ago) | 5 recuperados, 3 devueltos | ~3.2s en caliente |
| Búsqueda antigua | 10 recuperados | ~6.2s |

### Verificación determinista (anti-Goodhart) — por qué existe

Para medir si el conocimiento realmente se capitaliza (y no que "un LLM juzgue a otro LLM"), existe un banco de preguntas objetivas (`verification/bank.yaml`) con respuestas esperadas y rutas fuente. `run_eval.py` ejecuta la evaluación con un modelo (recomendado: granite-4.1-8b).

**Reglas:**
- El banco NO debe estar indexado en el RAG (contaminación).
- Las keywords de la respuesta esperada deben existir literalmente en la fuente.
- Evaluador `completitud_parcial`: detecta el fallo silencioso (respuesta que suena completa pero le falta 1 de N hechos).

### Comandos útiles

```bash
# Buscar en el RAG (híbrido)
~/.venv/hermes-rag/bin/python3 ~/joko-lab/tools/search.py --query "consulta" --top_k 3

# Con filtros por frontmatter
~/.venv/hermes-rag/bin/python3 ~/joko-lab/tools/search.py --query "reglas" --top_k 3 --type RULE
~/.venv/hermes-rag/bin/python3 ~/joko-lab/tools/search.py --query "vigentes" --top_k 5 --status activo

# Re-indexar (incremental: solo cambios; --force = total ~4h CPU, evitar)
~/.venv/hermes-rag/bin/python3 ~/joko-lab/tools/indexer.py --device cpu
~/.venv/hermes-rag/bin/python3 ~/joko-lab/tools/indexer.py --dry-run   # ver qué haría sin tocar

# Contexto inyectado (lo que ve el LLM)
echo "consulta" | ~/.venv/hermes-rag/bin/python3 ~/joko-lab/tools/context_builder.py

# Conocimiento estructurado
echo "consulta" | ~/.venv/hermes-rag/bin/python3 ~/joko-lab/tools/knowledge_resolver.py
```

### Repaso capítulo 10
- RAG = recuperar conocimiento del lab para responder con datos reales (no solo memoria del modelo).
- Embeddings = vectores de significado; LanceDB = base vectorial; chunks = fragmentos; reranker = reordena.
- Evolución: GPU bottleneck → daemon → indexador incremental → reranker optimizado → híbrido FTS+vectorial → filtros.
- Verificación determinista: banco de preguntas con respuestas esperadas.

---

# PARTE 5 — LA ARQUITECTURA

## Capítulo 11: El AI Router y las 4 capas

**AI Router** = el sistema que decide QUÉ modelo/proveedor se usa para cada tarea, basado en políticas y estado. Es determinista (no usa un LLM para decidir): recibe input, aplica reglas, devuelve JSON.

**La arquitectura en 4 capas (por qué existe):**

```
CAPA 1 — Infraestructura      (LM Studio, DeepSeek, Hermes)
CAPA 2 — Recuperación         (RAG, Knowledge Resolver, Context Builder)
CAPA 3 — Gobierno del conocimiento (KAP, Health Auditor, KOs, Decision Engine)
CAPA 4 — Evolución del conocimiento (KVC, KEL, Pruning, Evidence Contract)
```

**¿Por qué 4 capas?** Para separar responsabilidades: la infraestructura provee (modelos), la recuperación consulta (memoria), el gobierno regula (qué conocimiento es válido), y la evolución mantiene vivo el ciclo (nace → valida → retira).

### Los componentes del Runtime

```
State Manager       — observa, escribe state.json (cada 60s, 0% CPU)
Policy Engine       — interpreta políticas, nunca decide
Capability Registry — describe capacidades, nunca decide
Decision Engine     — decide basado en state + policies (7.5ms, sin LLM)
Runtime API         — interfaz estable (Runtime.resolve(), 9 campos)
Metrics             — datos de uso para decisiones basadas en evidencia
```

**Regla contract-first:** todo componente expone contrato (YAML/JSON) antes que implementación. **¿Por qué?** Para que los componentes puedan intercambiarse sin romper nada: el contrato es la interfaz estable.

### El flujo de decisión

```
apply-decision.sh (cron cada 30 min o bajo demanda)
    ↓
Runtime.resolve()  ← runtime/api.py — ÚNICA puerta de entrada
    ↓
decision_engine.decide()  ← puro: solo {provider, model, reason}
    ├── lee state.json (State Manager)
    ├── lee policies/*.yaml (8 archivos, 100% declarativas)
    └── devuelve {provider, model, reason}
    ↓
escribe ultima-decision.json + decision.log
    ↓
devuelve 9 campos: {provider, model, reason, policy, privacy,
                    verification, confidence, expires, decision_id}
    ↓
apply-decision.sh → hermes config set (modelo/proveedor/URL)
```

**El Decision Engine es PURO:** solo recibe input y devuelve JSON. No escribe archivos, no modifica config, no conoce ~/.hermes/. **¿Por qué?** Porque un componente que solo decide (y no actúa) es fácil de probar y no puede romper nada por efecto secundario.

### Las 8 políticas YAML

| Archivo | Propósito |
|---------|-----------|
| privacidad.yaml | Datos sensibles → forzar local (precedencia 1) |
| disponibilidad.yaml | Fallback si un proveedor cae |
| costes.yaml | Saldo mínimo antes de cloud |
| gpu.yaml | Desactivada para modelo principal (04-ago) |
| horario.yaml | Todo el día deepseek (04-ago) |
| niveles.yaml | Nivel de verificación por tarea |
| preferencias.yaml | Fallback final por defecto |
| modelos.yaml | Modelo por defecto por proveedor |

**Precedencia:** privacidad → disponibilidad → costes → GPU → horario → niveles → preferencias.

### La taxonomía de capacidades (JL-007)

El router NO pregunta "¿qué modelo?" sino "¿qué CAPACIDAD necesito?":
- **Cognitivas:** Conocimiento, Razonamiento, Creatividad, Código, Español, Consistencia
- **Funcionales:** JSON, Tool Calling, Visión, Memoria
- **Operativas:** Velocidad

Ejemplo:
```
Misión: landing página
  → ¿Necesito Visión? Sí → GLM (Visión=9)
  → ¿Necesito Creatividad alta? Sí → Gemma (Creatividad=10)
  → ¿Necesito Velocidad? Sí → Dolphin (Velocidad=10, Código=8)
```

### Repaso capítulo 11
- AI Router = decide qué modelo usar (determinista, sin LLM).
- 4 capas: infraestructura, recuperación, gobierno, evolución.
- Decision Engine es puro (no escribe, no actúa, solo decide).
- 8 políticas con precedencia; taxonomía por capacidades, no por modelo.

---

# PARTE 6 — LOS PRODUCTOS

## Capítulo 12: Los productos del lab (por qué el lab produce cosas)

**Distinción fundamental:** Joko Lab NO es un fin en sí mismo. Es el MEDIO (infraestructura + conocimiento + metodología) para producir PRODUCTOS reales.

```
Joko Lab (laboratorio)
    ↓ produce
PRODUCTOS (Perfume IA, Forense Digital, ...)
    ↓ generan
Problemas reales
    ↓ revelan
Principios
    ↓ suben a
LPA (conocimiento)
    ↓ retroalimenta
Joko Lab
```

**Regla LPA (dirección del conocimiento):** la dirección siempre es desde el proyecto hacia LPA, nunca al revés. LPA se desarrolla construyendo productos reales y observando qué principios sobreviven.

**Productos actuales:**
1. **Perfume IA** — Experimento 001 (tu colección personal con IA)
2. **Forense Digital** — peritaje informático (servicio real)
3. **Monitor LM Studio** — herramienta de observabilidad interna
4. **Benchmarks** — evaluación sistemática de modelos
5. **Experimentos LPA** — bolsa, mente-natural, psicología
6. **Biohacking Cerebral** — optimización cognitiva natural

### Perfume IA (el primer producto)

**Qué es:** una aplicación web para gestionar y descubrir tu colección de perfumes con IA. El "primer espécimen vivo de LPA": cada problema que revela alimenta el conocimiento.

**Datos reales (verificados 04-sep-2026):**
- Colección amplia (indeterminado) — la BD refleja tu colección REAL física, no el catálogo de Parfumo. (Regla del usuario: la guía no indica cifras de la colección porque cambian y se quedan obsoletas.)
- Los 8 perfumes de Mario Galindo (The Lab) están registrados.
- El chat consulta la colección REAL antes de cada mensaje.

**RAG sobre la colección (3 capas):** BGE-M3 + LanceDB para no competir con Dolphin en GPU. El chat consulta la colección real antes de cada mensaje.

**Anti-alucinación (3 capas):** fallback con top-5 del motor LPA si el RAG devuelve <2; prompt estricto ("NUNCA inventes un perfume que no esté en las listas"); post-filtro con regex. ~95% de alucinaciones atrapadas, 0 falsos positivos.

**Motor de recomendación (LPA v2):** 5 factores: temperatura, humedad, estación, hora del día, laboral/fin de semana. OJO: usa Erandio fijo — en días de viaje el motor NO sirve (usar open-meteo + SQLite directo).

**Servicio:** Flask en :5050. Arranque: `start-web.sh` o `scripts/inicio-perfume.sh`.

### Forense Digital

Un producto/servicio de peritaje informático: análisis de buzones de correo para procedimientos judiciales laborales en España. NO es "buscar correos": es peritaje con CADENA DE EVIDENCIA. Caso real 2026: 8.545 correos analizados.

### Repaso capítulo 12
- El lab produce productos; los productos revelan principios que suben a LPA.
- Perfume IA = primer producto (colección real + IA, anti-alucinación 3 capas).
- Forense Digital = peritaje con cadena de evidencia.

---

# PARTE 7 — CIERRE

## Capítulo 13: Mapa mental de todo el sistema

```
                ┌─────────────────────────────────────┐
                │          JOKO LAB                   │
                │  (lab para producir productos)      │
                └─────────────────────────────────────┘
                                   │
        ┌──────────────┬───────────┴───────────┬──────────────┐
        │              │                       │              │
   HARDWARE       HERMES (agente)         CONOCIMIENTO    PRODUCTOS
   A2000 12GB     orquesta todo            LPA + KOs      Perfume IA,
   i5-9500        skills/memoria/cron      E0-E4, KEL     Forense...
        │              │                       │              │
   DOCKER          MODELOS                  RAG            decisiones
   n8n, ollama     DeepSeek (cloud)         embeddings     reales →
   stirling-pdf    LM Studio (local)        LanceDB        principios
        │              │                       │              │
   SYSTEMD         ROUTER                   búsqueda        suben a LPA
   servicios       (qué modelo usar)        híbrida FTS     → mejoran el lab
   (daemons)       por política             + vectorial
        │              │                       │
   FILE BUS        TELEMETRÍA              VERIFICACIÓN
   sincroniza      mide lo real            banco anti-
   sesiones                                Goodhart
```

**Las 4 ideas que resumen TODO el lab:**

1. **Los 4 cerebros:** DeepSeek decide, LM Studio ve, Ollama simula, Telemetría mide. Quien decide no ve, quien ve no decide.
2. **El conocimiento vive en KOs con ciclo de vida:** nacen, se validan (E0-E4), se revisan, caducan, se retiran. Un sistema que solo acumula se degrada.
3. **El RAG da memoria real:** embeddings + LanceDB + búsqueda híbrida + reranker. Los datos del lab no salen del equipo.
4. **El lab produce productos, no solo conocimiento:** los productos revelan problemas reales, que generan principios, que suben a LPA.

---

## Capítulo 14: Cómo seguir (después de esta guía)

1. **Para consultar datos exactos** (puertos, comandos, rutas): `GUIA-JOKO-LAB.md`.
2. **Para ver el estado real del sistema:** `nvidia-smi`, `docker compose ps`, `free -h`, `df -h`.
3. **Para probar el RAG con tus propias preguntas:** los comandos del capítulo 10.
4. **Para entender un skill concreto:** pide a Hermes que cargue esa skill y te la explique.
5. **Cuando el lab cambie:** la GUIA-JOKO-LAB.md se actualiza (JL-013); esta guía de aprendizaje debería revisarse también.

---

## APÉNDICE: Mini-glosario de los términos que aparecen en esta guía

| Término | Definición simple |
|---------|-------------------|
| VRAM | Memoria de video (12 GB en la A2000 — el tope del lab) |
| Embeddings | Vectores que representan el significado del texto |
| Token | Unidad básica de texto que los modelos cuentan |
| Chunk | Fragmento de documento (el indexador parte en trozos) |
| Cuantización | Reducir el tamaño del modelo (Q4_K_M = 4 bits) |
| Daemon | Proceso persistente en segundo plano |
| API | Interfaz para que programas se comuniquen |
| RAG | Generar respuestas usando info recuperada de una base |
| Reranker | Modelo que reordena resultados por relevancia |
| FTS | Búsqueda por palabras exactas (BM25) |
| RRF | Fusión por rango de dos listas de resultados |
| LanceDB | Base de datos vectorial (guardar/buscar vectores) |
| KO | Knowledge Object: pieza de conocimiento con ciclo de vida |
| LPA | Living Product Architecture: el programa de investigación |
| E0-E4 | Niveles de evidencia (de observación a principio) |
| KAP | Asimilar conocimiento externo al lab |
| KVC | Validar decisiones (ciclo) |
| KEL | Evolucionar conocimiento (maquina de estados) |
| Pruning | Podar conocimiento obsoleto |
| systemd | Sistema de servicios de Linux |
| Skill | Procedimiento reutilizable que Hermes carga |
| Cron | Tarea programada |
| Gateway | Conexión de Hermes con plataformas (Telegram) |
| File bus | Sistema de archivos compartidos entre sesiones |
| sidecar | Archivo auxiliar (aquí: hashes para indexar solo cambios) |

---

FIN DE LA GUIA DE APRENDIZAJE

*Versión 1.1 — 2026-08-06. Revisión estructural sobre GUIA-JOKO-LAB.md (v1.2.0, actualizada 06-ago-2026).*
