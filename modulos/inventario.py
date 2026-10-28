"""MÓDULO INVENTARIO — Equipo 5 · Día 2.

Cada función tiene su especificación en el docstring. Implementa solo
el cuerpo; no cambies el nombre ni los parámetros, porque la app y las
pruebas dependen de ellos.

Cada producto trae dos campos de inventario:
    {"id": 2, "nombre": "Capuchino", ..., "stock": 8, "stock_minimo": 10}

Los pedidos tienen una lista "items"; cada item trae producto_id y
cantidad (ver modulos/pedidos.py), y la llave "inventario_descontado".
Para errores de validación lanza ValueError("mensaje claro").
"""

from nucleo.utilidades import normalizar


def registrar_entrada(repo, producto_id, cantidad):
    """Actividad 1 · Día 2 — Registrar entrada de mercancía.

      - Si el producto no existe -> ValueError.
      - cantidad puede llegar como texto ("12"); conviértela a int.
        Debe ser mayor que 0. Si no es un número entero -> ValueError.
    Suma la cantidad al stock del producto (repo.actualizar).
    Regresa el stock nuevo (int).
    """
    # TODO: implementar (Actividad 1 · Día 2)
    raise NotImplementedError("Actividad 1 pendiente")


def descontar_pedido(repo, pedido_id):
    """Actividad 2 · Día 2 — Descontar del inventario lo que lleva un pedido.

    Reglas (si alguna falla, lanza ValueError y NO cambia ningún stock):
      - El pedido debe existir.
      - No puede estar en estado "cancelado".
      - No puede tener ya "inventario_descontado": True.
      - Debe alcanzar el stock de TODOS sus productos. Si a uno solo le
        falta, no se descuenta nada (valida todo primero, guarda después).
    Resta la cantidad de cada item al stock de su producto y marca el
    pedido con "inventario_descontado": True.
    Regresa un dict {producto_id: stock_nuevo} con los productos del pedido.
    """
    # TODO: implementar (Actividad 2 · Día 2)
    raise NotImplementedError("Actividad 2 pendiente")


def productos_stock_bajo(repo):
    """Actividad 3 · Día 2 — Alerta de stock bajo.

    Regresa los productos cuyo stock es MENOR O IGUAL a su stock_minimo
    (incluye también los no disponibles).
    Orden: del stock más bajo al más alto; si empatan, por nombre (normalizado).
    A cada producto le agrega la llave "faltante" = stock_minimo - stock
    (cuántas piezas faltan para llegar al mínimo; puede ser 0).
    """
    # TODO: implementar (Actividad 3 · Día 2)
    raise NotImplementedError("Actividad 3 pendiente")
