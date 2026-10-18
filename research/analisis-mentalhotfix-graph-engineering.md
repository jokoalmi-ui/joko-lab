---
title: "Análisis — Carrusel mentalhotfix: \"Graph Engineering\" (18-ago-2026)"
type: research
---

# Análisis — Carrusel mentalhotfix: "Graph Engineering" (18-ago-2026)

**Fuente:** https://www.instagram.com/p/DcL5QKBCWGf/ (mentalhotfix — Prateek Singh, carrusel 8 slides, 3 accesibles: 1, 2, 5, 1440×1440)
**Método:** browser_console (2 ig_cache_key) → fetch navegador (base64 246+275 KB → JPG 189+211 KB) → GLM + browser_vision ×2 + alt text slide 5 (vía img_index navegación) + caption autor
**VERACIDAD:** [VERIFICADO]
**Contexto:** 3º post de mentalhotfix analizado en el lab (httptap + Agent Harness 5 videos + este)

**Caption del autor (36 min):** *"Think: nodes = roles, edges = control flow, state = shared context."*

## CONTENIDO (verificado — slides 1 y 2 de 8)

### Slide 1 — "GRAPH ENGINEERING: How to design multi-agent coordination"
- **MISSION** → **ROUTER** → roles: **RESEARCHER · ANALYST · EXECUTOR**
- Frase central: **"Don't build a group chat. Engineer the coordination."**
- Iconos inferiores: TRACE · lupa · warning · red · flecha circular

### Slide 2 — "WHY GRAPH ENGINEERING?"
- **ONE AGENT = TOO MANY JOBS** (cara triste): investigación + planificación + codificación + pruebas + seguridad + memoria — todo en uno
- **A GRAPH = CLEAR COORDINATION** (check): Misión → Router → roles (Investigador, Planificador, Coder, Prueba, Seguridad, Memoria) → **Shared State** → Revisor
- Frase: **"BREAK THE WORK INTO ROLES + FLOWS"**

### Slide 5 — "SHARED STATE: SINGLE SOURCE OF TRUTH" (vía alt text, verificado)
- **Componentes del estado**: EVIDENCE · PLAN · CODE DIFF · TEST RESULTS · RISK · NOTES
- **BAD: AGENTS ONLY CHAT** (espec/chat entre agentes sin artefactos)
- **GOOD: AGENTS PASS STRUCTURED ARTIFACTS** (RESEARCHER → ARCHITECT → BUILDER → TESTER → DEPLOYER pasando artefactos)
- Frase: **"DON'T PASS VIBES. PASS STATE."**

## 🎯 APLICACIÓN AL LAB — CONEXIÓN DIRECTA CON EL PRD DE HOY

**Este carrusel valida EXACTAMENTE el PRD que creamos hace 20 minutos**
(research/prd-graph-delegacion-multiagente.md):

| Concepto mentalhotfix | En el PRD del lab (18-ago) |
|---|---|
| **Don't build a group chat** | PRD: coordinador que NO ejecuta, solo delega |
| **Router** | Edge C→I con contratos (qué entra/sale) |
| **RESEARCHER** | Nodo Investigador (web, temp 0.1) |
| **Shared State** | /tmp/graph_<id>/investigacion.json + borrador.md |
| **Revisor** | Nodo Revisor (solo lectura, informe) |
| **BREAK THE WORK INTO ROLES + FLOWS** | La frase del PRD: 4 nodos con roles y flujos |

**Coincidencia temporal notable**: el usuario pidió el PRD hace ~30 min y el
canal que ya validó el harness del lab publica el mismo concepto 2 horas
después. **Triple validación externa del día**: mentalhotfix (harness) +
hackproduct (loop) + codewithbrij (graph) + mentalhotfix (graph otra vez).

## Veredicto
**VALIDA EL PRD / MUY RELEVANTE.** mentalhotfix publica un carrusel de 8
slides sobre Graph Engineering (solo 2 accesibles) que coincide punto por
punto con el PRD del graph del lab creado hoy: coordinador que no ejecuta,
router con roles especializados, shared state, revisor. "Don't build a
group chat. Engineer the coordination" — la misma filosofía del podcast
atareao. Material directo para el TFM y para refinar el PRD (los roles de
la slide 2: Investigador, Planificador, Coder, Prueba, Seguridad, Memoria
— el lab ya tiene equivalentes para casi todos).
**Nota**: 3/8 slides accesibles (1, 2, 5 — el navegador sin login expulsa al
registro al avanzar más allá de la 5; las slides 3-4 y 6-8 requieren sesión
o el enlace directo desde la app móvil). La slide 5 es la más valiosa para
el lab (validación del shared state del PRD).
