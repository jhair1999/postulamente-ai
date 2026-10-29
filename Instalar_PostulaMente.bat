@echo off
setlocal
cd /d "%~dp0"

echo ==============================================
echo   Instalacion de PostulaMente AI
echo ==============================================
echo.

where py >nul 2>&1
if errorlevel 1 (
    echo No se encontro Python en este equipo.
    echo Instala Python 3.12 o posterior desde https://www.python.org/downloads/
    pause
    exit /b 1
)

if exist ".venv\Scripts\python.exe" (
    echo El entorno virtual ya existe.
) else (
    py -3.12 --version >nul 2>&1
    if errorlevel 1 (
        echo Creando el entorno con la version disponible de Python...
        py -m venv .venv
    ) else (
        echo Creando el entorno con Python 3.12...
        py -3.12 -m venv .venv
    )
    if errorlevel 1 goto :error
)

echo Instalando dependencias...
".venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 goto :error
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto :error

echo.
echo Instalacion completada correctamente.
echo Ahora ejecuta Iniciar_PostulaMente.bat
pause
exit /b 0

:error
echo.
echo La instalacion no pudo completarse.
pause
exit /b 1
