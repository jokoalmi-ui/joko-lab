---
title: "Reasoning Gate — diseño (PROPUESTA, sin adoptar)"
type: research
---

# Reasoning Gate — diseño (PROPUESTA, sin adoptar)
**VERACIDAD:** [ALCANCE INTERNO]

- Estado: PROPUESTA pendiente de revisión (revisar 07-ago-2026)
- Origen: análisis del usuario (Joseba), sesión CLI 06-ago-2026 noche
- Fecha (España): 2026-08-06. Evidencia de fecha: cron bolsa creado en la misma
  sesión con next_run 2026-08-07T22:30+02:00 (no verificado con `date`).
- Relación: conecta con SVP (Gate-001), KCR (Gate-005) y las lecciones 7/8 de
  gobernanza-conocimiento (memoria NO es fuente canónica; incidentes 0.19?,
  0.20.1, V003).

---

## 1. Diagnóstico (texto del usuario, transcrito)

> El problema no es simplemente "tirar de memoria". Es un fallo de procedimiento
> cognitivo: el modelo recupera una representación interna ("recuerdo") y la
> trata como evidencia suficiente, cuando el LAB exige que cualquier dato de
> estado sea validado contra la fuente de verdad.
>
> No es un fallo de memoria. No es un fallo de RAG. Es un fallo en el ORDEN del
> razonamiento. Detectado tres veces (0.19?, 0.20.1, V003).

## 2. Árbol correcto vs árbol real

Razonamiento correcto (lo que exige el lab):

```
Pregunta
  -> ¿La respuesta depende de un estado cambiante?
       NO  -> Responder
       SI  -> Identificar fuentes -> Consultar fuentes -> Resolver conflictos
              -> Construir respuesta -> Responder
```

Lo que hace el modelo hoy (3 veces detectado):

```
Pregunta -> "Recuerdo algo parecido" -> Responder
```

Se saltó cuatro pasos: identificar fuente, consultar fuente, resolver
conflictos, y la decisión misma de si el dato depende de estado.

## 3. Reglas propuestas (RULE-PROC-001..005, texto del usuario)

### RULE-PROC-001 — Memory is never evidence

Una representación interna del modelo nunca constituye evidencia. Si la
respuesta depende de: versiones, decisiones, configuración, estado, cron,
roadmap, pendientes, gobernanza, conocimiento vivo — queda prohibido responder
desde memoria. La memoria únicamente puede servir para LOCALIZAR la fuente,
nunca para sustituirla.

### RULE-PROC-002 — State First

Antes de escribir una sola línea debe ejecutarse este árbol:

```
¿La pregunta depende del estado del sistema? SI
-> ¿Existe fuente de verdad? SI
-> Consultar fuente -> Construir respuesta -> Citar fuente utilizada -> Responder
```

Si la fuente no se consulta: STOP. La respuesta no puede emitirse.

### RULE-PROC-003 — Memory Validation

Cada afirmación recordada debe clasificarse: MEMORIA -> ¿está verificada? NO ->
no puede utilizarse -> buscar evidencia -> solo entonces responder.

### RULE-PROC-004 — Suspicious Memory Trigger

Expresiones que disparan automáticamente verificación: "creo", "me suena",
"recordaba", "debería ser", "era", "0.19", "0.20", "última versión", "la
decisión fue", "si no recuerdo mal", "probablemente". Si aparece cualquiera:
OBLIGATORIO consultar fuente.

### RULE-PROC-005 — State Question Detector

Antes de responder, clasificar la pregunta:

- DESCRIPTIVA -> no necesita fuentes dinámicas
- ESTADO -> necesita fuentes vivas
- HISTÓRICA -> necesita Decision Log
- CONFIGURACIÓN -> necesita configuración real
- OPERATIVA -> necesita estado actual

Cada tipo tiene un procedimiento distinto.

## 4. Checklists (pre-reasoning y post-reasoning)

PRE (antes del razonamiento, no después):

- [ ] ¿La pregunta depende de estado?
- [ ] ¿Existe una fuente viva?
- [ ] ¿La he consultado?
- [ ] ¿La respuesta contiene algún dato recordado?
- [ ] ¿Está verificado?

Si alguna respuesta es NO -> STOP.

POST (al terminar):

- [ ] Todas las afirmaciones de estado tienen fuente
- [ ] No quedan hipótesis sin marcar
- [ ] No hay versiones recordadas
- [ ] No hay decisiones recordadas
- [ ] No hay configuración recordada

## 5. Verifier específico — SVP PROCEDURE CHECK

El Verifier no mira el contenido; mira el PROCEDIMIENTO:

