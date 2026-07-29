"""
Seed del catálogo de status del flujo de validación.

Cada status se declara completo en un solo StatusDef (textos, flags,
estética, prompts y diálogos de confirmación). Las relaciones del
grafo — transiciones (NEXT_STATUSES) y reglas padre-hijo
(VALID_CHILD_STATUSES) — viven aparte porque son aristas, no
atributos: juntas se leen como el board de Miró.

El seed es la fuente de verdad de TODOS los campos, incluidos color,
icon y priority: re-sembrar sobreescribe cualquier ajuste hecho en el
admin (el admin sirve para experimentar, no para persistir).
_validate() truena ante typos en el grafo antes de tocar la BD.

Idempotente: upsert por PK y reconstrucción de los M2M con .set().
"""
from dataclasses import dataclass, field

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


@dataclass(frozen=True)
class StatusDef:
    """
    Definición completa de un status: una sola fuente por status.

    Flags: default (is_default), public (is_public),
    comment (comment_type=required), comment_opt (optional),
    up (propagates_up), down (propagates_down),
    auto (auto_on_first_save), edit (content_editable).
    Un diálogo en `confirm` implica requires_confirmation.
    """
    name: str
    public_name: str          # estado que muestra el chip
    action_name: str | None   # verbo del botón que transiciona HACIA él
    description: str          # tooltip del chip
    role: str | None = None   # ies / reviewer / None = terminal
    flags: set = field(default_factory=set)
    applies: list = field(default_factory=list)
    color: str = "grey"       # vuetify material color
    icon: str = "trip_origin"  # material symbol
    priority: int = 0         # mayor = más urgente, se muestra primero
    hint: str | None = None   # guía para quien tiene el turno (bajo el chip)
    hint_wait: str | None = None  # variante para el rol que espera
    comment_prompt: str | None = None  # rótulo de la caja de comentario
    confirm: tuple | None = None       # (título, cuerpo) del diálogo
    entry_rules: list = field(default_factory=list)


S = StatusDef

