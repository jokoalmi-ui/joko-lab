---
title: "Análisis — \"Microagentes o agentes atómicos\" (Emowe, 30-ago-2026)"
type: research
---

# Análisis — "Microagentes o agentes atómicos" (Emowe, 30-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://youtu.be/RLwjsaaJOAM (Emowe, 30-ago, 8.469 views, 22:46)
**Método:** pipelina YT → metadatos + descripción + **especificación íntegra del autor** (gist público, ~340 líneas, leído completo vía raw). Subs es-orig NO descargables (yt-dlp sin JS runtime, 3er caso hoy — refuerza Invidious). Análisis sobre la especificación real, no sobre el vídeo.

## Qué es Atomic Agents (spec v1.0, Marcos Emowe, en producción desde ago-2026)

**Tesis central**: "Un agente no es un proceso en ejecución. Es un contrato en lenguaje natural + una tarjeta que le da permiso para trabajar." Agente = **archivo**, no proceso.

**Problema que resuelve**: los sistemas de agentes son conversaciones (sesión abierta, memoria cargada, tool catalog). Eso falla cuando quieres trabajo sin ti: (1) no se ejecuta si no hay sesión, (2) no es reproducible (depende de qué había cargado), (3) no se puede entregar a nadie (vive en la sintaxis de una herramienta).

**Piezas**:
| Pieza | Qué es |
|---|---|
| **Profile** | El contrato (nombre = oficio, sustantivo). Declara qué maneja, qué rechaza, garantías. NUNCA contiene know-how |
| **Skill** | El know-how (nombre = verbo). Montado por profiles o por el agente continuo. "Dos puertas, un cuerpo de conocimiento" |
| **Card** | Unidad de trabajo + permiso de producción. `.md` en el tablero. Su estado ES la carpeta donde vive |
| **Board (kanban)** | pending/ → in-progress/ → done/ → archive/. Integración en el tablero, no en código |
| **Dispatcher** | Runner determinista y ciego: empareja cards con profiles por comparación de strings, sin modelo, sin juicio semántico |
| **Vault** | Base de conocimiento que los agentes leen y escriben |

**Propiedades definitorias**: sin contexto ambiente (todo llega por PROFILE.md + card) · efímero (nace para una card, muere al cerrarla) · bajo contrato (la card pide, el profile decide).

**Jerarquía fractal**: worker (trabaja y cierra, nunca crea cards) → director (posee un flujo, distribuye y encadena) → CEO (director de directores). Rango en los profiles, no en la infraestructura. **Regla de oro: una card a la vez** — el director crea UN hijo, muere, y crea el siguiente cuando el anterior cierra. "Si el paso 1 no produce nada, los pasos 2-3 nunca existen."

**Doctrina de dos capas**: trabajo que necesita LLM → card programada; script determinista (recordatorios, backups, watchdogs) → OS scheduler. "Algo tiene que latir fuera del tablero para que el tablero funcione."

**Seguridad en capas**: origin validado · "la card pide, no ordena" (anti prompt-injection) · hook de bloqueo de credenciales · keys por entorno solo en dispatch · toolsets mínimos · código del dispatcher FUERA del vault.

**Integridad**: front matter inviolable · **fail loud** ("nada desaparece en silencio") · trazabilidad durante la ejecución (milestone tras admission) · **"every scar ends in a test"** · un paquete debe valerse por sí solo.

## 🔴 Aplicación al LAB — VALOR MEDIO-ALTO (validación fuerte + ideas para PRD Graph)

