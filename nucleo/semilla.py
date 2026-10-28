"""Datos de ejemplo. Las fechas se calculan a partir de `hoy` para que
siempre haya ventas de hoy y de ayer. NO MODIFICAR."""

from datetime import date, timedelta


def datos_semilla(hoy=None):
    hoy = hoy or date.today()

    def dia(desplazamiento):
        return (hoy + timedelta(days=desplazamiento)).isoformat()

    # (id, nombre, correo, rol, activo)
    usuarios = [
        (1, "Ana Torres", "ana.torres@cafetec.mx", "admin", True),
        (2, "Bruno Díaz", "bruno.diaz@cafetec.mx", "cliente", True),
        (3, "Carla Méndez", "carla.mendez@cafetec.mx", "cliente", True),
        (4, "Diego Ramírez", "diego.ramirez@cafetec.mx", "cliente", False),
        (5, "Elena Ruiz", "elena.ruiz@cafetec.mx", "admin", True),
        (6, "Fernando Castillo", "fernando.castillo@cafetec.mx", "cliente", True),
        (7, "Gabriela Núñez", "gabriela.nunez@cafetec.mx", "cliente", True),
        (8, "Héctor Salinas", "hector.salinas@cafetec.mx", "cliente", False),
    ]

    # (id, nombre, categoria, precio, disponible, stock, stock_minimo)
    productos = [
        (1, "Café americano", "Bebidas", 25.0, True, 40, 10),
        (2, "Capuchino", "Bebidas", 38.0, True, 8, 10),
        (3, "Jugo de naranja", "Bebidas", 30.0, True, 15, 5),
        (4, "Agua natural", "Bebidas", 15.0, True, 3, 10),
        (5, "Burrito de deshebrada", "Comidas", 45.0, True, 20, 5),
        (6, "Torta de jamón", "Comidas", 50.0, True, 5, 5),
        (7, "Chilaquiles", "Comidas", 65.0, False, 0, 3),
        (8, "Ensalada César", "Comidas", 70.0, True, 12, 4),
        (9, "Pay de queso", "Postres", 35.0, True, 6, 4),
        (10, "Galleta de avena", "Postres", 18.0, True, 30, 10),
        (11, "Papas a la francesa", "Snacks", 28.0, True, 25, 8),
        (12, "Elote en vaso", "Snacks", 32.0, True, 2, 5),
    ]
    precios = {p[0]: p[3] for p in productos}

    # (id, usuario, [(producto, cantidad)], estado, dia, pagado, inventario_descontado)
    pedidos = [
        (1, 2, [(1, 2), (10, 1)], "entregado", -1, True, True),
        (2, 3, [(5, 1), (3, 1)], "entregado", -1, True, True),
        (3, 6, [(8, 1)], "cancelado", -1, False, False),
        (4, 2, [(2, 1), (9, 1)], "entregado", 0, True, True),
        (5, 7, [(5, 2), (4, 2)], "listo", 0, True, True),
        (6, 3, [(1, 1), (6, 1)], "preparando", 0, True, False),
        (7, 6, [(11, 1), (1, 1)], "pendiente", 0, False, False),
        (8, 7, [(12, 3)], "pendiente", 0, False, False),
        (9, 1, [(10, 2), (3, 1)], "pendiente", 0, False, False),
        (10, 2, [(5, 1)], "cancelado", 0, False, False),
    ]

    # (id, pedido, metodo, total, recibido, cambio, dia)
    pagos = [
        (1, 1, "efectivo", 68.0, 100.0, 32.0, -1),
        (2, 2, "tarjeta", 75.0, 75.0, 0.0, -1),
        (3, 4, "efectivo", 73.0, 80.0, 7.0, 0),
        (4, 5, "tarjeta", 120.0, 120.0, 0.0, 0),
        (5, 6, "efectivo", 75.0, 100.0, 25.0, 0),
    ]

    return {
        "usuarios": [
            {"id": i, "nombre": n, "correo": c, "rol": r, "activo": a}
            for i, n, c, r, a in usuarios
        ],
        "productos": [
            {"id": i, "nombre": n, "categoria": cat, "precio": pr, "disponible": d,
             "stock": st, "stock_minimo": mn}
            for i, n, cat, pr, d, st, mn in productos
        ],
        "pedidos": [
            {"id": i, "usuario_id": u,
             "items": [{"producto_id": p, "cantidad": c, "precio_unitario": precios[p]} for p, c in items],
             "estado": e, "fecha": dia(d), "pagado": pg, "inventario_descontado": inv}
            for i, u, items, e, d, pg, inv in pedidos
        ],
        "pagos": [
            {"id": i, "pedido_id": p, "metodo": m, "total": t, "recibido": r, "cambio": c, "fecha": dia(d)}
            for i, p, m, t, r, c, d in pagos
        ],
    }
