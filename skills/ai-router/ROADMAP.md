# ai-router — Roadmap

## Etapa actual: 3 — Actuar

### ✔ Completado en etapa 1

- [x] Definir criterios de enrutamiento (privacidad, razonamiento, multimodal, recursos, rapidez)
- [x] Documentar proveedores disponibles (Ollama, DeepSeek, Gemini, LM Studio)
- [x] Crear árbol de decisión
- [x] Documentar comandos de diagnóstico
- [x] Documentar riesgos y protecciones

### ✔ Completado en etapa 2

- [x] Probar acceso a Ollama desde comandos de COMMANDS.md
- [x] Probar acceso a LM Studio (API activa con 6 modelos)
- [x] Verificar VRAM real (10.9 GB libres) y ajustar umbrales
- [x] Comprobar modelos disponibles (3 Ollama, 6 LM Studio)
- [x] Probar árbol de decisión: consulta simple, razonamiento, visión
- [x] Comparativa rendimiento: llama31-8b-64k (1.9s), gemma-4-e4b (0.5s), DeepSeek (~2-3s)
- [x] Test de visión local con gemma-4-e4b y gemma-4-12b-qat
- [ ] Verificar si Gemini necesita configuración adicional

### ✔ Completado en etapa 3

- [x] Implementar script de enrutamiento automático (`ai-router.py`)
- [x] Probar rama simple (Ollama → responde correctamente)
- [x] Probar rama visión (LM Studio → responde correctamente)
- [x] Probar diagnóstico del sistema
- [x] Detectar VRAM baja y modelos no cargados
- [ ] Integrar la decisión en el flujo de Hermes (como skill tool o plugin)
- [ ] Definir qué hacer cuando el proveedor recomendado no está disponible

### Pendiente para etapa 4 (Optimizar)

- [x] Evaluar rendimiento de cada proveedor en tareas reales
- [x] Documentar coste aproximado de cada proveedor externo
- [ ] Ajustar umbrales de VRAM según experiencia
- [ ] Automatizar la decisión sin intervención del usuario
- [ ] Evaluar si tiene sentido un wrapper unificado (ej: LiteLLM, OpenRouter)
