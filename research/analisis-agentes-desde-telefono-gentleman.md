---
title: "Análisis — Así controlo mis agentes de IA desde el TELÉFONO (Gentleman Programming, 15-ago-2026)"
type: research
---

# Análisis — Así controlo mis agentes de IA desde el TELÉFONO (Gentleman Programming, 15-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://youtu.be/Yj51wXMwFwE (23 min, Gentleman Programming — 2º vídeo del canal hoy)
**Transcripción:** completa (es)

## Qué monta (stack completo, todo gratis)
1. **SSH server (openssh-server)** en la máquina que corre los agentes (su Vink S9, 24/7)
2. **Tailscale** (red privada mesh) — en vez de abrir el puerto 22 al mundo (bots probando contraseñas). Cero puertos abiertos, acceso con llaves. ⚠️ Pitfall: `tailscale ssh` y SSH normal son cosas distintas — si tailscale ssh está ON, se apropia del puerto 22 y tu llave no vale. `sudo tailscale set --ssh=false`.
3. **Firewall (UFW)** solo por la interfaz tailscale0 → port 22 (no abrir SSH a todo el mundo)
4. **Herder** (multiplexor hecho para agentes) — sesiones con nombre, cada una un servidor persistente; ves qué agente está bloqueado/trabajando/terminó; hooks de notificación
5. **`loginctl enable-linger`** — sin esto, systemd mata los servicios de usuario al cerrar sesión y tras reinicio se cae todo
6. **Moji** (app móvil SSH + notificaciones) — Easy Pair: escanea un QR (token temporal, no mostrar en stream), la llave privada se genera en el teléfono, la pública se instala sola en authorized_keys. Whisper local para dictar. Versión gratis suficiente; Pro 8,49 €/mes o 143 € lifetime.
7. **Privacidad**: transcripts/diffs viajan entre tu máquina y el teléfono; a los servidores de Moji llegan "resúmenes cortitos" para notificaciones — poco pero no cero.

## Las 3 reglas de higiene del autor (lo más valioso)
1. **Las notificaciones tienen horarios** — el teléfono se calla de noche; si un agente termina a las 4, me entero a las 8. "Me da culpa apagarlo, pero el dato puede esperar."
2. **Si me despierto y atiendo, no arranco nada nuevo** — solo el que ya está corriendo.
3. **Para dirigir, no para trabajar** — si estás escribiendo código serio con el pulgar, la planificación falló.

## Frase clave
"La pregunta no es si podés trabajar desde cualquier lado (sí, te lo acabo de mostrar). La pregunta es si vas a dejar de trabajar en algún lado." + "Hemos instalado un demonio cuya única función es despertarte" (3 de la mañana).

## Veredicto para el lab
**VALIDA la arquitectura del lab + 3 aportes concretos:**
- El lab YA tiene el patrón: procesos long-lived + cron + Telegram como superficie de control desde el móvil (Hermes = su "Moji"). La desconexión de sesiones investigada hoy es exactamente este tema.
- **Aporte 1 (Tailscale)**: ya estaba como futurible menor en el backlog — este vídeo muestra el caso de uso real (acceder al PC desde el móvil sin abrir puertos). Sigue siendo futurible, no urgente (el lab no necesita acceso SSH móvil hoy).
- **Aporte 2 (Moji/Herder)**: herramientas de referencia si algún día quiere gestionar agentes desde el móvil con UI dedicada. No accionable ahora (Hermes+Telegram cubre el caso).
- **Aporte 3 (3 reglas de higiene) — SÍ aplicable YA**: para Joseba (misofonía, duerme 23:30, los crons nocturnos del lab) la regla "notificaciones con horario" es oro: el lab ya tiene watchdog, pero conviene revisar que ningún cron moleste de noche.
- **Pitfall técnico nuevo para el lab**: `tailscale ssh` vs SSH normal (si se activa tailscale en el futuro). Y `loginctl enable-linger` si se montan servicios de usuario persistentes.

**NO accionable ahora** (todo el stack móvil) — el lab ya controla agentes desde el teléfono vía Telegram; no hace falta Moji. Se archiva como referencia para cuando haya una necesidad real de acceso móvil directo.
