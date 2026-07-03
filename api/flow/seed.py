"""
Seed del catálogo de status del flujo de validación.

Datos curados a partir del board de Miró (ies/flux_rules/analysis.json)
con las correcciones de PLAN_flujo_validacion.md — incluida la
dirección de las reglas padre-hijo (en dependencies[] del JSON,
from = hijo, to = padre).

Idempotente: upsert por PK y reconstrucción de los M2M con .set().
Los campos estéticos (color, icon) solo se asignan al crear, para no
pisar ajustes hechos en el admin.
"""
from django.contrib.contenttypes.models import ContentType

from flow.models import Status

# Labels de los modelos participantes (abreviados para las tablas).
P = "example.goodpracticepackage"     # GoodPracticePackage
GP = "example.goodpractice"           # GoodPractice
A = "survey.axisvalue"                # AxisValue
O = "answer.observableresponse"       # ObservableResponse
G = "answer.groupresponse"            # GroupResponse
GPK = "survey.generalpackage"         # GeneralPackage (raíz gen)
GEN = "survey.generalgroupresponse"   # GeneralGroupResponse (hijo gen)

# Flags: default, public, comment (comment_type=required),
#        comment_opt (comment_type=optional), up (propagates_up),
#        down (propagates_down), auto (auto_on_first_save),
#        edit (content_editable), confirm (requires_confirmation)
# Tuplas: (name, public_name, action_name, description, role, flags, aplica)
#   public_name = estado que muestra el chip; action_name = verbo del
#   botón/menú que transiciona HACIA ese status (None si nunca es destino
#   de una acción manual).
STATUSES = {
    "bp": [
        ("bp_draft", "Borrador", None,
         "En captura. La IES edita libremente y marca cada práctica "
         "como completada antes de enviar el paquete.",
         "ies", {"default", "down", "edit"}, [P, GP]),
        ("bp_completed", "Completada", "Marcar como completada",
         "La IES dio por terminada esta práctica; entrará a revisión "
         "cuando se envíe el paquete.",
         "reviewer", {"edit"}, [GP]),
        ("bp_sent", "Enviado a revisión", "Enviar a revisión",
         "El paquete se envió; las prácticas están en manos de la "
         "revisión.",
         "reviewer", {"confirm", "comment_opt"}, [P]),
        ("bp_adjusted", "Ajuste atendido", "Marcar como atendido",
         "La IES incorporó las correcciones; la práctica espera una "
         "nueva revisión.",
         "reviewer", {"edit", "comment_opt"}, [GP]),
        ("bp_resent", "Reenviado a revisión", "Reenviar a revisión",
         "El paquete se reenvió con los ajustes incorporados.",
         "reviewer", set(), [P]),
        ("bp_for_ruling", "Recibida", "Recibir",
         "La práctica cumplió los criterios y pasa a la etapa de "
         "dictamen.",
         None, {"public"}, [GP]),
        ("bp_finished", "Finalizado", "Finalizar",
         "La revisión del paquete concluyó; sin acciones pendientes.",
         None, set(), [P]),
        ("bp_need_changes", "Requiere ajustes", "Solicitar ajustes",
         "La revisión devolvió el paquete con correcciones para que "
         "la IES las atienda.",
         "ies", { "comment", "edit" }, [P, GP]),
        ("bp_rejected", "No acreditada", "Marcar como no acreditada",
         "La práctica no cumplió los criterios mínimos de la "
         "convocatoria.",
         None, {"comment"}, [GP]),
        ("bp_discarded", "Descartado", "Descartar",
         "La IES optó por no reportar buenas prácticas; su "
         "participación queda cerrada (reabrible mientras el periodo "
         "siga abierto).",
         "ies", { "down", "confirm" }, [P, GP]),
    ],
    "cp": [
        ("cp_pre_start", "Por iniciar", None,
         "El eje aún no tiene respuestas capturadas.",
         "ies", {"default", "edit"}, [A, O, G]),
        ("cp_filling", "En llenado", None,
         "La IES está capturando las respuestas del eje.",
         "ies", {"auto", "up", "edit"}, [A, O, G]),
        ("cp_completed", "Completado", "Marcar como completado",
         "La IES dio por terminada la respuesta; entrará a revisión "
         "cuando se envíe el eje.",
         "reviewer", {"edit"}, [O, G]),
        ("cp_sent", "Enviado a revisión", "Enviar a revisión",
         "El eje se envió; sus respuestas están en manos de la "
         "revisión.",
         "reviewer", set(), [A]),
        ("cp_in_review", "En revisión", "Iniciar revisión",
         "La revisión del eje está en curso.",
         "reviewer", set(), [A]),
        ("cp_need_changes", "Requiere ajustes", "Solicitar ajustes",
         "La revisión devolvió la respuesta con correcciones para que "
         "la IES las atienda.",
         "ies", {"comment", "edit"}, [A, O, G]),
        ("cp_in_adjustment", "En ajustes", "Iniciar ajustes",
         "La IES está capturando las correcciones solicitadas.",
         "ies", {"auto", "up", "edit"}, [A, O, G]),
        ("cp_adjusted", "Ajuste completo", "Marcar ajuste como completo",
         "La IES incorporó las correcciones; la respuesta espera una "
         "nueva revisión.",
         "reviewer", {"edit"}, [O, G]),
        ("cp_resent", "Reenviado a revisión", "Reenviar a revisión",
         "El eje se reenvió con los ajustes incorporados.",
         "reviewer", set(), [A]),
        ("cp_postponed", "Pospuesta", "Posponer",
         "La IES decidió responder esto más adelante.",
         "ies", set(), [O, G]),
        ("cp_voluntary_readjust", "Reajuste solicitado",
         "Solicitar reajuste",
         "La IES pidió reabrir una respuesta ya aprobada; la revisión "
         "debe autorizarlo.",
         "reviewer", {"comment", "up"}, [A, O, G]),
        ("cp_partial", "Parcialmente respondido",
         "Enviar parcial a corroborar",
         "Hay respuestas listas para corroborar mientras el resto "
         "sigue en captura.",
         "reviewer", {"comment"}, [O, G]),
        ("cp_partial_approved", "Parcialmente aprobado",
         "Aprobar parte entregada",
         "La parte entregada se validó; el resto sigue pendiente del "
         "lado de la IES.",
         "ies", {"edit"}, [O, G]),
        ("cp_approved", "Aprobado", "Aprobar",
         "La respuesta fue validada por la revisión.",
         "ies", {"public"}, [A, O, G]),
    ],
    "gen": [
        ("gen_draft", "Borrador", None,
         "En captura. La IES edita las preguntas generales y marca "
         "cada grupo como completado antes de enviar.",
         "ies", {"default", "edit"}, [GPK, GEN]),
        ("gen_completed", "Completado", "Marcar como completado",
         "La IES dio por terminado este grupo; entrará a revisión "
         "cuando se envíen las generales.",
         "reviewer", {"edit"}, [GEN]),
        ("gen_sent", "Enviado a revisión", "Enviar a revisión",
         "Las preguntas generales se enviaron; están en manos de la "
         "revisión.",
         "reviewer", set(), [GPK]),
        ("gen_need_changes", "Requiere ajustes", "Solicitar ajustes",
         "La revisión devolvió las generales con correcciones para "
         "que la IES las atienda.",
         "ies", {"comment", "edit"}, [GPK, GEN]),
        ("gen_adjusted", "Ajuste completo", "Marcar ajuste como completo",
         "La IES incorporó las correcciones; el grupo espera una "
         "nueva revisión.",
         "reviewer", {"edit"}, [GEN]),
        ("gen_resent", "Reenviado a revisión", "Reenviar a revisión",
         "Las preguntas generales se reenviaron con los ajustes "
         "incorporados.",
         "reviewer", set(), [GPK]),
        ("gen_approved", "Aprobado", "Aprobar",
         "El grupo fue validado por la revisión.",
         None, {"public"}, [GEN]),
        ("gen_finished", "Finalizado", "Finalizar",
         "La revisión de las preguntas generales concluyó; sin "
         "acciones pendientes.",
         None, set(), [GPK]),
    ],
}

