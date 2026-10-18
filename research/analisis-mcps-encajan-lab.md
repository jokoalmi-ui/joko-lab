---
title: "Análisis — ¿Qué MCPs encajarían en el LAB? (18-ago-2026)"
type: research
---

# Análisis — ¿Qué MCPs encajarían en el LAB? (18-ago-2026)
**VERACIDAD:** [VERIFICADO]

**Petición:** «Ahora mismo para investigación tenemos un modelo para ello,
investiga qué MCP encajarían en nuestro LAB»
**Método:** investigación EN SESIÓN (regla definitiva del graph — 9 búsquedas
web reales, fuentes verificadas por URL)
**Regla de filtrado aplicada (DataStreak):** herramientas/datos → MCP ·
know-how → Skill. Hermes ya cubre nativo muchas cosas → NO duplicar.

---

## VEREDICTO POR CANDIDATO (ordenado por encaje real)

### 🥇 PRIORIDAD 1 — MCP SQLite para las BD PROPIAS (perfume-ia, café-ia)
- **Qué:** MCP server SQLite (oficial `modelcontextprotocol/servers` → sqlite,
  o `madnh/mcp-server-sqlite` / `jparkerweb/mcp-sqlite`, Python, PyPI)
- **Por qué encaja:** el lab tiene BD SQLite propias: perfume-ia
  (`~/perfume-ia/data/coleccion.db`, 320 botellas) y café-ia
  (`~/cafe-ia/data/cafes.db`). Exponerlas como MCP = el futurible
  «MCP-BD» que YA estaba anotado en backlog (arquitectura, no rendimiento).
  El agente consultaría las BD con tools MCP en vez de scripts ad-hoc.
- **Coste:** 0 €, local, ~15-30 min de setup. **Riesgo:** mínimo (solo
  lectura al principio; escritura con contraseña/permitir solo lo necesario).
- **Fuentes:** https://github.com/modelcontextprotocol/servers ·
  https://pypi.org/project/mcp-server-sqlite/ · https://mcpservers.org/servers/panasenco/mcp-sqlite

### 🥈 PRIORIDAD 2 — n8n-MCP (gestión de workflows desde Hermes)
- **Qué:** `czlonkowski/n8n-mcp` — puente entre n8n y modelos de IA:
  listar/crear/actualizar/validar workflows de n8n vía MCP.
- **Por qué encaja:** el lab TIENE n8n en Docker (stack principal). Hermes
  podría crear/gestionar workflows por instrucción en lenguaje natural.
- **⚠️ CONDICIÓN:** n8n es ZONA PROTEGIDA. Cualquier integración exigiría:
  (1) confirmación explícita del usuario, (2) empezar SOLO lectura
  (listar/inspeccionar), (3) crear workflows con revisión humana antes de
  activarlos. Alternativa de menor riesgo: el MCP Server TRIGGER de n8n
  (exponer workflows EXISTENTES como tools MCP — lectura de resultado).
- **Fuentes:** https://github.com/czlonkowski/n8n-mcp · https://www.n8n-mcp.com/ ·
  https://guguroboticsreporter.medium.com/n8n-mcp-server-triggers-expose-workflows-as-ai-tools-for-ai-hackathons-85cb99dfee06

### 🥉 CON SEÑAL — Google Workspace MCP OFICIAL (futurible confirmado «Si»)
- **Qué:** MCP servers oficiales de Google (Gmail, Drive, Docs, Sheets,
  Slides, Calendar, Chat) — guía oficial en developers.google.com.
- **Por qué encaja:** futurible confirmado por el usuario (18-ago: «MCP que
  conecta con Google AI Studio y todo el ecosistema, para gestionar y crear,
  no solo lectura»). Con least-privilege: LECTURA primero.
- **Señal de activación:** una tarea concreta que exija Google (p.ej.
  gestionar el correo/Drive del TFM o del empleo) — NO instalarlo sin esa
  tarea (coste de OAuth + mantenimiento).
- **Fuentes:** https://developers.google.com/workspace/guides/configure-mcp-servers ·
  https://github.com/xing5/mcp-google-sheets · https://github.com/a-bonus/google-docs-mcp

### ❌ RECHAZADOS con motivo (3 puntos cada uno)

**Filesystem MCP (oficial):** (1) coste: setup + permisos adicionales;
(2) beneficio: NULO — Hermes ya tiene read_file/write_file/search_files
nativos; (3) timing: no aporta nada nuevo. → NO.

**Telegram MCP (Telethon/MTProto):** (1) coste: exponer cuenta personal de
Telegram a un MCP = riesgo de seguridad alto (MTProto, ban risk del número);
(2) beneficio: duplica el gateway de Telegram que Hermes YA tiene conectado
(este chat es prueba); (3) timing: la única ventaja (leer chats donde no
está el bot, p.ej. Skool/DECODE) no justifica el riesgo. → NO.

**Obsidian MCP:** (1) coste: medio (plugin/REST API + config);
(2) beneficio: el lab ya tiene research/ en markdown y skills obsidian;
depende de cuánto uses el vault real; (3) timing: sin tarea concreta de
vault → diferir hasta que haya una. → DIFERIDO.

---

## RESUMEN ACCIONABLE

| MCP | Encaje | Acción | Señal |
|---|---|---|---|
| **SQLite propio** (perfume-ia, café-ia) | ALTO | ⚡ Instalar (solo lectura) | Listo ahora |
| **n8n-MCP** | MEDIO-ALTO | 🛡️ Con condiciones (zona protegida) | Confirmación + solo lectura |
| **Google Workspace oficial** | MEDIO | ⏸️ Futurible confirmado | Tarea concreta con Google |
| Filesystem | BAJO | ❌ Rechazado (nativo) | — |
| Telegram | BAJO | ❌ Rechazado (riesgo) | — |
| Obsidian | MEDIO | ⏸️ Diferido | Tarea concreta de vault |

**Recomendación inmediata:** el MCP SQLite para las BD propias es el que más
valor da por menor coste — conecta con el futurible ya anotado y con la
directiva «primero tareas que mejoren LAB». n8n-MCP solo con confirmación
explícita y modo lectura.

**Etiqueta:** [VERIFICADO] (fuentes reales, URLs vistas en búsquedas)
