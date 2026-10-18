---
title: "Análisis — ¿Los MCP están muriendo? La verdad sobre Skills (Fazt Code, 22-ago-2026)"
type: research
---

# Análisis — ¿Los MCP están muriendo? La verdad sobre Skills (Fazt Code, 22-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://youtu.be/eWY6bHtid1o (Fazt Code, 16-03-2026, 16:29 min)
**Método:** subtítulos ES descargados (188 KB) + extracción de fragmentos clave

## Contenido: MCP vs Skills — el debate

**El debate**: en redes se habla de la "muerte de los MCPs" porque los skills + herramientas adicionales pueden hacer tareas muy similares. ¿Es verdad?

**La respuesta del vídeo (fragmentos extraídos)**:
1. **Skills = documentos** que describen habilidades: "son documentos que por lo general ustedes pueden describir y allí ustedes pueden dar ese tipo de habilidad" — se activan con un comando o archivo de configuración
2. **Diferencia clave de contexto**: "lo más importante es que no se carga en el contexto, simplemente se ejecuta el script, obtiene la respuesta" → el skill NO ocupa contexto del modelo (se ejecuta externamente)
3. **MCP = otra forma de comunicación**: "no es un reemplazo, es simplemente otra forma de comunicación" — el protocolo MCP conecta el agente con servicios externos
4. **El agente** (Claude Code, Cursor, VS Code) "no solo puede responderte un texto, sino que puede crear archivos, ejecutar programas, llamar comandos de tu sistema"
5. **Ejemplo**: un script que vive en una carpeta y navega a una API de clima → eso es un skill que el agente ejecuta
6. **Conclusión**: "el tema está en que si..." (cómo elegir cuándo usar cada uno) — los skills son más ligeros (documentos + scripts), los MCPs son protocolos de conexión con servicios

## 🔴 Para el LAB — VALOR: MEDIO-ALTO (aclara el debate que afecta directamente al lab)

| Concepto | En el lab |
|---|---|
| **Skills** (documentos de habilidad, no cargan contexto) | ✅ Hermes skills — EXACTAMENTE esto (SKILL.md + scripts que se ejecutan) |
| **MCPs** (protocolo de conexión con servicios) | ✅ 3 MCPs en producción (lab-db, lancedb, animation-server) |
| **No es reemplazo, es complemento** | ✅ El lab usa AMBOS (skills para procedimientos, MCPs para datos/servicios) |

**La lección clave**: el debate "MCP vs Skills" es falso — **son complementarios**. Skills = procedimientos ligeros (no cargan contexto, se ejecutan). MCPs = conexión con servicios externos (datos, herramientas). El lab ya hace lo correcto: usa skills para procedimientos (verificar_research, gen_video) y MCPs para acceder a datos (lab-db, lancedb).

**Sin futuribles** — el lab ya implementa la respuesta del vídeo. Útil como material para LinkedIn (explicar por qué Hermes usa ambos).

**Conclusión**: validación clara de la arquitectura del lab (skills + MCPs complementarios). El vídeo responde al hype "los MCP mueren" con la realidad: son formas distintas de comunicación, no competidoras.
