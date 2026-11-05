"""
Comprueba que están instaladas las librerías que necesitan las pruebas
(numpy y matplotlib) y, si faltan, las instala automáticamente en el Python
que está ejecutando el script.

Así da igual qué Python haya elegido VS Code: la primera vez que se ejecuta
una prueba se instala lo que falte y a partir de ahí funciona directamente.
"""

import importlib
import importlib.util
import site
import subprocess
import sys

NECESARIAS = ["numpy", "matplotlib"]


def _faltan():
    importlib.invalidate_caches()
    return [m for m in NECESARIAS if importlib.util.find_spec(m) is None]


def _instrucciones_manuales():
    return (
        "\n[ERROR] No se han podido instalar las librerías automáticamente.\n"
        "Soluciones:\n"
        "  1. En VS Code pulsa Ctrl+Shift+P, escribe 'Python: Select Interpreter'\n"
        "     y elige el Python 3.12 que instaló instalar.bat.\n"
        "  2. O abre una terminal y ejecuta:\n"
        f'       "{sys.executable}" -m pip install numpy matplotlib\n'
    )


def comprobar():
    faltan = _faltan()
    if not faltan:
        return

    print(f"[AVISO] A este Python le faltan librerías: {', '.join(faltan)}")
    print(f"        Python usado: {sys.executable}")
    print("        Instalándolas automáticamente (solo pasa la primera vez)...\n", flush=True)

    resultado = subprocess.run(
        [sys.executable, "-m", "pip", "install", "--disable-pip-version-check", *faltan]
    )
    if resultado.returncode != 0:
        sys.exit(_instrucciones_manuales())

    # Si pip ha instalado en la carpeta del usuario y esta no existía al arrancar,
    # Python todavía no la tiene en cuenta: la añadimos a mano.
    try:
        site.addsitedir(site.getusersitepackages())
    except Exception:
        pass

    if _faltan():
        sys.exit("\n[AVISO] Librerías instaladas. Vuelve a ejecutar el script.")
    print("\n[OK] Librerías instaladas. Continuando...\n", flush=True)
