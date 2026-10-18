#!/usr/bin/env python3
"""Genera reporte HTML visual desde los JSON del Critic Loop."""
import json
from pathlib import Path
from datetime import datetime

OUTPUTS = Path(__file__).parent / "outputs"

def load_evaluations():
    files = sorted(OUTPUTS.glob("*.json"))
    evals = []
    for f in files:
        with open(f) as fh:
            evals.append(json.load(fh))
    evals.sort(key=lambda e: e["meta"]["timestamp"])
    return evals

def score_bar(score, confidence, uncertainty):
    bar_color = "#4ade80" if score >= 8 else "#facc15" if score >= 6 else "#f87171"
    return f"""
    <div style='margin:6px 0'>
        <div style='display:flex;justify-content:space-between;font-size:13px'>
            <span>{score}/10</span>
            <span style='color:#6c7086;font-size:11px'>conf {confidence:.0%} · {uncertainty}</span>
        </div>
        <div style='background:#1e1e2e;border-radius:3px;height:5px;margin-top:3px'>
            <div style='background:{bar_color};height:5px;border-radius:3px;width:{score*10}%'></div>
        </div>
    </div>"""

def build_comparison_table(evals):
    if len(evals) < 2:
        return ""
    
    e1, e2 = evals[0], evals[1]
    p1 = {ev["principle"]: ev for ev in e1["evaluations"]}
    p2 = {ev["principle"]: ev for ev in e2["evaluations"]}
    
    principles = list(p1.keys())
    rows = ""
    for p in principles:
        s1 = p1[p]["score"]
        s2 = p2[p]["score"]
        delta = s2 - s1
        cls = "delta-plus" if delta > 0 else "delta-minus" if delta < 0 else "delta-zero"
        sign = f"+{delta}" if delta > 0 else str(delta)
        rows += f"<tr><td>{p}</td><td>{s1}</td><td>{s2}</td><td class='{cls}'>{sign}</td></tr>"
    
    tag1 = e1["meta"].get("tag", "v1")
    tag2 = e2["meta"].get("tag", "v2")
    
    return f"""
    <h3>Comparación: {tag1} → {tag2}</h3>
    <table>
        <tr><th>Principio</th><th>{tag1}</th><th>{tag2}</th><th>Δ</th></tr>
        {rows}
    </table>
    <div style='margin-top:8px;color:#6c7086;font-size:11px'>
        Media: {e1['aggregates']['mean_score']} → {e2['aggregates']['mean_score']} 
        (Δ {e2['aggregates']['mean_score'] - e1['aggregates']['mean_score']:+.1f})
    </div>
    """

def generate():
    evals = load_evaluations()
    if not evals:
        print("No hay evaluaciones en outputs/")
        return
    
    cards = ""
    for e in evals:
        tag = e["meta"].get("tag", "?")
        source = e["meta"].get("source", "?")
        model = e["meta"]["model"]
        agg = e["aggregates"]
        
        rows_html = ""
        for ev in sorted(e["evaluations"], key=lambda x: x["score"], reverse=True):
            rows_html += f"""
            <tr>
                <td style='font-weight:600'>{ev['principle']}</td>
                <td>{score_bar(ev['score'], ev['confidence'], ev['uncertainty'])}</td>
            </tr>"""
        
        cards += f"""
        <div style='background:#181825;border:1px solid #313244;border-radius:8px;padding:20px;margin-bottom:20px'>
            <div style='display:flex;justify-content:space-between;align-items:baseline;margin-bottom:16px'>
                <div>
                    <span style='background:#cba6f7;color:#11111b;padding:2px 10px;border-radius:4px;font-size:12px;font-weight:600'>{tag}</span>
                    <div style='color:#6c7086;font-size:11px;margin-top:6px'>{source[:80]}</div>
                </div>
                <div style='text-align:right'>
                    <div style='font-size:32px;font-weight:bold;color:#cdd6f4'>{agg['mean_score']}</div>
                    <div style='color:#6c7086;font-size:10px'>mean · {model} · conf {agg['mean_confidence']:.0%}</div>
                </div>
            </div>
            <table style='width:100%'>{rows_html}</table>
        </div>"""
    
    comparison = build_comparison_table(evals)
    
    html = f"""<!DOCTYPE html>
<html lang='es'>
<head>
<meta charset='utf-8'>
<title>Critic Loop · Perfume IA · Joko Lab</title>
<style>
body {{ background:#11111b; color:#cdd6f4; font-family:system-ui,sans-serif; max-width:780px; margin:40px auto; padding:20px }}
h1 {{ color:#cba6f7; font-size:22px; margin-bottom:4px }}
.subtitle {{ color:#6c7086; font-size:13px; margin-bottom:24px }}
h3 {{ color:#cba6f7; font-size:15px; margin:24px 0 12px }}
table {{ width:100%;border-collapse:collapse;font-size:13px }}
th,td {{ padding:8px 12px;text-align:left;border-bottom:1px solid #313244 }}
th {{ color:#a6adc8;font-weight:600 }}
.delta-plus {{ color:#4ade80;font-weight:600 }}
.delta-minus {{ color:#f87171;font-weight:600 }}
.delta-zero {{ color:#6c7086 }}
.note {{ background:#1e1e2e;border-left:3px solid #cba6f7;padding:12px 16px;border-radius:4px;font-size:13px;margin:20px 0;color:#a6adc8 }}
.note strong {{ color:#cdd6f4 }}
.footer {{ color:#6c7086;font-size:11px;margin-top:40px;text-align:center }}
</style>
</head>
<body>
<h1>Critic Loop v0.1</h1>
<div class='subtitle'>Perfume IA · Evaluación de principios de diseño · {len(evals)} ejecuciones</div>

<div class='note'>
<strong>Restricción constitucional:</strong> este instrumento no modifica nada. Solo observa, mide y registra.<br>
<strong>Propósito:</strong> validar si los principios del YAML producen evaluaciones consistentes y detectar cuáles necesitan refinamiento.
</div>

{cards}
{comparison}
<div class='footer'>Joko Lab · {datetime.now().strftime('%Y-%m-%d %H:%M')} · instrumento científico</div>
</body>
</html>"""
    
    report_path = OUTPUTS / "report.html"
    report_path.write_text(html)
    print(f"Reporte generado: {report_path.resolve()}")
    print(f"Abrir en navegador: file://{report_path.resolve()}")

if __name__ == "__main__":
    generate()
