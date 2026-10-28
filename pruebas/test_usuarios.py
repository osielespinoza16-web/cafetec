"""Pruebas del módulo USUARIOS (Equipo 1). NO MODIFICAR.
El nombre test_fN_... indica la actividad (N) que se está probando."""

import pytest

from modulos.usuarios import cambiar_estado_usuario, listar_usuarios, registrar_usuario


def ids(lista):
    return [x["id"] for x in lista]


# ------------------------------------------------------------ Actividad 1
def test_f1_regresa_todos_los_usuarios(repo):
    assert len(listar_usuarios(repo)) == 8, "Debe regresar los 8 usuarios de ejemplo"


def test_f1_ordenados_por_nombre(repo):
    nombres = [u["nombre"] for u in listar_usuarios(repo)]
    assert nombres[0] == "Ana Torres", "El primero debe ser 'Ana Torres'"
    assert nombres[-1] == "Héctor Salinas", "El último debe ser 'Héctor Salinas'"
    assert nombres == sorted(nombres, key=lambda n: n.lower()), "Deben ir en orden alfabético"


def test_f1_orden_ignora_acentos(repo):
    repo.agregar("usuarios", {"nombre": "Érika López", "correo": "erika@cafetec.mx", "rol": "cliente", "activo": True})
    nombres = [u["nombre"] for u in listar_usuarios(repo)]
    assert nombres.index("Érika López") == nombres.index("Elena Ruiz") + 1, \
        "'Érika' va después de 'Elena' y antes de 'Fernando' (orden sin acentos, usa normalizar)"


def test_f1_agrega_llave_estado(repo):
    por_id = {u["id"]: u for u in listar_usuarios(repo)}
    assert por_id[1]["estado"] == "Activo", "Un usuario activo debe tener estado 'Activo'"
    assert por_id[4]["estado"] == "Inactivo", "Un usuario inactivo debe tener estado 'Inactivo'"


def test_f1_solo_activos(repo):
    activos = listar_usuarios(repo, solo_activos=True)
    assert sorted(ids(activos)) == [1, 2, 3, 5, 6, 7], "Con solo_activos=True no deben salir los usuarios 4 y 8"


# ------------------------------------------------------------ Actividad 2
def test_f2_registra_y_regresa_id(repo):
    nuevo_id = registrar_usuario(repo, "Irma Vega", "irma.vega@cafetec.mx")
    assert nuevo_id == 9, "Debe regresar el id que asigna repo.agregar()"
    u = repo.obtener("usuarios", nuevo_id)
    assert u is not None, "El usuario no se guardó en el repositorio"
    assert u["rol"] == "cliente" and u["activo"] is True, "Por omisión es 'cliente' y queda activo"


def test_f2_limpia_nombre_y_correo(repo):
    nuevo_id = registrar_usuario(repo, "  Irma Vega ", "  Irma.VEGA@CafeTec.mx ", "admin")
    u = repo.obtener("usuarios", nuevo_id)
    assert u["nombre"] == "Irma Vega", "El nombre se guarda sin espacios en los extremos"
    assert u["correo"] == "irma.vega@cafetec.mx", "El correo se guarda sin espacios y en minúsculas"
    assert u["rol"] == "admin", "Debe guardar el rol recibido"


@pytest.mark.parametrize("correo", ["irma", "irma@", "@cafetec.mx", "irma@cafetec", "irma@.mx",
                                    "irma@cafetec.", "ir@ma@cafetec.mx", ""])
def test_f2_correo_invalido(repo, correo):
    with pytest.raises(ValueError):
        registrar_usuario(repo, "Irma Vega", correo)


def test_f2_correo_duplicado(repo):
    with pytest.raises(ValueError):
        registrar_usuario(repo, "Otra Ana", "  ANA.TORRES@cafetec.mx")


def test_f2_nombre_vacio(repo):
    with pytest.raises(ValueError):
        registrar_usuario(repo, "   ", "irma@cafetec.mx")


def test_f2_rol_invalido(repo):
    with pytest.raises(ValueError):
        registrar_usuario(repo, "Irma Vega", "irma@cafetec.mx", "gerente")


def test_f2_no_guarda_si_hay_error(repo):
    with pytest.raises(ValueError):
        registrar_usuario(repo, "Irma Vega", "irma@cafetec", "cliente")
    assert len(repo.listar("usuarios")) == 8, "Si hay error no se debe guardar nada"


# ------------------------------------------------------------ Actividad 3
def test_f3_desactiva_cliente(repo):
    u = cambiar_estado_usuario(repo, 2, False)
    assert u["activo"] is False, "Debe regresar el usuario actualizado"
    assert repo.obtener("usuarios", 2)["activo"] is False, "El cambio debe guardarse con repo.actualizar"


def test_f3_activa_usuario(repo):
    u = cambiar_estado_usuario(repo, 4, True)
    assert u["activo"] is True and repo.obtener("usuarios", 4)["activo"] is True


def test_f3_usuario_inexistente(repo):
    with pytest.raises(ValueError):
        cambiar_estado_usuario(repo, 99, False)


def test_f3_desactiva_admin_si_queda_otro(repo):
    u = cambiar_estado_usuario(repo, 5, False)
    assert u["activo"] is False, "Se puede desactivar a un admin si queda otro admin activo"


def test_f3_no_desactiva_al_ultimo_admin(repo):
    cambiar_estado_usuario(repo, 5, False)
    with pytest.raises(ValueError):
        cambiar_estado_usuario(repo, 1, False)
    assert repo.obtener("usuarios", 1)["activo"] is True, "El último admin debe seguir activo"


def test_f3_reactivar_admin_siempre_se_puede(repo):
    cambiar_estado_usuario(repo, 5, False)
    assert cambiar_estado_usuario(repo, 1, True)["activo"] is True, "Activar siempre se permite"
