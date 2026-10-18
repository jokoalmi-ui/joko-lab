---
id: gemma-4-e4b
name: Gemma 4 E4B
version: "4"
quantization: Q4_K_M (con mmproj BF16)
engine: LM Studio
added: 2026-07-26
status: retirado
superseded_by: lfm2.5-2.6b
retired: '2026-08-06'
motivo_retirada: "Bateria modelos 06-ago: 7/7 pero 29.2 tok/s; lfm2.5-2.6b lo supera en velocidad (55 tok/s) con la misma calidad. Estudio 06-ago lo señalaba como rival del LFM — el LFM gana. Capacidad de vision (mmproj) ya cubierta por glm-4.6v-flash. Sin RULE que lo seleccione. GGUF + mmproj eliminados del disco."
---
# Gemma 4 E4B (retirado)

Modelo retirado el 06-ago-2026 tras la batería de modelos. Redundante con LFM 2.5 2.6B (misma clase: pequeño, tool calling) que lo supera en latencia.

## Datos de la retirada

- Batería 06-ago: 7/7, 29.2 tok/s
- Sustituido por: lfm2.5-2.6b (7/7, 55.3 tok/s)
- Visión cubierta por: glm-4.6v-flash
- GGUF + mmproj eliminados del disco el 06-ago
