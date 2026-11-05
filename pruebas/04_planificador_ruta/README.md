# 04 · Planificador de rutas A*

Lee el mapa de `mapa.txt` y busca la ruta más corta de `S` a `G`.

| Carácter | Significado |
|----------|-------------|
| `#` | muro |
| `.` | suelo libre |
| `~` | barro (se puede pasar, pero cuesta más) |
| `S` | salida (solo una) |
| `G` | meta (solo una) |

```bash
python pruebas/04_planificador_ruta/ruta.py
```

**Qué tocar:** sobre todo `mapa.txt`. También `DIAGONALES` y `COSTE_BARRO` en `ruta.py`.

**Práctica de Git asociada:** **conflictos de merge**. Dos personas editan las mismas filas del mapa
en ramas distintas. Si queda un conflicto sin resolver, el script lo detecta y avisa. También `git blame`
("¿quién puso este muro?").
