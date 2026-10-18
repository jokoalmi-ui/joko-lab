#!/usr/bin/env python3
"""
lab_panel.py — Panel de estado del Joko Lab: instantánea REAL + HTML interactivo + servidor local.

Uso:
    python3 tools/lab_panel.py --once                 # recoge instantánea y genera el HTML
    python3 tools/lab_panel.py --serve [--port 8099]  # genera y sirve en http://localhost:8099
    python3 tools/lab_panel.py --json                 # imprime la instantánea (para otros scripts)

Naturaleza: SOLO LECTURA sobre el sistema (ls, git status, jobs.json, config.yaml, lms ps,
nvidia-smi, ss, tail de logs). Lo único que se escribe es la salida del panel:
    research/lab-panel/index.html  y  research/lab-panel/snapshot.json

Nada de esto reinicia, para ni toca servicios (n8n incluido).
"""
from __future__ import annotations

import argparse
import glob
import http.server
import json
import os
import re
import shutil
import socketserver
import subprocess
import sys
import threading
from datetime import datetime
from pathlib import Path

HOME = Path("/home/jokoalmi")
LAB = HOME / "joko-lab"
OUT_DIR = LAB / "research" / "lab-panel"
CRON_JOBS = HOME / ".hermes" / "cron" / "jobs.json"
HERMES_CFG = HOME / ".hermes" / "config.yaml"
SKILLS_DIR = HOME / ".hermes" / "skills"


# ─────────────────────────── utilidades ───────────────────────────
def sh(cmd: str, timeout: int = 120, cwd: Path | None = None) -> tuple[str, int]:
    try:
        p = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        return (p.stdout or "").strip(), p.returncode
    except Exception as e:  # noqa: BLE001
        return f"ERR {e}", 1


def n_entries(p: Path) -> int:
    try:
        return len(os.listdir(p))
    except Exception:  # noqa: BLE001
        return 0


def read_json(p: Path):
    try:
        return json.loads(p.read_text())
    except Exception:  # noqa: BLE001
        return None


# ─────────────────────────── recogida ───────────────────────────
_PY_YAML: list = []  # caché: vacía = sin calcular · [None] = ninguno sirve · [ruta] = intérprete bueno


def py_con_yaml() -> str | None:
    """Intérprete que pueda importar yaml (lo que necesita knowledge_health.py). None si ninguno puede."""
    if _PY_YAML:
        return _PY_YAML[0]
    candidatos = [sys.executable, "/usr/bin/python3", shutil.which("python3") or ""]
    for cand in candidatos:
        if not cand or not os.path.exists(cand):
            continue
        try:
            r = subprocess.run([cand, "-c", "import yaml"], capture_output=True, timeout=60)
            if r.returncode == 0:
                _PY_YAML.append(cand)
                return cand
        except Exception:  # noqa: BLE001
            continue
    _PY_YAML.append(None)
    return None


def snapshot() -> dict:
    s: dict = {}
    ts_hora, _ = sh("date '+%Y-%m-%d %H:%M %Z'")
    s["ts"] = ts_hora or datetime.now().strftime("%Y-%m-%d %H:%M")

    # estructura del lab
    s["capas"] = {d: n_entries(LAB / d) for d in sorted(os.listdir(LAB)) if (LAB / d).is_dir() and re.match(r"^\d\d-", d)}
    s["carpetas_sueltas"] = sorted(d for d in os.listdir(LAB) if (LAB / d).is_dir() and not re.match(r"^\d\d-", d))

    # conocimiento
    objs = LAB / "01-knowledge" / "objects"
    ficheros = sorted(os.listdir(objs)) if objs.is_dir() else []
    s["objetos"] = {
        "total": len(ficheros),
        "bak": sum(1 for f in ficheros if ".bak" in f),
        "por_tipo": {},
    }
    for f in ficheros:
        if ".bak" in f:
            continue
        m = re.match(r"^([A-Z]{2,}(?:-[A-Z]+)?)-", f)
        key = m.group(1) if m else "OTROS"
        s["objetos"]["por_tipo"][key] = s["objetos"]["por_tipo"].get(key, 0) + 1

    k = LAB / "01-knowledge"
    s["conocimiento"] = {
        d: len(list((k / d).rglob("*.md")))
        for d in sorted(os.listdir(k))
        if (k / d).is_dir() and not d.endswith("BACKUP")
    }

    # knowledge health (script del propio lab) — con el intérprete que tenga PyYAML, no con el que toque
    pykh = py_con_yaml()
    if pykh:
        kh, rc = sh(f"{pykh} {LAB}/tools/knowledge_health.py 2>&1 | tail -40", timeout=300, cwd=LAB)
    else:
        kh, rc = "ModuleNotFoundError: No module named 'yaml' (en todos los intérpretes probados)", 1
    s["knowledge_health"] = {"rc": rc, "salida": kh[-2500:], "parsed": parse_kh(kh), "py": pykh}

    # operaciones
    tools_dir = LAB / "tools"
    s["tools"] = {"total": n_entries(tools_dir), "bak": len(glob.glob(str(tools_dir / "*.bak*")))}
    for name in ("tests", "verification", "lpa", "docs", "research", "assets", "inbox", "reports", "instruments"):
        s[name] = {"total": n_entries(LAB / name), "lista": sorted(os.listdir(LAB / name))[:8] if (LAB / name).is_dir() else []}

    # repos git (solo lectura)
    s["repos"] = {}
    for p in (LAB, HOME / "hermes-lab", HOME / "perfume-ia", HOME / "lmstudio_real_monitor"):
        if not p.exists():
            continue
        if (p / ".git").is_dir():
            last, _ = sh("git log -1 --format='%h|%ad|%s' --date=short", cwd=p)
            dirty, _ = sh("git status --porcelain | wc -l", cwd=p)
            s["repos"][str(p)] = {"git": True, "last": last, "sin_commitear": int(dirty or 0)}
        else:
            ev, _ = sh("git status -sb 2>&1 | head -1", cwd=p)
            s["repos"][str(p)] = {"git": False, "evidencia": ev}

    # crons de Hermes
    data = read_json(CRON_JOBS) or {}
    js = data.get("jobs", data) if isinstance(data, dict) else data
    if isinstance(js, dict):
        js = list(js.values())
    jobs = js or []
    err = [j for j in jobs if j.get("last_status") == "error"]
    s["crons"] = {
        "total": len(jobs),
        "enabled": sum(1 for j in jobs if j.get("enabled")),
        "error": [{"nombre": j.get("name"), "streak": j.get("failure_streak"), "last": j.get("last_run_at"), "script": j.get("script")} for j in err],
        "ok": sum(1 for j in jobs if j.get("last_status") == "ok"),
        "sin_ejecutar": sum(1 for j in jobs if not j.get("last_status")),
        "top": sorted(
            [{"n": j.get("name"), "s": j.get("last_status"), "last": (j.get("last_run_at") or "")[:16]} for j in jobs if j.get("last_run_at")],
            key=lambda x: x["last"], reverse=True)[:6],
    }

    cront, _ = sh("crontab -l 2>&1 | grep -v '^#' | grep -v '^$'")
    s["crontab"] = [l for l in cront.splitlines() if l.strip()]

    # skills
    sk = glob.glob(str(SKILLS_DIR / "**" / "SKILL.md"), recursive=True)
    cats: dict[str, int] = {}
    for p in sk:
        rel = Path(p).relative_to(SKILLS_DIR)
        cats[rel.parts[0] if len(rel.parts) > 1 else "(raíz)"] = cats.get(rel.parts[0] if len(rel.parts) > 1 else "(raíz)", 0) + 1
    s["skills"] = {"total": len(sk), "por_categoria": dict(sorted(cats.items(), key=lambda x: -x[1]))}

    # MCP configurados
    s["mcp"] = []
    if HERMES_CFG.exists():
        txt = HERMES_CFG.read_text().splitlines()
        dentro = False
        for line in txt:
            if re.match(r"^mcp_servers:\s*$", line):
                dentro = True
                continue
            if dentro:
                if re.match(r"^\S", line):  # fin del bloque
                    break
                m = re.match(r"^  ([A-Za-z0-9_.\-]+):\s*$", line)
                if m:
                    s["mcp"].append(m.group(1))

    # inferencia + GPU
    lms, _ = sh("lms ps 2>&1 | head -8")
    s["inferencia"] = {
        "lmstudio": lms,
        "lmstudio_cargado": "IDLE" in lms or "LOADING" in lms,
        "ollama_raw": sh("curl -s --max-time 5 http://localhost:11434/v1/models")[0],
        "comfyui": sh("systemctl --user is-active comfyui")[0],
    }
    s["inferencia"]["ollama_modelos"] = re.findall(r'"id":"([^"]+)"', s["inferencia"]["ollama_raw"])
    s["gpu"] = sh("nvidia-smi --query-gpu=name,memory.used,memory.total,utilization.gpu,temperature.gpu --format=csv,noheader")[0]

    # puertos
    puertos, _ = sh("ss -ltn 2>/dev/null | awk 'NR>1{print $4}' | sed 's/.*://' | sort -n | uniq | tr '\\n' ' '")
    s["puertos"] = [int(x) for x in puertos.split() if x.isdigit()]

    # logs de vigilancia
    logs = {
        "docker_health": HOME / "hermes-lab/skills/docker-admin/logs/healthcheck.log",
        # ruta real: el cron */30 la escribe en docker-admin/logs; n8n-admin/logs no existe -> hueco falso
        "n8n_health": HOME / "hermes-lab/skills/docker-admin/logs/healthcheck-n8n.log",
    }
    s["logs"] = {}
    for k2, p in logs.items():
        if p.exists():
            txt = p.read_text(errors="replace").strip().splitlines()
            s["logs"][k2] = {"existe": True, "lineas": len(txt), "ultima": txt[-1][:220] if txt else ""}
        else:
            s["logs"][k2] = {"existe": False, "lineas": 0, "ultima": ""}

    # backups
    s["backups"] = {
        "destino_existe": (Path("/mnt/ssd_ia_datos/backups")).exists(),
        "jobs": [j["n"] for j in s["crons"]["top"] if "backup" in (j["n"] or "").lower()],
    }
    return s


