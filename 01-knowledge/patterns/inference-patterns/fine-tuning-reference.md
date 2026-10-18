---
type: knowledge
subtype: pattern
status: active
tags: [knowledge, pattern]
created: 2026-07-29
---
# Fine-Tuning Reference — Joko Lab
====================================
Fuente: Instagram @thepracticai (2026-07-29) + busqueda web
Estado: REFERENCIA — No implementado. Para estudio futuro.

═══════════════════════════════════════════════════════════
1. ¿QUE ES FINE-TUNING?
═══════════════════════════════════════════════════════════

Ajustar los pesos de un modelo pre-entrenado con datos
especificos para especializarlo en una tarea concreta.
A diferencia del RAG, que inyecta contexto externo sin
modificar el modelo, el fine-tuning cambia el modelo
permanentemente.

═══════════════════════════════════════════════════════════
2. METODOS PRINCIPALES
═══════════════════════════════════════════════════════════

| Metodo | VRAM necesario | Velocidad | Calidad relativa | Cuando usarlo |
|---|---|---|---|---|
| **Full Fine-Tuning** | 24GB+ (para 7B) | Lenta | 100% | Tienes GPU grande y muchos datos |
| **LoRA** | 8-12GB (para 7B) | Rapida | ~90-95% | Especializar sin perder lo aprendido |
| **QLoRA** | 6-8GB (para 7B) | Rapida | ~85-90% | GPU limitada — nuestro caso |
| **DoRA** | similar a LoRA | Similar | ~92-97% | Variante de LoRA que separa magnitud y direccion |
| **Adapter** | similar a LoRA | Similar | ~88-93% | Otra variante PEFT |

## LoRA vs QLoRA (detalle)

LoRA: entrena matrices de rango reducido (~0.1-1% parametros).
       El modelo base se queda congelado. Ocupa ~1-2GB extra en RAM.

QLoRA: igual que LoRA pero el modelo base se cuantiza a 4-bits.
        Ocupa ~4-5GB en total para un modelo de 7B.
        Mas lento que LoRA (~10-20%) porque des-cuantiza en cada forward.

Para nuestra RTX A2000 12GB:
  - LoRA: justo pero viable con modelos 7B (si el base cabe en FP16)
  - QLoRA: el metodo recomendado (cabe con holgura y deja VRAM para el KV cache)

═══════════════════════════════════════════════════════════
3. CUANDO USAR RAG VS FINE-TUNING
═══════════════════════════════════════════════════════════

Decision tree:

  ¿Los datos cambian frecuentemente?
  ├── Si → RAG (re-indexas y listo, no re-entrenas)
  └── No → ¿Necesitas que el modelo aprenda un estilo/tono/forma?
        ├── Si → Fine-Tuning
        └── No → ¿Tienes pocos datos (<500 ejemplos)?
              ├── Si → RAG
              └── No → Evalua si el RAG es suficiente
                      (si ya funciona bien con 3 chunks, no FT)

Tabla comparativa por criterio:

| Criterio | RAG | Fine-Tuning |
|---|---|---|
| Conocimiento dinamico (cambia a menudo) | ✅ Excelente | ❌ Malo (re-entrenar cada vez) |
| Conocimiento estatico (estilo, tono, dominio fijo) | ❌ Limitado | ✅ Excelente |
| Datos escasos (< 1000 ejemplos) | ✅ Funciona bien | ❌ Riesgo de overfitting |
| Datos abundantes (> 10000 ejemplos) | ✅ Funciona bien | ✅ Excelente |
| VRAM baja (< 12GB) | ✅ Consume ~1.2GB | ⚠️ Solo QLoRA cabe justo |
| Transparencia (saber fuente) | ✅ Fuente visible | ❌ Caja negra |
| Latencia de respuesta | ⚠️ ~+200ms (busqueda) | ✅ Sin overhead |
| Coste de mantenimiento | ✅ Bajo | ❌ Alto (re-entrenar) |

───────────
RECOMENDACION PARA JOKO LAB:
  HOY: RAG. Es la decision correcta. El fine-tuning no aporta valor.
  FUTURO: Si se necesita especializar un modelo local en tareas
  muy concretas (un modelo que solo hable de un dominio con tono
  propio), LoRA/QLoRA serian la via.
───────────

═══════════════════════════════════════════════════════════
4. RLHF Y RLAIF
═══════════════════════════════════════════════════════════

RLHF (Reinforcement Learning from Human Feedback):
  - Entrena un modelo "reward" con preferencias humanas
  - El LLM aprende a maximizar esa recompensa
  - Muy costoso (necesita anotadores humanos)
  - Usado por: ChatGPT, Claude, Gemini

