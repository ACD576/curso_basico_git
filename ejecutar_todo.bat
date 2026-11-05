@echo off
REM ============================================================
REM  Ejecuta todas las pruebas y abre la carpeta con las imagenes.
REM ============================================================
setlocal EnableExtensions
cd /d "%~dp0"

set "PY="
for %%C in ("py" "python" "%LOCALAPPDATA%\Programs\Python\Launcher\py.exe" "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" "%ProgramFiles%\Python312\python.exe") do (
    if not defined PY (
        %%C -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>nul && set "PY=%%~C"
    )
)
if not defined PY (
    echo [ERROR] No se encuentra Python. Ejecuta primero instalar.bat
    pause
    exit /b 1
)

"%PY%" run_all.py
echo.
if exist output start "" "output"
pause