def parse_kh(txt: str) -> dict:
    """Extrae las cifras del knowledge_health del lab (sin inventar: si no casa, queda None)."""
    def num(pat: str):
        m = re.search(pat, txt)
        return int(m.group(1)) if m else None

    def frac(pat: str):
        m = re.search(pat, txt)
        return (int(m.group(1)), int(m.group(2))) if m else (None, None)

    fm = frac(r"Frontmatter:\s+(\d+)/(\d+)")
    h1 = frac(r"H1:\s+(\d+)/(\d+)")
    h3 = frac(r"H3:\s+(\d+)/(\d+)")
    en = frac(r"Con enlaces:\s+(\d+)/(\d+)")
    con = frac(r"Cumplen contrato:\s+(\d+)/(\d+)")
    return {
        "score": num(r"KNOWLEDGE HEALTH:\s+(\d+)/100"),
        "docs": fm[1],
        "frontmatter": fm,
        "h1": h1,
        "h3": h3,
        "enlaces": en,
        "contrato": con,
        "supervivencia": num(r"Supervivencia:\s+(\d+)%"),
        "dec_activas": num(r"DEC activas:\s+(\d+)"),
    }


# ─────────────────────────── reglas de huecos ───────────────────────────
def kh_ciego(s: dict) -> str | None:
    """Si el medidor de conocimiento no puede ejecutarse, devuelve su error literal. No se inventa: o hay dato, o hay hueco."""
    kh = s["knowledge_health"]
    txt = kh.get("salida") or ""
    for l in txt.splitlines():
        if "ModuleNotFoundError" in l or "ImportError" in l:
            return l.strip()
    if "Traceback" in txt:
        return (txt.strip().splitlines() or ["traceback sin mensaje"])[-1].strip()
    if not kh.get("py"):
        return "ningún intérprete del sistema tiene PyYAML"
    return None


def huecos(s: dict) -> list[dict]:
    out: list[dict] = []

    def add(p, t, capa, ev, fix):
        out.append({"p": p, "t": t, "capa": capa, "ev": ev, "fix": fix})

    # P1 · instrumento ciego: sin esto, un medidor roto hace desaparecer huecos reales sin avisar
    ciego = kh_ciego(s)
    if ciego:
        add("P1", "instrumento ciego: knowledge_health no mide", "Conocimiento",
            f"$ {s['knowledge_health'].get('py') or 'python3'} tools/knowledge_health.py\n{ciego}",
            "Arreglar el intérprete (PyYAML) antes de dar por buenos los huecos de conocimiento: "
            "sus cifras (contrato, enlaces, score) llegan vacías y el panel se queda sin verlas.")

    # P0
    for path, info in s["repos"].items():
        if not info["git"] and path.endswith("/joko-lab"):
            add("P0", f"{path} sin control de versiones", "Operaciones",
                "$ git -C ~/joko-lab status -sb\n" + (info.get("evidencia") or "fatal: no es un repositorio git"),
                "Inicializar repo, primer commit y sumarlo al git-backup.sh que ya corre a las 22:35 para hermes-lab.")

    for e in s["crons"]["error"]:
        add("P0", f"cron '{e['nombre']}' en error", "Automatización",
            f"last_status=error · failure_streak={e.get('streak')} · último intento {e.get('last')} · script {e.get('script')}",
            "Leer su log y decidir: si el catchup ya cubre el trabajo, retirar el job; si no, arreglarlo.")

    kh = s["knowledge_health"]["parsed"]
    if kh["contrato"][1] and kh["contrato"][0] is not None and kh["contrato"][0] < kh["contrato"][1]:
        add("P1", f"Contrato de evidencia: {kh['contrato'][0]}/{kh['contrato'][1]}", "Conocimiento",
            f"Evidence Contract:\n  Cumplen contrato:  {kh['contrato'][0]}/{kh['contrato'][1]}",
            "Validar primero el medidor (un 0 absoluto apunta a instrumento mal calibrado, no a N documentos incumplidores).")

    if kh["enlaces"][1] and kh["enlaces"][0] is not None:
        pct = round(100 * kh["enlaces"][0] / kh["enlaces"][1])
        if pct < 20:
            add("P1", f"Documentos enlazados: {pct} % ({kh['enlaces'][0]}/{kh['enlaces'][1]})", "Conocimiento",
                f"Con enlaces: {kh['enlaces'][0]}/{kh['enlaces'][1]} ({pct} %)\nH3: {kh['h3'][0]}/{kh['h3'][1]}",
                "Enlazar cuando se reutiliza una DEC, un patrón o una observación; sin índice cruzado el corpus es opaco.")

    if s["reports"]["total"] < 3:
        add("P1", f"reports/ con {s['reports']['total']} fichero(s)", "Conocimiento",
            f"reports: {s['reports']['total']} entradas (frente a {s['conocimiento'].get('observations', 0)} observaciones)",
            "O generador de informes periódicos, o retirar la carpeta del árbol.")

    if s["objetos"]["bak"] > 0:
        add("P1", f"{s['objetos']['bak']} .bak dentro de objects/", "Conocimiento",
            f"objects/ = {s['objetos']['total']} entradas · {s['objetos']['bak']} con .bak · vivos: {s['objetos']['por_tipo']}",
            "Mover los .bak a cuarentena con fecha y dejar objects/ solo con objetos vivos.")

    for k2, log in s["logs"].items():
        if not log["existe"] or log["lineas"] == 0:
            add("P1", f"log de vigilancia vacío/inexistente: {k2}", "Infraestructura",
                f"{k2}: existe={log['existe']} · líneas={log['lineas']}",
                "Corregir la ruta del log y comprobar que escribe algo cuando todo va bien, no solo al fallar.")

    if s["tools"]["total"] and s["tools"]["bak"] / s["tools"]["total"] > 0.3:
        pct = round(100 * s["tools"]["bak"] / s["tools"]["total"])
        add("P2", f"tools/ con {pct} % de .bak", "Operaciones",
            f"tools/ = {s['tools']['total']} ficheros · .bak = {s['tools']['bak']}",
            "Archivar los .bak de más de 30 días en 04-operations/archive/ (borrado solo con OK explícito).")

    if s["instruments"]["total"] < 3:
        add("P2", f"instruments/ con {s['instruments']['total']} instrumento(s)", "Operaciones",
            f"instruments: {s['instruments']['total']} → {s['instruments']['lista']}",
            "Faltan al menos: medidor del contrato de evidencia, gate de veracidad, medidor de alucinaciones.")

    vacias = [n for n in ("assets", "inbox", "reports", "instruments") if s[n]["total"] <= 1]
    if vacias:
        add("P2", f"carpetas casi vacías: {', '.join(vacias)}", "Operaciones",
            "\n".join(f"{n}: {s[n]['total']} entradas" for n in vacias),
            "Decidir por carpeta: se usa o se retira. Carpetas vacías prometen algo que no existe.")

    sin_git = [p for p, i in s["repos"].items() if not i["git"] and not p.endswith("/joko-lab")]
    if sin_git:
        add("P2", f"proyectos sin git: {', '.join(Path(p).name for p in sin_git)}", "Operaciones",
            "\n".join(f"SIN GIT: {p}" for p in sin_git),
            "Mismo tratamiento que el lab: repo + primer commit.")

    return out


