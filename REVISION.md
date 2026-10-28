# Checklist de revisión del Pull Request

Lo usa el **equipo revisor** (ver la tabla de parejas en el README). Revisen el PR con esta
lista antes de aprobar. Cada punto que no se cumpla se pide como cambio en un comentario del
PR y **cuenta como un defecto encontrado en revisión** (anótenlo en la tabla C de su hoja).

## Antes de leer el código

- [ ] La revisión automática de GitHub (Actions · Pruebas) está en verde.
- [ ] El PR solo cambia `modulos/<modulo>.py` y archivos de `registro/` de ese módulo.
- [ ] La descripción trae la tabla de métricas y el "Closes #N" de cada tarjeta.

## Leyendo cada función

- [ ] Cada regla del docstring tiene su línea de código.
- [ ] Cada caso inválido lanza `ValueError` con un mensaje que se entiende.
- [ ] Valida todo **antes** de guardar (si hay error, no queda nada guardado a medias).
- [ ] Revisa que el registro exista (`repo.obtener()` puede regresar `None`).
- [ ] Convierte los tipos que pide la especificación (texto a `int` / `float`) y atrapa
      también `TypeError` cuando el valor puede ser `None`.
- [ ] Las fechas se guardan como texto `"AAAA-MM-DD"` (`.isoformat()`).
- [ ] Ordena como pide la especificación, incluido el desempate, usando `normalizar()`.
- [ ] Regresa exactamente lo que pide la especificación (tipo y forma).
- [ ] No hay código que la especificación no pida (eso es *funcionalidad extra*, un desperdicio).

## Al aprobar

1. Aprueben el PR (Review changes -> Approve).
2. El equipo dueño hace **Squash and merge**.
3. Anoten en su hoja la hora en que se abrió el PR y la hora en que lo aprobaron
   (es el tiempo que el trabajo **esperó** revisión).
