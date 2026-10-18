#!/usr/bin/env python3
"""diag-lms.py — Que devuelve exactamente LM Studio por modelo (respuesta cruda)."""
import json, urllib.request, urllib.error, sys

API = "http://localhost:1234/api/v0/chat/completions"
MODELOS = ["lfm2.5-2.6b", "granite-4.1-8b", "qwen3.6-35b-a3b-mtp"]
PROMPT = "Di solo la palabra OK."

for m in MODELOS:
    body = json.dumps({"model": m, "temperature": 0, "max_tokens": 40,
                       "messages": [{"role": "user", "content": PROMPT}]}).encode()
    req = urllib.request.Request(API, data=body, headers={"Content-Type": "application/json"})
    print("=" * 70)
    print("MODELO:", m)
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            d = json.loads(r.read().decode())
        ch = d.get("choices", [{}])[0]
        msg = ch.get("message", {})
        print("  id:", d.get("model"))
        print("  finish_reason:", ch.get("finish_reason"))
        print("  content:", repr(msg.get("content"))[:300])
        print("  reasoning:", repr(msg.get("reasoning_content") or msg.get("reasoning"))[:200])
        print("  usage:", d.get("usage"))
    except urllib.error.HTTPError as e:
        print("  HTTP", e.code)
        print("  body:", e.read().decode()[:600])
    except Exception as e:
        print("  ERROR:", type(e).__name__, e)
    sys.stdout.flush()
