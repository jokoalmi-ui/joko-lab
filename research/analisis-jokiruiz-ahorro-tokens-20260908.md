---
title: "Análisis: 11 trucos para ahorrar tokens (Joaquín Ruiz)"
type: research
---

# Análisis: «Deja de ver "vuelve en 5 horas": 11 trucos para ahorrar tokens» (Joaquín Ruiz)
**VERACIDAD:** [VERIFICADO]

**Fuente**: https://youtu.be/yWx7TrhZTxg · Joaquín Ruiz — IA para Desarrolladores (@jokioki) · 08-sep-2026
**Vídeo**: ~18 min · Transcripción real (411 líneas, íntegra)
**ID**: yWx7TrhZTxg · **Estado**: [VERIFICADO] con transcripción íntegra

## Qué presenta

Videotutorial de ahorro de tokens en agentes/APIs de pago. Tesis central:
«escribes 200 palabras y se envían 200.000» — el modelo no tiene memoria; cada
turno reenvía system + tools + historial (input reutilizado), y eso es la
inmensa mayoría de lo que se paga.

### Bloque 1 — hábitos sin instalar nada (trucos 1-6)
1. **Editar el mensaje** en vez de añadir correcciones encadenadas (la rama mala desaparece).
2. **Prompts CRIFO** (contexto-rol-instrucción-formato-objetivo) que cierran el formato de salida antes de enviar.
3. **Ventana nueva al cambiar de tarea** (clear no vuelve a cero: system + tools se reenvían, pero corta el arrastre del historial).
4. **Traspaso a fichero autocontenido** entre fases: ≤40 líneas con SOLO decisiones + porqué, restricciones, estado y siguiente paso; excluir alternativas descartadas, proceso e intentos fallidos.
5. **Limitar el output**: pedir solo el diff / función modificada / 5 líneas / JSON sin explicación (su demo: 10.000 → 6.700 tokens).
6. **Haz tú el grep** (rg/buscador) antes de pasar el fichero entero; dar solo las líneas que importan.

### Bloque 2 — técnico (trucos 7-10)
7. **MCP vs skills**: Claude Code carga MCP on-demand (su captura: 93 tools, 0 tokens); las **skills se inyectan SIEMPRE** (18 skills, 2.000 tokens en cada turno) → revisar y borrar skills sin uso. Excepción: MCP servidos por HTTP no se cargan on-demand.
8. **Elegir modelo por tarea** con SpecJudge (su herramienta open source).
9. **Prompt caching**: función de API (no botón de chat); con cache automática basta un campo y el sistema mueve el punto de corte. Leer de cache ≈ 10 % del precio de entrada; escribir ≈ +25 %. Cifras de **Anthropic**, NO aplicables 1:1 a DeepSeek.
10. **Compactación manual** en punto de corte natural con instrucciones (`/compact conserva las decisiones de arquitectura y nombres de ficheros, olvida intentos fallidos`); no dejarla saltar sola en mitad de tarea.

### Bloque 3 — café para cafeteros (truco 11)
11. **Capa local entre el cliente y la API**: (a) resolver sin llamada si la respuesta ya está en caché local; (b) recortar contexto a fragmentos útiles; (c) **límites duros** que bloqueen peticiones que pasen de X tokens. El autor promete vídeo completo del proxy si el vídeo tiene apoyo.

Top 5 del autor: editar en vez de discutir · ventana nueva al cambiar de tarea · compactar · desconectar MCPs/skills sin uso · elegir el modelo adecuado a la tarea.

## Verificación externa (gate de veracidad)

[VERIFICADO] **SpecJudge real**: GitHub `JoaquinRuiz/SpecJudge`, PyPI `specjudge`
v0.5.5 (publicada 04-sep-2026, attestation Sigstore, MIT), local-first con
Ollama (juez 8B local qwen3:8b/llama3.1:8b; specs nunca salen de la máquina),
catálogo 37 modelos en `data/models.yaml` con `pricing_date` verificable,
extensión aprobada en el catálogo comunitario de spec-kit. Coincide con el vídeo.

[VERIFICADO práctica] Captura real del autor (769.000 tokens de historial;
93 MCP tools a 0 tokens; skills siempre inyectadas). Coherente con el
funcionamiento de Claude Code y con el coste de catálogo de skills en system prompt.

[NO CONTRASTADO — no aplicable] Cifras «leer cache 10 %, escribir +25 %» son de
Anthropic. En DeepSeek el ratio es distinto (cache hit ~$0.007 vs miss ~$0.22
≈ 3 %): la política del lab de mantener cache hit sigue siendo correcta, pero
sin copiar porcentajes ajenos.

## Conexión con el lab

CONFIRMA (el lab ya lo tiene):
- **Prompt caching como palanca #1 de ahorro** = política combined-mode del lab (no romper cache hit).
- **Capa local delante de la API** (truco 11, su nivel más avanzado) = el lab ya la tiene montada: proxy :9911 + orquestador local-cloud + RAG + límites.
- **Traspaso autocontenido** (truco 4) = patrón SVP / state-verification-pattern / informes de cierre del lab.
- **Modelo según tarea** (truco 8) = `pipeline_seleccion_modelo.py` + `modelos_por_tarea.yaml` (SpecJudge es la variante por specs de spec-kit; el lab selecciona por tipo de tarea).

NUEVO / mejora potencial (accionable, sin urgencia):
- Auditoría de skills del lab (~150 en catálogo, todas viajan en system prompt cada turno) → watchdog `detectar-sin-uso`.
- Compactación guiada manual en puntos de corte naturales con instrucciones explícitas en sesiones largas.

## Valoración

MEDIO-ALTO como **confirmación de arquitectura**: valida que el lab va por
delante en la capa local y que su política de cache hit es correcta. No exige
implementar nada nuevo. 2 acciones menores opcionales (skills muertas,
compactación guiada). Autor con filosofía «medido en local, pantalla real, sin
humo» — afin al lab.
