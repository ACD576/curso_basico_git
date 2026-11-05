"""
Ejecuta todas las pruebas y guarda las imágenes en la carpeta output/.

    python run_all.py

Devuelve un código de error si alguna prueba falla (lo usa GitHub Actions).
"""

import subprocess
import sys
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parent

scripts = sorted(p for p in (RAIZ / "pruebas").glob("*/*.py") if not p.name.startswith("_"))
fallos = []

for script in scripts:
    nombre = script.relative_to(RAIZ).as_posix()
    print(f"\n=== {nombre} ===", flush=True)
    inicio = time.time()
    resultado = subprocess.run([sys.executable, str(script)], cwd=RAIZ)
    if resultado.returncode != 0:
        fallos.append(nombre)
        print(f"[FALLO] {nombre}", flush=True)
    else:
        print(f"({time.time() - inicio:.1f} s)", flush=True)

print("\n" + "=" * 50)
print(f"Pruebas correctas: {len(scripts) - len(fallos)}/{len(scripts)}")
for f in fallos:
    print(f"  - Falló: {f}")
print("Imágenes en la carpeta output/")

sys.exit(1 if fallos else 0)
