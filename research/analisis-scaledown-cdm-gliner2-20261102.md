# Análisis — ScaleDown «CDM» y el hueco real: GLiNER2.5 en local

**VERACIDAD:** [VERIFICADO] — cifras de precio, fechas y licencias leídas en fuente primaria o en API; las cifras de rendimiento son **declaraciones del vendedor** o de terceros, y van marcadas como tales.
**Fecha del análisis:** 2026-11-02 08:0x CET (medido con `date` → `2026-11-02 08:05:40 CET (lunes)`).
**Disparador:** reel `https://www.instagram.com/reel/DezbLh8sDxG/` — `@silvesttre.ai`, 22-oct-2026, **1.739 likes / 517 comentarios**. Leído por `og:description` (caption literal completo); no se ha descargado el vídeo.
**Fuentes primarias:** `docs.scaledown.ai/introduction` (leída 02-nov-2026) · API de Hugging Face para los tres modelos `fastino/gliner2.5-*` (licencia, fechas, tamaños) · `ibl.ai/blog/constrained-decoding-models-not-a-new-architecture` (16-oct-2026) · `magica.com/news/scaledown-specialist-models-frontier-api-cost-claims` (13-oct-2026).
**Método:** `og:description` + `web_extract` de documentación y prensa + API de HF. **No se ha ejecutado ningún modelo**: este documento es verificación documental, no medición.

## Qué dice el reel

Estructura en tres actos: «primero llegaron los LLM, luego **Jev**, y ahora los **CDM**». Los LLM escriben palabra a palabra y se paga cada palabra; Jev «no escribe: decide» Sí/No con su % de confianza en milisegundos; los CDM de ScaleDown hacen un solo trabajo (clasificar, extraer, resumir) con formato fijo. Cierre: «si tu app solo necesita una etiqueta o un JSON, deja de pagar por discursos» + llamada a comentar «CDM» para recibir un DM.

Es **publicidad con gancho de divulgación**, no un análisis: no cita precios, ni licencias, ni qué pasa cuando el modelo falla — aunque sí incluye un aviso honesto («que una IA no hable no significa que no se la pueda engañar»).

## Qué hay de cierto (verificado)

- **ScaleDown existe y los CDM son un producto real.** `docs.scaledown.ai` define **CDM = Constrained Decoding Models** para «classification and structured decisions». Familia de tres modelos —**Classify, Extract, Summarize**— más un cuarto previo, **Compress**.
- **Precio publicado:** **0,05 $ por 1 M de tokens de entrada y 0 $ de salida** (directorio de LiteLLM, 16-oct-2026, citado por ibl.ai; Magica lo publica el 13-oct-2026). La salida es gratis porque **no hay generación autorregresiva**.
- **Fechas del lanzamiento:** mediados de octubre de 2026. Ancla firme: **13-oct-2026**, guía de integración de LangChain (`langchain-scaledown`) coescrita por el CEO de ScaleDown.
- **«Jev» no es un modelo de ScaleDown.** Es otro producto; lo que ScaleDown ofrece es un *endpoint* compatible (**«Decisions API (Jev-compatible)»**). El reel presenta dos marcas distintas como si fueran una secuencia de la misma casa.

## Lo que el reel omite, y rompe el relato

- **467× más barato y 200× más rápido son cifras de la empresa sobre cargas muy estrechas**, no una reducción de la factura de un agente completo (Magica, 13-oct-2026).
- **No es una arquitectura nueva.** El *constrained decoding* es una técnica de decodificación documentada desde antes; lo que hay es una **línea de producto**. (ibl.ai, 16-oct-2026, título literal: «Constrained Decoding Models Are Not a New Architecture».)
- **En el propio benchmark de ScaleDown**, su modelo de extracción **de pago** supera a **GLiNER2.5** —gratis y Apache-2.0— por **0,2 puntos porcentuales** (ibl.ai, misma fuente). Es decir: el argumento de venta se apoya en una diferencia que no se ve.
- **Solo existe como API alojada.** En el índice de 28 páginas de documentación **no aparece on-premise, VPC ni pesos descargables** (ibl.ai). Para el lab, local-first, esto lo descarta como componente.

## El hueco real: GLiNER2.5 (esto sí es nuevo en el lab)

Cero menciones de **GLiNER** en `research/` y en las skills del lab (verificado con `grep -rI`), y ningún análisis de ScaleDown. Los tres pesos, comprobados por API de Hugging Face el 02-nov-2026:

| repo | licencia | creado | likes | descargas | `model.safetensors` |
|---|---|---|---|---|---|
| `fastino/gliner2.5-base-v1` | apache-2.0 | 2026-08-18 | 40 | 112.838 | 774,4 MB |
| `fastino/gliner2.5-multi-v1` | apache-2.0 | 2026-08-14 | 294 | 107.521 | 1.149,5 MB |
| `fastino/GLiNER2.5-Decide` | apache-2.0 | 2026-09-23 | 446 | 133.094 | 1.945,8 MB |

Tags declaradas: `Named Entity Recognition`, `Structured extraction`, `Json extraction`, `Intent classification`, `Text classification`. El `Decide` lleva `decision-model` y el arXiv `2507.18546`. Es decir: **el «Jev» del reel tiene equivalente abierto y local**, y el extractor de ScaleDown tiene un competidor gratuito que el propio vendedor usa como referencia.

## Posición del lab

La tesis del reel ya es doctrina aquí: `01-knowledge/modelos_por_tarea.yaml` reparte modelos por tarea, el router decide por palabras clave y los modelos pequeños locales hacen clasificación y extracción. La diferencia es de coste: **aquí la inferencia local no factura por token**. El lab **no necesita ScaleDown**; lo que sí puede aprovechar es un **extractor no generativo** que haga el trabajo de un LLM sin generar texto — y eso es GLiNER2.5.

## Prueba pendiente (a partir de las 12:00 del 02-nov-2026)

No ejecutada. Contorno acordado con el usuario, a falta de definir el banco de pruebas:

1. **OBS:** hoy la extracción de campos (fichas de perfume, triaje de canales, clasificación de correo) se hace con LLM generativo.
2. **HYP:** GLiNER2.5-base extrae los mismos campos con ≥ el acierto actual y **latencia menor**, sin GPU grande.
3. **EXP:** mismo conjunto de textos reales del lab, mismas etiquetas, medir acierto por campo + latencia + pico de VRAM. Comparar contra el modelo que hoy hace la tarea.
4. **DEC:** solo entra si gana en acierto **o** empata con ventaja clara de coste/velocidad.

Requisitos antes de empezar: **descarga de pesos** (`base-v1`, 774,4 MB — el más pequeño de los tres), instalación de `gliner2` en un venv dedicado (**nunca** en el Python de Hermes) y **OK explícito** del usuario para ambas cosas.

## Veredicto

**El reel no entra en el lab**: es publicidad, sus cifras son reivindicaciones del vendedor sobre cargas estrechas y la técnica no es nueva. **Lo que entra como candidato es GLiNER2.5**, porque cubre un hueco real (no hay ningún extractor no generativo en el lab), es Apache-2.0, corre en local y tiene una versión «Decide» que replica el producto que el reel anuncia. Queda pendiente la medición, no la promesa.
