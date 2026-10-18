#!/usr/bin/env python3
"""F1.5 — Volcado del prompt FIJO real (via instrumento nativo de Hermes) + medicion en tokens.

NO toca el sistema: construye un agente de inspeccion offline (misma ruta que
`hermes prompt-size`: credenciales dummy, sin llamada al proveedor) y mide el
texto resultante con el tokenizador local (LM Studio 127.0.0.1:1234, max_tokens=1).

Salida: /tmp/f1-contexto/fijo/*.txt + tabla en stdout + fijo_real.json
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, "/home/jokoalmi/.hermes/hermes-agent")
os.environ.setdefault("HERMES_HOME", "/home/jokoalmi/.hermes")

OUT = Path("/tmp/f1-contexto/fijo")
OUT.mkdir(parents=True, exist_ok=True)
LMSTUDIO = "http://127.0.0.1:1234/v1"
RE_SKILLS = None


def bytes_(s: str) -> int:
    return len(s.encode("utf-8"))


def modelo_local() -> str:
    import urllib.request
    with urllib.request.urlopen(f"{LMSTUDIO}/models", timeout=30) as r:
        d = json.load(r)
    ids = [m.get("id") for m in d.get("data", [])]
    if not ids:
        raise SystemExit("no hay modelo cargado en LM Studio -> NO se recarga sin OK")
    return ids[0]


def ntok(texto: str, modelo: str) -> int | None:
    """Tokens del prompt segun el tokenizador real del endpoint."""
    import urllib.request
    body = json.dumps({
        "model": modelo,
        "messages": [{"role": "user", "content": texto}],
        "max_tokens": 1,
    }).encode()
    req = urllib.request.Request(f"{LMSTUDIO}/chat/completions", data=body,
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            u = json.load(r)["usage"]
        return u["prompt_tokens"]
    except Exception as e:  # noqa: BLE001
        print(f"  [WARN] fallo al tokenizar ({bytes_(texto)} B): {e}")
        return None


def main() -> int:
    import re
    from agent.system_prompt import build_system_prompt, build_system_prompt_parts
    from hermes_cli.prompt_size import _build_inspection_agent

    plataforma = sys.argv[1] if len(sys.argv) > 1 else "telegram"
    modelo = modelo_local()
    print(f"modelo local: {modelo}  |  plataforma: {plataforma}")

    agent = _build_inspection_agent(plataforma)
    partes = build_system_prompt_parts(agent)
    full = build_system_prompt(agent)
    stable, ctx, volatile = (partes.get(k, "") for k in ("stable", "context", "volatile"))

    m = re.search(r"<available_skills>.*?</available_skills>", volatile, re.DOTALL) \
        or re.search(r"<available_skills>.*?</available_skills>", stable, re.DOTALL)
    skills = m.group(0) if m else ""

    store = getattr(agent, "_memory_store", None)
    mem = usr = ""
    if store is not None:
        try:
            if getattr(agent, "_memory_enabled", True):
                mem = store.format_for_system_prompt("memory") or ""
            if getattr(agent, "_user_profile_enabled", True):
                usr = store.format_for_system_prompt("user") or ""
        except Exception:  # noqa: BLE001
            pass

    tools = getattr(agent, "tools", None) or []
    tools_json = json.dumps(tools, ensure_ascii=False)

    piezas = [
        ("system_prompt (completo)", full),
        ("  tier stable", stable),
        ("  tier volatile", volatile),
        ("  tier context", ctx),
        ("  skills_index", skills),
        ("  memoria", mem),
        ("  user_profile", usr),
        ("tools_json (esquemas)", tools_json),
    ]

    # Guardar textos para auditoria
    (OUT / "system_prompt.txt").write_text(full, encoding="utf-8")
    (OUT / "skills_index.txt").write_text(skills, encoding="utf-8")
    (OUT / "tools.json").write_text(tools_json, encoding="utf-8")

    filas = []
    for nombre, texto in piezas:
        t = ntok(texto, modelo)
        filas.append({"pieza": nombre, "chars": len(texto), "bytes": bytes_(texto), "tokens": t})
        print(f"  {nombre:28s} {len(texto):7,} chars {bytes_(texto):8,} B  ->  {t if t is not None else '?'} tok")

    tot_tok = sum(f["tokens"] for f in filas if f["tokens"] is not None)
    sp_tok = filas[0]["tokens"] or 0
    tools_tok = filas[-1]["tokens"] or 0
    print(f"\n  FIJO TOTAL (system_prompt + tools) = {sp_tok + tools_tok:,} tok"
          f"  [system {sp_tok:,} + tools {tools_tok:,}]")
    print(f"  suma de piezas medidas = {tot_tok:,} tok (incluye dobles conteos de tiers)")

    res = {
        "modelo_tokenizador": modelo,
        "plataforma": plataforma,
        "filas": filas,
        "fijo_total_tokens": sp_tok + tools_tok,
        "system_tokens": sp_tok,
        "tools_tokens": tools_tok,
        "tools_count": len(tools),
        "nota": ("tokens medidos con el tokenizador local; el texto se envia como mensaje de "
                 "usuario, por lo que incluye un offset de framing no restado (F1.1 lo fijo en 71 tok "
                 "para un system prompt de prueba)"),
    }
    (OUT.parent / "fijo_real.json").write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n  escrito: {OUT}/ y fijo_real.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
