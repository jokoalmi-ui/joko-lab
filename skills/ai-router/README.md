# ai-router

Skill para enrutar tareas de IA entre modelos locales y externos según criterios de privacidad, complejidad, tipo de contenido y recursos disponibles.

## ¿Qué permite?

- Decidir qué modelo usar según cinco criterios: privacidad, razonamiento, multimodal, memoria disponible y velocidad
- Comprobar disponibilidad de modelos locales (Ollama, LM Studio)
- Comprobar VRAM libre antes de decidir qué modelo local cargar
- Conmutar entre proveedor principal (DeepSeek), local (Ollama) y multimodal (Gemini)
- Sugerir modelo ligero cuando los recursos son ajustados

## ¿Qué NO permite?

- No modificar la configuración de Hermes sin confirmación
- No cambiar el proveedor por defecto sin explicar el impacto
- No instalar modelos nuevos automáticamente sin autorización
- No enviar datos privados a proveedores externos aunque la tarea lo pida

## Dependencias

| Recurso | Puerto / Ruta | Uso |
|---|---|---|
| Ollama | `localhost:11434` | Modelos locales (privacidad, ligero) |
| LM Studio | `localhost:1234` (opcional) | Modelos locales adicionales |
| DeepSeek | API externa (v4-flash) | Razonamiento complejo |
| Gemini | API externa | Multimodal (imágenes, PDFs) |
| GPU NVIDIA | `nvidia-smi` | Medir VRAM disponible |
| Sistema | `/proc/meminfo`, `free -h` | Medir RAM disponible |

## Documentación relacionada

- `docs/estado-real.md` — estado actual de proveedores y recursos
- `docs/decisiones/` — decisiones sobre elección de proveedores
