@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Primero ejecuta Instalar_PostulaMente.bat
    pause
    exit /b 1
)

".venv\Scripts\python.exe" -m compileall -q app.py datos modulos tests
if errorlevel 1 goto :error
".venv\Scripts\python.exe" -m unittest discover -s tests -v
if errorlevel 1 goto :error

echo.
echo Todas las verificaciones terminaron correctamente.
pause
exit /b 0

:error
echo.
echo Se encontro un problema durante la verificacion.
pause
exit /b 1
