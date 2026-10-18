---
title: "Estudio de diseño — \"AI Simplified Series\" (nick.maughan, carrusel 5 slides)"
type: research
---

# Estudio de diseño — "AI Simplified Series" (nick.maughan, carrusel 5 slides)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://www.instagram.com/p/DYAf7M-kTnn/ (6-may-2026, 10,3 mil likes)
**Fecha estudio:** 2026-09-01 23:35 CEST
**Método:** 5 slides reales descargadas (1080×1350, 200-250 KB) + paleta EXACTA con PIL + análisis GLM visión (glm-4.6v-flash, max_tokens=4000) por slide

## 📐 La serie (5 slides)

| Slide | Título | Tema |
|---|---|---|
| 1 | **THE AI STACK** | Pila de IA en 6 capas (Apps → AI Models → Data → Infrastructure → Chips → Energy) con visual isométrico |
| 2 | **HOW AI WORKS** | Proceso de IA en 6 pasos + "Under the Hood" (ML vs DL, NLP vs GenAI) + aplicaciones reales |
| 3 | **WHAT IS QUANTUM COMPUTING?** | Clásico vs Cuántico + cómo funciona (4 etapas) + aplicaciones en investigación |
| 4 | **AI + QUANTUM + ROBOTICS** | Los 3 pilares + impacto real + "lo que NO significa" |
| 5 | **HUMANOID ROBOTS** | 5 secciones: qué los hace funcionar, evolución, hacia dónde van, cuellos de botella, mitos |

## 🎨 LA PALETA REAL (medida con PIL, no estimada)

**Fondo: blanco casi puro #f8f8f8 en TODAS las slides (62-81% de la imagen).** El diseño NO es colorido: es **minimalista con acentos estratégicos**. El color viene de:

- **1 color de marca por slide** (en el título):
  - Slide 1: azul real #4169E1 + morado #6A0DAD ("AI" azul, "STACK" morado)
  - Slide 2: gradiente violeta→azul #5B42E6→#2196F3 ("WORKS")
  - Slide 3: violeta profundo #5E17B8 ("QUANTUM")
  - Slide 4: azul índigo #3F51B5 + azul claro #2196F3
  - Slide 5: violeta #5B42E6 ("ROBOTS")

