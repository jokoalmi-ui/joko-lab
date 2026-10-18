---
title: "Análisis — Ventana de contexto: por qué llenarla sale mal (Gentleman Programming, 16-sep-2026)"
type: research
---

# Análisis — Ventana de contexto: por qué llenarla sale mal (Gentleman Programming, 16-sep-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://youtu.be/RE_Sd5BxzDo (Gentleman Programming, subido 16-09-2026, 37:33 min, 1.470 vistas al analizarlo)
**Método:** auto-subtítulos `es-orig` con yt-dlp (362.977 B / 8.296 líneas) → limpieza VTT + dedup de n-gramas → 39.202 caracteres (234 párrafos) leídos íntegros; más la **descripción escrita del propio autor**, que trae el índice con timestamps y sirve de contraste cuando el ASR deforma una cifra. No se ha visto el vídeo ni el audio.

**Qué es:** capítulo 3 del curso gratuito del canal ("from talking to agent"). Es un DIRECTO con chat, no un tutorial editado: hay preguntas de la audiencia, publicidad propia (gentle-ai, Engram, "el cursito del gentleman") y 20 h de directo acumuladas según el propio autor. Tema: la ventana de contexto como presupuesto y la diferencia entre memoria y contexto.

## Veredicto

**VALOR: MEDIO-ALTO como marco conceptual y como contabilidad de costes. BAJO como técnica nueva.** No introduce ninguna técnica que el lab no tenga ya montada, pero aporta (a) un criterio explícito de PODA de memoria que el lab no tiene escrito y (b) cifras cuantificadas de lo que cuesta el contexto fijo por request. Se separa en las tres cajas que exige la regla del lab:

### 1) NUEVO / APLICABLE

- **MCP y herramientas cargadas siempre: activarlas sólo cuando se usan.** Un espectador pregunta literalmente "¿hay forma de que sólo se cargue el MCP cuando se vaya a utilizar, porque muchas veces no se van a usar, pero con la primera llamada se carga y sube 35k el contexto?" y el autor responde que sí: desactivarlo y activarlo cuando haga falta. **El lab tiene 3 MCP en producción (lab-db, lancedb, animation-server) cuyas definiciones de herramientas viajan en cada request del perfil `default`**; el coste en tokens de esos 3 MCP no está medido. La lección no es "cargar el MCP bajo demanda" (concepto conocido) sino la **contabilidad**: las definiciones de herramientas son el bloque más caro del contexto fijo y hay que medirlo, no intuirlo. Candidato claro a medición (ver Futuribles F1).
- **Criterio de PODA de memoria escrito: qué NO va.** El autor lista lo que SÍ va a la memoria (decisiones de arquitectura **y su motivo**, convenciones del equipo, caminos que se probaron y fallaron, restricciones del proyecto, cómo se llaman las cosas en tu dominio) y lo que NO (resultados de una corrida de test, estado temporal, número de línea de un archivo, "lo que hoy importa mañana no"). El lab tiene la regla de poda pero centrada en "no logs / no narración de tareas"; **añadir el motivo a las decisiones y vetar explícitamente el estado temporal es un criterio más afilado y reutilizable**. Encaja con el problema real del lab: MEMORY.md al tope del presupuesto.
- **"Una memoria mal hecha es peor que no tener memoria".** El argumento: con memoria inflada crees que el modelo sabe algo (porque se lo cargaste), no te explicas, y entonces **alucina sobre una base que tú pagaste**. Es la justificación económica y de riesgo de la poda, no sólo estética.

### 2) MEJORA (ya lo hacemos; admite un ajuste)

- **La compactación/resumen tiene coste propio y degradación acumulativa.** El autor insiste en que cada compactación pierde detalles y sobre todo **el motivo** de las decisiones ("está muy bonito, se acuerda de que hubo una decisión, pero no entiende el por qué"), y que truncar es la peor de las tres estrategias (peor que resumir) porque corta por donde están las instrucciones. El lab ya usa compactación (compression 0.4, MEP-001 / memoria episódica antes de perder contexto): el vídeo apunta al mismo diseño, pero añade un matiz útil — **la memoria debería escribirse ANTES de compactar y releerse al salir de la compactación** (es lo que el autor hace con Engram: guardar decisiones y observaciones y recuperarlas tras el resumen). Es exactamente lo que hace MEP-001; queda como confirmación con el matiz de "releer al salir", no sólo "escribir antes".
- **Índice en vez de prompt completo (SDD).** Propone no cargar el system prompt de una metodología entera sino un índice ("cuando tengas que usar SDD, esto tienes que cargar") y cita Open Spec. El lab ya funciona así (skills que se cargan con `skill_view` bajo demanda, `.skills_prompt_snapshot.json` con sólo nombre+descripción al frente). Sin acción; refuerza la decisión de recortar 144/164 skills del perfil `investigador`.

