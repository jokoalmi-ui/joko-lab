# Análisis: "MCPs para LLM muy pequeños" (Nichonauta — Context 7 + Playwright)
**VERACIDAD:** [VERIFICADO]

**Fuente**: https://youtu.be/MeipNmJyWg0 · Nichonauta · 24-ago-2026 (liberado al público)
**Estado backlog**: [PENDIENTE 24-ago → ANALIZADO 03-sep cuando se liberó]
**Serie**: video previo = LLMs 2B/4B en llama.cpp para OpenCode; este = MCPs;
siguiente = Atomic AI (Proxy Atómico, ya analizado `analisis-proxy-atomico.md`)

## Qué hace el vídeo (transcripción completa verificada)

Contexto: Nichonauta desarrolla con **Qwen 3.5 2B y Gemma 4 E2B** en llama.cpp
(Q4, 1.28 GB) dentro de **OpenCode**. Descubrimiento: modelos pequeños tienen
habilidades pero NO conocimiento (ignoran versiones reales de librerías, APIs,
Bootstrap 5.3.3 etc). Su serie busca cerrar esa brecha con herramientas.

### Dos MCPs instalados en opencode.json
1. **Context7 MCP** (`npx` local): permite al LLM **consultar documentación
   actualizada** de librerías/packages → deja de alucinar APIs o dar versiones
   antiguas. No es que el modelo sepa más: es que puede consultar.
2. **Playwright MCP**: el modelo **usa el navegador él mismo** para probar su
   propio código (abrir web, verificar, leer consola).

Config clave en opencode.json: pedir permiso antes de editar/ejecutar (control
humano sobre acciones del modelo).

### Pruebas reales mostradas
- Bootstrap: detectó 5.3.3 en el HTML → Context7: la reciente es 5.3.8 ✓
- Bootstrap Icons: el modelo "actualizó" a 1.11.4 por su cuenta (inventado) y
  luego Context7 corrigió → resultado confuso (el propio Nichonauta lo muestra
  como límite del modelo pequeño, no del MCP)
- Playwright: abrió nichonauta.com, lanzó servidor :8001, entró al proyecto y
  **detectó errores de consola** (favicon ausente + error de sintaxis en main.js)
- Fallo Windows/Linux resuelto solo (probó `con` → `ls` → PowerShell) — resiliencia
  del modelo, no bug

### Veredicto del propio autor (clave)
"Un modelo pequeño no únicamente le bastan MCPs — aunque tenga la información
puede no entenderla o ni siquiera entender cómo usar el MCP." → la solución final
de su serie es **Atomic AI** (proxy atómico que descompone tareas; el vídeo del
10-ago ya analizado en el lab).

## Relevancia para el lab

**ALTA — validación + 1 candidato MCP concreto.**

- El lab opera **OpenCode con deepseek cloud** y tiene registrado que el local
  r1-14b es INUSABLE para coding (ctx 64K). El vídeo prueba la ruta contraria:
  modelos MUY pequeños (2B Q4) + MCPs de contexto = usable para tareas acotadas.
  Confirma la decisión del lab de no usar locales pequeños para coding real.
- El lab **ya tiene 3 MCPs** (lab-db, lancedb, animation-server) y skill mcp-lab
  para evaluar candidatos. Context7 (docs actualizadas de librerías) ataca un
  problema REAL del lab: modelos con cutoff de conocimiento usando librerías
  que cambian. Candidato razonable de evaluación futura para OpenCode + deepseek.
- Playwright MCP = el lab ya cubre navegación con browser tools/chrome-lab →
  NO añade capacidad nueva (duplicado funcional).
- Atomic AI (siguiente de la serie): ya analizado en el lab (10-ago) con valor
  señalado como futurible para orquestación.

## Decisión

- **VALIDACIÓN** del enfoque (MCPs de contexto para modelos con cutoff) — no
  requiere acción.
- **Futurible suave**: evaluar Context7 MCP en el lab cuando toque revisar
  MCPs (skill mcp-lab) — coste ~0, valor = menos alucinaciones de versiones/APIs
  en coding con OpenCode.
- NO a Playwright MCP (duplicado de browser tools).

## Notas de proceso
- Patrón confirmado: los vídeos members-only de Nichonauta se liberan en días
  (Proxy Atómico: 1 día; este: ~10 días). La estrategia "registrar pendiente y
  revisar al liberarse" funciona — el usuario la activó el 03-sep para los 2
  pendientes históricos. Proxy Atómico ya estaba analizado (10-ago); este era el
  único pendiente real.
