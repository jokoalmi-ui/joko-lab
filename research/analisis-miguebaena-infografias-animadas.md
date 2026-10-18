---
title: "Análisis — Infografías animadas con IA (Migue Baena IA, 22-ago-2026)"
type: research
---

# Análisis — Infografías animadas con IA (Migue Baena IA, 22-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://youtube.com/shorts/e2AaClbJj1Q (Migue Baena IA, 19-08-2026, 52s)
**Método:** subtítulos ES descargados (8.4 KB) + metadatos

## Contenido
- Las infografías estáticas "ya no funcionan como antes" — el problema no es el contenido sino cómo se presenta (bloque de texto = nadie lee)
- Con información que **se mueve, aparece por partes y guía la mirada** → la gente deja de hacer scroll
- **Proceso con 2 herramientas de IA** (no las nombra):
  1. Toma tu idea → con un prompt concreto organiza la información en estructura clara y visual
  2. Transforma esa estructura en **infografía animada** (transiciones, iconos, elementos gráficos) lista para publicar
- Resultado en minutos, "parece hecho por un estudio de diseño", sin ser diseñador

## 🔴 Para el LAB — VALOR: MEDIO (EL LAB YA TIENE ESTA CAPACIDAD)

| Capacidad del short | En el lab |
|---|---|
| Infografía estática | ✅ ficha del perfume (HTML → PNG 1080×1350) |
| Infografía animada (transiciones, iconos) | ✅ **POC ficha animada v1-v6** (tour, frasco flotante, despegue) + `gen_ficha_animada.sh` |
| Organización con IA (prompt) | ✅ gpt-oss local / DeepSeek redacta la estructura |
| Generación de vídeo | ✅ `gen_video_corto.sh` (escenas SDXL + zoompan + xfade + voz edge-tts) + Manim MCP |
| "Sin ser diseñador" | ✅ mismo caso (todo automatizado) |

**Diferencia honesta**: el short usa herramientas cloud de infografía animada (no las nombra — probablemente Napkin AI / Genially IA / similar). El lab usa su propio pipeline local (SDXL + ffmpeg + edge-tts) — **más privado, 0 €, y ya validado con el perfume**.

**Conclusión**: VALIDA el formato (infografía animada > estática para captar atención) — el lab ya lo implementó con la ficha animada del perfume. La lección de marketing ("guía la mirada, la gente deja de hacer scroll") es útil para el **LinkedIn educativo del lab** (contenido que se mueve = más alcance).

**Sin futuribles de infraestructura** — solo refuerza que la decisión de invertir en `gen_ficha_animada.sh` fue correcta. Posible uso: aplicar el formato animado a más contenido del lab (no solo perfume) cuando se necesite captar atención en LinkedIn/IG.