# Escala de priority: 90s = correcciones pendientes, 70s-80s = turno de
# la revisión, 50s-60s = trabajo de la IES en curso, 30s-40s = latente,
# <=20 = cerrado. Colores: azul = captura, cian = completado esperando
# envío, morados = en revisión, naranja/ámbar = correcciones, teal =
# corregido, verde = aprobado, rojo = rechazo, café = pausa/abandono,
# gris azulado = cerrado neutro.
STATUSES = {
    "bp": [
        S("bp_draft", "Borrador", "Reabrir participación",
          "En captura. La IES edita libremente y marca cada práctica "
          "como completada antes de enviar el paquete.",
          role="ies", flags={"default", "down", "edit"},
          applies=[P, GP], color="blue", icon="edit_note", priority=50,
          hint="Edita tus buenas prácticas, marca cada una como "
               "completada y envía el paquete a revisión.",
          hint_wait="La institución está capturando sus buenas "
                    "prácticas; aún no envía el paquete.",
          confirm=("¿Quieres reabrir tu participación en buenas "
                   "prácticas?",
                   "Podrás volver a capturar y enviar buenas "
                   "prácticas mientras el periodo siga abierto.")),
        S("bp_completed", "Completada", "Marcar como completada",
          "La IES dio por terminada esta práctica; entrará a revisión "
          "cuando se envíe el paquete.",
          role="reviewer", flags={"edit"},
          applies=[GP], color="cyan", icon="task_alt", priority=60,
          hint="Práctica completada por la IES; en espera de que se "
               "envíe el paquete para revisarla.",
          hint_wait="Marcaste esta práctica como completada. Envía el "
                    "paquete cuando todas estén listas.",
          entry_rules=["practice_complete"]),
        S("bp_sent", "Enviado a revisión", "Enviar a revisión",
          "El paquete se envió; las prácticas están en revisión.",
          role="reviewer", flags={"comment_opt"},
          applies=[P], color="deep-purple", icon="send", priority=75,
          hint="Paquete en revisión. Dictamina cada práctica o "
               "solicita ajustes.",
          hint_wait="Tu paquete está en revisión. Te avisaremos si se "
                    "requieren ajustes o cuando haya dictamen.",
          confirm=("¿De verdad quieres enviar a revisión las buenas "
                   "prácticas?",
                   "Una vez enviadas, no podrás realizar "
                   "modificaciones ni agregar nuevas.")),
        S("bp_adjusted", "Ajustes atendidos",
          "Marcar ajustes como atendidos",
          "La IES incorporó las correcciones; la práctica espera una "
          "nueva revisión.",
          role="reviewer", flags={"edit", "comment_opt"},
          applies=[GP], color="teal", icon="published_with_changes",
          priority=80,
          hint="Ajustes incorporados; en espera de nueva revisión.",
          hint_wait="Marcaste los ajustes como atendidos. Reenvía el "
                    "paquete para una nueva revisión.",
          comment_prompt="Si gustas, describe a la persona revisora "
                         "los ajustes que realizaste.",
          entry_rules=["practice_complete"]),
        S("bp_resent", "Reenviado a revisión", "Reenviar a revisión",
          "El paquete se reenvió con los ajustes incorporados.",
          role="reviewer", flags={"comment_opt"},
          applies=[P], color="indigo", icon="forward_to_inbox",
          priority=78,
          hint="Paquete reenviado con ajustes. Continúa la revisión.",
          hint_wait="Reenviaste el paquete con tus ajustes; la "
                    "revisión está en curso.",
          confirm=("¿Reenviar el paquete a revisión?",
                   "Asegúrate de haber atendido todas las "
                   "correcciones; no podrás modificar las prácticas "
                   "durante la revisión.")),
        S("bp_for_ruling", "Recibida para dictamen",
          "Recibir para dictamen",
          "La práctica cumplió los criterios y pasa a la etapa de "
          "dictamen.",
          role=None, flags={"public", "comment_opt"},
          applies=[GP], color="green", icon="verified", priority=30,
          hint="Práctica recibida para dictamen. Sin acciones "
               "pendientes aquí.",
          comment_prompt="Si gustas, agrega un mensaje para la "
                         "institución.",
          entry_rules=["features_rated"]),
        S("bp_finished", "Finalizado", "Finalizar",
          "La revisión del paquete concluyó; sin acciones pendientes.",
          role=None, applies=[P], color="blue-grey",
          icon="sports_score", priority=10,
          hint="Revisión del paquete concluida."),
        S("bp_need_changes", "Requiere ajustes", "Solicitar ajustes",
          "La revisión solicitó correcciones para que la IES las "
          "atienda.",
          role="ies", flags={"comment", "edit"},
          applies=[P, GP], color="orange", icon="new_releases",
          priority=90,
          hint="La revisión solicitó correcciones. Ajusta las "
               "prácticas y reenvía el paquete.",
          hint_wait="En espera de que la institución atienda las "
                    "correcciones solicitadas."),
        S("bp_rejected", "No acreditada", "Marcar como no acreditada",
          "La práctica no cumplió los criterios mínimos de la "
          "convocatoria.",
          role=None, flags={"comment"},
          applies=[GP], color="red", icon="cancel", priority=20,
          hint="No pasó los filtros mínimos de la convocatoria.",
          comment_prompt="Explica a la institución por qué la "
                         "práctica no fue acreditada.",
          confirm=("¿Marcar esta práctica como no acreditada?",
                   "La práctica quedará fuera del dictamen; esta "
                   "decisión no podrá deshacerse desde la "
                   "plataforma.")),
        S("bp_discarded", "Descartada", "Descartar",
          "La IES optó por no reportar buenas prácticas; su "
          "participación queda cerrada (reabrible mientras el periodo "
          "siga abierto).",
          role="ies", flags={"down"},
          applies=[P, GP], color="brown", icon="do_not_disturb_on",
          priority=15,
          hint="Participación cerrada. Puedes reabrir para cambiar "
               "tu respuesta mientras el periodo siga abierto.",
          hint_wait="La institución optó por no reportar buenas "
                    "prácticas.",
          confirm=("¿Confirmas que no deseas reportar buenas "
                   "prácticas?",
                   "Tu participación quedará cerrada. Mientras el "
                   "periodo siga abierto, podrás reabrirla y cambiar "
                   "tu respuesta.")),
    ],
    "cp": [
        S("cp_pre_start", "Por iniciar", None,
          "El eje aún no tiene respuestas capturadas.",
          role="ies", flags={"default", "edit"},
          applies=[A, O, G], color="blue-grey-lighten-1",
          icon="hourglass_empty", priority=35,
          hint="Comienza a capturar las respuestas del eje; el "
               "avance se guarda automáticamente.",
          hint_wait="La institución aún no comienza a capturar este "
                    "eje."),
        S("cp_filling", "En llenado", None,
          "La IES está capturando las respuestas del eje.",
          role="ies", flags={"auto", "up", "edit"},
          applies=[A, O, G], color="blue", icon="edit_note",
          priority=50,
          hint="Continúa la captura y marca cada respuesta como "
               "completada cuando esté lista.",
          hint_wait="La institución está capturando las respuestas "
                    "del eje."),
        S("cp_completed", "Completado", "Marcar como completado",
          "La IES dio por terminada la respuesta; entrará a revisión "
          "cuando se envíe el eje.",
          role="reviewer", flags={"edit"},
          applies=[O, G], color="cyan", icon="task_alt", priority=60,
          hint="Respuesta completada por la IES. Apruébala o "
               "solicita ajustes cuando el eje esté en revisión.",
          hint_wait="Marcaste esta respuesta como completada. Se "
                    "revisará cuando envíes el eje."),
        S("cp_sent", "Enviado a revisión", "Enviar a revisión",
          "El eje se envió; sus respuestas están en revisión.",
          role="reviewer", flags={"comment_opt"},
          applies=[A], color="deep-purple", icon="send", priority=75,
          hint="Eje enviado. Inicia la revisión cuando vayas a "
               "dictaminarlo.",
          hint_wait="Enviaste el eje a revisión. Te avisaremos cuando "
                    "la revisión inicie.",
          confirm=("¿Enviar el eje a revisión?",
                   "Una vez enviado no podrás modificar sus "
                   "respuestas hasta que la revisión concluya o "
                   "solicite ajustes.")),
        S("cp_in_review", "En revisión", "Iniciar revisión",
          "La revisión del eje está en curso.",
          role="reviewer", applies=[A], color="purple",
          icon="fact_check", priority=72,
          hint="Revisión en curso. Aprueba cada respuesta o solicita "
               "ajustes.",
          hint_wait="Tu eje está siendo revisado. Te avisaremos si "
                    "se requieren ajustes."),
        S("cp_need_changes", "Requiere ajustes", "Solicitar ajustes",
          "La revisión solicitó correcciones para que la IES las "
          "atienda.",
          role="ies", flags={"comment", "edit"},
          applies=[A, O, G], color="orange", icon="new_releases",
          priority=90,
          hint="La revisión solicitó correcciones. Atiende los "
               "señalamientos y reenvía el eje.",
          hint_wait="En espera de que la institución atienda las "
                    "correcciones solicitadas."),
        S("cp_in_adjustment", "En ajustes", "Iniciar ajustes",
          "La IES está capturando las correcciones solicitadas.",
          role="ies", flags={"auto", "up", "edit"},
          applies=[A, O, G], color="amber", icon="construction",
          priority=70,
          hint="Estás corrigiendo esta respuesta; marca los ajustes "
               "como atendidos al terminar.",
          hint_wait="La institución está capturando las correcciones "
                    "solicitadas."),
        S("cp_adjusted", "Ajustes atendidos",
          "Marcar ajustes como atendidos",
          "La IES incorporó las correcciones; la respuesta espera "
          "una nueva revisión.",
          role="reviewer", flags={"edit", "comment_opt"},
          applies=[O, G], color="teal", icon="published_with_changes",
          priority=80,
          hint="Ajustes incorporados; en espera de nueva revisión.",
          hint_wait="Marcaste los ajustes como atendidos. Reenvía el "
                    "eje para una nueva revisión.",
          comment_prompt="Si gustas, describe a la persona revisora "
                         "los ajustes que realizaste."),
        S("cp_resent", "Reenviado a revisión", "Reenviar a revisión",
          "El eje se reenvió con los ajustes incorporados.",
          role="reviewer", flags={"comment_opt"},
          applies=[A], color="indigo", icon="forward_to_inbox",
          priority=78,
          hint="Eje reenviado con ajustes. Continúa la revisión.",
          hint_wait="Reenviaste el eje con tus ajustes; la revisión "
                    "está en curso.",
          confirm=("¿Reenviar el eje a revisión?",
                   "Asegúrate de haber atendido todas las "
                   "correcciones solicitadas.")),
        S("cp_postponed", "Pospuesta", "Posponer",
          "La IES decidió responder esto más adelante.",
          role="ies", applies=[O, G], color="brown-lighten-1",
          icon="snooze", priority=40,
          hint="Respuesta pospuesta. Retómala antes del cierre del "
               "periodo.",
          hint_wait="La institución pospuso esta respuesta."),
        S("cp_voluntary_readjust", "Reajuste solicitado",
          "Solicitar reajuste",
          "La IES pidió reabrir una respuesta ya aprobada; la "
          "revisión debe autorizarlo.",
          role="reviewer", flags={"comment", "up"},
          applies=[A, O, G], color="pink", icon="lock_open",
          priority=85,
          hint="La IES pidió reabrir esta respuesta aprobada. "
               "Autoriza el reajuste solicitando los cambios.",
          hint_wait="Pediste reabrir esta respuesta; la revisión "
                    "debe autorizar el reajuste.",
          comment_prompt="Explica qué necesitas corregir y por qué "
                         "pides reabrir la respuesta."),
        S("cp_partial", "Parcialmente respondido",
          "Enviar avance parcial",
          "Hay respuestas listas para corroborar mientras el resto "
          "sigue en captura.",
          role="reviewer", flags={"comment"},
          applies=[O, G], color="lime-darken-2", icon="rule",
          priority=65,
          hint="Avance parcial enviado. Corrobora la parte entregada "
               "o solicita ajustes.",
          hint_wait="Enviaste un avance parcial; la revisión "
                    "corroborará la parte entregada.",
          comment_prompt="Describe qué respuestas están listas para "
                         "corroborar y qué falta."),
        S("cp_partial_approved", "Parcialmente aprobado",
          "Aprobar parte entregada",
          "La parte entregada se validó; el resto sigue pendiente "
          "del lado de la IES.",
          role="ies", flags={"edit"},
          applies=[O, G], color="light-green",
          icon="incomplete_circle", priority=55,
          hint="La parte entregada fue validada. Completa lo "
               "pendiente y envíalo.",
          hint_wait="En espera de que la institución complete las "
                    "respuestas pendientes."),
        S("cp_approved", "Aprobado", "Aprobar",
          "La respuesta fue validada por la revisión.",
          role="ies", flags={"public", "comment_opt"},
          applies=[A, O, G], color="green", icon="done_all",
          priority=10,
          hint="Respuesta aprobada. Si necesitas modificarla, "
               "solicita un reajuste.",
          hint_wait="Respuesta aprobada. La institución puede "
                    "solicitar un reajuste si lo necesita."),
    ],
    "gen": [
        S("gen_draft", "Borrador", None,
          "En captura. La IES edita las preguntas generales y marca "
          "cada grupo como completado antes de enviar.",
          role="ies", flags={"default", "edit"},
          applies=[GPK, GEN], color="blue", icon="edit_note",
          priority=50,
          hint="Edita las preguntas generales, marca cada grupo como "
               "completado y envía a revisión.",
          hint_wait="La institución está capturando sus preguntas "
                    "generales."),
        S("gen_completed", "Completado", "Marcar como completado",
          "La IES dio por terminado este grupo; entrará a revisión "
          "cuando se envíen las generales.",
          role="reviewer", flags={"edit"},
          applies=[GEN], color="cyan", icon="task_alt", priority=60,
          hint="Grupo completado por la IES; en espera de que se "
               "envíen las generales.",
          hint_wait="Marcaste este grupo como completado. Envía las "
                    "generales cuando todos estén listos."),
        S("gen_sent", "Enviado a revisión", "Enviar a revisión",
          "Las preguntas generales se enviaron; están en revisión.",
          role="reviewer", flags={"comment_opt"},
          applies=[GPK], color="deep-purple", icon="send", priority=75,
          hint="Preguntas generales en revisión. Aprueba cada grupo "
               "o solicita ajustes.",
          hint_wait="Tus preguntas generales están en revisión. Te "
                    "avisaremos si se requieren ajustes.",
          confirm=("¿Enviar las preguntas generales a revisión?",
                   "Una vez enviadas no podrás modificarlas hasta "
                   "que la revisión concluya o solicite ajustes.")),
        S("gen_need_changes", "Requiere ajustes", "Solicitar ajustes",
          "La revisión solicitó correcciones para que la IES las "
          "atienda.",
          role="ies", flags={"comment", "edit"},
          applies=[GPK, GEN], color="orange", icon="new_releases",
          priority=90,
          hint="La revisión solicitó correcciones. Ajusta y reenvía "
               "las preguntas generales.",
          hint_wait="En espera de que la institución atienda las "
                    "correcciones solicitadas."),
        S("gen_adjusted", "Ajustes atendidos",
          "Marcar ajustes como atendidos",
          "La IES incorporó las correcciones; el grupo espera una "
          "nueva revisión.",
          role="reviewer", flags={"edit", "comment_opt"},
          applies=[GEN], color="teal", icon="published_with_changes",
          priority=80,
          hint="Ajustes incorporados; en espera de nueva revisión.",
          hint_wait="Marcaste los ajustes como atendidos. Reenvía "
                    "las generales para una nueva revisión.",
          comment_prompt="Si gustas, describe a la persona revisora "
                         "los ajustes que realizaste."),
        S("gen_resent", "Reenviado a revisión", "Reenviar a revisión",
          "Las preguntas generales se reenviaron con los ajustes "
          "incorporados.",
          role="reviewer", flags={"comment_opt"},
          applies=[GPK], color="indigo", icon="forward_to_inbox",
          priority=78,
          hint="Preguntas generales reenviadas con ajustes. Continúa "
               "la revisión.",
          hint_wait="Reenviaste las preguntas generales; la revisión "
                    "está en curso.",
          confirm=("¿Reenviar las preguntas generales?",
                   "Asegúrate de haber atendido todas las "
                   "correcciones solicitadas.")),
        # gen_approved y gen_finished son terminales absolutos, sin
        # reapertura: los generales alimentan el arranque de cp y
        # modificarlos después invalidaría todo lo que depende de ellos.
        S("gen_approved", "Aprobado", "Aprobar",
          "El grupo fue validado por la revisión.",
          role=None, flags={"public", "comment_opt"},
          applies=[GEN], color="green", icon="done_all", priority=15,
          hint="Grupo aprobado; sin acciones pendientes.",
          comment_prompt="Si gustas, agrega un mensaje para la "
                         "institución."),
        S("gen_finished", "Finalizado", "Finalizar",
          "La revisión de las preguntas generales concluyó; sin "
          "acciones pendientes.",
          role=None, applies=[GPK], color="blue-grey",
          icon="sports_score", priority=10,
          hint="Revisión de las preguntas generales concluida."),
    ],
}

