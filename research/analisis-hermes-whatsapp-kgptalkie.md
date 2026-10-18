---
title: "Análisis — Hermes Agent WhatsApp Setup (KGP Talkie, 15-ago-2026)"
type: research
---

# Análisis — Hermes Agent WhatsApp Setup (KGP Talkie, 15-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://youtu.be/qnJGT0w-xn4 (KGP Talkie, ~10 min, inglés)
**Transcripción:** completa (en)

## Qué muestra el vídeo
Tutorial de conexión de **WhatsApp a Hermes Agent** para controlarlo desde el móvil:

1. `hermes gateway setup` → seleccionar WhatsApp (opción 4)
2. **Modo bot (número dedicado)** vs **número personal** (preferido: bot)
3. Añadir número autorizado (con código de país: +34 para Joseba) — solo esos números pueden hablar con el agente
4. Instala **WhatsApp Breeze** automáticamente → QR → escanear → pairing completado
5. Reiniciar gateway → WhatsApp conectado (blue dot en mensajería)
6. Enviar "hi" / peticiones desde el móvil → el agente responde con web_search

## Lo más interesante (no el setup)
**Prueba de "self-improving agent"**: al pedir "latest stock market news", el agente respondió Y ADEMÁS **patcheó su propio skill.md** con lo aprendido (skill "wave research alternatives") — auto-mejora real visible en logs.

## Veredicto para el lab
**REDUNDANTE + 1 CONFIRMACIÓN ÚTIL:**

### Redundante
- Joseba YA controla Hermes desde el móvil vía **Telegram** (esta misma conversación). WhatsApp sería un canal duplicado sin ventaja nueva.
- El patrón "controlar agente desde el móvil" ya fue validado con el vídeo de Gentleman Programming (agentes desde el teléfono — analizado hoy).

### Confirmación útil
- **El auto-mejora de skills es REAL y está en producción**: el vídeo muestra a Hermes parcheando su skill.md automáticamente tras una tarea — exactamente el comportamiento que el lab ya usa (skill_manage patch después de tareas difíciles, como se hizo hoy con los análisis).

### Dato práctico menor
- Si algún día Joseba quisiera WhatsApp: número de país +34, modo bot preferido, acceso restringido a su número. Pero Telegram ya cubre el caso.

## Registro
- Guardado: research/analisis-hermes-whatsapp-kgptalkie.md
- Decisión: NO accionable — no añadir WhatsApp al lab (redundante con Telegram).