```
Documento:      ...
Pregunta:       ...
Tipo:           ...
Fuentes requeridas:   ...
Fuentes consultadas:  ...
Afirmaciones de estado: ...
Afirmaciones verificadas: ...
Afirmaciones desde memoria: ...
Resultado: PASS / FAIL
```

## 6. Métricas metacognitivas nuevas (MEL)

MEL no debe preguntarse "¿la respuesta fue correcta?" (eso ya lo hace el
benchmark). Debe preguntarse "¿CÓMO llegué a esa respuesta?":

- ¿Cuántas respuestas utilizaron memoria?
- ¿Cuántas verificaron?
- ¿Cuántas omitieron una fuente?
- ¿Cuántas fueron corregidas posteriormente? ¿Por qué?

Métricas propuestas:

- **MOR — Memory Override Rate**: respuestas donde la memoria inicial fue
  sustituida por evidencia verificada. MOR = overrides / consultas de estado.
- **MTE — Memory Trust Error**: respuestas emitidas desde memoria que luego
  necesitaron corrección. MTE = errores_por_memoria / respuestas_desde_memoria.

No evalúan el contenido, sino la calidad del proceso de razonamiento.

## 7. Observación final del usuario (el cambio arquitectónico)

Flujo actual: Recuperar conocimiento -> Razonar -> Verificar.
Falta un paso intermedio: Recuperar -> CLASIFICAR (memoria vs estado) ->
Verificar si procede -> Razonar -> Verificar procedimiento.

> No añade otra capa funcional al procesamiento del conocimiento; introduce una
> disciplina de ejecución que obliga a razonar sobre la procedencia de la
> información antes de construir la respuesta. Es lo que una capa metacognitiva
> puede medir y mejorar de forma continua.

## 8. Análisis del agente (conexión con lo que ya existe)

- **Ya cubierto en parte por el lab**: SVP (Gate-001) distingue conocimiento
  descriptivo vs estado y exige state_sources; la lección 7 de
  gobernanza-conocimiento ya establece "la memoria persistente NO es fuente
  canónica para conocimiento de estado" (casos 0.19?, 0.20.1, V003); KCR
  (Gate-005) fuerza el orden de consulta del RAG.
- **Lo NUEVO de esta propuesta** respecto al lab actual:
  1. RULE-PROC-004: disparadores LINGÜÍSTICOS de duda ("creo", "me suena",
     "debería ser"...) — el SVP actual dispara por marcadores en documentos
     (?, TODO, pendiente), no por expresiones de incertidumbre en el
     razonamiento del agente.
  2. RULE-PROC-005: clasificador de TIPO de pregunta (descriptiva/estado/
     histórica/config/operativa) como gate de entrada, antes de razonar.
  3. Verifier de PROCEDIMIENTO sobre respuestas (SVP Procedure Check), no solo
     sobre documentos.
  4. MOR/MTE: métricas de proceso, extensión natural de MEL-2 (procedimental).