# En las listas mixtas el motor filtra por applicable_models según el
# nivel del objeto; se anota a qué nivel aplica cada destino.
NEXT_STATUSES = {
    # Buenas prácticas — P = paquete, GP = práctica
    "bp_draft": ["bp_completed",        # GP
                 "bp_sent",             # P
                 "bp_discarded"],       # P y GP
    "bp_discarded": ["bp_draft"],
    "bp_completed": ["bp_need_changes", "bp_for_ruling", "bp_rejected"],
    "bp_adjusted": ["bp_need_changes", "bp_for_ruling", "bp_rejected"],
    "bp_need_changes": ["bp_adjusted",  # GP
                        "bp_resent",    # P
                        "bp_discarded"],  # P y GP
    "bp_sent": ["bp_finished", "bp_need_changes"],
    "bp_resent": ["bp_finished", "bp_need_changes"],
    # Cuestionario principal — A = eje, O/G = respuestas
    "cp_pre_start": ["cp_filling"],
    "cp_filling": ["cp_completed",      # O y G
                   "cp_sent",           # A
                   "cp_postponed",      # O y G
                   "cp_partial"],       # O y G
    "cp_completed": ["cp_approved", "cp_need_changes"],
    "cp_sent": ["cp_in_review"],
    "cp_in_review": ["cp_approved", "cp_need_changes"],
    "cp_adjusted": ["cp_approved", "cp_need_changes"],
    "cp_resent": ["cp_in_review"],
    "cp_postponed": ["cp_completed", "cp_partial"],
    "cp_approved": ["cp_voluntary_readjust"],
    "cp_voluntary_readjust": ["cp_need_changes"],
    "cp_need_changes": ["cp_in_adjustment"],
    "cp_in_adjustment": ["cp_adjusted",   # O y G
                         "cp_resent",     # A
                         "cp_postponed"],  # O y G
    "cp_partial": ["cp_need_changes", "cp_partial_approved"],
    "cp_partial_approved": ["cp_completed", "cp_partial"],
    # Generales — GPK = paquete, GEN = grupo (espejo de bp)
    "gen_draft": ["gen_completed",      # GEN
                  "gen_sent"],          # GPK
    "gen_completed": ["gen_need_changes", "gen_approved"],
    "gen_adjusted": ["gen_need_changes", "gen_approved"],
    "gen_need_changes": ["gen_adjusted",  # GEN
                         "gen_resent"],   # GPK
    "gen_sent": ["gen_finished", "gen_need_changes"],
    "gen_resent": ["gen_finished", "gen_need_changes"],
}

