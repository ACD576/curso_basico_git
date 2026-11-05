"""Paquete común del curso de Git del equipo STAR."""

# Antes de nada: comprueba (e instala si hace falta) numpy y matplotlib
from .dependencias import comprobar as _comprobar

_comprobar()

from . import config  # noqa: E402
from .graficos import estilo_star, guardar_figura  # noqa: E402

__all__ = ["config", "estilo_star", "guardar_figura"]
