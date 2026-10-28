"""Crea en GitHub las etiquetas y las 18 tarjetas (issues) de la actividad.

Lo corre UNA sola vez quien administra el repositorio, después de subirlo.
Necesita GitHub CLI (https://cli.github.com) con sesión iniciada: gh auth login

    python scripts/crear_tablero.py               Crea etiquetas e issues
    python scripts/crear_tablero.py --proyecto    Además crea el tablero de flujo (GitHub Projects)
                                                  y agrega las 18 tarjetas.
                                                  Antes: gh auth refresh -s project

Se puede volver a correr sin duplicar: salta las tarjetas que ya existen.
"""

import json
import subprocess
import sys

MODULOS = {
    "usuarios": (1, 1, ["listar_usuarios", "registrar_usuario", "cambiar_estado_usuario"]),
    "catalogo": (2, 1, ["listar_menu", "agregar_producto", "cambiar_precio"]),
    "pedidos": (3, 1, ["crear_pedido", "listar_pedidos", "cambiar_estado_pedido"]),
    "caja": (4, 2, ["calcular_total", "cobrar_pedido", "corte_de_caja"]),
    "inventario": (5, 2, ["registrar_entrada", "descontar_pedido", "productos_stock_bajo"]),
    "reportes": (6, 2, ["ventas_del_dia", "productos_mas_vendidos", "resumen_por_estado"]),
}

ETIQUETAS = [
    ("actividad", "5b3a29", "Tarjeta de trabajo: una función de un módulo"),
    ("desperdicio", "a3302a", "Espera, retrabajo u otro desperdicio Lean"),
    ("metricas", "1d4e75", "Reportes automáticos de métricas de flujo"),
    ("dia-1", "c9a27e", "Se programa el día 1"),
    ("dia-2", "8c6a4f", "Se programa el día 2"),
] + [(f"equipo-{n}", "e6dbd0", f"Módulo {m}") for m, (n, _, _) in MODULOS.items()]


def gh(*argumentos, capturar=True):
    resultado = subprocess.run(["gh", *argumentos], capture_output=capturar, text=True)
    if resultado.returncode != 0 and capturar:
        raise RuntimeError(resultado.stderr.strip())
    return resultado.stdout if capturar else ""


def cuerpo(modulo, equipo, actividad, funcion):
    return f"""**Equipo:** {equipo}
**Módulo / archivo:** `modulos/{modulo}.py`
**Función:** `{funcion}()` — la especificación completa está en su docstring.

### Flujo de la tarjeta

1. Mueve esta tarjeta a **En progreso** y corre `python probar.py --iniciar {modulo} {actividad}`.
2. Programa la función.
3. Corre `python probar.py {modulo} {actividad}` hasta que diga **ACTIVIDAD COMPLETA**.
4. Mueve la tarjeta a **Revisión**. Se cierra sola cuando hacen merge del Pull Request (`Closes #<este número>`).

Si se quedan detenidos esperando algo: `python probar.py --bloqueo {modulo} "motivo"`.
"""


def main():
    try:
        gh("auth", "status")
    except (RuntimeError, FileNotFoundError):
        print("Necesitas GitHub CLI con sesión iniciada: instala https://cli.github.com y corre 'gh auth login'.")
        return

    print("Creando etiquetas...")
    for nombre, color, descripcion in ETIQUETAS:
        gh("label", "create", nombre, "--color", color, "--description", descripcion, "--force")

    existentes = {i["title"] for i in json.loads(gh("issue", "list", "--state", "all", "--limit", "200",
                                                     "--json", "title"))}
    creados = []
    print("Creando tarjetas...")
    for modulo, (equipo, dia, funciones) in MODULOS.items():
        for n, funcion in enumerate(funciones, 1):
            titulo = f"[{modulo}] Actividad {n} · {funcion}"
            if titulo in existentes:
                print(f"  ya existe: {titulo}")
                continue
            url = gh("issue", "create", "--title", titulo, "--body", cuerpo(modulo, equipo, n, funcion),
                     "--label", f"actividad,dia-{dia},equipo-{equipo}").strip()
            creados.append(url)
            print(f"  {titulo}  ->  {url}")

    if "--proyecto" in sys.argv:
        dueño = json.loads(gh("repo", "view", "--json", "owner"))["owner"]["login"]
        print("Creando el tablero de flujo en GitHub Projects...")
        proyecto = json.loads(gh("project", "create", "--owner", dueño, "--title", "Tablero de flujo CafeTec",
                                 "--format", "json"))
        numero = str(proyecto["number"])
        urls = [i["url"] for i in json.loads(gh("issue", "list", "--label", "actividad", "--state", "all",
                                                 "--limit", "100", "--json", "url"))]
        for url in urls:
            gh("project", "item-add", numero, "--owner", dueño, "--url", url)
        print(f"Tablero listo: {proyecto['url']}")
        print("Ábrelo y en la columna Status agrega la opción 'Revisión' entre 'In Progress' y 'Done'.")
        print("Luego en Settings del proyecto -> Manage access, da acceso de escritura a todos.")

    print(f"\nListo. Tarjetas nuevas: {len(creados)}.")


if __name__ == "__main__":
    main()
