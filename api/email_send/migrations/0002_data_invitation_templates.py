"""Crea los registros de TemplateBase para las invitaciones.

Los archivos HTML viven en `email_send/templates/email/`. Lo que
falta en BD es el TemplateBase que `send_named_template_email`
busca por nombre. Sin este registro, el envío falla en silencio
(solo deja warning en logs).

Idempotente vía `get_or_create`. Si ya existen, no toca nada.
"""

from django.db import migrations


INVITATION_TEMPLATES = [
    {
        'name': 'email/invitation_institution.html',
        'subject': 'Invitación ONIGIES — Registro de tu institución',
        'description': (
            'Invitación a una persona contacto de una IES para '
            'iniciar el registro de datos de su institución.'
        ),
    },
    {
        'name': 'email/invitation_generic.html',
        'subject': 'Invitación ONIGIES — Acceso como revisora',
        'description': (
            'Invitación genérica para personal staff, revisoras o '
            'superusuarias del sistema (sin institución asociada).'
        ),
    },
]


def create_invitation_templates(apps, schema_editor):
    TemplateBase = apps.get_model('email_send', 'TemplateBase')
    for data in INVITATION_TEMPLATES:
        TemplateBase.objects.get_or_create(
            name=data['name'],
            defaults={
                'subject': data['subject'],
                'description': data['description'],
            },
        )


def delete_invitation_templates(apps, schema_editor):
    TemplateBase = apps.get_model('email_send', 'TemplateBase')
    names = [t['name'] for t in INVITATION_TEMPLATES]
    TemplateBase.objects.filter(name__in=names).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('email_send', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            create_invitation_templates,
            reverse_code=delete_invitation_templates,
        ),
    ]