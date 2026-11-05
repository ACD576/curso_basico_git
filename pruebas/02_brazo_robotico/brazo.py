"""
Prueba 02 - Brazo robótico de 2 articulaciones
===============================================

Dibuja un brazo plano de dos eslabones en varias posturas (cinemática
directa), su espacio de trabajo y, si se define un OBJETIVO, las dos
soluciones de cinemática inversa (codo arriba / codo abajo) para alcanzarlo.

Cómo ejecutarlo:
    - En VS Code: abre este archivo y pulsa el botón ▶ (Run Python File).
    - O desde una terminal en la carpeta del repositorio:  py pruebas\02_brazo_robotico\brazo.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # para importar 'star'

import numpy as np  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402

from star import config, estilo_star, guardar_figura  # noqa: E402

# =====================================================================
#  PARÁMETROS  ->  ¡Modifica esto!
# =====================================================================

L1 = 1.0   # longitud del primer eslabón (hombro -> codo) [m]
L2 = 0.7   # longitud del segundo eslabón (codo -> pinza) [m]

# Límites de cada articulación [grados]
LIMITES_Q1 = (-30, 210)
LIMITES_Q2 = (-150, 150)

# Posturas a dibujar: (ángulo hombro, ángulo codo) en grados
POSTURAS = [
    (20, 40),
    (75, -50),
    (130, 60),
    (170, -100),
]

# Punto que queremos alcanzar con la pinza (o None para no calcularlo)
OBJETIVO = (0.9, 1.1)

# =====================================================================


def cinematica_directa(q1_deg, q2_deg):
    """Devuelve las posiciones (hombro, codo, pinza) para unos ángulos dados."""
    q1, q2 = np.radians(q1_deg), np.radians(q2_deg)
    hombro = np.array([0.0, 0.0])
    codo = hombro + L1 * np.array([np.cos(q1), np.sin(q1)])
    pinza = codo + L2 * np.array([np.cos(q1 + q2), np.sin(q1 + q2)])
    return hombro, codo, pinza


def cinematica_inversa(x, y):
    """Devuelve una lista con las soluciones (q1, q2) en grados que alcanzan (x, y)."""
    c2 = (x**2 + y**2 - L1**2 - L2**2) / (2 * L1 * L2)
    if abs(c2) > 1:
        return []  # fuera del alcance
    soluciones = []
    for signo in (+1, -1):  # codo abajo / codo arriba
        q2 = signo * np.arccos(c2)
        q1 = np.arctan2(y, x) - np.arctan2(L2 * np.sin(q2), L1 + L2 * np.cos(q2))
        soluciones.append((np.degrees(q1), np.degrees(q2)))
    return soluciones


def dentro_de_limites(q1, q2):
    q1 = (q1 - LIMITES_Q1[0]) % 360 + LIMITES_Q1[0]  # normaliza al rango
    return LIMITES_Q1[0] <= q1 <= LIMITES_Q1[1] and LIMITES_Q2[0] <= q2 <= LIMITES_Q2[1]


def dibujar_brazo(ax, q1, q2, color, etiqueta=None, estilo="-", alpha=1.0):
    hombro, codo, pinza = cinematica_directa(q1, q2)
    xs = [hombro[0], codo[0], pinza[0]]
    ys = [hombro[1], codo[1], pinza[1]]
    ax.plot(xs, ys, estilo, color=color, lw=6, solid_capstyle="round",
            alpha=alpha, label=etiqueta, zorder=3)
    ax.scatter(xs[:2], ys[:2], s=70, color="white", ec="black", zorder=4)
    ax.scatter([pinza[0]], [pinza[1]], s=60, marker="D", color=color, ec="black", zorder=5)
    return pinza


def main():
    estilo_star()
    fig, ax = plt.subplots(figsize=(8, 7))

    # Espacio de trabajo: muestreamos muchas combinaciones de ángulos
    q1s = np.linspace(*LIMITES_Q1, 160)
    q2s = np.linspace(*LIMITES_Q2, 160)
    Q1, Q2 = np.meshgrid(np.radians(q1s), np.radians(q2s))
    wx = L1 * np.cos(Q1) + L2 * np.cos(Q1 + Q2)
    wy = L1 * np.sin(Q1) + L2 * np.sin(Q1 + Q2)
    ax.scatter(wx, wy, s=1, color=config.COLOR_PRINCIPAL, alpha=0.08, zorder=1)
    ax.plot([], [], "s", color=config.COLOR_PRINCIPAL, alpha=0.3, label="espacio de trabajo")

    # Posturas definidas por el usuario
    colores = plt.cm.tab10(np.linspace(0, 1, 10))
    for i, (q1, q2) in enumerate(POSTURAS):
        pinza = dibujar_brazo(ax, q1, q2, colores[i % 10], f"q1={q1}°, q2={q2}°")
        ax.annotate(f"({pinza[0]:.2f}, {pinza[1]:.2f})", pinza,
                    textcoords="offset points", xytext=(8, 8), fontsize=8)

    # Cinemática inversa hacia el objetivo
    titulo_extra = ""
    if OBJETIVO is not None:
        ax.scatter(*OBJETIVO, s=300, marker="*", color=config.COLOR_SECUNDARIO,
                   ec="black", zorder=6, label="objetivo")
        soluciones = cinematica_inversa(*OBJETIVO)
        validas = [s for s in soluciones if dentro_de_limites(*s)]
        for q1, q2 in validas:
            dibujar_brazo(ax, q1, q2, "black", f"IK: q1={q1:.0f}°, q2={q2:.0f}°",
                          estilo="--", alpha=0.6)
        if not soluciones:
            titulo_extra = "\n¡El objetivo está fuera del alcance!"
            print("[AVISO] El objetivo está fuera del alcance del brazo.")
        elif not validas:
            titulo_extra = "\nEl objetivo se alcanza solo fuera de los límites articulares"
        else:
            titulo_extra = f"\n{len(validas)} solución(es) de cinemática inversa"

    # Base del robot
    ax.add_patch(plt.Rectangle((-0.15, -0.12), 0.3, 0.12, color=config.COLOR_OBSTACULO, zorder=2))

    alcance = L1 + L2
    ax.set_xlim(-alcance * 1.15, alcance * 1.15)
    ax.set_ylim(-alcance * 0.75, alcance * 1.15)
    ax.set_aspect("equal")
    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    ax.set_title(f"Brazo de {config.NOMBRE_ROBOT}  (L1={L1} m, L2={L2} m){titulo_extra}")
    ax.legend(loc="lower left", fontsize=8, framealpha=0.9)

    guardar_figura(fig, "02_brazo_robotico")


if __name__ == "__main__":
    main()