- **Riesgos / a decidir**:
  - RULE-PROC-004 puede generar falsos positivos ("creo" retórico): calibrar
    como "marcar para verificar", no bloqueo automático.
  - MOR/MTE necesitan instrumentación propia (ledger de respuestas con
    clasificación memoria/verificada). NO tocar mel_ledger.jsonl (Architecture
    Freeze; PIL ya supervisa sin mezclar).
  - Si se adopta como gate nuevo: requiere EVF (diseño -> EXP -> BENCHMARK ->
    ADOPTADO -> RULE), como cualquier evolución (freeze vigente).
  - Alternativa a evaluar: integrarlo en SVP existente en vez de gate aparte
    (menos superficie, mismo principio: "la consulta es obligatoria y un gate
    verifica que ocurrió").
- **Veredicto preliminar**: el diagnóstico es correcto y ya tenía registro
  parcial en el lab (lecciones 7/8). La propuesta lo sistematiza como
  procedimiento obligatorio con disparadores explícitos y métricas de proceso.
  La decisión de mañana: formalizar como gate EVF o ampliar SVP.

## 9. Segundo análisis del usuario (06-ago, misma sesión): caso A2A y Evidence Arbitration Layer

### 9.1 El caso A2A es el mejor caso de prueba

El incidente "¿Tiene Hermes A2A?" evidencia exactamente el defecto que se
quiere eliminar. Secuencia CORRECTA que debería haber ocurrido:

```
Pregunta: "¿Tiene Hermes A2A?"
  -> Clasificación: ¿es conocimiento estable? NO -> es conocimiento de ESTADO
     (versión instalada)
  -> Buscar fuente: pendientes.txt / decision log / estado del LAB
  -> La fuente dice: "Hermes 0.17.0. Esperar 0.20.1"
  -> Responder
```

Proceso que se EJECUTÓ:

```
Pregunta -> Activación de memoria "Hermes 0.20" -> Asociación
"0.20 incorpora A2A" -> Responder. Sin ninguna validación.
```

### 9.2 El error no es decir "0.20"

Decir "0.20" sería un error factual. El error de procedimiento es más grave:
el sistema dio PRIORIDAD A LA MEMORIA INTERNA sobre la fuente de verdad del
LAB. Eso viola la disciplina que el lab está construyendo.

### 9.3 Las piezas existentes deberían intervenir así (según el usuario)

- **KAP**: debe clasificar inmediatamente Tipo: Estado (no Tecnología).
- **KVC**: debe preguntar ¿existe evidencia? SI -> ¿ha sido consultada?
  NO -> FAIL.
- **KEL**: no interviene todavía.
- **MEL**: debe registrar el incidente: Tipo: Memory Override Failure;
  Causa: no se consultó la fuente; Consecuencia: respuesta incorrecta;
  Acción: modificar procedimiento.

### 9.4 La capa nueva: Evidence Arbitration Layer (Memory Arbitration)

Lo que todavía no está formalizado: no basta decir "consulta la fuente".
Debe existir un componente que pregunte: ¿TENGO PERMISO PARA UTILIZAR MI
MEMORIA? Ese componente no existe.

Su única responsabilidad sería decidir:

```
¿Memoria suficiente? -> NO -> Consultar fuente -> Ahora sí puedes razonar
```

Es distinto del RAG, del KVC y del MEL. No evalúa contenido. No evalúa
calidad. ARBITRA qué conocimiento puede entrar en el razonamiento.

### 9.5 Patrón común de los tres fallos (cadena causal única)

Los tres incidentes (0.19?, 0.20.1, V003) tienen la misma estructura:

```
Información en memoria -> parece coherente -> no se consulta la fuente
-> se responde -> posteriormente aparece la contradicción
```

No son tres errores independientes: son tres manifestaciones del MISMO
defecto procedimental. En ingeniería de calidad, cuando varios fallos
comparten la misma cadena causal, se corrige la cadena, no cada síntoma.
La cadena es:

```
Memoria -> (ningún arbitraje) -> Razonamiento -> Respuesta
```

La corrección con SVP + Procedural Gates + EVF va en la dirección adecuada:
introducir un punto de control que impida que una representación recordada
se convierta en evidencia sin pasar antes por una fuente verificable cuando
la pregunta depende del estado. Ataca la causa raíz, no solo el error
concreto "Hermes 0.20".

### 9.6 Análisis del agente sobre esta capa

- La Evidence Arbitration Layer es el nombre formal del gate de entrada que
  pedía el primer análisis: la pieza que falta entre clasificar y razonar.
  Encaja como capa de PROCEDIMIENTO (no de contenido), igual que SVP/KVC/PIL.
- Estado actual en el lab: KAP no tiene especificación formal todavía
  (gate-003-kvc.md lo declara); esta propuesta le asigna su primera
  responsabilidad operativa: clasificación de tipo en la entrada.
- El SVP Procedure Check (sección 5) sería el verifier natural de esta capa:
  comprobar que el arbitraje ocurrió (fuentes requeridas vs consultadas),
  no fiarse de que "parece bien".
- Riesgos: (1) no duplicar SVP — SVP ya exige state_sources y marcadores
  para DOCUMENTOS; la capa nueva aplica al RAZONAMIENTO del agente antes de
  responder; (2) no convertirla en otro ledger — es un punto de control,
  no un registro más; (3) Architecture Freeze: componente nuevo -> EVF
  obligatorio si se adopta.
- Pregunta a decidir: la capa es (a) componente propio, (b) el nombre
  operativo de lo que KCR/context_builder ya hace parcialmente (priorización
  de conocimiento gobernado), o (c) formalización del SVP aplicado al
  razonamiento. La respuesta cambia el alcance del EVF.

## 10. Pendiente para mañana (07-ago-2026)

1. Leer este diseño.
2. Decidir vía: (a) gate nuevo con EVF, (b) ampliación de SVP (Gate-001), (c)
   solo instrumentar MOR/MTE en MEL-2 primero, o (d) formalizar la Evidence
   Arbitration Layer (sección 9.4) como capa de arbitraje de memoria.
3. Si se adopta algo, seguir el ciclo EVF (baseline ANTES con modelo comparable,
   no inventar resultados) y registrar la clase de defecto.
4. No tocar mel_ledger ni añadir componentes sin cerrar el freeze (2 evoluciones
   completas pendientes).
