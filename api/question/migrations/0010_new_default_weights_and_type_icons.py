"""Nuevas ponderaciones por defecto, ícono y color de los seis tipos, y
la fila única de ajustes.

Solo se escribe donde nada se editó todavía (ponderación en su valor
viejo, ícono y color nulos): lo que venga del dashboard no se pisa.
"""
from decimal import Decimal

from django.db import migrations

# (name, valor viejo, valor nuevo, icon, color).
TYPE_DEFAULTS = [
    ('a_questions', Decimal('60.00'), Decimal('5.00'), 'gavel', 'indigo'),
    ('reach', Decimal('0.00'), Decimal('2.50'), 'groups', 'indigo'),
    ('b_questions', Decimal('40.00'), Decimal('2.50'),
     'account_tree', 'indigo'),
    ('plans', Decimal('0.00'), None, 'menu_book', 'deep-purple'),
    ('special', Decimal('0.00'), None, 'star', 'deep-purple'),
    ('population', Decimal('0.00'), None, 'diversity_3', 'deep-purple'),
]


def update_types(apps, schema_editor) -> None:
    QuestionType = apps.get_model('question', 'QuestionType')
    QuestionnaireSettings = apps.get_model(
        'question', 'QuestionnaireSettings')

    for name, old_weight, new_weight, icon, color in TYPE_DEFAULTS:
        question_type = QuestionType.objects.filter(name=name).first()
        if question_type is None:
            continue
        changed = []
        if question_type.default_weight == old_weight:
            question_type.default_weight = new_weight
            changed.append('default_weight')
        if question_type.icon is None:
            question_type.icon = icon
            changed.append('icon')
        if question_type.color is None:
            question_type.color = color
            changed.append('color')
        if changed:
            question_type.save(update_fields=changed)

    # El dump de catálogos la manda tal cual: sin fila no hay bandera
    # que leer en el frontend.
    QuestionnaireSettings.objects.get_or_create(
        pk=1, defaults={'content_open': True})


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0009_questionnaire_settings_and_type_icon_color'),
    ]

    operations = [
        migrations.RunPython(update_types, migrations.RunPython.noop),
    ]
