#!/bin/bash
# render_formato_cuaderno_dbms.sh — renderiza formato-cuaderno-dbms.html a PNG
# Salida: research/infografias/formato-cuaderno-dbms.png

cd /home/jokoalmi/joko-lab/research/infografias
# Render delegado al helper unico del lab (los flags se deciden en un solo sitio).
bash /home/jokoalmi/joko-lab/tools/render_html.sh \
  formato-cuaderno-dbms.html formato-cuaderno-dbms.png 1080 1440
echo "exit: $?"
ls -la /home/jokoalmi/joko-lab/research/infografias/formato-cuaderno-dbms.png
