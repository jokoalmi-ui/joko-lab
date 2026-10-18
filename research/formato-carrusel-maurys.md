---
title: "Formato de carrusel MAURYS — Referencia de estilo replicable (15-ago-2026)"
type: research
---

# Formato de carrusel MAURYS — Referencia de estilo replicable (15-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://www.instagram.com/p/DcByMArjN7L/ (carrusel "37 agentes", 10 slides)
**Análisis:** GLM-4.6V local, prompt de diseño por slide (10/10)
**Propósito:** documentar el formato que el usuario eligió como oficial del lab
("texto con gráficos bonitos y en español") para replicarlo en LinkedIn/TFM.

---

## 🎨 PALETA DE COLORES (consistente en las 10 slides)

| Elemento | Valor |
|---|---|
| **Fondo** | Crema/beige claro (#F5EFE6 aprox.) — tono cálido, papel |
| **Texto principal** | Negro (títulos y cuerpo) |
| **Acento** | **Naranja** (#FF7A00 aprox.) — títulos destacados, iconos, botones, flechas |
| **Tono general** | Claro, cálido, con contrastes fuertes negro/naranja |

**Regla:** fondo crema + texto negro + acento naranja. Nada más. (2 colores de
tinta + 1 acento = disciplina visual.)

---

## ✍️ TIPOGRAFÍA

- **Estilo:** sans-serif moderna (tipo Inter/Poppins/Montserrat)
- **Jerarquía (3 niveles):**
  1. **Título grande en MAYÚSCULAS, negrita** (ej. "EL CEREBRO EVITA ALUCINACIONES")
  2. **Subtítulo mediano** (a veces con palabra clave en naranja, ej. "HEADLESS")
  3. **Texto pequeño** para descripciones (regular, no negrita)
- **Regla:** TODO texto principal en negrita; descripciones en regular

---

## 📐 LAYOUT (patrón consistente slide a slide)

| Zona | Posición | Contenido |
|---|---|---|
| **Título** | Arriba izquierda (o centrado) | Frase potente, mayúsculas |
| **Cuerpo principal** | Centro | Gráfico/diagrama central (foco visual) |
| **Columna derecha o inferior** | Derecha/abajo | Listas con iconos ("Qué aporta", "Qué hace", beneficios) |
| **Pie / pasos** | Inferior horizontal | Secuencia de pasos (1-2-3-4) |

- **Margenes:** generosos, aire en todos los lados
- **Balance:** texto e imagen equilibrados (mitad/mitad o 60/40)
- **Densidad de texto:** BAJA — frases cortas, listas, nunca párrafos

---

## 📊 GRÁFICOS (el "gráficos bonitos")

- **Iconos circulares** para cada concepto/punto (target, terminal, candado, casa, estrella, engranaje...)
- **Diagramas centrales** como foco visual: dispositivo/monitor central con nodos conectados
- **Módulos hexagonales/circulares** con iconos (departamentos: Ventas, RR.HH., Marketing, Finanzas...)
- **Flujos con tuberías/flechas** que conectan elementos (proceso, pipeline)
- **Mapa del mundo con conexiones** (para "remoto/todos lados")
- **Ilustraciones de contexto** (monitor con código, laptop, dispositivo)
- **Regla:** cada idea = 1 icono + 1 frase corta. El gráfico explica, el texto apoya.

---

## 🧱 ESTRUCTURA DEL CARRUSEL (10 slides, arquetipos)

| Tipo de slide | Uso en maurys | Ejemplo |
|---|---|---|
| **Gancho** (slide 1) | Promesa grande | "Así manejo mi equipo de 37 agentes" |
| **Concepto** (2, 4) | Qué es, con diagrama | Agente Conductor, Paperclip |
| **Detalle técnico** (3, 6) | Cómo lo hace (headless, Hermes) | Monitor + iconos |
| **Beneficio/problema** (5, 7, 8) | Por qué (headless, memoria, local) | 3 problemas → 1 solución |
| **Escala/visión** (9) | Dónde llega | Tailscale, mapa mundo |
| **CTA** (10) | Acción | "Comenta BUILD" |

**Progresión narrativa:** Gancho → Concepto → Cómo → Por qué → Escala → CTA
(6 arquetipos, 10 slides = repite los medios según necesidad)

---

## ✅ LO QUE LA HACE ATRACTIVA (síntesis de las 10 slides)

1. **Contraste fuerte** negro/naranja sobre crema — legible y cálido
2. **Poco texto** — frases cortas, listas con iconos (nadie lee párrafos)
3. **Gráfico central por slide** — cada idea tiene su imagen
4. **Consistencia total** — misma paleta/tipografía/layout en las 10
5. **Narrativa progresiva** — cada slide avanza la historia
6. **En español** — conecta con el público objetivo

---

## 🛠️ CÓMO REPLICARLO EN EL LAB (pipeline ya existente)

1. **HTML por slide** con: fondo crema (#F5EFE6), texto negro, acento naranja,
   sans-serif (Inter), título mayúsculas negrita, iconos (SVG/emoji),
   gráfico central (CSS/SVG), margenes generosos
2. **Render:** Chrome headless → PNG 1080×1350 (validado 04-ago)
3. **Plantilla base:** adaptar la `plantilla-cuaderno-block.html` (ya usa
   papel crema + acento naranja — MISMA paleta) o crear `plantilla-maurys.html`
4. **Verificación:** GLM/browser_vision por slide
5. **Vídeo opcional:** `crear_video_explicativo.sh` (slides + edge-tts + ffmpeg)

**Pendiente para montar:** script orquestador `generar_carrusel_linkedin.py`
(ya planificado en el backlog, proyecto LinkedIn Lab 12-ago) + plantilla
`plantilla-maurys.html` con esta paleta/layout.

---

## Registro

- Guardado: research/formato-carrusel-maurys.md
- Relacionado: research/analisis-37-agentes-maurys.md (contenido)
- Veredicto: **REPLICABLE al 100% con el stack actual** (HTML→PNG + paleta ya usada en cuaderno-block)
