---
title: "Análisis — «What happens when your LLM provider goes down?» (datasciencebrain, 03-oct-2026)"
type: research
---

# Análisis — "What happens when your LLM provider goes down?" (datasciencebrain)

**VERACIDAD:** caption literal `[VERIFICADO]` · claim LiteLLM contrastado con docs oficiales `[VERIFICADO]` · contenido de las slides `[NO VERIFICADO — no leído]`

**Fuente:** https://www.instagram.com/datasciencebrain/p/DeDqYXvGDqE/
**Fecha:** el post se anuncia como *October 3, 2026* (OG); el informe IG del cron lo marca 04-oct 05:24 (Madrid)
**Método:** caption completo del post (OG + DOM renderizado) + verificación del claim técnico contra la documentación oficial de LiteLLM. **Las slides de la "guía completa" NO se han podido leer**: LM Studio no tenía el API server levantado (medido 04-oct 14:26 CEST → puerto 1234 sin ninguna escucha, `HTTP:000`, VRAM 677 MiB / 12282 MiB, ningún modelo cargado). Sin VLM local no hay lectura de imagen. Análisis entregado con **límite declarado**.

## CONTENIDO (caption literal)

> Interviewer: "What happens when your LLM provider goes down?"
> Most candidates: "...it shows an error?"
> The answer that gets you hired: "It fails over to another provider, and the user never knows."
>
> Build it once and you'll never fumble this question:
> → Provider abstraction: one call, any model
> → Retry with exponential backoff and jitter
> → Circuit breakers: closed, open, half-open
> → Graceful degradation, so nothing ever crashes
> → Plus the same thing rebuilt in LiteLLM, so you know both
>
> This is the reliability layer behind every serious AI product.

Formato del post: reel/carrusel de marca personal con estructura "entrevistador / candidato mediocre / respuesta que contrata" y lista de 5 bloques con flecha `→`. El resto del caption es monetización (PDF de la guía para suscriptores, Rs.45/mes) y promoción del canal — **bait de suscripción, no contenido**.

## Verificación del claim central (LiteLLM)

Contrastado con `docs.litellm.ai` (páginas *Router - Load Balancing*, *Fallbacks (Provider Failover)*, *config_settings*):

- **Fallbacks** (failover de proveedor) existen: `fallbacks=[{"modelo_a": ["modelo_b"]}]`, en orden, y por tipo de error: `context_window_fallbacks`, `content_policy_fallbacks` y `fallbacks` para el resto (429/500...).
- **Retries + timeouts** existen: la doc los lista junto a los fallbacks, con backoff fijo + exponencial.
- **Cooldowns** = el "circuit breaker" del post: `allowed_fails` (fallos por minuto antes de enfriar un deployment), `cooldown_time` (segundos de enfriamiento), `disable_cooldowns`. Los fallos se aíslan **por deployment**, no por grupo de modelos.
- **Recuperación**: al expirar el cooldown, el deployment se re-habilita solo y vuelve progresivamente a la rotación (reset del contador de fallos) → eso ES el estado *half-open*.
- **Políticas por excepción**: `RetryPolicy` (num_retries según la excepción) y `AllowedFailsPolicy` (umbral de fallos por tipo de error).

**Matices honestos:**
1. LiteLLM **no usa el término "circuit breaker"** en su documentación; usa *cooldown*. La equivalencia es razonable (cerrado → abierto tras `allowed_fails` → reintento tras `cooldown_time`), pero es una traducción de conceptos, no una feature con ese nombre.
2. El **jitter** no aparece en la doc del router; es un patrón estándar de reintentos (evitar tormenta sincronizada). El post lo nombra pero no lo desarrolla.

## Aplicación al LAB

| Patrón del post | Estado real en el lab | Veredicto |
|---|---|---|
| Provider abstraction ("one call, any model") | `tools/llm-router.sh` + `tools/decision_router.py` clasifican por tipo (batch/vision/check); no hay una capa única de abstracción de proveedor | 🟡 parcial |
| Retry con backoff + jitter | **No existe en el router**: grep de `backoff|jitter|retry|num_retries` en `tools/*.py` no devuelve nada del enrutado (el único `COOLDOWN` es el temporizador de `tools/watch_indexer.py`, ajeno) | ❌ hueco real |
| Circuit breaker (closed/open/half-open) | No existe: no hay `cooldown`, `allowed_fails` ni marcado de motor "enfermo" | ❌ hueco real |
| Degradación elegante | El diseño local→cloud escala al fallar el **verifier** (salida corrupta), no cuando **cae el proveedor** | 🟡 parcial |
| LiteLLM como implementación | El lab llama a la API oficial de DeepSeek y usa su proxy `:9911`; no usa LiteLLM como router | 🟡 referencia |

