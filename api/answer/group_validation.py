"""
Compuerta de contenido de un grupo del cuestionario principal (flujo
`cp`), del lado del servidor. Espejo de `survey/general_validation.py`
para los grupos por tipo de pregunta: un grupo vacío no se da por
completado ni por API directa.

Reglas por tipo (skill `cp-questionnaire`):
- A: cada AQuestion del observable con una opción elegida.
- B: los conteos que la pregunta incluye (académico siempre; admin solo
  con `includes_admin`) no nulos y sin rebasar las instancias declaradas
  en información base.
- Reach: al menos un sector, o `not_focalized` donde la pregunta ofrece
  la salida de planeación general (1.4 y 1.9).
- Plans (1.12): un conteo por nivel que la IES declaró en información
  base, sin rebasar los planes declarados.
- Special (1.14): total y cumplen no nulos, cumplen ≤ total.
- population (1.7): su contenido vive y se valida en información base;
  aquí nunca bloquea.

Donde la regla depende de información base y esta no tiene el dato, no
se bloquea: la falta viaja como advertencia (`warnings`), no como error.
"""

# Transiciones que comprometen el contenido del grupo ante la revisión.
VALIDATED_TARGETS = ('cp_completed', 'cp_adjusted')

MAX_LISTED_ISSUES = 8

# Pregunta general (por `name`) que fija el denominador de cada conteo.
B_DENOMINATORS = {
    'academic_instances_complying': ('academic_instances', 'académicas'),
    'admin_instances_complying': ('admin_instances', 'administrativas'),
}
PLAN_LEVELS = {
    'media_plans': ('media_plans', 'nivel medio superior'),
    'superior_plans': ('superior_plans', 'nivel superior'),
    'postgraduate_plans': ('postgraduate_plans', 'posgrado'),
}


class Completion:
    """Resultado de la compuerta: errores bloquean, advertencias no."""

    def __init__(self):
        self.errors: list[str] = []
        self.warnings: list[str] = []


def _gen_values(survey) -> dict:
    """{name: (valor entero o None, no_apply)} de las preguntas generales
    del survey; una pregunta sin fila cuenta como sin dato."""
    return {
        row.general_question.name: (row.value_integer, row.no_apply)
        for row in survey.question_responses.select_related(
            'general_question')
    }


def _short(text: str, limit: int = 80) -> str:
    text = ' '.join((text or '').split())
    return text if len(text) <= limit else text[:limit - 1] + '…'


def _a_issues(group, observable, result: Completion) -> None:
    answered = {
        r.question_id for r in group.a_responses.all()
        if r.selected_option_id is not None}
    for question in observable.aquestion_set.all():
        if question.id not in answered:
            result.errors.append(
                f'Falta responder: {_short(question.text)}')


def _count_within(value, name, label, gen: dict, what: str,
                  result: Completion) -> None:
    """Un conteo no puede rebasar su denominador de información base;
    sin denominador solo se advierte."""
    if name not in gen or gen[name][0] is None:
        result.warnings.append(
            f'Información base no declara {what} {label}; el conteo no '
            'se pudo contrastar.')
        return
    if value is not None and value > gen[name][0]:
        result.errors.append(
            f'El conteo de {what} {label} ({value}) rebasa lo declarado '
            f'en información base ({gen[name][0]}).')


def _b_issues(group, observable, gen: dict, result: Completion) -> None:
    responses = {r.question_id: r for r in group.b_responses.all()}
    for question in observable.bquestion_set.all():
        response = responses.get(question.id)
        fields = ['academic_instances_complying']
        if question.includes_admin:
            fields.append('admin_instances_complying')
        for field in fields:
            gen_name, label = B_DENOMINATORS[field]
            value = getattr(response, field, None)
            if value is None:
                result.errors.append(
                    f'Falta el número de instancias {label} que cumplen.')
                continue
            _count_within(value, gen_name, label, gen, 'instancias', result)


def _reach_issues(group, observable, result: Completion) -> None:
    responses = {r.question_id: r for r in group.reach_responses.all()}
    for question in observable.reachquestion_set.all():
        response = responses.get(question.id)
        if response is None:
            result.errors.append(
                'Falta indicar a qué poblaciones alcanza la medida.')
            continue
        escape = question.has_general_planning and response.not_focalized
        if not escape and not response.sectors.exists():
            result.errors.append(
                'Falta indicar a qué poblaciones alcanza la medida.')


def _plan_issues(group, observable, gen: dict, result: Completion) -> None:
    responses = {r.question_id: r for r in group.plan_responses.all()}
    for question in observable.planquestion_set.all():
        response = responses.get(question.id)
        for field, (gen_name, label) in PLAN_LEVELS.items():
            declared = gen.get(gen_name)
            if declared is None or declared[0] is None:
                if not (declared and declared[1]):
                    result.warnings.append(
                        f'Información base no declara planes de {label}; '
                        f'no se exige ese nivel en «{_short(question.text)}».')
                continue
            if declared[1]:
                continue
            value = getattr(response, field, None)
            if value is None:
                result.errors.append(
                    f'Falta el conteo de {label} en: '
                    f'{_short(question.text)}')
            elif value > declared[0]:
                result.errors.append(
                    f'El conteo de {label} ({value}) rebasa los planes '
                    f'declarados en información base ({declared[0]}) en: '
                    f'{_short(question.text)}')


def _special_issues(group, observable, result: Completion) -> None:
    responses = {r.question_id: r for r in group.special_responses.all()}
    for question in observable.specialquestion_set.all():
        response = responses.get(question.id)
        total = getattr(response, 'total', None)
        complying = getattr(response, 'complying', None)
        if total is None:
            result.errors.append(f'Falta el total en: {_short(question.text)}')
        if complying is None:
            result.errors.append(
                f'Falta cuántos cumplen en: {_short(question.text)}')
        if (total is not None and complying is not None
                and complying > total):
            result.errors.append(
                f'Los que cumplen ({complying}) rebasan el total ({total}) '
                f'en: {_short(question.text)}')


def group_completion(group_response) -> Completion:
    """Qué le falta al grupo para poder darse por completado."""
    result = Completion()
    observable_response = group_response.observable_response
    observable = observable_response.observable
    survey = observable_response.survey
    type_name = group_response.question_type_id

    if type_name == 'a_questions':
        _a_issues(group_response, observable, result)
    elif type_name == 'b_questions':
        _b_issues(group_response, observable, _gen_values(survey), result)
    elif type_name == 'reach':
        _reach_issues(group_response, observable, result)
    elif type_name == 'plans':
        _plan_issues(group_response, observable, _gen_values(survey), result)
    elif type_name == 'special':
        _special_issues(group_response, observable, result)
    return result


def completion_errors(group_response, target) -> list[str]:
    """Errores del gancho del motor para la transición pedida. Solo al
    entrar a los status que comprometen el grupo ante la revisión."""
    if target.name not in VALIDATED_TARGETS:
        return []
    issues = group_completion(group_response).errors
    if not issues:
        return []
    hidden = len(issues) - MAX_LISTED_ISSUES
    errors = issues[:MAX_LISTED_ISSUES]
    if hidden > 0:
        errors.append(
            f'… y {hidden} pendiente{"" if hidden == 1 else "s"} más.')
    return errors
