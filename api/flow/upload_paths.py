"""
Rutas de subida para flow.Attachment.

Reconstruye la ruta según el tipo del target, conservando el esquema de
carpetas que usaban los adjuntos viejos, para que los archivos migrados
y los nuevos convivan en los mismos directorios.
"""
import os

MAX_PATH_LENGTH = 255


def fit_upload_path(path: str, max_length: int = MAX_PATH_LENGTH) -> str:
    """Deja una sola extensión y recorta el nombre para que la ruta quepa.

    Django solo recorta lo anterior al primer punto del nombre; con
    nombres como «Inclusión_2.5_….pdf» no le queda qué recortar y la
    subida truena con un 400 (SuspiciousFileOperation).
    """
    folder, filename = os.path.split(path)
    stem, ext = os.path.splitext(filename)
    stem = stem.replace(".", "_") or "archivo"
    overflow = len(os.path.join(folder, stem + ext)) - max_length
    if overflow > 0:
        stem = stem[:max(len(stem) - overflow, 1)]
    return os.path.join(folder, stem + ext)


def resolve_upload_path(instance, filename: str) -> str:
    """Ruta de subida de un Attachment según el modelo de su target."""
    return fit_upload_path(_build_upload_path(instance, filename))


def _build_upload_path(instance, filename: str) -> str:
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

    # Carpeta plana histórica de las evidencias de bp; se conserva.
    if model in ("goodpractice", "featuregoodpractice",
                 "goodpracticepackage"):
        return join_path(["evidences"], filename)

    return join_path(["attachments", "other", model], filename)
