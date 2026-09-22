"""Documentos que se construyen al descargarlos, por clave de `generator`."""
from dataclasses import dataclass
from io import BytesIO
from typing import Callable

from documents.models import Generator

DOCX_CONTENT_TYPE = (
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document')


def _questionnaire_docx() -> BytesIO:
    # Import diferido: python-docx y el armado del cuestionario solo se
    # cargan cuando alguien descarga, no al importar las vistas.
    from question.export.questionnaire import build_questionnaire_docx
    return build_questionnaire_docx()


@dataclass(frozen=True)
class GeneratedFile:
    build: Callable[[], BytesIO]
    filename: str
    content_type: str


GENERATORS: dict[str, GeneratedFile] = {
    Generator.QUESTIONNAIRE_DOCX: GeneratedFile(
        build=_questionnaire_docx,
        filename='cuestionario-onigies-2026.docx',
        content_type=DOCX_CONTENT_TYPE,
    ),
}
