#!/usr/bin/env python3
"""F1 / Fase F1.2 — MEDICIÓN por bloques del contexto fijo (perfil default).

Requiere: F1.0 ejecutada (piezas.json) y F1.1 VALIDADA.
Mide cada bloque aislado (diferencia contra el offset/suelo) y ACUMULADO, para detectar
no-linealidad. Los bloques que no quepan en el contexto se marcan no_medido_por_contexto
(cero imputacion: nunca se rellena con 0 ni con una estimacion).

NO toca config ni ficheros de ~/.hermes. NO publica. NO decide la poda.

Uso:  python3 medir_bloques.py [--base URL] [--modelo ID] [--con-mcp]
"""
import json
import os
import subprocess
import sys
import urllib.request

BASE_DEF = "http://127.0.0.1:1234/v1"
TIMEOUT = 300
PIEZAS = "/tmp/f1-contexto/piezas.json"
SAL_JSON = "/tmp/f1-contexto/mediciones.json"
SAL_MD = "/tmp/f1-contexto/RESULTADOS.md"
ORDEN = ["B1_soul", "B2_memorias", "B3_skills", "B5_mcp"]


def pide(base, payload):
    req = urllib.request.Request(
        base + "/chat/completions", data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": "Bearer lm-studio"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.loads(r.read().decode("utf-8", "replace"))


def tokens(base, modelo, texto):
    d = pide(base, {"model": modelo, "temperature": 0, "max_tokens": 1,
                    "messages": [{"role": "system", "content": texto}]})
    pt = (d.get("usage") or {}).get("prompt_tokens")
    if pt is None:
        raise RuntimeError("respuesta sin usage.prompt_tokens")
    return int(pt)


def modelo(base, pedido=None):
    with urllib.request.urlopen(base + "/models", timeout=30) as r:
        ids = [m["id"] for m in json.loads(r.read().decode("utf-8", "replace")).get("data", [])]
    if not ids:
        raise SystemExit("ERROR: /models vacio")
    if pedido and pedido not in ids:
        raise SystemExit(f"ERROR: {pedido!r} no esta en /models: {ids}")
    return pedido or ids[0]


def bloques_mcp(config):
    """Nombres de los MCP habilitados, leidos de mcp_servers en config.yaml (sin YAML lib)."""
    dentro = False
    nombres = []
    for ln in (config or "").splitlines():
        if ln.startswith("mcp_servers:"):
            dentro = True
            continue
        if dentro:
            if ln and not ln[0].isspace():
                break
            if ln.startswith("  ") and not ln.startswith("    ") and ln.strip().endswith(":"):
                nombres.append(ln.strip()[:-1])
    return nombres


def main():
    argv = sys.argv[1:]
    base, pedido, con_mcp = BASE_DEF, None, "--con-mcp" in argv
    for i, a in enumerate(argv):
        if a == "--base" and i + 1 < len(argv):
            base = argv[i + 1]
        if a == "--modelo" and i + 1 < len(argv):
            pedido = argv[i + 1]
    base = base.rstrip("/")

    if not os.path.exists(PIEZAS):
        raise SystemExit(f"ERROR: falta {PIEZAS}. Ejecuta antes recolectar.py (F1.0).")
    with open(PIEZAS, "r", encoding="utf-8") as f:
        pz = json.load(f)

    mdl = modelo(base, pedido)
    print(f"endpoint {base} · modelo {mdl}")

    texto = {
        "B1_soul": pz.get("B1_soul"),
        "B2_memorias": None,
        "B3_skills": pz.get("B3_skills"),
    }
    if pz.get("B2_memoria") is not None and pz.get("B2_user") is not None:
        texto["B2_memorias"] = (pz["B2_memoria"].rstrip() + "\n" + pz["B2_user"].rstrip())

    # --- MCP (FASE SEPARADA: crea procesos; requiere --con-mcp explicito) ------
    mcp_info = {"medido": False, "motivo": "fase F1.4 no solicitada (--con-mcp)"}
    if con_mcp:
        json_mcp, avisos = mcp_tools_list(pz.get("config_yaml") or "")
        texto["B5_mcp"] = json_mcp
        mcp_info = {"medido": True, "avisos": avisos}

    # --- offset / suelo --------------------------------------------------------
    offset = tokens(base, mdl, "x")
    print(f"offset (suelo 1 char): {offset} tok")

    res = {"base": base, "modelo": mdl, "offset_tokens": offset, "bloques": {},
           "mcp": mcp_info, "no_medido_por_contexto": []}

    # --- medición individual ---------------------------------------------------
    for b in ORDEN:
        t = texto.get(b)
        if not t:
            res["bloques"][b] = {"estado": "no_calculable",
                                 "nota": "pieza ausente en piezas.json (cero imputacion)"}
            print(f"{b:12s} NO CALCULABLE (pieza ausente)")
            continue
        try:
            total = tokens(base, mdl, t)
        except Exception as e:  # noqa: BLE001 - se reporta el error literal, no se concluye
            res["bloques"][b] = {"estado": "error", "error": str(e)[:200],
                                 "chars": len(t)}
            res["no_medido_por_contexto"].append(b)
            print(f"{b:12s} ERROR: {str(e)[:120]}")
            continue
        res["bloques"][b] = {"estado": "medido", "chars": len(t),
                             "tokens_con_offset": total, "tokens_neto": total - offset,
                             "ratio_chars_por_token": round(len(t) / max(1, total - offset), 2)}
        print(f"{b:12s} {total:7d} tok totales · {total - offset:7d} netos · {len(t)} chars")

    # --- medición ACUMULADA (detecta no-linealidad) ----------------------------
    acum = []
    suma_texto = ""
    for b in ORDEN:
        if res["bloques"].get(b, {}).get("estado") != "medido":
            continue
        suma_texto = (suma_texto + "\n\n" + texto[b]) if suma_texto else texto[b]
        try:
            t_ac = tokens(base, mdl, suma_texto)
            acum.append({"hasta": b, "chars_acum": len(suma_texto),
                         "tokens_acum": t_ac, "tokens_neto_acum": t_ac - offset})
            print(f"acumulado hasta {b:12s}: {t_ac - offset:7d} tok netos")
        except Exception as e:  # noqa: BLE001
            acum.append({"hasta": b, "estado": "no_medido_por_contexto",
                         "chars_acum": len(suma_texto), "error": str(e)[:160]})
            res["no_medido_por_contexto"].append(f"acum:{b}")
            print(f"acumulado hasta {b:12s}: NO MEDIDO ({str(e)[:80]})")
    res["acumulado"] = acum

    # --- cierre -----------------------------------------------------------------
    medidos = {k: v["tokens_neto"] for k, v in res["bloques"].items()
               if v.get("estado") == "medido"}
    total_fijo = sum(medidos.values())
    res["total_fijo_tokens_netos"] = total_fijo
    res["fraccion_por_bloque"] = {k: round(v / max(1, total_fijo), 4) for k, v in medidos.items()}
    res["_meta"] = {"piezas_fecha": (pz.get("_meta") or {}).get("fecha"),
                    "instrumento": "usage.prompt_tokens de LM Studio (tokenizador del modelo local)",
                    "etiqueta": "orden de magnitud para el pipeline cloud; fraccion por bloque valida"}

    with open(SAL_JSON, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    escribe_md(res, pz)
    print(f"\ntotal contexto fijo medido: {total_fijo} tok netos")
    for k, v in sorted(medidos.items(), key=lambda x: -x[1]):
        print(f"  {k:12s} {v:7d} tok  {res['fraccion_por_bloque'][k]:6.1%}")
    print(f"escrito: {SAL_JSON} y {SAL_MD}")
    print("LAS CIFRAS SON ORDEN DE MAGNITUD hasta leer la validacion de F1.1.")
    return 0


def mcp_tools_list(config):
    """F1.4: pide tools/list a cada MCP via JSON-RPC stdio y CIERRA el proceso.
    Solo una peticion de lectura por servidor; timeout duro. No escribe nada suyo."""
    nombres = bloques_mcp(config)
    resultados, avisos = {}, {}
    # comandos reales leidos del bloque mcp_servers de config.yaml
    cmds = {}
    actual = None
    dentro = False
    for ln in (config or "").splitlines():
        if ln.startswith("mcp_servers:"):
            dentro = True
            continue
        if dentro:
            if ln and not ln[0].isspace():
                break
            if ln.startswith("  ") and not ln.startswith("    "):
                actual = ln.strip().rstrip(":")
                cmds[actual] = {"cmd": None, "args": []}
            elif actual and "command:" in ln:
                cmds[actual]["cmd"] = ln.split("command:", 1)[1].strip()
            elif actual and ln.strip().startswith("- "):
                cmds[actual]["args"].append(ln.strip()[2:].strip())
    for n in nombres:
        c = cmds.get(n) or {}
        if not c.get("cmd"):
            avisos[n] = "no_calculable: sin command en config.yaml"
            continue
        peticion = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/list",
                               "params": {}}) + "\n"
        try:
            p = subprocess.run([c["cmd"], *c["args"]], input=peticion, capture_output=True,
                               text=True, timeout=45)
            linea = next((l for l in p.stdout.splitlines() if '"result"' in l), None)
            if not linea:
                avisos[n] = f"no_calculable: sin result (stderr: {p.stderr[:120]!r})"
                continue
            res = json.loads(linea)["result"]
            resultados[n] = json.dumps(res, ensure_ascii=False)
            avisos[n] = f"ok: {len(res.get('tools', []))} herramientas"
        except Exception as e:  # noqa: BLE001
            avisos[n] = f"no_calculable: {str(e)[:140]}"
    return ("\n".join(f"# MCP {k}\n{v}" for k, v in resultados.items()) if resultados else None), avisos


