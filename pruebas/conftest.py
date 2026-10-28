"""Configuración de las pruebas y REGISTRO AUTOMÁTICO de resultados. NO MODIFICAR.

Cada vez que corren las pruebas, el resultado de cada una se agrega a
registro/ejecuciones_<modulo>.csv (un archivo por módulo, para que los
equipos no choquen al hacer merge). Con ese historial, probar.py detecta
cuándo una prueba pasó de FALLA a PASA (un defecto) y calcula las
métricas Lean de cada actividad.

En GitHub Actions (variable CI) no se registra nada y las funciones
todavía pendientes se marcan como "skipped" en lugar de fallar.
"""

import csv
import os
import re
from datetime import date, datetime
from pathlib import Path

import pytest

from nucleo.repositorio import Repositorio
from nucleo.semilla import datos_semilla

# Fecha fija para que las pruebas den siempre el mismo resultado.
HOY = date(2026, 10, 28)
AYER = date(2026, 10, 27)

RAIZ = Path(__file__).resolve().parent.parent
CARPETA_REGISTRO = RAIZ / "registro"
CAMPOS = ["fecha_hora", "ejecucion", "modulo", "actividad", "prueba", "resultado", "mensaje"]
PATRON = re.compile(r"test_(?P<modulo>\w+)\.py::test_f(?P<actividad>\d)_(?P<prueba>[\w\[\]\-. ]+)")
EJECUCION = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
EN_CI = bool(os.environ.get("CI"))


@pytest.fixture
def hoy():
    return HOY


@pytest.fixture
def ayer():
    return AYER


@pytest.fixture
def repo():
    """Repositorio en memoria con los datos de ejemplo (no toca el archivo de la app)."""
    return Repositorio(datos_semilla(HOY))


def _mensaje(report):
    crash = getattr(report.longrepr, "reprcrash", None)
    texto = crash.message if crash else str(report.longrepr)
    lineas = [l.strip() for l in texto.splitlines() if l.strip()]
    return (lineas[0] if lineas else "")[:180]


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    resultado = yield
    if not EN_CI:
        return
    reporte = resultado.get_result()
    if call.excinfo is not None and call.excinfo.errisinstance(NotImplementedError):
        reporte.outcome = "skipped"
        reporte.longrepr = (str(item.path), item.location[1] or 0, "Skipped: función pendiente")


def pytest_runtest_logreport(report):
    if EN_CI:
        return
    # Se registra la fase "call" (la prueba en sí) y los errores al preparar datos.
    if report.when != "call" and not (report.when == "setup" and report.failed):
        return
    coincidencia = PATRON.search(report.nodeid)
    if not coincidencia:
        return
    if report.passed:
        resultado, mensaje = "PASA", ""
    else:
        mensaje = _mensaje(report)
        resultado = "PENDIENTE" if "NotImplementedError" in mensaje else "FALLA"
    archivo_registro = CARPETA_REGISTRO / f"ejecuciones_{coincidencia['modulo']}.csv"
    CARPETA_REGISTRO.mkdir(parents=True, exist_ok=True)
    nuevo = not archivo_registro.exists()
    with archivo_registro.open("a", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        if nuevo:
            escritor.writerow(CAMPOS)
        escritor.writerow([
            datetime.now().isoformat(timespec="seconds"), EJECUCION,
            coincidencia["modulo"], coincidencia["actividad"], coincidencia["prueba"],
            resultado, mensaje,
        ])
