"""Pruebas del módulo CATÁLOGO (Equipo 2). NO MODIFICAR.
El nombre test_fN_... indica la actividad (N) que se está probando."""

import pytest

from modulos.catalogo import agregar_producto, cambiar_precio, listar_menu


def ids(lista):
    return [x["id"] for x in lista]


# ------------------------------------------------------------ Actividad 1
def test_f1_solo_disponibles(repo):
    menu = listar_menu(repo)
    assert len(menu) == 11, "Hay 12 productos y 1 no está disponible: deben salir 11"
    assert 7 not in ids(menu), "'Chilaquiles' no está disponible y no debe salir"


def test_f1_orden_por_categoria_y_nombre(repo):
    assert ids(listar_menu(repo)) == [4, 1, 2, 3, 5, 8, 6, 10, 9, 12, 11], \
        "Orden: Bebidas, Comidas, Postres, Snacks (como en CATEGORIAS) y dentro de cada una por nombre"


def test_f1_orden_ignora_acentos(repo):
    repo.agregar("productos", {"nombre": "Ácido de frutas", "categoria": "Bebidas", "precio": 20.0,
                               "disponible": True, "stock": 5, "stock_minimo": 5})
    bebidas = [p["nombre"] for p in listar_menu(repo, "Bebidas")]
    assert bebidas[:2] == ["Ácido de frutas", "Agua natural"], "'Ácido' va antes de 'Agua' (orden sin acentos, usa normalizar)"


def test_f1_filtra_por_categoria(repo):
    assert ids(listar_menu(repo, "Postres")) == [10, 9], "Postres: Galleta de avena y Pay de queso"


def test_f1_categoria_vacia_no_filtra(repo):
    assert len(listar_menu(repo, "")) == 11, "categoria '' o None no filtra"


def test_f1_categoria_invalida(repo):
    with pytest.raises(ValueError):
        listar_menu(repo, "Licores")


# ------------------------------------------------------------ Actividad 2
def test_f2_agrega_y_regresa_id(repo):
    nuevo_id = agregar_producto(repo, "Té chai", "Bebidas", 42)
    assert nuevo_id == 13, "Debe regresar el id que asigna repo.agregar()"
    p = repo.obtener("productos", nuevo_id)
    assert p is not None, "El producto no se guardó en el repositorio"
    assert p["disponible"] is True and p["stock"] == 0 and p["stock_minimo"] == 5, \
        "Nace disponible, con stock 0 y stock_minimo = STOCK_MINIMO"


def test_f2_limpia_nombre_y_convierte_precio(repo):
    nuevo_id = agregar_producto(repo, "  Té chai ", "Bebidas", "42.456")
    p = repo.obtener("productos", nuevo_id)
    assert p["nombre"] == "Té chai", "Nombre sin espacios en los extremos"
    assert p["precio"] == 42.46 and isinstance(p["precio"], float), "Precio como float con 2 decimales"


@pytest.mark.parametrize("precio", [0, -5, 300.01, "abc", None, ""])
def test_f2_precio_invalido(repo, precio):
    with pytest.raises(ValueError):
        agregar_producto(repo, "Té chai", "Bebidas", precio)


def test_f2_precio_maximo_es_valido(repo):
    nuevo_id = agregar_producto(repo, "Pastel completo", "Postres", 300)
    assert repo.obtener("productos", nuevo_id)["precio"] == 300.0, "300 es un precio válido"


def test_f2_nombre_duplicado(repo):
    with pytest.raises(ValueError):
        agregar_producto(repo, "  cafe AMERICANO", "Bebidas", 20)


def test_f2_nombre_vacio(repo):
    with pytest.raises(ValueError):
        agregar_producto(repo, "   ", "Bebidas", 20)


def test_f2_categoria_invalida(repo):
    with pytest.raises(ValueError):
        agregar_producto(repo, "Cerveza", "Licores", 40)
    assert len(repo.listar("productos")) == 12, "Si hay error no se debe guardar nada"


# ------------------------------------------------------------ Actividad 3
def test_f3_cambia_precio(repo):
    p = cambiar_precio(repo, 1, 27)
    assert p["precio"] == 27.0, "Debe regresar el producto actualizado"
    assert repo.obtener("productos", 1)["precio"] == 27.0, "El cambio debe guardarse con repo.actualizar"


def test_f3_precio_como_texto(repo):
    assert cambiar_precio(repo, 2, "39.999")["precio"] == 40.0, "Convierte el texto y redondea a 2 decimales"


def test_f3_producto_inexistente(repo):
    with pytest.raises(ValueError):
        cambiar_precio(repo, 99, 20)


@pytest.mark.parametrize("precio", [0, -1, 301, "veinte"])
def test_f3_precio_invalido(repo, precio):
    with pytest.raises(ValueError):
        cambiar_precio(repo, 1, precio)
    assert repo.obtener("productos", 1)["precio"] == 25.0, "Si hay error el precio no cambia"
