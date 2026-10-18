---
title: "Análisis — Post askpstudyinaustralia: \"12 ChatGPT Prompts for Critical Thinking\" (18-ago-2026)"
type: research
---

# Análisis — Post askpstudyinaustralia: "12 ChatGPT Prompts for Critical Thinking" (18-ago-2026)

**Fuente:** https://www.instagram.com/p/DcKfYiKiSv0/ (askpstudyinaustralia — Study In Australia 🐨, post, 17-ago)
**Método:** browser_get_images (URL con ig_cache_key) → fetch navegador (base64 277 KB → JPG 213 KB 1152×1440) → GLM + browser_vision (12 prompts completos)
**VERACIDAD:** [VERIFICADO]
**Autor original:** Andrew Bolis (LinkedIn/X) · FreeGuides.cc (REPOST)

## CONTENIDO (los 12 prompts verificados)

Infografía: **"12 CHATGPT PROMPTS FOR CRITICAL THINKING"** — cada prompt con
"cuándo usarlo" (When) y el prompt en sí:

1. **Question Your Assumptions** — cuando algo no tiene sentido → "¿qué suposiciones no examinadas hay bajo mi creencia?"
2. **Understand Opposing Views** — entender la perspectiva opuesta → "actúa como [quien se opone] y explica su perspectiva"
3. **Spotting Biases** — postura fuerte → "¿qué podría distorsionar mi punto de vista?"
4. **Testing Logic** — verificar razonamiento → "actúa como razonador: ¿dónde falta evidencia?"
5. **Analyze Ripple Effects** — impacto a largo plazo → "¿qué consecuencias de 2º y 3er orden?"
6. **Play Devil's Advocate** — idea correcta → "¿qué objeciones poderosas podrían hacerse?"
7. **Verifying Sources** — verificar afirmación → "¿cómo respondería alguien que discrepa?"
8. **Get Other Perspectives** — ampliar visión → "considero diferentes disciplinas"
9. **Define Precisely** — desacuerdo sobre términos → "ayúdame a entender el significado preciso de [término]"
10. **Challenge The Status Quo** — método actual falla → "¿qué alternativas no examinadas podríamos explorar?"
11. **Facts Versus Opinions** — discusión emocional → "¿qué puntos fácticos apoyarían ambas perspectivas?"
12. **Revealing Blind Spots** — atascado → "¿qué factores subyacentes estoy ignorando?"

## 🎯 APLICACIÓN AL LAB — VALIDA LA FILOSOFÍA + HERRAMIENTA DIRECTA

| Prompt | Equivalente real en el lab |
|---|---|
| **Verifying Sources** (7) | **Gate de veracidad** — exactamente lo que hace con [VERIFICADO] |
| **Play Devil's Advocate** (6) | Fail-closed / re-verificación / contrastar_externo |
| **Spotting Biases** (3) | Etiqueta manual honesta + corrección de sesgo (17-ago) |
| **Question Your Assumptions** (1) | "Verificar > asumir" — la regla #1 del lab |
| **Testing Logic** (4) | Suite 219 tests + verificador research |

**VALIDA**: los 12 prompts de pensamiento crítico son literalmente la
metodología del lab aplicada a prompts de ChatGPT. El lab ya implementa 5-6
de estos patrones de forma sistemática (gate, fail-closed, verificación).

**Futurible menor**: banco de prompts de pensamiento crítico reutilizable
para análisis del lab (p.ej. pasar "Devil's Advocate" a un análisis nuevo
antes de cerrarlo). Señal: cuando un análisis del lab quede "sospechosamente
redondo" sin contraargumentos.

## FORMATO (aislable)

- Estructura "When → Prompt" (cuándo usarlo → qué pedir) — patrón limpio
- Reutilizable para LinkedIn Lab: "12 prompts de pensamiento crítico que mi
  lab aplica sin llamarlos así"

## Veredicto
**VALIDA EL LAB / FORMATO ÚTIL.** Los 12 prompts de pensamiento crítico de
Andrew Bolis (FreeGuides.cc, reposteado por Study In Australia) son la
metodología del lab expresada como prompts: verificar fuentes, jugar al
abogado del diablo, detectar sesgos, cuestionar supuestos. El lab ya
implementa 5-6 patrones de forma sistemática (gate de veracidad, fail-closed,
"verificar > asumir", corrección de sesgo). Contenido educativo no del
núcleo técnico pero útil como formato y como validación de la filosofía.
**Nota proceso**: CDN t39.30808-6 (feed) SÍ exige efg (403 sin él) — pero el
fetch desde el navegador con la URL completa del DOM resuelve sin pisar el
pitfall 13 del write_file (nueva vía consolidada para este CDN).
