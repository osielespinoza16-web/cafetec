"""MÓDULO PEDIDOS — Equipo 3 · Día 1.

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
    """Actividad 1 · Día 1 — Crear pedido.

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
    # TODO: implementar (Actividad 1 · Día 1)
    raise NotImplementedError("Actividad 1 pendiente")


def listar_pedidos(repo, estado=None):
    """Actividad 2 · Día 1 — Listar pedidos.

      - estado: si es None o "", regresa todos. Si trae valor, debe estar
        en ESTADOS (si no -> ValueError) y solo regresa esos pedidos.
    Orden: del más reciente al más antiguo (id mayor primero).
    A cada pedido le agrega dos llaves:
      "cliente": el nombre del usuario que hizo el pedido
      "piezas":  la suma de las cantidades de todos sus items
    """
    # TODO: implementar (Actividad 2 · Día 1)
    raise NotImplementedError("Actividad 2 pendiente")


def cambiar_estado_pedido(repo, pedido_id, nuevo_estado):
    """Actividad 3 · Día 1 — Avanzar el estado de un pedido.

      - Si el pedido no existe -> ValueError.
      - nuevo_estado debe estar en ESTADOS -> si no, ValueError.
      - Solo se permite pasar a los estados que indica
        TRANSICIONES[estado_actual]; cualquier otro cambio -> ValueError.
        (pendiente -> preparando o cancelado; preparando -> listo o
        cancelado; listo -> entregado; entregado y cancelado ya no cambian)
    Regresa el pedido actualizado (el dict que regresa repo.actualizar).
    """
    # TODO: implementar (Actividad 3 · Día 1)
    raise NotImplementedError("Actividad 3 pendiente")
