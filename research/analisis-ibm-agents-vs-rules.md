---
title: "Análisis — AI Agents vs Business Rules (IBM Technology, 21-ago-2026)"
type: research
---

# Análisis — AI Agents vs Business Rules (IBM Technology, 21-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://youtu.be/i1ZmNUbRGD4 (IBM Technology, 20-08-2026, 10:25)
**Método:** transcripción EN completa (yt-dlp auto-subs, 23.5K chars, dedup parcial)

## Tesis del vídeo (IBM)
- **Business rules** (motores de reglas): deterministas, lógica escrita por humanos,
  condiciones+acción. Ventajas: sin coste de inferencia, unit-testable, explicables
  para auditorías ("la regla procesada ES la explicación"), baratas y rápidas.
- **AI agents**: probabilísticos (predicen tokens desde patrones), trabajan con objetivo
  + contexto + tools, generalizan a casos NO anticipados y datos sucios/no estructurados.
- **NO se sustituyen — se combinan en híbrido**:
  1. **Reglas primero** (baratas): cubren el 80-90% de casos claros → decisión directa
  2. **Escalar al agente** solo cuando: datos sucios (texto libre/foto) o juicio necesario
  3. **Guardrails deterministas DESPUÉS del agente**: validan su recomendación
  4. **Human-in-the-loop** para umbrales de alto riesgo (por encima de X → revisión humana)

## 🔴 Para el LAB — VEREDICTO: MEDIO (validación al 100% de la arquitectura)

| Patrón del vídeo | Implementación real en el lab |
|---|---|
| Reglas primero (deterministas, baratas) | ✅ `verificar_research.py`, checklists, gate de veracidad, crons `no_agent` (watchdogs) |
| Escalar al agente solo con datos sucios/juicio | ✅ RAG + gate + revisor solo cuando la tarea lo requiere |
| Guardrails tras el agente | ✅ Revisor en sesión + verificación de salida (regla 15: salida literal o "no verificado") |
| Human-in-the-loop para alto riesgo | ✅ Confirmación explícita del usuario (acciones sensibles, n8n, sudo, borrados) |
| "Regla procesada = explicación" | ✅ Mismo principio en el gate: datos verificables, no opinión |
| Reglas sin coste de inferencia | ✅ Watchdogs no_agent (0 tokens) — EXACTO |

**Sin futuribles nuevos.** IBM valida con autoridad industrial el diseño que el lab ya tiene:
determinismo primero, agente solo cuando hace falta, guardrails y humano al final.
Útil como cita/vocabulario para LinkedIn/TFM ("híbrido reglas+agentes", "guardrails
deterministas", "human-in-the-loop").

*Nota: transcripción auto-subs con triplicación (dedup parcial) — contenido inequívoco.*
