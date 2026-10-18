#!/usr/bin/env python3
"""proposer.py — L2 F3: genera PROPUESTAS candidatas desde la telemetria del lab.

Solo lectura de fuentes + escritura de propuestas en 04-operations/proposals/.
El humano decide SIEMPRE (JL-012): una propuesta es una SUGERENCIA, no un cambio.

Fuentes:
- knowledge_health.audit(): KOs con issues (sin evidencia, nunca validada,
  sin expiracion, confianza baja).
- activation-ledger.jsonl: RULEs activadas (las nunca activadas son candidatas).
- decision-ledger.jsonl: metricas de uso por politica.

Uso:
    python3 proposer.py            # genera propuestas nuevas (con dedupe)
    python3 proposer.py --dry      # muestra las propuestas sin escribir
"""
import sys, json, re
from pathlib import Path
from datetime import datetime

LAB = Path.home() / "joko-lab"
PROPOSALS_DIR = LAB / "04-operations" / "proposals"
ACTIVATION = Path("/mnt/ssd_ia_datos/lab-state/activation-ledger.jsonl")

sys.path.insert(0, str(LAB / "tools"))


def leer_issues_knowledge():
    """Issues del health auditor (KOs con problemas de evidencia/vigencia)."""
    try:
        from knowledge_health import audit
        res = audit()
        return res.get("issues", [])
    except Exception as e:
        print(f"  (knowledge_health no disponible: {e})", file=sys.stderr)
        return []


def leer_rules_activas():
    """RULEs con al menos una activacion registrada (activation-ledger).
    El ledger usa los campos model_selection, blocks, active_rules y policies
    (fix 05-ago: antes se leian rule/id/ko, que no existen -> falso positivo)."""
    activas = set()
    if ACTIVATION.exists():
        for line in ACTIVATION.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                e = json.loads(line)
            except Exception:
                continue
            for campo in ("model_selection", "blocks", "active_rules", "policies"):
                v = e.get(campo)
                if isinstance(v, str) and v:
                    activas.add(v.upper())
                elif isinstance(v, list):
                    for item in v:
                        if item:
                            activas.add(str(item).upper())
    return activas


def reglas_conocidas():
    """Ids de RULE del knowledge_health (para detectar nunca activadas)."""
    try:
        from knowledge_health import find_knowledge_files, parse_frontmatter, classify_file
        rules = []
        for f in find_knowledge_files():
            if classify_file(f, parse_frontmatter(f)) == "RULE":
                rules.append(f.stem.upper())
        return set(rules)
    except Exception:
        return set()


def generar_propuestas():
    """Construye lista de propuestas candidatas (dicts)."""
    props = []

    # 1. Issues del health auditor
    for issue in leer_issues_knowledge():
        m = re.match(r"\[([A-Z]+)\]\s+([\w.-]+):\s*(.*)", issue)
        if not m:
            continue
        ktype, kid, problema = m.group(1), m.group(2), m.group(3)
        accion = {
            "sin evidencia que la respalde": "recopilar evidencia (EXP/review/falsacion) o marcar como candidata a retirar",
            "nunca validada": "programar validacion y fijar last_validated",
            "sin fecha de expiraci": "fijar expires/next_review",
            "confianza baja": "revisar confianza: subirla con evidencia o bajarla a hipotesis",
        }
        acc = next((v for k, v in accion.items() if k in problema), "revisar")
        props.append({
            "tipo": "conocimiento",
            "target": kid,  # kid ya incluye el prefijo (RULE-006, POLICY-001...)
            "problema": problema,
            "accion": acc,
            "fuente": "knowledge_health",
        })

    # 2. RULEs nunca activadas
    activas = leer_rules_activas()
    conocidas = reglas_conocidas()
    for r in sorted(conocidas - activas):
        props.append({
            "tipo": "activacion",
            "target": r,
            "problema": "RULE nunca activada en activation-ledger",
            "accion": "revisar si sigue vigente o si falta su punto de activacion (no eliminar sin evidencia)",
            "fuente": "activation-ledger",
        })

    return props


def ya_propuesto(target, problema):
    """Dedupe: si ya existe una propuesta abierta para ese target+problema."""
    if not PROPOSALS_DIR.exists():
        return False
    for f in PROPOSALS_DIR.glob("PROP-*.yaml"):
        try:
            txt = f.read_text(encoding="utf-8", errors="replace")
            if f'id: "{target}"' in txt and problema[:40] in txt:
                return True
        except Exception:
            continue
    return False


def _parsear_propuesta(txt: str) -> dict:
    """Extrae estado, target y problema del YAML de una propuesta."""
    estado = "?"
    target = "?"
    problema = ""
    for line in txt.splitlines():
        if line.startswith("estado:"):
            estado = line.split(":", 1)[1].strip()
        elif line.startswith('id: "'):
            target = line.split('"')[1]
        elif line.startswith("problema:"):
            problema = line.split(":", 1)[1].strip()[:60]
    return {"estado": estado, "target": target, "problema": problema}


def _imprimir_lista(titulo: str, items: list, mostrar_uso: bool = False):
    """Imprime un grupo de propuestas con su título."""
    print(f"{titulo} ({len(items)}):")
    for p in items:
        print("  " + p)
    if mostrar_uso and items:
        print("\nUsa: proposer.py approve <PROP-id> [nota] | reject <PROP-id> [nota]")


