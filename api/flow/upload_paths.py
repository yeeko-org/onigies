"""
Rutas de subida para flow.Attachment.

Reconstruye la ruta según el tipo del target, conservando la estructura
de carpetas de los modelos viejos (GroupAttachment,
GeneralGroupAttachment, Evidence) para que los archivos migrados y los
nuevos convivan en los mismos directorios.
"""


def resolve_upload_path(instance, filename: str) -> str:
    """Ruta de subida de un Attachment según el modelo de su target."""
    from utils.files import join_path

    target = instance.target
    model = instance.content_type.model

    if model == "groupresponse":
        observable_response = target.observable_response
        survey = observable_response.survey
        observable = observable_response.observable
        axis = observable.component.axis.short_name
        elems = [
            "attachments", survey.institution.acronym,
            f"{survey.period_id}_{axis}",
            f"observable_{observable.number}",
        ]
        return join_path(elems, filename)

    if model == "generalgroupresponse":
        survey = target.survey
        elems = [
            "attachments", survey.institution.acronym,
            f"{survey.period_id}_general",
            f"group_{target.general_group.name}",
        ]
        return join_path(elems, filename)

    # Evidence viejo subía a 'evidences/' plano; se conserva.
    if model in ("goodpractice", "featuregoodpractice",
                 "goodpracticepackage"):
        return join_path(["evidences"], filename)

    return join_path(["attachments", "other", model], filename)
