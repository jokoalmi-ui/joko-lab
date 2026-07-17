# Informe de Razonamiento sobre Modelos de IA en Joko Lab

**Fecha:** 2026-07-16
**Fuentes:** docs/arquitectura.md, docs/estado-real.md, docs/vision/modelos-como-roles.md,
docs/agentic-architecture.md, 30 decisiones registradas, skills ai-architecture + ai-router + combined-mode,
runtime/CONTRACT.md, datos en caliente del sistema.

---

## 1. Resumen ejecutivo

Joko Lab dispone de **4 proveedores de IA** (2 cloud, 2 locales) con un total de
**~12 modelos** disponibles entre todos ellos. El sistema actual ha pasado por
tres iteraciones arquitectónicas y se encuentra en una cuarta fase de
consolidación (Sprint 3.3 completado, Runtime operativo).

El modelo principal activo en este momento de escritura es **DeepSeek V4 Flash**
(config.yaml lo confirma), aunque el Runtime decidió **Gemini 3.1 Flash-Lite**
a las 10:30 por política horaria sin que la aplicación surtiera efecto real
(ver §6.1 para este hallazgo activo).

---

## 2. Inventario completo de modelos disponibles

### 2.1 Cloud — Proveedores externos

| Proveedor | Modelo | Coste input | Coste output | Consulta típica | Estado |
|-----------|--------|:-----------:|:------------:|:---------------:|:------:|
| DeepSeek | deepseek-v4-flash | $0.077/M | $0.154/M | ~$0.00023 | ✅ Principal activo |
| Gemini | gemini-2.5-pro | $0.300/M | $2.500/M | ~$0.00305 | ✅ Autenticado |
| Gemini | gemini-3.1-flash-lite | $0.100/M | $0.400/M | ~$0.00050 | ✅ Autenticado |
| Gemini | gemini-3.5-flash | — | — | — | ✅ Disponible |
| Gemini | deep-research-max-preview | — | — | — | ✅ Disponible |
| Zhipu AI | GLM-4.7-Flash | **$0.000** (free) | **$0.000** (free) | $0.00000 | ⚠️ Evaluado, no integrado |

**Total modelos cloud disponibles:** 39+ en Gemini, 2 en DeepSeek.
**Total modelos cloud integrados en el sistema:** 5 (DeepSeek 1 + Gemini 4).

### 2.2 Local — Ollama

| Modelo | VRAM | Contexto | Tool-calling | Estado |
|--------|:----:|:--------:|:------------:|:------:|
| llama31-8b-64k | ~7 GB | 64K | ✅ Sí | ✅ Operativo |
| ~~llama3.1:8b~~ | — | 8K | — | ❌ Sustituido por 64k |
| ~~qwen2.5:7b~~ | — | — | — | ❌ Eliminado del código 2026-07-14 |

### 2.3 Local — LM Studio

| Modelo | Tamaño | Contexto | Tool-use | Visión | Estado |
|--------|:------:|:--------:|:--------:|:------:|:------:|
| glm-4.6v-flash | 7.95 GB | 131K | ✅ | ✅ | ✅ Operativo |
| google/gemma-4-12b | 7.56 GB | 262K | ✅ | ✅ | ✅ Operativo |
| google/gemma-4-12b-qat | — | — | ✅ | ✅ | ✅ Operativo |
| google/gemma-4-e4b | — | — | — | — | ✅ Descargado |
| qwen/qwen3.5-9b | 6.55 GB | 262K | ✅ | ✅ | ✅ Operativo |
| text-embedding-nomic-embed-text-v1.5 | — | — | Embeddings | — | ✅ Descargado |

**Total modelos locales:** 8 (2 Ollama + 6 LM Studio). **Total 6 funcionales** (Ollama
2 + LM Studio 3 benchmarkeados + embeddings).

---

## 3. Evolución del razonamiento arquitectónico (cronología)

### Fase 0 — Julio 2026 inicial: "Un solo modelo"

Hermes usaba un único modelo en config.yaml. Se cambiaba manualmente.

### Fase 1 — 2026-07-05 a 2026-07-08: "Router horario"

**Hipótesis:** DeepSeek tiene una franja cara (03:00-12:00). Conviene
cambiar a Gemini o local en esa franja para ahorrar.

Se implementó:
- Script `router-cron.sh` con cron a las 3:00 y 12:00
- `model-router.sh` sourceado desde `.bashrc`
- `/tmp/current-provider.txt` como estado compartido

**Resultado:** Falló. El cron escribía en un txt que nadie leía.
El `&&` encadenado impedía logs de error. Las URLs se desincronizaban
(DeepSeek llamando a Gemini endpoint y viceversa).

### Fase 2 — 2026-07-09 a 2026-07-10: "Roles como modelos"

