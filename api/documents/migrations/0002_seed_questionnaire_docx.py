from django.db import migrations


def seed_questionnaire(apps, schema_editor):
    PublicDocument = apps.get_model('documents', 'PublicDocument')
    # get_or_create: re-correr no duplica ni pisa lo que Rubén ya editó.
    PublicDocument.objects.get_or_create(
        slug='cuestionario-2026',
        defaults={
            'title': 'Cuestionario ONIGIES 2026 (Word)',
            'generator': 'questionnaire_docx',
            'is_published': True,
            'order': 1,
        },
    )


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_questionnaire, migrations.RunPython.noop),
    ]
