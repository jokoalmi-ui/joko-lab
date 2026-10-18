---
title: "Análisis — Reel dailydoseofds_: \"AI security goes far beyond AI\" (18-ago-2026)"
type: research
---

# Análisis — Reel dailydoseofds_: "AI security goes far beyond AI" (18-ago-2026)

**Fuente:** https://www.instagram.com/p/DcJQbhhiH6I/ (dailydoseofds_ — Daily Dose of Data Science, video, 17-ago, 17h)
**Método:** caption COMPLETO capturado del DOM real del post + video player (sin audio)
**VERACIDAD:** [VERIFICADO]

## CONTENIDO (lo que dice)

### "AI security goes far beyond AI 🔒 — The biggest risk isn't the model at all."

**El argumento (traza una llamada de modelo):**
1. El prompt sale de la app → endpoint del proveedor → **según su política de
   retención, queda en logs externos durante días**
2. Si el prompt lleva datos regulados/privados, **se mueve fuera del límite de
   la app** (app boundary)
3. **Prompt filtering NO es suficiente**: solo gobierna lo que ENTRA al
   modelo, no dónde pueden viajar los datos ni quién los almacena

**Dos preocupaciones de nivel infraestructura:**
1. **Per-request**: cada llamada mueve datos fuera de la app — ¿quién accede
   en tránsito? ¿Está scoped al tenant correcto?
2. **Posture drift**: ¿los proveedores retienen los datos y por cuánto?
   ¿Pueden los prompts de un tenant llegar al contexto de otro?

**Problema del enfoque por aplicación:** 10 features = 10 implementaciones
separadas de scoping/encryption/logging.

**Solución: mover ambos a la capa de infraestructura:**
- **IAM policies** — qué servicios pueden llamar a qué endpoints (cada nueva
  llamada hereda el límite automáticamente)
- **VPC isolation** — tráfico de tenants separado a nivel de red
- **Encryption + logging** — por defecto en todos los flujos de datos

**Caso real**: IDEMIA (datos de identidad de 45+ agencias US) → EKS GovCloud:
-30% costes, 4× velocidad, seguridad desde la infraestructura no desde el código.

Pregunta final: "¿Estás manejando la seguridad de IA en la capa de aplicación
o infraestructura?"

## 🎯 APLICACIÓN AL LAB — MUY RELEVANTE (seguridad real del lab)

| Concepto | En el lab (real, verificado) |
|---|---|
| **"El prompt sale de la app y queda en logs del proveedor"** | **El lab usa APIs cloud**: DeepSeek (deepseek-v4-flash), Gemini (API key), Google AI Pro — cada prompt va a sus servidores con su política de retención |
| **Prompt filtering no basta** | El gate de veracidad filtra contenido, pero NO controla la fuga de datos al proveedor |
| **Límite de la app (app boundary)** | Los datos del lab: café-ia, perfume-ia, Baskepensiones, TFM — ¿qué llega a los proveedores cloud? |
| **Mover a infraestructura** | El lab ya lo hace parcialmente: **local-first** (LM Studio, Ollama, RAG LanceDB) = los datos sensibles NO salen del lab |
| **IAM/VPC** | Futurible si algún día se expone el lab a terceros |

**Lectura honesta para el lab:** el post valida la decisión **local-first**
del lab — los datos que NO deben salir (BD personales, finanzas) se procesan
local (LM Studio + Ollama + LanceDB); solo lo que ya está en cloud (Google
workspace, DeepSeek API) viaja a proveedores. La "app boundary" del lab es
fuerte por diseño. Matiz: la suscripción Google AI Pro (~20€/mes) y DeepSeek
envían prompts a cloud — si algún día se procesan datos sensibles ahí,
aplicar la lección (¿qué se manda, quién lo retiene?).

## FORMATO (aislable)

- Estructura: traza de una llamada (capa app → proveedor → logs) + 2
  preocupaciones de infra + solución en capas (IAM/VPC/encryption/logging)
- Reutilizable para el TFM: "dónde vive la seguridad de un sistema LLM"

## Veredicto
**MUY RELEVANTE / VALIDA EL LOCAL-FIRST DEL LAB.** El post explica que la
seguridad de IA va más allá del modelo: el prompt sale de la app y queda en
logs del proveedor, y el filtering de la capa de aplicación no controla la
fuga de datos. Para el lab: **valida la arquitectura local-first** (los datos
sensibles no salen: LM Studio/Ollama/LanceDB) y deja un futurible claro
(mapear qué prompts van a cloud y con qué política de retención — DeepSeek,
Gemini, Google AI Pro). Coherente con least-privilege-lab (política del lab).
**Nota proceso**: caption íntegro capturado del DOM (video sin audio — el
caption ES el contenido).
