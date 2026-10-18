---
title: "Análisis — Comparativa SLMs en Programación (Nichonauta, 21-ago-2026)"
type: research
---

# Análisis — Comparativa SLMs en Programación (Nichonauta, 21-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://youtu.be/ArABLzPR5Ok (Nichonauta, 16-08-2026, 10:12)
**Método:** transcripción ES completa (yt-dlp auto-subs, 26.8K chars, dedup parcial)

## El experimento
4 modelos pequeños (SLMs) generando el MISMO juego desde el MISMO prompt (one-shot,
sin agente que itere): **Gemma 4 12B · LFM 2.5 8B A1B · Ornit 1.09B · Qwen 3.5 9B**.
Todos a 4 bits, 131K contexto, MTP/visión donde aplica. Objetivo: ¿puede un SLM
entregar un proyecto de ~1000 líneas bien a la primera?

## Resultados (verificados en el vídeo)

| Modelo | tok/s | Resultado |
|---|---|---|
| Gemma 4 12B | (alto) | Razona que escribe código pero NO hace nada — "razonamiento falso" (destilado de resúmenes de otros modelos, tokens por gastar) |
| LFM 2.5 8B A1B | muy rápido | 1 línea CSS, HTML vacío → NO preparado para código; útil para autocompletado/herramientas |
| Ornit 1.09B | 69 | Razonó en español, generó tokens similares a Gemma 12B, pero visualmente no se aprecia nada |
| Qwen 3.5 9B | 67 | 14K tokens, menú "más interesante", pero no responde al clic |

**Veredicto del vídeo**: ninguno basta para un one-shot de proyecto completo.
Sirven para autocompletar/trabajar en conjunto, no para delegarles un proyecto.

## Conclusión CLAVE de Nichonauta (la parte valiosa)
> Los modelos en línea funcionan mejor NO solo porque son más inteligentes,
> sino porque **ITERAN**: corrigen, prueban, ejecutan, compilan, dan muchas
> vueltas. El one-shot no es el método; la iteración es el método.

## 🔴 Para el LAB — VEREDICTO: MEDIO-BAJO (valida filosofía, sin acción)

| Hallazgo | En el lab |
|---|---|
| "Iterar > one-shot" | ✅ **EXACTO**: gate + revisor + verificar_research + iterar — el lab NUNCA entrega one-shot |
| SLMs para código: insuficientes solos | ✅ Coherente: el lab usa SLMs para tareas LIGERAS (LFM 2.6B), no para escribir código |
| Gemma 12B con razonamiento "falso" | 🟡 Dato: el lab tiene Gemma-4-12B descargado (7.15 GB) — no usarlo como generador de código serio |
| LFM 8B A1B no para código | 🟡 El lab usa LFM 2.6B (texto) y LFM VL 3B (visión) — sin conflicto con su uso actual |

**Sin futuribles nuevos.** El vídeo valida la dirección del lab (iteración +
gate, no one-shot) y aporta datos honestos sobre modelos que el lab ya tiene
(Gemma 12B no es generador de código; los SLM son para tareas ligeras).

*Dato reutilizable: si algún día el lab considera SLMs para generar código,
este vídeo es la referencia de que sin iteración (agente + pruebas) no
funcionan — el lab ya tiene ese bucle con gate/revisor.*