# Para mover el PADRE al status clave, TODOS sus hijos deben estar en
# alguno de los status de la lista (auto-loops incluidos).
VALID_CHILD_STATUSES = {
    "bp_sent": ["bp_completed", "bp_discarded"],
    "bp_discarded": ["bp_discarded", "bp_draft", "bp_need_changes"],
    # Incluye los dictámenes: en rondas mixtas (unas prácticas ya
    # dictaminadas, otras ajustadas) el paquete debe poder reenviarse.
    "bp_resent": ["bp_adjusted", "bp_completed", "bp_for_ruling",
                  "bp_rejected"],
    "bp_finished": ["bp_for_ruling", "bp_rejected"],
    "cp_approved": ["cp_approved"],
    "cp_completed": ["cp_completed"],
    "cp_adjusted": ["cp_adjusted", "cp_completed", "cp_approved"],
    "cp_sent": ["cp_completed", "cp_postponed", "cp_partial"],
    "cp_resent": ["cp_completed", "cp_adjusted", "cp_approved",
                  "cp_postponed", "cp_partial"],
    # cp_voluntary_readjust permite bajar el eje a cp_need_changes sin
    # tener que mover antes cada hijo reajustado.
    "cp_need_changes": ["cp_need_changes", "cp_approved",
                        "cp_postponed", "cp_voluntary_readjust"],
    "cp_partial": ["cp_completed", "cp_postponed"],
    "cp_partial_approved": ["cp_partial_approved"],
    # Generales (espejo de bp)
    "gen_sent": ["gen_completed"],
    "gen_resent": ["gen_adjusted", "gen_completed", "gen_approved"],
    "gen_finished": ["gen_approved"],
}

