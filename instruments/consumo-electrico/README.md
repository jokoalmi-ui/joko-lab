# Instrumento `consumo-electrico` — medidor solo-lectura de consumo eléctrico

**Versión:** v0.1 — 2026-10-11 CEST.
**Cierra:** el hueco 3 declarado en `tfm/ANEXO-METODOLOGICO-JOKO-LAB.txt:107-112` y 117
(«consumo eléctrico no medido»), en la versión **sin privilegios** elegida por el usuario.

## Restricción constitucional (molde `instruments/critic-loop`)

**NO modifica absolutamente nada**: no toca la config, no lanza ni para servicios, no
bloquea/limita/reintenta, no eleva privilegios. Solo **observar, medir y registrar**, y
escribe **únicamente dentro de su carpeta `outputs/`**. Sin umbrales a priori.

## Qué mide

- **GPU** (`nvidia-smi`, sin privilegio): potencia muestreada, media / mín / máx, **energía
  integrada** (Wh) por integración trapezoidal sobre las muestras reales, VRAM máxima y
  utilización.
- **RAPL** (`/sys/class/powercap/intel-rapl*`): estado de cada dominio y, **solo si
  `energy_uj` es legible sin privilegio**, energía (J) y potencia media de la ventana.
- **CPU** (`/proc/stat`, `/proc/loadavg`): **ocupación** (%), nunca vatios: sin RAPL no hay
  vatios de CPU y este instrumento no los estima.

## Qué NO hace

- No estima lo que no puede leer: lo declara `NO LEGIBLE`.
- No cubre discos, ventiladores, USB ni pérdidas de la fuente.
- La medida «de pared» exige un **medidor físico**: este instrumento no la sustituye.
- No calcula € salvo que se le pase `--precio-kwh` (y entonces solo cubre la energía de la GPU).

## Lecciones (v0.1.2)

1. **Arrancar el instrumento ANTES y pararlo DESPUÉS del trabajo.** Una ventana que no
   solapa con el trabajo mide **reposo**: ha ocurrido (corrida 2 del 11-oct) y queda
   registrada como falso negativo. No se interpreta una ventana sin marca de la carga.
2. **Cada muestra lleva hora absoluta** (`hora`) desde v0.1.2: sin ella, un tramo activo no
   se puede atribuir a un trabajo concreto (corrida 3 del 11-oct: actividad sin origen
   identificable). Para atribuir, se fecha el trabajo (`date`) y se cruza con la serie.
3. **La potencia no es un número, es una curva:** ~9,2 W en reposo, ~25 W en una pasada
   corta y aislada, **~66–68,8 W en inferencia sostenida** (98,2 % del límite de 70 W de la
   RTX A2000). Cualquier cifra única sin declarar el régimen está mal leída.
4. **RAPL está presente pero bloqueado** (6 dominios, `energy_uj` 0400 root): sin privilegio
   no hay vatios de CPU; **no se estiman**, se declara `NO LEGIBLE`.
5. El JSON individual guarda la **serie completa** de muestras; el JSONL guarda solo el
   agregado (histórico ligero).

## Uso

```bash
cd /home/jokoalmi/joko-lab
/usr/bin/python3 instruments/consumo-electrico/medir_consumo.py --ventana 30 --etiqueta "reposo"
/usr/bin/python3 instruments/consumo-electrico/medir_consumo.py --ventana 130 --etiqueta "bateria tool-calling"
/usr/bin/python3 instruments/consumo-electrico/medir_consumo.py --ventana 60 --etiqueta "inferencia" --precio-kwh 0.15
```

La ventana se muestrea **mientras ocurre el trabajo a medir**: el instrumento no lo lanza
(por la restricción de arriba), lo observa.

## Salidas

- `outputs/consumo-<AAAAMMDD_HHMMSS>.json` — corrida individual (registro completo).
- `outputs/consumo.jsonl` — append histórico (transversal, para comparar y detectar deriva).

## Límites de la medición (van siempre dentro del registro)

1. La potencia de GPU es muestreada con `nvidia-smi` e integrada con las muestras reales.
2. CPU/RAM/SoC solo son medibles por RAPL; si `energy_uj` no es legible, no se estiman.
3. No cubre discos, ventiladores, USB ni pérdidas de la fuente.
4. La medida de pared exige medidor físico.
