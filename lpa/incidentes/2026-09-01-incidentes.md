---
title: "Registro de incidentes — 2026-09-01"
type: knowledge
---

# Registro de incidentes — 2026-09-01

Fuente del mecanismo: sesión 2026-07-27 (acuerdo "Mecanismo de recogida de evidencias").
Pregunta obligatoria: ¿Ha ocurrido hoy algo que el laboratorio no sabía ayer?
Clasificación: FALLO / ACIERTO / DUDOSO / HIPÓTESIS. Fallo → lección → acción → skill.

---

## INC-20260901-001 — Carrusel LinkedIn renderizado como página de error (bug file:// relativa)

- **Tipo:** FALLO (proceso de verificación falso-positivo)
- **Qué ocurrió:** `generar_carrusel_linkedin.py` usaba `file://salidas/...` (ruta RELATIVA) en la URL de Chrome → `ERR_INVALID_URL` → Chrome renderizaba la página de error. Todos los carruseles, incluida la F1 "verificada", eran renders de error (PNG 33 KB oscuros).
- **Dónde falló:** URL de render en el script (falta `os.path.abspath`).
- **Cómo se descubrió:** al revisar el tamaño del PNG (33 KB = sospechoso) frente a los esperados con estilo real (60-95 KB).
- **Eslabón de la cadena:** generación/render (pre-verificación).
- **Gravedad:** alta (corrompió la salida "verificada" de días anteriores).
- **Lección reusable:** un render con PNG sospechosamente pequeño (< 50 KB para 1080×1350) es señal de error, no de éxito. La verificación debe comprobar TAMAÑO y contenido, no solo "el comando salió bien".
- **Acción:** fix `os.path.abspath(tmp_html)` aplicado; re-verificar F1 con el fix.
- **Convertido a:** checklist de tamaño mínimo en verificación de renders (skill infografia-html / linkedin-carrusel-lab).
- **Estado:** CORREGIDO / re-verificación de F1 pendiente.

**RE-VERIFICACIÓN F1 (20:40, INC-001 cerrado):** la F1 (lancedb, 2026-08-20) NO era render de error. Evidencia: (1) PNGs 53-82 KB (no los 33 KB del error); (2) análisis de píxeles perfil = referencia buena ecosistema (brillo ~233 claro, ~1% píxeles color, estilo crema maurys — un error de Chrome sería oscuro); (3) GLM local: infografía real con título "MI RAG OCUPABA 26 GB Y NO LO SABÍA", fondo beige, acentos naranja. La afirmación previa del backlog ("la F1 también era error") era inferencia no verificada — quedó refutada. El bug de file:// relativa afectó solo a carruseles generados el 01-sep antes del fix; los del 20-ago eran correctos. Lección añadida: NO extrapolar un bug a salidas anteriores sin verificar (mismo patrón que "no concluir que algo está caído sin salida real").

## INC-20260901-002 — Chrome headless con --disable-gpu dibuja el texto vacío

- **Tipo:** FALLO
- **Qué ocurrió:** render 2D con texto usando `--disable-gpu` → el texto NO se dibuja (PNG ~33 KB) aunque el HTML está bien.
- **Dónde falló:** flag de render de Chrome headless.
- **Cómo se descubrió:** PNG demasiado pequeño + comparación con el mismo HTML renderizado con GPU (52 KB+).
- **Eslabón:** render.
- **Gravedad:** media (fácil de detectar por tamaño, pero silencioso si no se mira).
- **Lección reusable:** NUNCA usar `--disable-gpu` para renders 2D con texto en Chrome headless.
- **Acción:** documentado en skill infographic-production (F6) + pitfall en infografia-html.
- **Convertido a:** regla en la skill.
- **Estado:** CORREGIDO.

## INC-20260901-003 — Saludo del perfume del día enviado como mensaje aparte (Hermes v0.17.0)

- **Tipo:** FALLO (dependencia de versión, no de flujo)
- **Qué ocurrió:** el texto tras `[media attachment]` se enviaba como mensaje separado antes de la burbuja de imagen sin caption. Causa raíz: Hermes v0.17.0; fix en v0.21.0 (`_media_caption_split`, línea 102 de `tools/send_message_tool.py`).
- **Dónde falló:** capa de envío de Hermes (no la skill).
- **Cómo se descubrió:** el usuario lo reportó ("el saludo ha llegado a parte").
- **Eslabón:** envío media+caption.
- **Gravedad:** media (cosmético pero molesto).
- **Lección reusable:** antes de diagnosticar un flujo propio, verificar la versión del runtime (causa raíz puede estar en la plataforma, no en la skill).
- **Acción:** actualizar Hermes a v0.21.0; simplificar el mensaje de la skill a SOLO el saludo (formato vigente confirmado por el usuario).
- **Convertido a:** formato vigente en skill perfume-del-dia (Paso 6).
- **Estado:** CORREGIDO / formato confirmado.

## INC-20260901-004 — Piloto de infografía rechazado: "los mismos cuadros con texto de antes"

