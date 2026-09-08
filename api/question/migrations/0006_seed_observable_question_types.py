"""Migra las seis columnas `*_weight` del observable a la tabla puente.

También fija `order` y `required` en los QuestionType ya sembrados, para
que una base que no vuelva a correr `migrate_initial_data` quede igual.
"""
from django.db import migrations

# (name, order, required, public_name). El nombre público viaja aquí
# porque `migrate_initial_data` ya solo lo escribe al crear la fila: sin
# esto, las bases existentes se quedarían con la nomenclatura anterior.
TYPE_STRUCTURE = [
    ('a_questions', 1, True, 'Armonización e institucionalización'),
    ('reach', 2, False, 'Transversalidad sectorial'),
    ('b_questions', 3, True, 'Transversalidad orgánica'),
    ('plans', 4, False, 'Planes de estudio'),
    ('special', 5, False, 'Pregunta especial'),
    ('population', 6, False, 'Distribución de población'),
]

# Tipo → columna de la que se copia la ponderación del observable.
LEGACY_WEIGHTS = {
    'a_questions': 'a_weight',
    'b_questions': 'b_weight',
    'reach': 'reach_weight',
    'plans': 'plan_weight',
    'special': 'special_weight',
    'population': 'pop_weight',
}

# El 1.7 se califica con la composición de población capturada en
# Generales, no con preguntas propias de ese tipo.
POPULATION_OBSERVABLE = '1.7'


def seed_through_rows(apps, schema_editor) -> None:
    QuestionType = apps.get_model('question', 'QuestionType')
    ObservableQuestionType = apps.get_model(
        'question', 'ObservableQuestionType')
    Observable = apps.get_model('indicator', 'Observable')

    for name, order, required, public_name in TYPE_STRUCTURE:
        QuestionType.objects.filter(name=name).update(
            order=order, required=required, public_name=public_name)

    types = {q.name: q for q in QuestionType.objects.all()}
    if not types:
        return
    observables = Observable.objects.prefetch_related(
        'reachquestion_set', 'planquestion_set', 'specialquestion_set')
    for observable in observables:
        applicable = ['a_questions', 'b_questions']
        if observable.reachquestion_set.exists():
            applicable.append('reach')
        if observable.planquestion_set.exists():
            applicable.append('plans')
        if observable.specialquestion_set.exists():
            applicable.append('special')
        if observable.number == POPULATION_OBSERVABLE:
            applicable.append('population')
        for name in applicable:
            question_type = types.get(name)
            if question_type is None:
                continue
            ObservableQuestionType.objects.get_or_create(
                observable=observable, question_type=question_type,
                defaults={
                    'weight': getattr(
                        observable, LEGACY_WEIGHTS[name], None),
                },
            )


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0005_alter_questiontype_options_questiontype_order_and_more'),
        ('indicator', '0009_remove_generalgroup_fields_generalgroup_instruction_and_more'),
    ]

    operations = [
        migrations.RunPython(
            seed_through_rows, migrations.RunPython.noop),
    ]
