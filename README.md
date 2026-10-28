# CafeTec · Actividad Lean Software Development

CafeTec es el sistema de pedidos de una cafetería escolar, hecho en Python (Flask).
La app, el diseño y las pruebas **ya están hechos**. Cada equipo programa las **3 funciones
de su módulo** en menos de una hora y **mide su flujo de trabajo** con métricas Lean.

| Equipo | Módulo | Archivo | Día | Revisa su PR | Observa el día que no programa |
|---|---|---|---|---|---|
| 1 | Usuarios | `modulos/usuarios.py` | 1 | Equipo 6 | Equipo 6 (día 2) |
| 2 | Catálogo (menú) | `modulos/catalogo.py` | 1 | Equipo 5 | Equipo 5 (día 2) |
| 3 | Pedidos | `modulos/pedidos.py` | 1 | Equipo 4 | Equipo 4 (día 2) |
| 4 | Caja | `modulos/caja.py` | 2 | Equipo 3 | Equipo 3 (día 1) |
| 5 | Inventario | `modulos/inventario.py` | 2 | Equipo 2 | Equipo 2 (día 1) |
| 6 | Reportes | `modulos/reportes.py` | 2 | Equipo 1 | Equipo 1 (día 1) |

Las parejas no son al azar: Caja cobra los pedidos, Inventario descuenta los productos del
catálogo y Reportes lee usuarios y ventas. Quien **usa** un módulo es quien lo revisa.

## 1. Instalación (antes del día 1)

Necesitas Python 3.10 o superior y Git.

```bash
git clone <url-del-repo>
cd cafetec
pip install -r requirements.txt
python app.py
```

Abre <http://127.0.0.1:5000>. Las secciones que aún no se programan aparecen como
**Pendiente**: es normal. Después corre `python probar.py <tu_modulo> 1`; debe decir
`PENDIENTE (función sin implementar)`.

Lee completo el docstring de las 3 funciones de tu módulo **antes** de la sesión.

## 2. Reglas

- Solo modificas **tu archivo** dentro de `modulos/`.
- **No** modifiques `app.py`, `nucleo/`, `pruebas/`, `templates/` ni `static/`.
- No cambies el nombre ni los parámetros de las funciones.
- Puedes crear funciones auxiliares (que empiecen con `_`) dentro de tu archivo.
- **Límite WIP = 1:** solo una actividad en progreso a la vez por equipo. `probar.py` no te
  deja iniciar otra hasta terminar la actual.
- Nada se considera terminado hasta que sus pruebas pasan **y** el PR se aprueba.

## 3. Lean en esta actividad

| Principio Lean | Cómo se aplica aquí |
|---|---|
| Eliminar desperdicio | Registran esperas (`--bloqueo`) y desperdicios (issue "Desperdicio") |
| Construir con calidad | Pruebas automáticas en cada corrida y en cada PR (GitHub Actions) |
| Amplificar el aprendizaje | La retrospectiva del día 1 alimenta la forma de trabajar del día 2 |
| Decidir lo más tarde posible | Los módulos son independientes; nadie espera a otro para programar |
| Entregar rápido | Sistema pull: cada equipo jala su siguiente tarjeta del tablero de flujo; lotes pequeños (una función por tarjeta) |
| Empoderar al equipo | Nadie asigna trabajo: cada equipo decide cuándo jalar y cómo resolver su tarjeta |
| Ver el todo | El tablero (`registro/TABLERO.md`) compara a los 6 equipos y a los 2 días |

### El tablero de flujo (herramientas de LSD)