# ─────────────────────────── nodos por capa ───────────────────────────
def nodos(s: dict) -> list[dict]:
    kh = s["knowledge_health"]["parsed"]
    kh_ciego_txt = kh_ciego(s)
    h = {x["t"]: x for x in huecos(s)}
    def p0(t): return any(x["p"] == "P0" for x in huecos(s) if t.split(" ")[0] in x["t"])
    err_rag = next((e for e in s["crons"]["error"]), None)
    gpu_txt = s["gpu"]
    errs_tot = len(s["crons"]["error"])
    git_lab = s["repos"].get(str(LAB), {})

    capas = [
        {"code": "05-inference", "nombre": "Inferencia", "meta": f"{s['capas'].get('05-inference', 0)} entradas · GPU {gpu_txt.split(',')[0] or 'n/d'}", "nodes": [
            {"id": "lmstudio", "t": "LM Studio (puerto 1234)", "s": "ok" if s["inferencia"]["lmstudio_cargado"] else "warn",
             "d": "Motor principal de inferencia local.",
             "meas": (s["inferencia"]["lmstudio"].splitlines()[1] if len(s["inferencia"]["lmstudio"].splitlines()) > 1 else s["inferencia"]["lmstudio"]),
             "evid": "$ lms ps\n" + s["inferencia"]["lmstudio"], "fix": "Nada."},
            {"id": "ollama", "t": "Ollama (puerto 11434)", "s": "ok" if s["inferencia"]["ollama_modelos"] else "bad",
             "d": "Segundo motor, API compatible OpenAI.",
             "meas": f"{len(s['inferencia']['ollama_modelos'])} modelos: {', '.join(s['inferencia']['ollama_modelos'][:3]) or 'sin respuesta'}",
             "evid": "$ curl -s localhost:11434/v1/models\n" + (s["inferencia"]["ollama_raw"][:300] or "sin respuesta"), "fix": "Nada."},
            {"id": "comfyui", "t": "ComfyUI (bajo demanda)", "s": "ok" if s["inferencia"]["comfyui"] in ("active", "inactive") else "bad",
             "d": "Generación de imagen local para arte de fichas e infografías.",
             "meas": f"systemctl --user is-active comfyui → {s['inferencia']['comfyui']}",
             "evid": "$ systemctl --user is-active comfyui\n" + s["inferencia"]["comfyui"],
             "fix": "Pararlo cuando no se usa es lo correcto: libera VRAM."},
            {"id": "gpu", "t": "GPU " + (gpu_txt.split(",")[0] or "NVIDIA"), "s": "ok" if gpu_txt else "bad",
             "d": "Memoria y temperatura reales del acelerador.",
             "meas": gpu_txt or "sin datos", "evid": "$ nvidia-smi --query-gpu=name,memory.used,memory.total,utilization.gpu,temperature.gpu --format=csv,noheader\n" + gpu_txt,
             "fix": "Si la VRAM va justa: descargar el modelo de visión antes de generar imagen."},
            {"id": "mcp", "t": f"MCP del lab ({len(s['mcp'])})", "s": "ok" if s["mcp"] else "bad",
             "d": "Herramientas del agente contra las bases del lab.",
             "meas": " · ".join(s["mcp"]) or "ninguno",
             "evid": "$ grep -A20 '^mcp_servers' ~/.hermes/config.yaml → " + ", ".join(s["mcp"]),
             "fix": "No hay MCP de git ni de inventario de crons: son justo los dos huecos P0/P1 de la lista."},
        ]},
        {"code": "03-automation", "nombre": "Automatización", "meta": f"{s['capas'].get('03-automation', 0)} entradas · {s['crons']['total']} crons", "nodes": [
            {"id": "crones", "t": "Crons de Hermes", "s": "ok" if not s["crons"]["error"] else "warn",
             "d": "El motor real del lab: jobs diarios, horarios y semanales.",
             "meas": f"{s['crons']['total']} total · {s['crons']['enabled']} activos · {len(s['crons']['error'])} en error · {s['crons']['ok']} ok",
             "evid": "$ cat ~/.hermes/cron/jobs.json (recuento)\ntotal=%d enabled=%d error=%s" % (s["crons"]["total"], s["crons"]["enabled"], [e["nombre"] for e in s["crons"]["error"]]),
             "fix": "Ver el hueco P0 de los jobs en error."},
            {"id": "ragjob", "t": f"job: {err_rag['nombre']}" if err_rag else "jobs en error: ninguno",
             "s": "bad" if err_rag else "ok",
             "d": "Job del RAG que alimenta las búsquedas del agente." if err_rag else "No hay ningún job con last_status=error.",
             "meas": (f"last_status=error · streak={err_rag.get('streak')} · {err_rag.get('last')}" if err_rag else "todos en ok"),
             "evid": (f"job '{err_rag['nombre']}' {{status:'error', failure_streak:{err_rag.get('streak')}, last:'{err_rag.get('last')}'}}" if err_rag else "sin errores: %d jobs ok de %d" % (s["crons"]["ok"], s["crons"]["total"])),
             "fix": "Leer su log y decidir si el catchup lo cubre." if err_rag else "Nada.", "crit": bool(err_rag), "prio": "P0" if err_rag else ""},
            {"id": "crontab", "t": f"crontab del sistema ({len(s['crontab'])} líneas)", "s": "warn" if any("healthcheck" in l for l in s["crontab"]) else "ok",
             "d": "Automatizaciones fuera de Hermes: healthchecks, state-manager, backups.",
             "meas": " · ".join(sorted({re.sub(r'\s+', ' ', l).split(' ')[5][:34] if len(l.split(' ')) > 5 else '?' for l in s["crontab"]})[:4]),
             "evid": "\n".join(l[:120] for l in s["crontab"][:4]),
             "fix": "Los vigilantes apuntan a logs que hay que comprobar (ver nodo de logs)."},
            {"id": "logsvig", "t": "Logs de los vigilantes", "s": "ok" if all(bool(v["existe"] and v["lineas"]) for v in s["logs"].values()) else "bad",
             "d": "Un vigilante del que no queda registro no es un vigilante.",
             "meas": " · ".join(f"{k}: {'ok' if v['existe'] and v['lineas'] else 'sin registro'}" for k, v in s["logs"].items()),
             "evid": "\n".join(f"$ tail -2 {k}\n{(v['ultima'] or '(sin salida)')[:160]}" for k, v in s["logs"].items()),
             "fix": "Arreglar la ruta del log y verificar que escribe también cuando todo va bien.", "prio": "P1"},
        ]},
        {"code": "01-knowledge", "nombre": "Conocimiento", "meta": f"{s['capas'].get('01-knowledge', 0)} entradas · {kh['docs'] or '?'} docs · {s['objetos']['total']} objetos", "nodes": [
            {"id": "salud", "t": "Knowledge health", "s": "bad" if kh_ciego_txt else ("ok" if (kh["score"] or 0) >= 90 else "warn"),
             "d": "El propio lab puntúa su estructura documental.",
             "meas": f"sin datos · {kh_ciego_txt}" if kh_ciego_txt else f"KNOWLEDGE HEALTH {kh['score']}/100 · supervivencia DEC {kh['supervivencia']}%",
             "evid": f"$ {s['knowledge_health'].get('py') or 'python3'} tools/knowledge_health.py\n" + "\n".join(s["knowledge_health"]["salida"].splitlines()[-6:]),
             "fix": "Es puntuación de estructura, no de utilidad: mira los nodos de al lado."},
            {"id": "objetos", "t": "Objetos de conocimiento", "s": "warn" if s["objetos"]["bak"] else "ok",
             "d": "Los ficheros que gobiernan el lab: reglas, decisiones, predicciones, patrones.",
             "meas": f"{s['objetos']['total']} entradas · vivos {s['objetos']['total'] - s['objetos']['bak']} · .bak {s['objetos']['bak']} · {s['objetos']['por_tipo']}",
             "evid": "$ ls 01-knowledge/objects | wc -l → %d\npor tipo: %s" % (s["objetos"]["total"], s["objetos"]["por_tipo"]),
             "fix": "Sacar los .bak de la carpeta canónica."},
            {"id": "corpus", "t": "Corpus documental", "s": "ok" if s["conocimiento"].get("observations") else "warn",
             "d": "Experimentos, observaciones, modelos y patrones documentados.",
             "meas": " · ".join(f"{k} {v}" for k, v in sorted(s["conocimiento"].items()) if v),
             "evid": "01-knowledge/{ " + ", ".join(f"{k}:{v}" for k, v in sorted(s["conocimiento"].items()) if v) + " }",
             "fix": "Nada."},
            {"id": "enlaces", "t": "Enlaces entre documentos", "s": "ok" if (kh["enlaces"][0] or 0) / max(kh["enlaces"][1] or 1, 1) >= 0.2 else "bad",
             "d": "Cuánto se referencian los documentos entre sí.",
             "meas": f"Con enlaces: {kh['enlaces'][0]}/{kh['enlaces'][1]}",
             "evid": "Estructura documental:\n  Frontmatter: %s/%s\n  Con enlaces: %s/%s" % (kh["frontmatter"][0], kh["frontmatter"][1], kh["enlaces"][0], kh["enlaces"][1]),
             "fix": "Enlazar al reutilizar una DEC, un patrón o una observación.", "prio": "P1"},
            {"id": "contrato", "t": "Contrato de evidencia", "s": "ok" if (kh["contrato"][0] or 0) >= (kh["contrato"][1] or 1) else "bad",
             "d": "Regla del lab: cada afirmación con su fuente.",
             "meas": f"Cumplen contrato: {kh['contrato'][0]}/{kh['contrato'][1]}",
             "evid": "Evidence Contract:\n  Cumplen contrato:  %s/%s" % (kh["contrato"][0], kh["contrato"][1]),
             "fix": "Validar el medidor antes de tocar documentos.", "prio": "P1"},
            {"id": "reports", "t": "Carpeta reports/", "s": "ok" if s["reports"]["total"] >= 3 else "bad",
             "d": "Capa prevista para informes consolidados.",
             "meas": f"{s['reports']['total']} entradas",
             "evid": f"reports: {s['reports']['total']} entradas",
             "fix": "Generador de informes o fuera del árbol.", "prio": "P1"},
        ]},
        {"code": "04-operations", "nombre": "Operaciones", "meta": f"{s['capas'].get('04-operations', 0)} entradas · tools, tests, verificación", "nodes": [
            {"id": "tools", "t": "tools/", "s": "bad" if s["tools"]["bak"] / max(s["tools"]["total"], 1) > 0.3 else "ok",
             "d": "Cajas de herramientas del lab. Crecen rápido y sin poda.",
             "meas": f"{s['tools']['total']} ficheros · {s['tools']['bak']} son .bak ({round(100 * s['tools']['bak'] / max(s['tools']['total'], 1))} %)",
             "evid": "$ ls tools | wc -l → %d\n$ ls tools/*.bak* | wc -l → %d" % (s["tools"]["total"], s["tools"]["bak"]),
             "fix": "Archivar los .bak antiguos fuera de tools/.", "prio": "P2"},
            {"id": "gitlab", "t": "Control de versiones del lab", "s": "ok" if git_lab.get("git") else "bad",
             "d": "Historial y vuelta atrás del lab entero." if not git_lab.get("git") else "El lab ya está versionado.",
             "meas": ("git status → " + (git_lab.get("evidencia") or "sin repo")) if not git_lab.get("git") else git_lab.get("last", ""),
             "evid": ("$ git -C ~/joko-lab status -sb\n" + (git_lab.get("evidencia") or "")) if not git_lab.get("git") else "$ git log -1 → " + git_lab.get("last", ""),
             "fix": "Inicializar repo y sumarlo a git-backup.sh.", "crit": not git_lab.get("git"), "prio": "P0" if not git_lab.get("git") else ""},
            {"id": "repos", "t": "Repos hermanos", "s": "warn" if any(not i["git"] for i in s["repos"].values()) else "ok",
             "d": "Comparativa de qué proyectos sí tienen historial.",
             "meas": " · ".join(f"{Path(p).name} {'SÍ' if i['git'] else 'NO'}" for p, i in s["repos"].items()),
             "evid": "\n".join(f"{'REPO' if i['git'] else 'SIN GIT'}: {p} {i.get('last', i.get('evidencia', ''))[:60]}" for p, i in s["repos"].items()),
             "fix": "Que el proyecto principal sea el único sin historial es la incoherencia a corregir."},
            {"id": "verif", "t": "tests/ y verification/", "s": "ok" if s["tests"]["total"] and s["verification"]["total"] else "warn",
             "d": "Red de seguridad del código del lab.",
             "meas": f"tests {s['tests']['total']} · verification {s['verification']['total']}",
             "evid": f"tests/ → {s['tests']['total']} · verification/ → {s['verification']['total']}", "fix": "Nada."},
            {"id": "instr", "t": "instruments/", "s": "ok" if s["instruments"]["total"] >= 3 else "bad",
             "d": "Instrumentos de medida del lab.",
             "meas": f"{s['instruments']['total']} entradas: {', '.join(s['instruments']['lista']) or '—'}",
             "evid": "instruments/ → " + ", ".join(s["instruments"]["lista"]),
             "fix": "Faltan medidor de contrato de evidencia, gate de veracidad y medidor de alucinaciones.", "prio": "P2"},
            {"id": "varias", "t": "assets/ · inbox/", "s": "warn",
             "d": "Carpetas creadas y casi sin uso.",
             "meas": f"assets {s['assets']['total']} · inbox {s['inbox']['total']}",
             "evid": "\n".join(f"{n}: {s[n]['total']} entradas" for n in ("assets", "inbox", "reports", "instruments")),
             "fix": "Unificar criterio: se usan o se retiran.", "prio": "P2"},
            {"id": "lpadocs", "t": "lpa/ · docs/ · research/", "s": "ok",
             "d": "Programa de investigación, documentación oficial y research.",
             "meas": f"lpa {s['lpa']['total']} · docs {s['docs']['total']} · research {s['research']['total']}",
             "evid": f"lpa/ → {s['lpa']['total']} · docs/ → {s['docs']['total']} · research/ → {s['research']['total']}", "fix": "Nada."},
        ]},
        {"code": "02-infrastructure", "nombre": "Infraestructura", "meta": f"{s['capas'].get('02-infrastructure', 0)} entradas · red, Docker, backups", "nodes": [
            {"id": "puertos", "t": "Servicios escuchando", "s": "ok" if s["puertos"] else "bad",
             "d": "Lo que hay realmente levantado en el host.",
             "meas": f"{len(s['puertos'])} puertos: " + " ".join(str(x) for x in s["puertos"][:12]),
             "evid": "$ ss -ltn | awk '{print $4}' | sed 's/.*://' | sort -n | uniq\n" + " ".join(str(x) for x in s["puertos"]),
             "fix": "Falta el inventario 'puerto → servicio → para qué sirve' dentro del lab."},
            {"id": "dockerlog", "t": "Vigilancia de servicios", "s": "ok" if all(v["existe"] and v["lineas"] for v in s["logs"].values()) else "warn",
             "d": "Healthchecks de Docker y n8n del crontab.",
             "meas": " · ".join(f"{k}: {v['lineas']} líneas" for k, v in s["logs"].items()),
             "evid": "\n".join(f"{k}: existe={v['existe']} lineas={v['lineas']} ultima={(v['ultima'] or '(sin salida)')[:120]}" for k, v in s["logs"].items()),
             "fix": "El estado del stack se consulta en solo lectura (docker compose ps); nunca reiniciando a ciegas.", "prio": "P1"},
            {"id": "n8n", "t": "n8n (puerto 5678)", "s": "warn" if 5678 not in s["puertos"] else "ok",
             "d": "Servicio protegido del lab: workflows y credenciales.",
             "meas": ("escuchando en 5678" if 5678 in s["puertos"] else "5678 no aparece en la lista"),
             "evid": "puertos en escucha: … 5678 …" if 5678 in s["puertos"] else "5678 no aparece en ss -ltn",
             "fix": "Solo se vigila. No se para, ni reinicia, ni recrea sin confirmación explícita."},
            {"id": "backups", "t": "Backups", "s": "warn" if not git_lab.get("git") else "ok",
             "d": "Copia diaria del lab y del estado de Hermes.",
             "meas": f"jobs con 'backup': {len(s['backups']['jobs'])} · destino /mnt/ssd_ia_datos/backups: {'existe' if s['backups']['destino_existe'] else 'NO'}",
             "evid": "jobs: " + (", ".join(s["backups"]["jobs"]) or "—") + f"\ndestino existe: {s['backups']['destino_existe']}",
             "fix": "Hay copia, pero sin git no hay historial navegable: los dos arreglos van juntos.", "prio": "P1"},
        ]},
    ]
    return capas