| Ángulo | Veredicto |
|---|---|
| **Skills = know-how (verbo+objeto)** | 🟢 **VALIDA el diseño del lab**: skills Hermes con SKILL.md (frontmatter + cuerpo) = el mismo patrón "skill = saber hacer, nombre = verbo" (transcribe-audio, capture-web... vs las del lab: verificar-research, crear-infografias) |
| **Model per task, sin hardcodear** | 🟢 Igual que llvm-router del lab (política de modelos por nodo, sin nombres en el perfil) — el lab ya lo hace |
| **"La card pide, no ordena" + origin validado** | 🟢 = gate de veracidad + least-privilege-lab + RULE-008 del lab (anti prompt-injection, fail-closed) |
| **Every scar ends in a test** | 🟢 = regression_guardian.py + tirith del lab |
| **Two-layer doctrine (determinista→OS, LLM→cards)** | 🟢 = crons no_agent (watchdogs deterministas) vs crons AGENT (investigaciones) — el lab YA lo implementa |
| **Director: "una card a la vez"** | 🟡 **IDEA DIRECTA para el PRD Graph (18-ago, pendiente F0)**: el PRD del lab propone coordinador→investigador→redactor→revisor; la spec añade el patrón anti-fallo: el coordinador NO debe lanzar los 3 subagentes en paralelo si el paso 1 puede producir nada — encadenar con señal (el hijo en done/ = señal para el siguiente). Mismo principio que el piloto recomendado (sin cambiar config) |
| **Wiring self-check del director** | 🟡 Idea valiosa: antes de morir en cada yield, el director re-verifica que la referencia al hijo coincide exactamente (el punto frágil es que un LLM escribe la ruta) — aplicable al PRD graph como gate |
| **Dispatcher ciego determinista** | ⚪ El lab NO tiene (usa delegate_task de Hermes con subagentes que heredan contexto). La spec argumenta "matching por strings destruye la indeterminación" — el lab mitiga con verificadores deterministas. No montar un kanban completo: sobredimensionado para el lab |
| **No es framework, es método** | 🟢 "Si la herramienta desaparece, conservas el método" — coincide con la filosofía del lab (skills como texto, sin depender de un vendor) |

**Conclusión**: VALOR MEDIO-ALTO — de los análisis de hoy, el más alineado con la arquitectura del lab. Sin implementar nada nuevo, pero con **2 ideas concretas que mejorarían el PRD Graph pendiente de tu OK (F0)**: (a) encadenar pasos por señal (una card a la vez) en vez de lanzar todo en paralelo; (b) self-check de rutas por el coordinador. Nota: análisis sobre la especificación íntegra del autor (más fiable que la transcripción del vídeo), sin inventar.

## ⚠️ CORRECCIÓN (01-sep-2026, detectada por el usuario): el KANBAN faltaba en el análisis

El vídeo de Emowe habla del **board/kanban como el estado de las cards** (pending → in-progress → done → archive) y el **dispatcher ciego** que empareja cards con profiles. El análisis original lo mencionó solo de pasada en la tabla. **Y el detalle que conecta TODO**: Hermes ya tiene un **kanban nativo integrado** que implementa exactamente ese diseño (verificado 01-sep con `hermes kanban --help`):

| Pieza de Emowe | Kanban nativo de Hermes (verificado) |
|---|---|
| Board (estado de cards) | ✅ `kanban.db` SQLite (existe desde 21-jul, VACÍO — nunca usado) |
| Cards con estado | ✅ tasks con estados, claims atómicos, dependencias entre tasks |
| Dispatcher ciego | ✅ dispatcher integrado en el gateway (`kanban.dispatch_in_gateway: true` por defecto) |
| Worker por card | ✅ workers con `HERMES_KANBAN_TASK` aislados |
| — | ➕ **`kanban swarm`**: grafo v1 (workers paralelos → verifier → synthesizer) — ES el PRD graph del lab ya implementado |
| — | ➕ `assign/reclaim/heartbeat/watch/stats/notify` — orquestación completa |

**RELEVANCIA PARA EL PRD GRAPH (pendiente desde 18-ago)**: el piloto F1 falló porque el investigador local no escribió el archivo de estado compartido (`investigacion.json` no existía → gate fail-closed). **El kanban nativo resuelve ese problema de raíz**: el estado de la card ES el tablero SQLite (no un archivo que el subagente debe recordar escribir), el dispatcher hace el wiring (no un coordinador que verifica rutas), y `swarm` ya tiene el patrón workers→verifier→synthesizer que el PRD quería construir a mano. **Acción recomendada**: evaluar el kanban nativo de Hermes como base del PRD graph en lugar de la delegación manual (evita reinventar el board). Pendiente de OK del usuario para probar `hermes kanban swarm` en un caso real.
