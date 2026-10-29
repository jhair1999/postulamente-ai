@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo PostulaMente AI necesita preparar sus dependencias.
    call Instalar_PostulaMente.bat
    if errorlevel 1 exit /b 1
)

echo ==============================================
echo   Iniciando PostulaMente AI
echo ==============================================
echo La aplicacion se abrira en http://localhost:8501
echo Para detenerla, presiona Ctrl+C en esta ventana.
echo.

".venv\Scripts\python.exe" -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501

if errorlevel 1 (
    echo.
    echo Ocurrio un error al iniciar la aplicacion.
    pause
)
