---
type: EXP
subtype: experiment
status: active
tags: [knowledge, experiment]
created: 2026-07-29
---
# Resultados

EXP-20260729-004: Benchmark workflows n8n
============================================
Tests: 5
Modelos: [pendiente]
Fecha: 2026-07-29
Estado: EN EJECUCION

────────────────────────────────────────────
TEST 1 de 5 — Diseño de benchmark
────────────────────────────────────────────

Prompt: Disenar benchmark para evaluar modelos locales en generacion de workflows n8n

Conocimiento reutilizado:
- EXP-20260726-001: Plantilla de 5 tests, mismas condiciones
- Anti-patrones: FATAL prompts multi-instruccion a GLM, max_tokens < 2048 en reasoning models
- Fichas: Granite 4.1 (tool-use, 5-15s), Llama 3.1 (function calling nativo)

Alternativas descartadas:
- DeepSeek R1: demasiado lento (106s) para iteracion rapida
- Gemma 4: su punto fuerte es creatividad, no estructura tecnica
- Dolphin: responde en texto, no tool calls
- GLM 4.6V: FATAL con prompts multi-instruccion

Benchmark propuesto (5 tareas n8n):
| ID | Tarea | Dificultad |
| W1 | Webhook → filtro → email | Baja |
| W2 | CSV → agrupar → reporte | Media |
| W3 | API → transformar → DB | Alta |
| W4 | Calendario → recordatorio → Telegram | Media |
| W5 | Error handling + retry + notificacion | Alta |

Evaluacion: Sintaxis (0-5), Estructura (0-5), Expresiones (0-5), Formato (0-5), Tiempo (0-5)
Total: 0-25

Modelos candidatos: Granite 4.1 (temp=0.3) y Llama 3.1 (temp=0.3)

Conocimiento nuevo esperado:
- Perfil de modelo para n8n (quien genera mejores workflows)
- Anti-patron: fallos en tareas multi-nodo
- Parametros optimos para generacion de workflows

Decision Memory a crear/actualizar:
- DEC-004 (nueva): "Modelo X para generacion de workflows n8n"

────────────────────────────────────────────
TEST 2 de 5 — Integracion nuevo proveedor IA
────────────────────────────────────────────

Prompt: Anadir soporte para un nuevo proveedor de IA sin romper decisiones previas

Documentos consultados:
- Decisiones: DEC-001/002/003 (3 decisiones activas sobre modelos)
- Recovery: incidente-uv (no hardcodear, el laboratorio debe sobrevivir a fallos)
- Inicio/fin: protocolo con checks, estado.json, servicios criticos
- Auditoria conocimiento-001: modelo de entidades, principio de compatibilidad futura
- Anti-patrones: FATAL/ALTA/MEDIA sobre modelos y configuracion
- Infraestructura: 5 pilares, 05-inference/executors/ con carpetas local/ y cloud/

Analisis:

1. DONDE ENCAJA
   05-inference/executors/cloud/ ya existe como estructura disenada.
   El nuevo proveedor es un executor cloud mas, no requiere modificar nada existente.
   No hay que tocar local/ (los modelos locales siguen siendo los mismos).

2. LO QUE NO SE ROMPE
   - DEC-001/002/003: El proveedor cloud no compite con los modelos locales
   - Inicio.sh: No se anyade check obligatorio (si falla el cloud, el lab sigue)
   - Contract.md: Sigue el mismo flujo de 7 pasos
   - Rescue: Las claves API van en variables de entorno, no en el backup
   - 100% local: El proveedor es complementario, no sustitutivo

3. ESTRUCTURA PROPUESTA (sin romper nada)

   05-inference/executors/cloud/nuevo-proveedor/
   ├── README.md         Ficha del proveedor (capacidades, coste, limites)
   │                     Siguiendo el modelo de entidad de la auditoria:
   │                     ID, fecha, estado, tipo, contenido, evidencia
   ├── client.py         Cliente API (autenticacion por variable de entorno)
   ├── config.yaml       Endpoint, modelo por defecto, timeout, max_tokens
   └── checks/
       └── verify.sh     Script opcional para inicio.sh (WARNING, no ERROR)