def cmd_list():
    """Lista propuestas pendientes de decision (gate F4: el humano decide, JL-012)."""
    if not PROPOSALS_DIR.exists():
        print("(sin propuestas)")
        return 0
    pendientes = []
    decididas = []
    for f in sorted(PROPOSALS_DIR.glob("PROP-*.yaml")):
        txt = f.read_text(encoding="utf-8", errors="replace")
        info = _parsear_propuesta(txt)
        item = f"{f.name} | {info['target']} | {info['problema']} | {info['estado']}"
        if info["estado"] == "propuesta":
            pendientes.append(item)
        else:
            decididas.append(item)
    _imprimir_lista("PENDIENTES DE DECISION", pendientes)
    # Nota: el contador usa el total de decididas, pero solo se imprimen las últimas 5
    if decididas:
        print(f"\nDECIDIDAS ({len(decididas)}):")
        for p in decididas[-5:]:
            print("  " + p)
    if pendientes:
        print("\nUsa: proposer.py approve <PROP-id> [nota] | reject <PROP-id> [nota]")
    return 0


def cmd_set_estado(accion, prop_id, nota):
    """Gate F4: el humano aprueba o descarta una propuesta (recibo con trazabilidad)."""
    if not PROPOSALS_DIR.exists():
        print("ERROR: sin directorio de propuestas")
        return 2
    encontrado = None
    for f in PROPOSALS_DIR.glob("PROP-*.yaml"):
        txt = f.read_text(encoding="utf-8", errors="replace")
        if f'id: "{prop_id}"' in txt or f"id: {prop_id}" in txt:
            encontrado = f
            break
    if not encontrado:
        print(f"ERROR: propuesta {prop_id} no encontrada (usa: proposer.py list)")
        return 2
    nuevo_estado = "aprobada" if accion == "approve" else "descartada"
    txt = encontrado.read_text(encoding="utf-8")
    txt = txt.replace("estado: propuesta", f"estado: {nuevo_estado}")
    txt = txt.replace("decision: pendiente", f"decision: {nota or 'sin nota'}")
    if "decision_fecha:" not in txt:
        txt += f"decision_fecha: {datetime.now().isoformat(timespec='seconds')}\n"
    encontrado.write_text(txt, encoding="utf-8")
    print(f"OK: {prop_id} -> {nuevo_estado} ({nota or 'sin nota'})")
    return 0


def _construir_contenido(p: dict, hoy: str, i: int) -> str:
    """Construye el YAML de una propuesta PROP."""
    return (
        "id: PROP-{hoy}-{i:03d}\n"
        "fecha: {fecha}\n"
        "tipo: {tipo}\n"
        'id: "{target}"\n'
        "problema: {problema}\n"
        "accion_sugerida: {accion}\n"
        "fuente: {fuente}\n"
        "estado: propuesta\n"
        "decision: pendiente\n"
    ).format(hoy=hoy, i=i, fecha=datetime.now().isoformat(timespec="seconds"),
             tipo=p["tipo"], target=p["target"], problema=p["problema"],
             accion=p["accion"], fuente=p["fuente"])


def _dispatch_comandos(args) -> int | None:
    """Maneja comandos CLI (list/approve/reject). Devuelve código o None si
    no es un comando (continuar con la generación)."""
    if args and args[0] == "list":
        return cmd_list()
    if args and args[0] in ("approve", "reject"):
        if len(args) < 2:
            print(f"Uso: proposer.py {args[0]} <PROP-id> [nota]")
            return 2
        return cmd_set_estado(args[0], args[1], " ".join(args[2:]))
    return None


def _escribir_propuestas(nuevas, hoy, dry) -> int:
    """Escribe (o imprime en dry) las propuestas. Devuelve cuántas escritas."""
    escritas = 0
    for i, p in enumerate(nuevas, 1):
        contenido = _construir_contenido(p, hoy, i)
        if dry:
            print("---\n" + contenido)
        else:
            out = PROPOSALS_DIR / f"PROP-{hoy}-{i:03d}.yaml"
            out.write_text(contenido, encoding="utf-8")
            print(f"Propuesta escrita: {out.name}")
            escritas += 1
    return escritas


def main():
    args = sys.argv[1:]
    codigo = _dispatch_comandos(args)
    if codigo is not None:
        return codigo
    dry = "--dry" in sys.argv
    PROPOSALS_DIR.mkdir(parents=True, exist_ok=True)

    props = generar_propuestas()
    if not props:
        print("No hay propuestas candidatas nuevas.")
        return 0

    nuevas = [p for p in props if not ya_propuesto(p["target"], p["problema"])]
    hoy = datetime.now().strftime("%Y%m%d")
    escritas = _escribir_propuestas(nuevas, hoy, dry)

    if not dry:
        print(f"\nTotal: {len(props)} candidatas, {escritas} nuevas escritas en {PROPOSALS_DIR}")
        print("El humano decide (JL-012): revisar las propuestas antes de actuar.")
    else:
        print(f"\n(dry) Total: {len(props)} candidatas, {len(nuevas)} nuevas.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
