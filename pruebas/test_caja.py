"""Pruebas del módulo CAJA (Equipo 4). NO MODIFICAR.
El nombre test_fN_... indica la actividad (N) que se está probando."""

import pytest

from modulos.caja import calcular_total, cobrar_pedido, corte_de_caja


# ------------------------------------------------------------ Actividad 1
@pytest.mark.parametrize("pedido_id, total", [(1, 68.0), (5, 120.0), (7, 53.0), (8, 96.0), (3, 70.0)])
def test_f1_total_del_pedido(repo, pedido_id, total):
    assert calcular_total(repo, pedido_id) == total


def test_f1_redondea_a_dos_decimales(repo):
    repo.actualizar("productos", 1, {"precio": 10.333})
    pid = repo.agregar("pedidos", {"usuario_id": 2, "items": [{"producto_id": 1, "cantidad": 3, "precio_unitario": 10.333}],
                                   "estado": "pendiente", "fecha": "2026-10-28", "pagado": False,
                                   "inventario_descontado": False})
    assert calcular_total(repo, pid) == 31.0, "10.333 × 3 = 30.999 -> 31.0"


def test_f1_pedido_inexistente(repo):
    with pytest.raises(ValueError):
        calcular_total(repo, 99)


# ------------------------------------------------------------ Actividad 2
def test_f2_cobra_en_efectivo(repo, hoy):
    t = cobrar_pedido(repo, 7, "efectivo", 100, hoy)
    assert t["id"] == 6, "El ticket debe incluir el id que asigna repo.agregar()"
    assert (t["pedido_id"], t["metodo"], t["total"], t["recibido"], t["cambio"]) == (7, "efectivo", 53.0, 100.0, 47.0)
    assert t["fecha"] == "2026-10-28", "La fecha va como texto AAAA-MM-DD"


def test_f2_guarda_pago_y_marca_pedido(repo, hoy):
    cobrar_pedido(repo, 7, "efectivo", 53, hoy)
    assert len(repo.listar("pagos")) == 6, "Debe guardar el pago en la colección 'pagos'"
    assert repo.obtener("pedidos", 7)["pagado"] is True, "El pedido debe quedar con pagado True"


def test_f2_recibido_como_texto(repo, hoy):
    t = cobrar_pedido(repo, 9, "efectivo", "70.50", hoy)
    assert t["recibido"] == 70.5 and t["cambio"] == 4.5, "Convierte el texto a float"


def test_f2_cobra_con_tarjeta(repo, hoy):
    t = cobrar_pedido(repo, 8, "tarjeta", None, hoy)
    assert (t["total"], t["recibido"], t["cambio"]) == (96.0, 96.0, 0.0), "Con tarjeta recibido = total y cambio 0"


def test_f2_tarjeta_ignora_recibido(repo, hoy):
    t = cobrar_pedido(repo, 8, "tarjeta", 500, hoy)
    assert t["recibido"] == 96.0 and t["cambio"] == 0.0


@pytest.mark.parametrize("pedido_id", [1, 3, 99])
def test_f2_ya_pagado_cancelado_o_inexistente(repo, hoy, pedido_id):
    with pytest.raises(ValueError):
        cobrar_pedido(repo, pedido_id, "tarjeta", None, hoy)


@pytest.mark.parametrize("recibido", [50, "50", "cien", None])
def test_f2_efectivo_insuficiente_o_invalido(repo, hoy, recibido):
    with pytest.raises(ValueError):
        cobrar_pedido(repo, 7, "efectivo", recibido, hoy)
    assert repo.obtener("pedidos", 7)["pagado"] is False and len(repo.listar("pagos")) == 5, \
        "Si hay error no se debe guardar nada"


def test_f2_metodo_invalido(repo, hoy):
    with pytest.raises(ValueError):
        cobrar_pedido(repo, 7, "bitcoin", 100, hoy)


# ------------------------------------------------------------ Actividad 3
def test_f3_corte_de_hoy(repo, hoy):
    assert corte_de_caja(repo, hoy) == {"fecha": "2026-10-28", "num_pagos": 3,
                                        "efectivo": 148.0, "tarjeta": 120.0, "total": 268.0}


def test_f3_fecha_como_texto(repo):
    assert corte_de_caja(repo, "2026-10-27") == {"fecha": "2026-10-27", "num_pagos": 2,
                                                 "efectivo": 68.0, "tarjeta": 75.0, "total": 143.0}


def test_f3_dia_sin_pagos(repo):
    assert corte_de_caja(repo, "2026-01-01") == {"fecha": "2026-01-01", "num_pagos": 0,
                                                 "efectivo": 0.0, "tarjeta": 0.0, "total": 0.0}


def test_f3_incluye_pagos_nuevos(repo, hoy):
    repo.agregar("pagos", {"pedido_id": 7, "metodo": "tarjeta", "total": 53.0, "recibido": 53.0,
                           "cambio": 0.0, "fecha": "2026-10-28"})
    c = corte_de_caja(repo, hoy)
    assert c["num_pagos"] == 4 and c["tarjeta"] == 173.0 and c["total"] == 321.0
