---
title: "Análisis — \"HOW TO CREATE A WEB AGENT\" (erandikoko_uda / @codecraftman, 01-sep-2026)"
type: research
---

# Análisis — "HOW TO CREATE A WEB AGENT" (erandikoko_uda / @codecraftman, 01-sep-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://www.instagram.com/reel/Dcu0OujMX-B/ (erandikoko_uda, hace 1h, reel educativo)
**Método:** el reel NO era accesible por browser (restricción de audiencia de la cuenta — Instagram devuelve "la cuenta ha establecido límites"); el usuario envió captura del móvil (imagen cache img_754c03a47145.jpg) → análisis sobre el contenido REAL de la captura, no inventado.

## Contenido (transcrito de la captura)

**Tesis**: un Web Agent = **LLM + Browser + Tools + Memory + Agent Loop**.

**Arquitectura (diagrama del post)**:
```
User Goal → LLM → Decide Action → Browser Tool → Website → Observe Result → Decide Next Action → (repeat) → Complete Task
```

**Componentes**:
- LLM: razonamiento y decisión
- Tools: buscar, hacer clic, escribir, extraer datos
- Memory/State: decide siguientes acciones; controla tareas de riesgo
- Agent Loop: determina qué hacer a continuación (repite)

**Ejemplo**: "Find the best laptop under $60,000" → abrir web → buscar → filtrar precio → leer detalles → comparar → elegir mejor opción

**⚠️ Nota de seguridad clave (textual del post)**: *"Don't give an agent unrestricted browser access. Interact with websites and require human approval for sensitive actions such as purchases, form submissions, or sending messages."*

**Key idea**: LLM + Browser + Tools + Memory = Agent Loop = WEB AGENT
**Hashtags**: #webagent #AIagents #Agentic #AIEngineering

## 🔴 Aplicación al LAB — VALOR MEDIO

| Ángulo | Veredicto |
|---|---|
| **El lab ES un web agent** | 🟢 Hermes ya implementa exactamente esta arquitectura: LLM + toolsets (browser, terminal, web) + memoria persistente + loop de acciones (run_conversation: LLM → tool_calls → observar → repetir). El diagrama del post = el loop real del lab |
| **⚠️ Nota de seguridad del post** | 🟢🟢 **VALIDACIÓN DIRECTA de la política del lab**: "no dar acceso irrestricto al navegador + aprobación humana para acciones sensibles" = exactamente lo que el lab hace con `approvals.mode: smart` + tirith + gates de veracidad + least-privilege-lab. 3ª validación externa del principio (tras Emowe y Fazt) |
| **Memory/State para controlar tareas de riesgo** | 🟢 Coincide con el memory + gates del lab |
| **Ejemplo de compra** | ⚪ El lab NO hace compras — pero el principio "acciones sensibles requieren aprobación" es el mismo que el gate de verificación de fidelidad y los approvals smart |
| **Futurible** | ⚪ Nada nuevo — el lab ya tiene browser toolset operativo (usado en barridos IG, Emowe, etc.) |

**Conclusión**: sin futuribles, sin cambios — el post es una **validación más (3ª externa esta semana) del diseño del lab como agente web con seguridad por diseño** (aprobación humana para acciones sensibles). Material conceptual para LinkedIn Lab (mismo tema que el PRD graph: el agente coordina, el humano aprueba). El único matiz: el post menciona "sending messages" como acción sensible — en el lab, el envío a canales está controlado por el flujo (nunca automático sin confirmación), coherente.

**Nota metodológica**: análisis basado en captura del usuario (contenido real, transcrito por visión); el reel original no era accesible por restricción de audiencia de la cuenta (verificado con browser, 2 intentos + embed).