- **Tipo:** FALLO (de proceso, el más importante)
- **Qué ocurrió:** produje un piloto de infografía 16:9 SIN pedir referencia visual previa. El usuario lo rechazó: estructura idéntica a lo anterior (tarjetas/cuadros con texto) aunque con más color y fondo generado.
- **Dónde falló:** F1 ANALYZE de la skill infographic-production — no pregunté por referencia/estilo objetivo antes de producir.
- **Cómo se descubrió:** feedback directo del usuario tras la entrega.
- **Eslabón:** captura de requisitos visuales.
- **Gravedad:** alta (trabajo perdido + frustración + 3ª iteración necesaria).
- **Lección reusable (la de proceso):** ANTES de producir una infografía, si existe posibilidad de referencia (IG/LinkedIn/captura), PEDIRLA y extraer el formato con GLM antes de montar nada. No asumir que "más color + fondo" satisface; el salto es de COMPOSICIÓN, no de estética.
- **Acción:** pedida la referencia → extraído formato de la slide 8 (TheVectorForge cheat sheet: fondo blanco flat, grid de cajas, acento verde, proporción 4:5) → replicado con datos reales del lab → verificado 7/7 GLM.
- **Convertido a:** regla obligatoria en skill infographic-production F1.
- **Estado:** CORREGIDO (V2 entregada) / lección integrada en la skill.

---

## ACIERTOS del día (para no perder el otro lado)

- **A-001:** Diagnóstico del saludo separado: se localizó la sesión de la mañana, se comparó con el código de Hermes (`_media_caption_split`) y se confirmó la causa raíz por versión, sin tocar n8n ni flujos ajenos.
- **A-002:** Extracción del formato de la slide 8 de referencia (IG) mediante descarga HEIC→JPG + análisis GLM — el formato se replicó fielmente (fondo blanco, grid, acento verde, 4:5).
- **A-003:** swap VRAM GLM↔SDXL para el fondo ComfyUI del piloto, validado sin romper nada (recarga de GLM OK).

## INC-20260901-005 — EL LAB APARCÓ LPA (el mayor fallo del día, señalado por el usuario 02-09 00:15)

- **Tipo:** FALLO (de proceso, raíz de todos los demás)
- **Qué ocurrió:** el mecanismo de evidencia acordado el 27-jul ("¿ha aprendido algo el lab hoy? → clasificar en LPA: FALLO/ACIERTO/DUDOSO/HIPÓTESIS") no existía materializado como archivo hasta el 02-09. Un mes sin que ningún fallo ascendiera a patterns-observed.md ni al incubator. LPA se convirtió en DOCUMENTACIÓN (KNOWN/HYPOTHESIS/UNKNOWN sin tocar desde 31-07/14-08) en vez de MECANISMO vivo: fallo → evidencia → lección → patrón → gobernanza.
- **Dónde falló:** la capa meta del lab. El día a día operativo (carruseles, crons, análisis IG/YT, outliers) devoró el bucle de aprendizaje. Es el problema que LPA mismo describe: el tiempo y la operación degradan el sistema si no hay un mecanismo que lo fuerce.
- **Cómo se descubrió:** el usuario lo señaló: "hoy tengo la sensación de que aquello que hacía diferente a nuestro lab, el concepto LPA de aprendizaje para forjar la gobernanza, se ha ido al carajo" — confirmado con fechas reales de modificación de los archivos LPA.
- **Gravedad:** CRÍTICA (es el fallo raíz: los demás fallos se registran pero no forjan gobernanza).
- **Lección reusable:** LPA sin ciclo de promoción activo = archivo muerto. La gobernanza operativa (RULEs, JL, gates) sobrevive; el aprendizaje que la alimenta se duerme si no hay una revisión periódica OBLIGATORIA que promueva incidentes → incubator → KNOWN.
- **Acción (propuesta, pendiente OK usuario):** ciclo semanal de 30 min: revisar incidentes → los que muestren patrón (2+ veces) suben a pattern-incubator; los de proceso van directos a skill. Mensual: incubator → KNOWN/HYPOTHESIS. Nada de infraestructura nueva — es el hábito, no el documento.
- **Estado:** REGISTRADO / revisión mañana 02-09 (cron 08:30) + decisión de activar el ciclo semanal.
- **Convertido a:** prioridad #1 de la revisión de mañana.

## HIPÓTESIS abiertas

- **H-001:** "Preguntar por referencia antes de producir reduce iteraciones rechazadas en infografías" — E0 (1 caso: INC-20260901-004). Si vuelve a ocurrir en otro formato (carrusel, póster), sube a E1.

---

## Acciones derivadas (backlog + skills)

1. Skill `infographic-production` F1: OBLIGATORIO pedir referencia visual si existe; extraer formato con GLM antes de producir. (hecho en la skill)
2. Skill `infografia-html`: pitfall tamaño mínimo de PNG en verificación. (existente, refuerza)
3. Re-verificar carrusel F1 con el fix de abspath. (pendiente)
4. Revisar semanalmente este registro (mecanismo del 27-julio: al final de cada tarea importante, clasificar evidencia).
