#!/usr/bin/env python3
"""blackboard_orchestrator.py — Patron 4: Orchestrator + Workers + Blackboard

Fase 3 del orchestrator-design.md: Workers reales que leen/escriben
en un Blackboard compartido. El Orchestrator coordina sin trabajar.

Uso:
  echo "objetivo del usuario" | python3 blackboard_orchestrator.py
"""
import os, sys, json, subprocess, time
from pathlib import Path

TOOL_DIR = os.path.expanduser("~/joko-lab/tools")

# ═══════════════════════════════════════════════════
# BLACKBOARD — Memoria compartida entre workers
# ═══════════════════════════════════════════════════
class Blackboard:
    """Estado compartido. Workers solo leen/escriben su seccion."""
    def __init__(self, goal: str):
        self.data = {
            "goal": goal,
            "artifact_type": "desconocido",
            "complexity": "baja",
            "context": "",
            "knowledge": "",
            "model": "",
            "params": {},
            "confidence": 30,
            "prompt": "",
            "evaluation": {},
            "errors": [],
            "started_at": time.time()
        }
    
    def read(self, key: str) -> any:
        return self.data.get(key, "")
    
    def write(self, key: str, value: any):
        self.data[key] = value
    
    def snapshot(self) -> dict:
        return dict(self.data)

# ═══════════════════════════════════════════════════
# WORKERS — Una responsabilidad por worker
# ═══════════════════════════════════════════════════

class ContextWorker:
    """Busca en RAG el contexto relevante"""
    def run(self, bb: Blackboard) -> bool:
        goal = bb.read("goal")
        try:
            result = subprocess.run(
                [sys.executable, os.path.join(TOOL_DIR, "context_builder.py")],
                input=goal,
                capture_output=True, text=True, timeout=20
            )
            bb.write("context", result.stdout[:1500] if result.returncode == 0 else "")
            return True
        except Exception as e:
            bb.data["errors"].append(f"ContextWorker: {e}")
            return False

class KnowledgeWorker:
    """Sintetiza el contexto en conocimiento estructurado"""
    def run(self, bb: Blackboard) -> bool:
        ctx = bb.read("context")
        if not ctx:
            return True  # Sin contexto, no hay nada que sintetizar
        try:
            result = subprocess.run(
                [sys.executable, os.path.join(TOOL_DIR, "knowledge_resolver.py")],
                input=ctx,
                capture_output=True, text=True, timeout=15
            )
            bb.write("knowledge", result.stdout[:1000] if result.returncode == 0 else "")
            return True
        except Exception as e:
            bb.data["errors"].append(f"KnowledgeWorker: {e}")
            return False

class RouterWorker:
    """Recomienda modelo y parametros"""
    def run(self, bb: Blackboard) -> bool:
        goal = bb.read("goal")
        try:
            result = subprocess.run(
                [sys.executable, os.path.join(TOOL_DIR, "decision_router.py"), "--json"],
                input=goal,
                capture_output=True, text=True, timeout=15
            )
            if result.returncode == 0:
                try:
                    route = json.loads(result.stdout)
                    rec = route.get("recommendation") or route.get("fallback", {})
                    bb.write("model", rec.get("model", "granite-4.1-8b"))
                    bb.write("params", rec.get("params", {"max_tokens": 1024, "temperature": 0.3}))
                    bb.write("confidence", {"ALTA": 90, "MEDIA": 60, "BAJA": 30}.get(
                        route.get("confidence", "BAJA"), 30))
                except json.JSONDecodeError:
                    bb.write("model", "granite-4.1-8b")
            return True
        except Exception as e:
            bb.data["errors"].append(f"RouterWorker: {e}")
            return False

class ValidationWorker:
    """Verifica anti-patrones antes de ejecutar"""
    def run(self, bb: Blackboard) -> bool:
        try:
            result = subprocess.run(
                [sys.executable, os.path.join(TOOL_DIR, "preflight_checklist.py")],
                capture_output=True, text=True, timeout=5
            )
            bb.write("preflight", result.stdout[:300])
            return True
        except Exception as e:
            bb.data["errors"].append(f"ValidationWorker: {e}")
            return False

class EvidenceWorker:
    """Decide si registrar conocimiento nuevo"""
    def run(self, bb: Blackboard) -> bool:
        eval_data = bb.read("evaluation")
        if not eval_data:
            return True
        try:
            result = subprocess.run(
                [sys.executable, os.path.join(TOOL_DIR, "evidence_collector.py")],
                input=json.dumps(eval_data),
                capture_output=True, text=True, timeout=5
            )
            bb.write("evidence", result.stdout[:500])
            return True
        except Exception:
            return True  # No critico

# ═══════════════════════════════════════════════════
# ORCHESTRATOR — Coordina, no trabaja
# ═══════════════════════════════════════════════════

WORKERS = {
    "context":       ContextWorker(),
    "knowledge":     KnowledgeWorker(),
    "router":        RouterWorker(),
    "validation":    ValidationWorker(),
    "evidence":      EvidenceWorker(),
}

def run_pipeline(goal: str, plan: list = None) -> dict:
    """Ejecuta workers en orden segun el plan"""
    bb = Blackboard(goal)
    
    if plan is None:
        plan = ["context", "knowledge", "router", "validation", "evidence"]
    
    results = []
    for step_name in plan:
        worker = WORKERS.get(step_name)
        if not worker:
            bb.data["errors"].append(f"Worker desconocido: {step_name}")
            continue
        
        success = worker.run(bb)
        results.append({
            "worker": step_name,
            "success": success,
            "duration_ms": int((time.time() - bb.data["started_at"]) * 1000)
        })
    
    bb.write("elapsed_ms", int((time.time() - bb.data["started_at"]) * 1000))
    bb.data["plan"] = plan
    bb.data["results"] = results
    
    return bb.snapshot()

def format_report(bb: dict) -> str:
    lines = []
    lines.append("══ ORCHESTRATOR + BLACKBOARD ══")
    lines.append(f"  Objetivo: {bb['goal'][:80]}")
    lines.append(f"  Tiempo: {bb.get('elapsed_ms', 0)}ms")
    lines.append(f"  Modelo: {bb.get('model', 'no seleccionado')}")
    lines.append(f"  Confianza: {bb.get('confidence', 0)}%")
    lines.append("")
    lines.append("  Workers ejecutados:")
    
    for r in bb.get("results", []):
        icon = "✅" if r["success"] else "❌"
        lines.append(f"    {icon} {r['worker']}")
    
    if bb.get("errors"):
        lines.append("")
        lines.append("  Errores:")
        for e in bb["errors"][:3]:
            lines.append(f"    ⚠ {e[:100]}")
    
    lines.append("═══════════════════════════════")
    return "\n".join(lines)

if __name__ == "__main__":
    if not sys.stdin.isatty():
        goal = sys.stdin.read().strip()
    elif len(sys.argv) > 1:
        goal = " ".join(sys.argv[1:])
    else:
        print("Uso: echo 'objetivo' | python3 blackboard_orchestrator.py")
        sys.exit(1)
    
    result = run_pipeline(goal)
    print(format_report(result))
