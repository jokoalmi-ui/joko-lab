#!/usr/bin/env python3
"""extraer_frames_escenas.py — Extrae frames INTELIGENTES de un vídeo/reel.

MEJORA 13-ago-2026: el método antiguo extraía frames cada N segundos
(fps=1/3) — podían caer en mitad del MISMO plano (frames redundantes).
Este script usa el filtro `scdet` de ffmpeg para detectar CAMBIOS DE ESCENA
y extrae un frame en cada momento donde el contenido cambia + un frame
adicional a mitad de cada escena larga (>5s) para no perder contexto.

USO:
    python3 extraer_frames_escenas.py <video.mp4> [dir_salida] [max_frames]
"""
import sys
import os
import subprocess
import re


def detectar_escenas(video: str, threshold: float = 0.3) -> list[float]:
    """Devuelve los tiempos (s) donde hay cambios de escena usando scdet."""
    cmd = [
        "ffmpeg", "-hide_banner", "-i", video,
        "-vf", f"scdet=threshold={threshold},metadata=print:key=lavfi.scd.score",
        "-f", "null", "-",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    # El filtro imprime "lavfi.scd.time: X" en los cambios de escena
    tiempos = []
    for line in proc.stderr.splitlines():
        m = re.search(r"lavfi\.scd\.time:\s*([\d.]+)", line)
        if m:
            # Sólo considerar scores altos (corte real, no fade suave)
            score_m = re.search(r"lavfi\.scd\.score:\s*([\d.]+)", line)
            if score_m and float(score_m.group(1)) > 1.0:
                tiempos.append(float(m.group(1)))
    return tiempos


def extraer_frame(video: str, t: float, salida: str):
    """Extrae un frame en el tiempo t (formato JPG)."""
    subprocess.run(
        ["ffmpeg", "-y", "-ss", str(t), "-i", video, "-frames:v", "1",
         "-q:v", "2", salida],
        check=True,
        capture_output=True,
    )


def main():
    if len(sys.argv) < 2:
        print("Uso: extraer_frames_escenas.py <video.mp4> [dir_salida] [max_frames]")
        sys.exit(1)

    video = sys.argv[1]
    salida_dir = sys.argv[2] if len(sys.argv) > 2 else "frames_escenas"
    max_frames = int(sys.argv[3]) if len(sys.argv) > 3 else 12

    os.makedirs(salida_dir, exist_ok=True)

    print(f"🎬 Detectando escenas en {video}...")
    escenas = detectar_escenas(video)
    print(f"   Cambios de escena en: {[f'{t:.1f}s' for t in escenas]}")

    # Duración total
    proc = subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
         "-of", "csv=p=0", video],
        capture_output=True, text=True,
    )
    duracion = float(proc.stdout.strip())

    # Puntos a capturar: cambios de escena + mitad de escenas largas
    puntos = [0.0] + escenas
    # Añadir mitad de escenas largas (>5s entre cambios)
    puntos_ordenados = sorted(set(puntos + [duracion]))
    extras = []
    for i in range(len(puntos_ordenados) - 1):
        inicio, fin = puntos_ordenados[i], puntos_ordenados[i + 1]
        if fin - inicio > 5:
            extras.append(inicio + (fin - inicio) / 2)
    todos = sorted(set(puntos + extras))

    # Limitar a max_frames
    if len(todos) > max_frames:
        # Mantener primero, último y distribuir el resto
        paso = (len(todos) - 2) / (max_frames - 2)
        indices = [0] + [int(1 + i * paso) for i in range(max_frames - 2)] + [len(todos) - 1]
        todos = [todos[i] for i in sorted(set(indices))]

    print(f"📸 Extrayendo {len(todos)} frames en: {[f'{t:.1f}s' for t in todos]}")
    for i, t in enumerate(todos, 1):
        salida = os.path.join(salida_dir, f"frame_{i:02d}.jpg")
        extraer_frame(video, t, salida)
        print(f"   [{i}/{len(todos)}] t={t:.1f}s → {salida}")

    print(f"\n✅ {len(todos)} frames extraídos en {salida_dir}")


if __name__ == "__main__":
    main()
