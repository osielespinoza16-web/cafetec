"""Pruebas del módulo PEDIDOS (Equipo 3). NO MODIFICAR.
El nombre test_fN_... indica la actividad (N) que se está probando."""

import pytest

from modulos.pedidos import cambiar_estado_pedido, crear_pedido, listar_pedidos


def ids(lista):
    return [x["id"] for x in lista]


# ------------------------------------------------------------ Actividad 1
def test_f1_crea_y_regresa_id(repo, hoy):
    nuevo_id = crear_pedido(repo, 2, [{"producto_id": 1, "cantidad": 2}], hoy)
    assert nuevo_id == 11, "Debe regresar el id que asigna repo.agregar()"
    p = repo.obtener("pedidos", nuevo_id)
    assert p is not None, "El pedido no se guardó en el repositorio"
    assert p["usuario_id"] == 2


def test_f1_campos_iniciales(repo, hoy):
    p = repo.obtener("pedidos", crear_pedido(repo, 2, [{"producto_id": 1, "cantidad": 2}], hoy))
    assert p["estado"] == "pendiente", "Un pedido nuevo está 'pendiente'"
    assert p["fecha"] == "2026-10-28", "La fecha se guarda como texto AAAA-MM-DD (usa .isoformat())"
    assert p["pagado"] is False and p["inventario_descontado"] is False


def test_f1_items_con_precio_actual(repo, hoy):
    items = [{"producto_id": 1, "cantidad": "2"}, {"producto_id": 9, "cantidad": 1}]
    p = repo.obtener("pedidos", crear_pedido(repo, 3, items, hoy))
    assert p["items"] == [
        {"producto_id": 1, "cantidad": 2, "precio_unitario": 25.0},
        {"producto_id": 9, "cantidad": 1, "precio_unitario": 35.0},
    ], "Cada item lleva producto_id, cantidad (int) y precio_unitario del catálogo"


@pytest.mark.parametrize("usuario_id", [4, 99])
def test_f1_usuario_inactivo_o_inexistente(repo, hoy, usuario_id):
    with pytest.raises(ValueError):
        crear_pedido(repo, usuario_id, [{"producto_id": 1, "cantidad": 1}], hoy)


def test_f1_sin_items(repo, hoy):
    with pytest.raises(ValueError):
        crear_pedido(repo, 2, [], hoy)


@pytest.mark.parametrize("producto_id", [7, 99])
def test_f1_producto_no_disponible_o_inexistente(repo, hoy, producto_id):
    with pytest.raises(ValueError):
        crear_pedido(repo, 2, [{"producto_id": producto_id, "cantidad": 1}], hoy)


@pytest.mark.parametrize("cantidad", [0, 11, -1, "abc", "1.5", None])
def test_f1_cantidad_invalida(repo, hoy, cantidad):
    with pytest.raises(ValueError):
        crear_pedido(repo, 2, [{"producto_id": 1, "cantidad": cantidad}], hoy)


def test_f1_no_guarda_si_un_item_falla(repo, hoy):
    with pytest.raises(ValueError):
        crear_pedido(repo, 2, [{"producto_id": 1, "cantidad": 1}, {"producto_id": 7, "cantidad": 1}], hoy)
    assert len(repo.listar("pedidos")) == 10, "Si hay error no se debe guardar nada"


# ------------------------------------------------------------ Actividad 2
def test_f2_todos_del_mas_reciente(repo):
    assert ids(listar_pedidos(repo)) == [10, 9, 8, 7, 6, 5, 4, 3, 2, 1], "Orden: id mayor primero"


def test_f2_agrega_cliente_y_piezas(repo):
    por_id = {p["id"]: p for p in listar_pedidos(repo)}
    assert por_id[5]["cliente"] == "Gabriela Núñez", "'cliente' es el nombre del usuario"
    assert por_id[5]["piezas"] == 4, "El pedido 5 tiene 2 burritos + 2 aguas = 4 piezas"
    assert por_id[1]["piezas"] == 3


def test_f2_filtra_por_estado(repo):
    assert ids(listar_pedidos(repo, "pendiente")) == [9, 8, 7]
    assert ids(listar_pedidos(repo, "cancelado")) == [10, 3]


def test_f2_estado_vacio_no_filtra(repo):
    assert len(listar_pedidos(repo, "")) == 10


def test_f2_estado_invalido(repo):
    with pytest.raises(ValueError):
        listar_pedidos(repo, "perdido")


# ------------------------------------------------------------ Actividad 3
@pytest.mark.parametrize("pedido_id, nuevo", [(7, "preparando"), (7, "cancelado"), (6, "listo"),
                                              (6, "cancelado"), (5, "entregado")])
def test_f3_transiciones_validas(repo, pedido_id, nuevo):
    p = cambiar_estado_pedido(repo, pedido_id, nuevo)
    assert p["estado"] == nuevo, "Debe regresar el pedido actualizado"
    assert repo.obtener("pedidos", pedido_id)["estado"] == nuevo, "El cambio debe guardarse"


@pytest.mark.parametrize("pedido_id, nuevo", [(7, "listo"), (7, "entregado"), (5, "pendiente"),
                                              (1, "cancelado"), (3, "pendiente"), (6, "preparando")])
def test_f3_transiciones_no_permitidas(repo, pedido_id, nuevo):
    antes = repo.obtener("pedidos", pedido_id)["estado"]
    with pytest.raises(ValueError):
        cambiar_estado_pedido(repo, pedido_id, nuevo)
    assert repo.obtener("pedidos", pedido_id)["estado"] == antes, "Si hay error el estado no cambia"


def test_f3_estado_desconocido(repo):
    with pytest.raises(ValueError):
        cambiar_estado_pedido(repo, 7, "volando")


def test_f3_pedido_inexistente(repo):
    with pytest.raises(ValueError):
        cambiar_estado_pedido(repo, 99, "preparando")