**Confirma un pendiente ya identificado por el lab** — `research/local-cloud-orchestrator-diseno.md`, "Qué falta para producción", punto 6: «Pitfall conocido (ai-router): "try local, escalate to cloud" no existe nativamente en Hermes (solo fallback por error HTTP). Este orquestador LO CONSTRUYE explícitamente».

Es decir: **no descubre el problema, le pone vocabulario e implementación de referencia** (los dos números que faltaban: umbral de fallos y ventana de enfriamiento).

## Formatos reutilizables

- Estructura de gancho "pregunta de entrevista → respuesta mediocre → respuesta que contrata" (útil para LinkedIn, ya probada en el post de `hackproduct`).
- Lista de 5 bloques con `→`, un patrón por línea, sin desarrollo: formato de "mapa mental", no de tutorial.

## Veredicto honesto

- **CONFIRMA + concreta** un hueco propio y ya documentado (resiliencia del enrutado local/cloud). El valor está en el vocabulario y en la implementación de referencia, **no** en el caption.
- **El contenido real (código) está en las slides y NO se ha leído.** Sin VLM no se puede cerrar ese análisis; se entrega con límite declarado.
- **Backlog:** 2 ítems (cooldown/umbral en el enrutado del lab; decidir LiteLLM como capa vs. implementar el cooldown a mano en el orquestador).

---

## AMPLIACIÓN (04-oct-2026, ~15:00 CEST) — LECTURA DE LAS 20 LÁMINAS CON VLM LOCAL

**Qué cambia:** el límite declarado arriba («las slides NO se han podido leer») queda **subsanado**. El post **no es un reel ni una imagen única**: es un **carrusel de 20 láminas** que reproduce un **documento técnico troceado**. Láminas 1–19 = portada + páginas 1–18 del documento; lámina 20 = CTA de suscripción (el documento se corta a mitad de la sección 11). *La línea de VERACIDAD de la cabecera se deja tal cual: la rectificación se AÑADE, no se reescribe (regla de `edicion-aditiva-registros` §3).*

**Instrumento:** VLM local `glm-4.6v-flash` en LM Studio headless (`http://localhost:1234`), 20 láminas 1440×1800 sin redimensionar, 20/20 en **1136 s** (~19 min, 3 workers). Transcripción literal guardada en **`research/transcripcion-datasciencebrain-llm-router-failover-20261004.txt` (39.357 B, md5 `3094d101…`)**; origen: `/tmp/ig_dl/slides_texto.json` (39.940 B, md5 `b7c2ba49…`).

**Título del documento:** *«Build an LLM Router That Survives Provider Outages — in 40 Minutes»*. Stack declarado y verificado por el autor el 03-oct: Python 3.12 + `uv`, `google-genai==2.28.0`, `groq==1.7.0`, `ollama==0.6.3`, `litellm==1.103.2`, `python-dotenv==1.2.4`; modelos `gemini-3.5-flash-lite`, `openai/gpt-oss-20b` (Groq), `llama3.2:3b` (Ollama local, «2 GB, último recurso: rápido y JSON válido, ~3 s en un portátil»).

### Lo que dice el documento (apartados 1–11, antes del corte)

