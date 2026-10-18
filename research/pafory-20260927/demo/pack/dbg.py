#!/usr/bin/env python3
"""Mide la altura real de cada bloque de una pieza (para saber qué recortar)."""
import re, subprocess, sys, pathlib
P = pathlib.Path(__file__).parent / "out"
name = sys.argv[1]
JS = """<pre id="dbg"></pre><script>
var c=[].slice.call(document.querySelector('.pad').children);
document.getElementById('dbg').textContent=c.map(function(e,i){
  var r=e.getBoundingClientRect();
  return i+') '+(e.className||e.tagName)+' h='+Math.round(r.height)+' bot='+Math.round(r.bottom);
}).join(' | ');
</script>"""
src = (P / f"{name}.html").read_text()
(P / f"dbg_{name}.html").write_text(src.replace("</body>", JS + "</body>"))
out = subprocess.run(["/usr/bin/google-chrome", "--headless=new", "--disable-gpu",
                      "--virtual-time-budget=5000", "--dump-dom", f"file://{P}/dbg_{name}.html"],
                     capture_output=True, text=True).stdout
m = re.search(r'<pre id="dbg">(.*?)</pre>', out, re.S)
txt = m.group(1) if m else "sin datos"
for bloque in txt.split(" | "):
    print(bloque)
print("--- total:", len(txt.split(" | ")), "bloques")