def kpis(s: dict) -> list[dict]:
    hs = huecos(s)
    p0 = sum(1 for h in hs if h["p"] == "P0")
    p1 = sum(1 for h in hs if h["p"] == "P1")
    p2 = sum(1 for h in hs if h["p"] == "P2")
    kh = s["knowledge_health"]["parsed"]
    return [
        {"v": str(s["crons"]["total"]), "l": "crons Hermes", "n": f"{s['crons']['enabled']} activos · {len(s['crons']['error'])} en error", "s": "ok" if not s["crons"]["error"] else "warn", "go": "capa-03-automation"},
        {"v": str(s["skills"]["total"]), "l": "skills", "n": f"{s['skills']['por_categoria'].get('joko-lab', 0)} de dominio joko-lab", "s": "info", "go": "resumen"},
        {"v": str(kh["docs"] or 0), "l": "docs de conocimiento", "n": f"frontmatter {kh['frontmatter'][0]}/{kh['frontmatter'][1]}", "s": "ok", "go": "capa-01-knowledge"},
        {"v": str(len(hs)), "l": "huecos detectados", "n": f"{p0} críticos · {p1} altos · {p2} menores", "s": "bad" if p0 else ("warn" if p1 else "ok"), "go": "falt"},
        {"v": f"{len(s['mcp'])}", "l": "MCP conectados", "n": " · ".join(s["mcp"]) or "ninguno", "s": "ok" if s["mcp"] else "bad", "go": "capa-05-inference"},
        {"v": str((1 if s["inferencia"]["lmstudio_cargado"] else 0) + (1 if s["inferencia"]["ollama_modelos"] else 0)), "l": "motores vivos", "n": "LM Studio + Ollama", "s": "ok", "go": "capa-05-inference"},
        {"v": str(s["objetos"]["total"] - s["objetos"]["bak"]), "l": "objetos vivos", "n": " · ".join(f"{v} {k}" for k, v in list(s["objetos"]["por_tipo"].items())[:3]), "s": "info", "go": "capa-01-knowledge"},
        {"v": str(s["tools"]["bak"]), "l": ".bak en tools/", "n": f"de {s['tools']['total']} ficheros", "s": "bad", "go": "capa-04-operations"},
    ]