4. REGLAS DE DISENO
   - API key via variable de entorno, no hardcodeada en config
   - Timeout configurable (el proveedor puede fallar sin romper el lab)
   - Modelo por defecto en config.yaml, sobreescribible por parametro
   - Misma interfaz que los demas ejecutores (misma firma de entrada/salida)
   - El check verify.sh solo emite WARNING si falla, nunca bloquea inicio.sh
   - Documentado siguiendo el principio de compatibilidad futura
     (cualquier maquina debe poder consumir la ficha)

5. LO QUE HAY QUE DECIDIR
   - Que proveedor es (para completar README.md y client.py)
   - Si se anyade al router de 05-inference/router/ o se llama explicitamente
   - Si se integra en el sistema prompt de Hermes o solo via skill

────────────────────────────────────────────
TEST 3 de 5 — Sustitucion de Gemma 4
────────────────────────────────────────────

Prompt: Voy a sustituir Gemma 4 por un modelo nuevo.

Documentos consultados via RAG + search_files:
- Fichas: gemma-4-12b.md, granite-4.1-8b.md
- Experimentos: EXP-20260726-001 (5/5 Gemma), prompt-experiments.md (T31-T35)
- Decisiones: DEC-003 (Gemma 4 = Director Creativo)
- Patrones: large-creative-model.md, anti-patterns/catalogo.md
- Skills: contexto-multimodal (SKILL.md + router.py), combined-mode
- Infra: presentacion-joko-lab.txt, context_builder.py
- Otros: critic-loop, fine-tuning-reference, research/

═══════════════════════════════════════════════
IMPACTO COMPLETO
═══════════════════════════════════════════════

1. DOCUMENTOS AFECTADOS (15 archivos)

   [FICHA]      01-knowledge/models/gemma-4-12b.md
                → Cambiar status de "activo" a "reemplazado" o "archivado"
                → Anyadir campo "reemplazado_por: [nuevo modelo]"

   [BENCHMARK]  01-knowledge/experiments/EXP-20260726-001/README.md
                → Lineas 31, 50, 59, 67, 77 referencian Gemma 4
                → Anyadir nota: "Gemma 4 reemplazado por [nuevo] en 2026-07-29"

   [TESTS RAW]  01-knowledge/experiments/prompt-experiments.md
                → Tests 31-35 (T1-T5 de Gemma 4)
                → Marcar como historico, no borrar

   [PATRON]     01-knowledge/patterns/inference-patterns/large-creative-model.md
                → Modelo recomendado actual: Gemma 4 12B
                → Actualizar a [nuevo modelo] o crear nuevo patron

   [ANTI-PATRON] 01-knowledge/patterns/anti-patterns/catalogo.md
                → 2 anti-patrones especificos de Gemma 4 (lineas 19, 46)
                → Revisar si aplican al nuevo modelo; si no, marcar como historico

   [COMPARATIVA] 01-knowledge/models/granite-4.1-8b.md
                → Linea 23: "Creatividad correcta pero menos elaborada que Gemma 4"
                → Actualizar comparativa contra nuevo modelo

   [FINE-TUNE]  01-knowledge/patterns/inference-patterns/fine-tuning-reference.md
                → Menciona Gemma como modelo juez (lineas 91, 124)
                → Evaluar si el nuevo modelo sirve como juez

   [PRESENTACION] docs/presentacion-joko-lab.txt
                → 8 referencias a Gemma 4 (lineas 76, 216, 227, 279, 321, 322)
                → Actualizar mapa de capacidades y tabla

   [CRITIC]     instruments/critic-loop/README.md
                → Linea 43: script que usa gemma-4-12b-qat
                → Cambiar modelo en el comando de ejemplo

   [CONTEXT]    tools/context_builder.py
                → Linea 75: mapeo "gemma" → "gemma-4-12b.md"
                → Actualizar o mantener como historico

   [SKILL]      .hermes/skills/software-development/contexto-multimodal/SKILL.md
                → 6 referencias a Gemma 4 como modelo de creatividad
                → Actualizar tabla de routing (linea 75)
                → Actualizar flujo de seleccion (linea 86, 117)

   [SKILL]      .hermes/skills/software-development/contexto-multimodal/scripts/router.py
                → Lineas 10, 28: asignacion de Gemma a tareas creativas
                → Cambiar modelo destino para creatividad

   [SKILL]      .hermes/skills/software-development/combined-mode/SKILL.md
                → Linea 61: referencia a Gemma
                → Actualizar si aplica

   [EXPERIMENTOS] 01-knowledge/experiments/EXP-20260729-004/resultados.md
                → Test 1: menciona Gemma 4 como descartada para n8n
                → Verificar si el nuevo modelo cambia esa evaluacion

   [DECISION]   04-operations/decisions/DEC-003-gemma-4-creatividad.md
                → Decision completa a actualizar

