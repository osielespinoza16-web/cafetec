"""MÓDULO CATÁLOGO (MENÚ) — Equipo 2 · Día 1.

Cada función tiene su especificación en el docstring. Implementa solo
el cuerpo; no cambies el nombre ni los parámetros, porque la app y las
pruebas dependen de ellos.

Datos de un producto:
    {"id": 1, "nombre": "Café americano", "categoria": "Bebidas",
     "precio": 25.0, "disponible": True, "stock": 40, "stock_minimo": 10}

(stock y stock_minimo los maneja el Equipo 5 · Inventario; aquí solo
los inicializas al crear un producto.)
Para errores de validación lanza ValueError("mensaje claro").
"""

from nucleo.config import CATEGORIAS, PRECIO_MAXIMO, STOCK_MINIMO
from nucleo.utilidades import normalizar
from pruebas.conftest import repo

def _precio_valido(precio):
    if precio is None or isinstance(precio, bool):
        raise ValueError("El precio debe ser un número válido")

    try:
        precio_float = float(precio)
    except (TypeError, ValueError):
        raise ValueError("El precio debe ser un número")

    if precio_float <= 0 or precio_float > PRECIO_MAXIMO:
        raise ValueError(f"El precio debe ser mayor que 0 y máximo {PRECIO_MAXIMO}")

    return round(precio_float, 2)

    if not isinstance(nombre, str):
        raise ValueError("El nombre debe ser una cadena de texto")

def listar_menu(repo, categoria=None):
    """Actividad 1 · Día 1 — Menú del día.

    Regresa solo los productos con disponible True.
      - categoria: si es None o "", no filtra. Si trae valor, debe estar
        en CATEGORIAS (si no -> ValueError) y solo regresa esos productos.
    Orden: primero por categoría, en el MISMO orden en que aparecen en
    CATEGORIAS (Bebidas, Comidas, Postres, Snacks); dentro de cada
    categoría, por nombre (normalizado).
    """
    if categoria and categoria not in CATEGORIAS:
        raise ValueError(f"Categoría inválida: {categoria}")
    menu = repo.filtrar("productos", lambda p: p["disponible"] and (not categoria or p["categoria"] == categoria))

    return sorted(menu, key=lambda p: (CATEGORIAS.index(p["categoria"]), normalizar(p["nombre"])))

    # TODO: implementar (Actividad 1 · Día 1)
    raise NotImplementedError("Actividad 1 pendiente")


def agregar_producto(repo, nombre, categoria, precio):
    """Actividad 2 · Día 1 — Agregar producto con validación.

    Reglas (si alguna falla, lanza ValueError):
      - nombre no puede quedar vacío (después de quitar espacios).
      - No puede existir otro producto con el mismo nombre, sin importar
        mayúsculas ni acentos ("cafe AMERICANO" choca con "Café americano").
      - categoria: debe estar en CATEGORIAS.
      - precio: puede llegar como texto ("25.5"); conviértelo a float.
        Debe ser mayor que 0 y menor o igual a PRECIO_MAXIMO (300).
        Si no es un número, también es ValueError.
    Guarda el producto con: nombre sin espacios en los extremos,
    categoria, precio redondeado a 2 decimales, "disponible": True,
    "stock": 0 y "stock_minimo": STOCK_MINIMO.
    Regresa el id asignado.
    """
    
    nombre = nombre.strip()
    if not nombre:
        raise ValueError("El nombre es obligatorio")
    if repo.filtrar("productos", lambda p: normalizar(p["nombre"]) == normalizar(nombre)):
        raise ValueError("Ya existe un producto con ese nombre")
    if categoria not in CATEGORIAS:
        raise ValueError("Categoría inválida")
    precio = _precio_valido(precio)
    return repo.agregar(
        "productos",
        {
            "nombre": nombre,
            "categoria": categoria,
            "precio": precio,
            "disponible": True,
            "stock": 0,
            "stock_minimo": STOCK_MINIMO,
        },
    )

    # TODO: implementar (Actividad 2 · Día 1)
    raise NotImplementedError("Actividad 2 pendiente")


def cambiar_precio(repo, producto_id, nuevo_precio):
    """Actividad 3 · Día 1 — Cambiar el precio de un producto.

      - Si el producto no existe -> ValueError.
      - nuevo_precio se valida con las mismas reglas de agregar_producto
        (texto o número, > 0, <= PRECIO_MAXIMO, redondeado a 2 decimales).
    Regresa el producto actualizado (el dict que regresa repo.actualizar).
    """
    if repo.obtener("productos", producto_id) is None:
        raise ValueError("El producto no existe")
    return repo.actualizar("productos", producto_id, {"precio": _precio_valido(nuevo_precio)})

    # TODO: implementar (Actividad 3 · Día 1)
    raise NotImplementedError("Actividad 3 pendiente")
