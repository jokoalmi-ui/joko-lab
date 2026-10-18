---
title: "Análisis: Qwen 3.5 9B ¿Vale la PENA? (Nichonauta)"
type: operations
---

# Análisis: Qwen 3.5 9B ¿Vale la PENA? (Nichonauta)
**VERACIDAD:** [VERIFICADO]

**Fuente**: https://youtu.be/y-SMykh7Y8c · Nichonauta (@nichonauta) · 02-sep-2026
**Vídeo**: ~10 min · Transcripción real (10.788 chars, `--language es`)
**ID**: y-SMykh7Y8c · **Estado**: [VERIFICADO] con transcripción

## Qué prueba el vídeo

4º vídeo de la serie Qwen 3.5 en RTX 3060 **12 GB** (misma clase que la A2000 12 GB del lab):
0.8B sin cuantizar → 2B Q8 → 4B Q4+KV Q8 → **9B Q4 + KV Q8, ventana a la mitad (131K de 162K)**.

Por qué no cabe: el 9B carga modelo + visión + MTP + KV del MTP + KV del principal
≈ **10 GB VRAM** con la ventana recortada. Aun cuantizando modelo a Q4 y KV a Q8.

## Resultados (mismos prompts que 0.8B/2B/4B)

| Prueba | Resultado 9B vs anteriores |
|---|---|
| Landing page HTML | ≈ 4B, no mejor (solo "diferente") |
| Calculadora HTML/CSS/JS | ✅ **la mejor de la serie** — funcional a la primera |
| Reloj analógico | ❌ peor que 2B/4B — ni manecillas ni cambio de tema |
| Simulación de fluidos | 🟡 1ª vez que muestra algo (parcial, no funcional del todo) |

## Veredicto del autor (textual)

- 0.8B sin cuantizar: no merece la pena (poca calidad general)
- 2B Q8: interesante · 4B Q4: aún más interesante (casi misma memoria que 2B Q8)
- **9B Q4: pesa más, es más lento y la inteligencia NO mejora de forma constante**
  → se queda con el 4B Q4 o el 2B Q8
- Dato de KV cache (clave): 2B→1.5 GB, 4B y 9B→4 GB (hay que cuantizarla a Q8 = 2 GB)

## Filtro de valor para el lab (regla 20-ago)

**VALIDACIÓN, no acción.** El lab ya eligió sus modelos para la A2000 12 GB
(GLM, gpt-oss-20b, deepseek-r1-14b, gemma-4-12b — ninguno Qwen) con la misma
lógica: punto dulce en modelos pequeños/medios con cuantización consciente de
la KV cache. El vídeo confirma desde el hardware real del lab que **el salto
4B→9B en 12 GB no paga** (más VRAM, más lento, ganancia no consistente).

Futurible débil (NO anotar como pendiente): probar Qwen 3.5 4B Q4+KV Q8 como
candidato de respaldo no aporta — el lab ya tiene cubierto ese nicho con
modelos validados por su propia batería 5x5.

Conecta con: `analisis-nichonauta-qwen27b-cuantizado.md`, `reto-modelos-2b.md`
(serie del canal), mapa-capacidades (Evaluación modelos = batería propia).
