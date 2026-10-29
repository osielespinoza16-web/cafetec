## Equipo y módulo

- Equipo: 1
- Módulo: usuarios
- Cierra: Closes #1, Closes #2, Closes #3

## Archivos que cambian

- [x] Solo modifiqué `modulos/<mi_modulo>.py` y mis archivos de `registro/`.
- [x] No toqué `app.py`, `nucleo/`, `pruebas/`, `templates/` ni `static/`.

## Pruebas

- [x] `python probar.py usuarios` dice ACTIVIDAD COMPLETA en las 3 actividades.
- [x] Revisé mi sección en la app (`python app.py`) y funciona.

## Métricas del equipo

Pega aquí la tabla que imprime `python probar.py --metricas usuarios`:

```
=== Métricas Lean · Equipo 1 · usuarios ===

Act Función                  Inicio    Fin   Lead  Espera  Efic.  Corridas  Defectos  Min corr.  1a vez
1   listar_usuarios               -      -      -     0.0      -         2        0          0      Sí
2   registrar_usuario             -      -      -     0.0      -         2        0          0      Sí
3   cambiar_estado_usuario        -      -      -     0.0      -         2        0          0      Sí

Lead = minutos desde --iniciar hasta que pasan todas las pruebas.
Espera = minutos bloqueados. Efic. = eficiencia de flujo (tiempo sin espera / lead).
1a vez = ¿la primera corrida de pruebas ya pasó todo? (calidad a la primera)
```

Desperdicios que notamos (esperas, retrabajo, cambio de tarea, etc.):

- Ninguno registrado. Total: 0 min.

---

**Para el equipo organizador (revisor):** usen el checklist `REVISION.md` (está en la raíz del repo). Si piden cambios, cada cambio
pedido cuenta como un defecto encontrado en revisión.
