---
title: "Análisis — \"Los Bots Están Destruyendo Internet (Y Cloudflare Tiene las Pruebas)\" (CodeSimple, 25-ago-2026)"
type: research
---

# Análisis — "Los Bots Están Destruyendo Internet (Y Cloudflare Tiene las Pruebas)" (CodeSimple, 25-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://youtu.be/i1UBCpWJ_YI (CodeSimple, 8 min, 226 views)
**Método:** metadatos + subtítulos ES (67 KB → 7.4K chars limpios, lectura completa)

## Qué dice el vídeo (datos citados)

1. **El trato se rompió**: Google rastreaba 5:1 (5 visitas reales por cada rastreo); el rastreador de Anthropic visita **70.000 veces por cada persona real** que llega. En junio de 2026, **57,5% de todo el tráfico web ya era bots** (proyección de Cloudflare para 2027, adelantada).
2. **Tres tipos de bot**: ① entrena modelos (copia contenido sin pagar), ② mantiene índice para motores de respuesta (cita sin clic), ③ entra en vivo cuando alguien pregunta a un chatbot. El 52% del rastreo de IA en junio = entrenar modelos, descargando páginas sin cambios.
3. **Costes reales**: Read the Docs: 1 bot descargó 73 TB/mes ($5.000+); iFixit: ~1M solicitudes de bots en 24h; Wikimedia: ancho de banda +50% en 1 año — los bots son 35% de visitas pero generan **65% de las solicitudes más caras** (sin caché: 1-2s CPU vs 20ms en caché).
4. **La escalera de defensa (y por qué cada peldaño falla)**:
   - `robots.txt` = sugerencia, no control de acceso (estándar 2022 lo dice literalmente)
   - Bloquear por User-Agent = falla (el bot escribe "Chrome")
   - Bloquear rangos de IP = falla (proxies residenciales: 5M solicitudes de 2M de IPs distintas en 1 día)
   - Proof-of-work = falló (los bots ya resuelven acertijos; aunque Nginx/FFmpeg/kernel lo usan)
   - **Nivel más alto: mentir** — laberintos de texto basura para atrapar al rastreador (1.5M páginas basura/día servidas sin que el bot note); comunidad de "data poisoning" para envenenar entrenamiento
5. **Perplexity pillado**: Cloudflare creó dominios secretos prohibidos en robots.txt; el buscador de OpenAI respetó, Perplexity apareció igual con navegador genérico → **expulsado de los bots verificados de Cloudflare** (Perplexity culpa a un proveedor externo).
6. **Tribunales**: caso Google vs herramienta de extracción → desestimado (resultados de búsqueda sin copyright); Reddit vs misma herramienta + Perplexity → sobrevive casi intacta. Sin regla clara: derechos de autor pierde, contratos ganan.
7. **Cheques**: Google→Reddit $60M/año; Reddit contratos de datos $203M; NewsCorp↔OpenAI $250M/5 años.
8. **Pago por rastreo**: Cloudflare y Amazon lanzaron sistemas de pago por rastreo; código **HTTP 402 Payment Required** (30 años sin usarse). Pero ese dinero no baja a servidores pequeños de 6€/mes.
9. **Consejo práctico**: no ganarás con más reglas; **deja de dar munición**: ordena tu web, elimina paginación infinita, no enlaces a calendarios infinitos, imágenes en tamaño fijo, caché en rutas caras ("un rastreador no puede quebrar un endpoint que ya no existe"). Futuro: estándar de **firma criptográfica por rastreo** (Cloudflare/Amazon ya verifican, OpenAI ya firma).

## 🔴 Aplicación al LAB — VALOR MEDIO-ALTO (explicativo + lecciones)

### ✅ Explica los bloqueos que el lab YA sufre
- **Fragrantica / Medium** bloqueadas por Cloudflare → es la escalera de defensa en acción (el lab no es un bot, pero Cloudflare no distingue).
- **Wallapop CloudFront 403** (24-ago) → bot-detection moderna; los proxies residenciales y navegadores genéricos de la defensa explican por qué "no scrapeable sin sesión".
- El lab usa yt-dlp/curl/browser legítimamente → entender la defensa del otro lado evita prometer scraping imposible (lección Wallapop aplicada).

### ✅ Lecciones para el FUTURO del lab
| Lección | Aplicación |
|---|---|
| robots.txt = sugerencia | El lab puede rastrear sitios que no lo prohíben explícitamente (Tecnoempleo verificado 25-ago: robots.txt permite) |
| HTTP 402 (pago por rastreo) | Futuro: algunas APIs/sitios empezarán a exigir pago — considerar en el buscador de precios |
| Firma criptográfica de rastreadores | Futuro: scraping de sitios "firmados" requerirá acreditación — vigilar |
| Consejo: no dejar endpoints inútiles | Aplicable si el lab publica web (ficha perfume, LinkedIn no aplica) |
| **No existe scraping 100% garantizado** | Confirmado: cada defensa tiene contra-defensa; verificar SIEMPRE antes de prometer (lección Wallapop, Tecnoempleo OK) |

### ⚠️ Nada accionable HOY
- No cambia nada del stack actual (el lab no tiene web pública que defender).
- No habilita nuevos scraping (los bloqueos siguen igual: Cloudflare/Fragrantica/Medium siguen bloqueados).
- Material de contexto/TFM: el fenómeno "bots vs web abierta" es un tema de actualidad válido para LinkedIn Lab educativo.

## Conclusión
VALOR MEDIO-ALTO como **conocimiento de contexto**: explica de forma verificada por qué el lab encuentra bloqueos (Cloudflare, CloudFront), refuerza la regla "verificar antes de prometer scraping" y da contexto legal/económico para el futuro (HTTP 402, firmas criptográficas). Nada accionable hoy — pero es material que evita decisiones equivocadas en el futuro (p.ej. intentar scrapear Wallapop/Medium con más empeño).
