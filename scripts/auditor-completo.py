#!/usr/bin/env python3
"""
auditor-completo.py — Auditoría externa combinada para Joko Lab

Fusión de:
  - auditor-externo.py (JSON, datos de sistema)
  - audit-externo.sh (secretos, backups, HTTP directo, n8n API)

Filosofía: NO confía en nada que el proyecto afirme sobre sí mismo.
Todo se comprueba contra el sistema real.

Uso:
  ./auditor-completo.py [--json] [--output dir]
    --json       genera ademas un archivo JSON con datos estructurados
    --output     carpeta donde guardar los informes (defecto: /tmp)
"""

import json, os, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

# ── CONFIG ──────────────────────────────────────────────────────────
REPO_DIR = os.environ.get("REPO_DIR", os.path.expanduser("~/hermes-lab"))
BACKUP_DIR = os.environ.get("BACKUP_DIR", "/home/jokoalmi/hermes-lab/backups")
N8N_API_KEY = os.environ.get("N8N_API_KEY", "")
N8N_URL = os.environ.get("N8N_URL", "http://127.0.0.1:5678")
MAX_BACKUP_AGE_HOURS = 30
STACK_DIR = "/home/jokoalmi/automation-stack"

SERVICES = [
    ("n8n",           "127.0.0.1:5678",  "/healthz"),
    ("Ollama",        "127.0.0.1:11434", "/api/tags"),
    ("Stirling-PDF",  "127.0.0.1:8081",  "/"),
    ("pdf-cleaner",   "127.0.0.1:8000",  "/"),
    ("LM Studio",     "127.0.0.1:1234",  "/v1/models"),
]
INTERNAL_PORTS = [5678, 11434, 8081, 8000, 1234]

# ── SALIDA ──────────────────────────────────────────────────────────
PASS = "✅"; WARN = "⚠️ "; FAIL = "❌"; SKIP = "⏭️ "
INFO = "ℹ️ "

lines = []  # acumula texto del informe

def L(t=""):
    lines.append(t)

def section(title):
    L(); L("-" * 70); L(f"  {title}"); L("-" * 70)

def report(icon, text):
    L(f"  {icon} {text}")

