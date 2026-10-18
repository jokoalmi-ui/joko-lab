---
title: "Análisis — Intercambiar Modelos en llama.cpp (Nichonauta, 21-ago-2026)"
type: research
---

# Análisis — Intercambiar Modelos en llama.cpp (Nichonauta, 21-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://youtu.be/d1RgwB378Sg (Nichonauta, 20-08-2026, 3:38)
**Método:** transcripción ES completa (yt-dlp auto-subs, 9.4K chars, dedup parcial — auto-subs triplicadas)

## Qué propone el vídeo
Configurar **llama.cpp** con un único archivo `presets.ini` que contiene los ajustes de ejecución
de varios modelos (globales + específicos por modelo) y un `llama.cpp.bat` que lanza
`llama-server` en el puerto 8080 con `models autoload`. Resultado: la interfaz web de
llama.cpp permite **intercambiar entre modelos sin abrir/cerrar procesos**, vaciar la memoria
de uno antes de cargar otro, y añadir tantos modelos como se quiera.

- Modelos del vídeo: **Gemma 4 2B** y **Qwen 3.5 2B** (los del día a día de Nichonauta)
- Elimina la necesidad de utilidades externas de swap (menciona "Yamas Swap")
- Guarda los `.bat` originales como respaldo
- Siguiente vídeo prometido: usar estos modelos dentro de OpenCode con visión + contexto

## 🔴 Para el LAB — VEREDICTO: BAJO (ya resuelto con LM Studio)

| Aspecto | Veredicto |
|---|---|
| "Intercambiar modelos sin reiniciar" | ✅ **El lab YA lo hace con LM Studio**: `lms load` / `lms unload` / API `v0/models` (validado hoy mismo: gpt-oss → GLM) |
| `presets.ini` con ajustes por modelo | ⚪ Equivalente en LM Studio: el panel de "Server" + configs por modelo; el lab ya gestiona esto |
| Puertos/scripts .bat | ❌ No aplica (Linux, no Windows) |
| Gemma 4 2B + Qwen 3.5 2B | ✅ Ya conocidos (Nichonauta 20-ago: 173/136 tok/s; Gemma = candidato batch futuro del lab) |

**Sin futuribles nuevos.** Es una serie coherente del canal (modelos pequeños + iteración),
pero este vídeo concreto resuelve un problema que el lab ya tiene resuelto con LM Studio
headless + `lms`. La señal real del canal sigue siendo la misma: optimizar el ENTORNO,
no cambiar de modelo.

*Nota: transcripción auto-subs con triplicación (el dedup no fue perfecto) pero el contenido
técnico es inequívoco. Canal validado por el usuario como interesante y alineado.*
