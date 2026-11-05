# curso_basico_git

Repositorio temporal del **curso básico de Git y GitHub** del equipo **STAR** (Student Team of Advanced Robotics).
Sirve para que los asistentes hagan pruebas en un entorno controlado. Al acabar el curso se borrará.

El repositorio contiene pequeños scripts de Python con temática de robótica que **generan imágenes**.
Así cada cambio que hagas se *ve*, y es fácil comparar versiones, revisar Pull Requests y entender los conflictos.

## Puesta en marcha

```bash
git clone https://github.com/star-uma/curso_basico_git.git
cd curso_basico_git

python -m venv .venv
# Windows:      .venv\Scripts\activate
# Linux / Mac:  source .venv/bin/activate

pip install -r requirements.txt
python run_all.py
```

Las imágenes se guardan en la carpeta `output/` (que **no** se sube a GitHub, ver `.gitignore`).
Para abrir una ventana con la gráfica añade `--show`:

```bash
python pruebas/01_trayectoria/trayectoria.py --show
```

## Pruebas

| # | Prueba | Qué se ve | Qué se modifica | Práctica de Git |
|---|--------|-----------|-----------------|-----------------|
| 01 | [Trayectoria](pruebas/01_trayectoria) | Camino de un robot diferencial | Lista de órdenes | Primer commit, `diff`, historial |
| 02 | [Brazo robótico](pruebas/02_brazo_robotico) | Brazo de 2 GDL, espacio de trabajo, IK | Longitudes y ángulos | Issues, `revert` |
| 03 | [Sensor LIDAR](pruebas/03_sensor_lidar) | Rayos láser en una sala | Obstáculos y sensor | `stash`, ramas en paralelo |
| 04 | [Planificador A*](pruebas/04_planificador_ruta) | Ruta más corta en un laberinto | `mapa.txt` | **Conflictos**, `blame` |
| 05 | [Control PID](pruebas/05_control_pid) | Respuesta de varios ajustes PID | Ganancias | Code review, sugerencias |
| 06 | [Galería de robots](pruebas/06_galeria_robots) | Un robot por participante | Tu propio `.json` | **Primer Pull Request**, CI |

## Estructura

```
curso_basico_git/
├── star/                  # código común: colores, estilo y guardado de imágenes
│   └── config.py          # configuración del equipo (¡cambiarla afecta a todas las imágenes!)
├── pruebas/
│   ├── 01_trayectoria/
│   ├── 02_brazo_robotico/
│   ├── 03_sensor_lidar/
│   ├── 04_planificador_ruta/
│   ├── 05_control_pid/
│   └── 06_galeria_robots/
│       └── participantes/ # aquí cada uno añade su robot
├── .github/               # plantillas de issues / PR y GitHub Actions
├── run_all.py             # ejecuta todas las pruebas
└── requirements.txt
```

Cada script tiene arriba una sección **PARÁMETROS** con lo que se puede modificar sin miedo.

## Normas del repo durante el curso

- No se trabaja directamente sobre `main`: **crea una rama** para cada cambio.
- Todo entra en `main` mediante un **Pull Request** revisado por otra persona.
- Nombres de rama: `tipo/usuario-descripcion`, por ejemplo `galeria/pepe-robot` o `fix/ana-mapa`.
- Mensajes de commit cortos y en imperativo: *"Añade obstáculo en la sala"*.
- No subas la carpeta `output/` ni archivos generados.