CSS = """<style>
:root{--bg:#0a0d13;--panel:#141b26;--panel2:#1a2331;--line:#243044;--txt:#e8eef7;--dim:#8ea0b8;--dim2:#5f7186;
--ok:#33d17a;--warn:#f5b942;--bad:#ff5d5d;--info:#4ea1ff;--mono:ui-monospace,"JetBrains Mono",Menlo,Consolas,monospace;
--sans:Inter,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
*{box-sizing:border-box}html,body{margin:0;background:radial-gradient(1200px 600px at 20% -10%,#16233a 0%,var(--bg) 55%) no-repeat,var(--bg);
color:var(--txt);font-family:var(--sans);-webkit-font-smoothing:antialiased}
.wrap{max-width:1600px;margin:0 auto;padding:24px 24px 60px}
header.top{display:flex;flex-wrap:wrap;gap:16px;align-items:flex-end;justify-content:space-between;border-bottom:1px solid var(--line);padding-bottom:14px}
.brand{display:flex;align-items:center;gap:13px}.logo{width:44px;height:44px;border-radius:12px;background:linear-gradient(145deg,#2b3f63,#111826);
display:grid;place-items:center;font-weight:800;color:#cfe3ff;border:1px solid #33405e;font-size:18px}
h1{margin:0;font-size:22px;letter-spacing:-.3px}.sub{color:var(--dim);font-size:12.5px;margin-top:3px}
.stamp{font-family:var(--mono);font-size:11px;color:var(--dim2);text-align:right;line-height:1.7}.stamp b{color:var(--ok)}
.bar{display:flex;flex-wrap:wrap;gap:9px;align-items:center;margin:16px 0 12px}
.seg{display:flex;background:var(--panel);border:1px solid var(--line);border-radius:11px;overflow:hidden}
.seg button{background:none;border:0;color:var(--dim);padding:9px 14px;font:600 12.5px var(--sans);cursor:pointer}
.seg button.on{background:#22314a;color:#fff}.seg button:hover{color:#fff}
input.search{background:var(--panel);border:1px solid var(--line);border-radius:11px;padding:10px 13px;color:var(--txt);font:13px var(--sans);min-width:220px;outline:none}
.spacer{flex:1}.kpibar{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:10px;margin:6px 0 18px}
.kpi{background:linear-gradient(180deg,var(--panel2),var(--panel));border:1px solid var(--line);border-radius:14px;padding:12px;cursor:pointer}
.kpi:hover{border-color:#3a537a}.kpi .v{font-size:21px;font-weight:750;letter-spacing:-.5px}
.kpi .l{font-size:10.5px;color:var(--dim);text-transform:uppercase;letter-spacing:.7px;margin-top:3px}
.kpi .n{font-size:10.5px;color:var(--dim2);margin-top:6px}
.kpi.bad .v{color:var(--bad)}.kpi.warn .v{color:var(--warn)}.kpi.ok .v{color:var(--ok)}.kpi.info .v{color:var(--info)}
/* ── solapas ── */
.tabs{display:flex;flex-wrap:wrap;align-items:flex-end;gap:5px;margin:18px 0 0;border-bottom:1px solid var(--line)}
.tg{display:flex;gap:5px;align-items:flex-end}
.tsep{width:1px;height:24px;background:var(--line);margin:0 7px 7px}
.tab{background:#0f1620;border:1px solid var(--line);border-bottom:0;border-radius:10px 10px 0 0;color:var(--dim);
padding:9px 13px;font:600 12.5px var(--sans);cursor:pointer;display:flex;align-items:center;gap:7px;position:relative;top:1px}
.tab:hover{color:#fff;background:#182233}
.tab.on{background:var(--panel);color:#fff;border-color:#3a537a;box-shadow:inset 0 2px 0 var(--info)}
.tab .cnt{font-family:var(--mono);font-size:10px;color:var(--dim2)}
.tab .cnt.bad{color:var(--bad)}.tab .cnt.warn{color:var(--warn)}
.view{display:none}.view.on{display:block;padding-top:14px}
.vhead{display:flex;flex-wrap:wrap;gap:10px;align-items:baseline;justify-content:space-between;margin:4px 0 12px}
.vhead h2{margin:0;font-size:17px;letter-spacing:-.2px}
.vhead .code{font-family:var(--mono);font-size:10px;color:var(--dim2);background:#0e141e;border:1px solid var(--line);padding:1px 6px;border-radius:6px;margin-left:7px}
.vhead .meta{color:var(--dim2);font-size:11.5px}
.caps{display:grid;grid-template-columns:repeat(auto-fit,minmax(208px,1fr));gap:10px;margin-bottom:16px}
.capcard{background:linear-gradient(180deg,var(--panel2),var(--panel));border:1px solid var(--line);border-radius:13px;
padding:12px;cursor:pointer;transition:.14s}
.capcard:hover{border-color:#3a537a;transform:translateY(-1px)}
.capcard .n{font-size:13px;font-weight:650;display:flex;align-items:center;gap:7px}
.capcard .c{font-family:var(--mono);font-size:10px;color:var(--dim2);margin:3px 0 8px}
.capcard .st{display:flex;gap:10px;font-size:11.5px;color:var(--dim);flex-wrap:wrap}
.capcard .st b{font-family:var(--mono)}
.p0row{display:flex;gap:9px;align-items:center;padding:7px 10px;border:1px solid var(--line);border-left:3px solid var(--bad);
border-radius:9px;background:var(--panel);margin-bottom:7px;font-size:12.5px;cursor:pointer}
.p0row:hover{background:#1a2432}
.p0row .mono{font-size:10.5px;color:var(--dim2);margin-left:auto}
.nodes{display:grid;grid-template-columns:repeat(auto-fill,minmax(430px,1fr));gap:10px;align-items:start}
@media(max-width:940px){.nodes{grid-template-columns:1fr}}
.node{background:var(--panel);border:1px solid var(--line);border-left:3px solid var(--dim2);border-radius:11px;padding:10px 12px;cursor:pointer;transition:.14s}
.node:hover{background:#1c2739}
.node.ok{border-left-color:var(--ok)}.node.warn{border-left-color:var(--warn)}.node.bad{border-left-color:var(--bad)}
.node.crit{background:linear-gradient(90deg,rgba(255,93,93,.12),var(--panel));border-color:#5a2b2b}
.node.hide{opacity:.13;filter:grayscale(.7)}
.node.open{background:#1a2432;border-color:#3a537a}
.node .cab{display:flex;gap:10px;align-items:flex-start;justify-content:space-between}
.node .t{font-size:12.8px;font-weight:600;display:flex;align-items:center;gap:7px;flex-wrap:wrap}
.node .measr{font-family:var(--mono);font-size:10.5px;color:#9fb4cf;text-align:right;max-width:44%}
.node .chev{color:var(--dim2);font-size:14px;display:inline-block;transition:.16s;margin-left:3px}
.node.open .chev{transform:rotate(90deg);color:var(--info)}
.node .det{display:none}
.node.open .det{display:block;margin-top:10px;border-top:1px dashed var(--line);padding-top:10px}
.node .d{font-size:12px;color:var(--dim);line-height:1.55}
.dot{width:8px;height:8px;border-radius:50%;flex:0 0 auto}.dot.ok{background:var(--ok)}.dot.warn{background:var(--warn)}.dot.bad{background:var(--bad)}
.evid{background:#0b1119;border:1px solid var(--line);border-radius:9px;padding:9px 10px;font-family:var(--mono);font-size:10.5px;
color:#9fd4b4;white-space:pre-wrap;word-break:break-word;line-height:1.55}
.evid.bad{color:#ffb3b3;border-color:#4a2727;background:#160e0e}
.lbl{font-size:10px;text-transform:uppercase;letter-spacing:.8px;color:var(--dim2);margin:11px 0 5px;font-weight:700}
.fix{border-left:2px solid var(--info);padding-left:10px;font-size:12.5px;color:#d6e3f5;line-height:1.6}
table.falt{width:100%;border-collapse:collapse;font-size:12.5px}
table.falt th{text-align:left;font-size:10.5px;text-transform:uppercase;letter-spacing:.7px;color:var(--dim2);border-bottom:1px solid var(--line);padding:8px 9px}
table.falt td{border-bottom:1px solid #1b2431;padding:10px 9px;vertical-align:top;color:#cfdcec}
tr.main:hover td{background:#141d2a;cursor:pointer}
tr.detrow{display:none}
tr.detrow.on{display:table-row}
tr.detrow>td{background:#0d141d;border-bottom:1px solid var(--line);padding:2px 16px 16px}
.mono{font-family:var(--mono);font-size:11px;color:#9fb4cf;white-space:pre-wrap}
.tag{font-size:9.5px;font-family:var(--mono);padding:1px 5px;border-radius:5px;border:1px solid var(--line);color:var(--dim);text-transform:uppercase}
.tag.p0{color:#ffd0d0;border-color:#7a3333;background:#3a1a1a}.tag.p1{color:#ffe6bf;border-color:#7a5a2b;background:#3a2c14}
.tag.p2{color:#cfe0ff;border-color:#33507a;background:#16233a}
.legend{display:flex;gap:14px;flex-wrap:wrap;font-size:11.5px;color:var(--dim);margin-bottom:11px}
.legend span{display:flex;align-items:center;gap:6px}
footer.note{margin-top:20px;border-top:1px solid var(--line);padding-top:13px;color:var(--dim2);font-size:11.5px;line-height:1.75}
</style>"""

