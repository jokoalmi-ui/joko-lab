---
title: "Análisis — Joaquín Ruiz: 4 arquitecturas de equipos de agentes medidas (13-nov-2026)"
type: research
---

# Análisis — Joaquín Ruiz: 4 arquitecturas de equipos de agentes medidas (13-nov-2026)

**VERACIDAD:** [NO VERIFICADO] — corregido a mano tras el post-procesador, que etiqueta por flujo y había puesto [VERIFICADO]. Las cifras vienen del audio del autor sin artefacto publicado (ver «VERIFICACIÓN REAL»).
**CALIDAD:** pendiente (el juez requiere LM Studio con modelo cargado)

**Fuente:** https://youtu.be/xFGolsBNMZs — «4 equipos de agentes de IA pasan los tests. Solo UNO dejó la API igual» (canal Joaquín Ruiz, publicado 2026-11-13, registrado por el cron `vigilar-canales-yt` el 13-11-2026 17:23).

**Método:** transcripción automática ES/EN completa (`fetch_transcript.py --text-only --timestamps`), 12.162 caracteres, leída íntegra. Todas las cifras proceden del AUDIO del autor: no hay repositorio, capturas de la suite ni banco de casos publicado en el vídeo. Los nombres propios (Sonnet 5.5, TaskFlow, Médula, Gas Town) vienen dictados por voz y pueden estar deformados por el ASR.

## Qué mide el vídeo

Mismo modelo (Claude Sonnet 5.5, tal como suena en el audio), misma versión de Claude Code, misma cuenta de Anthropic, `agent teams` desactivados en todas las corridas, y un directorio home limpio por ejecución. Dos pruebas × cuatro arquitecturas, con la misma API de partida: **TaskFlow**, un servicio Flask con tests.

Arquitecturas comparadas:

1. **Freelance** — un solo agente, sin reparto.
2. **Cadena** — un agente especifica, otro construye, tres revisores revisan y aprueban.
3. **Capataz** — un agente jefe que crea subagentes en copias aisladas del repositorio (worktrees) y consolida.
4. **Enjambre** — sin jefe; los agentes se coordinan por turnos con un fichero de candado y push.

## Prueba 1 — cuatro tickets pequeños

- Freelance: 12/12 tests, ~1:30 min, **$0,25**
- Cadena: 12/12, ~4 min, **$1,00**
- Capataz: 12/12, ~1:30 min, **$0,55**
- Enjambre: 12/12, ~1:10 min, **$0,67**

## Prueba 2 — migrar Flask a FastAPI, con trampas deliberadas

Trampas incluidas a propósito: 422 frente a 400, redirecciones, y una fixture instalada adrede para que la suite no sea trivial.

- Freelance: 12/12, 5:30 min, **$0,96**
- Cadena: 12/12 en la suite oculta, pero **se quedó sin rondas y nunca llegó a aprobarse**, 17 min, **$4,65**
- Capataz: 12/12, menos de 4 min, **$0,97**
- Enjambre: 12/12, ~3:15 min, **$1,17**

Multiplicador de coste entre la prueba fácil y la difícil: freelance ×3 o más, cadena ×4 o más, capataz y enjambre ×1,8 aproximadamente.

## El dato que rompe la intuición: los 12 casos raros

Los cuatro equipos pasan la suite. Se añaden entonces doce casos raros (HEAD, barra de más, un carácter en árabe en la URL) y se comparan contra la aplicación Flask original:

- **Cadena: 12/12 — idéntico al comportamiento original.**
- Freelance: 5/12.
- Capataz: 2/12.
- Enjambre: 0/12.

Es decir: la arquitectura con más revisores fue la única que preservó la interfaz. Pasar los tests no equivale a no cambiarla.

## Fallo sistémico observado

En capataz y enjambre hay un defecto que el autor califica de grave: dos aplicaciones quedan vivas en el mismo proceso y **la primera escribe en la base de datos de la segunda**. El agente jefe del capataz dejó constancia escrita del riesgo durante la ejecución y aun así ocurrió. El aislamiento por worktree no aísla los recursos compartidos del proceso.

## Conclusión del autor (paráfrasis fiel)

- Reparto de agentes solo cuando el trabajo es divisible y los trozos no se pisan.
- Un solo agente para lo pequeño: repartir cuesta más dinero y no mejora el resultado.
- Cadena de revisores cuando el requisito es que el comportamiento quede idéntico, asumiendo un coste de alrededor de cinco veces.
- Frase de cierre: los agentes no piensan por ti en lo que no has escrito.

## Qué aporta al laboratorio

1. **Regla operativa para `delegate_task`:** un solo agente para tareas pequeñas; reparto solo si los trozos no comparten ficheros, puertos ni bases de datos; revisores con contexto propio solo cuando el objetivo es preservar comportamiento existente.
2. **Riesgo concreto y medido:** subagentes en paralelo que comparten un recurso escriben donde no deben. En este lab los recursos compartidos son `state.db`, el índice `.lancedb`, los puertos 1234/5678/5000 y las bases de `perfume-ia` y `empleo-seguimiento`. El aislamiento de directorio no protege ninguno de ellos.
3. **Coste del reparto mal usado:** en la prueba pequeña, cadena y enjambre multiplican el gasto sin mejorar el 12/12.

## Lo que este análisis NO es

- **No es una medición verificada.** Las cifras son del audio del autor, sin artefacto publicado que las respalde. Sirven como hipótesis ordinal (qué arquitectura se comportó mejor en qué caso), no como cifras citables.
- **No es una comparación de modelos.** Un único modelo, un único proveedor, una versión concreta.
- **No cubre** el resto de los siete vídeos del informe del 13-11: cinco quedaron triados sin transcribir (noticias de mercado, opinión de ingeniería sin medición, herramienta de avatar en la nube) y el de IBM Technology («Why AI Agents Need RAG + Observability») se leyó pero no genera ficha propia: es divulgación conceptual, sin cifras, que confirma un patrón ya usado en el lab (separar evidencia, impacto y siguientes pasos, y no confundir inferencia con causa).

## VERIFICACIÓN REAL

- Transcripción obtenida y leída completa (12.162 caracteres) — verificado.
- Canal, título y fecha — verificado contra la salida del cron `c84f8d890630` del 13-11-2026 17:23.
- Cifras de coste, duración y aciertos — **NO verificadas**: no existe repositorio ni captura publicada; `yt-dlp` no está instalado en este host, por lo que ni siquiera se pudo contrastar título o duración por metadatos de la API de YouTube en esta sesión.
- Búsqueda de fuente escrita independiente: no realizada en esta sesión. Si se quiere citar fuera del lab, hay que contrastar antes con el autor o con la suite publicada.