NEXT_STATUSES = {
    # Buenas prácticas
    "bp_draft": ["bp_completed", "bp_sent", "bp_discarded"],
    "bp_discarded": ["bp_draft"],
    "bp_completed": ["bp_need_changes", "bp_for_ruling", "bp_rejected"],
    "bp_adjusted": ["bp_need_changes", "bp_for_ruling", "bp_rejected"],
    "bp_need_changes": ["bp_adjusted", "bp_resent", "bp_discarded"],
    "bp_sent": ["bp_finished", "bp_need_changes"],
    "bp_resent": ["bp_finished"],
    # Cuestionario principal
    "cp_pre_start": ["cp_filling"],
    "cp_filling": ["cp_completed", "cp_sent", "cp_postponed", "cp_partial"],
    "cp_completed": ["cp_approved", "cp_need_changes"],
    "cp_sent": ["cp_in_review"],
    "cp_in_review": ["cp_approved", "cp_need_changes"],
    "cp_adjusted": ["cp_approved", "cp_need_changes"],
    "cp_resent": ["cp_in_review"],
    "cp_postponed": ["cp_completed", "cp_partial"],
    "cp_approved": ["cp_voluntary_readjust"],
    "cp_voluntary_readjust": ["cp_need_changes"],
    "cp_need_changes": ["cp_in_adjustment"],
    "cp_in_adjustment": ["cp_adjusted", "cp_resent", "cp_postponed"],
    "cp_partial": ["cp_need_changes", "cp_partial_approved"],
    "cp_partial_approved": ["cp_completed", "cp_partial"],
    # Generales (espejo de bp: paquete que se envía + aprobación por grupo)
    "gen_draft": ["gen_completed", "gen_sent"],
    "gen_completed": ["gen_need_changes", "gen_approved"],
    "gen_adjusted": ["gen_need_changes", "gen_approved"],
    "gen_need_changes": ["gen_adjusted", "gen_resent"],
    "gen_sent": ["gen_finished", "gen_need_changes"],
    "gen_resent": ["gen_finished"],
}

