"""CafeTec — aplicación web. NO MODIFICAR durante la actividad.

Ejecutar:   python app.py            -> abre http://127.0.0.1:5000
Reiniciar los datos de ejemplo:  python app.py --reiniciar

La app llama a las funciones de los seis archivos de modulos/. Mientras
una función no esté implementada, su sección muestra "Pendiente" en
lugar de romper la página.
"""

import sys
from datetime import date
from pathlib import Path
from types import SimpleNamespace

from flask import Flask, flash, redirect, render_template, request, url_for

from modulos import caja, catalogo, inventario, pedidos, reportes, usuarios
from nucleo.config import CATEGORIAS, ESTADOS, METODOS_PAGO, ROLES, TRANSICIONES
from nucleo.repositorio import Repositorio
from nucleo.semilla import datos_semilla

RUTA_DATOS = Path(__file__).parent / "datos" / "cafeteria.json"

app = Flask(__name__)
app.secret_key = "cafetec-lean"


def obtener_repo():
    return Repositorio.desde_archivo(RUTA_DATOS, datos_semilla)


def llamar(funcion, *args, **kwargs):
    """Ejecuta una función de los módulos y atrapa sus errores."""
    try:
        return SimpleNamespace(ok=True, valor=funcion(*args, **kwargs), pendiente=False, error=None)
    except NotImplementedError:
        return SimpleNamespace(ok=False, valor=None, pendiente=True,
                               error=f"{funcion.__name__}() aún está pendiente")
    except ValueError as e:
        return SimpleNamespace(ok=False, valor=None, pendiente=False, error=str(e))
    except Exception as e:  # error inesperado en el código del módulo
        return SimpleNamespace(ok=False, valor=None, pendiente=False,
                               error=f"Error inesperado en {funcion.__name__}(): "
                                     f"{type(e).__name__}: {e}")


def avisar(resultado, mensaje_ok):
    if resultado.ok:
        flash(mensaje_ok, "exito")
    elif resultado.pendiente:
        flash(resultado.error, "pendiente")
    else:
        flash(resultado.error, "error")


def nombres_de_productos(repo):
    return {p["id"]: p["nombre"] for p in repo.listar("productos")}


@app.context_processor
def globales():
    return {"CATEGORIAS": CATEGORIAS, "ESTADOS": ESTADOS, "ROLES": ROLES,
            "METODOS_PAGO": METODOS_PAGO, "TRANSICIONES": TRANSICIONES,
            "HOY": date.today().isoformat()}


# ---------------------------------------------------------------- inicio
@app.route("/")
def inicio():
    repo = obtener_repo()
    hoy = date.today().isoformat()
    return render_template(
        "inicio.html",
        usuarios=llamar(usuarios.listar_usuarios, repo, True),
        menu=llamar(catalogo.listar_menu, repo),
        estados=llamar(reportes.resumen_por_estado, repo),
        ventas=llamar(reportes.ventas_del_dia, repo, hoy),
        corte=llamar(caja.corte_de_caja, repo, hoy),
        bajo=llamar(inventario.productos_stock_bajo, repo),
    )


# ---------------------------------------------------------------- Equipo 1 · usuarios
@app.route("/usuarios")
def ver_usuarios():
    solo_activos = request.args.get("solo_activos") == "1"
    lista = llamar(usuarios.listar_usuarios, obtener_repo(), solo_activos)
    return render_template("usuarios.html", lista=lista, solo_activos=solo_activos)


@app.post("/usuarios/registrar")
def registrar_usuario():
    f = request.form
    r = llamar(usuarios.registrar_usuario, obtener_repo(), f.get("nombre", ""),
               f.get("correo", ""), f.get("rol", "cliente"))
    avisar(r, f"Usuario registrado con id {r.valor}")
    return redirect(url_for("ver_usuarios"))


@app.post("/usuarios/<int:usuario_id>/estado")
def cambiar_estado_usuario(usuario_id):
    activar = request.form.get("activo") == "1"
    r = llamar(usuarios.cambiar_estado_usuario, obtener_repo(), usuario_id, activar)
    avisar(r, "Usuario activado" if activar else "Usuario desactivado")
    return redirect(url_for("ver_usuarios"))


# ---------------------------------------------------------------- Equipo 2 · catálogo
@app.route("/menu")
def ver_menu():
    categoria = request.args.get("categoria", "")
    lista = llamar(catalogo.listar_menu, obtener_repo(), categoria or None)
    return render_template("menu.html", lista=lista, categoria=categoria)


@app.post("/menu/agregar")
def agregar_producto():
    f = request.form
    r = llamar(catalogo.agregar_producto, obtener_repo(), f.get("nombre", ""),
               f.get("categoria", ""), f.get("precio", ""))
    avisar(r, f"Producto agregado con id {r.valor}")
    return redirect(url_for("ver_menu"))


@app.post("/menu/<int:producto_id>/precio")
def cambiar_precio(producto_id):
    r = llamar(catalogo.cambiar_precio, obtener_repo(), producto_id, request.form.get("precio", ""))
    avisar(r, "Precio actualizado")
    return redirect(url_for("ver_menu"))


