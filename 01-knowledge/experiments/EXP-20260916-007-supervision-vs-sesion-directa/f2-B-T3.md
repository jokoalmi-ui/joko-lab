# EXP-20260916-007 — F2 celda B(T3): servir un MoE de 22,6 GB en 12 GB de VRAM (swarm)

- **Fecha**: 2026-09-16, ventana **16:13 → 16:31 CEST** (18 min de reloj).
- **Modo**: B — swarm supervisado, tenant `exp007-f2-t3`. Topología: root/blackboard `t_f79b035d` → worker `t_48af067f` → verifier `t_4ada7aff` (gate PASS 16:24) → synthesizer `t_fe011ec3` (informe final 16:31).
- **Tarea T3**: idéntica a A(T3) — cómo servir un MoE de 22,6 GB (Qwen3.6-35B-A3B Q4_K_M) en una GPU de 12 GB por offload de capas, con fuentes y cita literal.

## Coste y latencia (medidor, tarifa oficial)

| métrica | valor |
|---|---|
| llamadas | **135** |
| prompt tokens | **9.559.678** |
| completion tokens | 161.943 |
| **coste** | **0,214731 USD** (cota superior) |
| ttfb_total | 16.934,2 s |
| total_ms_total | 899,0 s |
| ttfb medio | 894,8 ms |
| latencia media por llamada | 6.659,3 ms |
| líneas sin desglose de caché | 4 → contadas como *miss* |

**Limitación del instrumento de coste (declarada)**: la ventana 16:13–16:31 incluye también el tráfico de mi propia sesión directa, así que el coste de B es **cota superior, nunca 0**. Igual que en B(T2).

## Calidad (instrumento objetivo: `curl` + cita literal, **v3 corregido**)

- **12 claims reales → 12/12 PASS (100 %)**. 12/12 URLs HTTP 200. **0 antibot.**
- **Control negativo** (cita inventada «quantum entanglement drafters…») → correctamente **no encontrado**.
- Detalle de vías: 10 por coincidencia exacta + 2 por la vía nueva `crudo` (ver nota de instrumento abajo).

## Entregables

- Síntesis final: **253 líneas / 22.126 B** (workspace 22.065 B, sha256 `813a896b50fa58fe2dcb1e69701c101bfdac822a02b9a2f7d78a9922ebee2746`).
- Informe del worker: `informe-moe-expertos-en-cpu.md` **20.787 B**.
- Verificación del verifier: `verificacion-t_48af067f.md` **12.518 B**.

## Qué aportó el swarm más allá de A(T3)

1. **Gate de verificación en vivo con re-fetch al commit exacto** `dfe45163e1c98491bbd7ccab4339422ea3f80100` (no a `master`), más ficheros locales de la instalación LM Studio.
2. **Dos correcciones obligatorias aplicadas antes de cerrar**:
   - Se eliminó una afirmación falsa del propio informe (la advertencia «highest numbered» **sí** está en el gist; una búsqueda de subcadena fallaba por el marcador de cursiva entre las dos palabras). Además corrigió el propietario real del gist: `DocShotgun`, no `Doctor-Shotgun`.
   - Separó explícitamente **VERIFICADO** (nombre y contrato del campo del SDK + ausencia del parámetro en la REST) de **NO VERIFICADO** (comportamiento efectivo del slider 0.4.x, descrito solo por informes de usuario).
3. **Un hallazgo material que A(T3) no detectó**: la guía de HF advierte que `--n-cpu-moe` cuenta «desde las capas de numeración más alta», pero el **código** del commit (`i = 0..N-1`) implementa **las primeras N**, y el ejemplo de la propia guía (`-ot blk.(0..30)` + `--n-cpu-moe 31`) confirma las primeras N. **La guía se contradice a sí misma**; A(T3) se quedó con la advertencia de la guía sin contrastarla con el código.
4. **5 residuales declarados sin verificar** (en vez de rellenarlos): texto de la UI de 0.4.x, recuento de ficheros de #15191, cita de `#1454`, conversión ratio→N en LM Studio, y cuál de las dos asignaciones de `LLAMA_VERSION` aplica al build instalado.

## Nota de instrumento (v2 → v3)

La medición con el medidor **v2** daba 11/12. El claim descartado (`--n-cpu-ffn`) es un **falso negativo del instrumento**: `norm()` aplicaba `re.sub(r"<[^>]+>", " ")` para limpiar HTML, pero en fuentes de código C++ los `<`/`>` son operadores y ese patrón borraba tramos enteros del texto. Verificado: la cita está literalmente en el fichero del commit (comprobado con `grep` y con Python sobre el crudo). Con la pasada `crudo` del v3 → **PASS**.
