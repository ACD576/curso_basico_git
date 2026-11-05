"""
Prueba 03 - Simulación de un sensor LIDAR
==========================================

El robot está dentro de una habitación con obstáculos y lanza rayos láser
en todas direcciones. Se dibuja el mapa con los rayos y, a la derecha,
la lectura del sensor en coordenadas polares (lo que "ve" el robot).

Cómo ejecutarlo:
    - En VS Code: abre este archivo y pulsa el botón ▶ (Run Python File).
    - O desde una terminal en la carpeta del repositorio:  py pruebas\03_sensor_lidar\lidar.py
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

ANCHO_SALA = 10.0   # [m]
ALTO_SALA = 6.0     # [m]

# Obstáculos circulares: (x, y, radio) en metros
OBSTACULOS_CIRCULARES = [
    (2.0, 4.5, 0.6),
    (7.5, 1.5, 0.8),
    (6.0, 4.2, 0.4),
]

# Obstáculos rectangulares (cajas): (x_esquina, y_esquina, ancho, alto)
OBSTACULOS_CAJA = [
    (3.5, 1.0, 1.2, 0.8),
    (8.2, 3.8, 0.9, 1.4),
]

POSICION_ROBOT = (4.5, 3.2)  # (x, y) [m]
NUM_RAYOS = 180              # resolución angular del sensor
ALCANCE_MAX = 5.0            # distancia máxima que mide el sensor [m]
RUIDO = 0.03                 # desviación típica del ruido de medida [m]
SEMILLA = 42                 # para que el ruido sea siempre el mismo

# =====================================================================


def segmentos_del_mundo():
    """Devuelve todas las paredes y cajas como lista de segmentos (a, b)."""
    segs = []

    def rectangulo(x, y, w, h):
        p = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
        return [(np.array(p[i]), np.array(p[(i + 1) % 4])) for i in range(4)]

    segs += rectangulo(0, 0, ANCHO_SALA, ALTO_SALA)  # paredes de la sala
    for caja in OBSTACULOS_CAJA:
        segs += rectangulo(*caja)
    return segs


def distancia_a_segmento(origen, dirs, a, b):
    """Distancia desde 'origen' en cada dirección de 'dirs' hasta el segmento a-b."""
    e = b - a
    w = a - origen
    den = dirs[:, 0] * e[1] - dirs[:, 1] * e[0]
    with np.errstate(divide="ignore", invalid="ignore"):
        t = (w[0] * e[1] - w[1] * e[0]) / den
        u = (w[0] * dirs[:, 1] - w[1] * dirs[:, 0]) / den
    valido = (np.abs(den) > 1e-12) & (t > 0) & (u >= 0) & (u <= 1)
    return np.where(valido, t, np.inf)


def distancia_a_circulo(origen, dirs, cx, cy, r):
    """Distancia desde 'origen' en cada dirección de 'dirs' hasta un círculo."""
    oc = origen - np.array([cx, cy])
    b = dirs @ oc
    c = oc @ oc - r**2
    disc = b**2 - c
    with np.errstate(invalid="ignore"):
        t = -b - np.sqrt(disc)
    return np.where((disc >= 0) & (t > 0), t, np.inf)


def escanear(origen):
    angulos = np.linspace(-np.pi, np.pi, NUM_RAYOS, endpoint=False)
    dirs = np.column_stack([np.cos(angulos), np.sin(angulos)])
    dist = np.full(NUM_RAYOS, np.inf)
    for a, b in segmentos_del_mundo():
        dist = np.minimum(dist, distancia_a_segmento(origen, dirs, a, b))
    for cx, cy, r in OBSTACULOS_CIRCULARES:
        dist = np.minimum(dist, distancia_a_circulo(origen, dirs, cx, cy, r))

    rng = np.random.default_rng(SEMILLA)
    dist = dist + rng.normal(0, RUIDO, NUM_RAYOS)
    detectado = dist < ALCANCE_MAX
    dist = np.clip(dist, 0, ALCANCE_MAX)
    return angulos, dirs, dist, detectado


def main():
    estilo_star()
    origen = np.array(POSICION_ROBOT, dtype=float)
    angulos, dirs, dist, detectado = escanear(origen)
    impactos = origen + dirs * dist[:, None]

    fig = plt.figure(figsize=(14, 6))
    ax_mapa = fig.add_subplot(1, 2, 1)
    ax_polar = fig.add_subplot(1, 2, 2, projection="polar")

    # --- Mapa ---
    ax_mapa.add_patch(plt.Rectangle((0, 0), ANCHO_SALA, ALTO_SALA, fill=False,
                                    lw=3, ec=config.COLOR_OBSTACULO))
    for x, y, w, h in OBSTACULOS_CAJA:
        ax_mapa.add_patch(plt.Rectangle((x, y), w, h, color=config.COLOR_OBSTACULO))
    for cx, cy, r in OBSTACULOS_CIRCULARES:
        ax_mapa.add_patch(plt.Circle((cx, cy), r, color=config.COLOR_OBSTACULO))

    for (px, py), ok in zip(impactos, detectado):
        ax_mapa.plot([origen[0], px], [origen[1], py], lw=0.5,
                     color=config.COLOR_SECUNDARIO if ok else "#CCCCCC", alpha=0.6)
    ax_mapa.scatter(impactos[detectado, 0], impactos[detectado, 1], s=8,
                    color="#C0392B", zorder=4, label="impacto del láser")
    ax_mapa.add_patch(plt.Circle(origen, 0.25, color=config.COLOR_PRINCIPAL, ec="black", zorder=5))
    ax_mapa.set_xlim(-0.5, ANCHO_SALA + 0.5)
    ax_mapa.set_ylim(-0.5, ALTO_SALA + 0.5)
    ax_mapa.set_aspect("equal")
    ax_mapa.set_title(f"Mapa: {config.NOMBRE_ROBOT} en la sala")
    ax_mapa.set_xlabel("x [m]")
    ax_mapa.set_ylabel("y [m]")
    ax_mapa.legend(loc="upper right", fontsize=8)

    # --- Lectura polar ---
    ax_polar.plot(np.append(angulos, angulos[0]), np.append(dist, dist[0]),
                  color=config.COLOR_PRINCIPAL, lw=1.5)
    ax_polar.fill(angulos, dist, color=config.COLOR_PRINCIPAL, alpha=0.2)
    ax_polar.scatter(angulos[~detectado], dist[~detectado], s=6, color="#AAAAAA",
                     label="sin eco (fuera de alcance)")
    ax_polar.set_rmax(ALCANCE_MAX)
    ax_polar.set_title(f"Lectura del LIDAR ({NUM_RAYOS} rayos)", pad=18)
    ax_polar.legend(loc="lower left", bbox_to_anchor=(-0.15, -0.12), fontsize=8)

    print(f"Distancia mínima detectada: {dist.min():.2f} m")
    guardar_figura(fig, "03_sensor_lidar")


if __name__ == "__main__":
    main()
