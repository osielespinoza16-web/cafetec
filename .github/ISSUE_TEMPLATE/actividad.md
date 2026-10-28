---
name: Actividad (tarjeta del tablero)
about: Una función de un módulo. Se jala, se programa y se cierra con el Pull Request.
title: "[modulo] Actividad N · nombre_de_la_funcion"
labels: actividad
---

**Equipo:**
**Módulo / archivo:** `modulos/<modulo>.py`
**Función:** `<funcion>()` — la especificación completa está en su docstring.

### Flujo de la tarjeta

1. Mueve esta tarjeta a **En progreso** y corre `python probar.py --iniciar <modulo> <N>`.
2. Programa la función.
3. Corre `python probar.py <modulo> <N>` hasta que diga **ACTIVIDAD COMPLETA**.
4. Mueve la tarjeta a **Revisión**. Se cierra sola cuando hacen merge del Pull Request.

Si se quedan detenidos esperando algo: `python probar.py --bloqueo <modulo> "motivo"`.