# Rótulos por defecto de la caja de comentario, según el role del
# status destino (= a quién le toca el turno después = quién leerá el
# mensaje). Los obligatorios usan redacción imperativa; los status con
# comment_prompt propio ignoran estos defaults.
REQUIRED_PROMPT_BY_ROLE = {
    "ies": "Describe las correcciones que la institución debe atender.",
    "reviewer": "Describe el motivo de tu solicitud para la revisión.",
}
OPTIONAL_PROMPT_BY_ROLE = {
    "reviewer": "Si gustas, agrega un mensaje para la persona revisora.",
    "ies": "Si gustas, agrega un mensaje para la institución.",
    None: "Si gustas, agrega un mensaje.",
}


def _content_type(label: str) -> ContentType:
    app_label, model = label.split(".")
    return ContentType.objects.get_by_natural_key(app_label, model)


def _validate() -> None:
    """Mata los typos silenciosos: todo nombre usado en el grafo debe
    existir en STATUSES."""
    names = {s.name for rows in STATUSES.values() for s in rows}
    graphs = [("NEXT_STATUSES", NEXT_STATUSES),
              ("VALID_CHILD_STATUSES", VALID_CHILD_STATUSES)]
    for label, graph in graphs:
        for origin, targets in graph.items():
            unknown = {origin, *targets} - names
            if unknown:
                raise ValueError(
                    f"{label}: status desconocidos {sorted(unknown)}")


