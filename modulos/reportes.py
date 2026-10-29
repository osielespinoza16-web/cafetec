"""MÓDULO REPORTES — Equipo 6.

Cada función tiene su especificación en el docstring. Implementa solo
el cuerpo; no cambies el nombre ni los parámetros, porque la app y las
pruebas dependen de ellos.

Los reportes leen los pedidos directamente del repositorio:
    {"id": 4, "usuario_id": 2,
     "items": [{"producto_id": 2, "cantidad": 1, "precio_unitario": 38.0}, ...],
     "estado": "entregado", "fecha": "2026-10-28",
     "pagado": True, "inventario_descontado": True}

Una VENTA es un pedido con "pagado": True.
Para errores de validación lanza ValueError("mensaje claro").
"""

from nucleo.config import ESTADOS
from nucleo.utilidades import a_fecha, normalizar, total_de_items


def ventas_del_dia(repo, fecha):
    """Actividad 1 — Ventas de un día.

    `fecha` puede llegar como texto "AAAA-MM-DD" o como date.
    Toma los pedidos pagados cuya "fecha" sea esa fecha y regresa:
        {"fecha": "AAAA-MM-DD", "pedidos": 3, "total": 268.0}
    "total" es la suma de los totales de esos pedidos (total_de_items),
    redondeada a 2 decimales. Si no hubo ventas, pedidos 0 y total 0.0.
    """
    fecha = a_fecha(fecha).isoformat()
    pedidos = repo.filtrar("pedidos", lambda p: p["pagado"] and p["fecha"] == fecha)
    total = round(sum(total_de_items(p["items"]) for p in pedidos), 2)
    return {"fecha": fecha, "pedidos": len(pedidos), "total": total}


def productos_mas_vendidos(repo, limite=3):
    """Actividad 2 — Productos más vendidos.

      - limite puede llegar como texto ("5"); conviértelo a int. Debe ser
        1 o mayor. Si no es un entero o es menor que 1 -> ValueError.
    Suma las cantidades vendidas de cada producto en los pedidos pagados.
    Regresa una lista de dicts {"producto_id", "nombre", "cantidad"}
    ordenada de la cantidad mayor a la menor; si empatan, por nombre
    (normalizado). Regresa como máximo `limite` elementos.
    """
    # TODO: implementar (Actividad 2)
    raise NotImplementedError("Actividad 2 pendiente")


def resumen_por_estado(repo):
    """Actividad 3 — Pedidos por estado.

    Regresa un dict con TODOS los estados de ESTADOS, en ese mismo orden,
    y cuántos pedidos (pagados o no) hay en cada uno. Los estados sin
    pedidos van con 0. Ejemplo:
        {"pendiente": 3, "preparando": 1, "listo": 1,
         "entregado": 3, "cancelado": 2}
    """
    # TODO: implementar (Actividad 3)
    raise NotImplementedError("Actividad 3 pendiente")
