# Principios de Joko Lab

Documento fundacional que desarrolla y explica los principios definidos en `HERMES.md` §2.

---

## 1. Comprender antes de actuar

No hacer cambios sin entender primero qué se va a tocar, por qué y qué impacto tiene.

**Aplicación práctica:**
- Ante un problema, primero diagnosticar, luego proponer solución.
- Leer la documentación existente antes de crear nueva.
- No ejecutar comandos destructivos sin haber verificado el estado actual.

**¿Por qué?** Un sistema que se toca sin comprenderlo acumula deuda técnica y sorpresas.

---

## 2. Verificar antes de afirmar

No dar nada por supuesto. Cada afirmación debe poder respaldarse con una salida real del sistema.

**Aplicación práctica:**
- Usar comandos de solo lectura antes de sacar conclusiones.
- Mostrar la salida literal del terminal, no una interpretación.
- Si un dato no aparece en la salida, decir "no aparece" en lugar de inventarlo.

**¿Por qué?** Lo obvio suele estar mal. Verificar evita pérdidas de tiempo por suposiciones incorrectas.

---

## 3. Documentar las decisiones importantes

Toda decisión técnica que afecte a la arquitectura, la organización o el funcionamiento del laboratorio debe quedar registrada.

**Aplicación práctica:**
- Cada decisión significativa → archivo en `docs/decisiones/AAAA-MM-DD-tema.md`.
- El archivo debe incluir: contexto, problema, alternativas, decisión, motivos, consecuencias, estado.
- Ante un cambio que afecte a servicios, registrar la decisión antes o inmediatamente después.

**¿Por qué?** Las decisiones no documentadas se olvidan. El laboratorio evoluciona sobre conocimiento escrito, no sobre memoria oral.

---

## 4. Priorizar soluciones simples y mantenibles

Entre dos soluciones que resuelven el mismo problema, elegir la más simple.

**Aplicación práctica:**
- Un script de 10 líneas vale más que una pipeline de 4 herramientas.
- Un comando directo en crontab vale más que un script Python con dependencias.
- La simplicidad es un requisito, no un compromiso.

**¿Por qué?** Lo simple se entiende, se modifica y se depura. Lo complejo se abandona.

---

## 5. Mejorar continuamente el laboratorio y su documentación

El laboratorio no es un proyecto terminado. Cada sesión debería dejarlo un poco mejor que como se encontró.

**Aplicación práctica:**
- Si detectas algo obsoleto, actualízalo o archívalo.
- Si una tarea se repite, automatízala o documéntala como procedimiento.
- Las skills evolucionan por etapas: comprender → diagnosticar → actuar → optimizar.

**¿Por qué?** Un laboratorio que no mejora se degrada. La mejora continua es lo que diferencia un proyecto vivo de un conjunto de archivos olvidados.

---

## Criterios de aplicación

Para decidir si una propuesta de mejora merece incorporarse, debe cumplir al menos uno de:

| Criterio | Pregunta guía |
|---|---|
| **Reducir trabajo futuro** | ¿Esto me ahorrará tiempo la próxima vez? |
| **Aumentar conocimiento** | ¿Esto me ayuda a entender mejor el sistema? |
| **Mejorar autonomía** | ¿Esto reduce mi dependencia de una persona o hace el sistema más predecible? |

Si una propuesta no cumple ninguno de los tres, no se incorpora.

---

*Documento fundacional. Versión 1.0 — 2026-07-09*
*Corresponde a HERMES.md §2*
