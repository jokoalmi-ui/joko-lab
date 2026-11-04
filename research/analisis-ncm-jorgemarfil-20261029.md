---
title: "Análisis — Jorge Marfil: «¿Es El Fin De Los LLM? (NCM)» (29-oct-2026)"
type: research
---

# Análisis — «¿Es El Fin De Los LLM? (NCM)»

**VERACIDAD:** [VERIFICADO] contra fuente primaria (paper + repo + ficheros del modelo). Transcripción leída en su tramo final; las cifras se comprobaron en el paper, no en el audio.

**Fuente**: https://youtu.be/2BicjJgRkms · canal **Jorge Marfil** · publicado **2026-10-29** · **33:37** (2.017 s) · **12.031 vistas**, 420 likes (leído 29-10-2026 con `yt-dlp --print`, exit 0).
**ID**: `2BicjJgRkms` · **Transcripción**: `/tmp/ncm_trans.txt` (907 líneas, 39.491 B) · **Canal no vigilado** por `tools/monitor_yt.py`; el vídeo llega por aportación del usuario.

**Naturaleza de la fuente**: divulgación en español de un paper de Stanford. El autor **no amplifica el titular: lo desmonta** («NSM es un LLM… el titular lleva todo el rato respondiendo mal a su propia pregunta»). Novedad frente a la tónica del canal: cita cifras que se pueden comprobar y avisa de las que no.

**Paper primario**: *Next-Concept Modeling: Fast, Parallel Coarse-to-Fine Text Generation* · **arXiv 2610.14162** · enviado **2026-10-09 17:49:45Z** · Kumbong, Khare, Mlauzi, Woen, Ding, Buchanan, Arora, Mirhoseini, Ré (Stanford / HazyResearch). Código: `github.com/HazyResearch/ncm` (**MIT**, 1.262 ★, último push 2026-10-14). Pesos: `huggingface.co/hazyresearch/ncm-checkpoints` (última modificación 2026-10-16).

## Relación con análisis previos del lab

| Previo | Fecha | Qué cubre ya |
|---|---|---|
| `research/analisis-nichonauta-llamacpp-velocidad-razonamiento-20261020.md` | 20-10-2026 | Mismo eje (ancho de banda de memoria vs cálculo) desde llama.cpp: batch/ubatch, slots, tamaño de modelo |
| `research/analisis-nichonauta-speculative-decoding.md` | — | Otra vía de saltarse la lectura de pesos por token |

**Relación: VALIDACIÓN del eje + arquitectura nueva.** Aporta un cuarto camino, distinto de bajar precisión, especular o trocear el modelo: **escribir por niveles de abstracción en vez de token a token**.

## Cifras del vídeo, comprobadas contra el paper

- **31×** — XSum: NCM corre **31×** más rápido que **AURORA-LM** con **16× menos evaluaciones (NFE)**. §4.6 mide wall-clock de 1.024 secuencias, batch 16, **una H100 SXM 80 GB**.
- **21×** — LM1B: contra **DUO**, con **11× menos NFE** y mejor perplejidad generativa.
- **Nunca contra un autorregresivo**: §4.6 solo tabula DUO y AURORA-LM. La sección de eficiencia **no cronometra NCM frente a un modelo palabra a palabra**. El vídeo lo afirma y el paper lo respalda por omisión.
- **Sudoku (tabla 3), 25M de parámetros, tableros difíciles**: NCM **86,1 %** · autorregresivo *greedy* **1,0 %** · autorregresivo *sampling* 0,6 % · mejor difusión (FMLM+ 29M) **81,3 %**. NCM usa 12 NFE frente a 128 de casi todos los rivales.
- **Traducción WMT14 De→En (tabla 2)**: autorregresivo **25,2 BLEU** con 64 NFE · NCM **22,6** con 11 · NCM+MBR **25,2** con **132**. Empata, y pagando el doble de pasadas que el autorregresivo.
- **Resúmenes XSum (tabla 2)**: NCM **88M** → ROUGE-L **28,0** con **8 NFE** · AURORA-LM 130M → 26,6 con 128.
- **Techo de tamaño**: generadores de 97M / 317M / **725M** (escalado solo en LM1B). El resto se evalúa a ~100M.

## El «fichero de 5 bytes»: literal, pero con matiz

`owt/TODO.md` mide **exactamente 5 bytes** (`TODO\n`): el modelo de **texto web (OpenWebText)** no está publicado.

**Matiz que el vídeo no explicita**: sí hay pesos reales de **lm1b** (small/medium/large), **xsum**, **wmt14**, **tinystories** y **sudoku** (easy/medium/hard). Tamaños por `content-length`: `lm1b/large/generator.pt` **2.901.184.267 B (2,9 GB)**, `xsum` 354.355.211 B, `sudoku/hard` 102.560.203 B. Lo que falta es el modelo de propósito general, no todo el proyecto.

**Configuración del 725M** (`lm1b/large/config.yaml`): 36 capas, `n_embd` 1280, contexto 129, atención `block_diagonal`, **12 niveles** de jerarquía (`manual_levels` 1…128) y tokenizador VQ-VAE de 6 capas con vocabulario 8192 por nivel. El código publicado es **de evaluación** y recomienda CUDA.

## Lo que el vídeo omite (no inventa)

- Todo se mide a **~100M de parámetros**; no hay nada a 7B ni 70B.
- El empate en traducción llega vía **MBR** (generar varios candidatos y elegir), que cuesta más pasadas — el propio vídeo lo dice del 132 vs 64, pero no lo generaliza.
- El reparto de calidad de **DiffusionGemma** (69,1 vs 88,3 en AIME 2026; 69,1 vs 77,1 en LiveCodeBench V6) se cita de las cifras de Google; **no se ha verificado contra la fuente de Google en esta sesión**.

## Lectura para el lab

El argumento que importa es el de **ancho de banda**: escribir token a token obliga a releer todos los pesos en cada paso, y en local no hay miles de conversaciones con las que repartir ese coste. Pasar de ~1.024 lecturas de pesos (una por token) a 8–32 (una por nivel) ataca el cuello de botella real de la RTX A2000.

**No cambia ninguna decisión de compra ni de configuración hoy**: no hay NCM utilizable como chat. Queda como línea a seguir (jerarquía coarse-to-fine + decodificación paralela), no como herramienta.

## Fuentes consultadas (29-10-2026)

- `https://arxiv.org/html/2610.14162` — tablas 2 y 3, §4.6
- `https://export.arxiv.org/api/query?id_list=2610.14162` — título, fecha y autoría
- `https://api.github.com/repos/HazyResearch/ncm` — licencia MIT, estrellas, último push
- `https://huggingface.co/api/models/hazyresearch/ncm-checkpoints?full=true` — inventario de ficheros
- `https://huggingface.co/hazyresearch/ncm-checkpoints/raw/main/owt/TODO.md` — 5 bytes
- `https://youtu.be/2BicjJgRkms` — metadatos vía `yt_dlp --skip-download --print`