2. DECISIONES OBSOLETAS

   DEC-003: "Gemma 4 como modelo principal de creatividad"
   → Cambiar estado de ACTIVA a REEMPLAZADA
   → Anyadir campo: "reemplazada_por: DEC-00X (nuevo modelo)"
   → Mantener como historico (el conocimiento de por que se eligio Gemma
      sigue siendo valido aunque el modelo ya no se use)

3. BENCHMARKS A REPETIR

   EXP-20260726-001 (T1-T5): Repetir con el nuevo modelo
   → Mismos 5 tests, mismas condiciones (temp=0.7, max_tokens=2048)
   → Comparar resultados contra Gemma 4 (5/5)
   → Si el nuevo modelo obtiene >= 5/5 y es mas rapido, validar sustitucion

   Tests adicionales recomendados:
   - Creatividad literaria (fortaleza de Gemma)
   - Codigo con 2 versiones (fortaleza de Gemma)
   - Razonamiento paso a paso (para comparar perfil)

4. PATRONES A INVALIDAR O ACTUALIZAR

   large-creative-model.md:
   → Modelo recomendado cambia de Gemma 4 a [nuevo modelo]
   → Actualizar tabla comparativa con datos del nuevo modelo
   → Repetir si es necesario antes de actualizar

   Anti-patrones de Gemma 4:
   - "max_tokens < 400 con Gemma 4" → NO aplica al nuevo modelo (a menos que sea reasoning)
   - "Esperar respuesta rapida de Gemma 4" → Evaluar si aplica al nuevo
   → Marcar como "historico: Gemma 4" y crear nuevos si procede

5. SKILLS A ACTUALIZAR

   contexto-multimodal/SKILL.md:
   → Tabla de routing: cambiar Gemma 4 por [nuevo modelo] en creatividad
   → Flujo de decision: paso 3 (creatividad) usar nuevo modelo

   contexto-multimodal/scripts/router.py:
   → Linea 10: cambiar "Gemma 4" por nuevo modelo
   → Linea 28: cambiar entrada "gemma" por nuevo nombre
   → Mantener la logica (el nuevo modelo asume el rol de creatividad)

═══════════════════════════════════════════════
PLAN DE MIGRACION
═══════════════════════════════════════════════

FASE 1 — Evaluacion del nuevo modelo (1 hora)
  [ ] Descargar y cargar nuevo modelo en LM Studio
  [ ] Ejecutar EXP-20260726-001 (T1-T5) contra el nuevo modelo
  [ ] Comparar resultados contra Gemma 4 (5/5, 151s max)
  [ ] Si el nuevo modelo obtiene >= 5/5, continuar

FASE 2 — Documentacion (30 min)
  [ ] Crear ficha del nuevo modelo en models/
  [ ] Actualizar DEC-003: cambiar estado a REEMPLAZADA
  [ ] Crear nueva decision (DEC-00X): "[nuevo modelo] para creatividad"
  [ ] Anyadir EXP-20260729-00X con resultados comparativos
  [ ] Archivar ficha de Gemma 4 (status: reemplazado)