JS = """<script>
const PANEL = __PANEL__;
const esc = s => String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
const dot = s => `<i class="dot ${s}"></i>`;
const TODOS = PANEL.capas.flatMap(L=>L.nodes.map(n=>({...n,capa:L.nombre,cc:L.code})));

document.getElementById('ts').textContent = PANEL.snap.ts;
document.getElementById('nodo-n').textContent = TODOS.length;
document.getElementById('hueco-n').textContent = PANEL.huecos.length;

/* ── solapas: Resumen · una por capa · Qué falta · Inventario ── */
const TABS = [{v:'resumen',t:'Resumen'},
  ...PANEL.capas.map(L=>({v:'capa-'+L.code,t:L.nombre,cnt:L.nodes.length,
    bad:L.nodes.filter(n=>n.s==='bad').length, warn:L.nodes.filter(n=>n.s==='warn').length})),
  {v:'falt',t:'Qué falta',cnt:PANEL.huecos.length,bad:PANEL.huecos.filter(h=>h.p==='P0').length,
    warn:PANEL.huecos.filter(h=>h.p==='P1').length},
  {v:'list',t:'Inventario',cnt:TODOS.length}];
document.getElementById('tabs').innerHTML = TABS.map((t,i)=>{
  const sep = (i===1 || t.v==='falt') ? '<span class="tsep"></span>' : '';
  const cnt = t.cnt ? `<span class="cnt ${t.bad?'bad':(t.warn?'warn':'')}">${t.cnt}</span>` : '';
  return sep+`<button class="tab" role="tab" aria-selected="false" data-v="${t.v}">${t.t}${cnt}</button>`;}).join('');

/* ── resumen: KPIs, estado por capa y prioridades abiertas ── */
document.getElementById('kpibar').innerHTML = PANEL.kpis.map(k=>`
  <div class="kpi ${k.s}" data-go="${k.go}"><div class="v">${k.v}</div><div class="l">${esc(k.l)}</div><div class="n">${esc(k.n)}</div></div>`).join('');

document.getElementById('caps').innerHTML = PANEL.capas.map(L=>{
  const ok=L.nodes.filter(n=>n.s==='ok').length, w=L.nodes.filter(n=>n.s==='warn').length, b=L.nodes.filter(n=>n.s==='bad').length;
  return `<div class="capcard" data-go="capa-${L.code}"><div class="n">${dot(b?'bad':(w?'warn':'ok'))}${esc(L.nombre)}</div>
  <div class="c">${esc(L.code)}</div><div class="st"><span>OK <b>${ok}</b></span><span>parcial <b>${w}</b></span><span>hueco <b>${b}</b></span></div></div>`;}).join('');

const ABIERTOS = PANEL.huecos.map((h,i)=>({...h,i})).filter(h=>h.p!=='P2');
document.getElementById('p0list').innerHTML = ABIERTOS.length ? ABIERTOS.map(h=>`
  <div class="p0row" data-go="falt" data-i="${h.i}"><span class="tag ${h.p.toLowerCase()}">${h.p}</span>
  <b>${esc(h.t)}</b><span class="mono">${esc(h.capa)}</span></div>`).join('')
  : '<i style="color:var(--dim2);font-size:12.5px">ningún hueco P0/P1 en esta instantánea</i>';

/* ── una solapa por capa: cada componente se despliega ahí mismo ── */
PANEL.capas.forEach(L=>{
  const cont = document.getElementById('nodes-'+L.code); if(!cont) return;
  cont.innerHTML = L.nodes.map(n=>`
    <div class="node ${n.s}${n.crit?' crit':''}" data-id="${n.id}" data-s="${n.s}" data-cc="${L.code}"
         data-t="${esc(n.t)}" data-capa="${esc(L.nombre)}">
      <div class="cab"><div class="t">${dot(n.s)}${esc(n.t)}${n.prio?` <span class="tag ${n.prio.toLowerCase()}">${n.prio}</span>`:''}</div>
      <div style="text-align:right;white-space:nowrap"><span class="measr">${esc(n.meas)}</span><span class="chev">▸</span></div></div>
      <div class="det"><div class="lbl">Estado</div><div class="d">${esc(n.d)}</div>
        <div class="lbl">Medición de hoy</div><div class="evid">${esc(n.meas)}</div>
        <div class="lbl">Evidencia (salida literal)</div><div class="evid ${/fatal|no existe|no aparece|SIN GIT|\\(sin salida\\)|error/i.test(n.evid)?'bad':''}">${esc(n.evid)}</div>
        ${n.fix?`<div class="lbl">Qué falta / qué haría</div><div class="fix">${esc(n.fix)}</div>`:''}</div></div>`).join('');
});

/* ── qué falta: cada fila despliega su evidencia debajo, en la misma solapa ── */
document.getElementById('faltbody').innerHTML = PANEL.huecos.map((h,i)=>`
  <tr class="main" data-i="${i}" data-t="${esc(h.t)}" data-capa="${esc(h.capa)}" data-p="${h.p}">
    <td style="width:64px"><span class="tag ${h.p.toLowerCase()}">${h.p}</span></td>
    <td style="width:250px"><b>${esc(h.t)}</b><div class="mono">${esc(h.capa)}</div></td>
    <td class="mono">${esc((h.ev.split('\\n')[0]||'').slice(0,150))}</td>
    <td style="width:80px"><span class="chev">▸</span> ver</td></tr>
  <tr class="detrow" id="detf-${i}"><td colspan="4">
    <div class="lbl">Evidencia (salida literal)</div><div class="evid bad">${esc(h.ev)}</div>
    <div class="lbl">Cómo se cierra</div><div class="fix">${esc(h.fix)}</div></td></tr>`).join('');

/* ── inventario plano (clic en una fila → su solapa de capa, nodo abierto) ── */
document.getElementById('listbody').innerHTML = TODOS.map(n=>`
  <tr class="main" data-id="${n.id}" data-cc="${n.cc}"><td class="mono" style="width:150px">${esc(n.cc)}</td>
  <td style="width:240px"><b>${esc(n.t)}</b></td>
  <td style="width:92px">${dot(n.s)}<span style="font-size:11.5px;color:var(--dim)">${n.s==='ok'?'OK':(n.s==='warn'?'parcial':'hueco')}</span></td>
  <td class="mono">${esc(n.meas)}</td></tr>`).join('');

/* ── navegación ── */
function vista(v, sinScroll){
  if(!document.getElementById('v-'+v)) v = 'resumen';
  document.querySelectorAll('.view').forEach(s=>s.classList.toggle('on', s.id==='v-'+v));
  document.querySelectorAll('#tabs .tab').forEach(b=>{const on=b.dataset.v===v;
    b.classList.toggle('on',on); b.setAttribute('aria-selected',on?'true':'false');});
  if(!sinScroll) window.scrollTo({top:0, behavior:'smooth'});
  return v;
}
function abrir(id, sinScroll){
  const n = TODOS.find(x=>x.id===id); if(!n) return;
  vista('capa-'+n.cc, true);
  document.querySelectorAll('.node').forEach(el=>el.classList.toggle('open', el.dataset.id===id));
  const el = document.querySelector('.node[data-id="'+id+'"]');
  if(el && !sinScroll) el.scrollIntoView({block:'center', behavior:'smooth'});
}

document.addEventListener('click', e=>{
  const tab = e.target.closest('#tabs .tab');
  if(tab){ vista(tab.dataset.v); return; }
  const go = e.target.closest('[data-go]');
  if(go){ const v = vista(go.dataset.go);
    if(v==='falt' && go.dataset.i!==undefined){
      const d = document.getElementById('detf-'+go.dataset.i); if(d) d.classList.add('on');
      const tr = document.querySelector('#faltbody tr.main[data-i="'+go.dataset.i+'"]');
      if(tr) tr.scrollIntoView({block:'center', behavior:'smooth'});
    } return; }
  const nd = e.target.closest('.node'); if(nd){ nd.classList.toggle('open'); return; }
  const tr = e.target.closest('tr.main');
  if(tr){
    if(tr.dataset.i!==undefined){ const d=document.getElementById('detf-'+tr.dataset.i); if(d) d.classList.toggle('on'); return; }
    if(tr.dataset.id){ abrir(tr.dataset.id); return; }
  }
});

/* ── filtro y búsqueda (los nodos se atenúan; las filas se ocultan) ── */
let filtro='all', texto='';
function aplicar(){
  document.querySelectorAll('.node').forEach(el=>{
    const okF = filtro==='all' || el.dataset.s===filtro;
    const okT = !texto || (el.dataset.t+' '+el.dataset.capa+' '+el.textContent).toLowerCase().includes(texto);
    el.classList.toggle('hide', !(okF&&okT));});
  document.querySelectorAll('#faltbody tr.main').forEach(tr=>{
    const okF = filtro==='all' || filtro==='bad' || (filtro==='warn' ? tr.dataset.p!=='P0' : false);
    const okT = !texto || (tr.dataset.t+' '+tr.dataset.capa+' '+tr.textContent).toLowerCase().includes(texto);
    const ver = okF&&okT; tr.style.display = ver?'':'none';
    const d = document.getElementById('detf-'+tr.dataset.i); if(d && !ver) d.classList.remove('on');});
  document.querySelectorAll('#listbody tr.main').forEach(tr=>{
    const n = TODOS.find(x=>x.id===tr.dataset.id);
    const okF = filtro==='all' || n.s===filtro;
    const okT = !texto || (n.t+' '+n.d+' '+n.id).toLowerCase().includes(texto);
    tr.style.display = (okF&&okT)?'':'none';});
}
document.querySelectorAll('#filters button').forEach(b=>b.onclick=()=>{filtro=b.dataset.f;
  document.querySelectorAll('#filters button').forEach(x=>x.classList.toggle('on',x===b)); aplicar();});
document.getElementById('q').oninput = e=>{texto=e.target.value.toLowerCase().trim(); aplicar();};

/* ── la interfaz recuerda dónde estabas (solapa, filtro, búsqueda, nodo) ── */
const UIKEY='labpanel_ui';
function guardarUI(){try{sessionStorage.setItem(UIKEY,JSON.stringify({
  v:(document.querySelector('.view.on')||{id:'v-resumen'}).id.slice(2), f:filtro, t:texto,
  n:(document.querySelector('.node.open')||{dataset:{}}).dataset.id||''}));}catch(e){}}
function restaurarUI(){try{const u=JSON.parse(sessionStorage.getItem(UIKEY)||'null'); if(!u)return;
  if(u.f){const b=[...document.querySelectorAll('#filters button')].find(x=>x.dataset.f===u.f); if(b)b.click();}
  if(u.t){const q=document.getElementById('q'); q.value=u.t; texto=u.t.toLowerCase().trim(); aplicar();}
  if(u.v)vista(u.v,true);
  if(u.n)abrir(u.n,true);}catch(e){}}
document.addEventListener('click',()=>setTimeout(guardarUI,0));   // diferido: primero cambia la solapa, luego se guarda
document.getElementById('q').addEventListener('input',()=>setTimeout(guardarUI,0));
setTimeout(restaurarUI,0);   // al final del script, cuando ya está pintado todo

/* ── enlace directo: #falt · #capa-04-operations · #capa-04-operations~gitlab ── */
(function(){const h=decodeURIComponent((location.hash||'').replace(/^#/,''));
  if(!h)return; const p=h.split('~'); if(p[0])vista(p[0],true); if(p[1])abrir(p[1],true);})();

/* ── autorefresco: la instantánea se regenera sola y esta pestaña se recarga ── */
const REFRESH = __REFRESH__;
if(REFRESH>0){
  const et = document.getElementById('auto');
  const txt = REFRESH<1 ? Math.round(REFRESH*60)+' s' : REFRESH+' min';
  if(et) et.textContent = '↻ autorefresco cada '+txt;
  setTimeout(()=>location.reload(), REFRESH*60000);
}
</script>"""


