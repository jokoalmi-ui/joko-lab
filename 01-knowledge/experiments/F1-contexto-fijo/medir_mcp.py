#!/usr/bin/env python3
"""F1.4 — Coste REAL de los 3 MCP en el contexto fijo del perfil `default`.

Fuentes REALES (solo lectura, sin arrancar ningun servidor MCP):
  (a) cache/mcp_schema_cache.json  -> esquemas completos de los 25 tools MCP
  (b) sessions/request_dump_*.json -> request HTTP autentico del 2026-09-14 22:33
      - system prompt real (55.157 chars)
      - 20 tools reales (37.349 B)
      - tool_search con el catalogo deferred COMPLETO (2.697 chars, 25 lineas mcp__)

Del catalogo se separa lo atribuible a MCP:
  catalogo_real (2.697) - catalogo_base (454: cronjob/session_search/terminal/todo) = delta MCP

Medicion: tokenizador local LM Studio 127.0.0.1:1234 via usage.prompt_tokens (max_tokens=1).
NO escribe en ~/.hermes. Salida: mcp_real.json + stdout.
"""
from __future__ import annotations

import json
import urllib.request
from pathlib import Path

HERMES = Path("/home/jokoalmi/.hermes")
OUT = Path("/tmp/f1-contexto")
FIJO = OUT / "fijo"
LMSTUDIO = "http://127.0.0.1:1234/v1"
DUMP = HERMES / "sessions/request_dump_20260914_172635_d00cc0_20260914_223309_841438.json"


def modelo_local() -> str:
    with urllib.request.urlopen(f"{LMSTUDIO}/models", timeout=30) as r:
        ids = [m.get("id") for m in json.load(r).get("data", [])]
    if not ids:
        raise SystemExit("no hay modelo cargado en LM Studio -> NO se recarga sin OK")
    return ids[0]


def ntok(texto: str, modelo: str) -> int | None:
    body = json.dumps({
        "model": modelo,
        "messages": [{"role": "user", "content": texto}],
        "max_tokens": 1,
    }).encode()
    req = urllib.request.Request(f"{LMSTUDIO}/chat/completions", data=body,
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=900) as r:
            return json.load(r)["usage"]["prompt_tokens"]
    except Exception as e:  # noqa: BLE001
        print(f"  [WARN] fallo al tokenizar ({len(texto)} chars): {e}")
        return None


def mcp_a_openai(server: str, t: dict) -> dict:
    """Esquema MCP -> forma OpenAI function, como lo mandaria el runtime."""
    name = t.get("name") or t.get("function", {}).get("name", "")
    desc = t.get("description") or ""
    params = t.get("inputSchema") or t.get("parameters") or {"type": "object", "properties": {}}
    return {"type": "function",
            "function": {"name": f"mcp__{server.replace('-', '_')}__{name}",
                         "description": desc,
                         "parameters": params}}


def main() -> int:
    modelo = modelo_local()
    print(f"modelo tokenizador: {modelo}\n")

    # --- (a) esquemas MCP completos ---
    cache = json.loads((HERMES / "cache/mcp_schema_cache.json").read_text())
    completos: list[dict] = []
    por_server: dict[str, int] = {}
    for srv, blob in cache.items():
        defs = list(blob.get("tools") or []) + list(blob.get("utility_tools") or [])
        por_server[srv] = len(defs)
        completos += [mcp_a_openai(srv, d) for d in defs]
    mcp_json = json.dumps(completos, ensure_ascii=False)

    # --- (b) request real del 14-sep ---
    body = json.loads(DUMP.read_text())["request"]["body"]
    tools = body["tools"]
    sysm = next(m for m in body["messages"] if m.get("role") == "system")
    sys_txt = sysm["content"] if isinstance(sysm["content"], str) else json.dumps(sysm["content"], ensure_ascii=False)
    tools_txt = json.dumps(tools, ensure_ascii=False)

    # --- (c) catalogos (real con MCP vs base sin MCP) ---
    cat_real = (FIJO / "catalogo_real.txt").read_text()
    cat_base = (FIJO / "catalogo_base.txt").read_text()

    # Solo las lineas atribuibles a MCP: sus 25 bullets + las 3 cabeceras de grupo
    mcp_lines = "\n".join(l for l in cat_real.splitlines()
                          if l.startswith("- mcp__")
                          or l.startswith(("animation-server tools", "lab-db tools", "lancedb tools")))

    piezas = [
        ("catalogo_real (con 25 MCP)", cat_real),
        ("catalogo_base (sin MCP)", cat_base),
        ("solo lineas MCP (25+3 cabeceras)", mcp_lines),
        ("25 esquemas MCP completos", mcp_json),
        ("system prompt real 14-sep", sys_txt),
        ("20 tools reales 14-sep", tools_txt),
        ("FIJO real 14-sep (system+tools)", sys_txt + tools_txt),
    ]

    filas = []
    for nombre, texto in piezas:
        t = ntok(texto, modelo)
        filas.append({"pieza": nombre, "chars": len(texto), "bytes": len(texto.encode()), "tokens": t})
        print(f"  {nombre:34s} {len(texto):8,} chars  ->  {t if t is not None else '?':>7} tok")

    def tok(nombre: str) -> int:
        return next(f["tokens"] for f in filas if f["pieza"] == nombre) or 0

    tr, tb = tok("catalogo_real (con 25 MCP)"), tok("catalogo_base (sin MCP)")
    print(f"\n  COSTE MCP como catalogo  = {tr} - {tb} = {tr - tb} tok")
    print(f"  COSTE si NO estuvieran deferred = {tok('25 esquemas MCP completos')} tok (esquemas completos)")
    print(f"  FIJO real de esa sesion  = {tok('FIJO real 14-sep (system+tools)')} tok")
    print(f"  (sin MCP, medido hoy)    = 23.292 tok  ->  delta MCP sobre el fijo")

    res = {"modelo_tokenizador": modelo, "por_server": por_server,
           "mcp_tools_total": len(completos), "filas": filas,
           "catalogo_real_tokens": tr, "catalogo_base_tokens": tb,
           "coste_mcp_como_catalogo_tokens": tr - tb,
           "coste_mcp_completos_tokens": tok("25 esquemas MCP completos"),
           "fijo_real_14sep_tokens": tok("FIJO real 14-sep (system+tools)"),
           "fuente": str(DUMP), "nota": "medido con tokenizador local; framing ~67 tok por pieza"}
    (OUT / "mcp_real.json").write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
    (FIJO / "mcp_completos.json").write_text(mcp_json, encoding="utf-8")
    print(f"\n  escrito: {OUT}/mcp_real.json y fijo/mcp_completos.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
