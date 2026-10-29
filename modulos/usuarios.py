"""MÓDULO USUARIOS — Equipo 1.

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


def _correo_valido(correo):
    """Valida un correo siguiendo las reglas del ejercicio."""
    if correo is None:
        return False

    correo = str(correo).strip().lower()
    if not correo or correo.count("@") != 1:
        return False

    local, dominio = correo.split("@", 1)
    if not local or not dominio:
        return False
    if dominio.startswith(".") or dominio.endswith(".") or "." not in dominio:
        return False
    return True


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


def registrar_usuario(repo, nombre, correo, rol="cliente"):
    """Actividad 2 — Registrar usuario con validación.

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
    nombre_limpio = str(nombre).strip()
    if not nombre_limpio:
        raise ValueError("El nombre no puede quedar vacío")

    correo_limpio = str(correo).strip().lower()
    if not _correo_valido(correo_limpio):
        raise ValueError("Correo inválido")

    if any(u["correo"].strip().lower() == correo_limpio for u in repo.listar("usuarios")):
        raise ValueError("Ya existe un usuario con ese correo")

    if rol not in ROLES:
        raise ValueError("Rol inválido")

    usuario = {
        "nombre": nombre_limpio,
        "correo": correo_limpio,
        "rol": rol,
        "activo": True,
    }
    return repo.agregar("usuarios", usuario)


def cambiar_estado_usuario(repo, usuario_id, activo):
    """Actividad 3 — Activar o desactivar un usuario.

      - Si el usuario no existe -> ValueError.
      - No se puede desactivar (activo=False) al ÚLTIMO admin activo:
        la cafetería siempre necesita al menos un admin -> ValueError.
      - Desactivar a un cliente, o a un admin cuando hay otro admin
        activo, sí se puede. Activar siempre se puede.
    Regresa el usuario actualizado (el dict que regresa repo.actualizar).
    """
    usuario = repo.obtener("usuarios", usuario_id)
    if usuario is None:
        raise ValueError("Usuario no encontrado")

    if activo is False and usuario.get("rol") == "admin":
        admins_activos = [
            u for u in repo.listar("usuarios")
            if u["rol"] == "admin" and u["activo"] is True and u["id"] != usuario_id
        ]
        if not admins_activos:
            raise ValueError("No se puede desactivar al último admin activo")

    return repo.actualizar("usuarios", usuario_id, {"activo": bool(activo)})