- **Color-codificación semántica** (la clave del sistema):
  - Slide 1: cada capa de la pila tiene SU color (Apps=verde #2E8B57, Models=azul marino #191970, Data=teal #008B8B, Infra=índigo #4B0082, Chips=azul #000080, Energy=naranja #D2691E)
  - Slide 2: pasos 1-6 en círculos de colores progresivos (azul claro→azul→violeta→verde→teal→verde)
  - Slide 5: 6 colores funcionales (violeta=inteligencia, azul=percepción, teal=destreza, verde=doméstico, naranja=coste, rojo=riesgo)
  - **El mismo color = el mismo concepto en toda la serie** (consistencia inter-slide)

- **Acentos vibrantes sobre blanco**: iconos flat de color en cada bloque (nunca más de 3-4 colores simultáneos visibles)

## 🖋 TÉCNICAS DE DISEÑO (lo que podemos copiar)

| Técnica | Detalle |
|---|---|
| **Fondo blanco + 1 color de marca** | El color NO llena el fondo: es acento. Fondo #f8f8f8 (62-81%) + título en color + iconos coloridos |
| **Color-codificación semántica** | Cada concepto tiene un color fijo que se repite en icono + texto + visual. El color ES información |
| **Jerarquía tipográfica brutal** | Título 60-80px bold · sección 24-32px bold · texto 12-14px regular gris #4A4A4A. Solo 4 niveles, claros |
| **Iconos flat vectoriales** | Símbolos simples (círculo con número blanco, icono lineal) — NO emojis, NO fotos |
| **Ilustración isométrica central** | Slide 1: bloques 3D apilados de la pila. Slide 3: átomo con gradiente. Slide 4: robot + nube cuántica |
| **Bloque final "IN A NUTSHELL"** | Fondo azul marino #1A237E + texto blanco — cierre de marca en cada slide |
| **Secciones numeradas (01, 02...)** | Números grandes en círculo de color — guían la lectura |
| **Fuente de autoridad** | Pie con "NMF.org" (origen de datos) — credibilidad |
| **Mucho espacio en blanco** | Secciones separadas por espacio, NO por líneas ni cajas |

## 🆚 vs LO QUE HACE EL LAB (honestidad)

| Aspecto | nick.maughan | Lab (maurys/actual) |
|---|---|---|
| Fondo | Blanco puro, minimalista | Crema #F5EFE6 (lleno) |
| Color | Acento + color-codificación semántica | Naranja #FF7A00 decorativo |
| Iconos | Flat vectorial consistente | Emojis |
| Jerarquía | 4 niveles claros | Variable |
| Cierre | Bloque "IN A NUTSHELL" de marca | Sin patrón de cierre |
| Origen de datos | Fuente citada (NMF.org) | No siempre |

**La diferencia clave**: el color en nick.maughan es **semántico** (transmite información: qué es qué); en el lab es **decorativo** (embellece cajas). Ese es el salto a dar.

## 🔴 QUÉ PODEMOS IMPLEMENTAR EN EL LAB

1. **Paleta semántica por ficha**: definir 1 color de marca + N colores de concepto (repetidos en icono+texto+visual)
2. **Fondo blanco/gris claro + acentos** (no crema lleno)
3. **Iconos flat SVG** en vez de emojis (ya tenemos la vía: SVG dibujado en el carrusel de prueba)
4. **Bloque de cierre "EN RESUMEN"** con fondo oscuro (patrón fijo de la serie)
5. **Fuente de datos citada** en el pie
6. **Espacio en blanco entre secciones** en vez de cajas

Todo con el pipeline nuevo (SDXL para ilustraciones centrales + HTML/SVG para iconos y texto + Chrome render).

## Notas honestas

- Los colores HEX de este informe son aproximaciones de GLM visión sobre imágenes comprimidas (los exactos de la paleta base #f8f8f8 SÍ son medición PIL). Para réplica exacta habría que medir píxel a píxel las zonas de color.
- nick.maughan cita NMF.org como fuente — la serie parece derivada de material educativo oficial (probablemente del National Museum of Computing o similar). El valor del diseño es suyo; la autoría del contenido es mixta.
- El carrusel es de hace 16 semanas (6-may-2026) — el estilo sigue vigente en el feed.


## ANTI-PATRÓN registrado 02-sep 09:50 (referencia NEGATIVA del usuario)

Post IG **DcxT4UIB-_C** — el usuario lo señala como EJEMPLO DE LO QUE NO QUIERE:
"es igual a lo que haríamos nosotros y es lo que NO quiero, este tipo de grafismo".
Síntoma: infografía genérica de cajas/recuadros con texto (el patrón que el lab producía).
Pendiente: extraer slides (navegador bloqueado por permiso Chrome; Chrome persistente a las 12:00)
+ documentar formalmente como anti-patrón lado a lado con nick.maughan (positivo).


## ANTI-PATRÓN DOCUMENTADO: datasciencescoop 'MCP Actually Explained' (DcxT4UIB-_C, 02-sep)

Referencia NEGATIVA explícita del usuario: 'es igual a lo que haríamos nosotros y es lo que NO quiero, este tipo de grafismo'.

Qué es: post de datasciencescoop (Asif Bhat, 01-sep-2026, 19 likes), imagen única 2700x3375. GLM visión confirma:
(1) Diseño con CAJAS numeradas (recuadros 1-5) combinando texto e iconos
(2) Fondo CREMA claro + negro + rojo alertas + amarillo notas
(3) Tipografía script en título + sans-serif en cuerpo
(4) Cajas separadas numeradas, texto alineado sobre fondo claro, flechas de proceso
(5) Iconos simples genéricos (herramienta, documento), alerta triángulo, escudo 'Trust'

Por qué es el anti-patrón (criterios del lab, lección nick.maughan):
- COLOR DECORATIVO, no semántico: crema de fondo no aporta información; rojo/amarillo = alertas genéricas sin sistema
- CAJAS como contenedores (el patrón que el usuario rechazó en F1/TFM/ficha perfume)
- Iconos flat genéricos de stock, no SVG propios
- Texto en recuadros, sin jerarquía de aire ni color de marca único
- NO es arte: no hay ilustración ni composición, solo plantilla de cajas

Contraste con el estándar del lab (02-sep): arte SDXL generado local + tipografía sobre arte, sin cajas, color semántico, cada pieza >= anterior. Este post es el 'antes' que NO repetir.

Contexto del post: sobre MCP (Model Context Protocol) — el tema sí era relevante para el lab (integración MCP), pero el GRAFISMO es el ejemplo de lo que no hacer. Guardado como referencia negativa junto al estudio nick.maughan (positiva).
