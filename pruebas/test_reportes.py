"""Pruebas del módulo REPORTES (Equipo 6). NO MODIFICAR.
El nombre test_fN_... indica la actividad (N) que se está probando."""

import pytest

from modulos.reportes import productos_mas_vendidos, resumen_por_estado, ventas_del_dia


# ------------------------------------------------------------ Actividad 1
def test_f1_ventas_de_hoy(repo, hoy):
    assert ventas_del_dia(repo, hoy) == {"fecha": "2026-10-28", "pedidos": 3, "total": 268.0}


def test_f1_fecha_como_texto(repo):
    assert ventas_del_dia(repo, "2026-10-27") == {"fecha": "2026-10-27", "pedidos": 2, "total": 143.0}


def test_f1_no_cuenta_pedidos_sin_pagar(repo, hoy):
    repo.actualizar("pedidos", 7, {"estado": "entregado"})  # entregado pero sin pagar
    assert ventas_del_dia(repo, hoy)["pedidos"] == 3, "Solo cuentan los pedidos con pagado True"


def test_f1_dia_sin_ventas(repo):
    assert ventas_del_dia(repo, "2026-01-01") == {"fecha": "2026-01-01", "pedidos": 0, "total": 0.0}


# ------------------------------------------------------------ Actividad 2
def test_f2_top_tres(repo):
    assert productos_mas_vendidos(repo) == [
        {"producto_id": 5, "nombre": "Burrito de deshebrada", "cantidad": 3},
        {"producto_id": 1, "nombre": "Café americano", "cantidad": 3},
        {"producto_id": 4, "nombre": "Agua natural", "cantidad": 2},
    ], "Mayor cantidad primero; si empatan, por nombre. Por omisión limite=3"


def test_f2_empates_por_nombre(repo):
    nombres = [p["nombre"] for p in productos_mas_vendidos(repo, 8)]
    assert nombres[3:] == ["Capuchino", "Galleta de avena", "Jugo de naranja", "Pay de queso", "Torta de jamón"]


def test_f2_limite_como_texto(repo):
    assert len(productos_mas_vendidos(repo, "5")) == 5


def test_f2_limite_mayor_al_total(repo):
    assert len(productos_mas_vendidos(repo, 50)) == 8, "Solo 8 productos distintos se han vendido"


def test_f2_solo_pedidos_pagados(repo):
    vendidos = {p["producto_id"] for p in productos_mas_vendidos(repo, 50)}
    assert 12 not in vendidos and 11 not in vendidos, "Los pedidos sin pagar no cuentan"


@pytest.mark.parametrize("limite", [0, -2, "tres", None])
def test_f2_limite_invalido(repo, limite):
    with pytest.raises(ValueError):
        productos_mas_vendidos(repo, limite)


# ------------------------------------------------------------ Actividad 3
def test_f3_conteo_por_estado(repo):
    assert resumen_por_estado(repo) == {"pendiente": 3, "preparando": 1, "listo": 1,
                                        "entregado": 3, "cancelado": 2}


def test_f3_orden_de_las_llaves(repo):
    assert list(resumen_por_estado(repo)) == ["pendiente", "preparando", "listo", "entregado", "cancelado"], \
        "Las llaves van en el mismo orden que ESTADOS"


def test_f3_estados_en_cero(repo):
    for p in repo.listar("pedidos"):
        repo.actualizar("pedidos", p["id"], {"estado": "entregado"})
    assert resumen_por_estado(repo) == {"pendiente": 0, "preparando": 0, "listo": 0,
                                        "entregado": 10, "cancelado": 0}
