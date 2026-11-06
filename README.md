# curso_basico_git

Repositorio temporal del **curso básico de Git y GitHub** del equipo **STAR** (Student Team of Advanced Robotics).
Sirve para que los asistentes hagan pruebas en un entorno controlado. Al acabar el curso se borrará.

El repositorio contiene pequeños scripts de Python con temática de robótica que **generan imágenes**.
Así cada cambio que hagas se *ve*, y es fácil comparar versiones, revisar Pull Requests y entender los conflictos.

## Qué necesitas (Windows)

| Programa | Para qué |
|----------|----------|
| **GitHub Desktop** | Trabajar con Git sin usar la terminal |
| **Python 3.10 o superior** | Ejecutar las pruebas |
| **Visual Studio Code** + extensión **Python** | Editar archivos, ejecutar scripts y resolver conflictos |
| `numpy` y `matplotlib` | Librerías que usan los scripts |

Y una cuenta de GitHub.

**No hace falta instalarlo a mano:** [`instalar.bat`](instalar.bat) comprueba qué tienes y
instala lo que falte (sin permisos de administrador).

## Puesta en marcha

1. **Antes del curso**, abre [`instalar.bat`](instalar.bat) aquí en GitHub, pulsa el botón
   **Download raw file** (la flecha hacia abajo) y haz doble clic en el archivo descargado.
   - Si Windows muestra *"Windows protegió su PC"*, pulsa **Más información → Ejecutar de todas formas**.
   - Al final aparece un resumen: todo debe poner `OK`.
2. Abre GitHub Desktop: **File → Options → Accounts → Sign in** con tu cuenta de GitHub.
3. **File → Clone repository… → GitHub.com** → elige `star-uma/curso_basico_git` → **Clone**.
4. **Repository → Show in Explorer** y haz doble clic en `ejecutar_todo.bat`: ejecuta todas las
   pruebas y abre la carpeta `output/` con las imágenes.
5. Para trabajar: **Repository → Open in Visual Studio Code**. Abre cualquier script de `pruebas/`
   y pulsa ▶ (*Run Python File*). La imagen se guarda en `output/` y VS Code la puede mostrar.

Si algo falla, también puedes volver a ejecutar `instalar.bat` desde la carpeta del repositorio.

La carpeta `output/` **no** se sube a GitHub (está en `.gitignore`), por eso no aparece en GitHub Desktop.

> Consejo: clona el repositorio en una carpeta que **no** esté sincronizada con OneDrive
> (por ejemplo `C:\Users\<tu-usuario>\GitHub`), para evitar archivos bloqueados.

## Pruebas

| # | Prueba | Qué se ve | Qué se modifica | Práctica de Git |
|---|--------|-----------|-----------------|-----------------|
| 01 | [Trayectoria](pruebas/01_trayectoria) | Camino de un robot diferencial | Lista de órdenes | Primer commit, ver cambios |
| 02 | [Brazo robótico](pruebas/02_brazo_robotico) | Brazo de 2 GDL, espacio de trabajo, IK | Longitudes y ángulos | Issues, revertir commits |
| 03 | [Sensor LIDAR](pruebas/03_sensor_lidar) | Rayos láser en una sala | Obstáculos y sensor | Stash, ramas en paralelo |
| 04 | [Planificador A*](pruebas/04_planificador_ruta) | Ruta más corta en un laberinto | `mapa.txt` | **Conflictos**, Blame |
| 05 | [Control PID](pruebas/05_control_pid) | Respuesta de varios ajustes PID | Ganancias | Revisión de código |
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
├── instalar.bat           # doble clic: instala GitHub Desktop, Python, VS Code y librerías
├── ejecutar_todo.bat      # doble clic: ejecuta todas las pruebas
├── run_all.py
└── requirements.txt
```

Cada script tiene arriba una sección **PARÁMETROS** con lo que se puede modificar sin miedo.

## Normas del repo durante el curso

- No se trabaja directamente sobre `main`: **crea una rama** para cada cambio (*Current Branch → New Branch*).
- Todo entra en `main` mediante un **Pull Request** revisado por otra persona.
- Nombres de rama: `tipo/usuario-descripcion`, por ejemplo `galeria/pepe-robot` o `fix/ana-mapa`.
- Mensajes de commit cortos y en imperativo: *"Añade obstáculo en la sala"*.
- No subas la carpeta `output/` ni archivos generados.

Prueba de Push: Hola Adrián :D