def _comment_fields(s: StatusDef) -> tuple:
    """Deriva (comment_type, comment_prompt) de los flags, con
    defaults por rol y prompt obligatorio garantizado."""
    if "comment" in s.flags:
        prompt = s.comment_prompt or REQUIRED_PROMPT_BY_ROLE.get(s.role)
        if not prompt:
            raise ValueError(
                f"{s.name}: comentario obligatorio sin prompt "
                f"(role={s.role} no tiene default)")
        return "required", prompt
    if "comment_opt" in s.flags:
        prompt = s.comment_prompt or OPTIONAL_PROMPT_BY_ROLE[s.role]
        return "optional", prompt
    return "none", None


def seed_flow() -> dict:
    """
    Crea o actualiza el catálogo completo de Status y sus M2M.
    Devuelve conteos {created, updated} para reporte.
    """
    _validate()
    created_count = 0
    updated_count = 0
    applicability: dict[str, list] = {}

    # Limpia is_default de los grupos gestionados antes del upsert: evita
    # chocar con unique_default_per_group cuando el default de un grupo
    # cambió de nombre (p.ej. gen_pre_start → gen_draft). El loop lo
    # reasigna enseguida.
    Status.objects.filter(group__in=STATUSES).update(is_default=False)

    for group, rows in STATUSES.items():
        for order, s in enumerate(rows, start=1):
            comment_type, comment_prompt = _comment_fields(s)
            confirm_title, confirm_text = s.confirm or (None, None)
            _, created = Status.objects.update_or_create(
                name=s.name,
                defaults={
                    "group": group,
                    "public_name": s.public_name,
                    "action_name": s.action_name,
                    "description": s.description,
                    "role": s.role,
                    "order": order,
                    "priority": s.priority,
                    "color": s.color,
                    "icon": s.icon,
                    "is_default": "default" in s.flags,
                    "is_public": "public" in s.flags,
                    "comment_type": comment_type,
                    "comment_prompt": comment_prompt,
                    "requires_confirmation": s.confirm is not None,
                    "confirm_title": confirm_title,
                    "confirm_text": confirm_text,
                    "propagates_up": "up" in s.flags,
                    "propagates_down": "down" in s.flags,
                    "auto_on_first_save": "auto" in s.flags,
                    "content_editable": "edit" in s.flags,
                    "hint": s.hint,
                    "hint_wait": s.hint_wait,
                    "entry_rules": s.entry_rules,
                },
            )
            if created:
                created_count += 1
            else:
                updated_count += 1
            applicability[s.name] = s.applies

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