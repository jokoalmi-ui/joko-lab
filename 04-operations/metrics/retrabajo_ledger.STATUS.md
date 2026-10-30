# retrabajo_ledger.jsonl — NO ES UN INSTRUMENTO (retirado 30-10-2026)

**Veredicto:** declarado **no-instrumento** por decisión explícita del usuario el
**30-10-2026 17:30 CET** (opción b del pendiente C del ciclo LPA semanal).
El fichero de datos **se conserva tal cual como evidencia**. No se borra, ni se
mueve, ni se edita ningún byte de `retrabajo_ledger.jsonl`.

## Por qué (medido, no estimado)

- **1 fila**, fechada **2026-09-25** (tipo E6, sesión `20260925_090159_b65803`).
  Instrumento: `wc -l retrabajo_ledger.jsonl` = 1 · `ls -l` = 566 B, mtime 25-09 13:29.
- **35 días congelado** a 30-10-2026, en 4 ciclos LPA consecutivos sin moverse.
- **0 productores**: ningún `.py` ni `.sh` del repo escribe en él
  (`grep -rln retrabajo_ledger --include=*.py --include=*.sh` → solo un script de
  investigación del 30-09 que **cuenta filas** para un informe; no escribe).
- **0 consumidores**: ningún cron, watchdog ni informe lo lee para decidir nada.
- Patrón aplicable: **CP-009 — un instrumento sin disparador no se usa**. Un ledger
  que solo avanza cuando un humano se acuerda de anotarlo no es un instrumento.

## Regla de lectura (obligatoria)

**Prohibido citarlo como dato de retrabajo.** «1 fila» no significa «poco
retrabajo»: significa **«sin instrumento»**. Cualquier informe, análisis o comparación
que use este fichero para afirmar una tasa de retrabajo está publicando un **falso ok**.

## Condición para revivirlo

Solo con las **dos** piezas a la vez, no una:

1. **Productor**: el punto del lab donde el retrabajo ya ocurre de verdad (ciclo EXP,
   iteración de una herramienta) escribe el asiento solo, sin que nadie lo recuerde.
2. **Consumidor**: algo se rompe o avisa si el fichero deja de recibir filas. Sin
   consumidor, su silencio es indistinguible del éxito.

Contraste medido el 30-10 que justifica la regla: el productor del informe diario
(con consumidores que se quejan cada día) se diagnosticó y se arregló en la misma
sesión en que se trató; este ledger, sin consumidor, llevaba 4 ciclos decidiéndose
sin moverse.

## Estado administrativo

Pendiente **C** del ciclo LPA del 23-10, reescalado el 26-10 y el 30-10 (tope
02-11-2026): **cerrado por esta vía** el 30-10-2026. No se reabre salvo que
existan productor **y** consumidor a la vez.