# Para mover el PADRE al status clave, TODOS sus hijos deben estar en
# alguno de los status de la lista (auto-loops incluidos).
VALID_CHILD_STATUSES = {
    "bp_sent": ["bp_completed", "bp_discarded"],
    "bp_discarded": ["bp_discarded", "bp_draft", "bp_need_changes"],
    "bp_resent": ["bp_adjusted", "bp_completed"],
    "bp_finished": ["bp_for_ruling", "bp_rejected"],
    "cp_approved": ["cp_approved"],
    "cp_completed": ["cp_completed"],
    "cp_adjusted": ["cp_adjusted", "cp_completed", "cp_approved"],
    "cp_sent": ["cp_completed", "cp_postponed", "cp_partial"],
    "cp_resent": ["cp_completed", "cp_adjusted", "cp_approved",
                  "cp_postponed", "cp_partial"],
    "cp_need_changes": ["cp_need_changes", "cp_approved", "cp_postponed"],
    "cp_partial": ["cp_completed", "cp_postponed"],
    "cp_partial_approved": ["cp_partial_approved"],
    # Generales (espejo de bp)
    "gen_sent": ["gen_completed"],
    "gen_resent": ["gen_adjusted", "gen_completed", "gen_approved"],
    "gen_finished": ["gen_approved"],
}

# Guía de siguiente paso por status (frontend la muestra bajo el control)
HINTS = {
    "bp_discarded": "Participación cerrada. Puedes reabrir para cambiar tu "
                    "respuesta mientras el periodo siga abierto.",
    "bp_completed": "Práctica completada por la IES; en espera de que se "
                    "envíe el paquete para revisarla.",
    "bp_sent": "Paquete en revisión. Dictamina cada práctica o solicita "
               "ajustes.",
    "bp_need_changes": "La revisión solicitó correcciones. Ajusta las "
                       "prácticas y reenvía el paquete.",
    "bp_adjusted": "Ajustes incorporados; en espera de nueva revisión.",
    "bp_resent": "Paquete reenviado con ajustes. Continúa la revisión.",
    "bp_for_ruling": "Práctica recibida para dictamen. Sin acciones "
                     "pendientes aquí.",
    "bp_rejected": "No pasó los filtros mínimos de la convocatoria.",
    "bp_finished": "Revisión del paquete concluida.",
    "gen_draft": "Edita las preguntas generales, marca cada grupo como "
                 "completado y envía a revisión.",
    "gen_sent": "Preguntas generales en revisión. Aprueba cada grupo o "
                "solicita ajustes.",
    "gen_need_changes": "La revisión solicitó correcciones. Ajusta y "
                        "reenvía las preguntas generales.",
    "gen_finished": "Revisión de las preguntas generales concluida.",
}

# Diálogo de confirmación (título, cuerpo) para los status con flag
# "confirm". El título cae a un default derivado de action_name si es None.
CONFIRM_DIALOGS = {
    "bp_discarded": (
        "¿De verdad quieres descartar esta buena práctica?",
        "Esta buena práctica quedará descartada. Podrás reabrirla "
        "mientras el periodo siga abierto.",
    ),
    "bp_sent": (
        "¿De verdad quieres enviar a revisión las buenas prácticas?",
        "Una vez enviadas, no podrás realizar modificaciones ni agregar "
        "nuevas.",
    ),
}

