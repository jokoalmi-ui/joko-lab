---
title: "Análisis — n8n MCP para Claude: agentes con un prompt (Michele Torti, 22-ago-2026)"
type: research
---

# Análisis — n8n MCP para Claude: agentes con un prompt (Michele Torti, 22-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://youtu.be/g8TwasIoC3Q (Michele Torti, 28-09-2025, 16:05 min)
**Método:** subtítulos EN descargados (182 KB) + extracción de fragmentos clave

## Contenido: el MCP oficial de n8n
- **n8n lanzó su MCP oficial**: permite a Claude (Desktop) **crear workflows de n8n end-to-end desde un solo prompt**
- **Setup paso a paso**:
  1. Instalar **Claude Desktop**
  2. Instalar **NodeJS**
  3. Configurar el **MCP de n8n** con 2 datos: **n8n API URL + API Key** (claves para que Claude hable con tu instancia)
  4. Añadir al config de Claude Desktop → verificar que el MCP server está corriendo
  5. Conectar credenciales (Slack, OpenAI, etc.)
- **Limitación**: los proyectos en n8n requieren plan de pago (en free plan hay límites)
- La metáfora: Claude = el asistente (input), MCP = hub que conecta con apps (Gmail, Slack, docs, n8n), y el agente toma acción según tu petición

## 🔴 Para el LAB — VALOR: MEDIO (el lab TIENE n8n + puede probar el MCP oficial)

| Aspecto | Análisis |
|---|---|
| n8n en el lab | ✅ Stack principal (`automation-stack`, workflow ENVIO WHATSAPP) — n8n self-hosted |
| MCP oficial de n8n | ⚪ NO probado aún — el MCP conectaría un agente (Claude/Hermes) a la instancia n8n del lab |
| ¿Claude Desktop? | ❌ No es el flujo del lab (Hermes es el agente, no Claude Desktop) |
| ¿Aplicable con Hermes? | ⚪ El MCP de n8n es un servidor MCP estándar → **podría conectarse a Hermes** igual que los otros 3 MCPs |

**Futurible MEDIO (documentado)**: conectar el **MCP oficial de n8n a Hermes** para que Hermes pueda crear/modificar workflows de n8n desde Telegram (en vez de hacerlo a mano en la UI). Señal de activación: cuando haya que crear workflows n8n con frecuencia. Hoy el lab solo tiene 1 workflow activo (ENVIO WHATSAPP) — no justifica el setup aún.

**Conclusión**: el vídeo demuestra el MCP oficial de n8n (útil y potente), pero el lab no necesita Claude Desktop (ya tiene Hermes como agente). El futurible real es conectar ese MCP a Hermes cuando se necesite automatizar la creación de workflows n8n. Referencia anotada.
