"""
Prueba 04 - Planificador de rutas A*
=====================================

Lee el mapa desde 'mapa.txt' y busca el camino más corto desde la salida (S)
hasta la meta (G) usando el algoritmo A*.

Leyenda del mapa:
    #  muro
    .  suelo libre
    ~  barro (se puede pasar, pero cuesta más)
    S  salida  (debe haber exactamente una)
    G  meta    (debe haber exactamente una)

Ejecutar desde la raíz del repositorio:
    python pruebas/04_planificador_ruta/ruta.py
"""

import heapq
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # para importar 'star'

import numpy as np  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import ListedColormap  # noqa: E402

from star import config, estilo_star, guardar_figura  # noqa: E402

# =====================================================================
#  PARÁMETROS  ->  ¡Modifica esto! (y sobre todo, modifica mapa.txt)
# =====================================================================

ARCHIVO_MAPA = Path(__file__).with_name("mapa.txt")
DIAGONALES = True     # ¿puede moverse en diagonal?
COSTE_BARRO = 5.0     # cuánto cuesta atravesar una casilla de barro

# =====================================================================

LIBRE, MURO, BARRO = 0, 1, 2


def leer_mapa(ruta):
    lineas = ruta.read_text(encoding="utf-8").splitlines()
    lineas = [l.rstrip() for l in lineas if l.strip()]

    # Detecta un conflicto de git sin resolver y avisa con un mensaje claro
    for n, l in enumerate(lineas, 1):
        if l.startswith(("<<<<<<<", "=======", ">>>>>>>")):
            sys.exit(f"[ERROR] {ruta.name}, línea {n}: parece un conflicto de git sin "
                     f"resolver ('{l[:20]}'). Edita el archivo, elige qué cambios "
                     f"quedarse y borra las marcas <<<<<<< ======= >>>>>>>.")

    ancho = max(len(l) for l in lineas)
    if any(len(l) != ancho for l in lineas):
        print(f"[AVISO] No todas las filas de {ruta.name} miden lo mismo; "
              f"se rellenan con muro.")
    lineas = [l.ljust(ancho, "#") for l in lineas]

    grid = np.zeros((len(lineas), ancho), dtype=int)
    inicio = meta = None
    for f, linea in enumerate(lineas):
        for c, ch in enumerate(linea):
            if ch == "#":
                grid[f, c] = MURO
            elif ch == "~":
                grid[f, c] = BARRO
            elif ch == "S":
                if inicio is not None:
                    sys.exit("[ERROR] El mapa tiene más de una 'S'.")
                inicio = (f, c)
            elif ch == "G":
                if meta is not None:
                    sys.exit("[ERROR] El mapa tiene más de una 'G'.")
                meta = (f, c)
            elif ch != ".":
                sys.exit(f"[ERROR] Carácter desconocido '{ch}' en fila {f + 1}, columna {c + 1}.")
    if inicio is None or meta is None:
        sys.exit("[ERROR] El mapa necesita una 'S' (salida) y una 'G' (meta).")
    return grid, inicio, meta


def a_estrella(grid, inicio, meta):
    """Devuelve (camino, casillas_exploradas). camino = [] si no hay ruta."""
    filas, cols = grid.shape
    movs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    if DIAGONALES:
        movs += [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    def h(p):  # heurística: distancia euclídea
        return np.hypot(p[0] - meta[0], p[1] - meta[1])

    abiertos = [(h(inicio), 0.0, inicio)]
    coste = {inicio: 0.0}
    padre = {}
    explorado = set()

    while abiertos:
        _, g, actual = heapq.heappop(abiertos)
        if actual in explorado:
            continue
        explorado.add(actual)
        if actual == meta:
            break
        for df, dc in movs:
            f, c = actual[0] + df, actual[1] + dc
            if not (0 <= f < filas and 0 <= c < cols) or grid[f, c] == MURO:
                continue
            # no cortar esquinas en diagonal
            if df and dc and (grid[actual[0] + df, actual[1]] == MURO
                              or grid[actual[0], actual[1] + dc] == MURO):
                continue
            paso = np.hypot(df, dc) * (COSTE_BARRO if grid[f, c] == BARRO else 1.0)
            nuevo = g + paso
            if nuevo < coste.get((f, c), np.inf):
                coste[(f, c)] = nuevo
                padre[(f, c)] = actual
                heapq.heappush(abiertos, (nuevo + h((f, c)), nuevo, (f, c)))

    if meta not in padre and meta != inicio:
        return [], explorado, np.inf
    camino = [meta]
    while camino[-1] != inicio:
        camino.append(padre[camino[-1]])
    return camino[::-1], explorado, coste[meta]


def main():
    estilo_star()
    grid, inicio, meta = leer_mapa(ARCHIVO_MAPA)
    camino, explorado, coste_total = a_estrella(grid, inicio, meta)

    fig, ax = plt.subplots(figsize=(grid.shape[1] * 0.4 + 1, grid.shape[0] * 0.4 + 1.2))
    cmap = ListedColormap(["#FFFFFF", config.COLOR_OBSTACULO, "#B5895A"])
    ax.imshow(grid, cmap=cmap, vmin=0, vmax=2)

    # Casillas exploradas por A*
    if explorado:
        ef, ec = zip(*explorado)
        ax.scatter(ec, ef, s=40, marker="s", color=config.COLOR_PRINCIPAL, alpha=0.15,
                   label=f"exploradas ({len(explorado)})")

    if camino:
        cf, cc = zip(*camino)
        ax.plot(cc, cf, "-", color=config.COLOR_SECUNDARIO, lw=3.5, label="ruta")
        titulo = f"Ruta A* de {config.NOMBRE_ROBOT}: {len(camino) - 1} pasos, coste {coste_total:.1f}"
    else:
        titulo = "¡No existe ninguna ruta hasta la meta!"
        print("[AVISO] No hay ruta posible entre S y G.")

    if (grid == BARRO).any():
        ax.scatter([], [], s=80, marker="s", color="#B5895A", label=f"barro (coste x{COSTE_BARRO:g})")
    ax.scatter([inicio[1]], [inicio[0]], s=200, marker="o", color=config.COLOR_ACENTO,
               ec="black", zorder=5, label="salida (S)")
    ax.scatter([meta[1]], [meta[0]], s=320, marker="*", color="#F4D03F",
               ec="black", zorder=5, label="meta (G)")

    ax.set_title(titulo)
    ax.set_xticks(range(grid.shape[1]))
    ax.set_yticks(range(grid.shape[0]))
    ax.tick_params(labelsize=6)
    ax.grid(False)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.06), ncol=5, fontsize=8)

    guardar_figura(fig, "04_planificador_ruta")


if __name__ == "__main__":
    main()
