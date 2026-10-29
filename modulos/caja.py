"""MÓDULO CAJA — Equipo 4.

Cada función tiene su especificación en el docstring. Implementa solo
el cuerpo; no cambies el nombre ni los parámetros, porque la app y las
pruebas dependen de ellos.

Datos de un pago (ticket):
    {"id": 1, "pedido_id": 4, "metodo": "efectivo", "total": 73.0,
     "recibido": 80.0, "cambio": 7.0, "fecha": "2026-10-28"}

Los pedidos tienen una lista "items"; cada item trae producto_id,
cantidad y precio_unitario (ver modulos/pedidos.py).
Para errores de validación lanza ValueError("mensaje claro").
"""

from nucleo.config import METODOS_PAGO
from nucleo.utilidades import a_fecha, hoy_o, total_de_items


def calcular_total(repo, pedido_id):
    """Actividad 1 — Total de un pedido.

      - Si el pedido no existe -> ValueError.
    Regresa la suma de precio_unitario * cantidad de todos sus items,
    redondeada a 2 decimales (float). Tip: total_de_items() ya lo hace.
    """
    # TODO: implementar (Actividad 1)
    raise NotImplementedError("Actividad 1 pendiente")


def cobrar_pedido(repo, pedido_id, metodo, recibido=None, hoy=None):
    """Actividad 2 — Cobrar un pedido.

    Reglas (si alguna falla, lanza ValueError y NO guarda nada):
      - El pedido debe existir.
      - No puede estar ya pagado (pagado True) ni en estado "cancelado".
      - metodo debe estar en METODOS_PAGO ("efectivo" o "tarjeta").
      - Si es "efectivo": recibido puede llegar como texto ("100");
        conviértelo a float. Debe ser mayor o igual al total del pedido.
        Si no es un número, también es ValueError.
        cambio = recibido - total.
      - Si es "tarjeta": se ignora `recibido`; recibido = total y cambio = 0.0.
    Guarda en "pagos" el registro con pedido_id, metodo, total, recibido,
    cambio (los tres montos redondeados a 2 decimales) y "fecha" = hoy en
    texto "AAAA-MM-DD"; después marca el pedido con "pagado": True.
    Regresa el ticket completo: el dict del pago INCLUYENDO su "id".
    """
    # TODO: implementar (Actividad 2)
    raise NotImplementedError("Actividad 2 pendiente")


def corte_de_caja(repo, fecha):
    """Actividad 3 — Corte de caja del día.

    `fecha` puede llegar como texto "AAAA-MM-DD" o como date.
    Toma los pagos cuya "fecha" sea esa fecha y regresa un dict:
        {"fecha": "AAAA-MM-DD", "num_pagos": 3,
         "efectivo": 148.0, "tarjeta": 120.0, "total": 268.0}
    "efectivo" y "tarjeta" suman el total de los pagos de cada método;
    "total" es la suma de los dos. Montos redondeados a 2 decimales.
    Si no hubo pagos ese día, todo va en 0 (y "fecha" igual se llena).
    """
    # TODO: implementar (Actividad 3)
    raise NotImplementedError("Actividad 3 pendiente")