### 3) CONFIRMA (sin acción)

- **Fijo adelante, variable atrás** — con la demo de caché: poner la fecha/hora/ID de sesión delante invalida el prefijo y se paga entero; ponerlo detrás deja **el 99 % del prompt cacheado** entre peticiones. Es la regla que el lab ya aplica (SOUL.md y prompt de sistema estables al frente, historial y datos volátiles detrás).
- **Buscar barato, profundizar caro** = RAG superficial → candidatos → leer sólo 3 de 400 archivos. Es el patrón `agentic-rag` del lab, literal.
- **"Llenar el contexto no es una estrategia, es una remediación"**: pegar todo el repo/documentación esperando que el modelo encuentre lo importante es "tercerizar el criterio".
- **Pérdida en el medio**: lo del principio y lo del final se usan bien; lo del medio se paga y baja de fiabilidad (y se degrada acumulativamente con cada compactación en un sistema 24/7).
- **Memoria ≠ contexto**: contexto = mesa efímera; RAG = bibliotecario (conocimiento externo: docs, manuales, papers, **skills**); memoria = el cuadernito que construyes tú desde fuera. La frase del vídeo que resume su tesis: "la memoria hay que construirla desde afuera, sí o sí".

## Contenido con cifras (lo medible del vídeo)

1. **Quién compite por la ventana**: system prompt, definiciones de herramientas, documentos pegados, historial y **la propia respuesta** (responder ocupa lugar: el autor recuerda que suele olvidarse). Si la respuesta no cabe, no se genera.
2. **Demo 1 — las herramientas son caras** (API real, Claude Opus 5 según el autor): system prompt de 878 caracteres = **355 tokens**; cuatro herramientas (leer archivo, escribir archivo, ejecutar comandos, búsqueda web) = **1.183 tokens**. Total ~1.500 tokens antes de que el usuario escriba nada. *El desglose por herramienta que da en el directo (542 / ~900 / ~1.340 / ~15.500) no es legible con fiabilidad en el ASR: sólo se citan las dos cifras que aparecen literales en la transcripción y repetidas en la descripción del autor.*
3. **Los tres costes**: dinero, tiempo y atención.
   - Dinero: ~5.000 tokens fijos por request × 10.000 requests/día ≈ **150 $/día ≈ 4.500 $/mes "sólo por leer instrucciones"** (cifra también en la descripción del autor). La aritmética intermedia no es reproducible desde la transcripción: el ASR mezcla 10.000 y 150 requests/día.
   - Tiempo: "la imprenta se estira" — más contexto, más tarda en salir el primer token, con el usuario mirando una pantalla en blanco.
   - Atención: más texto no es mejor respuesta, es **ruido**.
4. **Demo 2 — pérdida en el medio** (catálogo de 44.328 caracteres, **221 fichas**, ficha 0847 "Reina de la Noche" con el dato anómalo). Petición A con el dato al final, B con el dato en medio: **el modelo acertó en las dos**. El autor lo dice sin adornos: "no se rompe siempre, eso es otra cosa, pero lo que baja es la confiabilidad cuanto más en el medio esté". **Un vídeo de divulgación que declara el resultado nulo de su propia demostración es señal de honestidad** y debe anotarse como tal: la pérdida en el medio NO es un fallo reproducible en cada ejecución.
5. **Demo 3 — caché**: con la variable (fecha + ID de sesión) al principio, el segundo request reenvía todo; con la variable al final, **el 99 % del prompt queda cacheado** ("eso es dinero que no se paga"). Las cifras de tokens que va cantando (18, 707, 70.095, 727, 795) no son fiables por ASR.
6. **Tres estrategias, de peor a mejor**: (1) truncar — la peor, porque corta instrucciones y el modelo olvida por qué pasan las cosas; (2) resumir/compactar — pierde detalles y el porqué, y degrada en cada pasada; (3) **no llenarla**: índice + carga perezosa, patrón "orquestador-minion", RAG superficial.
7. **Demo 4 — la memoria inflada paga alquiler**: memoria sin podar de **428 líneas ≈ 91 $/mes** frente a una podada de **19 líneas / 192 tokens ≈ 3 $/mes**; diferencia declarada "+87,59 $/mes" y "26 veces más grande". *Aviso aritmético: 428/19 = 22,5 veces en líneas, no 26 — el factor de 26 probablemente se refiera a tokens, pero la cifra de tokens de la memoria inflada no se entiende en el ASR ("58 tokens" no cuadra). No usar ese 26 como dato.*
8. **Tarea que propone al final** (sirve de plantilla para el lab): medir tokens de system prompt + tokens de herramientas + requests/día, y sectorizar con un índice qué se carga cuándo.

