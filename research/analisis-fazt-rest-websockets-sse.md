---
title: "Análisis — REST API vs WebSockets vs SSE (Fazt Code, 20-ago-2026)"
type: research
---

# Análisis — REST API vs WebSockets vs SSE (Fazt Code, 20-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://youtu.be/UYRwN9v9pi4 (Fazt Code, 19-08-2026, 22:40)
**Método:** transcripción ES (yt-dlp auto-subs, VTT limpio + dedup, ~29.7K chars)
**Veredicto:** [VERIFICADO]

## VALOR REAL: BAJO-MEDIO (fundamentos, 1 futurible menor)

Contenido de fundamentos de arquitectura web (cliente-servidor) — el lab ya usa
REST (Flask :5000, proxy :9911, LM Studio :1234) y no tiene apps de tiempo real.
NO es accionable hoy; aporta 1 dato reutilizable (SSE para el dashboard del
monitor LM Studio en vez de polling) y refuerza el criterio de elección.

---

## Contenido (resumen fiel)

### REST API (la base, ~90% de internet)
- Arquitectura cliente-servidor: el cliente SIEMPRE inicia la petición (GET/POST/PUT/DELETE)
- Protocolo HTTP · respuesta en JSON
- **Límite**: no hay tiempo real — si otro cliente modifica datos, los demás no se enteran sin refrescar

### Long Polling (la solución antigua de Gmail)
- El cliente pregunta al servidor cada X segundos si hay cambios
- **Problema**: satura el servidor con peticiones inútiles y los cambios se ven con retraso (intervalo)

### WebSockets (comunicación bidireccional)
- Cliente y servidor mantienen un canal ABIERTO: cualquiera de los dos puede enviar/recibir
- **Ideal para**: chats, tableros colaborativos (su demo: 4 navegadores sincronizados al instante)
- **Coste**: conexión persistente, más pesado de lo necesario si solo necesitas push del servidor

### SSE (Server-Side Events — "la mitad del websocket")
- Push UNIDIRECCIONAL: el servidor notifica al cliente, el cliente no responde
- **Ideal para**: notificaciones, feeds de actividad, respuestas streaming de IA, errores del servidor
- **Clave del vídeo**: "SSE + REST cubren casi toda la comunicación bidireccional que necesitas — mucho más común que websockets"

### GraphQL (mención final)
- No es por la comunicación sino por la FORMA de responder: envía SOLO los datos pedidos
- **Ideal para**: móviles/APIs con ancho de banda limitado

## 🔴 Conexión con el LAB

| Aspecto | Estado |
|---|---|
| REST (Flask :5000, proxy :9911, LM Studio :1234) | ✅ El lab es 100% REST hoy — correcto para su escala |
| **SSE para el monitor LM Studio** | 🟡 **Futurible MENOR**: el dashboard Flask :5000 actualiza con polling; SSE daría actualizaciones de VRAM/temperatura en vivo sin refrescar. Señal: cuando el monitor se use de forma continua en pantalla |
| Websockets | ❌ No aplica (sin apps colaborativas/chat) |
| GraphQL | ❌ No aplica (sin clientes móviles) |
| "SSE + REST = casi todo" | ✅ Regla útil si el lab construye dashboards en vivo |

## Veredicto honesto

**Valor bajo-medio.** Es un curso de fundamentos bien explicado (útil si el usuario
aprende arquitectura web para su TFM/LinkedIn), pero para el lab: solo 1 futurible
menor (SSE en el monitor) y validación de que la arquitectura REST actual es la
correcta. El canal (Fazt Code) es formativo, no de nicho — el contenido no cambia
ninguna decisión del lab hoy.

## Nota honesta

Transcripción auto-subs ES (con anuncio de sponsor de hosting al inicio — ignorado).
No se descargó el vídeo (solo transcripción): las demos son de tablero Kanban con
Playwright CLI (4 navegadores) — la demo con agentes de IA es lo único destacable
a nivel práctico (usar Playwright para simular N clientes en una app realtime).
