---
title: "Curso IA y agentes — Lección 0: ¿Qué es realmente un LLM?"
type: guion-infografia
serie: ia-agentes (6 niveles · de lo básico a lo avanzado)
leccion: 0 de 6
estado: guion cerrado — pendiente formato y render
created: 2026-09-14
---

# LECCIÓN 0 — ¿Qué es realmente un LLM?

**Serie:** curso divulgativo de IA y agentes (NO del LAB). Cada nivel = una lección; cada lección termina con un gancho a la siguiente, para que se pueda leer en orden como curso.
**Plan completo:** `research/analisis-techyybanda-ai-agents-20260914.md` (secciones «CLASIFICACIÓN POR NIVELES» y «SUBNIVELES POR NIVEL»).
**Escalera didáctica de cada lección:** qué es → cómo funciona → confusión típica → ejemplo real → dato medible → cierre con gancho.

## TEXTO DE LAS SLIDES (exacto, para maquetar)

**S1 · Portada**
- Título: `LECCIÓN 0 · Qué es un LLM`
- Subtítulo: `La máquina que no busca: genera`
- Pie: `Curso de IA y agentes · 1 de 6`

**S2 · Qué es (0.1)**
- Titular: `Un patrón aprendido, no una enciclopedia`
- Texto: `Un LLM es un programa que ha leído muchísimo texto y ha aprendido un patrón: qué palabra suele venir después de cada palabra. No guarda las frases: guarda la estadística del idioma.`

**S3 · Cómo funciona (0.2)**
- Titular: `Escribe en cadena, un trozo cada vez`
- Pasos: `1. Tu texto se corta en trozos (tokens).` · `2. El modelo calcula qué token es más probable que siga.` · `3. Elige uno y lo añade al final.` · `4. Repite mirando todo lo anterior.`

**S4 · Confusión típica (0.3)** — caja tipo «Mistake»
- `❌ «La IA busca en internet y me lee el dato.»`
- `✅ Genera la respuesta más probable. Si no lo sabe, no se queda en blanco: produce algo que suena bien.`
- Cierre: `A eso lo llamamos alucinación (lección 5).`

**S5 · Ejemplo real (0.4)**
- `Le pides el autor de un informe interno que nunca ha visto.`
- `Sin tus datos: te da un nombre inventado, y con seguridad.`
- `Con tus documentos conectados (RAG, lección 2): responde y cita de dónde lo saca.`

**S6 · Dato medible (0.5)** — MEDIDO en el lab el 14-sep-2026
- Titular: `Se mide en tokens, no en palabras`
- Texto: `En español, 1 palabra ≈ 1,4 tokens (medido: 141 palabras → 195 tokens; 51 palabras → 69 tokens).`
- `La «ventana de contexto» es cuántos tokens puede tener delante a la vez. El modelo con el que se midió admite 131.072 tokens (~128.000). Si se llena, empieza a olvidar lo del principio.`
- Pie de método: `Medición propia: API de Ollama en local, modelo ibm/granite4.2:8b (14-sep-2026); tokens descontando los 15 de la plantilla interna; ventana de contexto según el propio modelo instalado.`

**S7 · Cierre**
- `En 1 minuto: (1) un LLM genera, no consulta; (2) escribe token a token; (3) se equivoca con seguridad — por eso hay que verificar.`
- Gancho: `Lección 1: cómo pedirle las cosas (prompt).`

## DATOS
- **Reales y medibles ya disponibles en el lab** (de la lección 5, no de esta): medición de alucinaciones (0/81 directo; 9,9 % bruto → 1,2 % real con razonamiento, 14-sep-2026).
- **Medidos y verificados (14-sep-2026):** ratio palabra→token en español (~1,4) y ventana de contexto del modelo (131.072 tokens). Método reproducible con la API local de Ollama.
- **Pendiente de fuente (no se publica sin verificar):** coste por millón de tokens de un modelo comercial (opcional en esta lección).

## FORMATO (a decidir con el usuario antes del render)
Estilos disponibles en `infografia-html`: paneles claros estilo MAURYS (estilo oficial contenido público, densidad baja, español), LAB NOTES / cuaderno con espiral, notas premium, dark técnico. La serie necesita **un solo estilo** para las 6 lecciones (coherencia de curso).