1. **El problema:** un 429 o un 503 («model is experiencing high demand») mata al agente a mitad de trabajo. En tiers gratuitos no es raro: `gemini-3.5-flash` respondió 503 a un simple «say hi» el día de la prueba.
2. **Arquitectura:** `Gemini (primario) → Groq (fallback) → Ollama local (último recurso) → mensaje de espera + ticket marcado para humano`. El agente **solo habla con el router**, y el historial de conversación pertenece al agente, nunca a un proveedor (así sobrevive al failover).
3. **Abstracción de proveedor:** una única `await provider.complete(messages)` con mensajes en forma OpenAI; cada SDK se traduce a **un solo** `ProviderError` con `retryable` y `retry_after`. Lista cerrada de códigos reintentables: **`RETRYABLE_STATUS = {408, 429, 500, 502, 503, 504}`**; 401/400/404 son fatales y no se reintentan («reintentar un 401 solo hace esperar tres veces por el mismo fallo»).
4. **Reintento con backoff:** `MAX_RETRIES = 2`, `BACKOFF_BASE_S = 0.5`, `BACKOFF_CAP_S = 8.0`, **full jitter** (`random.uniform(0, min(cap, base * 2**attempt))`). Regla fina: **si el servidor dice cuánto esperar se le cree, salvo que pida más que el cap** → entonces no se espera, **se hace failover** (caso real: Gemini mandó `retryDelay: "41s"`; nadie espera 41 s teniendo otro proveedor).
5. **Circuit breaker:** 3 estados (closed / open / half-open) con **probe perezoso** (`allow()` mueve open→half_open al expirar el enfriamiento). Parámetros: **`BREAKER_THRESHOLD = 2`**, **`BREAKER_COOLDOWN_S = 30.0`**, timeout por llamada **`CALL_TIMEOUT_S = 30.0`**. Reloj **inyectable** (`clock: Callable = time.monotonic`) para que el self-test salte los 30 s sin esperarlos.
6. **Nuance que suele faltar:** cuenta como **un** fallo *una llamada que falló tras agotar sus reintentos*, no cada intento → «**los reintentos gestionan los parpadeos; el breaker gestiona las caídas**». Con `MAX_RETRIES=2`, un proveedor muerto cuesta 3 intentos y ≤1,5 s; el breaker evita pagar eso en cada ticket.
7. **Un único dueño de los reintentos:** `AsyncGroq(max_retries=0)` (por defecto reintenta 2 veces → los logs mentirían y el backoff propio se apilaría) y `google-genai` reintenta **solo** si se le pasa `retry_options` (no lo hacen). Regla explícita: una sola capa posee los reintentos.
8. **Degradación elegante:** `Reply` = `text + provider + attempts + failovers + latency_s`; si todo cae, `DEGRADED_TEXT` en **el mismo JSON** que devuelve un modelo → el agente no necesita un caso especial para «ningún modelo contestó».
9. **Chaos testing:** en lugar de una excepción inventada, `chaos.py` construye **el tipo de excepción real de cada SDK** (`google.genai.ClientError` con 429, `groq.RateLimitError` envolviendo una respuesta HTTP 429, el `ConnectionError` de Ollama apagado) para que `to_provider_error`, los reintentos y los breakers recorran **el mismo camino de código** que en una caída real. CLI: `--kill gemini@3-4` (caído solo en los tickets 3-4), `--flaky groq` (falla una vez).
10. **Corte del carrusel:** el documento se interrumpe al empezar la sección 11 (el agente que triajea 6 tickets con historial compartido) y salta al CTA «Want Complete Version? … Exclusive Instagram Subscribers». Las secciones **12–17 del índice — incluidas «15. The Same Router in LiteLLM» y «16. Common Errors & Fixes» — NO están en el carrusel**: la promesa de la portada («plus the same thing rebuilt in LiteLLM») no se puede comprobar leyendo el post; solo ese índice la menciona.

### Actualización de la tabla «Aplicación al LAB»

| Patrón del post | Estado real en el lab | Veredicto |
|---|---|---|
| Provider abstraction (`complete(messages)`, un error único) | `tools/llm-router.sh` + `tools/decision_router.py` clasifican por tipo (batch/vision/check), pero **no** hay error único ni interfaz común | 🟡 parcial |
| Retry con backoff + jitter | **No existe** (grep `backoff|jitter|retry|num_retries` en `tools/*.py` → nada del enrutado) | ❌ hueco real |
| Circuit breaker (closed/open/half-open) | **No existe** | ❌ hueco real |
| Degradación elegante | Escala cuando falla el **verifier**, no cuando cae el proveedor; no hay respuesta degradada con formato fijo | 🟡 parcial |
| **Números concretos** | Antes: «faltaban los dos números». Ahora **medidos en el documento**: umbral 2 fallos, enfriamiento 30 s, 2 reintentos, base 0,5 s, cap 8 s, timeout 30 s | ✅ disponible |
| LiteLLM como capa | El lab llama a la API de DeepSeek y su proxy `:9911`; no usa LiteLLM como router | 🟡 referencia |

### Lo copiable tal cual (3 piezas pequeñas, sin dependencias nuevas)

1. **Lista cerrada de estados reintentables** (`{408, 429, 500, 502, 503, 504}`) y su complemento: fatal = no reintentar. Hoy el lab no clasifica por código HTTP.
2. **Regla «espera pedida por el servidor > cap ⇒ failover, no esperar»** — evita colgar un turno 41 s por una cabecera.
3. **Reloj inyectable** en el futuro cooldown del orquestador: sin él, cualquier prueba del enfriamiento o tarda 30 s reales o se hace con `sleep` (lo mismo con otro nombre).

Y un **aviso directo**: antes de implementar reintentos propios, **comprobar si algún cliente del lab reintenta por su cuenta** (el equivalente a `AsyncGroq(max_retries=0)`): apilar reintentos duplica esperas y **falsea las medidas de latencia/TTFB** que el lab ya registra en `aplicabilidad_ledger.jsonl` y en los informes de observabilidad.

### Límite honesto (lo que sigue sin saberse)

- La transcripción es **OCR de láminas**: las líneas de código largas aparecen cortadas por el ancho de la lámina y la indentación se pierde → **el código NO es copiable ni ejecutable tal cual**.
- **Las secciones 12–17 del documento NO están** en el carrusel: el corte es deliberado (es el anuncio de un PDF de pago).
- De la sección «The Same Router in LiteLLM» **no se puede decir nada por el post**; la verificación de la cabecera sigue siendo la hecha **contra la documentación oficial de LiteLLM**, no contra este tutorial.
- El valor aprovechable (láminas 1–19) es genuino, con código y números reales, pero **no está incompleto por accidente**.
