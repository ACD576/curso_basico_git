"""
Utilidades de dibujo compartidas por todas las pruebas.

- estilo_star():   aplica un estilo común a las gráficas.
- guardar_figura(): guarda la figura en la carpeta output/ (ignorada por git).

Si ejecutas cualquier prueba con la opción --show, además de guardar
la imagen se abrirá una ventana para verla:

    py pruebas\01_trayectoria\trayectoria.py --show
"""

import sys
from pathlib import Path

import matplotlib

MOSTRAR = "--show" in sys.argv
if not MOSTRAR:
    # Sin ventana: solo genera archivos (funciona también en GitHub Actions)
    matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402

from . import config  # noqa: E402

RAIZ = Path(__file__).resolve().parents[1]
CARPETA_SALIDA = RAIZ / "output"


def estilo_star():
    """Aplica el estilo visual común del equipo."""
    plt.rcParams.update({
        "figure.facecolor": "white",
        "axes.facecolor": "#FAFAFA",
        "axes.edgecolor": "#BBBBBB",
        "axes.grid": True,
        "grid.color": "#E3E3E3",
        "grid.linestyle": "-",
        "axes.titleweight": "bold",
        "axes.titlesize": 13,
        "axes.labelsize": 11,
        "axes.prop_cycle": matplotlib.cycler(color=[
            config.COLOR_PRINCIPAL, config.COLOR_SECUNDARIO, config.COLOR_ACENTO,
            "#8E44AD", "#C0392B", "#16A085",
        ]),
        "font.size": 10,
    })


def guardar_figura(fig, nombre):
    """Guarda la figura como output/<nombre>.png y la muestra si se pidió --show."""
    CARPETA_SALIDA.mkdir(exist_ok=True)
    ruta = CARPETA_SALIDA / f"{nombre}.png"

    # Firma del equipo en la esquina inferior derecha
    fig.text(0.995, 0.005, f"{config.EQUIPO} - {config.EQUIPO_COMPLETO}",
             ha="right", va="bottom", fontsize=7, color="#888888")

    fig.savefig(ruta, dpi=config.DPI, bbox_inches="tight")
    print(f"[OK] Imagen guardada en {ruta.relative_to(RAIZ)}")

    if MOSTRAR:
        plt.show()
    plt.close(fig)
    return ruta
