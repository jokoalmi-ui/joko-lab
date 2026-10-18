#!/usr/bin/env python3
"""convert_sessions.py - Convierte sesiones de Hermes a .md para indexar"""
import os, json, sys
from datetime import datetime

SESSIONS_FILE = "/tmp/hermes-sessions.jsonl"
OUTPUT_DIR = os.path.expanduser("~/joko-lab/04-operations/metrics/sesiones/raw")

def _formatear_conversacion(messages: list) -> str:
    """Convierte mensajes a markdown (primeras 3 + últimas 2 si hay más de 5).
    Formato byte-idéntico al original: '## Conversacion\n\n' + '**role:** texto\n\n'."""
    if not messages:
        return ""
    partes = ["## Conversacion\n\n"]
    msgs_mostrar = messages[:3] + messages[-2:] if len(messages) > 5 else messages
    for msg in msgs_mostrar:
        if isinstance(msg, dict):
            role = msg.get("role", "?")
            texto = str(msg.get("content", ""))[:300]
            if texto:
                partes.append(f"**{role}:** {texto}\n\n")
    return "".join(partes)


def _construir_contenido(sid: str, fecha: str, source: str, model: str,
                         system: str, messages: list) -> str:
    """Construye el contenido .md completo de una sesión."""
    content = f"# Sesion {sid}\n\n"
    content += f"- **Fecha:** {fecha}\n"
    content += f"- **Origen:** {source}\n"
    content += f"- **Modelo:** {model}\n"
    content += f"- **ID:** {sid}\n\n"
    if system:
        content += f"## Sistema\n\n{system}\n\n"
    content += _formatear_conversacion(messages)
    return content


def convert():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    count = 0
    
    with open(SESSIONS_FILE, "r") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                session = json.loads(line)
            except json.JSONDecodeError:
                continue
            
            sid = session.get("id", f"session-{count}")
            source = session.get("source", "desconocido")
            model = session.get("model", "desconocido")
            started = session.get("started_at", 0)
            
            # Formatear fecha
            if started:
                fecha = datetime.fromtimestamp(started).strftime("%Y-%m-%d %H:%M")
            else:
                fecha = "desconocida"
            
            # Extraer sistema y mensajes si existen
            system = session.get("system_prompt", "")
            messages = session.get("messages", session.get("conversation", []))
            
            # Crear contenido .md
            content = _construir_contenido(sid, fecha, source, model, system, messages)
            
            # Guardar archivo
            fecha_file = datetime.fromtimestamp(started).strftime("%Y%m%d") if started else "unknown"
            filename = f"{fecha_file}_{sid[:20]}.md"
            filepath = os.path.join(OUTPUT_DIR, filename)
            
            with open(filepath, "w", encoding="utf-8") as out:
                out.write(content)
            
            count += 1
    
    print(f"[✓] {count} sesiones convertidas a {OUTPUT_DIR}")

if __name__ == "__main__":
    convert()