def cmd(c, timeout=15):
    try:
        r = subprocess.run(c, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip()
    except: return ""

def cmd_int(c, default=0):
    try: return int(cmd(c))
    except: return default

# ── DATOS ESTRUCTURADOS ────────────────────────────────────────────
data = {
    "fecha": datetime.now(timezone.utc).isoformat(),
    "hostname": cmd("hostname"),
    "hardware": {},
    "git": {"existe": False},
    "secretos": {},
    "puertos": {},
    "backups": {"test_integridad": False},
    "servicios": {},
    "n8n": {"ejecuciones": None},
    "docker": {},
}


# ═══════════════════════════════════════════════════════════════════
# 1. ENCABEZADO
# ═══════════════════════════════════════════════════════════════════
L("=" * 70)
L(f"  AUDITORIA COMBINADA — Joko Lab")
L(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  |  host: {cmd('hostname')}")
L("=" * 70)

# ═══════════════════════════════════════════════════════════════════
# 2. SEGURIDAD
# ═══════════════════════════════════════════════════════════════════
section("1. SEGURIDAD")

# 1.1 Secretos en Git
if os.path.isdir(os.path.join(REPO_DIR, ".git")):
    os.chdir(REPO_DIR)
    L(); L("  1.1  Escaneo de secretos en historial Git")
    secret_hits = cmd("git log -p --all 2>/dev/null | grep -iEc 'api[_-]?key|secret[_-]?key|password\\s*=|BEGIN (RSA|OPENSSH) PRIVATE KEY|token\\s*='")
    try:
        n = int(secret_hits)
        if n == 0:
            report(PASS, f"No se encontraron patrones de secretos en el historial ({n} coincidencias).")
        else:
            report(FAIL, f"Se encontraron {n} posibles secretos en el historial. Revisar: git log -p --all | grep -iE 'api_key|secret|password|token'")
        data["secretos"]["historial"] = n
    except: pass

    # 1.2 Archivos sensibles
    L(); L("  1.2  Archivos con nombre sospechoso versionados")
    sensitive = cmd("git ls-files | grep -iE '\\.env$|\\.pem$|\\.key$|id_rsa|credentials\\.json' || true")
    if sensitive:
        report(FAIL, "Archivos sospechosos encontrados:")
        for f in sensitive.split("\n"):
            L(f"         {f}")
    else:
        report(PASS, "No hay archivos con nombre sospechoso en HEAD.")

    # 1.3 Remoto Git
    L(); L("  1.3  Remoto Git")
    remote = cmd("git remote -v 2>/dev/null | head -1")
    if remote:
        report(PASS, f"Remoto configurado: {remote}")
        last_push = cmd(f"git log origin/$(git branch --show-current) -1 --format=%cd --date=relative 2>/dev/null || echo 'desconocido'")
        L(f"         Ultimo push al remoto: {last_push}")
        data["git"]["remoto"] = remote.split()[1] if remote else None
    else:
        report(FAIL, "No hay remoto Git configurado. Solo existe en este disco.")
        data["git"]["remoto"] = None

    data["git"]["existe"] = True
    data["git"]["commits"] = cmd_int("git rev-list --count HEAD")
    data["git"]["ultimo_commit"] = cmd("git log -1 --format=%ci")
    data["git"]["rama"] = cmd("git branch --show-current")
    data["git"]["archivos"] = cmd_int("git ls-files | wc -l")
else:
    report(FAIL, "No se encontro repo Git en REPO_DIR")

# 1.4 Exposicion de puertos
L(); L("  1.4  Exposicion de puertos")
for port in INTERNAL_PORTS:
    bind = cmd(f"ss -tlnp 2>/dev/null | grep ':{port} '")
    data["puertos"][str(port)] = {"escuchando": bool(bind)}
    if not bind:
        report(SKIP, f"Puerto {port} no esta escuchando.")
        data["puertos"][str(port)]["estado"] = "parado"
    elif "127.0.0.1" in bind or "::1" in bind:
        report(PASS, f"Puerto {port} solo escucha en localhost.")
        data["puertos"][str(port)]["estado"] = "localhost"
    else:
        proc = cmd(f"ss -tlnp 2>/dev/null | grep ':{port} ' | grep -oP 'users:\\(\\(\"(.*?)\"' | head -1 | sed 's/users:.((\"//;s/\"//'")
        report(FAIL, f"Puerto {port} escucha en todas las interfaces -- revisar exposicion ({proc})")
        data["puertos"][str(port)]["estado"] = "expuesto"

# 1.5 Imagenes Docker
L(); L("  1.5  Imagenes Docker en uso")
docker_images = cmd("docker images --format 'table {{.Repository}}\t{{.Tag}}\t{{.CreatedSince}}' 2>/dev/null | head -20")
if docker_images:
    for line in docker_images.split("\n")[:10]:
        L(f"         {line}")
    L("         (Manual: verificar versiones contra CVE feed de cada proyecto)")
else:
    report(SKIP, "Docker no disponible o sin imagenes.")

# ═══════════════════════════════════════════════════════════════════
# 3. BACKUPS
# ═══════════════════════════════════════════════════════════════════
section("2. BACKUPS")

bp = Path(BACKUP_DIR)
if bp.is_dir():
    backups_found = list(bp.rglob("*.tar.gz")) + list(bp.rglob("*.tgz")) + list(bp.rglob("*.zip"))
    if backups_found:
        for f in backups_found:
            age_h = int((datetime.now().timestamp() - f.stat().st_mtime) / 3600)
            size = f.stat().st_size
            size_h = f"{size/1024/1024:.1f}M" if size > 1024*1024 else f"{size/1024:.1f}K"
            if age_h <= MAX_BACKUP_AGE_HOURS:
                report(PASS, f"{f.name} -- hace {age_h}h, {size_h}")
            else:
                report(FAIL, f"{f.name} -- hace {age_h}h (supera umbral {MAX_BACKUP_AGE_HOURS}h), {size_h}")

            # Test de integridad
            int_result = ""
            if f.suffix in (".gz", ".tgz") or "tar" in f.suffix:
                r = subprocess.run(["tar", "-tzf", str(f)], capture_output=True, timeout=30)
                if r.returncode == 0:
                    int_result = f"{PASS} integro (se lista sin error)"
                    data["backups"]["test_integridad"] = True
                else:
                    int_result = f"{FAIL} CORRUPTO o ilegible"
            elif f.suffix == ".zip":
                r = subprocess.run(["unzip", "-t", str(f)], capture_output=True, timeout=30)
                if r.returncode == 0:
                    int_result = f"{PASS} integro"
                    data["backups"]["test_integridad"] = True
                else:
                    int_result = f"{FAIL} CORRUPTO"
            L(f"           Integridad: {int_result}")
    else:
        report(FAIL, "No se encontraron backups en BACKUP_DIR")
else:
    report(FAIL, f"No existe la carpeta de backups: {BACKUP_DIR}")

# Backup remoto GDrive
L()
gdrive = cmd("rclone ls gdrive:hermes-lab-backups/ 2>/dev/null | sort -k2 | tail -1")
if gdrive:
    report(PASS, f"Backup en Google Drive: {gdrive}")
    data["backups"]["gdrive"] = gdrive
else:
    report(SKIP, "No se pudo acceder a gdrive:hermes-lab-backups/")

report(WARN, "PENDIENTE MANUAL: restaurar el backup mas reciente en un entorno de prueba.")

# ═══════════════════════════════════════════════════════════════════
# 4. SALUD DE SERVICIOS (HTTP directo, independiente)
# ═══════════════════════════════════════════════════════════════════
section("3. SALUD DE SERVICIOS (verificacion directa via HTTP)")

for name, hostport, path in SERVICES:
    url = f"http://{hostport}{path}"
    start = datetime.now()
    r = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "--max-time", "5", url],
                       capture_output=True, text=True, timeout=10)
    ms = int((datetime.now() - start).total_seconds() * 1000)
    code = r.stdout.strip()

    svc = {"url": url, "http_code": code, "ms": ms}
    data["servicios"][name] = svc

    if not code or code == "000":
        report(FAIL, f"{name} ({url}) -- sin respuesta (caido o timeout)")
        svc["estado"] = "caido"
    elif 200 <= int(code) < 500:
        report(PASS, f"{name} ({url}) -- HTTP {code}, {ms}ms")
        svc["estado"] = "ok"
    else:
        report(FAIL, f"{name} ({url}) -- HTTP {code} (error), {ms}ms")
        svc["estado"] = "error"