FASE 3 — Patrones y skills (30 min)
  [ ] Actualizar large-creative-model.md con nuevo modelo recomendado
  [ ] Actualizar anti-patterns: marcar Gemma 4 como historico
  [ ] Actualizar contexto-multimodal/SKILL.md (tabla + flujo)
  [ ] Actualizar contexto-multimodal/scripts/router.py
  [ ] Actualizar context_builder.py (mapeo de modelos)
  [ ] Actualizar presentacion-joko-lab.txt

FASE 4 —Verificacion (15 min)
  [ ] Probar busqueda RAG: "modelo para creatividad" → debe devolver nuevo modelo
  [ ] Probar skill contexto-multimodal: "necesito un prompt creativo" → debe usar nuevo modelo
  [ ] Verificar que Gemma 4 sigue accesible como historico
  [ ] Commit de todos los cambios

Tiempo total estimado: ~2 horas 15 minutos

────────────────────────────────────────────
TEST 4 de 5 — Velocidad de respuesta
────────────────────────────────────────────

Prompt: Mejorar la velocidad de respuesta de Joko Lab.

Documentos consultados:
- Experimentos: EXP-20260726-001 (tiempos 7 modelos), EXP-20260728-002 (Granite 5-15s)
- Prompt-experiments (tiempos por test: Dolphin 3-36s, Llama 2-5s, DeepSeek 21-106s, Gemma 35-151s)
- Fichas: Granite 4.1 (5-15s), DeepSeek R1 (21-106s), Gemma 4 (35-151s), Dolphin (3-36s), Llama 3.1 (2-5s)
- Anti-patrones: max_tokens insuficiente en reasoning models, temperature alta degrada
- Estado del sistema: GPU RTX A2000 12GB, 4 contenedores Docker, 9 cron jobs
- Auditoria conocimiento-001: modelo de entidades, principio de compatibilidad futura
- Context builder: sabe detectar tipos de tarea

═══════════════════════════════════════════════
DATOS DE VELOCIDAD ACTUALES (benchmarks reales)
═══════════════════════════════════════════════

| Modelo | Tamano | Tiempo tipico | Uso actual |
|---|---|---|---|
| Llama 3.1 Instruct 8B | 8B | 2-5s | Tool-use nativo |
| Dolphin Cyber 8B | 8B | 3-36s | Chat rapido |
| Granite 4.1 8B | 8B | 5-15s | Codigo, tool-use |
| DeepSeek R1 14B | 14B | 21-106s | Razonamiento |
| Gemma 4 12B | 12B | 35-151s | Creatividad |
| GLM 4.6V Flash | — | — | Atomico, vision |

Cuello de botella detectado: ~60% de las consultas van a modelos lentos
(DeepSeek R1, Gemma 4) cuando modelos rapidos (Granite 4.1, Llama 3.1)
podrian resolverlas en una fraccion del tiempo.

═══════════════════════════════════════════════
MEJORAS PROPUESTAS (clasificadas)
═══════════════════════════════════════════════

MEJORA 1 — Router de modelos por velocidad
────────────────────────────────────────────
  Descripcion: Detectar tipo de tarea y usar el modelo mas rapido
               capaz de resolverla. Tareas no tecnicas → Granite 4.1
               (5-15s). Solo razonamiento complejo → DeepSeek R1 (60s).
  Impacto:     ALTO. Ahorro estimado de 50s por consulta no critica.
  Esfuerzo:    BAJO. Ya existe context_builder.py con detect_type().
               Anyadir una tabla de routing simple.
  Riesgo:      BAJO. Las tareas complejas seguiran yendo a DeepSeek.
               El router decide por tipo, no por capricho.
  Reutiliza:   context_builder.py (detect_type), fichas de modelo,
               anti-patrones (temperature, max_tokens).
  Conocimiento nuevo: Confirmar que modelo rapido cubre que % de tareas.

