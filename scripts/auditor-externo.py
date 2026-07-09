#!/usr/bin/env python3
"""auditor-externo.py — Genera JSON objetivo del laboratorio.
   Sin leer documentacion, skills ni archivos del proyecto.
   Solo comandos de sistema. Para ser interpretado por un agente externo."""
import json, subprocess, os, sys
from datetime import datetime, timezone

def cmd(c, timeout=10):
    try: r = subprocess.run(c, shell=True, capture_output=True, text=True, timeout=timeout); return r.stdout.strip()
    except: return ""

def cmd_int(c, default=0):
    try: return int(cmd(c))
    except: return default

LAB = "/home/jokoalmi/hermes-lab"
STACK = "/home/jokoalmi/automation-stack"
OUTPUT = sys.argv[1] if len(sys.argv) > 1 else f"/tmp/auditoria-externa-{datetime.now().strftime('%Y%m%d-%H%M')}.json"

data = {
    "fecha": datetime.now(timezone.utc).isoformat(),
    "hostname": cmd("hostname"),
    "hardware": {
        "cpu": cmd("cat /proc/cpuinfo | grep 'model name' | head -1 | cut -d: -f2 | xargs"),
        "ram_gb": cmd_int("free -g | awk '/^Mem:/ {print $2}'"),
        "gpu": cmd("nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null | head -1 | xargs"),
        "vram_gb": cmd_int("nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits 2>/dev/null | head -1"),

    },
    "procesos": {
        "total": cmd_int("ps -e --no-headers 2>/dev/null | wc -l"),
        "docker": cmd_int("ps -e --no-headers -o comm 2>/dev/null | grep -c dockerd"),
        "n8n": cmd_int("ps -e --no-headers -o comm 2>/dev/null | grep -ci n8n"),
        "ollama": cmd_int("ps -e --no-headers -o comm 2>/dev/null | grep -ci ollama"),
    },
    "puertos": {},
    "git": {"existe": False},
    "backups": {
        "cron_backups": 0,
        "cron_healthchecks": 0,
        "ultimo_git_bundle_gdrive": "",
        "restore_probado": False,
    },
    "scripts": {},
    "docker": {"contenedores_activos": 0, "contenedores_totales": 0},
    "smoke_tests": {"ejecutados": False, "pass": 0, "fail": 0, "total": 0},
    "tamano_repo_bytes": 0,
    "skills_pobladas": 0,
    "skills_vacias": 0,
}

# Puertos
for p in [5678, 11434, 8081, 8000, 1234]:
    proc = cmd(f"ss -ltnp 'sport = :{p}' 2>/dev/null | grep -oP 'users:\\(\\(\"(.*?)\"' | head -1 | sed 's/users:.((\"//;s/\"//'")
    data["puertos"][str(p)] = proc if proc else None

# Git
if os.path.isdir(os.path.join(LAB, ".git")):
    data["git"] = {
        "existe": True,
        "commits": cmd_int(f"cd {LAB} && git rev-list --count HEAD 2>/dev/null"),
        "ultimo_commit": cmd(f"cd {LAB} && git log -1 --format=%ci 2>/dev/null"),
        "rama": cmd(f"cd {LAB} && git branch --show-current 2>/dev/null"),
        "archivos": cmd_int(f"cd {LAB} && git ls-files 2>/dev/null | wc -l"),
    }

# Backups
cron = cmd("crontab -l 2>/dev/null")
data["backups"]["cron_backups"] = cron.count("backup-volumen") + cron.count("git-backup")
data["backups"]["cron_healthchecks"] = cron.count("healthcheck")
data["backups"]["ultimo_git_bundle_gdrive"] = cmd("rclone ls gdrive:hermes-lab-backups/ 2>/dev/null | sort -k2 | tail -1 | awk '{print $2, $1\" bytes\"}'")

# Scripts
scripts_dir = os.path.join(LAB, "scripts")
if os.path.isdir(scripts_dir):
    for s in sorted(os.listdir(scripts_dir)):
        if s.endswith(".sh"):
            path = os.path.join(scripts_dir, s)
            sintaxis = cmd(f"bash -n {path} 2>&1") == ""
            data["scripts"][s] = {
                "sintaxis": sintaxis,
                "ejecutable": os.access(path, os.X_OK),
                "tamano_b": os.path.getsize(path),
            }

# Docker
data["docker"]["contenedores_activos"] = cmd_int("docker ps -q 2>/dev/null | wc -l")
data["docker"]["contenedores_totales"] = cmd_int("docker ps -aq 2>/dev/null | wc -l")

# Smoke tests
smoke = os.path.join(LAB, "scripts", "smoke-test.sh")
if os.access(smoke, os.X_OK):
    out = cmd(f"{smoke} --quiet 2>&1")
    data["smoke_tests"]["ejecutados"] = True
    for line in out.split("\n"):
        if "PASS:" in line:
            data["smoke_tests"]["pass"] = int(line.split("PASS:")[1].split()[0])
        if "FAIL:" in line:
            data["smoke_tests"]["fail"] = int(line.split("FAIL:")[1].split()[0])
    data["smoke_tests"]["total"] = data["smoke_tests"]["pass"] + data["smoke_tests"]["fail"]

# Tamano repo
data["tamano_repo_bytes"] = cmd_int(f"du -sb {LAB} 2>/dev/null | cut -f1")

# Skills
skills_dir = os.path.join(LAB, "skills")
if os.path.isdir(skills_dir):
    for d in os.listdir(skills_dir):
        sp = os.path.join(skills_dir, d, "SKILL.md")
        if os.path.isfile(sp):
            data["skills_pobladas"] += 1
        else:
            data["skills_vacias"] += 1

with open(OUTPUT, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(json.dumps({"status": "ok", "archivo": OUTPUT, "tamano_bytes": os.path.getsize(OUTPUT)}))
