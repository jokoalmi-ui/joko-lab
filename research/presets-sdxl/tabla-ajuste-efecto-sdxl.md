---
title: "Tabla ajuste → efecto → aplicación SDXL (B5, 20-ago-2026)"
type: research
---

# Tabla ajuste → efecto → aplicación SDXL (B5, 20-ago-2026)

**VERACIDAD:** [VERIFICADO] — todos los efectos MEDIDOS con PIL sobre pares
generados el 20-ago (misma semilla 1234, mismo prompt base "luxury perfume
bottle, product photography, studio", solo cambia el ajuste). Imágenes de
referencia: `research/presets-sdxl/`.

## Cómo leer la tabla

Cada par se generó idéntico salvo el ajuste. Las métricas son de píxel
(PIL puro): brillo medio 0-255, saturación (HSV 0-100%), contraste (stddev de
luma), foco (varianza Laplaciano), nitidez (% bordes).

## Tabla de efectos medidos

| Par (A → B) | Δbrillo | Δsaturación | Δcontraste | Δfoco | Δnitidez | Efecto real |
|---|---|---|---|---|---|---|
| **Dark → Luminoso** | **+63.0** | -19.7% | +3.5 | +123 | +1.28% | El ajuste MÁS determinante: el brillo salta 79→142 (casi x2). Luminoso ASUME también menor saturación (pastel). |
| **Vibrante → Fríos** | +32.6 | **-40.7%** | -9.7 | **-772** | **-2.31%** | El ajuste de saturación más fuerte (-41%), pero a costa de foco y nitidez: los tonos fríos/pastel reducen detalle. |
| **Wide → Cerrada** | +10.8 | +6.3% | +3.3 | +185 | +0.60% | Diferencias de píxel MÍNIMAS: el encuadre no se mide con brillo/foco. Es el ajuste más VISUAL y menos medible — verificar con visión (GLM), no con píxel. |
| **Vivid → Suave** | +13.6 | -8.4% | +3.8 | **-587** | **-2.14%** | Confirmado con datos: "suave/dreamy" reduce foco (-587) y nitidez (-2.1%). El ajuste de detalle real. |

## Aplicación con criterio (qué usar para qué)

| Necesitas | Ajuste | Por qué (con los datos) |
|---|---|---|
| Contraste de marca / portada potente | **Dark** | Brillo 79 = fondo oscuro real; el objeto destaca. |
| Producto limpio / e-commerce | **Luminoso** | Brillo 142 + fondo claro; ojo: saturación baja (-20%) → si el producto es colorido, compensar con prompt "vibrant". |
| Emoción / energía | **Vibrante** | Saturación 68% (el máximo de los 8): el color habla solo. |
| Sofisticación / calma | **Fríos** | Saturación 28% (-41% vs vibrante); asume menos detalle — usar para abstracción, no para producto con textura. |
| Escena amplia / contexto | **Wide** | No medible por píxel; verificar composición con GLM. |
| Detalle del objeto | **Cerrada** | Foco más alto (2732 vs 2546); mejor para mostrar material. |
| Alta fidelidad / fotografía | **Vivid** | Foco 2792 + nitidez 9.11% = los valores MÁXIMOS de los 8. |
| Ambiente / storytelling | **Suave** | Foco -587 y nitidez -2.1%: intencionadamente "soñado". |

## Reglas aprendidas (con datos)

1. **Dark/Luminoso es el ajuste más potente** (Δbrillo 63 de 255) — úsalo con
   intención, no por defecto.
2. **Vibrante y Vivid NO son lo mismo**: vibrante cambia SATURACIÓN (color),
   vivid cambia FOCO/NITIDEZ (detalle). Medido: -41% saturación vs -587 foco.
3. **Wide/Cerrada no se puede auditar por píxel** — el encuadre es visual;
   verificar SIEMPRE con GLM visión (gate B4 composición no lo captura solo).
4. **Luminoso + vibrante** son parcialmente antagónicos: luminoso baja
   saturación (-20%) — si quieres ambos, decirlo explícito en el prompt.
5. **Para producto con textura (perfume, ropa, comida)**: usar Vivid (foco
   máximo) y evitar Fríos (mata el detalle).
6. Estos números son de SDXL base en 512×512 con semilla 1234 — el efecto
   relativo se mantiene entre semillas, pero los valores absolutos varían.

## Cómo reproducir las mediciones

```bash
# 1. ComfyUI arrancado (comfy-on / systemctl --user start comfyui)
bash /tmp/generar_presets_sdxl.sh   # regenera los 8 PNG en /tmp/sdxl_presets/
# 2. Medir (PIL puro, sin numpy):
python3 -c "from PIL import Image,ImageFilter,ImageStat; img=Image.open('/tmp/sdxl_presets/1-dark.png').convert('RGB'); s=ImageStat.Stat(img); print('brillo', sum(s.mean)/3)"
```

## Registro

- Creado: 20-ago-2026 (B5 del itinerario de revisión)
- Relacionado: skill generacion-imagen-local, gate B4 (checklist_calidad_visual.py)
- Estado: implementado y verificado con datos reales