def render(s: dict, capas: list[dict], hs: list[dict], ks: list[dict], refresh_min: float = 0.0) -> str:
    panel = {"snap": s, "capas": capas, "huecos": hs, "kpis": ks}
    json_txt = json.dumps(panel, ensure_ascii=False).replace("</", "<\\/")
    p0 = sum(1 for h in hs if h["p"] == "P0")
    n_total = sum(len(c["nodes"]) for c in capas)

    def _e(t: object) -> str:  # escapado mínimo para texto que va a HTML
        return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    legend = ('<i class="dot ok"></i> funcionando &nbsp; <i class="dot warn"></i> parcial / sin uso &nbsp; '
              '<i class="dot bad"></i> hueco o error &nbsp; <span style="color:var(--dim2)">'
              '· clic en un componente → se despliega aquí mismo su estado, medición y evidencia literal</span>')

    # una solapa por capa, generada desde las capas reales de la instantánea
    capas_html = "\n".join(
        f'<section class="view" id="v-capa-{c["code"]}">'
        f'<div class="vhead"><h2>{_e(c["nombre"])}<span class="code">{_e(c["code"])}</span></h2>'
        f'<div class="meta">{_e(c["meta"])}</div></div>'
        f'<div class="legend"><span>{legend}</span></div>'
        f'<div class="nodes" id="nodes-{c["code"]}"></div></section>'
        for c in capas)

    html = f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Joko Lab · panel de estado</title>{CSS}</head><body><div class="wrap">
