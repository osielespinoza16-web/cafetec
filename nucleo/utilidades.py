"""Funciones de apoyo que pueden usar los seis módulos. NO MODIFICAR."""

import unicodedata
from datetime import date


def normalizar(texto):
    """Convierte a minúsculas, quita acentos y espacios de los extremos.

    normalizar("  Café AMERICANO ") -> "cafe americano"
    """
    if texto is None:
        return ""
    texto = unicodedata.normalize("NFKD", str(texto))
    sin_acentos = "".join(c for c in texto if not unicodedata.combining(c))
    return sin_acentos.strip().lower()


def a_fecha(valor):
    """Acepta un objeto date o un texto "AAAA-MM-DD" y regresa un date."""
    if isinstance(valor, date):
        return valor
    return date.fromisoformat(str(valor))


def hoy_o(hoy=None):
    """Regresa la fecha recibida o, si es None, la fecha de hoy (como date).

    Las funciones que dependen de la fecha reciben un parámetro `hoy`
    para que las pruebas puedan usar siempre la misma fecha.
    Para guardarla en un registro usa .isoformat() -> "AAAA-MM-DD".
    """
    return a_fecha(hoy) if hoy is not None else date.today()


def total_de_items(items):
    """Suma precio_unitario * cantidad de una lista de items de pedido.

    total_de_items([{"producto_id": 1, "cantidad": 2, "precio_unitario": 25.0}]) -> 50.0
    """
    return round(sum(i["precio_unitario"] * i["cantidad"] for i in items), 2)
