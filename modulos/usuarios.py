"""MÓDULO USUARIOS — Equipo 1.

Cada función tiene su especificación en el docstring. Implementa solo
el cuerpo; no cambies el nombre ni los parámetros, porque la app y las
pruebas dependen de ellos.

Datos de un usuario:
    {"id": 1, "nombre": "Ana Torres", "correo": "ana.torres@cafetec.mx",
     "rol": "admin", "activo": True}

Para errores de validación lanza ValueError("mensaje claro").
"""

from nucleo.utilidades import normalizar


def listar_usuarios(repo, solo_activos=False):
    """Actividad 1 — Listar usuarios.

    Regresa los usuarios ordenados por nombre (sin importar mayúsculas
    ni acentos; usa normalizar()).
      - Si solo_activos es True, regresa solo los que tienen activo True.
    A cada usuario le agrega la llave "estado" con el texto "Activo"
    si activo es True, o "Inactivo" si es False.
    """
    usuarios = repo.listar("usuarios")
    if solo_activos:
        usuarios = [u for u in usuarios if u["activo"] is True]

    for usuario in usuarios:
        usuario["estado"] = "Activo" if usuario["activo"] is True else "Inactivo"

    return sorted(usuarios, key=lambda u: normalizar(u["nombre"]))
