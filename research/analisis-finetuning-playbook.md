---
title: "Análisis — LLM Fine-Tuning Playbook (serie 9 notas)"
type: research
---

# Análisis — LLM Fine-Tuning Playbook (serie 9 notas)
**VERACIDAD:** [ALCANCE INTERNO]

**Fecha:** 04-ago-2026
**Fuente:** Serie de 9 posts de sreemantideytech en redes sociales
**Imágenes:** `~/.hermes/image_cache/img_5ac3c3ae025a.jpg` (portada) + 8 páginas

---

## La serie (9/9)

| # | Página | Tema clave |
|---|---|---|
| — | Portada (1/9) | base → LoRA → YOUR model ("send a fresh grad to specialty school") |
| 1 | FT vs Prompt vs RAG (2/9) | Árbol de decisión + regla de oro |
| 2 | Data Curation (3/9) | Calidad > cantidad, LIMA 1000 ejemplos |
| 3 | LoRA | W+ΔW, ~0.1% params, α=2r, variantes (DoRA/VeRA) |
| 4 | QLoRA (5/9) | NF4, 7B≈6GB total, stack (PEFT/TRL/Unsloth) |
| 5 | SFT & Training | Hiperparámetros, bugs comunes, sanity checks |
| 6 | Preference Tuning (7/9) | DPO = estándar 2026, fórmula, datos |
| 7 | Eval & Iterate (8/9) | Evals ANTES de entrenar, métodos, canary deploy |
| — | Big Picture (9/9) | Base → SFT(LoRA) → DPO → Quant+Serve |

---

## El árbol de decisión (página 2) — clave

| Necesitas... | Solución |
|---|---|
| Datos frescos | RAG (NO FT — no actualiza conocimiento) |
| Estilo/marca/voz | Fine-tune |
| Skill nueva (function calling, razonamiento niche) | Fine-tune (o few-shot fuerte) |
| Inferencia más barata/rápida | Distilar: FT modelo pequeño |
| Mejor output en skills existentes | Prompt engineering PRIMERO |

**Regla de oro:** "No fine-tunees para arreglar un problema de prompt.
Fine-tunea cuando hay patrones repetibles que el modelo no hace bien ni con
prompting."

**Coste vs beneficio:** prompt eng (0 cost, probar primero) < RAG (coste
moderado, fácil actualizar) < Fine-tune (coste de entrenamiento + dataset) <<
Pre-train ($$$ millones, casi nunca).

---

## Las 3 etapas del entrenamiento

1. **Continued pre-training** → texto de dominio, sin etiquetas (legal/médico)
2. **SFT** (instruction tuning) → pares (instrucción → respuesta)
3. **Preference tuning** → DPO/RLHF sobre pares (chosen, rejected)

Nota: "La mayoría de equipos solo hace SFT."

---

## LoRA / QLoRA (relevancia directa para RTX A2000 12GB)

- **LoRA:** W + ΔW, ΔW = A·B (r << d), entrena ~0.1% de parámetros, 10-100x
  menos VRAM, sin coste de inferencia si mergeas.
- **QLoRA:** base en 4-bit NF4 (~75% menos memoria) + adaptadores bf16.
  **7B ≈ 6GB total → cabe en 12GB.** "El momento democratizador".
- **Stack:** bitsandbytes, PEFT, TRL (SFTTrainer/DPOTrainer), Unsloth (2-5x
  rápido), Axolotl (YAML), Llama-Factory (UI).
- **Hiperparámetros LoRA:** rank 8-64 (empezar 8/16), α = 2r, target all-linear
  (mejor que q_proj/v_proj solo), dropout 0.05.

---

## Eval & Iterate (página 8)

- **Construir evals ANTES de entrenar** — sin eval set no sabes si ayudaste o
  perjudicaste. 50-200 casos difíciles, pineados, nunca cambian.
- **Métodos:** exact match/F1, BLEU/ROUGE, LLM-as-judge, pairwise A/B, humano,
  task-specific (código pasa tests, JSON parsea).
- **Comparar:** FT vs base, FT vs mejor prompt, FT vs hosted GPT/Claude,
  múltiples runs FT entre sí.
- **Iterar:** correr → mirar fallos manualmente → categorizar → arreglar datos
  → retrain → re-eval.
- **Deploy:** GGUF/EXL2 o vLLM/TGI → **shadow → canary → full** → monitor drift.

---

## Aplicación a Joko Lab (estado real 04-ago)

| Principio del playbook | Estado en el lab |
|---|---|
| RAG para conocimiento | ✅ LanceDB + BGE-M3 + reranker |
| Prompt engineering primero | ✅ Skill prompt-engineering |
| LoRA/QLoRA para estilo | ✅ Dolphin Cyber LoRA (8B) |
| Evals antes de entrenar | ✅ Evidence Contract + certificación |
| QLoRA 7B ≈ 6GB | 💡 Posibilidad futura: entrenar LoRA propio en A2000 |
| DPO post-SFT | ⏳ Futuro, solo si se necesita afinamiento fino |
| Canary/monitor deploy | ❌ Gap detectado (aplica al lab también) |

**Conclusión:** el playbook valida la arquitectura actual del lab. La
posibilidad nueva más interesante: **entrenar un LoRA propio** (QLoRA 7B cabe
en la RTX A2000) — para darle "brand voice" o skills específicas al lab sin
depender de LoRAs descargados.

---

## Nota

Serie de divulgación técnica de alta calidad (495 likes, 795 saves). Alineada
con la práctica estándar de fine-tuning 2026. Referencia útil para
`ai-architecture` (sección modelos/entrenamiento) y para decidir si algún día
se entrena un LoRA propio.
