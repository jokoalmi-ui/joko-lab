---
title: "Análisis — Air LLM: modelos gigantes con 4 GB VRAM (Dev Knives, 21-ago-2026)"
type: research
---

# Análisis — Air LLM: modelos gigantes con 4 GB VRAM (Dev Knives, 21-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://youtu.be/-6I52TK654g (Dev Knives, 20-08-2026, 12:58)
**Método:** transcripción ES completa (yt-dlp auto-subs, 35.6K chars, dedup parcial)

## Qué es Air LLM
Librería open source que ejecuta modelos gigantes con poca VRAM mediante
**carga secuencial de capas**: carga capa 1 → ejecuta → borra → carga capa 2...
En vez de cargar el modelo completo (que requiere 48 GB para un 70B), solo hay
una capa en VRAM a la vez → se depende del tamaño de CADA CAPA, no del modelo.
Para arquitecturas MoE (Qwen 3), además solo carga el experto que necesita.

**Clave**: NO cuantiza → NO pierde calidad (misma inteligencia, solo más lento).

## Prueba real (Dev Knives, RTX 5080 16 GB)
- Modelo: **Qwen 3 32B a 4 bits**
- Carga: 4.5 segundos ✅
- Respuesta (5 tokens limitados): **251 segundos = 4.5 minutos** ⚠️
- Medición: **1-3 tok/s** con SSD bueno; una frase normal = 30 min; un resumen
  complejo = "un día entero ejecutándose"

## Veredicto de Dev Knives
"Tiene más contras que pros": la velocidad es el punto negativo (nada paraleliza).
**NO sirve para chat ni para programar** — solo para experimentar o como avance
técnico hacia el futuro (correr modelos top sin PC tope de gama).

## 🔴 Para el LAB — VEREDICTO: BAJO (no accionable, valida la decisión del lab)

| Aspecto | Veredicto |
|---|---|
| Velocidad (1-3 tok/s) | ❌ Inaceptable para el uso del lab (interactivo, batch, pipelines) |
| Qwen 3.8 27B (F6) con esta técnica | ⚪ Técnicamente posible pero inutilizable en la práctica (misma velocidad) |
| Calidad sin cuantizar | 🟡 Interesante en teoría, irrelevante si no puedes usarlo |
| Modelos que CABEN (LFM 2.6B 55 tok/s, gpt-oss 15 tok/s) | ✅ **La filosofía del lab ya es la correcta**: elegir el modelo por la VRAM, no forzar gigantes a rastras |

**Sin futuribles.** El lab ya tomó la decisión correcta (batería PRODUCCIÓN +
modelos que caben en 12 GB). Air LLM es un avance de laboratorio que confirma
que el futuro local pasa por eficiencia, no por forzar modelos gigantes con
swap de capas a velocidad inutilizable.

*Dato reutilizable: si algún día el lab considera un modelo gigante (Qwen 3.8),
la referencia honesta es que Air LLM lo correría a 1-3 tok/s — mejor un modelo
que cabe bien y responde rápido que uno gigante que tarda 30 min en una frase.
La regla del lab (VRAM → modelo, no al revés) queda reforzada.*
