---
title: "Análisis — CodeGraph: la herramienta local que hace más inteligentes a tus agentes (Michael Sahlmann Diaz, 15-ago-2026)"
type: research
---

# Análisis — CodeGraph: la herramienta local que hace más inteligentes a tus agentes (Michael Sahlmann Diaz, 15-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://www.youtube.com/live/Ig3epHN4Bes (live #50, ~1h, Michael Sahlmann Diaz)
**Transcripción:** completa (es)

## Qué es CodeGraph
Herramienta open source (56K estrellas, 3.5K forks, despegue mayo-junio 2026) que construye un **grafo de conocimiento local del código de un proyecto** (tree-sitter parsing → grafo de dependencias → SQLite). Es un "RAG de código": la IA consulta el grafo en vez de leer todos los archivos.

**MCP server automático** para: Claude Code, Cursor, Codex, OpenCode, **Hermes** (!), Gemini, Antigravity, Kiro. Si tu herramienta no está, configuración manual MCP.

## Instalación/uso (según la live)
1. Script `sh` de instalación (Linux/Mac) o PowerShell (Windows) — **a nivel proyecto, no global**
2. `codegraph init` en el proyecto → indexa en segundos (ej. del autor: 1.274 archivos en 1.4s)
3. Se queda en carpeta `.codegraph/` (SQLite, super ligero)
4. `codegraph index` (reindexar) / `codegraph sync` (actualización incremental automática) / `codegraph uninstall`
5. En el agente: `/mcp` → codegraph conectado → el prompt del agente busca en el grafo

## Beneficios medidos (según el autor)
- **Zero Read Cut**: reduce lecturas de archivos a cero para entender contexto
- **22% más rápido** en búsqueda
- **616 tokens por llamada** (ejemplo real: entender el flujo de confirmación de asistencia sin leer el código)
- "El agente no se pierde ni gasta tokens buscando"

## Configuración avanzada
- Instala instrucciones en `CLAUDE.md` / `AGENTS.md` / `GEMINI.md` por proyecto
- Modo "auto-autorizar" vs pedir permiso por herramienta (recomienda NO autoautorizar para gestión de tokens)
- Prompts con `how/who/trace` disparan búsquedas automáticas

## Veredicto para el lab
**VALIDA + GAP REAL identificado (aunque ya cubierto parcialmente):**

### Lo que el lab ya tiene
- RAG de conocimiento/documentos (LanceDB, BGE-M3, 19.894 filas, recall@5 100%)
- Suite 205 tests + gates (SVP/F4/KVC/KCR) para verificar refactors
- Procedimiento anti-colisión entre sesiones + skill de refactor seguro

### El GAP
- **El lab NO tiene grafo de CÓDIGO**: cuando OpenCode/Aider refactorizan joko-lab (344 funciones), leen los archivos enteros — gastan tokens de contexto (la palanca #1 del coste DeepSeek, 99% contexto)
- CodeGraph ataca EXACTAMENTE esa palanca: menos tokens de lectura = menos contexto = menos coste

### Pero (honestidad)
- El lab ya tiene el patrón de "refactor seguro con verificación" que funciona (24 refactors en un día, 0 ≥14)
- CodeGraph es una herramienta más para proyectos grandes de código con agentes — el lab ya tiene su propio sistema
- La VRAM/CPU del lab puede correrlo sin problema (SQLite, ligero)

## Decisión propuesta
**Futurible concreto**: probar CodeGraph en joko-lab (o en un proyecto de prueba) para medir si reduce el consumo de contexto de los refactors con OpenCode. Coste: bajo (instalación local, open source). Beneficio potencial: alineado con la estrategia de reducir contexto (coste DeepSeek). **NO urgente** — el lab funciona sin él; es optimización.

⚠️ Nota: el autor menciona que soporta Hermes como MCP automático — relevante para cuando se pruebe.

## Registro
- Guardado: research/analisis-codegraph-agentes-local.md
- Futurible: probar CodeGraph en joko-lab cuando se retome la tanda de refactors o si el coste DeepSeek sube.
