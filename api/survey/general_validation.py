"""
Compuerta de contenido de un grupo de «Información base» (flujo `gen`),
del lado del servidor.

Espejo exacto de `nuxt/app/composables/useGeneralValidation.js`: el
frontend impide llegar aquí con el grupo incompleto, pero la transición
también se puede pedir por API directa, y un grupo vacío marcado como
completado entra a revisión como si tuviera datos. Esta es la red de
integridad; los mensajes son los mismos para que digan QUÉ falta.

Reglas madre, iguales en los cuatro grupos: el nulo es «sin responder» y
bloquea; el «no» explícito y el «No aplica» eximen lo que cuelga de
ellos; y el cero es un dato capturado, nunca un vacío.
"""
from django.db.models import Q

# Transiciones que comprometen el contenido del grupo ante la revisión.
# Guardar nunca valida: la IES captura en varias sesiones.
VALIDATED_TARGETS = ('gen_completed', 'gen_adjusted')

# Los tres conteos de una fila, en el orden de captura (Mujeres antes que
# Hombres, convención de toda la sección).
COUNT_FIELDS = (
    ('number_women', 'mujeres'),
    ('number_men', 'hombres'),
    ('number_non_binary', 'personas no binarias'),
)

# Cuántos faltantes se enumeran antes de resumir el resto: el 400 debe
# decir qué falta sin devolver un muro de texto.
MAX_LISTED_ISSUES = 8


def _count_issues(sector, row, measures_non_binary: bool,
                  issues: list[str]) -> None:
    """Conteos faltantes de una fila. `row` puede ser None: una fila que
    nunca se guardó equivale a los tres conteos vacíos."""
    for field, label in COUNT_FIELDS:
        if field == 'number_non_binary' and not measures_non_binary:
            continue
        if getattr(row, field, None) is None:
            issues.append(f'{sector.name}: falta el conteo de {label}.')


def _population_issues(survey, rows: dict, sectors: list) -> list[str]:
    """Las 12 poblaciones declaran presencia; solo las 10 principales
    esperan conteo (las 2 extra son estructurales y nunca se cuentan)."""
    issues: list[str] = []
    if survey.measures_non_binary is None:
        issues.append('Falta indicar si su institución contempla la '
                      'categoría no binaria.')
    measures = survey.measures_non_binary is True
    for sector in sectors:
        row = rows.get(sector.id)
        if row is None or row.is_present is None:
            issues.append(f'{sector.name}: falta indicar si está presente.')
            continue
        if row.is_present and sector.is_main:
            _count_issues(sector, row, measures, issues)
    return issues


def _authority_issues(survey, rows: dict, sectors: list) -> list[str]:
    """Las autoridades no declaran presencia: su escape es el «No
    aplica» por renglón. La titular es unipersonal y no tiene escape."""
    issues: list[str] = []
    measures = survey.measures_non_binary is True
    for sector in sectors:
        row = rows.get(sector.id)
        if sector.is_ies_head:
            # Su sexo y género se guarda como un 1 en el conteo que
            # corresponde; los otros dos quedan en 0.
            counts = [getattr(row, field, None) for field, _ in COUNT_FIELDS]
            if 1 not in counts:
                issues.append('Falta indicar el sexo y género de la '
                              'persona titular de la institución.')
            continue
        if row is not None and row.no_apply:
            continue
        _count_issues(sector, row, measures, issues)
    return issues


def _answered_value(question, response):
    """Valor capturado de una pregunta, en la columna tipada que dicta su
    `q_type`. La cadena vacía cuenta como vacío igual que el nulo: es lo
    que manda el input recién vaciado del frontend."""
    if response is None:
        return None
    field = ('value_boolean' if question.q_type == 'boolean'
             else 'value_integer')
    value = getattr(response, field, None)
    return None if value == '' else value


def _question_issues(survey, questions: list, responses: dict) -> list[str]:
    """Grupos de preguntas escalares: cada respuesta es una fila de
    `GeneralQuestionResponse`, con su valor y su exención dentro.

    Solo las preguntas marcadas con `allow_no_apply` en su `addl_config`
    ofrecen el escape (hoy las tres de planes de estudio: una IES puede
    no impartir un nivel, y sin la casilla su cero no se distinguiría de
    «no ofrecemos ese nivel»).
    """
    issues: list[str] = []
    for question in questions:
        response = responses.get(question.id)
        allows_no_apply = question.addl_config.get('allow_no_apply')
        if allows_no_apply and response is not None and response.no_apply:
            continue
        if _answered_value(question, response) is None:
            issues.append(f'Falta la respuesta: {question.text}')
    return issues


def _load_survey(survey_id: int):
    """Survey con todo lo que la compuerta lee, en tres queries."""
    from survey.models import Survey

    return (Survey.objects
            .prefetch_related('population_quantities', 'question_responses')
            .get(pk=survey_id))


def group_completion_issues(group_response) -> list[str]:
    """Qué le falta responder al grupo para poder darse por completado.

    Lista vacía = el grupo puede marcarse como completado.
    """
    from indicator.models import Sector

    survey = _load_survey(group_response.survey_id)
    rows = {row.sector_id: row for row in survey.population_quantities.all()}
    group = group_response.general_group
    name = group.name

    if name in ('poblaciones', 'autoridades'):
        sectors = list(Sector.objects.filter(
            Q(is_main=True) | Q(is_standard_extra=True)
            | Q(is_authority=True)))
        if name == 'poblaciones':
            population = [s for s in sectors
                          if s.is_main or s.is_standard_extra]
            return _population_issues(survey, rows, population)
        authorities = [s for s in sectors if s.is_authority]
        return _authority_issues(survey, rows, authorities)

    responses = {response.general_question_id: response
                 for response in survey.question_responses.all()}
    return _question_issues(survey, list(group.questions.all()), responses)


def completion_errors(group_response, target) -> list[str]:
    """Errores del gancho del motor para la transición pedida.

    Solo se valida al entrar a los status que comprometen el grupo; el
    resto del flujo (regresos, revisión) no exige contenido completo.
    """
    if target.name not in VALIDATED_TARGETS:
        return []
    issues = group_completion_issues(group_response)
    if not issues:
        return []
    hidden = len(issues) - MAX_LISTED_ISSUES
    errors = issues[:MAX_LISTED_ISSUES]
    if hidden > 0:
        errors.append(
            f'… y {hidden} respuesta{"" if hidden == 1 else "s"} más.')
    return errors
