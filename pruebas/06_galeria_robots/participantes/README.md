# Participantes

Aquí cada persona añade **un único archivo** con su robot.

1. Copia `_plantilla.json` y llámalo con tu usuario de GitHub, por ejemplo `pepe-garcia.json`.
   (Activa en el Explorador de Windows *Ver → Mostrar → Extensiones de nombre de archivo*
   para no acabar con un `pepe-garcia.json.json`).
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

3. Comprueba que funciona: abre `galeria.py` en VS Code y pulsa ▶.
4. Haz commit en GitHub Desktop, publica la rama y abre un Pull Request.

Los archivos que empiezan por `_` se ignoran.
