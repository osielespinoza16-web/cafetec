"""Pruebas del módulo INVENTARIO (Equipo 5). NO MODIFICAR.
El nombre test_fN_... indica la actividad (N) que se está probando."""

import pytest

from modulos.inventario import descontar_pedido, productos_stock_bajo, registrar_entrada


def stock(repo, producto_id):
    return repo.obtener("productos", producto_id)["stock"]


# ------------------------------------------------------------ Actividad 1
def test_f1_suma_y_regresa_stock(repo):
    assert registrar_entrada(repo, 2, 12) == 20, "Capuchino tenía 8; con 12 más quedan 20"
    assert stock(repo, 2) == 20, "El cambio debe guardarse con repo.actualizar"


def test_f1_cantidad_como_texto(repo):
    assert registrar_entrada(repo, 7, "3") == 3, "Convierte el texto a int"


def test_f1_producto_inexistente(repo):
    with pytest.raises(ValueError):
        registrar_entrada(repo, 99, 5)


@pytest.mark.parametrize("cantidad", [0, -4, "abc", "2.5", None])
def test_f1_cantidad_invalida(repo, cantidad):
    with pytest.raises(ValueError):
        registrar_entrada(repo, 2, cantidad)
    assert stock(repo, 2) == 8, "Si hay error el stock no cambia"


# ------------------------------------------------------------ Actividad 2
def test_f2_descuenta_y_regresa_stocks(repo):
    assert descontar_pedido(repo, 7) == {11: 24, 1: 39}, "Pedido 7: 1 papas (25->24) y 1 café (40->39)"
    assert stock(repo, 11) == 24 and stock(repo, 1) == 39, "Los cambios deben guardarse"


def test_f2_marca_el_pedido(repo):
    descontar_pedido(repo, 9)
    assert repo.obtener("pedidos", 9)["inventario_descontado"] is True


def test_f2_cantidades_mayores_a_uno(repo):
    assert descontar_pedido(repo, 9) == {10: 28, 3: 14}, "Pedido 9: 2 galletas (30->28) y 1 jugo (15->14)"


def test_f2_stock_insuficiente(repo):
    with pytest.raises(ValueError):
        descontar_pedido(repo, 8)  # 3 elotes y solo hay 2


def test_f2_no_descuenta_a_medias(repo):
    pid = repo.agregar("pedidos", {"usuario_id": 2, "estado": "pendiente", "fecha": "2026-10-28",
                                   "pagado": False, "inventario_descontado": False,
                                   "items": [{"producto_id": 1, "cantidad": 2, "precio_unitario": 25.0},
                                             {"producto_id": 12, "cantidad": 5, "precio_unitario": 32.0}]})
    with pytest.raises(ValueError):
        descontar_pedido(repo, pid)
    assert stock(repo, 1) == 40, "Si a un producto le falta stock, no se descuenta NINGUNO"
    assert repo.obtener("pedidos", pid)["inventario_descontado"] is False


@pytest.mark.parametrize("pedido_id", [1, 3, 99])
def test_f2_ya_descontado_cancelado_o_inexistente(repo, pedido_id):
    with pytest.raises(ValueError):
        descontar_pedido(repo, pedido_id)


# ------------------------------------------------------------ Actividad 3
def test_f3_productos_con_stock_bajo(repo):
    assert [p["id"] for p in productos_stock_bajo(repo)] == [7, 12, 4, 6, 2], \
        "Stock <= mínimo, del stock más bajo al más alto"


def test_f3_incluye_igual_al_minimo(repo):
    assert 6 in [p["id"] for p in productos_stock_bajo(repo)], "Torta: stock 5 y mínimo 5 también es stock bajo"


def test_f3_llave_faltante(repo):
    faltante = {p["id"]: p["faltante"] for p in productos_stock_bajo(repo)}
    assert faltante == {7: 3, 12: 3, 4: 7, 6: 0, 2: 2}, "faltante = stock_minimo - stock"


def test_f3_empate_por_nombre(repo):
    repo.actualizar("productos", 9, {"stock": 2})  # Pay de queso empata con Elote en vaso
    nombres = [p["nombre"] for p in productos_stock_bajo(repo)][:3]
    assert nombres == ["Chilaquiles", "Elote en vaso", "Pay de queso"], "Si empatan en stock, por nombre"


def test_f3_sin_stock_bajo(repo):
    for p in repo.listar("productos"):
        repo.actualizar("productos", p["id"], {"stock": 100})
    assert productos_stock_bajo(repo) == []
