#!/usr/bin/env bash
# model-router.sh — Router horario para Hermes Agent
#
# ANALISIS DE COSTES REALES (Julio 2026):
#   DeepSeek V4 Flash: $0.077/M input, $0.154/M output
#   Gemini 2.5 Flash:  $0.300/M input, $2.500/M output
#   Gemini 2.5 FL:     $0.100/M input, $0.400/M output
#
# DeepSeek es 13x mas barato que Gemini 2.5 Flash y 2.2x mas barato
# que Gemini Flash-Lite en output. La politica original de "cambiar a
# Gemini en franja cara para ahorrar costes" estaba basada en datos
# previos o en otro proveedor. Con los precios actuales NO hay motivo
# para cambiar de modelo por coste.
#
# El unico motivo para usar local (Ollama) es privacidad de datos,
# no coste. DeepSeek V4 Flash se mantiene como default permanente.
#
# Este script se mantiene por compatibilidad pero ya no realiza
# cambios de modelo. Se conserva para futuros routers si se
# necesitaran y para no romver ~/.bashrc que lo sourcea.

unset HERMES_MODEL
