@echo off
REM ============================================================
REM  Instala las librerias de Python que necesita el curso.
REM  Basta con hacer doble clic en este archivo una sola vez.
REM ============================================================
cd /d "%~dp0"
where py >nul 2>nul && (set PY=py) || (set PY=python)

%PY% --version >nul 2>nul
if errorlevel 1 (
    echo [ERROR] No se encuentra Python. Instalalo desde python.org
    echo         marcando la casilla "Add python.exe to PATH".
    pause
    exit /b 1
)

echo Instalando numpy y matplotlib...
%PY% -m pip install --user --disable-pip-version-check -r requirements.txt
if errorlevel 1 (
    echo.
    echo [ERROR] No se pudieron instalar las librerias.
) else (
    echo.
    echo [OK] Todo listo. Ahora haz doble clic en ejecutar_todo.bat
)
pause