### CLAIMS NO CONTRASTADOS (RULE-017)

- "GPT 5.6 ahora mismo estamos en 500.000 [tokens de contexto]" — afirmación de parte, sin fuente en el vídeo, dicha al pasar.
- Todas las cifras en dólares son **cálculos del autor con supuestos que no declara del todo** (modelo, tarifa por millón, tamaño de las herramientas): valen como orden de magnitud y como método, no como precio de referencia.
- El autor cita sus propias herramientas (gentle-ai, Engram, patrón orquestador-minion) sin datos de rendimiento: son parte interesada.

### Lo que NO hay (para no inflar el análisis)

Nada de **IA local**: ni modelos pequeños, ni cuantización, ni VRAM, ni hardware, ni evaluación de modelos, ni nada de n8n/Docker. Todo el vídeo se mueve en la nube (Claude Opus 5 y una suscripción) y en su propio stack de herramientas. Es divulgación con buenas metáforas, no un tutorial reproducible.

## Para el lab

| Afirmación del vídeo | Estado en el lab |
|---|---|
| Herramientas/MCP se cargan siempre y cuestan contexto | **PARCIAL**: `platform_toolsets` ya recorta toolsets por perfil; el coste en tokens de los 3 MCP no está medido → F1 |
| Qué NO debe ir a la memoria (estado temporal, resultado de test, números de línea) | **MEJORA**: regla de poda más afilada, con el motivo de cada decisión |
| Memoria inflada = coste recurrente y riesgo de alucinación | **ALINEADO**: MEMORY.md al tope del presupuesto; el vídeo aporta la cuantificación |
| Escribir memoria antes de compactar y releerla al salir | **YA EXISTE**: MEP-001 (`memoria-episodica.sh`), RULE-011 |
| Fijo adelante / variable atrás + caché | **YA EXISTE**: SOUL.md estable al frente, datos volátiles detrás |
| Buscar barato, profundizar caro | **YA EXISTE**: RAG + `agentic-rag` |
| Índice en vez de prompt completo (SDD) | **YA EXISTE**: skills bajo demanda, 144/164 desactivadas en `investigador` |
| Truncar = peor estrategia | **ALINEADO**: el lab compacta/resume, no trunca |
| Memoria ≠ contexto (RAG = bibliotecario) | **ALINEADO**: RAG LanceDB + memoria + contexto separados en la arquitectura del lab |

## Futuribles (sólo con señal real)

- **F1 (señal MEDIA, coste ~0 €): medir el coste en tokens del contexto fijo del lab** — SOUL + skills (ya hay `.skills_prompt_snapshot.json`) + definiciones de los 3 MCP + toolsets, y con ello decidir si algún MCP debe pasar a carga bajo demanda. Instrumento a validar antes de sacar conclusiones (RULE-015); es el mismo tipo de medición que pide el vídeo en su tarea final.
- **F2 (señal BAJA): añadir "el motivo" como campo obligatorio en las entradas de decisión** de la memoria/backlog, para no perder el *por qué* en la compactación.

Nada más: el resto del vídeo es marco conceptual ya implementado.

## Límites del análisis

- Hecho sobre auto-subtítulos (sin vídeo ni audio), con dedup de n-gramas: pueden faltar matices y **cifras concretas del ASR no son fiables** (marcadas arriba).
- El directo incluye preguntas del chat sin contexto; se han descartado las intervenciones que no aportan (una sobre release candidates de una herramienta, otra sobre setup de una librería).
- Registro creado el mismo día de publicación del vídeo (no hay otras fuentes que lo citen aún).