El [tablero de flujo](https://github.com/users/osielespinoza16-web/projects/2) aplica dos
herramientas del principio **"Entregar lo más rápido posible"** del libro de Mary y Tom
Poppendieck, *Lean Software Development: An Agile Toolkit*:

- **Sistemas pull:** el trabajo no se asigna, cada equipo *jala* su siguiente tarjeta cuando
  termina la anterior.
- **Teoría de colas:** limitar el trabajo en curso (WIP = 1) y reducir las colas, por ejemplo
  los PR que esperan revisión, para que el trabajo fluya.

También sirve al principio **"Ver el todo"**: cualquiera ve en qué va cada equipo y dónde se
atora el flujo. Columnas: *Todo → In Progress → Revision → Done*.

## 4. Agenda de cada sesión (≤ 55 min)

| Minuto | Equipos que programan | Equipos que no programan ese día |
|---|---|---|
| 0–5 | `git pull`, crear rama, iniciar la actividad 1 | Se sientan con el equipo que van a observar |
| 5–35 | Actividades 1, 2 y 3 (≈10 min cada una), un commit por actividad | **Observan** y anotan desperdicios que vean (tabla B de la hoja); leen sus propios docstrings |
| 35–45 | Abren el PR con sus métricas | **Revisan** el PR con `REVISION.md` y lo aprueban |
| 45–55 | Merge, `--metricas` y retrospectiva en la hoja de Excel | Retrospectiva juntos |

Al terminar el día 1, el grupo elige **1 o 2 mejoras** de la retrospectiva y los equipos del
día 2 las aplican (eso es *kaizen*). Al final se comparan los dos días con datos.

## 5. Roles dentro del equipo (rotan en cada actividad)

- **Programador:** escribe el código.
- **Navegante:** lee la especificación en voz alta y revisa cada línea mientras se escribe.
- **Encargado de flujo:** mueve la tarjeta, corre `--iniciar`, `--bloqueo` y las pruebas, y
  anota desperdicios.

## 6. Ciclo de cada actividad (una tarjeta)

1. **Jalar.** Mueve la tarjeta a *In Progress* en el tablero de flujo y corre:
   ```bash
   python probar.py --iniciar pedidos 1
   ```
2. **Programar.** Lee el docstring completo y programa la función.
3. **Probar.** Corre las pruebas hasta que diga `ACTIVIDAD COMPLETA`:
   ```bash
   python probar.py pedidos 1
   ```
   Cada prueba que pasa de FALLA a PASA queda registrada sola como **defecto**, con su
   tiempo de corrección. La tarjeta se cierra sola cuando todo pasa.
4. **Si se atoran** (dudas, esperar a alguien, la computadora falla):
   ```bash
   python probar.py --bloqueo pedidos "esperando respuesta del profe"
   python probar.py --desbloqueo pedidos
   ```
5. **Cerrar.** Commit y mueve la tarjeta a *Revision* en el tablero de flujo:
   ```bash
   git add modulos/pedidos.py registro/
   git commit -m "Actividad 1: crear_pedido"
   ```

## 7. Git: una rama y un PR por equipo

```bash
git checkout main
git pull
git checkout -b equipo-3-pedidos
# ... actividades 1, 2 y 3, con un commit cada una ...
git push -u origin equipo-3-pedidos
```

Luego abren el Pull Request en GitHub (la plantilla ya trae lo que deben llenar) y escriben
`Closes #N` por cada tarjeta. El equipo revisor aprueba y el equipo dueño hace
**Squash and merge**. No hay conflictos: cada equipo toca archivos distintos, y el registro de
métricas va en archivos separados por módulo.

## 8. Métricas que se recaban

| Métrica | Qué dice | De dónde sale |
|---|---|---|
| Lead time por actividad | Minutos desde que se jala la tarjeta hasta que sus pruebas pasan | `probar.py --metricas` |
| Espera | Minutos que el equipo estuvo bloqueado | `--bloqueo` / `--desbloqueo` |
| Eficiencia de flujo | % del lead time que no fue espera | `probar.py --metricas` |
| Defectos en pruebas | Pruebas que fallaron y luego se corrigieron | Automático |
| Calidad a la primera | ¿La primera corrida de pruebas ya pasó todo? | Automático |
| Defectos en revisión | Cambios que pidió el equipo revisor | Comentarios del PR → hoja de Excel |
| Espera de revisión | Tiempo entre que se abre el PR y se aprueba | Hoja de Excel y workflow "Métricas de flujo" |
| Throughput | Actividades terminadas por equipo y por día | `registro/TABLERO.md` |
| Desperdicios | Los 7 desperdicios Lean observados | Issues "Desperdicio" y tabla B de la hoja |

Los datos crudos quedan en `registro/` (un archivo por módulo) y suben con el PR, así que
al final todo el historial está en el repositorio.

## 9. Al final de cada día (10 min)

```bash
python probar.py --metricas pedidos
```

Esto genera `registro/metricas_pedidos.txt`. Ábrelo, selecciona todo, copia y pégalo en la
celda **Act.** de la tabla A de la hoja de tu equipo en `Plantilla_Lean_CafeTec.xlsx`. Luego
llena a mano la tabla B (desperdicios), la C (revisión del PR) y la D (retrospectiva).

Quien administra el repo, después del último merge del día:

```bash
git pull
python probar.py --tablero
```

Esto genera `registro/TABLERO.md` con los 6 equipos y la comparación día 1 contra día 2.
También puede correr el workflow **Actions → Métricas de flujo → Run workflow** para que
GitHub calcule el tiempo de cierre de cada tarjeta y la espera de cada PR.

## 10. Comandos

| Comando | Para qué |
|---|---|
| `python app.py` | Levanta la app en <http://127.0.0.1:5000> |
| `python app.py --reiniciar` | Restaura los datos de ejemplo |
| `python probar.py --iniciar pedidos 1` | Jala la tarjeta (arranca el lead time) |
| `python probar.py pedidos 1` | Pruebas de la actividad 1 de pedidos |
| `python probar.py pedidos` | Todas las pruebas de pedidos |
| `python probar.py --bloqueo pedidos "motivo"` | Empieza a contar una espera |
| `python probar.py --desbloqueo pedidos` | Termina la espera |
| `python probar.py --metricas pedidos` | Métricas del equipo y archivo para Excel |
| `python probar.py --tablero` | Resumen de los 6 equipos en `registro/TABLERO.md` |

## 11. Datos útiles para programar

```python
repo.listar("productos")                         # lista de dicts (copias)
repo.obtener("usuarios", 3)                      # dict o None
repo.agregar("pedidos", {...})                   # regresa el id nuevo
repo.actualizar("productos", 3, {"stock": 20})   # regresa el dict actualizado
repo.filtrar("pedidos", lambda p: p["pagado"])   # lista de dicts
```

Colecciones: `usuarios`, `productos`, `pedidos`, `pagos`.
Funciones de apoyo en `nucleo/utilidades.py`: `normalizar()`, `a_fecha()`, `hoy_o()`,
`total_de_items()`. Reglas de negocio en `nucleo/config.py`.
Las fechas se guardan como texto `"AAAA-MM-DD"`.

## 12. Para quien administra el repositorio

1. Sube esta carpeta a un repositorio nuevo de GitHub.
2. En *Settings → Collaborators*, agrega a todos los integrantes con permiso de escritura.
3. En *Settings → Branches*, protege `main`: pide 1 aprobación antes de hacer merge y que
   pase la revisión **Pruebas**.
4. Crea las etiquetas, las 18 tarjetas y el tablero de flujo (necesita [GitHub CLI](https://cli.github.com)):
   ```bash
   gh auth login
   gh auth refresh -s project
   python scripts/crear_tablero.py --proyecto
   ```
5. Sube `Plantilla_Lean_CafeTec.xlsx` a una carpeta compartida (Drive u OneDrive).
