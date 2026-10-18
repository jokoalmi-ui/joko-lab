---
title: "Indice de Knowledge Objects — Joko Lab"
type: verification
---

# Indice de Knowledge Objects — Joko Lab
# scope: decisions_rules_policies_only
# NOTA PARA EL AGENTE: este indice cubre SOLO el scope declarado arriba.
# Si la pregunta cae fuera de ese scope, NO concluyas 'no existe' —
# consulta el RAG antes de responder que algo no esta incluido.

- DEC-001 [DEC/activo]: Qwen 3.5 descartado como modelo principal tras 0/5 tests. No usar bajo ninguna circunstancia. Ver [[RULE-004]]. — DEC-001.yaml
- DEC-002 [DEC/activo]: DeepSeek R1 destilado en Qwen 14B para tareas de razonamiento paso a paso. Límite de tokens: max_tokens 2048 (nunca menos, nunca 512/768/1024). Ver [[RULE-003]]. — DEC-002.yaml
- DEC-003 [DEC/activo]: Gemma 4 12B para tareas creativas (poemas, relatos, brainstorming). Ver [[RULE-001]]. — DEC-003.yaml
- DEC-GAIPRO-001 [DEC/active]: # Estrategia Google AI Pro (~20 EUR/mes)

Objetivo: sacar el maximo rendimiento a la suscripcion Google AI Pro,
usandola SOLO donde es insuperable, y dejando lo automatizable en local
(Hermes + RAG + crons, ya pagado). Decision con datos al mes.

## Que incluye el plan (verificado 2026-08-03)

- Gemini 3.1 Pro en gemini.google.com con limites muy superiores al gratis
- Gems: asistentes personalizados (se usan en la web, manualmente)
- NotebookLM Plus: cuadernos con mas fuentes + podcasts de audio (Deep Dive) + guias
- Deep Research (informes largos), Gemini Live (voz), Canvas, Google Flow, imagenes
- Integracion Workspace: Gemini en Gmail, Docs, Drive

## Que NO incluye

- Creditos de API. La Gemini API (AI Studio) se paga aparte; su free tier
  cubre uso ligero sin coste. No pagar la suscripcion esperando API.

## Reparto de tareas

| Tarea | Donde | Por que |
|---|---|---|
| Documentos enormes / contexto 1M (papers, juicio, informes largos) | Gemini web (3.1 Pro) | Capacidad que el local no alcanza |
| Investigacion larga con informe | Gemini web (Deep Research) | Exclusivo del plan |
| Asistentes personalizados manuales | Gemini web (Gems) | Equivalente web de las skills de Hermes |
| Cuadernos de fuentes + podcasts de audio | NotebookLM Plus | No replicable local |
| Resumir/redactar en Gmail y Docs | Gemini en Workspace | Integracion nativa |
| Pipelines, RAG, crons, skills, monitorizacion | Local (Hermes) | Ya pagado y automatizable |
| Automatizacion puntual con Gemini (vision de fotos, etc.) | API AI Studio (free tier) | No requiere pagar |

## Gems candidatos

- Analista de papers: resumir y extraer evidencia (nivel, dosis, resultados)
- Resumidor de documentos del juicio
- Consultor de suplementos: dosis vs evidencia (en paralelo a biohacking)
- Revisor de entregables Founderz
- Asesor de compras de perfume (en paralelo a perfume-ia, con la BD)

## Cuadernos NotebookLM rentables

- Biohacking: las 12 fuentes curadas + papers nuevos + registros
- Juicio: documentos y piezas (resumen + busqueda en las fuentes)
- Founderz: material de modulos
- Perfume IA: reviews de Parfumo/Fragrantica (alternativas)

## Registro mensual de uso (rellenar en 04-operations/registro-uso-gemini.md)

| Semana | Tareas exclusivas en Gemini web | Valor (1-5) | Alternativa local? | Notas |
|---|---|---|---|---|
| 1 (03-09 ago) | | | | |
| 2 (10-16 ago) | | | | |
| 3 (17-23 ago) | | | | |
| 4 (24-30 ago) | | | | |

## Regla de decision (dia ~30, next_review 2026-09-03)

- Uso real de lo exclusivo (3.1 Pro / NotebookLM / Deep Research) >= 3-4 veces
  por semana -> mantener la suscripcion
- Uso trivial (chat normal que el local cubre) -> considerar Google AI Plus
  (escalon mas barato) o plan gratis + API free tier
- Decidir con datos, no por impresion
 — DEC-GAIPRO-001.yaml
