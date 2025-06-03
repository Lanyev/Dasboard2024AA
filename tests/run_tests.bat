@echo off
echo.
echo ================================
echo  MOBA Dashboard Test Runner
echo ================================
echo.
echo Ejecutando tests automatizados...
echo.

python test_dashboard.py

echo.
if %ERRORLEVEL% EQU 0 (
    echo ✅ TESTS PASARON - Dashboard listo para commit
    echo.
    echo Para hacer commit, ejecuta:
    echo git add . && git commit -m "Tu mensaje aqui"
) else (
    echo ❌ TESTS FALLARON - Revisa errores antes del commit
)
echo.
pause
