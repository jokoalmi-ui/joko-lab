---
title: "Análisis — Nichonauta: optimizar velocidad y razonamiento en llama.cpp (20-oct-2026)"
type: research
---

# Análisis — «Optimizar Modelos de IA con llama.cpp: MEJORAR la Velocidad y el Razonamiento»

**VERACIDAD:** [VERIFICADO] contra transcripción íntegra.

**Fuente**: https://youtu.be/MOfbqHDVxJ0 · canal **Nichonauta** · publicado **2026-10-20** · **11:02** · 5 vistas (leído 20-10-2026 con `yt-dlp --print`, exit 0).
**ID**: `MOfbqHDVxJ0` · **Transcripción**: `/tmp/clean_MOfbqHDVxJ0.txt` (12.708 B), mismas condiciones que el vídeo hermano (`nkoId8SX9mM`).

**Naturaleza de la fuente**: fragmento del **mismo directo** que el vídeo del 35B. Subtítulos automáticos: el ASR escribe «yubatch» donde el autor dice `ubatch`, y «MSP» donde dice MCP. Los nombres de flags se dan por su forma técnica, no por el audio.

## Relación con análisis previos del lab

| Previo | Fecha | Qué cubre ya |
|---|---|---|
| `research/analisis-nichonauta-llamacpp-optimizacion-20261009.md` (vídeo `zR7nPlyLQGo`) | 09-10-2026 | Precompilado vs compilar, `--moe-cache-mib`, multi-GPU/CUDA. **VALIDACIÓN**, no hallazgo |
| `research/analisis-nichonauta-ngram-mtp.md` y `research/analisis-nichonauta-speculative-decoding.md` | — | MTP / decodificación especulativa |

**Relación: MEJORA concreta.** No reanaliza el modelo ni el binario: mide **cuatro palancas de configuración** sobre la máquina del 35B.

## Las cuatro palancas, con las cifras del autor

1. **Cadena de razonamiento desactivada: 100 → 20.** «Si desactivo la cadena de razonamiento, pues va a ir lo que ahora tarda 100, sin cadena de razonamiento va a tardar 20». Sobre el coste: «Va a ser peor, sí, pero a lo mejor qué tanto peor».
2. **`batch`/`ubatch` de 4.000 a 8.000.** «estos nuevos ajustes de 8,000 en vez de 4,000 del batch y yubatch» con el resultado «está en el límite» — sigue cabiendo en 12 GB, sin margen.
3. **Slots en paralelo.** «si estoy haciendo una única respuesta, estoy generando 40 tokens por segundo. Si estoy generando dos respuestas, cada respuesta está generando 30 tokens por segundo. Sí, es menos, pero en total son 60». El caso que lo motiva: «cuando va a leer o escribir archivos, lo hace en distintos hilos» (Claude Code).
4. **Modelo intermedio en vez de extremos.** «si el 4B se me queda corto en inteligencia y el 35B en velocidad se me queda corto, necesito más velocidad, pues ejecuto el 9B, el intermedio».

Aviso de percepción incluido: la velocidad *aparente* depende de cuántas palabras caben por línea en la interfaz, así que comparar dos herramientas «a ojo» no mide nada.

## Encaje en el LAB

- **(1) razonamiento off** — aplicable ya, sin tocar nada: los pasos deterministas del orquestador (clasificar, resumir, extraer) no necesitan cadena de razonamiento. Es la palanca más rentable y la más barata de probar.
- **(2) batch/ubatch 8.000** — **no aplicable tal cual**: el lab sirve modelos con LM Studio, que no expone esos flags en la interfaz; exige `llama-server`/llama.cpp. Queda como pendiente si algún día se levanta llama.cpp aparte.
- **(3) slots** — LM Studio sí admite peticiones concurrentes. El orquestador y OpenCode hacen lecturas simultáneas, así que es **medible** con el material del lab. Falta la medición.
- **(4) el 9B intermedio** — ya está decidido en el lab con `qwen3.5-9b`; el vídeo lo confirma, no lo descubre.

## Veredicto

**MEJORA con coste 0 € en dos de las cuatro palancas** (razonamiento off y slots), **una no aplicable** con la arquitectura actual (batch/ubatch: LM Studio) y **una que ya estaba decidida** (modelo intermedio). No contradice el veredicto del 09-10 (aquel vídeo era validación de decisiones; este es ajuste fino).

Lo que este vídeo **no** aporta al lab: nada sobre cuantización, nada sobre MoE, nada sobre calidad medida con instrumento. Las cifras son lecturas de pantalla del autor.

## Lo que NO se ha verificado

- Los 100→20 y los 40/30/60 tok/s son del autor en **su** máquina (3060 12 GB + 64 GB RAM). No son medidas del lab.
- Ninguna de las cuatro palancas se ha probado aquí: **no se ha tocado LM Studio ni Ollama**.
- El efecto de `batch=8.000` en la A2000 es desconocido; el autor lo describe como «en el límite» en una tarjeta de la misma VRAM pero distinta arquitectura.