# ═══════════════════════════════════════════════════════════════════
# 5. TASA DE EXITO DE WORKFLOWS N8N
# ═══════════════════════════════════════════════════════════════════
section("4. WORKFLOWS N8N -- TASA DE EXITO")

if N8N_API_KEY:
    r = subprocess.run(
        ["curl", "-s", "--max-time", "8", "-H", f"X-N8N-API-KEY: {N8N_API_KEY}", f"{N8N_URL}/api/v1/executions?limit=100"],
        capture_output=True, text=True, timeout=15)
    if r.stdout:
        try:
            execs = json.loads(r.stdout)
            all_execs = execs.get("data", [])
            total = len(all_execs)
            success = sum(1 for e in all_execs if e.get("status") == "success")
            error = sum(1 for e in all_execs if e.get("status") == "error")
            rate = (100 * success // total) if total else 0
            data["n8n"] = {"ejecuciones": {"total": total, "success": success, "error": error, "tasa_exito": rate}}

            if total:
                report(PASS, f"Ultimas {total} ejecuciones: {success} exitos / {error} errores = {rate}% exito")
                if rate < 70:
                    report(WARN, "Tasa de exito < 70% -- no calificar workflows como 'solidos' sin arreglar causa raiz")
            else:
                report(SKIP, "No hay ejecuciones registradas")
        except: report(FAIL, "Error al parsear respuesta de API n8n")
    else:
        report(FAIL, "API n8n no respondio. Revisa N8N_API_KEY")
else:
    report(SKIP, "N8N_API_KEY no definida. Exportala para auditar tasa de exito real.")
    L("         Generar API key en n8n: Settings → API → Create API key")

# ═══════════════════════════════════════════════════════════════════
# 6. DATOS DEL SISTEMA
# ═══════════════════════════════════════════════════════════════════
section("5. DATOS DEL SISTEMA")

data["hardware"] = {
    "cpu": cmd("cat /proc/cpuinfo | grep 'model name' | head -1 | cut -d: -f2 | xargs"),
    "ram_gb": cmd_int("free -g | awk '/^Mem:/ {print $2}'"),
    "gpu": cmd("nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null | head -1 | xargs"),
    "vram_gb": cmd_int("nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits 2>/dev/null | head -1"),
}
report(INFO, f"CPU: {data['hardware']['cpu']}")
report(INFO, f"RAM: {data['hardware']['ram_gb']} GB")
report(INFO, f"GPU: {data['hardware']['gpu']} ({data['hardware']['vram_gb']} MB VRAM)")

procs = {
    "total": cmd_int("ps -e --no-headers 2>/dev/null | wc -l"),
    "docker": cmd_int("ps -e --no-headers -o comm 2>/dev/null | grep -c dockerd"),
}
report(INFO, f"Procesos: {procs['total']} total, dockerd: {'si' if procs['docker'] else 'no'}")
data["procesos"] = procs

docker_ct = cmd_int("docker ps -q 2>/dev/null | wc -l")
docker_all = cmd_int("docker ps -aq 2>/dev/null | wc -l")
data["docker"] = {"activos": docker_ct, "totales": docker_all}
report(INFO, f"Docker: {docker_ct} contenedores activos / {docker_all} totales")

if data["git"]["existe"]:
    report(INFO, f"Git: {data['git']['commits']} commits, rama {data['git']['rama']}, {data['git']['archivos']} archivos versionados")

repo_size = cmd_int(f"du -sb {REPO_DIR} 2>/dev/null | cut -f1")
data["tamano_repo_bytes"] = repo_size
report(INFO, f"Tamano del repositorio: {repo_size/1024:.0f} KB")

skills_pob = len([d for d in Path(f"{REPO_DIR}/skills").iterdir() if (d / "SKILL.md").exists()]) if Path(f"{REPO_DIR}/skills").exists() else 0
skills_vac = len([d for d in Path(f"{REPO_DIR}/skills").iterdir() if not (d / "SKILL.md").exists()]) if Path(f"{REPO_DIR}/skills").exists() else 0
data["skills"] = {"pobladas": skills_pob, "vacias": skills_vac}
report(INFO, f"Skills: {skills_pob} pobladas, {skills_vac} vacias")

# ═══════════════════════════════════════════════════════════════════
# 7. PENDIENTE DE REVISION MANUAL
# ═══════════════════════════════════════════════════════════════════
section("6. PENDIENTE DE REVISION MANUAL")

L("""  Estos puntos requieren juicio humano y NO estan cubiertos arriba:

  [ ] Restauracion real de un backup en entorno de prueba
      (no solo test de integridad del archivo, sino levantar
      el servicio con esos datos)

  [ ] ¿Hay alerta real a un humano si un servicio cae de madrugada?
      (provocar una caida simulada y comprobar si llega notificacion)

  [ ] Contrastar esta auditoria con la interna generada por el propio
      Hermes. La diferencia entre ambas es en si misma una metrica.

  [ ] Evaluar si nuevas propuestas (ej. capa de orquestacion)
      resuelven una necesidad concreta o son sobre-ingenieria.

  [ ] Las 3 skills vacias (betterbird, perfumes, evolution):
      mantenerlas congeladas o eliminarlas del arbol.
""")

# ═══════════════════════════════════════════════════════════════════
# 8. CIERRE
# ═══════════════════════════════════════════════════════════════════
L("-" * 70)
L(f"  FIN DE AUDITORIA — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
L("-" * 70)

# ── SALIDA ──────────────────────────────────────────────────────────
output_dir = sys.argv[sys.argv.index("--output") + 1] if "--output" in sys.argv else os.path.join(REPO_DIR, "logs")
Path(output_dir).mkdir(parents=True, exist_ok=True)

# Texto
text_path = Path(output_dir) / f"auditoria-completa-{datetime.now().strftime('%Y%m%d-%H%M')}.txt"
text_path.write_text("\n".join(lines))
print(f"\nInforme guardado: {text_path}")

# JSON (opcional)
if "--json" in sys.argv:
    json_path = Path(output_dir) / f"auditoria-completa-{datetime.now().strftime('%Y%m%d-%H%M')}.json"
    json_path.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    print(f"Datos JSON:      {json_path}")

# Mostrar informe en pantalla
print("\n" + "\n".join(lines))
