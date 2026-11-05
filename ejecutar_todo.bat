@echo off
REM ============================================================
REM  Ejecuta todas las pruebas y abre la carpeta con las imagenes.
REM ============================================================
cd /d "%~dp0"
where py >nul 2>nul && (set PY=py) || (set PY=python)

%PY% run_all.py
echo.
if exist output start "" "output"
pause
