"""
Prueba 06 - Galería de robots del equipo
=========================================

Cada participante añade UN archivo propio en la carpeta 'participantes/'
describiendo su robot (copia '_plantilla.json'). Este script lee todos los
archivos y dibuja una galería con todos los robots del equipo.

Como cada persona toca un archivo distinto, es la prueba ideal para
practicar ramas y Pull Requests sin conflictos.

Cómo ejecutarlo:
    - En VS Code: abre este archivo y pulsa el botón ▶ (Run Python File).
    - O desde una terminal en la carpeta del repositorio:  py pruebas/06_galeria_robots/galeria.py
"""

import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # para importar 'star'

# Importar 'star' primero: comprueba que numpy y matplotlib están instalados
from star import config, estilo_star, guardar_figura  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import patches  # noqa: E402
from matplotlib.colors import is_color_like  # noqa: E402

CARPETA = Path(__file__).with_name("participantes")
COLUMNAS = 4

FORMAS = ("cuadrado", "circulo", "triangulo", "hexagono")
TRACCIONES = ("ruedas", "orugas", "patas", "helices")


# ---------------------------------------------------------------------
#  Lectura y validación
# ---------------------------------------------------------------------

def cargar_participantes():
    errores, robots = [], []
    archivos = sorted(p for p in CARPETA.glob("*.json") if not p.name.startswith("_"))

    for archivo in archivos:
        texto = archivo.read_text(encoding="utf-8")
        if "<<<<<<<" in texto or ">>>>>>>" in texto:
            errores.append(f"{archivo.name}: tiene marcas de conflicto de git sin resolver.")
            continue
        try:
            datos = json.loads(texto)
        except json.JSONDecodeError as e:
            errores.append(f"{archivo.name}: JSON no válido (línea {e.lineno}, "
                           f"columna {e.colno}): {e.msg}. ¿Falta una coma o unas comillas?")
            continue

        problemas = validar(datos)
        if problemas:
            errores += [f"{archivo.name}: {p}" for p in problemas]
        else:
            datos["_archivo"] = archivo.name
            robots.append(datos)

    return robots, errores


def validar(d):
    p = []
    for campo in ("nombre", "robot", "color"):
        if not isinstance(d.get(campo), str) or not d.get(campo).strip():
            p.append(f"falta el campo obligatorio '{campo}' (texto)")
    if "color" in d and not is_color_like(d["color"]):
        p.append(f"el color '{d['color']}' no es válido (usa '#RRGGBB' o un nombre como 'red')")
    if d.get("forma", "cuadrado") not in FORMAS:
        p.append(f"'forma' debe ser una de {FORMAS}")
    if d.get("traccion", "ruedas") not in TRACCIONES:
        p.append(f"'traccion' debe ser una de {TRACCIONES}")
    ojos = d.get("ojos", 2)
    if not isinstance(ojos, int) or not 1 <= ojos <= 3:
        p.append("'ojos' debe ser un número entero entre 1 y 3")
    if not isinstance(d.get("antena", True), bool):
        p.append("'antena' debe ser true o false (sin comillas)")
    if len(d.get("lema", "")) > 40:
        p.append("el 'lema' no puede tener más de 40 caracteres")
    return p


# ---------------------------------------------------------------------
#  Dibujo de un robot
# ---------------------------------------------------------------------