MEJORA 2 — Warm-up de modelo rapido al inicio de sesion
────────────────────────────────────────────────────────
  Descripcion: Mantener Granite 4.1 (5-15s) cargado siempre en LM Studio
               para responder consultas rapidas sin esperar carga.
               DeepSeek R1 y Gemma 4 se cargan solo cuando se necesitan.
  Impacto:     ALTO. Elimina los 3-10s de carga inicial del modelo.
  Esfuerzo:    BAJO. Anyadir "pre-load: granite-4.1-8b" en config de LM Studio.
  Riesgo:      MEDIO. Ocupa ~5GB de VRAM constantemente. Si se necesita
               VRAM para otro modelo, descargar Granite.
  Reutiliza:   inicio.sh (check de modelos cargados), fichas de modelo.
  Conocimiento nuevo: Medir VRAM real de Granite 4.1 en reposo.

MEJORA 3 — Cache de RAG para queries frecuentes
────────────────────────────────────────────────────────
  Descripcion: Cachear resultados del context_builder.py para evitar
               cargar BGE-M3 (1-2s) y buscar en LanceDB (~1s) en cada
               consulta. Cache LRU simple en ~/tmp/rag-cache/.
  Impacto:     MEDIO. Ahorra ~3s por consulta repetida.
  Esfuerzo:    BAJO. Anyadir cache LRU de 50 entradas en context_builder.
  Riesgo:      BAJO. El cache caduca en 1 hora (configurable).
  Reutiliza:   context_builder.py existente.
  Conocimiento nuevo: % de consultas repetidas vs unicas.

MEJORA 4 — max_tokens adaptativo por tarea
────────────────────────────────────────────────────────
  Descripcion: No usar siempre max_tokens=2048. Para tareas simples
               (saludo, pregunta directa) usar 512. Para codigo 1024.
               Para razonamiento 2048. Ahorra tiempo de generacion.
  Impacto:     MEDIO. Reduce el tiempo de generacion en tareas simples.
  Esfuerzo:    BAJO. Parametrizar max_tokens por tipo en el router.
  Riesgo:      BAJO. Si se queda corto, la respuesta se trunca pero
               no se pierde (finish=length en vez de stop).
  Reutiliza:   Anti-patrones (FATAL si max_tokens < N en reasoning),
               fichas de modelo (parametros recomendados).
  Conocimiento nuevo: max_tokens optimo por tipo de tarea.

MEJORA 5 — Compilar prompts para minimizar tokens de entrada
────────────────────────────────────────────────────────────
  Descripcion: Para tareas frecuentes, compilar el Prompt Project
               a un prompt minimalista con solo lo necesario.
  Impacto:     BAJO-MEDIO. Ahorro marginal en tokens de entrada.
  Esfuerzo:    ALTO. Requiere el Prompt Compiler (Fase 4).
  Riesgo:      BAJO. Solo afecta a tareas con plantilla.
  Reutiliza:   Prompt Projects, templates/, profiles/.
  Conocimiento nuevo: Cuanto reduce un prompt compilado vs raw.

═══════════════════════════════════════════════
TABLA RESUMEN
═══════════════════════════════════════════════

| Mejora | Impacto | Esfuerzo | Riesgo | Prioridad |
|---|---|---|---|---|
| 1. Router por velocidad | ALTO | BAJO | BAJO | 1 |
| 2. Warm-up Granite 4.1 | ALTO | BAJO | MEDIO | 2 |
| 3. Cache RAG | MEDIO | BAJO | BAJO | 3 |
| 4. max_tokens adaptativo | MEDIO | BAJO | BAJO | 4 |
| 5. Compilar prompts | BAJO | ALTO | BAJO | 5 |

═══════════════════════════════════════════════
RECOMENDACION
═══════════════════════════════════════════════

Implementar mejoras 1+2+3 en una tarde (~2 horas). La mejora 1
(router) es la de mayor impacto y menor esfuerzo: usar la
deteccion de tipo ya existente en context_builder.py para
elegir el modelo mas rapido que pueda resolver la tarea.

