# CafeTec · Actividad Lean Software Development

CafeTec es el sistema de pedidos de una cafetería escolar, hecho en Python (Flask).
La app, el diseño y las pruebas **ya están hechos**. Cada equipo programa las **3 funciones
de su módulo** en menos de una hora y **mide su flujo de trabajo** con métricas Lean.

| Equipo | Módulo | Archivo | Día | Revisa su PR |
|---|---|---|---|---|
| 1 | Usuarios | `modulos/usuarios.py` | 1 | Equipo 6 |
| 2 | Catálogo (menú) | `modulos/catalogo.py` | 1 | Equipo 5 |
| 3 | Pedidos | `modulos/pedidos.py` | 1 | Equipo 4 |
| 4 | Caja | `modulos/caja.py` | 2 | Equipo 3 |
| 5 | Inventario | `modulos/inventario.py` | 2 | Equipo 2 |
| 6 | Reportes | `modulos/reportes.py` | 2 | Equipo 1 |

**Enlaces:** [tablero de flujo](https://github.com/users/osielespinoza16-web/projects/2) · [bitácora en Drive](https://docs.google.com/spreadsheets/d/1FdRbUE111QeKUcwXqgW4CiPu0fcylvST/edit)

Las parejas no son al azar: Caja cobra los pedidos, Inventario descuenta los productos del
catálogo y Reportes lee usuarios y ventas. Quien **usa** un módulo es quien lo revisa.

## 1. Instalación (antes del día 1)

Necesitas Python 3.10 o superior y Git.

```bash
git clone https://github.com/osielespinoza16-web/cafetec.git
cd cafetec
pip install -r requirements.txt
python app.py
```

Abre <http://127.0.0.1:5000>. Las secciones que aún no se programan aparecen como
**Pendiente**: es normal. Después corre `python probar.py <tu_modulo> 1`; debe decir
`PENDIENTE (función sin implementar)`.

Lee completo el docstring de las 3 funciones de tu módulo **antes** de la sesión.

### Si usas Windows

1. **Abre PowerShell:** menú Inicio, escribe "PowerShell" y ábrelo.
2. **Instala Python y Git** (si no los tienes), un comando a la vez:
   ```powershell
   winget install Python.Python.3.12
   winget install Git.Git
   ```
   Al terminar, **cierra PowerShell y vuelve a abrirlo** para que reconozca los programas nuevos.
3. **Descarga el proyecto e instala lo que necesita** (solo la primera vez), un comando a la vez:
   ```powershell
   git clone https://github.com/osielespinoza16-web/cafetec.git
   cd cafetec
   pip install -r requirements.txt
   ```
4. **Enciende la app:** `python app.py` y espera a que diga `Running on http://127.0.0.1:5000`.
5. **Abre la página** en el navegador: <http://127.0.0.1:5000>.

Las siguientes veces solo necesitas:

```powershell
cd cafetec
git pull
python app.py
```

Tómalo en cuenta:

- Si no reconoce `python` o `pip`, usa `py` en su lugar: `py app.py`, `py -m pip install -r requirements.txt`.
- Si no reconoce `git` después de instalarlo, cierra PowerShell y vuelve a abrirlo.
- **No cierres PowerShell** mientras usas la página. Para apagarla, presiona **Ctrl + C**.
- `127.0.0.1` es tu propia computadora: cada quien ve su copia. Los cambios de otros equipos te
  llegan cuando hacen merge y tú corres `git pull`.
- Escribe un comando por línea y presiona Enter en cada uno; dos comandos en la misma línea dan error.

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
| Eliminar desperdicio | Módulos independientes para que nadie espere a nadie; cada equipo registra sus desperdicios con `--desperdicio` y esperas, retrabajo y cambios de tarea se registran solos |
| Construir con calidad | Pruebas automáticas en cada corrida y en cada PR (GitHub Actions) |
| Amplificar el aprendizaje | La retrospectiva del día 1 alimenta la forma de trabajar del día 2 |
| Decidir lo más tarde posible | Cada función se diseña al jalarla, y la mejora del día 2 se decide hasta ver los datos del día 1 |
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

La clase puede ser remota: nadie necesita ver la pantalla de otro equipo. Cada equipo trabaja
en su propia llamada o sala, y los desperdicios los registra el mismo equipo con `probar.py`.

| Minuto | Equipos que programan | Equipos revisores (no programan ese día) |
|---|---|---|
| 0–5 | `git pull`, crear rama, iniciar la actividad 1 | Confirman que su rama existe y que `python app.py` funciona |
| 5–35 | Actividades 1, 2 y 3 (≈10 min cada una), un commit por actividad; el encargado de flujo anota desperdicios con `--desperdicio` | Leen el módulo que van a revisar y preparan el suyo (detalle abajo) |
| 35–45 | Abren el PR con sus métricas | **Revisan** el PR en GitHub con `REVISION.md` y lo aprueban |
| 45–55 | Merge, `--metricas` y pegar en la bitácora (Excel) | Retrospectiva juntos y eligen la mejora que aplicarán |

Al terminar el día 1, el grupo elige **1 o 2 mejoras** de la retrospectiva y los equipos del
día 2 las aplican (eso es *kaizen*). Al final se comparan los dos días con datos.

### Qué hacen los equipos revisores

El día que un equipo **no programa** es **revisor**: el día 1 lo son los equipos 4, 5 y 6, y el
día 2 los equipos 1, 2 y 3. Con la clase remota no observan a nadie; su trabajo es revisar el
código de su pareja y prepararse para su propio día.

| Revisor | Revisa a | Por qué esa pareja |
|---|---|---|
| Equipo 4 · Caja | Equipo 3 · Pedidos | Caja cobra los pedidos |
| Equipo 5 · Inventario | Equipo 2 · Catálogo | Inventario descuenta productos del catálogo |
| Equipo 6 · Reportes | Equipo 1 · Usuarios | Reportes lee usuarios y ventas |

El día 2 se invierte: el Equipo 3 revisa al 4, el 2 al 5 y el 1 al 6.

**Paso a paso del revisor**

1. **Minutos 0–5 · Estar listos.** Su developer confirma que su rama ya existe (por ejemplo,
   `equipo-4-caja`) y que `python app.py` funciona en su computadora.
2. **Minutos 5–35 · Prepararse.**
   - Leen los docstrings del módulo que van a revisar (el Equipo 4 lee `modulos/pedidos.py`)
     para saber qué debe cumplir el código.
   - Leen las 3 funciones de su propio módulo para el día que les toca programar.
   - Escriben en la hoja **Retrospectiva** de la bitácora, en su renglón, cómo planean
     organizarse cuando les toque programar.
   - Quedan disponibles por si el equipo que programa tiene dudas.
3. **Minutos 35–45 · Revisar el Pull Request.** Estén atentos: en cuanto su pareja abra el PR,
   cada minuto que tarden cuenta como **espera** (desperdicio).
   - En GitHub, pestaña **Pull requests**, abren el PR de su pareja y van a **Files changed**.
   - Revisan el código con [REVISION.md](REVISION.md) y confirman que la revisión automática
     (**Pruebas**) esté en verde.
   - Si algo falla: comentan en la línea y eligen **Review changes → Request changes**. Cada
     cambio pedido cuenta como **defecto encontrado en revisión**.
   - Si está bien: **Review changes → Approve**.
   - Anotan en la bitácora, hoja **Revisiones**: hora en que se abrió el PR, hora en que lo
     aprobaron y cuántos cambios pidieron.
4. **Minutos 45–55 · Retrospectiva.** Participan y ayudan a elegir la mejora que ellos mismos
   aplicarán cuando les toque programar.

**Por qué importa en LSD:** sin su aprobación nada entra a `main` (*construir con calidad*);
si tardan en revisar, generan espera (*eliminar desperdicio*); y como usan ese módulo cuando
les toca programar, revisarlo antes les ayuda a trabajar mejor (*amplificar el aprendizaje*).

## 5. Roles dentro del equipo (rotan en cada actividad)

- **Programador:** escribe el código.
- **Navegante:** lee la especificación en voz alta y revisa cada línea mientras se escribe.
- **Encargado de flujo:** mueve la tarjeta, corre `--iniciar`, `--bloqueo` y las pruebas, y
  registra con `--desperdicio` todo lo que les haga perder tiempo.

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
5. **Si pierden tiempo por otra cosa**, el encargado de flujo lo registra en el momento:
   ```bash
   python probar.py --desperdicio pedidos "cambio de tarea" 3 "revisamos la act. 3 sin terminar la 2"
   ```
   Tipos: `espera`, `retrabajo`, `parcial`, `cambio de tarea`, `extra`, `transferencia`, `demora`.
   No hace falta anotar lo que `probar.py` ya registra solo: esperas (`--bloqueo`), pruebas que
   fallaron (retrabajo), intentos frenados por el límite WIP (cambio de tarea) y actividades que
   quedaron sin terminar.
6. **Cerrar.** Commit y mueve la tarjeta a *Revision* en el tablero de flujo:
   ```bash
   git add modulos/pedidos.py registro/
   git commit -m "Actividad 1: crear_pedido"
   ```

## 7. Git: una rama y un PR por equipo

Cada equipo elige **un developer**: el integrante que hace los commits y abre el Pull Request.
Ese integrante debe estar invitado como colaborador del repositorio.

### Nombre de la rama (debe ser idéntico)

| Equipo | Rama |
|---|---|
| 1 · Usuarios | `equipo-1-usuarios` |
| 2 · Catálogo | `equipo-2-catalogo` |
| 3 · Pedidos | `equipo-3-pedidos` |
| 4 · Caja | `equipo-4-caja` |
| 5 · Inventario | `equipo-5-inventario` |
| 6 · Reportes | `equipo-6-reportes` |

Todo en minúsculas, con guiones, sin acentos ni espacios.

### Crear la rama antes de la clase (solo el developer)

1. Acepta la invitación al repositorio (llega a tu correo o en <https://github.com/notifications>).
2. En la terminal, un comando a la vez (ejemplo con el Equipo 3; cambia el nombre por el de tu rama):
   ```bash
   git clone https://github.com/osielespinoza16-web/cafetec.git
   cd cafetec
   git checkout -b equipo-3-pedidos
   git push -u origin equipo-3-pedidos
   ```
3. Revisa en GitHub, en el botón de ramas (arriba a la izquierda, donde dice `main`), que tu rama
   aparezca con el nombre exacto.
4. Verifica en tu terminal que estás en tu rama: `git branch` debe marcar tu rama con `*`.

Si ya habías clonado antes, en lugar de `git clone` entra a la carpeta y corre `git pull` antes de
`git checkout -b`.

### El día de la sesión

```bash
git checkout equipo-3-pedidos
git pull origin main
# ... actividades 1, 2 y 3, con un commit cada una ...
git push
```

`git pull origin main` trae lo que otros equipos ya unieron (importante para el día 2).
Luego abren el Pull Request en GitHub de su rama hacia `main` (la plantilla ya trae lo que deben
llenar) y escriben `Closes #N` por cada tarjeta. El equipo revisor aprueba y el developer hace
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
| Defectos en revisión | Cambios que pidió el equipo revisor | Comentarios del PR → hoja Revisiones |
| Espera de revisión | Tiempo entre que se abre el PR y se aprueba | Hoja Revisiones y workflow "Métricas de flujo" |
| Throughput | Actividades terminadas por equipo y por día | `registro/TABLERO.md` |
| Desperdicios | Los 7 desperdicios Lean, con sus minutos | `--desperdicio` + detección automática → hoja Desperdicios |

Los datos crudos quedan en `registro/` (un archivo por módulo) y suben con el PR, así que
al final todo el historial está en el repositorio.

## 9. Al final de cada día (10 min)

```bash
python probar.py --metricas pedidos
```

Esto muestra sus métricas y sus desperdicios, y genera dos archivos para la
**[bitácora del grupo en Google Drive](https://docs.google.com/spreadsheets/d/1FdRbUE111QeKUcwXqgW4CiPu0fcylvST/edit)**. Se llena ahí, no en el archivo
`Plantilla_Lean_CafeTec.xlsx` del repositorio (ese es solo la plantilla de respaldo).
En cada archivo: ábrelo, selecciona todo y copia.

- `registro/metricas_pedidos.txt` → hoja **Flujo**, en la celda marcada con ◀ en la fila de tu equipo.
- `registro/desperdicios_pedidos.txt` → hoja **Desperdicios**, en la primera fila libre de la columna
  **Día**. Después escriban la contramedida de los que costaron más minutos.

La bitácora tiene una hoja por tema, compartida por todo el grupo:

| Hoja | Quién la llena | Cuándo |
|---|---|---|
| **Portada** | Cada equipo escribe sus integrantes | Antes del día 1 |
| **Flujo** | Cada equipo pega su salida de `--metricas` | Al terminar sus 3 actividades |
| **Desperdicios** | Cada equipo pega `registro/desperdicios_<modulo>.txt` y escribe la contramedida | Al terminar sus 3 actividades |
| **Revisiones** | El equipo revisor (horas del PR y cambios pedidos) | Al aprobar el PR |
| **Retrospectiva** | Cada equipo su renglón; el grupo, el acuerdo y la conclusión | Al final de cada día |
| **Resultados** | Nadie: se calcula sola, con gráficas | — |

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
| `python probar.py --desperdicio pedidos "tipo" 3 "qué pasó"` | Registra un desperdicio con sus minutos |
| `python probar.py --metricas pedidos` | Métricas y desperdicios del equipo, con sus archivos para Excel |
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