def escribe_md(res, pz):
    L = []
    L.append("# F1 — Coste en tokens del contexto fijo (perfil default)\n")
    L.append(f"- Instrumento: `{res['_meta']['instrumento']}`")
    L.append(f"- Modelo: `{res['modelo']}` · endpoint `{res['base']}`")
    L.append(f"- Piezas recolectadas: {res['_meta']['piezas_fecha']} · offset/suelo: {res['offset_tokens']} tok")
    L.append(f"- Etiqueta de validez: **{res['_meta']['etiqueta']}**")
    L.append(f"- **Total contexto fijo medido: {res.get('total_fijo_tokens_netos', 'no_calculable')} tok netos**\n")
    L.append("## Por bloque\n")
    L.append("| bloque | chars | tokens netos | % del fijo | chars/token |")
    L.append("|---|---|---|---|---|")
    for b in ORDEN:
        d = res["bloques"].get(b, {})
        if d.get("estado") == "medido":
            L.append(f"| {b} | {d['chars']} | {d['tokens_neto']} | "
                     f"{res['fraccion_por_bloque'].get(b, 0):.1%} | {d['ratio_chars_por_token']} |")
        else:
            L.append(f"| {b} | {d.get('chars', 'no_calculable')} | {d.get('estado')} | — | — |")
    L.append("\n## Acumulado (no-linealidad)\n")
    L.append("| hasta | chars acum | tokens netos acum |")
    L.append("|---|---|---|")
    for a in res.get("acumulado", []):
        L.append(f"| {a['hasta']} | {a['chars_acum']} | {a.get('tokens_neto_acum', a.get('estado'))} |")
    if res.get("no_medido_por_contexto"):
        L.append("\n## no_medido_por_contexto (cero imputacion)\n")
        L.append(", ".join(str(x) for x in res["no_medido_por_contexto"]))
    L.append("\n## MCP (F1.4)\n")
    L.append(f"- {res.get('mcp')}")
    L.append("\n> Sin recomendacion de poda: el umbral se fija DESPUES del baseline (RULE-015).\n")
    with open(SAL_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(L))


if __name__ == "__main__":
    sys.exit(main())
