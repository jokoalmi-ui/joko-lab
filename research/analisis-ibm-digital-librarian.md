---
title: "Análisis — \"Digital Librarian AI Agent: Connecting SQL & Vector Database\" (IBM Technology, 24-ago-2026)"
type: research
---

# Análisis — "Digital Librarian AI Agent: Connecting SQL & Vector Database" (IBM Technology, 24-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://www.youtube.com/watch?v=eFf2OvkZxEM (IBM Technology, 23-08-2026, 5:21 min, 6.509 views)
**Método:** subtítulos EN (6.4 KB, ES 429) → limpieza → análisis completo (4.5K chars)

## El concepto

**"Digital Librarian Agent"** — un agente que resuelve el problema **"el qué vs el porqué"**:

| Mundo | Qué contiene | Ejemplo (farmacia) |
|---|---|---|
| **SQL database** (el QUÉ) | Números duros, datos estructurados | "¿Está cubierta tu prescripción?" → SÍ/NO en una tabla |
| **Vector database** (el PORQUÉ) | Contexto, reglas, letra pequeña, documentos | "¿Por qué?" → página 14 del manual de 50 páginas en PDF |

El problema: los dos sistemas **no se hablan** → el técnico de farmacia no puede decirte por qué te deniegan algo.

## Los 6 pasos del agente (el patrón)

1. **Leer la pregunta** (LLM)
2. **Decidir qué es QUÉ y qué es PORQUÉ** — qué parte va a SQL y qué parte a vector (LLM)
3. **Construir las consultas** (LLM)
4. **Ejecutar las consultas** (tool/API)
5. **Compilar** las dos respuestas (Python/código de formateo)
6. **Responder la pregunta original** (LLM)

**Herramientas**: LLM para entender/decidir/responder (pasos 1,2,3,6) + tools para ejecutar y formatear (pasos 4,5).

## 🔴 Aplicación al LAB — VALOR MEDIO-ALTO (validación del diseño existente)

| Concepto del vídeo | En el lab |
|---|---|
| **SQL database (el qué)** | ✅ `lab-db` MCP (SQLite: coleccion.db, futuribles.db, cafes.db) |
| **Vector database (el porqué)** | ✅ `lancedb` MCP (RAG: 21.537 fragmentos de docs del lab) |
| **Agente que decide cuándo usar cada uno** | ✅ **Hermes decide** — con las 2 herramientas MCP disponibles según la pregunta |
| **Compilar + responder** | ✅ Hermes compila y responde con gate de veracidad |
| **"Entregas respuestas, no datos"** | ✅ El lab entrega informes/fichas con contexto, no dump de datos |

**La lección clave**: el lab **YA ES un "Digital Librarian Agent"** — tiene el QUÉ (SQL vía lab-db) y el PORQUÉ (RAG vía lancedb), y Hermes como el agente que decide cuándo consultar cada uno y compila. La validación de IBM (una de las empresas más serias del sector) confirma que este patrón es el estándar de la industria.

## El matiz honesto

- El vídeo es **conceptual** (IBM Technology, formato educativo corporativo) — no aporta implementación nueva, ni código, ni datos técnicos
- El ejemplo de farmacia es ilustrativo, no un caso real implementado
- **No hay futuribles** — es validación de una arquitectura que el lab ya tiene montada y funcionando

## Veredicto: VALOR MEDIO (validación)

- ✅ **Confirma externamente** (IBM) que el patrón SQL + Vector + agente que decide es el estándar
- ✅ El lab ya lo implementa con 2 MCPs (lab-db + lancedb) — sin nada que añadir
- ⚪ Único dato conceptual reutilizable: la **nomenclatura "el qué vs el porqué"** — útil para explicar el lab en LinkedIn/TFM ("mi lab separa los datos duros del contexto, y el agente decide cuándo usar cada uno")
- Sin futuribles

**Material LinkedIn/TFM**: "el QUÉ (SQL) + el PORQUÉ (RAG) + un agente que decide = Digital Librarian" — frase corta y potente para explicar la arquitectura del lab a no técnicos.
