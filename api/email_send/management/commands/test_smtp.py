"""Comando de diagnostico para probar el envio SMTP.

Verifica de forma aislada si una cuenta de correo permite la
autenticacion SMTP (SMTP AUTH) y, opcionalmente, si logra
entregar un mensaje real.

Pensado para validar la cuenta onigies@unam.mx contra
Microsoft 365 antes de registrar un EmailProfile definitivo.
"""

import os
import smtplib
import socket

from django.core.mail import get_connection, EmailMultiAlternatives
from django.core.management.base import BaseCommand


SMTP_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Fragmentos del mensaje de error de Microsoft 365 cuando
# SMTP AUTH esta deshabilitado a nivel tenant o buzon.
SMTP_AUTH_DISABLED_HINTS = (
    'smtpclientauthentication is disabled',
    '5.7.139',
)


class Command(BaseCommand):
    help = (
        'Prueba la autenticacion SMTP de una cuenta de correo '
        '(por defecto, onigies@unam.mx en Microsoft 365).'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--host',
            default='smtp.office365.com',
            help='Servidor SMTP (default: smtp.office365.com).',
        )
        parser.add_argument(
            '--port',
            type=int,
            default=587,
            help='Puerto SMTP (default: 587).',
        )
        parser.add_argument(
            '--user',
            default='onigies@unam.mx',
            help='Cuenta que se autentica.',
        )
        parser.add_argument(
            '--password-env',
            default='EMAIL_OUTLOOK_PASSWORD',
            help=(
                'Variable de entorno con la contrasena de '
                'aplicacion (default: EMAIL_OUTLOOK_PASSWORD).'
            ),
        )
        parser.add_argument(
            '--to',
            default=None,
            help=(
                'Si se indica una direccion, ademas de autenticar '
                'envia un correo de prueba real a esa direccion.'
            ),
        )
        parser.add_argument(
            '--use-ssl',
            action='store_true',
            help='Usar SSL directo (puerto 465) en vez de TLS.',
        )

    def handle(self, *args, **options):
        host = options['host']
        port = options['port']
        user = options['user']
        password_env = options['password_env']
        recipient = options['to']
        use_ssl = options['use_ssl']
        use_tls = not use_ssl

        password = os.getenv(password_env, '')

        self.stdout.write('')
        self.stdout.write('=== Prueba de conexion SMTP ===')
        self.stdout.write(f'  Host    : {host}:{port}')
        self.stdout.write(f'  Usuario : {user}')
        self.stdout.write(
            f'  Cifrado : {"SSL" if use_ssl else "STARTTLS"}'
        )
        estado = 'definida' if password else 'VACIA'
        self.stdout.write(
            f'  Password: variable {password_env} ({estado})'
        )
        self.stdout.write('')

        if not password:
            self.stderr.write(self.style.ERROR(
                f'[FALLO] La variable {password_env} esta vacia '
                f'o no existe.\n'
                f'  Agrega al archivo .env la linea:\n'
                f'      {password_env}=<contrasena de aplicacion>'
            ))
            return

        connection = get_connection(
            backend=SMTP_BACKEND,
            host=host,
            port=port,
            username=user,
            password=password,
            use_tls=use_tls,
            use_ssl=use_ssl,
        )

        # Paso 1: abrir la conexion equivale a autenticar.
        try:
            connection.open()
        except smtplib.SMTPAuthenticationError as exc:
            self._report_auth_error(exc)
            return
        except (socket.gaierror, OSError) as exc:
            self.stderr.write(self.style.ERROR(
                f'[FALLO] No se pudo conectar a {host}:{port}.\n'
                f'  Detalle: {exc}\n'
                f'  Suele ser DNS, firewall o puerto bloqueado.'
            ))
            return
        except smtplib.SMTPException as exc:
            self.stderr.write(self.style.ERROR(
                f'[FALLO] Error SMTP al abrir la conexion: {exc}'
            ))
            return

        self.stdout.write(self.style.SUCCESS(
            '[OK] Autenticacion SMTP exitosa: la cuenta '
            'permite SMTP AUTH.'
        ))

        # Paso 2 (opcional): enviar un correo real de prueba.
        if recipient:
            self._send_test_email(connection, user, recipient)

        connection.close()

    def _report_auth_error(self, exc):
        """Interpreta el fallo de autenticacion SMTP."""
        detail = str(exc).lower()
        is_disabled = any(
            hint in detail for hint in SMTP_AUTH_DISABLED_HINTS
        )
        if is_disabled:
            self.stderr.write(self.style.ERROR(
                '[FALLO] SMTP AUTH esta DESHABILITADO para esta '
                'cuenta o para todo el tenant.\n'
                '  La contrasena de aplicacion podria ser '
                'correcta, pero Microsoft 365 rechaza el SMTP.\n'
                '  Requiere que TI de la UNAM habilite SMTP AUTH '
                'o pasar a Microsoft Graph API.'
            ))
        else:
            self.stderr.write(self.style.ERROR(
                '[FALLO] Autenticacion rechazada (credenciales).\n'
                '  Revisa el usuario y la contrasena de '
                'aplicacion.'
            ))
        self.stderr.write(f'  Respuesta del servidor: {exc}')

    def _send_test_email(self, connection, sender, recipient):
        """Envia un correo de prueba reutilizando la conexion."""
        try:
            msg = EmailMultiAlternatives(
                subject='Prueba de envio - ONIGIES',
                body=(
                    'Correo de prueba enviado desde el backend '
                    'de ONIGIES para verificar la configuracion '
                    'SMTP.'
                ),
                from_email=sender,
                to=[recipient],
                connection=connection,
            )
            sent = msg.send()
        except smtplib.SMTPException as exc:
            self.stderr.write(self.style.ERROR(
                f'[FALLO] Autentico, pero fallo el envio: {exc}'
            ))
            return

        if sent:
            self.stdout.write(self.style.SUCCESS(
                f'[OK] Correo de prueba entregado a {recipient}.'
            ))
        else:
            self.stdout.write(self.style.WARNING(
                '[AVISO] El envio no reporto error pero '
                'devolvio 0.'
            ))