# ---------------------------------------------------------------- Equipo 3 · pedidos
@app.route("/pedidos")
def ver_pedidos():
    repo = obtener_repo()
    estado = request.args.get("estado", "")
    return render_template(
        "pedidos.html",
        lista=llamar(pedidos.listar_pedidos, repo, estado or None),
        estado=estado,
        clientes=repo.filtrar("usuarios", lambda u: u["activo"]),
        productos=repo.filtrar("productos", lambda p: p["disponible"]),
        nombres=nombres_de_productos(repo),
    )


@app.post("/pedidos/crear")
def crear_pedido():
    f = request.form
    try:
        usuario_id = int(f.get("usuario_id", ""))
    except ValueError:
        flash("Selecciona un cliente", "error")
        return redirect(url_for("ver_pedidos"))
    items = []
    for n in (1, 2, 3):
        producto = f.get(f"producto_{n}", "")
        if producto:
            items.append({"producto_id": int(producto), "cantidad": f.get(f"cantidad_{n}", "")})
    r = llamar(pedidos.crear_pedido, obtener_repo(), usuario_id, items)
    avisar(r, f"Pedido creado con folio {r.valor}")
    return redirect(url_for("ver_pedidos"))


@app.post("/pedidos/<int:pedido_id>/estado")
def cambiar_estado_pedido(pedido_id):
    nuevo = request.form.get("estado", "")
    r = llamar(pedidos.cambiar_estado_pedido, obtener_repo(), pedido_id, nuevo)
    avisar(r, f"Pedido {pedido_id} ahora está: {nuevo}")
    return redirect(request.referrer or url_for("ver_pedidos"))


# ---------------------------------------------------------------- Equipo 4 · caja
@app.route("/caja")
def ver_caja():
    repo = obtener_repo()
    fecha = request.args.get("fecha") or date.today().isoformat()
    por_cobrar = repo.filtrar("pedidos", lambda p: not p["pagado"] and p["estado"] != "cancelado")
    totales = {p["id"]: llamar(caja.calcular_total, repo, p["id"]) for p in por_cobrar}
    return render_template(
        "caja.html",
        por_cobrar=sorted(por_cobrar, key=lambda p: p["id"]),
        totales=totales,
        corte=llamar(caja.corte_de_caja, repo, fecha),
        fecha=fecha,
        pagos=sorted(repo.listar("pagos"), key=lambda p: p["id"], reverse=True)[:8],
    )


@app.post("/caja/<int:pedido_id>/cobrar")
def cobrar(pedido_id):
    f = request.form
    r = llamar(caja.cobrar_pedido, obtener_repo(), pedido_id, f.get("metodo", ""), f.get("recibido") or None)
    if r.ok:
        flash(f"Ticket {r.valor['id']} · pedido {pedido_id} · total ${r.valor['total']:.2f} · "
              f"cambio ${r.valor['cambio']:.2f}", "exito")
    else:
        avisar(r, "")
    return redirect(url_for("ver_caja"))


# ---------------------------------------------------------------- Equipo 5 · inventario
@app.route("/inventario")
def ver_inventario():
    repo = obtener_repo()
    return render_template(
        "inventario.html",
        productos=sorted(repo.listar("productos"), key=lambda p: p["id"]),
        bajo=llamar(inventario.productos_stock_bajo, repo),
        por_descontar=repo.filtrar("pedidos", lambda p: p["pagado"] and not p["inventario_descontado"]
                                   and p["estado"] != "cancelado"),
        nombres=nombres_de_productos(repo),
    )


@app.post("/inventario/entrada")
def registrar_entrada():
    f = request.form
    try:
        producto_id = int(f.get("producto_id", ""))
    except ValueError:
        flash("Selecciona un producto", "error")
        return redirect(url_for("ver_inventario"))
    r = llamar(inventario.registrar_entrada, obtener_repo(), producto_id, f.get("cantidad", ""))
    avisar(r, f"Entrada registrada. Stock nuevo: {r.valor}")
    return redirect(url_for("ver_inventario"))


@app.post("/inventario/descontar/<int:pedido_id>")
def descontar(pedido_id):
    r = llamar(inventario.descontar_pedido, obtener_repo(), pedido_id)
    avisar(r, f"Inventario descontado para el pedido {pedido_id}")
    return redirect(url_for("ver_inventario"))


# ---------------------------------------------------------------- Equipo 6 · reportes
@app.route("/reportes")
def ver_reportes():
    repo = obtener_repo()
    fecha = request.args.get("fecha") or date.today().isoformat()
    limite = request.args.get("limite") or "3"
    return render_template(
        "reportes.html",
        ventas=llamar(reportes.ventas_del_dia, repo, fecha),
        top=llamar(reportes.productos_mas_vendidos, repo, limite),
        estados=llamar(reportes.resumen_por_estado, repo),
        fecha=fecha,
        limite=limite,
    )


# ---------------------------------------------------------------- utilidades
@app.post("/reiniciar")
def reiniciar():
    RUTA_DATOS.unlink(missing_ok=True)
    flash("Datos de ejemplo restaurados", "exito")
    return redirect(request.referrer or url_for("inicio"))


if __name__ == "__main__":
    if "--reiniciar" in sys.argv:
        RUTA_DATOS.unlink(missing_ok=True)
        print("Datos de ejemplo restaurados.")
    app.run(debug=True)
