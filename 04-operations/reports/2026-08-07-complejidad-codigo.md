---
title: "Complejidad ciclomática del código del lab (2026-08-07)"
type: operations
---

# Complejidad ciclomática del código del lab (2026-08-07)

Fecha: 2026-08-07
Herramienta: tools/complejidad_crap.py (AST puro, sin dependencias)
Método: McCabe (1 + puntos de decisión: if/for/while/except/assert/and/or/ifs en comprehensions)
Scripts analizados: tools/*.py (46 archivos, 264 funciones)

## Resultado

- Total funciones: 264
- Complejas (11-20): 37 (14%)
- Muy complejas (>20): 9 (3.4%)
- Resto (≤10, mantenible): ~82%

## Top 9 muy complejas (>20)

| Complejidad | Función | Nota |
|---|---|---|
| 52 | knowledge_health.py audit() | La más compleja del lab; probablemente mezcla varias responsabilidades |
| 36 | observer.py main() | |
| 30 | context_builder_estructurado.py extraer_resumen_estructurado() | |
| 30 | migrate_to_ko.py migrate_dec() | |
| 26 | verificar_fk_kos.py escanear_ko() | Integridad referencial |
| 23 | knowledge_resolver.py format_synthesis() | |
| 22 | activation_engine.py activate() | Zona del bug condicion:null (04-ago) |
| 22 | indexer.py load_notes_con_hash() | Zona del lío del sidecar (05-ago) |
| 21 | indexer.py build_index() | Zona de recreación de índices (05-ago) |

## Interpretación

- El lab está sano en general: 82% del código en zona mantenible.
- Las 9 muy complejas coinciden con los scripts que ya dieron problemas reales
  (indexer, activation_engine) — la métrica valida empíricamente dónde está el
  riesgo de cambio.
- No es obligación refactorizar: es señal para priorizar revisión/gates.
- knowledge_health.audit() (52) es el candidato más claro a dividir en
  responsabilidades si se toca.

## Límite honesto

Esto es COMPLEJIDAD, no CRAP completo. CRAP = complejidad × (1 - cobertura);
sin tests unitarios de tools/ la cobertura es ~0, así que CRAP se degradaría a
complejidad. CRAP completo requiere primero infraestructura de tests (tarea
futura de otro tamaño). La complejidad es el primer factor de CRAP y la señal
accionable hoy.

## Uso

```bash
~/.venv/hermes-rag/bin/python3 ~/joko-lab/tools/complejidad_crap.py            # ranking completo
~/.venv/hermes-rag/bin/python3 ~/joko-lab/tools/complejidad_crap.py --top 15    # solo las peores
~/.venv/hermes-rag/bin/python3 ~/joko-lab/tools/complejidad_crap.py --json      # salida para L2/ledger
```

Solo lectura. No modifica nada.
