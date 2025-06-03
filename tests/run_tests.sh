#!/bin/bash
echo ""
echo "================================"
echo " MOBA Dashboard Test Runner"
echo "================================"
echo ""
echo "Ejecutando tests automatizados..."
echo ""

python test_dashboard.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ TESTS PASARON - Dashboard listo para commit"
    echo ""
    echo "Para hacer commit, ejecuta:"
    echo "git add . && git commit -m 'Tu mensaje aqui'"
else
    echo ""
    echo "❌ TESTS FALLARON - Revisa errores antes del commit"
fi
echo ""
