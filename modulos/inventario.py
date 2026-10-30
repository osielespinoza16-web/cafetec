"""MÓDULO INVENTARIO — Equipo 5.

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
    """Actividad 1 — Registrar entrada de mercancía.

      - Si el producto no existe -> ValueError.
      - cantidad puede llegar como texto ("12"); conviértela a int.
        Debe ser mayor que 0. Si no es un número entero -> ValueError.
    Suma la cantidad al stock del producto (repo.actualizar).
    Regresa el stock nuevo (int).
    """
    # 1. Validar y convertir la cantidad
    try:
        cantidad = int(cantidad)
    except (ValueError, TypeError):
        raise ValueError("La cantidad debe ser un entero")

    if cantidad <= 0:
        raise ValueError("La cantidad debe ser mayor a 0")

    # 2. Verificar que el producto exista
    producto = repo.obtener("productos", producto_id)
    if not producto:
        raise ValueError("El producto no existe")

    # 3. Sumar al stock y actualizar
    stock_nuevo = producto["stock"] + cantidad
    repo.actualizar("productos", producto_id, {"stock": stock_nuevo})

    # 4. Regresar el nuevo stock
    return stock_nuevo


def descontar_pedido(repo, pedido_id):
    """Actividad 2 — Descontar del inventario lo que lleva un pedido.

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
    """Actividad 2 — Descontar del inventario lo que lleva un pedido."""
    # 1. Obtener y validar que el pedido exista
    pedido = repo.obtener("pedidos", pedido_id)
    if not pedido:
        raise ValueError("El pedido no existe")

    # 2. Validar estado y si ya fue descontado
    if pedido.get("estado") == "cancelado":
        raise ValueError("El pedido está cancelado")
    
    if pedido.get("inventario_descontado") is True:
        raise ValueError("El inventario de este pedido ya fue descontado")

    items = pedido.get("items", [])
    if not items:
        raise ValueError("El pedido no contiene items")

    # 3. Validar stock de TODOS los productos primero (sin modificar nada todavía)
    stocks_actualizados = {}
    for item in items:
        prod_id = item.get("producto_id")
        cantidad_requerida = item.get("cantidad", 0)

        producto = repo.obtener("productos", prod_id)
        if not producto:
            raise ValueError(f"El producto con ID {prod_id} no existe")

        stock_actual = producto.get("stock", 0)
        if stock_actual < cantidad_requerida:
            raise ValueError(f"Stock insuficiente para el producto {prod_id}")

        stocks_actualizados[prod_id] = stock_actual - cantidad_requerida

    # 4. Si todo pasó la validación, aplicar los cambios
    for prod_id, stock_nuevo in stocks_actualizados.items():
        repo.actualizar("productos", prod_id, {"stock": stock_nuevo})

    # 5. Marcar el pedido como inventario descontado
    repo.actualizar("pedidos", pedido_id, {"inventario_descontado": True})

    # 6. Regresar el diccionario con los stocks nuevos
    return stocks_actualizados


def productos_stock_bajo(repo):
    """Actividad 3 — Alerta de stock bajo.

    Regresa los productos cuyo stock es MENOR O IGUAL a su stock_minimo
    (incluye también los no disponibles).
    Orden: del stock más bajo al más alto; si empatan, por nombre (normalizado).
    A cada producto le agrega la llave "faltante" = stock_minimo - stock
    (cuántas piezas faltan para llegar al mínimo; puede ser 0).
    """
    """Actividad 3 — Alerta de stock bajo.

    Regresa los productos cuyo stock es MENOR O IGUAL a su stock_minimo
    (incluye también los no disponibles).
    Orden: del stock más bajo al más alto; si empatan, por nombre (normalizado).
    A cada producto le agrega la llave "faltante" = stock_minimo - stock
    (cuántas piezas faltan para llegar al mínimo; puede ser 0).
    """
    productos = repo.listar("productos")
    resultado = []

    for p in productos:
        stock = p.get("stock", 0)
        stock_minimo = p.get("stock_minimo", 0)

        if stock <= stock_minimo:
            # Creamos una copia para no alterar el diccionario original de la base de datos
            prod_copia = dict(p)
            prod_copia["faltante"] = stock_minimo - stock
            resultado.append(prod_copia)

    # Ordenar: primero por stock (ascendente), luego por nombre normalizado
    resultado.sort(key=lambda p: (p.get("stock", 0), normalizar(p.get("nombre", ""))))

    return resultado