**Decisión** (`docs/vision/modelos-como-roles.md`):
Los modelos dejan de ser proveedores. Son **roles**:

| Rol | Modelo | Disponibilidad | Coste |
|-----|--------|:-------------:|:-----:|
| Arquitecto residente | Mistral Nemo (Ollama) | 24/7 | Gratuito |
| Especialista alto razonamiento | DeepSeek v4-flash | Franja normal | Bajo |
| Especialista apoyo | Gemini 3.1 Flash Lite | Franja cara | Bajo |

**Flujo:** ¿Puede resolverlo Mistral? → local. ¿No? → según hora: Gemini o DeepSeek.

**Problema:** Mistral Nemo (12.2B) era demasiado pesado para la RTX A2000
(12 GB VRAM). Ocupaba ~11.9 GB dejando solo ~300 MB libres. Velocidad ~28 tok/s
por swapping. Se sustituyó por `llama31-8b-64k` (~7 GB, más rápido).

### Fase 3 — 2026-07-10: "Arquitectura híbrida Cloud-Local v2"

**Decisión** (`2026-07-10-arquitectura-hibrida-cloud-local.md`):
Se invierte el paradigma:

| Rol | Tecnología | Función |
|-----|-----------|---------|
| Orquestador (Director) | DeepSeek/Gemini (Cloud) | Planifica, razona, decide herramientas |
| Ejecutor (Worker) | Ollama/llama31 (Local) | Tareas mecánicas bajo supervisión |

**Mecanismo:** DeepSeek como modelo principal. `delegate_task` para tareas
mecánicas al local. `fallback_providers` en config.yaml para resiliencia.

### Fase 4 — 2026-07-14: "El fin del router horario"

**Descubrimiento crítico:** Los precios oficiales de DeepSeek V4 Flash son
**$0.077/$0.154 por M tokens** — no $0.14/$0.28 como se asumía originalmente.
Y Gemini 2.5 Flash cuesta **$0.300/$2.500** (13x más caro en output).

| Modelo | Input ($/M) | Output ($/M) | Coste consulta típica |
|--------|:----------:|:-----------:|:--------------------:|
| DeepSeek V4 Flash | **$0.077** | **$0.154** | **~$0.00023** |
| Gemini 2.5 Flash-Lite | $0.100 | $0.400 | ~$0.00050 |
| Gemini 2.5 Flash | $0.300 | $2.500 | ~$0.00305 |
| Ollama local | $0.000 | $0.000 | $0.00000 |

**DeepSeek es 13x más barato que Gemini 2.5 Flash y 2.2x más barato que
Gemini Flash-Lite.** No existe "franja cara" en DeepSeek. La política
horaria queda obsoleta por datos reales de precio.

**Conclusión:** El único motivo para usar local es **privacidad**, no coste.
DeepSeek es el cloud por defecto permanente.

### Fase 5 — 2026-07-14 a actualidad: "Runtime consolidado"

Sprint 3.3 completado. El Runtime es un motor de decisión puro que:

1. **State Manager** observa el laboratorio cada 60s, escribe state.json
2. **Decision Engine** lee state.json + 6 políticas YAML y decide proveedor
3. **Runtime.resolve()** es la API pública (9 campos del contrato)
4. **apply-decision.sh** es el adaptador que ejecuta `hermes config set`

Políticas activas (por orden de precedencia):

| Prioridad | Política | Función |
|:---------:|----------|---------|
| 1 | privacidad.yaml | Datos sensibles → forzar Ollama |
| 2 | disponibilidad.yaml | Fallback si cloud caído |
| 3 | costes.yaml | Saldo mínimo antes de cloud |
| 4 | horario.yaml | Franja horaria |
| 5 | preferencias.yaml | Fallback por defecto |

---

## 4. Árbol de decisión actual (válido julio 2026)

```
                    ┌─────────────────────┐
                    │    Tarea entrante    │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │  ¿Datos sensibles   │
                    │  o privacidad?      │
                    └──────────┬──────────┘
                    ┌──────────┴──────────┐
                    │ Sí                  │ No
                    ▼                     ▼
              Ollama llama31         ┌──────────┐
              (local, gratuito)      │DeepSeek  │
                                     │V4 Flash  │
                                     │(cloud,   │
                                     │~$0.00023)│
                                     └──────────┘
                               ┌──────────┼──────────┐
                               │          │          │
                               ▼          ▼          ▼
                          ¿Multimodal?  ¿Complejo?  ¿Mecánico?
                               │          │          │
                               ▼          ▼          ▼
                         LM Studio    DeepSeek   delegate_task
                         (VLM local)  (directo)  → Ollama llama31
```

**Reglas del árbol:**