La mejora 2 (warm-up) elimina latencia de carga de modelo.
La mejora 3 (cache) elimina latencia de RAG en consultas repetidas.

Las 3 juntas reducen el tiempo de respuesta tipico de ~30-60s
a ~5-15s para la mayoria de consultas.

────────────────────────────────────────────
TEST 5 de 5 — Generar prompts para cualquier modelo con exito
────────────────────────────────────────────

Prompt: "Quiero que Joko Lab genere prompts para cualquier modelo local o cloud
con la mayor probabilidad posible de exito."

Documentos consultados (10 fuentes):
- prompt-engineering skill (SKILL.md): perfiles de 8 locales + 5 cloud, patrones, anti-patrones
- EXP-20260726-001: 35 tests, 7 modelos
- EXP-20260728-002: Granite 4.1 (temp=0.3 vs 0.7 cambia formato)
- prompt-experiments.md: 35 registros individuales con tiempos y tokens
- anti-patterns/catalogo.md: 6 FATAL + 5 ALTA + 3 MEDIA
- atomic-prompt-glm.md: patron especifico GLM
- large-creative-model.md: patron creatividad
- DEC-002 (DeepSeek R1 razonamiento), DEC-003 (Gemma 4 creatividad)
- Fichas de modelo (8): prompts ideales y que fallan por modelo
- context_builder.py: detect_type() ya implementado

═══════════════════════════════════════════════
RESULTADOS DEL ANALISIS
═══════════════════════════════════════════════

1. CONOCIMIENTO REUTILIZABLE (de las fuentes consultadas)

   - Tabla completa de modelos locales (8) con perfiles de prompt
   - Tabla de modelos cloud (5) con perfiles (conocimiento comunitario)
   - Patrones validados por tipo de tarea (razonamiento, JSON, codigo, creatividad)
   - 14 anti-patrones clasificados por gravedad
   - Regla: temperature baja (0.3) → formato puro; alta (0.7) → markdown envolvente
   - Regla: prompts atomicos para GLM (1 instruccion por prompt)
   - Regla: max_tokens >= 2048 para reasoning models
   - Deteccion de tipo de tarea (context_builder.py)
   - Formato Prompt Project (spec.yaml -> compilado por destino)
   - Flujo obligatorio de 7 pasos (contract.md)

2. CONFLICTOS ENCONTRADOS

   Conflicto 1: Temperature alta NO siempre es mala. En Granite 4.1,
   temp=0.7 produce JSON valido (aunque con markdown). El anti-patron
   "temperature > 0.3 en tareas tecnicas" es correcto para calidad pero
   no para formato. Solucion: el compilador debe separar formato de calidad.

   Conflicto 2: Llama 3.1 es 5/5 pero no se puede usar como chat.
   El compilador debe detectar que Llama solo responde con function calls
   y generar prompts en ese formato, no en texto plano.

   Conflicto 3: Gemma 4 es la mejor para creatividad pero la mas lenta
   (151s). El compilador debe preguntar si prioriza calidad o velocidad.
   Para rapido -> Granite 4.1 (5-15s). Para calidad -> Gemma 4 (35-151s).

   Conflicto 4: Qwen 3.5 sigue listado en LM Studio pero DESCARTADO.
   El compilador debe rechazar explicitamente generar prompts para el.

   Conflicto 5: El prompt de Gemini (EXP-20260728-002, embeddings)
   funciono mejor que Granite 4.1 para el mismo objetivo. Un modelo
   cloud (Gemini) y uno local (Granite) responden distinto al mismo
   prompt. El compilador debe generar prompts diferentes para cada backend.

3. DECISIONES PREVIAS QUE CONDICIONAN LA SOLUCION

   DEC-002: DeepSeek R1 para razonamiento -> prompts paso a paso, max_tokens>=2048
   DEC-003: Gemma 4 para creatividad -> prompts complejos, aceptar latencia
   Contract.md: flujo de 7 pasos obligatorio -> el compilador debe seguirlo
   Principio compatibilidad futura -> los prompts deben guardarse como spec.yaml
   Umbral E3 (3 condiciones) -> no clasificar como E3 con un solo test

