#!/usr/bin/env python3
"""watchdog_salud_sistema.py — Vigilancia de salud del PC (patrón servidor).

Métricas vigiladas:
- Swap usado % (umbral aviso 80, alerta 92)
- Zombies (cualquiera = aviso)
- Procesos con >500 MB en swap (residuos de memoria)
- RAM disponible (umbral aviso <1.5 GB, alerta <0.8 GB)
- Uptime (aviso >48 h, alerta >72 h)

Salida: SILENCIO si todo OK (patrón watchdog).
        Mensaje claro si algo supera umbral (se entrega a Telegram).

Uso: python3 watchdog_salud_sistema.py
"""
import os
import re
from datetime import datetime

AVISO_SWAP = 80
ALERTA_SWAP = 92
AVISO_RAM = 1.5  # GB disponibles
ALERTA_RAM = 0.8
AVISO_UPTIME_H = 48
ALERTA_UPTIME_H = 72
SWAP_PROCESO_MB = 500  # aviso si un proceso usa más de esto en swap

def leer_uptime_horas():
    try:
        with open('/proc/uptime') as f:
            return float(f.read().split()[0]) / 3600
    except Exception:
        return 0.0

def leer_swap():
    try:
        with open('/proc/meminfo') as f:
            data = f.read()
        total = int(re.search(r'SwapTotal:\s+(\d+)', data).group(1))
        libre = int(re.search(r'SwapFree:\s+(\d+)', data).group(1))
        usado = total - libre
        pct = (usado / total * 100) if total else 0
        return usado, total, pct
    except Exception:
        return 0, 0, 0.0

def leer_ram_disponible_gb():
    try:
        with open('/proc/meminfo') as f:
            data = f.read()
        # MemAvailable en kB -> GB
        kb = int(re.search(r'MemAvailable:\s+(\d+)', data).group(1))
        return kb / 1024 / 1024
    except Exception:
        return 0.0

def contar_zombies():
    n = 0
    for pid in os.listdir('/proc'):
        if not pid.isdigit():
            continue
        try:
            with open(f'/proc/{pid}/stat') as f:
                estado = f.read().split(' ')[2] if len(f.read().split(' ')) > 2 else ''
            # Re-leer correctamente: el estado esta entre parentesis
            with open(f'/proc/{pid}/stat') as f:
                stat = f.read()
            # despues del ultimo ')' viene el estado
            estado = stat[stat.rfind(')')+2:stat.rfind(')')+3]
            if estado == 'Z':
                n += 1
        except Exception:
            continue
    return n

def procesos_con_swap():
    """Devuelve lista de (swap_kb, pid, comm) con swap > umbral."""
    res = []
    for pid in os.listdir('/proc'):
        if not pid.isdigit():
            continue
        try:
            with open(f'/proc/{pid}/status') as f:
                status = f.read()
            m = re.search(r'VmSwap:\s+(\d+)', status)
            if m:
                kb = int(m.group(1))
                if kb > SWAP_PROCESO_MB * 1024:
                    with open(f'/proc/{pid}/comm') as f:
                        comm = f.read().strip()
                    res.append((kb // 1024, pid, comm))
        except Exception:
            continue
    res.sort(reverse=True)
    return res

def _check_uptime(uptime_h: float) -> str | None:
    if uptime_h >= ALERTA_UPTIME_H:
        return f"🔴 UPTIME: {uptime_h:.0f}h (>={ALERTA_UPTIME_H}h) — reinicio recomendado YA"
    if uptime_h >= AVISO_UPTIME_H:
        return f"🟠 UPTIME: {uptime_h:.0f}h (>={AVISO_UPTIME_H}h) — planificar reinicio"
    return None

def _check_swap(pct_swap: float, usado_swap: int, total_swap: int) -> str | None:
    if pct_swap >= ALERTA_SWAP:
        return (f"🔴 SWAP: {pct_swap:.0f}% usado ({usado_swap//1024//1024:.1f}/"
                f"{total_swap//1024//1024:.1f} GB) — reinicio recomendado")
    if pct_swap >= AVISO_SWAP:
        return (f"🟠 SWAP: {pct_swap:.0f}% usado ({usado_swap//1024//1024:.1f}/"
                f"{total_swap//1024//1024:.1f} GB) — vigilar")
    return None

def _check_ram(ram_libre: float) -> str | None:
    if ram_libre <= ALERTA_RAM:
        return f"🔴 RAM disponible: {ram_libre:.1f} GB (<= {ALERTA_RAM}) — presión alta"
    if ram_libre <= AVISO_RAM:
        return f"🟠 RAM disponible: {ram_libre:.1f} GB (<= {AVISO_RAM}) — vigilar"
    return None

def _check_zombies(zombies: int) -> str | None:
    if zombies > 0:
        return f"🟠 ZOMBIES: {zombies} proceso(s) defunct"
    return None

def _check_swap_procesos(swap_procs: list) -> str | None:
    if not swap_procs:
        return None
    top = swap_procs[0]
    return (f"🟠 SWAP PROCESO: {top[2]} (PID {top[1]}) usa {top[0]} MB en swap"
            + (f" +{len(swap_procs)-1} más" if len(swap_procs) > 1 else ""))

def main():
    uptime_h = leer_uptime_horas()
    usado_swap, total_swap, pct_swap = leer_swap()
    ram_libre = leer_ram_disponible_gb()
    zombies = contar_zombies()
    swap_procs = procesos_con_swap()

    hora = datetime.now().strftime('%Y-%m-%d %H:%M')

    problemas = [
        _check_uptime(uptime_h),
        _check_swap(pct_swap, usado_swap, total_swap),
        _check_ram(ram_libre),
        _check_zombies(zombies),
        _check_swap_procesos(swap_procs),
    ]
    problemas = [p for p in problemas if p]

    if not problemas:
        return  # silencio = todo bien

    # Si hay problemas, emitir informe
    print(f"🖥️ SALUD DEL SISTEMA — {hora}")
    print(f"Uptime: {uptime_h:.0f}h | RAM libre: {ram_libre:.1f} GB | Swap: {pct_swap:.0f}%")
    print()
    for p in problemas:
        print(p)
    print()
    if pct_swap >= ALERTA_SWAP or uptime_h >= ALERTA_UPTIME_H or ram_libre <= ALERTA_RAM:
        print("💡 Acción recomendada: reiniciar el PC cuando puedas (limpia swap y residuos).")

if __name__ == '__main__':
    main()
