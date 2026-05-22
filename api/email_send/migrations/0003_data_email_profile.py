"""Crea el EmailProfile por defecto para envíos vía Microsoft 365.

Los servicios `send_template_email` / `send_simple_email` resuelven
el perfil con `get_default_profile()`. Sin un EmailProfile activo y
marcado como default, todo envío falla con "No email profile
available".

La fila NO contiene el secreto: `password_env_var` guarda solo el
*nombre* de la variable de entorno. Por eso esta fila es idéntica
en todos los entornos y puede vivir en una migración. Cada entorno
(local y servidor) debe definir en su propio `.env` la variable:

    EMAIL_OUTLOOK_PASSWORD=<contraseña de aplicación>

Idempotente vía `get_or_create`: si el perfil ya existe, no toca
nada.
"""

from django.db import migrations


# provider='outlook' fija el host smtp.office365.com de forma
# automática. Los defaults del modelo (puerto 587, TLS) son los
# correctos para Microsoft 365; from_email vacío reutiliza el
# username como remitente.
EMAIL_PROFILE = {
    'name': 'Microsoft 365 (onigies@unam.mx)',
    'provider': 'outlook',
    'username': 'onigies@unam.mx',
    'password_env_var': 'EMAIL_OUTLOOK_PASSWORD',
    'from_name': 'Soporte ONIGIES',
}


def create_email_profile(apps, schema_editor):
    EmailProfile = apps.get_model('email_send', 'EmailProfile')
    EmailProfile.objects.get_or_create(
        name=EMAIL_PROFILE['name'],
        defaults={
            'provider': EMAIL_PROFILE['provider'],
            'username': EMAIL_PROFILE['username'],
            'password_env_var': EMAIL_PROFILE['password_env_var'],
            'from_name': EMAIL_PROFILE['from_name'],
            'is_active': True,
            'is_default': True,
        },
    )


def delete_email_profile(apps, schema_editor):
    EmailProfile = apps.get_model('email_send', 'EmailProfile')
    EmailProfile.objects.filter(
        name=EMAIL_PROFILE['name']
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('email_send', '0002_data_invitation_templates'),
    ]

    operations = [
        migrations.RunPython(
            create_email_profile,
            reverse_code=delete_email_profile,
        ),
    ]