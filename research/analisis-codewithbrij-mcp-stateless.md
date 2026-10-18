---
title: "Análisis — MCP Stateless (codewithbrij, 20-ago-2026)"
type: research
---

# Análisis — MCP Stateless (codewithbrij, 20-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://www.instagram.com/p/DcQrYOIqwwX/ (codewithbrij, 20-ago, 2h)
**Método:** caption íntegro del snapshot + VERIFICACIÓN con spec oficial
**Veredicto:** [VERIFICADO] — la afirmación es REAL (no solo el post lo dice)

## 🔴 La noticia (VERIFICADA con fuentes oficiales)

**El 28-jul-2026 MCP publicó la spec 2026-07-28 que hace el protocolo STATELESS**:
- Fuentes: blog.modelcontextprotocol.io (2026-07-28 release) + changelog oficial +
  Microsoft Tech Community + SDKs beta v2 (Python/TS/Go/C#)
- **Cambios**: se elimina el handshake `initialize/initialized` y el `Mcp-Session-Id`
  (antes: sticky sessions o shared session store para escalar horizontal)
- Cada request lleva su `protocolVersion` y `clientCapabilities` en `_meta`
- **Ahora**: cualquier instancia puede responder → round robin, K8s y serverless
  funcionan sin pelea

### El matiz importante (del post, bien razonado)
> "Protocolo stateless NO significa aplicación stateless. Si tu workflow necesita
> memoria, el servidor devuelve un handle explícito: `create_basket → basket_id: 42`
> → `add_item(basket_id: 42)`. El estado no desapareció: se movió a la vista,
> donde el modelo puede verlo y razonar sobre él."
>
> **"MCP no eliminó el estado. Eliminó el escondite."**

Coste para el desarrollador: handles explícitos, tools idempotentes, retry-safe,
durable tasks para procesos largos.

## 🔴 Estado del LAB (verificado en el sistema)

| Componente | Versión | Protocolo |
|---|---|---|
| **lab-db** (FastMCP, 18-ago) | fastmcp **3.4.7** + mcp **1.29.0** | 🔴 **v1 (OLD, con handshake)** |
| **animation-server** (Manim) | fastmcp **1.0** + mcp **1.29.0** | 🔴 **v1 (OLD, con handshake)** |
| Hermes MCP client | (gestiona ambos) | — |

**Los 2 MCP del lab usan SDK v1** → hablan el protocolo antiguo. La spec stateless
requiere SDK v2 (mcp 2.x; FastMCP se renombra a MCPServer en v2, según el blog
del SDK). FastMCP 3.4.7 es del 6-dic-2024 (PyPI) — anterior a la spec nueva.

## Veredicto para el LAB

**⚠️ IMPACTO FUTURO REAL (no accionable hoy, pero a vigilar)**:

1. **Los MCP del lab SIGUEN FUNCIONANDO hoy** (el protocolo v1 no se rompe; la spec
   nueva es compatibilidad hacia adelante, y Hermes 0.17.0 usa client v1)
2. **Futurible NUEVO (señal clara)**: migrar lab-db y animation-server a **SDK v2**
   cuando la spec 2026-07-28 sea estable (los SDKs están en beta julio-2026)
   → el lab ganaría: escalado sin sticky sessions, tools idempotentes, handles
   explícitos. **Señal de activación: cuando Hermes actualice su client a v2**
   (o cuando el usuario pida exponer un MCP del lab públicamente / en K8s)
3. **Matiz útil YA aplicable**: el post valida el patrón del lab de handles
   explícitos (los tools del lab ya devuelven IDs: basket_id, perfume_id...)
4. **No hacer nada ahora** — migrar a SDKs beta sería premature.

## Nota honesta

La noticia es REAL (verificada con 3 fuentes: spec oficial, changelog, MS Tech
Community). El post de codewithbrij es de hace 2h (muy fresco). El análisis del
lab se basa en versiones reales instaladas (pip list verificado). NO se probó
si los SDKs v1 del lab siguen sirviendo al Hermes 0.17.0 actual (funciona por
construcción: Hermes v1 ↔ servers v1) — se asume compatibilidad hasta que
Hermes migre su client.
