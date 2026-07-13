#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Validate Ports Script — Joko Lab [Dimensión 2 - Conocimiento]
Analiza la salida de 'ss -tln' para verificar si los puertos declarados en la
arquitectura están abiertos y bindeados de manera segura (localhost/127.0.0.1).
Solo lectura. No requiere privilegios de superusuario.
"""

import sys
import subprocess

# Configuración de puertos de la arquitectura
# required: True si su ausencia hace fallar el script, False si es opcional.
EXPECTED_PORTS = {
    5678: {"service": "n8n (Workflow Automation)", "required": True},
    11434: {"service": "Ollama (Local LLMs)", "required": True},
    8081: {"service": "Stirling-PDF (PDF Processing)", "required": True},
    8000: {"service": "pdf-cleaner (PDF Sanitization)", "required": True},
    1234: {"service": "LM Studio API (Local Inference)", "required": False},
    5000: {"service": "LM Studio Real Monitor (Dashboard)", "required": False}
}

def get_active_bindings():
    """Ejecuta ss -tln and devuelve un mapa de puerto -> lista de direcciones IP de bindeo."""
    bindings = {}
    try:
        # ss -tln muestra sockets de escucha TCP numéricos de solo lectura sin sudo
        result = subprocess.run(["ss", "-tln"], capture_output=True, text=True, check=True)
        lines = result.stdout.splitlines()
        
        # Saltamos la cabecera
        for line in lines[1:]:
            parts = line.split()
            if len(parts) < 4:
                continue
            
            local_address = parts[3] # Ej: 127.0.0.1:5678, *:8081, [::1]:11434, :::8000
            
            # Separamos la dirección del puerto buscando el último ':'
            if ":" in local_address:
                ip, _, port_str = local_address.rpartition(":")
                try:
                    port = int(port_str)
                    if port not in bindings:
                        bindings[port] = []
                    bindings[port].append(ip)
                except ValueError:
                    continue
    except Exception as e:
        print(f"❌ Error al ejecutar 'ss -tln': {e}")
        sys.exit(2)
        
    return bindings

def is_secure_binding(ips):
    """
    Verifica si los bindeos de un puerto se limitan a interfaces locales (seguras).
    Si se bindea a '0.0.0.0', '*', '::' o '[::]', se considera expuesto.
    """
    insecure_markers = {"0.0.0.0", "*", "::", "[::]"}
    for ip in ips:
        # Limpieza de corchetes en IPv6 si los hubiera
        clean_ip = ip.strip("[]")
        if clean_ip in insecure_markers:
            return False
    return True

def run_validation():
    print("=" * 70)
    print("  JOKO LAB — VALIDACIÓN PROGRAMÁTICA Y AUDITORÍA DE PUERTOS")
    print("=" * 70)
    print("Verificando estado y bindeos seguros mediante 'ss -tln'...")
    print("-" * 70)

    bindings = get_active_bindings()
    validation_failed = False

    for port, config in EXPECTED_PORTS.items():
        service = config["service"]
        is_required = config["required"]
        
        if port in bindings:
            ips = bindings[port]
            secure = is_secure_binding(ips)
            
            bind_str = ", ".join(ips)
            security_status = "🔒 localhost" if secure else "🔓 EXPUESTO EXTERNAMENTE"
            indicator = "✅" if secure else "⚠️"
            
            print(f"{indicator} Puerto {port:<5} | ACTIVO | {security_status:<22} | {service}")
            print(f"      IPs de escucha: {bind_str}")
            
            # Si está expuesto externamente, lo marcamos como fallo de seguridad
            if not secure:
                validation_failed = True
        else:
            if is_required:
                print(f"❌ Puerto {port:<5} | INACTIVO (REQUERIDO) | {'':<22} | {service}")
                validation_failed = True
            else:
                print(f"💤 Puerto {port:<5} | INACTIVO (OPCIONAL)  | {'':<22} | {service} (Apagado a propósito)")

    print("-" * 70)
    
    if validation_failed:
        print("\n❌ RESULTADO: Fallo en la validación de puertos de la arquitectura.")
        print("Motivo: Hay puertos requeridos inactivos o expuestos externamente.")
        sys.exit(1)
    else:
        print("\n✅ RESULTADO: Validación exitosa.")
        print("Todos los puertos requeridos están activos y correctamente bindeados a localhost.")
        sys.exit(0)

if __name__ == "__main__":
    run_validation()
