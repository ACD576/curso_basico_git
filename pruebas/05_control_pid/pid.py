"""
Prueba 05 - Ajuste de un controlador PID
=========================================

Simula un robot que tiene que avanzar exactamente DISTANCIA_OBJETIVO metros
usando un controlador PID. Se comparan varios ajustes de ganancias y se
calculan sus métricas (sobreoscilación, tiempo de establecimiento, error final).

Cómo ejecutarlo:
    - En VS Code: abre este archivo y pulsa el botón ▶ (Run Python File).
    - O desde una terminal en la carpeta del repositorio:  py pruebas\05_control_pid\pid.py
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

DISTANCIA_OBJETIVO = 1.0   # [m]
MASA = 2.0                 # masa del robot [kg]
ROZAMIENTO = 0.5           # rozamiento viscoso [N·s/m]
FUERZA_MAX = 6.0           # saturación de los motores [N]
DURACION = 10.0            # tiempo simulado [s]
DT = 0.005                 # paso de simulación [s]

# Ajustes a comparar:  "nombre": (Kp, Ki, Kd)
# >>> Añade tu propio ajuste en una línea nueva al final <<<
AJUSTES = {
    "Solo P": (8.0, 0.0, 0.0),
    "PD": (8.0, 0.0, 4.0),
    "PID": (8.0, 1.5, 4.0),
}

# =====================================================================


def simular(kp, ki, kd):
    n = int(DURACION / DT)
    t = np.arange(n) * DT
    x = np.zeros(n)   # posición
    v = 0.0           # velocidad
    u = np.zeros(n)   # fuerza aplicada
    integral = 0.0
    error_prev = DISTANCIA_OBJETIVO

    for k in range(1, n):
        error = DISTANCIA_OBJETIVO - x[k - 1]
        integral += error * DT
        derivada = (error - error_prev) / DT
        error_prev = error

        fuerza = kp * error + ki * integral + kd * derivada
        fuerza = np.clip(fuerza, -FUERZA_MAX, FUERZA_MAX)
        u[k] = fuerza

        a = (fuerza - ROZAMIENTO * v) / MASA
        v += a * DT
        x[k] = x[k - 1] + v * DT

    return t, x, u


def metricas(t, x):
    sobre = max(0.0, (x.max() - DISTANCIA_OBJETIVO) / DISTANCIA_OBJETIVO * 100)
    banda = 0.02 * DISTANCIA_OBJETIVO
    fuera = np.where(np.abs(x - DISTANCIA_OBJETIVO) > banda)[0]
    if len(fuera) == 0:
        t_est = 0.0
    elif fuera[-1] == len(t) - 1:
        t_est = np.inf  # termina fuera de la banda: nunca se estabiliza
    else:
        t_est = t[fuera[-1] + 1]  # último instante en que entra en la banda
    error_final = abs(DISTANCIA_OBJETIVO - x[-1])
    return sobre, t_est, error_final


def main():
    estilo_star()
    fig, (ax_x, ax_u) = plt.subplots(2, 1, figsize=(10, 7), sharex=True,
                                     gridspec_kw={"height_ratios": [3, 1.3]})

    ax_x.axhline(DISTANCIA_OBJETIVO, color="black", ls="--", lw=1, label="objetivo")
    ax_x.axhspan(DISTANCIA_OBJETIVO * 0.98, DISTANCIA_OBJETIVO * 1.02,
                 color=config.COLOR_ACENTO, alpha=0.15, label="banda ±2 %")

    print(f"{'Ajuste':<14}{'Kp':>6}{'Ki':>6}{'Kd':>6}{'Sobreosc.':>11}{'t_est':>9}{'error':>9}")
    for nombre, (kp, ki, kd) in AJUSTES.items():
        t, x, u = simular(kp, ki, kd)
        sobre, t_est, err = metricas(t, x)
        t_txt = "nunca" if np.isinf(t_est) else f"{t_est:.2f}s"
        etiqueta = f"{nombre}  (Kp={kp}, Ki={ki}, Kd={kd})  ->  {sobre:.0f}% / {t_txt}"
        linea, = ax_x.plot(t, x, lw=2, label=etiqueta)
        ax_u.plot(t, u, lw=1.2, color=linea.get_color())
        print(f"{nombre:<14}{kp:>6}{ki:>6}{kd:>6}{sobre:>10.1f}%{t_txt:>9}{err:>9.3f}")

    ax_x.set_ylabel("posición [m]")
    ax_x.set_title(f"Control PID de {config.NOMBRE_ROBOT}: avanzar {DISTANCIA_OBJETIVO} m\n"
                   "(leyenda: sobreoscilación / tiempo de establecimiento)")
    ax_x.legend(loc="lower right", fontsize=8)
    ax_u.axhline(FUERZA_MAX, color="#999999", ls=":", lw=1)
    ax_u.axhline(-FUERZA_MAX, color="#999999", ls=":", lw=1)
    ax_u.set_ylabel("fuerza [N]")
    ax_u.set_xlabel("tiempo [s]")

    guardar_figura(fig, "05_control_pid")


if __name__ == "__main__":
    main()
