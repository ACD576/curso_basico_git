# 05 · Ajuste de un controlador PID

El robot debe avanzar 1 m exactos. Se comparan varios ajustes `(Kp, Ki, Kd)` y se calculan
sobreoscilación, tiempo de establecimiento y error final.

```bash
python pruebas/05_control_pid/pid.py
```

**Qué tocar:** el diccionario `AJUSTES` (añade tu ajuste en una línea nueva) y los parámetros físicos.

**Reto:** consigue menos de un 5 % de sobreoscilación y menos de 3 s de establecimiento.

**Práctica de Git asociada:** conflicto "suave" (dos personas añaden una línea al final del mismo bloque),
revisión de código con sugerencias en el Pull Request.
