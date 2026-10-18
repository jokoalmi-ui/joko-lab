---
title: "Análisis — Carrusel albertoarius: Google AI Studio + Pomelli (17-ago-2026)"
type: research
---

# Análisis — Carrusel albertoarius: Google AI Studio + Pomelli (17-ago-2026)

**Fuente:** https://www.instagram.com/p/DbtQbkhkR7N/ (albertoarius, img_index=3 — carrusel de herramientas IA)
**Método:** browser_get_images → descarga 2 slides (1080×1350) → GLM + browser_vision
**VERACIDAD:** [VERIFICADO]
**⚠️ CARRUSEL PARCIAL**: solo se descargaron 2 slides (las visibles en img_index=3); puede haber más.

## CONTENIDO (lo que dice)

### Slide 1 — "Google AI Studio (el centro de Google)"
- Generar **imágenes, audios, vídeos y textos**
- Crear **aplicaciones completas** (frontend + backend)
- **Gratis** + acceso anticipado a actualizaciones de modelos de Google

### Slide 2 — "Pomelli"
- Para **PYMEs**: crear campañas de redes sociales alineadas con la marca
- Analiza el sitio web de la empresa → crea un **"ADN de la marca"** → sugiere campañas y creatividades alineadas
- Tagline: "Easily generate on-brand content for your business"

## 🎯 CONTEXTO DEL USUARIO (lo que motivó el envío)

El usuario está explorando: **MCP que conecta con Google AI Studio y todo el
ecosistema Google, para GESTIONAR y CREAR (no solo lectura) — conectar y
automatizar Google desde Linux.**

## APLICACIÓN AL LAB — OPINIÓN (conectando con lo que ya existe)

### Lo que el lab YA tiene (verificado):
- **Skill `google-workspace`**: Gmail, Calendar, Drive, Docs, Sheets vía gws CLI/Python
- **Skill `google-ai-pro`**: aprovechar la suscripción Google AI Pro (~20 €/mes) que el usuario YA paga
- **Experiencia MCP del día**: Manim MCP implementado en totalidad (17-ago)

### Mi opinión sobre "conectar y automatizar Google desde Linux":

| Opción | Qué es | Encaje con el lab |
|---|---|---|
| **Google MCP servers** (oficiales de Google: Gmail, Calendar, Drive, Docs, Sheets, Tasks) | Servidores MCP publicados por Google (abril-2025) | 🟡 **Muy interesante** — el lab ya tiene skills Google por CLI; el MCP estandarizaría el acceso |
| **Google AI Studio MCP** | MCP para usar Gemini/AI Studio desde agentes | 🟡 Complementario a google-ai-pro |
| **gws CLI (ya instalado)** | Acceso Google por terminal | ✅ Ya funciona — el MCP añadiría estandarización multi-agente |

### Mi veredicto honesto
**"Conectar y automatizar Google desde Linux" es un caso de uso REAL y el lab
está a medio camino**: ya tiene las skills (google-workspace, google-ai-pro)
pero por CLI scripteada, no como MCP. El siguiente paso natural, aplicando la
regla del post DataStreak (datos/herramientas externas → MCP), sería:

1. **Conectar los MCP oficiales de Google a Hermes** (Gmail, Calendar, Drive) — gratis, local-first (los datos de Google ya están en la nube de Google; el MCP solo es el puente)
2. **Verificar permisos mínimos** (least-privilege-lab R4: scopes limitados, nunca acceso total)
3. Casos de uso reales: automatizar el envío de informes del lab por Gmail, calendarizar hitos, subir exports a Drive

**⚠️ Matiz importante**: "no solo lectura" (escribir/crear en Google) implica
scopes de escritura → más riesgo. Con la política de mínimo privilegio del lab,
empezaría SOLO con lectura (informes, búsqueda) y añadiría escritura cuando
haya un caso concreto (p.ej. enviar informe diario por Gmail).

### Pomelli (slide 2)
Herramienta cloud para PYMEs (crear campañas con "ADN de marca") — 🟡
relevante solo como concepto para el futuro embudo de ventas/creación de
contenido, pero cloud y de pago → choca con local-first. No accionable hoy.

## Veredicto
**INTERESANTE y CONECTA con el hilo del día (MCPs).** Google AI Studio como
herramienta de creación es cloud (choca parcialmente con local-first, aunque
el usuario YA paga Google AI Pro). La vía más alineada: **MCPs oficiales de
Google** (Gmail/Calendar/Drive) para automatizar desde Linux con Hermes,
empezando por lectura (least-privilege). Pomelli: solo concepto, no accionable.