def dibujar_robot(ax, r):
    color = r["color"]
    forma = r.get("forma", "cuadrado")
    kw = dict(fc=color, ec="black", lw=2, zorder=3)

    # Cuerpo (centrado en 0, 0.1)
    if forma == "cuadrado":
        cuerpo = patches.FancyBboxPatch((-0.6, -0.45), 1.2, 1.1,
                                        boxstyle="round,pad=0.02,rounding_size=0.15", **kw)
    elif forma == "circulo":
        cuerpo = patches.Circle((0, 0.1), 0.62, **kw)
    elif forma == "triangulo":
        cuerpo = patches.Polygon([(-0.75, -0.45), (0.75, -0.45), (0, 0.85)], **kw)
    else:  # hexagono
        cuerpo = patches.RegularPolygon((0, 0.1), 6, radius=0.68, orientation=math.pi / 6, **kw)
    ax.add_patch(cuerpo)

    # Ojos
    ojos = r.get("ojos", 2)
    triangular = forma == "triangulo"
    y_ojos = 0.0 if triangular else 0.25
    sep = 0.24 if triangular else 0.32
    radio = 0.1 if triangular else 0.12
    xs = [(i - (ojos - 1) / 2) * sep for i in range(ojos)]
    for x in xs:
        ax.add_patch(patches.Circle((x, y_ojos), radio, fc="white", ec="black", lw=1.5, zorder=4))
        ax.add_patch(patches.Circle((x + 0.025, y_ojos), radio * 0.42, fc="black", zorder=5))

    # Boca / panel
    ax.add_patch(patches.Rectangle((-0.22, -0.22), 0.44, 0.08, fc="#222222", zorder=4))

    # Antena
    tope = {"triangulo": 0.85, "circulo": 0.72, "hexagono": 0.69, "cuadrado": 0.67}[forma]
    if r.get("antena", True):
        ax.plot([0, 0], [tope, tope + 0.3], color="black", lw=2, zorder=2)
        ax.add_patch(patches.Circle((0, tope + 0.35), 0.07, fc=config.COLOR_SECUNDARIO,
                                    ec="black", zorder=3))

    # Tracción
    traccion = r.get("traccion", "ruedas")
    if traccion == "ruedas":
        for x in (-0.4, 0.4):
            ax.add_patch(patches.Circle((x, -0.6), 0.17, fc="#333333", ec="black", zorder=2))
            ax.add_patch(patches.Circle((x, -0.6), 0.06, fc="#BBBBBB", zorder=3))
    elif traccion == "orugas":
        ax.add_patch(patches.FancyBboxPatch((-0.7, -0.78), 1.4, 0.3,
                                            boxstyle="round,pad=0,rounding_size=0.15",
                                            fc="#333333", ec="black", zorder=2))
        for i in range(5):
            ax.add_patch(patches.Circle((-0.5 + i * 0.25, -0.63), 0.06, fc="#999999", zorder=3))
    elif traccion == "patas":
        for x in (-0.35, 0.35):
            ax.plot([x, x * 1.3], [-0.45, -0.8], color="black", lw=4, zorder=2)
            ax.add_patch(patches.Ellipse((x * 1.3, -0.82), 0.25, 0.08, fc="#333333", zorder=3))
    else:  # helices
        for x in (-0.75, 0.75):
            ax.plot([x * 0.8, x], [0.1, 0.45], color="black", lw=2, zorder=2)
            ax.add_patch(patches.Ellipse((x, 0.5), 0.55, 0.08, fc="#666666", ec="black", zorder=3))

    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.55, 1.35)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(r["robot"], fontsize=12, fontweight="bold", color="black", pad=2)
    texto = r["nombre"]
    if r.get("lema"):
        texto += f'\n"{r["lema"]}"'
    ax.text(0, -1.02, texto, ha="center", va="top", fontsize=8.5, style="italic")


# ---------------------------------------------------------------------

def main():
    estilo_star()
    robots, errores = cargar_participantes()

    for e in errores:
        print(f"[ERROR] {e}")
    if errores:
        sys.exit(f"\nHay {len(errores)} error(es) en 'participantes/'. Corrígelos y vuelve a ejecutar.")
    if not robots:
        sys.exit("[ERROR] No hay ningún participante todavía. Copia _plantilla.json.")

    filas = math.ceil(len(robots) / COLUMNAS)
    columnas = min(COLUMNAS, len(robots))
    fig, axes = plt.subplots(filas, columnas, figsize=(3.2 * columnas, 3.9 * filas), squeeze=False)

    for ax in axes.flat:
        ax.axis("off")
    for ax, r in zip(axes.flat, robots):
        dibujar_robot(ax, r)

    fig.suptitle(f"Galería de robots del equipo {config.EQUIPO}  ({len(robots)} participantes)",
                 fontsize=15, fontweight="bold", color=config.COLOR_PRINCIPAL)
    fig.tight_layout(rect=(0, 0.02, 1, 0.95))
    print(f"Robots en la galería: {', '.join(r['robot'] for r in robots)}")
    guardar_figura(fig, "06_galeria_robots")


if __name__ == "__main__":
    main()
