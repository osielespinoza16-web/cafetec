"""Reglas de negocio compartidas por los seis módulos. NO MODIFICAR."""

# Usuarios (Equipo 1)
ROLES = ["cliente", "admin"]

# Catálogo (Equipo 2)
CATEGORIAS = ["Bebidas", "Comidas", "Postres", "Snacks"]   # también es el orden del menú
PRECIO_MAXIMO = 300.0        # pesos; ningún producto puede costar más
STOCK_MINIMO = 5             # stock mínimo con el que nace un producto nuevo

# Pedidos (Equipo 3)
ESTADOS = ["pendiente", "preparando", "listo", "entregado", "cancelado"]
TRANSICIONES = {             # a qué estados se puede pasar desde cada estado
    "pendiente": ["preparando", "cancelado"],
    "preparando": ["listo", "cancelado"],
    "listo": ["entregado"],
    "entregado": [],
    "cancelado": [],
}
MAX_POR_PRODUCTO = 10        # piezas máximas de un mismo producto en un pedido

# Caja (Equipo 4)
METODOS_PAGO = ["efectivo", "tarjeta"]
