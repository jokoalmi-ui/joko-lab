#!/usr/bin/env python3
"""F2.3 - regimen ACTUAL del ledger: caché de prompt por semana, por dia (14 dias),
y p50/p90 sobre el regimen actual. Solo lectura."""
import json, statistics, collections, datetime

LEDGER = "/home/jokoalmi/joko-lab/04-operations/metrics/pipeline_obs.jsonl"
UMBRAL = 1000
rows = []
with open(LEDGER) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue
        pt = r.get("prompt_tokens")
        if r.get("path") != "/v1/chat/completions" or not isinstance(pt, int) or pt < UMBRAL:
            continue
        try:
            d = datetime.datetime.fromisoformat(str(r["timestamp"]).replace("Z", "+00:00"))
        except Exception:
            continue
        rows.append((d, pt, r.get("prompt_cache_hit_tokens"), r.get("prompt_cache_miss_tokens")))

print(f"filas utiles (chat/completions, >= {UMBRAL} tok): {len(rows)}")
print(f"rango: {min(r[0] for r in rows).date()} -> {max(r[0] for r in rows).date()}")

por, sem = collections.defaultdict(list), collections.defaultdict(list)
for d, pt, hit, miss in rows:
    por[d.date()].append((pt, hit, miss))
    sem[d.isocalendar()[:2]].append((pt, hit, miss))

print("\n=== por semana: tamano + cache de prompt ===")
print(f"{'semana':10s} {'n':>6s} {'p50':>8s} {'p90':>8s} | {'filas cache':>11s} {'hit%':>6s}")
for w in sorted(sem):
    v = [x[0] for x in sem[w]]
    c = [(h, m) for _, h, m in sem[w] if isinstance(h, int) and isinstance(m, int) and (h + m) > 0]
    hit = sum(h for h, _ in c) / sum(h + m for h, m in c) * 100 if c else float("nan")
    print(f"{str(w):10s} {len(v):6d} {statistics.median(v):8.0f} {sorted(v)[int(len(v)*0.9)-1]:8d} | "
          f"{len(c):11d} {hit:5.1f}%")

print("\n=== ultimos 14 dias ===")
print(f"{'fecha':12s} {'n':>5s} {'p50':>8s} {'p90':>8s} {'max':>8s} {'mayor%':>7s}")
for d in sorted(por)[-14:]:
    v = sorted(x[0] for x in por[d])
    print(f"{str(d):12s} {len(v):5d} {statistics.median(v):8.0f} {v[int(len(v)*0.9)-1]:8d} {v[-1]:8d} "
          f"{100*sum(1 for y in v if y > 200000)/len(v):6.1f}%")

ult = [r for r in rows if r[0].date() >= max(x[0].date() for x in rows) - datetime.timedelta(days=6)]
v = sorted(r[1] for r in ult)
n = len(v)
print(f"\n=== regimen actual (ultimos 7 dias, n={n}) ===")
print(f"min {v[0]} | p25 {v[int(n*0.25)]} | p50 {statistics.median(v):.0f} | p75 {v[int(n*0.75)]} | "
      f"p90 {v[int(n*0.9)]} | max {v[-1]} | media {statistics.mean(v):.0f}")
print(f"% >131k: {100*sum(1 for y in v if y>131072)/n:.1f}% | % >200k: {100*sum(1 for y in v if y>200000)/n:.1f}%")
print(f"fijo F1 (23.292 tok) sobre p50 actual = {23292/statistics.median(v)*100:.1f}% | "
      f"dinamico = {100-23292/statistics.median(v)*100:.1f}%")
