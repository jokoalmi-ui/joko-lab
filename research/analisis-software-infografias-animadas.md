---
title: "Análisis — Software open source para infografías animadas (19-ago-2026)"
type: research
---

# Análisis — Software open source para infografías animadas (19-ago-2026)
**VERACIDAD:** [VERIFICADO]

**Petición:** «¿qué software OpenSource podemos implementar para crear
infografías animadas?»
**Método:** investigación en sesión (regla del lab) — 6 búsquedas web reales,
fuentes verificadas por URL
**Contexto:** el lab YA tiene Manim MCP en producción (animaciones estilo
3Blue1Brown, 1080p60) + pipeline HTML/CSS estático (infografia-html v2).
Se busca qué AÑADIR, no empezar de cero.

---

## VEREDICTO: 3 CANDIDATOS REALES (open source, verificados)

### 1. 🥇 Motion Canvas (TypeScript) — el mejor encaje para el lab
- **Qué:** librería TypeScript que genera animaciones desde código (generators)
  + editor con preview en tiempo real. MIT.
- **Fuentes:** https://github.com/motion-canvas/motion-canvas ·
  https://awesome.ecosyste.ms/projects/github.com/motion-canvas/motion-canvas
- **Por qué encaja:** es EL "Manim de TypeScript" — mismo modelo mental
  (animación por código), pero orientado a UI/diagramas/tech explainers,
  no a matemáticas. Complementa a Manim: donde Manim necesita ecuaciones/
  gráficas, Motion Canvas brilla en **diagramas de flujo, arquitecturas,
  comparativas** — exactamente el estilo de las infografías de LinkedIn.
- **Coste:** 0 €, local, Node 22 ya instalado. **Riesgo:** nuevo stack
  (TypeScript), curva media.

### 2. 🥈 Revideo (fork de Motion Canvas enfocado a producción)
- **Qué:** fork de Motion Canvas enfocado a render en producción (APIs,
  pipelines batch). Open source.
- **Fuentes:** https://trybuildpilot.com/363-remotion-vs-motion-canvas-vs-revideo-2026 ·
  https://www.pkgpulse.com/guides/remotion-vs-motion-canvas-vs-revideo-programmatic-video-2026
- **Por qué:** si el lab quisiera GENERAR vídeos en batch (una plantilla →
  N variaciones), Revideo es la capa de producción encima de Motion Canvas.
  ⚠️ No probar hasta que haya necesidad real de batch.

### 3. 🥉 AntV Infographic (Ant Group, TypeScript) — declarativo + IA
- **Qué:** framework declarativo de Ant Group para generar infografías desde
  sintaxis de texto; **incluye skills para agentes de IA** (infographic-creator,
  infographic-syntax-creator). Open source.
- **Fuentes:** https://github.com/antvis/Infographic · https://infographic.antv.vision/ai ·
  https://dev.co/ai/frameworks/infographic
- **Por qué:** es EL más nuevo y "AI-friendly" — pensado para que un agente
  genere la infografía desde descripción. Encaja con la filosofía del lab
  (el agente crea el contenido). PERO: genera HTML/SVG estático (no vídeo
  animado); la animación habría que añadirla (CSS/canvas) o combinarlo con
  Motion Canvas/Manim.

---

## Comparativa rápida (fuentes cruzadas)

| Herramienta | Stack | Salida | Modelo mental | Mejor para |
|---|---|---|---|---|
| **Manim** (YA en el lab) | Python | Vídeo MP4 | Matemáticas | Ecuaciones, gráficas, explicaciones técnicas |
| **Motion Canvas** | TypeScript | Vídeo (render) | UI/diagramas | Diagramas de flujo, arquitecturas, comparativas |
| **Revideo** | TypeScript | Vídeo batch | Producción | Plantilla → N vídeos (cuando haya necesidad) |
| **AntV Infographic** | TypeScript | HTML/SVG | Declarativo + IA | Infografías estáticas generadas por agente |
| Remotion | React/JS | Vídeo MP4/GIF | React componentes | Web/UI (el vídeo de Lorena Bordonaba) — ya analizado, diferido |

---

## RECOMENDACIÓN (criterio coste/beneficio/timing)

**NO implementar nada hoy.** El lab ya produce infografías animadas (Manim)
y estáticas (HTML/CSS). Los candidatos son complementos, no sustitutos:

1. **Motion Canvas** = la mejor opción futura para el hueco real del lab:
   infografías de LinkedIn estilo "diagrama/arquitectura" animadas (donde
   Manim es torpe). **Señal:** primera vez que un post LinkedIn requiera
   un diagrama animado de arquitectura/flujo (p.ej. explicar el graph
   multi-agente o el pipeline RAG del lab en movimiento).
2. **AntV Infographic** = opción a vigilar (muy nuevo, con skills de agente);
   podría simplificar el pipeline estático actual. **Señal:** si el pipeline
   HTML/CSS manual se vuelve repetitivo.
3. **Revideo** = SOLO cuando haya batch real (plantilla → N variaciones).

**Regla DataStreak aplicada:** know-how (cómo hacer infografías animadas) →
ya está en skills; herramientas (manim, motion canvas) → se añaden con señal.

**Etiqueta:** [VERIFICADO] (URLs vistas en búsquedas, 6 fuentes cruzadas)
