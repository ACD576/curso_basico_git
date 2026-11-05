@echo off
REM ======================================================================
REM  Curso de Git y GitHub - Equipo STAR
REM  Comprueba e instala todo lo necesario para el curso:
REM    1. GitHub Desktop
REM    2. Python 3.12
REM    3. Visual Studio Code + extension de Python
REM    4. Librerias numpy y matplotlib
REM  Lo que ya este instalado no se toca. No necesita administrador.
REM
REM  Se puede ejecutar ANTES de clonar el repositorio: basta con descargar
REM  este archivo desde GitHub (boton "Download raw file") y hacer doble clic.
REM ======================================================================
setlocal EnableExtensions
cd /d "%~dp0"
title Curso Git STAR - Instalacion

echo ======================================================================
echo   Curso de Git y GitHub - Equipo STAR
echo.
echo   Este programa comprueba e instala lo que falte:
echo     1. GitHub Desktop
echo     2. Python 3.12
echo     3. Visual Studio Code + extension de Python
echo     4. Librerias numpy y matplotlib
echo.
echo   Lo que ya tengas instalado no se toca. Puede tardar varios minutos.
echo ======================================================================
echo.
pause

set "WINGET=1"
winget --version >nul 2>nul || set "WINGET=0"
if "%WINGET%"=="0" (
    echo.
    echo [AVISO] No se encuentra "winget" en este ordenador.
    echo         Lo que falte se tendra que instalar a mano: se abriran las paginas de descarga.
)

set "R_DESKTOP=FALTA"
set "R_PYTHON=FALTA"
set "R_CODE=FALTA"
set "R_EXT=FALTA"
set "R_LIBS=FALTA"

REM ----------------------------------------------------------------------
echo.
echo [1/4] GitHub Desktop
call :buscar_desktop
if defined DESKTOP (
    echo       Ya instalado.
    goto :desktop_ok
)
call :instalar GitHub.GitHubDesktop "https://desktop.github.com"
call :buscar_desktop
:desktop_ok
if defined DESKTOP set "R_DESKTOP=OK"

REM ----------------------------------------------------------------------
echo.
echo [2/4] Python
call :buscar_python
if defined PY (
    echo       Ya instalado.
    goto :python_ok
)
call :instalar Python.Python.3.12 "https://www.python.org/downloads/" "/quiet InstallAllUsers=0 PrependPath=1 Include_launcher=1 InstallLauncherAllUsers=0 Include_test=0"
call :buscar_python
:python_ok
if defined PY set "R_PYTHON=OK"

REM ----------------------------------------------------------------------
echo.
echo [3/4] Visual Studio Code
call :buscar_code
if defined CODE (
    echo       Ya instalado.
    goto :code_ok
)
call :instalar Microsoft.VisualStudioCode "https://code.visualstudio.com"
call :buscar_code
:code_ok
if not defined CODE goto :libs
set "R_CODE=OK"
echo       Instalando la extension de Python para VS Code...
call "%CODE%" --install-extension ms-python.python >nul 2>nul
if not errorlevel 1 set "R_EXT=OK"

REM ----------------------------------------------------------------------
:libs
echo.
echo [4/4] Librerias de Python (numpy y matplotlib)
if not defined PY (
    echo       No se puede: falta Python.
    goto :extensiones
)
if exist "requirements.txt" (
    "%PY%" -m pip install --user --disable-pip-version-check -q -r requirements.txt
) else (
    "%PY%" -m pip install --user --disable-pip-version-check -q numpy matplotlib
)
"%PY%" -c "import numpy, matplotlib" >nul 2>nul && set "R_LIBS=OK"

REM ----------------------------------------------------------------------
:extensiones
echo.
echo Recomendado: que el Explorador de Windows muestre las extensiones de los
echo archivos, para no acabar con nombres como "robot.json.json".
choice /c SN /m "Activarlo ahora? S = si, N = no"
if errorlevel 2 goto :resumen
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" /v HideFileExt /t REG_DWORD /d 0 /f >nul
echo       Hecho. Se nota al abrir una ventana nueva del Explorador.

REM ----------------------------------------------------------------------
:resumen
echo.
echo ======================================================================
echo   RESUMEN
echo     GitHub Desktop .............. %R_DESKTOP%
echo     Python ...................... %R_PYTHON%
echo     Visual Studio Code .......... %R_CODE%
echo     Extension Python de VS Code . %R_EXT%
echo     numpy y matplotlib .......... %R_LIBS%
echo ======================================================================
echo.
if "%R_DESKTOP%%R_PYTHON%%R_CODE%%R_EXT%%R_LIBS%"=="OKOKOKOKOK" (
    echo   Todo listo. Siguiente paso: abre GitHub Desktop e inicia sesion
    echo   con tu cuenta de GitHub: File - Options - Accounts - Sign in.
) else (
    echo   Algo ha fallado. Instala a mano lo que pone FALTA, o vuelve a
    echo   ejecutar este archivo. Si sigue fallando, avisa al instructor.
)
echo.
pause
exit /b 0


REM ======================================================================
REM  Subrutinas
REM ======================================================================

:instalar
REM  %1 = id de winget   %2 = pagina de descarga   %3 = opciones del instalador (opcional)
if "%WINGET%"=="0" goto :instalar_manual
set "OVR="
if not "%~3"=="" set OVR=--override "%~3"
echo       Instalando %~1 ...
winget install -e --id %~1 --scope user --silent --accept-package-agreements --accept-source-agreements %OVR%
if not errorlevel 1 exit /b 0
echo       Reintentando sin la opcion de usuario...
winget install -e --id %~1 --silent --accept-package-agreements --accept-source-agreements %OVR%
if not errorlevel 1 exit /b 0
:instalar_manual
echo       No se ha podido instalar automaticamente. Se abre la pagina de descarga:
echo       %~2
start "" "%~2"
echo       Instalalo y despues pulsa una tecla para seguir.
pause >nul
exit /b 1

:buscar_desktop
set "DESKTOP="
if exist "%LOCALAPPDATA%\GitHubDesktop\GitHubDesktop.exe" set "DESKTOP=%LOCALAPPDATA%\GitHubDesktop\GitHubDesktop.exe"
if exist "%ProgramFiles%\GitHub Desktop\GitHubDesktop.exe" set "DESKTOP=%ProgramFiles%\GitHub Desktop\GitHubDesktop.exe"
exit /b 0

:buscar_python
REM  Busca un Python 3.10 o superior (el alias de la Microsoft Store no cuenta)
set "PY="
for %%C in ("py" "python" "%LOCALAPPDATA%\Programs\Python\Launcher\py.exe" "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" "%ProgramFiles%\Python312\python.exe") do (
    if not defined PY (
        %%C -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>nul && set "PY=%%~C"
    )
)
exit /b 0

:buscar_code
set "CODE="
if exist "%LOCALAPPDATA%\Programs\Microsoft VS Code\bin\code.cmd" set "CODE=%LOCALAPPDATA%\Programs\Microsoft VS Code\bin\code.cmd"
if exist "%ProgramFiles%\Microsoft VS Code\bin\code.cmd" set "CODE=%ProgramFiles%\Microsoft VS Code\bin\code.cmd"
if defined CODE exit /b 0
where code >nul 2>nul && set "CODE=code"
exit /b 0
