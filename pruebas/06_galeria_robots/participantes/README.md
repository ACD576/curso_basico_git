# Participantes

Aquí cada persona añade **un único archivo** con su robot.

1. Copia `_plantilla.json` y llámalo con tu usuario de GitHub, por ejemplo `pepe-garcia.json`.
2. Rellena los campos:

| Campo      | Obligatorio | Valores posibles                                   |
|------------|-------------|----------------------------------------------------|
| `nombre`   | sí          | tu nombre                                          |
| `robot`    | sí          | el nombre de tu robot                              |
| `color`    | sí          | `"#RRGGBB"` o un nombre en inglés (`"tomato"`)     |
| `forma`    | no          | `cuadrado`, `circulo`, `triangulo`, `hexagono`     |
| `ojos`     | no          | `1`, `2` o `3` (número, sin comillas)              |
| `antena`   | no          | `true` o `false` (sin comillas)                    |
| `traccion` | no          | `ruedas`, `orugas`, `patas`, `helices`             |
| `lema`     | no          | frase de hasta 40 caracteres                       |

3. Comprueba que funciona: `python pruebas/06_galeria_robots/galeria.py`
4. Abre un Pull Request.

Los archivos que empiezan por `_` se ignoran.
