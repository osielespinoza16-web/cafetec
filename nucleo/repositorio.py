"""Capa de datos compartida. NO MODIFICAR.

Guarda cuatro colecciones: "usuarios", "productos", "pedidos" y "pagos".
Cada registro es un diccionario con un campo "id" entero.

    repo.listar("productos")                      -> lista de dicts (copias)
    repo.obtener("productos", 3)                  -> dict o None si no existe
    repo.agregar("productos", {...})              -> id asignado (int)
    repo.actualizar("productos", 3, {"precio": 30.0}) -> dict actualizado
    repo.eliminar("productos", 3)                 -> True / False
    repo.filtrar("pedidos", lambda p: p["usuario_id"] == 2) -> lista de dicts

Los registros que regresa son COPIAS: modificarlos no cambia los datos.
Para guardar cambios hay que usar actualizar().
"""

import copy
import json
from pathlib import Path

COLECCIONES = ("usuarios", "productos", "pedidos", "pagos")


class Repositorio:
    def __init__(self, datos=None, ruta=None):
        datos = datos or {}
        self._datos = {c: copy.deepcopy(datos.get(c, [])) for c in COLECCIONES}
        self._ruta = Path(ruta) if ruta else None

    # ---------- creación desde archivo ----------
    @classmethod
    def desde_archivo(cls, ruta, crear_datos):
        """Carga el JSON de `ruta`; si no existe, lo crea con crear_datos()."""
        ruta = Path(ruta)
        if ruta.exists():
            datos = json.loads(ruta.read_text(encoding="utf-8"))
        else:
            datos = crear_datos()
        repo = cls(datos, ruta)
        repo._guardar()
        return repo

    def _guardar(self):
        if self._ruta:
            self._ruta.parent.mkdir(parents=True, exist_ok=True)
            self._ruta.write_text(
                json.dumps(self._datos, ensure_ascii=False, indent=2), encoding="utf-8"
            )

    def _coleccion(self, nombre):
        if nombre not in COLECCIONES:
            raise ValueError(f"Colección desconocida: {nombre}")
        return self._datos[nombre]

    # ---------- operaciones ----------
    def listar(self, coleccion):
        return [copy.deepcopy(r) for r in self._coleccion(coleccion)]

    def obtener(self, coleccion, id_):
        for registro in self._coleccion(coleccion):
            if registro["id"] == id_:
                return copy.deepcopy(registro)
        return None

    def agregar(self, coleccion, registro):
        filas = self._coleccion(coleccion)
        nuevo = copy.deepcopy(registro)
        nuevo["id"] = max((r["id"] for r in filas), default=0) + 1
        filas.append(nuevo)
        self._guardar()
        return nuevo["id"]

    def actualizar(self, coleccion, id_, cambios):
        for registro in self._coleccion(coleccion):
            if registro["id"] == id_:
                cambios = {k: v for k, v in cambios.items() if k != "id"}
                registro.update(copy.deepcopy(cambios))
                self._guardar()
                return copy.deepcopy(registro)
        raise KeyError(f"No existe {coleccion} con id {id_}")

    def eliminar(self, coleccion, id_):
        filas = self._coleccion(coleccion)
        for i, registro in enumerate(filas):
            if registro["id"] == id_:
                filas.pop(i)
                self._guardar()
                return True
        return False

    def filtrar(self, coleccion, condicion):
        return [copy.deepcopy(r) for r in self._coleccion(coleccion) if condicion(r)]
