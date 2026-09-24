"""Descripción de los seis tipos de preguntas (`QuestionType.description`).

Los textos son borradores para que Rubén los revise; desde aquí el
dashboard es dueño del campo. Solo se escriben donde la fila existe y la
descripción sigue vacía: lo que venga del dashboard no se pisa.
"""
from django.db import migrations, models

TYPE_DESCRIPTIONS = {
    'a_questions': ('Normas, instancias y procedimientos con los que la '
                    'institución formaliza la medida.'),
    'b_questions': ('En cuántas de sus instancias académicas y '
                    'administrativas opera la medida.'),
    'reach': 'A qué poblaciones de la comunidad alcanza la medida.',
    'plans': ('Cuántos planes de estudio, por nivel, incorporan la '
              'medida.'),
    'special': ('Dato propio de este observable que no cabe en los demás '
                'grupos.'),
    'population': ('Composición sexo-género capturada en Información base '
                   'y calificada aquí.'),
}


def seed_descriptions(apps, schema_editor) -> None:
    QuestionType = apps.get_model('question', 'QuestionType')
    for name, description in TYPE_DESCRIPTIONS.items():
        QuestionType.objects.filter(
            name=name,
        ).filter(
            models.Q(description__isnull=True) | models.Q(description=''),
        ).update(description=description)


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0010_new_default_weights_and_type_icons'),
    ]

    operations = [
        migrations.AddField(
            model_name='questiontype',
            name='description',
            field=models.TextField(
                blank=True, null=True, verbose_name='Descripción',
                help_text='Qué mide este bloque de preguntas, en una frase.'),
        ),
        migrations.RunPython(seed_descriptions, migrations.RunPython.noop),
    ]