# Rótulo de la caja de comentario (front), por defecto según a quién le
# toca el turno tras la transición (role del status destino = quién leerá
# el mensaje). Solo se asigna cuando comment_type != "none".
COMMENT_PROMPT_BY_ROLE = {
    "reviewer": "Si gustas, agrega un mensaje para la persona revisora.",
    "ies": "Si gustas, agrega un mensaje para la institución.",
}

# Override fino por status (gana sobre el default por rol).
COMMENT_PROMPTS = {
    "bp_sent": "Si gustas, puedes agregar un mensaje para la persona "
               "revisora que revisará tus buenas prácticas.",
    "bp_adjusted": "Si gustas, describe a la persona revisora los "
                   "ajustes que realizaste.",
}

# Reglas de UX (nombres del registry flowRules en el frontend) que deben
# cumplirse para mover un objeto a ese status. El motor no las valida.
ENTRY_RULES = {
    "bp_completed": ["practice_complete"],
    "bp_adjusted": ["practice_complete"],
    "bp_for_ruling": ["features_rated"],
}

# Color inicial según el rol (tonos del board de Miró → vuetify).
ROLE_COLORS = {
    "ies": "blue-lighten-4",
    "reviewer": "deep-purple-lighten-4",
    None: "yellow-lighten-3",
}


def _content_type(label: str) -> ContentType:
    app_label, model = label.split(".")
    return ContentType.objects.get_by_natural_key(app_label, model)


def seed_flow() -> dict:
    """
    Crea o actualiza el catálogo completo de Status y sus M2M.
    Devuelve conteos {created, updated} para reporte.
    """
    created_count = 0
    updated_count = 0
    applicability: dict[str, list] = {}

    # Limpia is_default de los grupos gestionados antes del upsert: evita
    # chocar con unique_default_per_group cuando el default de un grupo
    # cambió de nombre (p.ej. gen_pre_start → gen_draft). El loop lo
    # reasigna enseguida.
    Status.objects.filter(group__in=STATUSES).update(is_default=False)

    for group, rows in STATUSES.items():
        for order, row in enumerate(rows, start=1):
            (name, public_name, action_name, description, role, flags,
             applies) = row
            confirm_title, confirm_text = CONFIRM_DIALOGS.get(
                name, (None, None))
            if "comment" in flags:
                comment_type = "required"
            elif "comment_opt" in flags:
                comment_type = "optional"
            else:
                comment_type = "none"
            comment_prompt = None
            if comment_type != "none":
                comment_prompt = (COMMENT_PROMPTS.get(name)
                                  or COMMENT_PROMPT_BY_ROLE.get(role))
            status, created = Status.objects.update_or_create(
                name=name,
                defaults={
                    "group": group,
                    "public_name": public_name,
                    "action_name": action_name,
                    "description": description,
                    "role": role,
                    "order": order,
                    "is_default": "default" in flags,
                    "is_public": "public" in flags,
                    "comment_type": comment_type,
                    "comment_prompt": comment_prompt,
                    "requires_confirmation": "confirm" in flags,
                    "confirm_title": confirm_title,
                    "confirm_text": confirm_text,
                    "propagates_up": "up" in flags,
                    "propagates_down": "down" in flags,
                    "auto_on_first_save": "auto" in flags,
                    "content_editable": "edit" in flags,
                    "hint": HINTS.get(name),
                    "entry_rules": ENTRY_RULES.get(name, []),
                },
            )
            if created:
                status.color = ROLE_COLORS[role]
                status.save()
                created_count += 1
            else:
                updated_count += 1
            applicability[name] = applies

    for name, labels in applicability.items():
        cts = [_content_type(label) for label in labels]
        Status.objects.get(name=name).applicable_models.set(cts)

    for name, targets in NEXT_STATUSES.items():
        Status.objects.get(name=name).next_statuses.set(targets)

    all_names = set(applicability)
    for name in all_names:
        children = VALID_CHILD_STATUSES.get(name, [])
        Status.objects.get(name=name).valid_child_statuses.set(children)

    # Baja de status obsoletos de los grupos gestionados (p.ej. el gen
    # viejo de un solo nivel, reemplazado por el flujo con GeneralPackage).
    # Si algún FlowEvent aún los referencia (PROTECT), la baja falla: hay
    # que migrar esos eventos antes de re-sembrar.
    Status.objects.filter(group__in=STATUSES).exclude(
        name__in=all_names).delete()

    return {"created": created_count, "updated": updated_count}
