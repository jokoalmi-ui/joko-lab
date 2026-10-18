---
title: "Análisis carrusel TheVectorForge — Rate Limiting (13-ago-2026)"
type: research
---

# Análisis carrusel Instagram — TheVectorForge: Rate Limiting explained
**VERACIDAD:** [VERIFICADO]

- Fecha: 2026-08-13
- Fuente: https://www.instagram.com/p/Db8TzZ7Er5_/ (cuenta thevectorforge — Backend y AI)
- Tipo: carrusel 9 slides (heic → jpg vía stp)
- Método: navegación sin login → URLs JSON embebido (dedup) → descarga 9 slides →
  análisis GLM 4.6V local con `analizar_carrusel_rapido.py` (9 imgs en 71s,
  7.8s/img, paralelismo 3x) → formato visual con GLM max_tokens 1500 (3 slides
  clave: portada, Token Bucket, cheat sheet). browser_vision falló (modelo
  auxiliar rechaza image_url) → vía GLM con tokens altos.
- Clasificación: **APORTA conocimiento de system design** (formato reutilizable
  + contenido de rate limiting aplicable al gateway/router del lab).

## FORMATO (cómo se ve) — ✅ reutilizable para infografías propias

Patrón visual consistente en las 9 slides (verificado en portada, interior y
cheat sheet):

- **Estructura:** grid de secciones con títulos en MAYÚSCULAS bold; cada
  sección es un panel con fondo de color suave y borde ligero; paneles
  numerados para workflows (ej. "HOW TOKEN BUCKET WORKS" con 4 pasos);
  sidebar "QUICK TAKE" (resumen) en panel naranja claro; diagrama central
  ("THE BIG PICTURE") con flechas de flujo (aceptar/rechazar).
- **Paleta (hex aproximados):** título principal violeta #6A0DAD / #6c63ff;
  subtítulo/subsecciones verde #2E8B57 / #4caf50; iconos azul #4682B4 /
  #2196f3; rechazo/rate limiter rojo #DC143C / #e53935; Quick Take naranja
  #FFA500 / #ff9800 con fondo #F4C2A7; fondos de sección suaves (morado claro
  #9370DB, verde claro #90EE90); fondo general BLANCO puro.
- **Tipografía:** sans-serif; título grande/negrita (dos colores: violeta +
  verde), cuerpo pequeño/regular, encabezados de sección en mayúsculas.
- **Decorativos:** iconos de línea simple (usuario, escudo, servidor, reloj,
  cesta de tokens, gráfico, dólar, lightbulb en Quick Take, rocket en footer);
  checkmarks; logos reales (Google Cloud, AWS, Stripe) en "REAL-WORLD USAGE".
- **Aislable y reutilizable:** fila de 5 tarjetas de beneficios con iconos de
  colores; tabla comparativa de algoritmos; panel Quick Take; timeline
  (t=0s..t=4s); checklist de producción; cabecera HTTP con código.

## CONTENIDO (lo que dice) — 🟡 APORTA conceptos de rate limiting al lab

1. **Qué es:** controlar solicitudes por usuario/cliente; protege backends de
   sobrecarga, previene abuso, uso justo, estabilidad, control de costes.
2. **Flujo de un rate limiter:** solicitud → extraer key (IP, ID usuario) →
   verificar límite → permitir (incrementar contador) o rechazar HTTP 429 +
   cabecera `Retry-After`. Ubicación: API Gateway, Load Balancer, Backend.
3. **Algoritmos:** Fixed Window (problema de ráfagas en el borde — "Burst
   Problem"), Sliding Window (más preciso), Token Bucket (el más popular:
   bolsa de tokens que se rellenan a tasa constante; gestiona picos pero
   necesita almacenamiento; usado en AWS API Gateway), Leaky Bucket.
   Comparativa: precisión, manejo de ráfagas, memoria, complejidad.
4. **Distribuido con Redis:** contador compartido entre API Servers
   (multi-nodo); retos: condiciones de carrera, alta concurrencia,
   inestabilidad; escalado con TTL, caché, monitoreo; alternativas DynamoDB,
   Elasticsearch.
5. **Estrategias de límite:** per user, per IP, per producto, per patrón de
   uso; ejemplo combinado API Gateway + Rate Limiter.
6. **Arquitectura real:** cliente → DNS/CDN → API Gateway → Rate Limiter →
   Backend Services; cabeceras HTTP para comunicar límites al cliente
   (RateLimit-Limit / -Remaining / -Reset, Retry-After); checklist de
   producción y observabilidad.

## APLICACIÓN AL LAB (veredicto honesto)

- **FORMATO: ✅ accionable** — es el estilo "cheat sheet técnico" perfecto
  para infografías propias (infografia-html) y para las slides del TFM:
  paneles numerados, Quick Take, tabla comparativa, paleta violeta/verde sobre
  blanco. Se puede replicar sin copiar (patrón, no diseño).
- **CONTENIDO: 🟡 aporta contexto** — el lab NO expone APIs públicas que
  necesiten rate limiting crítico hoy, pero: (a) el gateway de Telegram /
  ai-router podrían necesitar límites (protección contra spam, costes por
  usuario); (b) refuerza el knowledge de system design para el TFM y para
  entrevistas/empleo (perfil senior IT + IA); (c) HTTP 429 ya lo conocemos de
  Yahoo/Stooq en bolsa — contexto unificado.
- **NO hay nada que implementar ya** — anotar como conocimiento + plantilla
  de formato.

## Registro

- Backlog 2026-08-06: entrada añadida (13-ago).
- Slides en /tmp/ig_rate_limiting/ (limpiadas tras análisis).