<header class="top"><div class="brand"><div class="logo">JL</div><div>
<h1>Joko Lab · panel de estado</h1>
<div class="sub">Instantánea real del sistema — <b>generada por tools/lab_panel.py</b>, sin datos de muestra.</div></div></div>
<div class="stamp">instantánea: <b id="ts">—</b><br>nodos <span id="nodo-n"></span> · huecos <span id="hueco-n"></span> · críticos {p0}<br>
<span id="auto" style="color:var(--ok)"></span><br>
solo lectura: ls · git status · jobs.json · knowledge_health.py · lms ps · nvidia-smi · ss · tail de logs</div></header>
<nav class="tabs" id="tabs" role="tablist"></nav>
<div class="bar"><div class="seg" id="filters"><button data-f="all" class="on">Todo</button><button data-f="bad">Huecos</button>
<button data-f="warn">Parcial</button><button data-f="ok">OK</button></div>
<input class="search" id="q" placeholder="filtrar por nombre… (p. ej. git, rag, mcp)"><div class="spacer"></div>
<span style="color:var(--dim2);font-size:11px">una solapa por sección · el filtro y el buscador se aplican a todas</span></div>
<section class="view on" id="v-resumen">
<div class="kpibar" id="kpibar"></div>
<div class="vhead"><h2>Estado por capa</h2><div class="meta">clic en una tarjeta → esa capa, ya separada en su solapa</div></div>
<div class="caps" id="caps"></div>
<div class="vhead"><h2>Prioridades abiertas (P0/P1)</h2><div class="meta">clic en una fila → su evidencia literal en la solapa «Qué falta»</div></div>
<div id="p0list"></div></section>
{capas_html}
<section class="view" id="v-falt">
<div class="vhead"><h2>Qué falta</h2><div class="meta">ordenado por impacto · {len(hs)} huecos · P0 {p0}</div></div>
<div class="legend"><span>cada fila despliega debajo su evidencia literal y cómo se cierra</span></div>
<table class="falt"><thead><tr><th style="width:64px">Prior.</th><th style="width:250px">Hueco</th><th>Evidencia real</th>
<th style="width:80px"></th></tr></thead><tbody id="faltbody"></tbody></table></section>
<section class="view" id="v-list">
<div class="vhead"><h2>Inventario</h2><div class="meta">{n_total} componentes en una tabla plana · clic en una fila → ese componente en su capa</div></div>
<table class="falt"><thead><tr><th style="width:150px">Capa</th><th style="width:240px">Componente</th>
<th style="width:92px">Estado</th><th>Medición real</th></tr></thead><tbody id="listbody"></tbody></table></section>
<footer class="note">Generado por <span class="mono">~/joko-lab/tools/lab_panel.py</span> a partir de una instantánea en modo lectura.
Regenerar: <span class="mono">python3 tools/lab_panel.py --once</span> · servir: <span class="mono">python3 tools/lab_panel.py --serve --open --refresh 5</span>.
Doble clic: <span class="mono">~/joko-lab/tools/lab-panel.sh</span> (o el lanzador del escritorio).
Enlace directo a una solapa: <span class="mono">index.html#falt</span> · <span class="mono">index.html#capa-04-operations</span> · <span class="mono">index.html#capa-04-operations~gitlab</span>.
Nada de lo que hay aquí modifica el sistema (n8n incluido: solo se consulta su puerto, nunca se toca el servicio).</footer>
</div>{JS.replace('__PANEL__', json_txt).replace('__REFRESH__', '%g' % refresh_min)}</body></html>"""
    return html


# ─────────────────────────── servidor ───────────────────────────
class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(OUT_DIR), **kw)

    def log_message(self, fmt, *args):  # silencio salvo errores
        if int(getattr(self, "last_status", 200) or 200) >= 400:
            sys.stderr.write("panel: " + fmt % args + "\n")


def generar(refresh_min: float = 0.0) -> tuple[dict, list, list, list]:
    """Recoge la instantánea, la escribe y devuelve (snapshot, capas, huecos, kpis)."""
    s = snapshot()
    capas = nodos(s)
    hs = huecos(s)
    ks = kpis(s)
    s["resumen"] = {"nodos": sum(len(c["nodes"]) for c in capas), "huecos": len(hs),
                    "p0": sum(1 for h in hs if h["p"] == "P0"), "p1": sum(1 for h in hs if h["p"] == "P1"),
                    "p2": sum(1 for h in hs if h["p"] == "P2")}
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "snapshot.json").write_text(json.dumps({"snap": s, "capas": capas, "huecos": hs, "kpis": ks},
                                                      ensure_ascii=False, indent=1), encoding="utf-8")
    (OUT_DIR / "index.html").write_text(render(s, capas, hs, ks, refresh_min), encoding="utf-8")
    return s, capas, hs, ks


def abrir_navegador(url: str) -> None:
    """Abre la URL en el navegador del escritorio. Si no hay entorno gráfico, solo lo dice."""
    if not (os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY")):
        print(f"panel: sin entorno gráfico detectado — abre tú {url}")
        return
    xdg = shutil.which("xdg-open")
    try:
        if xdg:
            subprocess.Popen([xdg, url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                             start_new_session=True)
        else:
            import webbrowser
            webbrowser.open(url)
        print(f"panel: abriendo el navegador en {url}")
    except Exception as e:  # nunca romper el panel por no poder abrir el navegador
        print(f"panel: no he podido abrir el navegador ({e}) — abre tú {url}")


def hilo_refresco(intervalo_min: float, parar: threading.Event) -> None:
    """Regenera la instantánea cada X minutos mientras el servidor está vivo."""
    while not parar.wait(intervalo_min * 60):
        try:
            s, _, hs, _ = generar(intervalo_min)
            hh = datetime.now().strftime("%H:%M:%S")
            print(f"  ↻ {hh} regenerado · nodos {s['resumen']['nodos']} · huecos {s['resumen']['huecos']} "
                  f"(P0 {s['resumen']['p0']}) · la pestaña abierta se recarga sola")
        except Exception as e:
            print(f"  ↻ fallo al regenerar ({e}) — sigo sirviendo la última instantánea")


def main() -> int:
    try:  # sin terminal (nohup → fichero) Python bufferiza y el log saldría vacío al parar
        sys.stdout.reconfigure(line_buffering=True)
        sys.stderr.reconfigure(line_buffering=True)
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="Panel de estado del Joko Lab (solo lectura).")
    ap.add_argument("--once", action="store_true", help="genera instantánea + HTML y sale")
    ap.add_argument("--serve", action="store_true", help="genera y sirve en localhost hasta Ctrl-C")
    ap.add_argument("--open", action="store_true", help="abre el navegador al arrancar (implica --serve)")
    ap.add_argument("--refresh", type=float, default=0.0, metavar="MIN",
                    help="regenera la instantánea cada MIN minutos (0 = no; admite decimales)")
    ap.add_argument("--port", type=int, default=8099)
    ap.add_argument("--json", action="store_true", help="imprime la instantánea por stdout")
    a = ap.parse_args()

    if a.json:
        s = snapshot()
        print(json.dumps({"snap": s, "huecos": huecos(s), "kpis": kpis(s)}, ensure_ascii=False, indent=1))
        return 0

    if a.open:
        a.serve = True
    if a.refresh and not a.serve:
        print("panel: --refresh solo tiene sentido con --serve (o --open). Genero una vez y salgo.")

    refresh = a.refresh if a.serve else 0.0
    s, _, hs, _ = generar(refresh)
    print(f"panel: {OUT_DIR/'index.html'}")
    print(f"instantánea: {s['ts']} · nodos {s['resumen']['nodos']} · huecos {s['resumen']['huecos']} "
          f"(P0 {s['resumen']['p0']} / P1 {s['resumen']['p1']} / P2 {s['resumen']['p2']})")
    for h in hs:
        if h["p"] == "P0":
            print(f"  P0 · {h['t']}")

    if not a.serve:
        return 0

    os.chdir(OUT_DIR)
    socketserver.TCPServer.allow_reuse_address = True
    try:
        httpd = socketserver.TCPServer(("127.0.0.1", a.port), Handler)
    except OSError as e:
        print(f"panel: no puedo usar el puerto {a.port} ({e.strerror or e}).")
        print(f"       ¿ya hay un panel corriendo? prueba a abrir http://localhost:{a.port}/")
        return 2

    parar = threading.Event()
    if refresh > 0:
        threading.Thread(target=hilo_refresco, args=(refresh, parar), daemon=True).start()

    url = f"http://localhost:{a.port}/"
    with httpd:
        print(f"sirviendo {url}  (Ctrl-C para parar — no toca ningún servicio)")
        if refresh > 0:
            print(f"autorefresco: la instantánea se regenera cada {'%g' % refresh} min y la pestaña se recarga sola")
        if a.open:
            abrir_navegador(url)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nparado")
        finally:
            parar.set()
    return 0


if __name__ == "__main__":
    sys.exit(main())
