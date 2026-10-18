---
title: "Análisis futurible: Memoria comercial desde llamadas (Tactiq→Claude, Javi Consuegra)"
type: research
fecha: 2026-08-20
---

# Análisis futurible: "Construye tu memoria comercial" (Javi Consuegra)

**VERACIDAD:** [VERIFICADO]
(LinkedIn Pulse, 20-ago-2026): https://www.linkedin.com/pulse/prompt-dentro-construye-tu-memoria-comercial-javi-consuegra-hhbqe/

**Pregunta:** ¿es futurible para el lab? ¿Qué aporta, qué duplica, con qué señal?

---

## La idea en 1 párrafo

Convertir las transcripciones de llamadas comerciales (el autor usa Tactiq,
pero vale cualquier herramienta con conector LLM/MCP: Fathom, Fireflies,
Otter) en un sistema que aprende de cada conversación:

```
llamada → transcripción → análisis estructurado → base de objeciones → activo comercial → mejor conversación
```

7 pasos concretos: (1) conectar la fuente; (2) sincronizar sin duplicar
(check "¿ya la trabajaste?" antes de analizar); (3) conservar el bruto como
evidencia; (4) enriquecer con estructura FIJA (objetivos deseados, criterios
de compra, lenguaje del comprador, personas implicadas, riesgos percibidos,
fase, objeciones, próximos pasos — CADA afirmación con su cita textual);
(5) base de objeciones con lenguaje LITERAL ("Nos preocupa pagar por una
herramienta que el equipo use solo las dos primeras semanas", no "objeción
de precio"); (6) informes de frecuencia/fase; (7) convertir lo que se repite
3+ veces en un activo (sección de presentación, correo, guion, contenido).

Reglas de higiene del autor: una objeción frecuente NO demuestra que cause
la pérdida (cruzarla con el resultado real); la memoria crece despacio
(evidencia repetida, no impresiones del último martes); dos ritmos (semanal
corto + mensual amplio); validar el prompt a mano 2 semanas antes de
automatizar (rutinas automáticas con prompt mal calibrado = ruido automático).

---

## Qué YA tiene el lab (anti-duplicado)

| Componente de la idea | ¿Ya existe en el lab? | Dónde |
|---|---|---|
| Transcripción de audio local | ✅ **faster-whisper en GPU** | skill `dictado-voz` (transcribir.py, CUDA) |
| Transcripción de vídeo/reuniones | ✅ VTT desde oEmbed | skill `video-transcription` (Vimeo/YT) |
| Pipeline de reuniones Teams | ✅ `hermes teams-pipeline` (resúmenes, action items, Graph) | skill `teams-meeting-pipeline` (sin credenciales MSGRAPH configuradas — setup pendiente) |
| LLM local para análisis | ✅ GLM/gpt-oss en LM Studio | router local (coste 0 tras 12:00) |
| Síntesis con citas | ✅ **deep_research.py (B7, hoy mismo)** | tools/deep_research.py + skill deep-research-lab |
| Análisis estructurado fijo | ✅ patrón ficha por patrón / 6 componentes (B6) | skill prompt-engineering |
| Memoria que persiste | ✅ memoria episódica MEP-001 + RAG | scripts/memoria-episodica.sh + lancedb |
| Base de objeciones con cita textual | ❌ NO existe | — |
| Activos comerciales generados desde objeciones | ❌ NO existe (el lab no vende aún) | — |

## Qué NO existe y sería nuevo

1. **Estructura de análisis de llamada comercial fija** (los 8 campos del paso 4)
   — nadie en el lab analiza conversaciones comerciales.
2. **Base de objeciones con lenguaje literal** + regla de promoción con
   evidencia (3+ repeticiones + relación con resultado).
3. **Bucle objeción → activo** (que una objeción repetida CAMBIE un material
   que se usa).
4. Los dos ritmos (semanal/mensual) aplicados a un dominio real.

## Viabilidad técnica en el lab (100% local, coste 0)

- **Alternativa local al conector Tactiq→Claude**: grabar/descargar el audio
  de la llamada → `transcribir.py` (faster-whisper GPU, ya existe) → el
  análisis estructurado con GLM local vía prompt 6 componentes (B6) →
  citas textuales verificables → base de objeciones en markdown/SQLite.
- **Tactiq/Fathom no hacen falta**: el lab ya transcribe local; lo único
  externo sería el consentimiento para procesar llamadas de clientes (regla
  del autor: "confirmar qué llamadas puedo procesar").
- **deep_research.py (B7) ya demuestra el patrón**: fuentes → síntesis con
  citas [S1..Sn] → informe con ahorro de contexto. La "memoria comercial"
  es el mismo patrón aplicado a llamadas: transcripción bruta → análisis con
  cita textual → base que crece.

## Señal de activación (cuándo merece la pena)

La idea ES futurible, pero el lab NO tiene aún llamadas comerciales que
analizar (el usuario está en búsqueda de empleo, no en venta B2B). La señal
real sería una de estas:

1. **Entrevistas de trabajo como "llamadas comerciales"**: si el usuario
   empieza a grabar (con permiso) sus entrevistas y quiere extraer
   objeciones del reclutador (criterios, riesgos percibidos, quién decide),
   el patrón aplica IDÉNTICO y es el caso de uso inmediato más realista.
2. **Reuniones Teams activas**: si se configuran las credenciales MSGRAPH
   (skill teams-meeting-pipeline, setup pendiente) y hay reuniones
   recurrentes que resumir con estructura.
3. **Si el usuario retoma venta/consultoría**: entonces la versión completa
   (objeciones → activos comerciales) cobra sentido de inmediato.

Sin ninguna de esas señales, construir el sistema completo hoy sería
"infraestructura esperando datos" — el anti-patrón que el propio lab
rechaza (verificar antes de construir).

## Qué NO hacer ahora

- No conectar Tactiq (herramienta cloud de pago) — el lab no la usa.
- No montar el pipeline completo de objeciones→activos (sin llamadas reales).
- No crear rutinas semanales/mensuales de análisis (no hay datos).

## Veredicto

**FUTURIBLE — con señal clara (caso de uso: entrevistas de empleo o venta
real).** La idea es sólida y el lab tiene el 80% de la infraestructura
(transcripción local + LLM + síntesis con citas + memoria persistente).
Lo que falta es el DOMINIO (llamadas reales). Cuando aparezca la señal
(entrevistas grabables con permiso, o reuniones Teams configuradas), el
pipeline se monta en horas: transcribir.py + prompt 6 componentes + base de
objeciones en markdown. La regla del autor más valiosa y generalizable:
"cada afirmación del análisis enlaza con su cita textual" — es la misma
disciplina de veracidad del lab (gate-veracidad, datos reales).

## Referencias futuras (señal de activación)

- **Caso 1 — entrevistas de empleo**: si el usuario quiere analizar sus
  entrevistas (con consentimiento), montar: audio → transcribir.py →
  estructura de 8 campos (objetivos/criterios/lenguaje/personas/riesgos/
  fase/objeciones/próximos pasos) → base de objeciones del reclutador.
  Es el arranque más barato y con retorno inmediato (mejora su búsqueda).
- **Caso 2 — Teams configurado**: si MSGRAPH se configura, reutilizar
  teams-meeting-pipeline + añadir el análisis estructurado sobre las
  transcripciones que ya llegan.
- **Caso 3 — venta/consultoría**: versión completa con activos comerciales
  (secciones de presentación, correos, guiones) según el ritmo semanal/
  mensual del autor.
- **Advertencia**: el conector Tactiq→Claude del artículo NO es necesario
  en el lab (local-first); no pagar por él.

## Registro

- Fuente: artículo LinkedIn Javi Consuegra (20-ago-2026), extraído completo.
- Relacionado: skills dictado-voz, video-transcription, teams-meeting-pipeline,
  deep-research-lab (B7), prompt-engineering (B6), gate-veracidad.
- Veredicto: FUTURIBLE con señal — no implementar sin datos reales.
