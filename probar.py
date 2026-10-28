"""Herramienta de la actividad Lean. NO MODIFICAR.

Flujo de cada actividad (una tarjeta del tablero):
  python probar.py --iniciar pedidos 1    Jalas la tarjeta: arranca el reloj (límite WIP = 1)
  python probar.py pedidos 1              Corres las pruebas; cuando todas pasan se cierra sola
  python probar.py --bloqueo pedidos "esperando respuesta del equipo 1"
  python probar.py --desbloqueo pedidos   Registran el tiempo que estuvieron detenidos (espera)

Desperdicios (los anota el encargado de flujo en el momento):
  python probar.py --desperdicio pedidos "cambio de tarea" 3 "qué pasó"
      Tipos: espera, retrabajo, parcial, cambio de tarea, extra, transferencia, demora
  Además se registran solos: esperas (--bloqueo), retrabajo (pruebas que fallaron),
  cambio de tarea (intentos frenados por el límite WIP) y trabajo parcialmente hecho.

Métricas:
  python probar.py --metricas pedidos     Métricas Lean del módulo (y archivo para pegar en Excel)
  python probar.py --tablero              Resumen de los 6 módulos -> registro/TABLERO.md

Otros:
  python probar.py pedidos                Corre todas las pruebas del módulo

Módulos: usuarios, catalogo, pedidos (día 1) · caja, inventario, reportes (día 2)
"""

import csv
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
CARPETA = RAIZ / "registro"

FUNCIONES = {
    "usuarios": ["listar_usuarios", "registrar_usuario", "cambiar_estado_usuario"],
    "catalogo": ["listar_menu", "agregar_producto", "cambiar_precio"],
    "pedidos": ["crear_pedido", "listar_pedidos", "cambiar_estado_pedido"],
    "caja": ["calcular_total", "cobrar_pedido", "corte_de_caja"],
    "inventario": ["registrar_entrada", "descontar_pedido", "productos_stock_bajo"],
    "reportes": ["ventas_del_dia", "productos_mas_vendidos", "resumen_por_estado"],
}
EQUIPO = {"usuarios": 1, "catalogo": 2, "pedidos": 3, "caja": 4, "inventario": 5, "reportes": 6}
DIA = {"usuarios": 1, "catalogo": 1, "pedidos": 1, "caja": 2, "inventario": 2, "reportes": 2}
MODULOS = tuple(FUNCIONES)
ACTIVIDADES = ("1", "2", "3")
LIMITE_WIP = 1
CAMPOS_FLUJO = ["fecha_hora", "modulo", "actividad", "evento", "detalle"]
CAMPOS_DESPERDICIO = ["fecha_hora", "modulo", "actividad", "tipo", "minutos", "descripcion", "origen"]
AUTOMATICO = "probar.py"
MANUAL = "Mismo equipo"
# Los 7 desperdicios del software (Poppendieck) y las palabras con que se pueden escribir.
TIPOS_DESPERDICIO = {
    "Espera": ("espera", "esperando", "bloqueo"),
    "Retrabajo / defecto": ("retrabajo", "defecto", "error", "rehacer"),
    "Trabajo parcialmente hecho": ("parcial", "medias", "incompleto", "sin terminar"),
    "Cambio de tarea": ("cambio", "tarea", "multitarea", "saltar"),
    "Funcionalidad extra": ("extra", "funcionalidad", "de mas"),
    "Transferencia / traspaso": ("transferencia", "traspaso", "pasar informacion"),
    "Demoras de proceso": ("demora", "proceso", "tramite", "configuracion", "instalacion"),
}


def ahora():
    return datetime.now().isoformat(timespec="seconds")


def minutos(desde, hasta):
    return round((datetime.fromisoformat(hasta) - datetime.fromisoformat(desde)).total_seconds() / 60, 1)


# ====================================================================== registros
def leer_csv(ruta):
    if not ruta.exists():
        return []
    with ruta.open(encoding="utf-8", newline="") as archivo:
        return list(csv.DictReader(archivo))


