# Alias para Joko Lab
# ANOMALIAS: muestra anomalias si inicio.sh detecta problemas.
# No bloquea. Corre en segundo plano, solo notifica si hay fallos.
#
# Uso: Al abrir terminal, se ejecuta inicio.sh --quick
# Si todo OK, silencioso. Si hay anomalias, notificacion visible.
#
# Instalacion: anadir a ~/.bashrc

alias joko-status='bash ~/joko-lab/02-infrastructure/inicio/inicio.sh 2>/dev/null | grep -E "(FAIL|WARN|ANOMALIAS|LABORATORIO)"'

# Arranque semi-automatico: muestra anomalias sin bloquear
# Se ejecuta al abrir terminal. Solo muestra si hay problemas.
if [ -f ~/joko-lab/02-infrastructure/inicio/inicio.sh ]; then
    ANOMALIAS=$(bash ~/joko-lab/02-infrastructure/inicio/inicio.sh 2>/dev/null | grep -E "(FAIL|ANOMALIAS)")
    if [ -n "$ANOMALIAS" ]; then
        echo ""
        echo "⚠ Joko Lab: anomalias detectadas. Ejecuta 'joko-status' para detalles."
        echo ""
    fi
fi
