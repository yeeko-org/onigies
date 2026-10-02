---
type: record
id: 2026-10-02-comentarios-editables-y-valvula-de-admin
date: 2026-10-02
related: ["[[task-70]]", "[[task-99]]"]
---

# Comentarios editables por turno y válvula de admin en el flujo

Sesión de diálogo del 2026-10-02 (session-log `01LBwEJ1Fob8VFVxUuA2cfie`), sin implementación. Ricardo trajo dos peticiones y las cerró en tres rondas de preguntas.

## Lo que pidió

> ¿Es posible que los comentarios sean editables por «la revisora» (sin importar quién sea la revisora) mientras siga siendo el turno de las revisoras?

> También me gustaría que los usuarios con is_staff puedan hacer cambios libres a cualquier status que pueda establecer la revisora a nivel de hijos o nietos (por ejemplo, una buena práctica o un grupo de preguntas generales, o un observable) siempre y cuando esté todo el grupo completo (por el nivel más alto) en el turno de las revisoras.

## Estado de partida verificado

- Un comentario es un `FlowEvent` con `comment`; no hay PATCH ni DELETE sobre eventos en ningún nivel, ni campos de auditoría; el admin del timeline es de solo lectura por decisión.
- El guard del POST de comentarios (`api/flow/views.py`, `FlowEventView.post`) compara el rol del usuario con el status **propio** del objeto, no con la raíz; `canEditContent` y [[adr-0019]] usan la raíz. Esa divergencia ya estaba anotada en [[task-124]].
- `is_staff` no tiene ningún poder propio en el flujo: `User.is_reviewer` es `is_superuser or is_staff or reviewer`. Las nueve revisoras reales de producción no son staff ([[2026-09-28-revisoras-sin-is-staff-en-generales]]), así que «staff» en la práctica significa Ricardo o un admin.
- La raíz de `cp` es `AxisValue`, uno por eje, no la encuesta. El nivel «nieto» solo existe en `cp`; en `bp` las features no tienen status.
- `cp-backend` no contenía `a6cd4cd` (el fix de `is_reviewer`); se rebasó sobre `main` en esta misma sesión.

## Decisiones de Ricardo

**Cambio 1, comentarios.** La regla del turno para editar y borrar es la raíz, como [[adr-0019]] («P1. La raíz»). Aplica a ambos lados, IES y revisión, cada uno sobre los comentarios de su lado sin importar la autoría («P2. Ambos»). Borrar sí, «borrar solo el comentario»: en un comentario puro se borra la fila; en uno de transición se vacía el texto y el evento se queda. Sin `edited_at`: «Siento innecesario el edited_at»; el modelo coincidió porque mientras la raíz siga de tu lado la contraparte aún no ha actuado sobre ese comentario. El campo privado `comments` de los criterios de bp sigue la misma regla («P11. sí»). Esto extiende [[task-70]] (que decía «propios») y no la contradice.

La excepción que el modelo propuso para el comentario de la transición raíz que dispara el correo se retiró: con la regla de la raíz sale sola, porque ese correo se envía justo cuando la raíz deja el lado revisor.

**Cambio 2, válvula de admin.** Lectura confirmada: cualquier status que la revisión puede establecer, desde cualquier origen, **terminales incluidos** («P5. La lectura es la 3»), con un botón especial junto al menú de transiciones, solo para admin, «con un diálogo muy claro que diga que no se recomienda y que si está bien segura de eso». Conserva la regla de hijos y la propagación («P6. Sí como propones»); la unidad en `cp` es el eje («P7. confirmo»); vive en la UI normal, oculto, con candado en los endpoints («P8. … tiene sentido?» → sí). Sin columna `is_override`: el timeline deriva «cambio administrativo» cuando el destino no está entre los siguientes legales del origen. El check se llama `is_admin` en ambos lados, nunca `is_staff` en componentes. La motivación confirmada por Ricardo es [[task-58]]: un grupo gen devuelto sin devolver el paquete queda en rol IES bajo una raíz en turno revisor y nadie puede deshacerlo.

Esto acota [[adr-0002]]: los terminales siguen sin salida en el flujo normal; la válvula es la única excepción. Queda en el ADR nuevo.

**Cierre del diálogo (misma sesión, tras el diseño UX).** El brief al diseño dijo «status de rol reviewer», que no es lo que Ricardo pidió; corregido: el selector lista lo que la revisión establece **y** los status de rol reviewer para deshacer («P12. Las dos»). El timeline y el motivo son visibles para la IES («P13. Transparencia total»). Nombre en la UI: «Cambio administrativo» («P14. Tu recomendación»). Resueltos por un solo camino: request con `target_status`, montaje dentro de `FlowStatusActions`, raíces finalizadas excluidas, detección «fuera del grafo y con comentario». La sesión paralela (sector TSU) comparte el árbol de trabajo y dejó `sector-tsu` como rama activa; los docs de hoy se commitean a `cp-backend` sin mover el checkout.

**Ramas.** «tú decide cómo, si rebase o merge»: se hizo rebase porque `cp-backend` era local, sin upstream y sin conflictos ([[task-186]]).

## Lo que sigue

Diseño del botón y del diálogo con `ux-designer`, y la implementación de ambos cambios briefeada con los nodos de esta sesión.
