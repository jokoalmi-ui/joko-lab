---
title: "Análisis — SFT vs RLHF vs DPO (codeby.akash, 22-ago-2026)"
type: research
---

# Análisis — SFT vs RLHF vs DPO (codeby.akash, 22-ago-2026)

**VERACIDAD:** [VERIFICADO]

**Fuente:** https://www.instagram.com/reel/DcTCtVvNgtU/ (codeby.akash, 21-08-2026, 4 likes)
**Método:** caption íntegro extraído (browser_console)

## Contenido: las 3 vías de adaptación/alineación de LLMs

| Técnica | Qué hace | Mejor para |
|---|---|---|
| **SFT** (Supervised Fine-Tuning) | Entrena con ejemplos prompt → respuesta ideal | Enseñar qué es una buena respuesta |
| **RLHF** (RL from Human Feedback) | Usa preferencias humanas para entrenar un reward model | Alineación fuerte de comportamiento |
| **DPO** (Direct Preference Optimization) | Entrena directo con pares elegido/rechazado, SIN reward model | Alineación simple y eficiente |

**Pipeline común**: Pretraining → SFT → RLHF o DPO → LLM alineado

**Takeaway**: SFT = aprender la tarea · RLHF = alinear con preferencias humanas · DPO = alinear directo con pares de preferencia

## 🔴 Para el LAB — VALOR: BAJO-MEDIO (referencia, conecta con fine-tuning)

| Aspecto | Análisis |
|---|---|
| ¿El lab fine-tunea? | ❌ NO hoy (usamos modelos listos + prompts + skills) |
| Conexión | El futurible de fine-tuning ya documentado (learnbay 21-ago): si algún día se fine-tunea LFM 2.6B con Unsloth → el pipeline sería SFT → DPO (más simple que RLHF para 12 GB VRAM) |
| Material | Útil para TFM/LinkedIn (vocabulario de alineación: SFT/RLHF/DPO) |

**Sin futuribles nuevos** — refuerza el mismo camino ya anotado: si el lab fine-tunea localmente, la ruta realista es **SFT + DPO** (DPO no necesita reward model → cabe en 12 GB). RLHF queda descartado para el lab (reward model = mucho más VRAM).

**Conclusión**: referencia educativa sólida; conecta con el futurible de fine-tuning existente y afina la ruta (SFT→DPO, no RLHF).