RLAIF (RL from AI Feedback):
  - Usa otro LLM como juez en vez de humanos
  - Mas escalable (un modelo evalua al otro)
  - Ideal para laboratorios pequeños
  - Para Joko Lab: usar Gemma 4 o DeepSeek R1 como juez

Evaluacion por pares (para nuestro caso):
  Modelo A genera respuesta → Modelo B (juez) puntua →
  Nos quedamos con la mejor → Retroalimentamos el knowledge base

═══════════════════════════════════════════════════════════
5. HIPERPARAMETROS QUE IMPORTAN
═══════════════════════════════════════════════════════════

| Parametro | Full FT | LoRA | QLoRA |
|---|---|---|---|
| Learning Rate | 2e-5 | 1e-4 | 2e-4 |
| Batch Size | 16-64 | 8-32 | 4-16 |
| Epochs | 3-5 | 3-5 | 3-5 |
| LoRA Rank (r) | — | 8-16 | 8-16 |
| LoRA Alpha | — | 16-32 | 16-32 |
| Quantization | — | — | 4-bit NF4 |

Regla general: empezar con valores por defecto de PEFT + bitsandbytes
y ajustar solo si no converge.

═══════════════════════════════════════════════════════════
6. FLUJO DE TRABAJO COMPLETO PARA IMPLEMENTAR
═══════════════════════════════════════════════════════════

(Si en el futuro se decide implementar)

1. Preparar datos: formato JSONL con "instruction" + "output"
2. Cuantizar modelo base con bitsandbytes (4-bit NF4)
3. Configurar LoRA con PEFT (rank=8, alpha=16)
4. Entrenar con Trainer de HuggingFace
5. Fusionar pesos LoRA con el base (opcional)
6. Evaluar con modelo juez (Gemma/DeepSeek)
7. Subir a LM Studio como nuevo modelo

Librerias necesarias:
  pip install peft bitsandbytes transformers accelerate trl

Ejemplo minimo (para cuando se decida implementar):
  from peft import LoraConfig, get_peft_model
  from transformers import AutoModelForCausalLM, AutoTokenizer
  from trl import SFTTrainer

  model = AutoModelForCausalLM.from_pretrained(
      "modelo-base",
      load_in_4bit=True,
      device_map="auto"
  )
  lora_config = LoraConfig(
      r=8, lora_alpha=16, target_modules=["q_proj", "v_proj"],
      lora_dropout=0.05, bias="none", task_type="CAUSAL_LM"
  )
  model = get_peft_model(model, lora_config)

═══════════════════════════════════════════════════════════
7. ERRORES COMUNES
═══════════════════════════════════════════════════════════

  - Fine-tunear cuando un RAG bien configurado bastaria (el mas comun)
  - Usar Full FT sin tener GPU suficiente → OOM
  - Entrenar con pocos datos (< 1000 ejemplos) → overfitting
  - No evaluar antes/despues → no sabes si mejoro
  - Olvidar fijar seed → resultados no reproducibles
  - Usar learning rate demasiado alto → destruye el modelo base

═══════════════════════════════════════════════════════════
8. RECURSOS PARA ESTUDIO FUTURO
═══════════════════════════════════════════════════════════

  - HuggingFace PEFT: https://github.com/huggingface/peft
  - bitsandbytes: https://github.com/TimDettmers/bitsandbytes
  - TRL (Transformer Reinforcement Learning): https://github.com/huggingface/trl
  - Unsloth (optimizado para LoRA/QLoRA): https://github.com/unslothai/unsloth
  - Fine-tuning cheat sheet: Instagram @thepracticai

  Pendiente de leer:
  - RAG vs Fine-Tuning: montecarlo.ai/blog-rag-vs-fine-tuning
  - Fine-tuning vs RAG: finetunedb.com/blog/fine-tuning-vs-rag

═══════════════════════════════════════════════════════════
DECISION PARA JOKO LAB
═══════════════════════════════════════════════════════════

  HOY:     RAG. No implementar fine-tuning.
           El RAG con BGE-M3 + LanceDB cubre las necesidades.

  CORTO PLAZO (1-3 meses): Seguir con RAG.
           Mejorar chunking, re-ranking, watchdog.

  MEDIO PLAZO (3-6 meses): Evaluar LoRA/QLoRA si:
           - Tenemos un dominio muy especifico que requiera
             tono/estilo propio (ej: critico de perfumes)
           - El RAG se queda corto en precision
           - Aparece un modelo base que nos interese especializar

  LARGO PLAZO (6-12 meses): Considerar RLHF/RLAIF si:
           - Tenemos un pipeline de evaluacion consolidado
           - Queremos que el laboratorio aprenda de sus errores
           - El volumen de datos lo justifica

═══════════════════════════════════════════════════════════
FIN DE LA REFERENCIA
═══════════════════════════════════════════════════════════
