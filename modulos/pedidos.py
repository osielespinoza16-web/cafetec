"""MÓDULO PEDIDOS — Equipo 3.

Cada función tiene su especificación en el docstring. Implementa solo
el cuerpo; no cambies el nombre ni los parámetros, porque la app y las
pruebas dependen de ellos.

Datos de un pedido:
    {"id": 1, "usuario_id": 2,
     "items": [{"producto_id": 1, "cantidad": 2, "precio_unitario": 25.0}],
     "estado": "pendiente", "fecha": "2026-10-28",
     "pagado": False, "inventario_descontado": False}

(pagado lo cambia el Equipo 4 · Caja e inventario_descontado el
Equipo 5 · Inventario; aquí solo los inicializas en False.)
Para errores de validación lanza ValueError("mensaje claro").
"""

from nucleo.config import ESTADOS, MAX_POR_PRODUCTO, TRANSICIONES
from nucleo.utilidades import hoy_o


def crear_pedido(repo, usuario_id, items, hoy=None):
    """Actividad 1 — Crear pedido.

    `items` es una lista de dicts: [{"producto_id": 1, "cantidad": 2}, ...]
    Reglas (si alguna falla, lanza ValueError y NO guarda nada):
      - El usuario debe existir y tener activo True.
      - items no puede venir vacío.
      - Cada producto debe existir y tener disponible True.
      - Cada cantidad puede llegar como texto ("2"); conviértela a int.
        Debe estar entre 1 y MAX_POR_PRODUCTO (10). Si no es un número
        entero, también es ValueError.
    Guarda el pedido con: usuario_id, items (cada uno con producto_id,
    cantidad como int y precio_unitario = el precio ACTUAL del producto),
    "estado": "pendiente", "fecha": hoy en texto "AAAA-MM-DD",
    "pagado": False e "inventario_descontado": False.
    Regresa el id asignado.
    """
    usuario = repo.obtener("usuarios", usuario_id)
    if usuario is None or not usuario.get("activo"):
        raise ValueError("El usuario no existe o no está activo")
    if not items:
        raise ValueError("El pedido debe tener al menos un producto")

    items_validados = []
    for item in items:
        producto = repo.obtener("productos", item.get("producto_id"))
        if producto is None or not producto.get("disponible"):
            raise ValueError(f"El producto {item.get('producto_id')} no existe o no está disponible")
        try:
            cantidad = int(item.get("cantidad"))
        except (TypeError, ValueError):
            raise ValueError("La cantidad debe ser un número entero")
        if not 1 <= cantidad <= MAX_POR_PRODUCTO:
            raise ValueError(f"La cantidad debe estar entre 1 y {MAX_POR_PRODUCTO}")
        items_validados.append({
            "producto_id": producto["id"],
            "cantidad": cantidad,
            "precio_unitario": producto["precio"],
        })

    return repo.agregar("pedidos", {
        "usuario_id": usuario_id,
        "items": items_validados,
        "estado": "pendiente",
        "fecha": hoy_o(hoy).isoformat(),
        "pagado": False,
        "inventario_descontado": False,
    })


def listar_pedidos(repo, estado=None):
    """Actividad 2 — Listar pedidos.

      - estado: si es None o "", regresa todos. Si trae valor, debe estar
        en ESTADOS (si no -> ValueError) y solo regresa esos pedidos.
    Orden: del más reciente al más antiguo (id mayor primero).
    A cada pedido le agrega dos llaves:
      "cliente": el nombre del usuario que hizo el pedido
      "piezas":  la suma de las cantidades de todos sus items
    """
    # TODO: implementar (Actividad 2)
    raise NotImplementedError("Actividad 2 pendiente")


def cambiar_estado_pedido(repo, pedido_id, nuevo_estado):
    """Actividad 3 — Avanzar el estado de un pedido.

      - Si el pedido no existe -> ValueError.
      - nuevo_estado debe estar en ESTADOS -> si no, ValueError.
      - Solo se permite pasar a los estados que indica
        TRANSICIONES[estado_actual]; cualquier otro cambio -> ValueError.
        (pendiente -> preparando o cancelado; preparando -> listo o
        cancelado; listo -> entregado; entregado y cancelado ya no cambian)
    Regresa el pedido actualizado (el dict que regresa repo.actualizar).
    """
    # TODO: implementar (Actividad 3)
    raise NotImplementedError("Actividad 3 pendiente")
