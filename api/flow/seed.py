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
GEN = "survey.generalgroupresponse"   # GeneralGroupResponse

# Flags: default, public, comment (requires_comment), up (propagates_up),
#        down (propagates_down), auto (auto_on_first_save)
# Tuplas: (name, public_name, description, role, flags, aplica)
STATUSES = {
    "bp": [
        ("bp_draft", "Borrador",
         "En captura; la IES puede editar libremente.",
         "ies", {"default", "down"}, [P, GP]),
        ("bp_discarded", "Descartado",
         "La IES descartó enviarlas.",
         "ies", {"down"}, [P, GP]),
        ("bp_completed", "Completada",
         "La IES la marcó como completa; se revisará cuando se envíe "
         "el paquete.",
         "reviewer", set(), [GP]),
        ("bp_sent", "Enviado",
         "Paquete enviado; las prácticas están en revisión.",
         "reviewer", set(), [P]),
        ("bp_need_changes", "Requiere ajustes",
         "La revisión solicitó correcciones a la IES.",
         "ies", {"comment"}, [P, GP]),
        ("bp_adjusted", "Ajuste completo",
         "Correcciones incorporadas; en espera de nueva revisión.",
         "reviewer", set(), [GP]),
        ("bp_resent", "Enviado con ajustes",
         "Paquete reenviado tras incorporar las correcciones.",
         "reviewer", set(), [P]),
        ("bp_for_ruling", "Recibida para dictamen",
         "Cumplió los criterios; pasa a la etapa de dictamen.",
         None, {"public"}, [GP]),
        ("bp_rejected", "No pasó los filtros",
         "Recibida, pero no cumplió los criterios mínimos de la "
         "convocatoria.",
         None, {"comment"}, [GP]),
        ("bp_finished", "Finalizado",
         "Revisión del paquete concluida; sin acciones pendientes.",
         None, set(), [P]),
    ],
    "cp": [
        ("cp_pre_start", "Por iniciar",
         "Aún no se captura ninguna respuesta.",
         "ies", {"default"}, [A, O, G]),
        ("cp_filling", "En llenado",
         "Captura en curso por la IES.",
         "ies", {"auto", "up"}, [A, O, G]),
        ("cp_completed", "Completado",
         "Terminado por la IES; en espera de revisión.",
         "reviewer", set(), [O, G]),
        ("cp_sent", "Enviado",
         "Eje enviado para revisión.",
         "reviewer", set(), [A]),
        ("cp_in_review", "En revisión",
         "La revisión del eje está en curso.",
         "reviewer", set(), [A]),
        ("cp_need_changes", "Requiere ajustes",
         "La revisión solicitó correcciones a la IES.",
         "ies", {"comment"}, [A, O, G]),
        ("cp_in_adjustment", "En ajustes",
         "Captura de correcciones en curso.",
         "ies", {"auto", "up"}, [A, O, G]),
        ("cp_adjusted", "Ajuste completo",
         "Correcciones incorporadas; en espera de nueva revisión.",
         "reviewer", set(), [O, G]),
        ("cp_resent", "Enviado con ajustes",
         "Eje reenviado tras incorporar las correcciones.",
         "reviewer", set(), [A]),
        ("cp_postponed", "Pospuesta",
         "La IES decidió responder esto más adelante.",
         "ies", set(), [O, G]),
        ("cp_voluntary_readjust", "Reajuste voluntario solicitado",
         "La IES pidió reabrir una respuesta ya aprobada.",
         "reviewer", {"comment", "up"}, [A, O, G]),
        ("cp_partial", "Parcialmente respondido",
         "Hay respuestas listas para corroborar mientras el resto "
         "sigue en captura.",
         "reviewer", {"comment"}, [O, G]),
        ("cp_partial_approved", "Parcialmente aprobado",
         "La parte entregada fue validada; el resto sigue pendiente.",
         "ies", set(), [O, G]),
        ("cp_approved", "Aprobado",
         "Respuesta validada por la revisión.",
         "ies", {"public"}, [A, O, G]),
    ],
    "gen": [
        ("gen_pre_start", "Por iniciar",
         "Aún no se captura ninguna respuesta.",
         "ies", {"default"}, [GEN]),
        ("gen_filling", "En llenado",
         "Captura en curso por la IES.",
         "ies", {"auto"}, [GEN]),
        ("gen_completed", "Completado",
         "La IES terminó; en espera de revisión.",
         "reviewer", set(), [GEN]),
        ("gen_need_changes", "Requiere ajustes",
         "La revisión encontró puntos por corregir.",
         "ies", {"comment"}, [GEN]),
        ("gen_adjusted", "Ajuste completo",
         "Correcciones incorporadas; en espera de nueva revisión.",
         "reviewer", set(), [GEN]),
        ("gen_approved", "Aprobado",
         "Respuestas validadas por la revisión.",
         "reviewer", {"public"}, [GEN]),
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
    # Generales (gen_approved → gen_need_changes es la reapertura)
    "gen_pre_start": ["gen_filling"],
    "gen_filling": ["gen_completed"],
    "gen_completed": ["gen_approved", "gen_need_changes"],
    "gen_need_changes": ["gen_adjusted"],
    "gen_adjusted": ["gen_approved", "gen_need_changes"],
    "gen_approved": ["gen_need_changes"],
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
}

# Guía de siguiente paso por status (frontend la muestra bajo el control)
HINTS = {
    "bp_draft": "Edita los datos, marca cada práctica como completada y "
                "envía el paquete a revisión.",
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
}

# Reglas de UX (nombres del registry flowRules en el frontend) que deben
# cumplirse para mover un objeto a ese status. El motor no las valida.
ENTRY_RULES = {
    "bp_completed": ["practice_complete"],
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

    for group, rows in STATUSES.items():
        for order, row in enumerate(rows, start=1):
            name, public_name, description, role, flags, applies = row
            status, created = Status.objects.update_or_create(
                name=name,
                defaults={
                    "group": group,
                    "public_name": public_name,
                    "description": description,
                    "role": role,
                    "order": order,
                    "is_default": "default" in flags,
                    "is_public": "public" in flags,
                    "requires_comment": "comment" in flags,
                    "propagates_up": "up" in flags,
                    "propagates_down": "down" in flags,
                    "auto_on_first_save": "auto" in flags,
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

    return {"created": created_count, "updated": updated_count}
