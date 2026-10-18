---
title: "Análisis — DeepSeek Harness + modelos locales llama.cpp (Nichonauta, 21-ago-2026)"
type: research
---

# Análisis — DeepSeek Harness + modelos locales llama.cpp (Nichonauta, 21-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://youtu.be/nYsJn7Fbj_c (Nichonauta, 14-08-2026, 14:38)
**Método:** transcripción ES completa (yt-dlp auto-subs, 39.7K chars, dedup parcial)

## Qué es (según el vídeo)
**DeepSeek Harness** = arnés agéntico de código abierto (instalación: 1 comando npm),
entorno de chat/agente estilo OpenCode/Hermes/P+agent que:
- Se conecta a proveedores personalizados, incluidos **modelos LOCALES vía llama.cpp**
  (probado con Qwen 3.5 9B, GPU, 131K contexto)
- Compatible con 3 tipos de API: OpenAI Completions/Responses + Anthropic Messages
- **Modos agénticos**: código (herramientas de desarrollo), minimal (más ligero),
  plan (escribe plan → apruebas → implementa), solo-leer / todo-dentro-proyecto
- **Telemetría poco común**: tokens de entrada/salida, tok/s promedio, % en cache —
  visibles en cada conversación

## Pruebas reales del vídeo (con modelo local Qwen 3.5 9B)
1. **Modo código + "analiza el proyecto"**: falló 4 veces seguidas al inicio
   (se INVENTÓ los archivos que no existen — alucinación de rutas), pero luego
   produjo un análisis excelente del proyecto (estructura, pipeline, flujo)
2. **Modo minimal**: falló más rápido, se rindió — usaba comandos de Linux/Mac
   en Windows (no adaptó el SO); mejoró al decirle "estamos en Windows"
3. **Modo plan**: leyó plan.md, generó plan definitivo estructurado, aprobación →
   implementó un videojuego Battle City modificado en 1 archivo (~13 min,
   12K+ tokens generados); el juego funcionaba con sonido pero con bug de menú
   (depende del modelo, no del arnés)

## Veredicto de Nichonauta
El arnés le gusta (fácil de instalar, modos útiles, telemetría, funciona como
chat general también). Los fallos iniciales de herramientas = adaptación
modelo+agente, no del arnés en sí.

## 🔴 Para el LAB — VEREDICTO: BAJO (el lab YA tiene todo esto con Hermes)

| Capacidad del Harness | Equivalente en el lab | Estado |
|---|---|---|
| Modos agénticos (código/plan/minimal) | Hermes con skills (plan, spike, TDD) + gates | ✅ Ya lo tiene, mejor |
| Modelos locales (llama.cpp/LM Studio) | Hermes → LM Studio :1234 (GLM, gpt-oss, LFM) | ✅ Ya lo tiene |
| Telemetría tokens/tok/s/cache | pipeline_proxy.py :9911 (telemetría completa) | ✅ Ya lo tiene, mejor |
| Aprobación de plan antes de implementar | Gate de veracidad + revisar-decisiones + confirmación explícita | ✅ Ya lo tiene, mejor |
| Herramientas fallando (alucina archivos) | Gate + verificar_research + regla 15 (no inventar) | ✅ Mitigado por diseño |

**Sin futuribles.** Es otro entorno agéntico (DeepSeek Harness) que duplica lo que
Hermes ya hace en el lab con más integración (skills, crons, MCPs, gate). El vídeo
valida el patrón (agente + modelo local + telemetría) que el lab ya implementa.

*Dato útil reutilizable: la telemetría de cache/tokens que muestra el Harness es
exactamente lo que el proxy :9911 ya registra en el lab (TTFB, tokens, coste) —
validación externa de la dirección de observabilidad del lab.*
