---
title: "Veredicto — Qwen 3.6 35B A3B en el LAB (prueba real, 10-ago-2026)"
type: research
---

# Veredicto — Qwen 3.6 35B A3B en el LAB (prueba real, 10-ago-2026)
**VERACIDAD:** [ALCANCE INTERNO]

## Resultado del benchmark (datos reales, no estimados)

| Prueba | Resultado |
|---|---|
| Carga | ✅ 38.4s vía REST API (flash_attention + offload_kv_cache_to_gpu=false) |
| VRAM | 9.4 GB de 12 GB (expertos MoE a CPU automáticamente) |
| Resumen 400 tok | **2.7 tok/s** (146.7s) — inutilizable |
| Respuesta corta | **9.0 tok/s** (pero TODO en reasoning_content, la respuesta no llega) |
| Clasificación corta | **8.5 tok/s** (ídem, se queda en thinking) |

## Comparativa con lo que el lab ya tiene

| Métrica | R1-14B (actual) | Qwen 35B A3B (probado) |
|---|---|---|
| Velocidad útil | **11 tok/s** | 2.7-9 tok/s (mayormente razonamiento) |
| VRAM | 8.5 GB | 9.4 GB |
| Respuesta directa | ✅ Sí (con prompt "no razones") | ❌ Se queda en thinking process |

## Por qué NO funciona en el lab (causas verificadas)

1. **CPU débil**: i5-9500 (6C/6T). Los expertos MoE (la parte pesada) van a CPU con
   ncmoe automático → el cuello de botella es la CPU, no la GPU. El artículo de
   Habr usaba 12 núcleos físicos (doble).

2. **Ancho de banda GPU**: A2000 = 288 GB/s vs RTX 4070 = 504 GB/s (1.75x menos).
   Aun con los expertos en GPU, la A2000 transfiere datos más lento.

3. **El modelo razona SIEMPRE**: Qwen 3.6 A3B es un modelo de razonamiento —
   gasta tokens en "thinking process" incluso para "di el número 7". Para
   tareas batch rápidas esto es inaceptable (150 tokens de razón para nada).

4. **R1-14B es mejor para el caso de uso del lab**: razonamiento visible pero
   controlable con prompt, 11 tok/s reales, respuestas directas.

## Conclusión HONESTA

**Qwen 3.6 35B A3B NO es viable en el lab (A2000 + i5-9500).** La teoría del
estudio (MoE cabe en 12 GB) es cierta, pero el rendimiento real depende del
CPU (expertos) y del ancho de banda — ambos son débiles en este equipo.

**El experimento se cierra con resultado NEGATIVO:**
- ✅ Descargado (22 GB) y cargado (9.4 GB VRAM)
- ❌ Velocidad inutilizable para batch (2.7-9 tok/s)
- ❌ El razonamiento forzado lo hace peor que R1-14B en todo

**R1-14B sigue siendo el modelo local de referencia del lab** (11 tok/s, 0 €,
respuestas directas, suficiente para batch). La A2000 de 12 GB es el límite:
los MoE grandes (30B+) requieren CPU potente + GPU con más ancho de banda
(4070/3060 ti en adelante) o el futuro PC con i9-9900K + más VRAM.

## Futurible actualizado

El modelo queda DESCARGADO (22 GB, no cuesta nada mantenerlo). Si algún día:
- Se monta el i9-9900K (más núcleos → expertos más rápido)
- O se consigue una GPU con más ancho de banda
- O se usa solo con contexto corto y sin razonamiento

...se puede re-probar. Hoy: NO usar. El router local/cloud sigue apuntando a R1-14B.

## Detalles técnicos (para no repetir el error)

- `lms load --gpu 0.5` → SIGABRT (offload 50% no funciona para MoE)
- **La forma correcta**: REST API `POST /api/v1/models/load` con
  `flash_attention: true` + `offload_kv_cache_to_gpu: false` → carga 38.4s, 9.4 GB
- El ncmoe (expertos a CPU) se aplica automáticamente cuando la VRAM no basta
- El modelo SIEMPRE genera reasoning_content (modelo de razonamiento puro)
