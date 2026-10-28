"""MÓDULO USUARIOS — Equipo 1 · Día 1.

Cada función tiene su especificación en el docstring. Implementa solo
el cuerpo; no cambies el nombre ni los parámetros, porque la app y las
pruebas dependen de ellos.

Datos de un usuario:
    {"id": 1, "nombre": "Ana Torres", "correo": "ana.torres@cafetec.mx",
     "rol": "admin", "activo": True}

Para errores de validación lanza ValueError("mensaje claro").
"""

from nucleo.config import ROLES
from nucleo.utilidades import normalizar


def listar_usuarios(repo, solo_activos=False):
    """Actividad 1 · Día 1 — Listar usuarios.

    Regresa los usuarios ordenados por nombre (sin importar mayúsculas
    ni acentos; usa normalizar()).
      - Si solo_activos es True, regresa solo los que tienen activo True.
    A cada usuario le agrega la llave "estado" con el texto "Activo"
    si activo es True, o "Inactivo" si es False.
    """
    # TODO: implementar (Actividad 1 · Día 1)
    raise NotImplementedError("Actividad 1 pendiente")


def registrar_usuario(repo, nombre, correo, rol="cliente"):
    """Actividad 2 · Día 1 — Registrar usuario con validación.

    Reglas (si alguna falla, lanza ValueError):
      - nombre no puede quedar vacío (después de quitar espacios).
      - correo: se le quitan los espacios de los extremos y se pasa a
        minúsculas. Debe tener exactamente un "@", con texto antes, y la
        parte después del "@" debe tener un "." que no esté ni al inicio
        ni al final  ("ana@cafetec.mx" sí, "ana@mx", "ana@.mx" y "@cafetec.mx" no).
      - No puede existir otro usuario con el mismo correo (compara ya
        limpio y en minúsculas).
      - rol: debe estar en ROLES ("cliente" o "admin").
    Guarda el usuario con el nombre sin espacios en los extremos, el
    correo limpio, el rol y "activo": True.
    Regresa el id asignado.
    """
    # TODO: implementar (Actividad 2 · Día 1)
    raise NotImplementedError("Actividad 2 pendiente")


def cambiar_estado_usuario(repo, usuario_id, activo):
    """Actividad 3 · Día 1 — Activar o desactivar un usuario.

      - Si el usuario no existe -> ValueError.
      - No se puede desactivar (activo=False) al ÚLTIMO admin activo:
        la cafetería siempre necesita al menos un admin -> ValueError.
      - Desactivar a un cliente, o a un admin cuando hay otro admin
        activo, sí se puede. Activar siempre se puede.
    Regresa el usuario actualizado (el dict que regresa repo.actualizar).
    """
    # TODO: implementar (Actividad 3 · Día 1)
    raise NotImplementedError("Actividad 3 pendiente")