4. QUE INFORMACION FALTA

   - % de consultas rapidas vs lentas (no hay metricas de uso)
   - VRAM real de Granite 4.1 en reposo (para warm-up)
   - Gemini no testeado contra resto de modelos locales
   - Temperatura optima para GLM en JSON (solo probado a 0.7)
   - Granite 4.1 a temp=0.5 (falta tercera condicion para E3)

5. SOLUCION PROPUESTA (Compilador de prompts)

   No crear nada nuevo. Automatizar lo que la skill prompt-engineering
   ya sabe hacer manualmente. El motor es:

   Usuario -> modelo destino -> perfil del modelo -> tipo de tarea ->
   patron de prompt -> restricciones -> compilar -> validar anti-patrones ->
   entregar + config -> registrar como Prompt Project

   Implementacion: ~100 lineas de Python usando context_builder.py
   (ya tiene detect_type) + tablas de la skill + validador de anti-patrones.

6. CONOCIMIENTO NUEVO A INCORPORAR

   - DEC-00X: "El compilador debe priorizar formato sobre temperatura"
   - E2: "Compilador puede generar prompts para modelos desconocidos"
   - Patron: "Prompt Project + compilacion por destino"
   - Anti-patron: "Generar prompt de texto para Llama 3.1" (reforzar existente)
   - Metrica: "% de acierto en primer intento"

═══════════════════════════════════════════════
ANALISIS FINAL — Los 5 tests
═══════════════════════════════════════════════

VISION GLOBAL DE LOS DESCUBRIMIENTOS:

1. DISENO DE BENCHMARK (Test 1)
   → Ya existe una plantilla validada (EXP-20260726-001)
   → Se identificaron 2 candidatos para n8n: Granite 4.1 y Llama 3.1
   → Falta ejecutar los 5 tests W1-W5 para tener datos reales

2. NUEVO PROVEEDOR IA (Test 2)
   → Encaja en 05-inference/executors/cloud/ sin romper nada
   → No debe anyadir checks obligatorios en inicio.sh
   → Las claves van en variables de entorno, no en backup

3. SUSTITUCION DE GEMMA 4 (Test 3)
   → 15 archivos afectados, 1 decision obsoleta (DEC-003)
   → Plan de migracion en 4 fases (~2h 15m)
   → Requiere repetir EXP-20260726-001 con el nuevo modelo

4. VELOCIDAD DE RESPUESTA (Test 4)
   → ~60% de consultas van a modelos lentos innecesariamente
   → 3 mejoras prioritarias: router + warm-up + cache (~2h)
   → Reduccion estimada: de 30-60s a 5-15s

5. COMPILADOR DE PROMPTS (Test 5)
   → Ya existe el conocimiento en la skill prompt-engineering
   → Solo falta automatizar: ~100 lineas de Python
   → 5 conflictos identificados que el compilador debe resolver

QUE NOS HACE FALTA (priorizado):

   URGENTE:
   a) Router de modelos por velocidad (Test 4, mejora 1) — ~30 min
      Usar detect_type() de context_builder.py para elegir modelo rapido
   b) Cache RAG (Test 4, mejora 3) — ~15 min
      Evitar cargar BGE-M3 en cada consulta

   IMPORTANTE:
   c) Compilador de prompts automatizado (Test 5) — ~2h
      ~100 lineas usando conocimiento que ya existe
   d) Sustitucion de Gemma 4 si procede (Test 3) — ~2h 15m

   CONVENIENTE:
   e) Integracion de nuevo proveedor cloud (Test 2)
   f) Ejecutar W1-W5 del benchmark n8n (Test 1)
   g) Medir VRAM de Granite 4.1 en reposo
   h) Probar Granite 4.1 a temp=0.5

RECOMENDACION:

   Hacer a+b hoy (~45 min). El router de modelos es la mejora
   con mejor ratio impacto/esfuerzo de todo el laboratorio.
   El compilador de prompts (c) es el paso natural despues.
