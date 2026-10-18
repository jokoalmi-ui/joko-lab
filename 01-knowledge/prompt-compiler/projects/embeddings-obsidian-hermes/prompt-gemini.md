---
type: knowledge
subtype: prompt
status: active
tags: [knowledge, prompt]
created: 2026-07-28
---
# Prompt gemini

PROMPT OPTIMIZADO — Gemini: Embeddings + Obsidian + Hermes Agent
================================================================
Creado: 2026-07-28
Skill: prompt-engineering v1.0.0
Destino: Gemini (Google) — modelo cloud, no testeado en Joko Lab
Estilo: Directo, técnico, instrucciones explicitas, tablas y codigo

═══════════════════════════════════════════════════════════
INSTRUCCIONES DE USO
═══════════════════════════════════════════════════════════

Este prompt esta disenado para ser usado con Gemini.
Se puede enviar directamente a la API de Gemini o copiar
en su interfaz web.

Configuracion recomendada:
- Temperature: 0.2
- max_output_tokens: 8192
- Sin tool-use (es texto plano)

═══════════════════════════════════════════════════════════
PROMPT
═══════════════════════════════════════════════════════════

Eres un ingeniero de IA especializado en sistemas RAG locales
y personal knowledge management. Tu tarea es investigar y
documentar como integrar embeddings (BGE-M3) con Obsidian
para mejorar las capacidades de Hermes Agent.

Contexto: Hermes Agent (v0.17.0) es un agente de IA que se
ejecuta en local (Ubuntu 24.04, GPU RTX A2000 12GB). Tiene
un sistema de skills (prompts reutilizables con frontmatter
YAML), una memoria persistente, y acceso a herramientas de
archivos y terminal. El usuario documenta su trabajo en
formato Markdown dentro de ~/joko-lab/.

Objetivo: Disenar un sistema donde:
1. Las notas de Obsidian (o archivos .md del proyecto) se
   indexen con BGE-M3 (o el mejor embedding multilingue
   disponible)
2. Hermes Agent pueda consultar semanticamente esas notas
   durante una conversacion para recuperar contexto relevante
3. El sistema funcione 100% local, sin dependencias cloud

Requisitos del informe:
- Explica que es BGE-M3 y por que es mejor que nomic-embed-text
  para contenido en espanol (el laboratorio documenta en
  castellano)
- Compara opciones de indices vectoriales: FAISS, sqlite-vec,
  Chroma, LanceDB. Recomienda UNA con justificacion.
- Incluye un ejemplo practico completo:
  * Codigo Python para generar embeddings de archivos .md
  * Codigo Python para buscar por similitud semantica
  * Integracion basica con Hermes Agent (como skill o plugin)
- Describe el flujo: usuario escribe nota en Obsidian →
  indexacion automatica → Hermes recupera contexto relevante
  en conversaciones futuras
- Incluye metricas de rendimiento esperadas (tiempo de
  indexacion, latencia de busqueda, precision estimada)
- Proxismos pasos para productionizar el sistema

Formato de salida: Informe tecnico en Markdown, con
secciones numeradas, tablas comparativas, bloques de codigo
con sintaxis, y ejemplos ejecutables.

Restricciones:
- Sin servicios cloud. Todo local.
- Sin depender de npm o Node.js si es posible. Preferir
  Python con pip.
- Los modelos de embedding deben caber en 12GB de VRAM
  compartida con el LLM principal.
- El codigo debe ser funcional, no pseudocodigo.

Estructura del informe:
1. Resumen ejecutivo
2. Que son los embeddings y BGE-M3
3. Comparativa de indices vectoriales (tabla)
4. Arquitectura propuesta (diagrama en texto)
5. Implementacion paso a paso
   a. Instalacion de dependencias
   b. Indexacion de notas
   c. Busqueda semantica
   d. Integracion con Hermes Agent
6. Ejemplo practico completo (codigo funcional)
7. Metricas y rendimiento
8. Limitaciones y proxismas mejoras
9. Conclusion

Genera el informe completo ahora. No te detengas hasta
terminar todas las secciones. Si no sabes algo con certeza,
indicalo como "pendiente de verificacion" pero completa el
resto del diseno.

═══════════════════════════════════════════════════════════
FIN DEL PROMPT
═══════════════════════════════════════════════════════════