- **Privacidad** es la única regla que fuerza local (política #1)
- **DeepSeek es el cloud por defecto permanente** — no hay franja cara
- **LM Studio** solo cuando se necesita visión local (y está activo)
- **Gemini** solo si DeepSeek está caído (fallback), o si se necesita
  un modelo específico que solo Gemini tiene
- **GLM-4.7-Flash** (Zhipu) está evaluado como potencial suplente de Gemini
  pero no integrado. Pendiente de prueba de calidad real

---

## 5. Evaluación de modelos individuales

### 5.1 DeepSeek V4 Flash — Cloud principal

| Dimensión | Valoración |
|-----------|:----------:|
| Coste | ✅ Más barato de todos los cloud ($0.00023/consulta) |
| Razonamiento | ✅ Superior (benchmark verificado) |
| Disponibilidad | ✅ Con validación pre-aplicación (key + endpoint + modelo) |
| Privacidad | ❌ Datos salen del laboratorio |
| Tool-calling | ✅ Excelente |

**Rol:** Modelo principal. Orquestador Cloud. Planifica, razona, decide.

### 5.2 Gemini — Cloud secundario

| Dimensión | Valoración |
|-----------|:----------:|
| Coste | ❌ 2.2x a 13x más caro que DeepSeek |
| Razonamiento | ✅ Similar a DeepSeek |
| Disponibilidad | ✅ Autenticado vía API key en secrets/ |
| Multimodal | ✅ Ventaja: nativo, no necesita LM Studio |

**Rol:** Fallback si DeepSeek cae. Multimodal si LM Studio no está activo.

### 5.3 GLM-4.7-Flash (Zhipu) — Evaluado, no integrado

| Dimensión | Valoración |
|-----------|:----------:|
| Coste | ✅ Gratuito (tier free) |
| Razonamiento | ⚠️ Tool-calling/agentes por debajo de DeepSeek |
| Sin comparativa directa | ❌ No existe benchmark GLM vs Gemini Flash-Lite |
| Ahorro real | ❌ Marginal (~$0.04/día) frente a DeepSeek actual |

**Decisión:** No integrado. Pendiente de prueba de calidad real con tareas
del laboratorio. El ahorro marginal no justifica la complejidad de integración
sin validación previa.

### 5.4 Ollama — Local principal

| Dimensión | Valoración |
|-----------|:----------:|
| Coste | ✅ Gratuito |
| Privacidad | ✅ Todo local |
| Razonamiento | ❌ Significativamente peor que DeepSeek (benchmark: 3.0 vs 4.7) |
| Velocidad | ✅ Responde en localhost, sin latencia de red |
| Modelo activo | llama31-8b-64k (~7 GB VRAM, 64K contexto, tool-calling ✅) |

**Rol:** Arquitecto residente. Privacidad. Tareas mecánicas vía delegate_task.
Fallback si DeepSeek cae.

### 5.5 LM Studio — VLM local

| Dimensión | Valoración |
|-----------|:----------:|
| Modelos | 6 descargados (35.62 GB), 3 benchmarkeados |
| Visión | ✅ glm-4.6v-flash, gemma-4-12b, qwen3.5-9b |
| API Server | ⚠️ Actualmente no activo (según estado-real.md) |
| Rendimiento | ✅ Headless vía `lms` CLI, systemd service |

**Rol:** VLM local para procesamiento multimodal. Se activa bajo demanda.

---

## 6. Hallazgos activos (no resueltos)

### 6.1 Desincronización Runtime → config.yaml (ALTA)

**Verificado en caliente hoy:**

```
ultima-decision.json:  {
  "provider": "gemini",
  "model": "gemini-3.1-flash-lite",
  "reason": "Horario: 03:00-12:00, ahora 10:29"
}

config.yaml:  provider: deepseek, default: deepseek-v4-flash
```

`apply-decision.sh` ejecutó a las 10:30:01 y logueó
`"Cambiando: / → gemini/gemini-3.1-flash-lite"` pero **config.yaml no cambió**.

El campo OLD_PROVIDER aparece vacío (`/`), que es un patrón preexistente desde
el 13 de julio. Esto sugiere que `hermes config show model.provider` devuelve
vacío en el contexto del cron, o que el `hermes config set` falla silenciosamente
en ejecución desatendida.

**Impacto:** Hermes usa DeepSeek aunque el Runtime ha decidido Gemini.
Si DeepSeek cayera, Hermes no tendría el fallback automático configurado.

### 6.2 base_url residual (MEDIA — corregida en código, no verificada en producción)

El fix `ec56982` añadió un mapa provider→base_url en apply-decision.sh.
Sin embargo, la desincronización del punto anterior impide verificar si
el fix funciona correctamente en producción.

### 6.3 Políticas huérfanas (BAJA)

- `gpu.yaml` — existe pero el DE no la consume. Para umbrales de VRAM.
- `niveles.yaml` — existe pero el DE no la consume. Para niveles de verificación.

### 6.4 decision-ledger.json no implementado (BAJA — aceptado)

Se evaluó crear un ledger agregado en Sprint 3.3. Se descartó porque
`decision.log` (JSON por línea) ya cubre el historial. No hay consumidor
real que justifique la implementación.

---

## 7. Comparativa benchmark (plan de pruebas)

Benchmark diseñado en `docs/benchmark/plan-pruebas-local-vs-online.md`:

| Tarea | Local (Ollama) | Online (DeepSeek) | Combinado |
|-------|:--------------:|:-----------------:|:---------:|
| 1. Explicar Dockerfile | 4.0 | 4.5 | 4.5 |
| 2. Diagnosticar log n8n | 3.0 | 5.0 | 5.0 |
| 3. Diseñar workflow | 2.5 | 4.5 | 4.5 |
| 4. Optimizar script bash | 3.5 | 5.0 | 5.0 |
| 5. Regex precisa | 2.0 | 4.5 | 4.5 |
| **Media ponderada** | **3.0** | **4.7** | **4.7** |
| **Coste estimado** | **$0.00** | **~$0.05** | **~$0.02** |

**Conclusión del benchmark:** DeepSeek gana 5/5 tareas en calidad. El modo
combinado gana 4/5 pero iguala en media. Local (Ollama) solo es competitivo
en tareas de análisis simple.

---

## 8. Costes reales y proyección

### Coste por consulta típica (~2.000 input + 500 output tokens)

| Proveedor | Consulta | 100 consultas/día | 30 días |
|-----------|:--------:|:-----------------:|:-------:|
| DeepSeek V4 Flash | $0.00023 | $0.023 | $0.69 |
| Gemini 3.1 Flash-Lite | $0.00050 | $0.050 | $1.50 |
| Gemini 2.5 Flash | $0.00305 | $0.305 | $9.15 |
| Ollama local | $0.00000 | $0.000 | $0.00 |

**Estimación realista mensual:** ~$0.70 con DeepSeek como principal,
más ~$0.25 de Gemini como fallback ocasional = **~$1/mes**.

### Ahorro de GLM-4.7-Flash (si se integrara)

Sustituir Gemini como fallback por GLM gratuito ahorraría ~$0.04/día =
**~$1.20/mes**. El ahorro es real pero marginal.

---

## 9. Línea de evolución futura

### Corto plazo (Sprint 3.4)

- Corregir la desincronización Runtime ↔ config.yaml (§6.1)
- Sistema de observabilidad de costes reales (ya implementado en Sprint 3.4)
- Verificar que base_url se actualiza correctamente en producción

### Medio plazo

- **GPU Scheduler:** Arbitrar VRAM (12 GB RTX A2000) descargando modelos
  de Ollama/LM Studio antes de levantar modelos pesados
- **Semantic Router:** Enrutamiento dinámico multicriterio en lugar de
  políticas fijas
- **Métricas acumuladas:** TTFT, tokens/minuto, latencia, coste acumulado
  por proveedor (diseñado en CONTRACT.md §12)

### Largo plazo

- **Prueba de calidad real de GLM-4.7-Flash** y posible integración como
  suplente gratuito de Gemini
- **Verificador (Verifier):** Sistema de validación de respuestas (contrato
  hecho en niveles.yaml, sin implementar)
- **Director Estratégico** (Fase 2): el Decision Engine deriva tareas
  complejas a un planificador LLM solo cuando es necesario (3+ pasos,
  arquitectura, investigación)

---

## 10. Reglas inmutables del razonamiento actual

1. **DeepSeek es el cloud por defecto permanente.** No existe franja cara.
   Verificado con precios oficiales 2026-07-14.

2. **Privacidad es el único motivo para forzar local.** El coste de DeepSeek
   es tan bajo (~$0.00023/consulta) que el ahorro local no es relevante.

3. **El Runtime decide, no la configuración.** config.yaml es un artefacto
   de aplicación. state.json + policies/*.yaml son la fuente de verdad.

4. **Validación pre-aplicación obligatoria.** apply-decision.sh verifica
   contra la API real antes de tocar config.yaml. Si falla, no cambia nada.

5. **Gemini solo como fallback.** DeepSeek caído, o necesidad de un modelo
   que solo Gemini ofrece (multimodal nativo si LM Studio no está activo).

6. **GLM-4.7-Flash requiere prueba manual antes de integrar.** Sin benchmark
   público contra Gemini Flash-Lite, no se decide por especulación.

7. **LM Studio bajo demanda.** El API Server no está siempre activo. Se
   activa cuando se necesita visión local.

8. **El modelo local no decide.** Solo ejecuta bajo supervisión vía
   `delegate_task`. No tiene autoridad para planificar.