- POLICY-001 [POLICY/activo]: Nunca usar un modelo si existe un FATAL activo que lo bloquea. Ejemplo: [[RULE-004]]. — POLICY-001.yaml
- POLICY-002 [POLICY/activo]: No exponer datos sensibles a proveedores cloud. Ver [[POLICY-001]] (regla general de uso). — POLICY-002.yaml
- PRED-001 [PRED/pendiente]: PRED-001 — PRED-001.yaml
- PRED-002 [PRED/pendiente]: PRED-002 — PRED-002.yaml
- PRED-0XX [PRED/pendiente]: PRED-0XX — PRED-template.yaml
- RULE-001 [RULE/activo]: Usar Gemma 4 (google/gemma-4-12b-qat) para tareas de creatividad, brainstorming y código completo. Modelo recomendado para creatividad. Ver [[DEC-003]]. — RULE-001.yaml
- RULE-002 [RULE/activo]: Usar Granite 4.1 temp=0.3 para JSON estructurado. Ver [[RULE-001]] para alternativas de creatividad. — RULE-002.yaml
- RULE-003 [RULE/activo]: Usar DeepSeek R1 para razonamiento paso a paso. Ver [[DEC-002]] (límite de tokens). — RULE-003.yaml
- RULE-004 [RULE/activo]: Bloquear Qwen 3.5 — descartado (0/5 tests). Ver [[DEC-001]] (decisión original). — RULE-004.yaml
- RULE-005 [RULE/activo]: Actualizar GUIA-JOKO-LAB.md ante cada cambio estructural del laboratorio, en la misma sesion. Origen: norma JL-013 (lpa/constitucion/normas-jl.md). — RULE-005.yaml
- RULE-006 [RULE/draft]: Recibo SHA obligatorio antes de commit en hermes-lab. Ningun commit se acepta si el arbol de cambios en staging no coincide con el hash de un recibo generado tras revision explicita. Un solo byte distinto invalida el recibo. Blindaje determinista contra cambios silenciosos de agentes (Hermes, Claude Code, o cualquier otro). Concreta el Evidence Contract del lab: no confiar en que el agente reporte 'esta bien', exigir comprobacion externa atada a algo inmutable.

MECANISMO
1. Congelar: hash del arbol en staging con `git write-tree` (nativo de Git, determinista). Identifica esos bytes exactos, no 'el cambio' en abstracto.
2. Revisar: humano o Hermes confirma que el diff corresponde EXACTAMENTE a lo solicitado (nada mas, nada menos).
3. Generar recibo: hooks/generar_recibo.sh <nombre> [nota] escribe hash + aprobado_por + timestamp en .git/joko-recibo.json (fuera de control de versiones).
4. Gate: el hook pre-commit recalcula el hash del staging; si no hay recibo o el hash diverge (se toco algo despues de revisar), el commit se bloquea.

INSTALACION (2026-08-03)
- Hook activo en hermes-lab: core.hooksPath=hooks; ficheros hooks/pre-commit y hooks/generar_recibo.sh.
- fin.sh (checkpoint de cierre) usa JOKO_RDD_DISABLE=1 explicito en su commit automatico (linea 150): bypass documentado y visible, no silencioso.

KILL SWITCH
- JOKO_RDD_DISABLE=1: desactiva el gate una sola vez (aviso en el log del hook).
- Fichero .joko-rdd-disable en la raiz del repo: desactiva para todo el repo (aviso).
- Nunca bypass implicito por patron de mensaje (p.ej. prefijo 'checkpoint:' en el hook).

ALCANCE
- Solo hermes-lab (repo git). joko-lab NO es repo git (verificado 2026-08-03); si algun dia se versiona con git, la regla aplicara automaticamente.

LIMITES CONOCIDOS
- No sustituye la revision humana/de Hermes, solo la hace vinculante una vez hecha.
- No verifica CALIDAD del cambio, solo identidad de bytes del arbol en staging.
- No detecta archivos nuevos sin `git add` (solo certifica el staging, no el working tree completo).
- git commit --no-verify se salta el hook por diseno de Git (barrera de proceso, no criptografia).
- El recibo vive en .git/ (no versionado, no viaja a clones) — intencional: cada checkout revisa lo suyo.

VALIDACION PENDIENTE
- Probar 1-2 semanas en repo real antes de pasar status a 'active'.
- Confirmar que no genera friccion excesiva en el flujo diario (mismo riesgo que inicio.sh). — RULE-006.yaml
- RULE-007 [RULE/activo]: Antes de modificar un archivo existente sin versionar en git, crear copia de seguridad (cp archivo archivo.bak-YYYYMMDD). Prohibido write_file (reemplazo completo) sobre archivo existente sin backup previo. Para anadir contenido usar patch/append. Excepcion: archivos trackeados en git con commit previo. Origen: norma JL-014 (lpa/constitucion/normas-jl.md). — RULE-007.yaml

# Total: 16 objetos indexados (scope: decisions_rules_policies_only)