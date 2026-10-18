---
title: "Análisis — Infografía \"AI Made Simple: 4 Key AI Concepts\" (Hope AI, 16-ago-2026)"
type: research
---

# Análisis — Infografía "AI Made Simple: 4 Key AI Concepts" (Hope AI, 16-ago-2026)

**Fuente:** https://www.instagram.com/p/Db-Wn7bTSbV/ (hope_artificial_intelligence, post de imagen única 1440×1800)
**VERACIDAD:** [VERIFICADO]

## Qué es (resumen)

Póster/infografía vertical "AI MADE SIMPLE: 4 KEY AI CONCEPTS YOU SHOULD KNOW".
Explica 4 conceptos clave de IA con analogías visuales sencillas, formato
didáctico tipo póster (marca Hope AI, "Your Future Starts Here").

## Los 4 bloques (con su color)

| Bloque | Color | Icono | Analogía |
|---|---|---|---|
| **AI Agents** | Naranja | Cerebro | "Brain + Action" — toma acciones, usa memoria y herramientas, logra objetivos |
| **Gen AI** | Azul | Pecho mecánico/engranajes | "Creativity Engine" — genera contenido nuevo (texto, imagen, código, audio), aprende patrones |
| **LLM** | Morado | Cabeza humana con cerebro | "Brain (Language)" — entiende y genera texto, entrenado con datos masivos |
| **RAG** | Verde | Persona leyendo con cerebro | "Brain + Knowledge" — LLM + conocimiento externo (documentos, BD), respuestas precisas y actualizadas |

## Diseño visual (análisis GLM)

- **Fondo**: blanco puro (#FFFFFF).
- **Layout**: vertical. Cabecera central con título + logo arriba derecha.
  4 bloques apilados verticalmente (no 2x2), cada uno con: icono → caja con
  título/definición/bullets → ejemplo visual → flecha conectora hacia el siguiente.
- **Cajas**: rectángulos con esquinas redondeadas, cada una con su color de
  acento (borde/texto/bullets del color del bloque).
- **Iconos**: ilustraciones de cerebro, engranajes, cabeza, persona leyendo
  (los 2 primeros con color de bloque; los 2 últimos morados).
- **Tipografía**: sans-serif. Título grande (~48px, negrita, negro) con
  símbolos decorativos; títulos de bloque ~28px negrita en mayúsculas;
  descripción ~16px regular.
- **Flechas**: horizontales, color del bloque, conectan una sección con la siguiente.

## ¿SE PUEDE REPLICAR CON EL LAB? → SÍ, con HTML/CSS propio

| Elemento | Facilidad | Cómo en el lab |
|---|---|---|
| Cajas redondeadas + colores | ✅ Fácil | CSS border-radius + variables de color |
| Layout vertical 4 bloques | ✅ Fácil | Flexbox/Grid |
| Tipografía sans-serif | ✅ Fácil | Fonts del sistema o Google Fonts |
| Flechas conectoras | ✅ Fácil | CSS/SVG (flechas simples horizontales) |
| Iconos (cerebro, engranajes, cabeza, persona) | 🟡 Medio | Emojis/SVG libres (o iconos simples hechos en SVG) |
| Ilustraciones tipo "robot en plataforma", "monitor", "libros" | 🟡 Medio | SVG simple o iconos; no necesita ilustración compleja |
| Estilo general | ✅ Fácil | Mismo pipeline que plantilla maurys / cuaderno (HTML/CSS → captura → PNG) |

**Conclusión**: la infografía es 100% replicable con el stack del lab
(HTML/CSS + captura, como las plantillas maurys/cuaderno ya usadas para
carruseles). Los iconos son lo único que requiere trabajo (SVG o emoji),
pero nada exige herramientas externas.

## Relevancia para el LAB

- **Formato**: patrón "1 concepto = 1 caja de color + icono + analogía" —
  excelente plantilla didáctica reutilizable (carruseles LinkedIn, material
  educativo).
- **Contenido**: los 4 conceptos (Agent, Gen AI, LLM, RAG) son exactamente el
  stack del lab — material perfecto para la marca personal.
- **Acción**: si se quiere, se puede generar una versión propia (por ejemplo
  "IA local para empresas" con 4 conceptos del lab) con la plantilla maurys.

## Futuribles (registrar)

1. **Plantilla "4 conceptos en 4 cajas de color"** para carruseles del lab
   (HTML/CSS reutilizable, estilo maurys) — sirve para LinkedIn Lab
2. **Versión propia**: "4 conceptos de IA local" (Ollama/LM Studio, RAG,
   agentes, GGUF) con el mismo formato — contenido educativo de marca