def ejecuciones(modulo):
    return leer_csv(CARPETA / f"ejecuciones_{modulo}.csv")


def flujo(modulo):
    return leer_csv(CARPETA / f"flujo_{modulo}.csv")


def anotar_flujo(modulo, actividad, evento, detalle=""):
    ruta = CARPETA / f"flujo_{modulo}.csv"
    CARPETA.mkdir(parents=True, exist_ok=True)
    nuevo = not ruta.exists()
    with ruta.open("a", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        if nuevo:
            escritor.writerow(CAMPOS_FLUJO)
        escritor.writerow([ahora(), modulo, actividad, evento, detalle])


def estado_tarjetas(modulo):
    """Regresa {actividad: {"inicio":..., "fin":..., "bloqueos": [[desde, hasta], ...]}}."""
    tarjetas = {a: {"inicio": None, "fin": None, "bloqueos": []} for a in ACTIVIDADES}
    for fila in flujo(modulo):
        t = tarjetas.get(fila["actividad"])
        if t is None:
            continue
        if fila["evento"] == "INICIO" and t["inicio"] is None:
            t["inicio"] = fila["fecha_hora"]
        elif fila["evento"] == "FIN" and t["fin"] is None:
            t["fin"] = fila["fecha_hora"]
        elif fila["evento"] == "BLOQUEO":
            t["bloqueos"].append([fila["fecha_hora"], None, fila["detalle"]])
        elif fila["evento"] == "DESBLOQUEO" and t["bloqueos"] and t["bloqueos"][-1][1] is None:
            t["bloqueos"][-1][1] = fila["fecha_hora"]
    return tarjetas


def quitar_acentos(texto):
    import unicodedata
    texto = unicodedata.normalize("NFKD", str(texto))
    return "".join(c for c in texto if not unicodedata.combining(c)).strip().lower()


def tipo_desperdicio(texto):
    texto = quitar_acentos(texto)
    for tipo, palabras in TIPOS_DESPERDICIO.items():
        if quitar_acentos(tipo) == texto or any(p in texto for p in palabras):
            return tipo
    return None


def anotar_desperdicio(modulo, actividad, tipo, minutos_perdidos, descripcion, origen):
    ruta = CARPETA / f"desperdicios_{modulo}.csv"
    CARPETA.mkdir(parents=True, exist_ok=True)
    nuevo = not ruta.exists()
    with ruta.open("a", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        if nuevo:
            escritor.writerow(CAMPOS_DESPERDICIO)
        escritor.writerow([ahora(), modulo, actividad, tipo, minutos_perdidos, descripcion, origen])


def en_progreso(tarjetas):
    return [a for a, t in tarjetas.items() if t["inicio"] and not t["fin"]]


# ====================================================================== flujo (sistema pull)
def iniciar(modulo, actividad):
    tarjetas = estado_tarjetas(modulo)
    t = tarjetas[actividad]
    if t["fin"]:
        print(f"La actividad {actividad} de {modulo} ya está terminada.")
        return
    if t["inicio"]:
        print(f"La actividad {actividad} ya estaba en progreso desde {t['inicio'][11:16]}.")
        return
    abiertas = en_progreso(tarjetas)
    if len(abiertas) >= LIMITE_WIP:
        print(f"LÍMITE WIP ({LIMITE_WIP}): termina primero la actividad {abiertas[0]} de {modulo}.")
        print("En Lean se termina lo que se empezó antes de jalar más trabajo.")
        anotar_desperdicio(modulo, abiertas[0], "Cambio de tarea", 0,
                           f"Intentaron iniciar la actividad {actividad} sin terminar la {abiertas[0]} "
                           f"(lo frenó el límite WIP)", AUTOMATICO)
        print("(Quedó registrado como desperdicio: cambio de tarea.)")
        return
    anotar_flujo(modulo, actividad, "INICIO", FUNCIONES[modulo][int(actividad) - 1])
    print(f"Actividad {actividad} de {modulo} EN PROGRESO desde las {ahora()[11:16]}: "
          f"{FUNCIONES[modulo][int(actividad) - 1]}()")
    print("Recuerda mover también la tarjeta en el tablero de flujo de GitHub a 'In Progress'.")


def bloquear(modulo, motivo):
    tarjetas = estado_tarjetas(modulo)
    abiertas = en_progreso(tarjetas)
    if not abiertas:
        print("No hay ninguna actividad en progreso que se pueda bloquear.")
        return
    actividad = abiertas[0]
    if tarjetas[actividad]["bloqueos"] and tarjetas[actividad]["bloqueos"][-1][1] is None:
        print("Ya estaban bloqueados. Cuando se resuelva: python probar.py --desbloqueo " + modulo)
        return
    anotar_flujo(modulo, actividad, "BLOQUEO", motivo or "sin motivo")
    print(f"Actividad {actividad} BLOQUEADA desde las {ahora()[11:16]} ({motivo or 'sin motivo'}).")
    print("Ese tiempo cuenta como ESPERA (desperdicio) y se registra solo.")


def desbloquear(modulo):
    tarjetas = estado_tarjetas(modulo)
    for actividad, t in tarjetas.items():
        if t["bloqueos"] and t["bloqueos"][-1][1] is None:
            anotar_flujo(modulo, actividad, "DESBLOQUEO")
            print(f"Actividad {actividad} desbloqueada. Espera: {minutos(t['bloqueos'][-1][0], ahora())} min.")
            return
    print("No había ningún bloqueo abierto.")


def registrar_desperdicio(modulo, argumentos):
    uso = ('Uso: python probar.py --desperdicio <modulo> "<tipo>" <minutos> "<qué pasó>"\n'
           'Ejemplo: python probar.py --desperdicio pedidos "cambio de tarea" 3 "revisamos la act. 3 sin terminar la 2"\n'
           "Tipos: " + ", ".join(TIPOS_DESPERDICIO))
    if len(argumentos) < 3:
        print(uso)
        return
    tipo = tipo_desperdicio(argumentos[0])
    if tipo is None:
        print(f"No reconozco el tipo '{argumentos[0]}'.\n{uso}")
        return
    try:
        minutos_perdidos = round(float(argumentos[1].replace(",", ".")), 1)
        if minutos_perdidos < 0:
            raise ValueError
    except ValueError:
        print(f"Los minutos deben ser un número, por ejemplo 3 o 1.5.\n{uso}")
        return
    descripcion = " ".join(argumentos[2:]).strip()
    abiertas = en_progreso(estado_tarjetas(modulo))
    actividad = abiertas[0] if abiertas else ""
    anotar_desperdicio(modulo, actividad, tipo, minutos_perdidos, descripcion, MANUAL)
    donde = f" (actividad {actividad})" if actividad else ""
    print(f"Desperdicio registrado{donde}: {tipo} · {minutos_perdidos} min · {descripcion}")


def desperdicios_modulo(modulo):
    """Junta los desperdicios anotados a mano, los automáticos y los que salen del flujo."""
    lista = [{"fecha_hora": f["fecha_hora"], "actividad": f["actividad"], "tipo": f["tipo"],
              "minutos": float(f["minutos"] or 0), "descripcion": f["descripcion"], "origen": f["origen"]}
             for f in leer_csv(CARPETA / f"desperdicios_{modulo}.csv")]
    corte = ahora()
    for act, t in estado_tarjetas(modulo).items():
        for desde, hasta, motivo in t["bloqueos"]:
            lista.append({"fecha_hora": desde, "actividad": act, "tipo": "Espera",
                          "minutos": minutos(desde, hasta or corte),
                          "descripcion": f"Bloqueados: {motivo}" + ("" if hasta else " (sigue abierto)"),
                          "origen": AUTOMATICO})
        if t["inicio"] and not t["fin"]:
            lista.append({"fecha_hora": t["inicio"], "actividad": act, "tipo": "Trabajo parcialmente hecho",
                          "minutos": minutos(t["inicio"], corte),
                          "descripcion": f"La actividad {act} ({FUNCIONES[modulo][int(act) - 1]}) quedó iniciada sin terminar",
                          "origen": AUTOMATICO})
    for d in detectar_defectos(modulo):
        lista.append({"fecha_hora": d["detectado"], "actividad": d["actividad"], "tipo": "Retrabajo / defecto",
                      "minutos": d["minutos"] or 0.0,
                      "descripcion": "Prueba que falló y se corrigió: " + d["descripcion"][:150]
                                     + ("" if d["minutos"] is not None else " (sin corregir)"),
                      "origen": AUTOMATICO})
    return sorted(lista, key=lambda d: d["fecha_hora"])


# ====================================================================== pruebas
def correr_pruebas(modulo, actividad=None):
    import pytest

    tarjetas = estado_tarjetas(modulo)
    revisar = [actividad] if actividad else list(ACTIVIDADES)
    sin_iniciar = [a for a in revisar if not tarjetas[a]["inicio"]]
    if actividad and sin_iniciar:
        print(f"AVISO: no iniciaste la actividad {actividad}. Su lead time no se va a medir.")
        print(f"       Corre primero: python probar.py --iniciar {modulo} {actividad}\n")

    argumentos = ["-q", "--tb=line", "-p", "no:cacheprovider", f"pruebas/test_{modulo}.py"]
    if actividad:
        argumentos += ["-k", f"test_f{actividad}_"]
    print(f"=== Pruebas de {modulo}" + (f", actividad {actividad}" if actividad else "") + " ===\n")
    filas_antes = len(ejecuciones(modulo))
    pytest.main(argumentos)
    nuevas = ejecuciones(modulo)[filas_antes:]
    if not nuevas:
        print("\nNo se ejecutó ninguna prueba. Revisa el nombre del módulo y la actividad.")
        return

    por_actividad = defaultdict(lambda: defaultdict(int))
    for fila in nuevas:
        por_actividad[fila["actividad"]][fila["resultado"]] += 1
    print("\n--- Resumen ---")
    for act in sorted(por_actividad):
        c = por_actividad[act]
        total = sum(c.values())
        if c["PENDIENTE"] == total:
            print(f"  Actividad {act}: PENDIENTE (función sin implementar)")
        elif c["FALLA"] or c["PENDIENTE"]:
            print(f"  Actividad {act}: {c['PASA']}/{total} pasan")
        else:
            print(f"  Actividad {act}: {total}/{total} pasan  -> ACTIVIDAD COMPLETA")
            t = tarjetas[act]
            if t["inicio"] and not t["fin"]:
                if t["bloqueos"] and t["bloqueos"][-1][1] is None:
                    anotar_flujo(modulo, act, "DESBLOQUEO")
                anotar_flujo(modulo, act, "FIN")
                print(f"     Tarjeta cerrada. Lead time: {minutos(t['inicio'], ahora())} min. "
                      f"Mueve la tarjeta a 'Revision' en el tablero de flujo.")

    ejecucion = nuevas[0]["ejecucion"]
    defectos = detectar_defectos(modulo)
    for d in defectos:
        if d["ejecucion_inicio"] == ejecucion:
            print(f"\n  [X] Defecto detectado (act. {d['actividad']}): {d['descripcion']}")
        if d["ejecucion_fin"] == ejecucion:
            print(f"  [OK] Defecto corregido (act. {d['actividad']}) en {d['minutos']} min")


# ====================================================================== defectos
def detectar_defectos(modulo):
    """Un defecto es una prueba que pasó de FALLA a PASA. Los casos de una misma
    prueba parametrizada que fallan y se corrigen juntos cuentan como UNO."""
    abiertos, parejas = {}, []
    for fila in ejecuciones(modulo):
        llave = (fila["actividad"], fila["prueba"])
        if fila["resultado"] == "FALLA" and llave not in abiertos:
            abiertos[llave] = fila
        elif fila["resultado"] == "PASA" and llave in abiertos:
            parejas.append((abiertos.pop(llave), fila))
    parejas += [(inicio, None) for inicio in abiertos.values()]

    grupos = {}
    for inicio, fin in parejas:
        llave = (inicio["actividad"], inicio["ejecucion"], fin["ejecucion"] if fin else None,
                 inicio["prueba"].split("[")[0])
        grupos.setdefault(llave, {"inicio": inicio, "fin": fin, "casos": 0})["casos"] += 1

    defectos = []
    for (act, ej_ini, ej_fin, base), g in sorted(grupos.items(), key=lambda x: x[1]["inicio"]["fecha_hora"]):
        mensaje = g["inicio"]["mensaje"]
        defectos.append({
            "actividad": act,
            "detectado": g["inicio"]["fecha_hora"],
            "corregido": g["fin"]["fecha_hora"] if g["fin"] else "",
            "minutos": max(minutos(g["inicio"]["fecha_hora"], g["fin"]["fecha_hora"]), 0.1) if g["fin"] else None,
            "descripcion": f"{base}" + (f" ({g['casos']} casos)" if g["casos"] > 1 else "") + (f": {mensaje}" if mensaje else ""),
            "ejecucion_inicio": ej_ini,
            "ejecucion_fin": ej_fin,
        })
    return defectos


# ====================================================================== métricas
def metricas_modulo(modulo):
    tarjetas = estado_tarjetas(modulo)
    defectos = detectar_defectos(modulo)
    filas = ejecuciones(modulo)
    resultado = []
    for act in ACTIVIDADES:
        t = tarjetas[act]
        m = {"actividad": act, "funcion": FUNCIONES[modulo][int(act) - 1],
             "inicio": t["inicio"], "fin": t["fin"], "lead": None, "bloqueado": 0.0,
             "ejecuciones": 0, "defectos": 0, "min_corrigiendo": 0.0, "primera": "", "eficiencia": None}
        corte = t["fin"] or ahora()
        if t["inicio"]:
            m["lead"] = minutos(t["inicio"], corte) if t["fin"] else None
            m["bloqueado"] = round(float(sum(minutos(desde, hasta or corte) for desde, hasta, _ in t["bloqueos"])), 1)
            de_la_act = [f for f in filas if f["actividad"] == act and t["inicio"] <= f["fecha_hora"] <= corte]
        else:
            de_la_act = [f for f in filas if f["actividad"] == act]
        por_ejecucion = defaultdict(list)
        for f in de_la_act:
            por_ejecucion[f["ejecucion"]].append(f["resultado"])
        reales = [res for _, res in sorted(por_ejecucion.items()) if not all(r == "PENDIENTE" for r in res)]
        m["ejecuciones"] = len(reales)
        if reales:
            m["primera"] = "Sí" if all(r == "PASA" for r in reales[0]) else "No"
        mios = [d for d in defectos if d["actividad"] == act]
        m["defectos"] = len(mios)
        m["min_corrigiendo"] = round(sum(d["minutos"] or 0 for d in mios), 1)
        if m["lead"]:
            m["eficiencia"] = round((m["lead"] - m["bloqueado"]) / m["lead"] * 100)
        resultado.append(m)
    return resultado


def hora(valor):
    return valor[11:16] if valor else "-"


def mostrar_metricas(modulo):
    datos = metricas_modulo(modulo)
    print(f"\n=== Métricas Lean · Equipo {EQUIPO[modulo]} · {modulo} (día {DIA[modulo]}) ===\n")
    print(f"{'Act':<4}{'Función':<24}{'Inicio':>7}{'Fin':>7}{'Lead':>7}{'Espera':>8}{'Efic.':>7}"
          f"{'Corridas':>10}{'Defectos':>10}{'Min corr.':>11}{'1a vez':>8}")
    for m in datos:
        lead = f"{m['lead']}" if m["lead"] is not None else ("en curso" if m["inicio"] else "-")
        efic = f"{m['eficiencia']}%" if m["eficiencia"] is not None else "-"
        print(f"{m['actividad']:<4}{m['funcion']:<24}{hora(m['inicio']):>7}{hora(m['fin']):>7}{lead:>7}"
              f"{m['bloqueado']:>8}{efic:>7}{m['ejecuciones']:>10}{m['defectos']:>10}"
              f"{m['min_corrigiendo']:>11}{m['primera'] or '-':>8}")
    print("\nLead = minutos desde --iniciar hasta que pasan todas las pruebas.")
    print("Espera = minutos bloqueados. Efic. = eficiencia de flujo (tiempo sin espera / lead).")
    print("1a vez = ¿la primera corrida de pruebas ya pasó todo? (calidad a la primera)")

    salida = CARPETA / f"metricas_{modulo}.txt"
    CARPETA.mkdir(parents=True, exist_ok=True)
    with salida.open("w", encoding="utf-8", newline="") as archivo:
        for m in datos:
            # Columnas de Excel: Act | Función | Inicio | Fin | Lead | Espera | Corridas | Defectos | Min corr. | 1a vez
            archivo.write("\t".join([
                m["actividad"], m["funcion"], hora(m["inicio"]).replace("-", ""), hora(m["fin"]).replace("-", ""),
                "" if m["lead"] is None else str(m["lead"]), str(m["bloqueado"]), str(m["ejecuciones"]),
                str(m["defectos"]), str(m["min_corrigiendo"]), m["primera"],
            ]) + "\r\n")
    print(f"\nArchivo para Excel: registro/{salida.name}")
    print("Ábrelo, selecciona todo (Ctrl+A), copia y pégalo en la hoja Flujo, en la celda ◀ de tu equipo (columna Act.).")

    desperdicios = desperdicios_modulo(modulo)
    print(f"\n=== Desperdicios · Equipo {EQUIPO[modulo]} ===\n")
    if not desperdicios:
        print("  No hay desperdicios registrados.")
    for d in desperdicios:
        act = f"act. {d['actividad']}" if d["actividad"] else "general"
        print(f"  {hora(d['fecha_hora'])}  {act:<8} {d['tipo']:<27} {d['minutos']:>5} min  "
              f"{d['descripcion'][:70]}  [{d['origen']}]")
    print(f"\n  Total: {round(sum(d['minutos'] for d in desperdicios), 1)} min")
    salida = CARPETA / f"desperdicios_{modulo}.txt"
    with salida.open("w", encoding="utf-8", newline="") as archivo:
        for d in desperdicios:
            # Columnas de Excel: Día | Equipo | Tipo | Qué pasó | Min perdidos | Contramedida | Lo detectó
            texto = (f"Act {d['actividad']}: " if d["actividad"] else "") + d["descripcion"].replace("\t", " ")
            archivo.write("\t".join([str(DIA[modulo]), f"Equipo {EQUIPO[modulo]}", d["tipo"], texto,
                                      str(d["minutos"]), "", d["origen"]]) + "\r\n")
    print(f"\nArchivo para Excel: registro/{salida.name}")
    print("Ábrelo, copia todo y pégalo en la hoja Desperdicios, en la primera fila libre de la columna Día.")
    print("Después escriban la contramedida de los que costaron más minutos.")


def tablero():
    lineas = ["# Tablero de métricas Lean · CafeTec", "",
              f"Generado: {ahora().replace('T', ' ')}", "",
              "| Día | Equipo | Módulo | Terminadas | Lead total (min) | Lead prom. | Espera (min) "
              "| Eficiencia | Defectos | Bien a la 1a | Desperdicio (min) |",
              "|---|---|---|---|---|---|---|---|---|---|---|"]
    por_dia = defaultdict(list)
    for modulo in MODULOS:
        datos = metricas_modulo(modulo)
        hechas = [m for m in datos if m["lead"] is not None]
        lead_total = round(float(sum(m["lead"] for m in hechas)), 1)
        espera = round(float(sum(m["bloqueado"] for m in hechas)), 1)
        defectos = sum(m["defectos"] for m in datos)
        con_corrida = [m for m in datos if m["primera"]]
        fpy = round(100 * sum(m["primera"] == "Sí" for m in con_corrida) / len(con_corrida)) if con_corrida else None
        efic = round((lead_total - espera) / lead_total * 100) if lead_total else None
        desperdicio = round(float(sum(d["minutos"] for d in desperdicios_modulo(modulo))), 1)
        fila = {"hechas": len(hechas), "lead": lead_total, "espera": espera, "defectos": defectos, "fpy": fpy,
                "desperdicio": desperdicio}
        por_dia[DIA[modulo]].append(fila)
        lineas.append(
            f"| {DIA[modulo]} | {EQUIPO[modulo]} | {modulo} | {len(hechas)}/3 | {lead_total} | "
            f"{round(lead_total / len(hechas), 1) if hechas else '-'} | {espera} | "
            f"{f'{efic}%' if efic is not None else '-'} | {defectos} | {f'{fpy}%' if fpy is not None else '-'} | "
            f"{desperdicio} |")

    lineas += ["", "## Día 1 contra día 2", "",
               "| Día | Actividades terminadas | Lead promedio por actividad (min) | Espera total (min) "
               "| Defectos por actividad | Desperdicio (min) |", "|---|---|---|---|---|---|"]
    for dia in (1, 2):
        filas = por_dia[dia]
        hechas = sum(f["hechas"] for f in filas)
        lead = sum(f["lead"] for f in filas)
        lineas.append(f"| {dia} | {hechas}/9 | {round(lead / hechas, 1) if hechas else '-'} | "
                      f"{round(sum(f['espera'] for f in filas), 1)} | "
                      f"{round(sum(f['defectos'] for f in filas) / hechas, 2) if hechas else '-'} | "
                      f"{round(sum(f['desperdicio'] for f in filas), 1)} |")
    lineas += ["", "Lead time: desde que se jala la tarjeta (--iniciar) hasta que pasan todas sus pruebas.",
               "Eficiencia de flujo: porcentaje del lead time sin espera (bloqueos).",
               "Bien a la 1a: actividades cuya primera corrida de pruebas pasó completa."]
    salida = CARPETA / "TABLERO.md"
    CARPETA.mkdir(parents=True, exist_ok=True)
    salida.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    print("\n".join(lineas))
    print(f"\nGuardado en registro/{salida.name}")


# ====================================================================== entrada
def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return
    comando = argv[0]
    if comando == "--tablero":
        tablero()
        return
    if comando.startswith("--"):
        if len(argv) < 2 or argv[1] not in MODULOS:
            print(f"Indica el módulo: {', '.join(MODULOS)}")
            return
        modulo = argv[1]
        if comando == "--iniciar":
            if len(argv) < 3 or argv[2] not in ACTIVIDADES:
                print("Indica la actividad: 1, 2 o 3.  Ejemplo: python probar.py --iniciar pedidos 1")
                return
            iniciar(modulo, argv[2])
        elif comando == "--bloqueo":
            bloquear(modulo, " ".join(argv[2:]))
        elif comando == "--desbloqueo":
            desbloquear(modulo)
        elif comando == "--desperdicio":
            registrar_desperdicio(modulo, argv[2:])
        elif comando == "--metricas":
            mostrar_metricas(modulo)
        else:
            print(f"Comando desconocido: {comando}\n")
            print(__doc__)
        return
    if comando not in MODULOS:
        print(f"Módulo desconocido '{comando}'. Usa: {', '.join(MODULOS)}")
        return
    actividad = argv[1] if len(argv) > 1 else None
    if actividad and actividad not in ACTIVIDADES:
        print("La actividad debe ser 1, 2 o 3")
        return
    correr_pruebas(comando, actividad)


if __name__ == "__main__":
    main(sys.argv[1:])
