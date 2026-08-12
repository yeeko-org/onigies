from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
import uuid as uuid_lib

YEAR_VALIDATORS = [MinValueValidator(2025), MaxValueValidator(2040)]

TYPE_INSTANCES = (
    ("academic", "Académica"),
    ("admin", "Administrativa"),
)


class Institution(models.Model):

    name = models.CharField(max_length=255, help_text="Nombre completo")
    logo = models.ImageField(upload_to="ies", blank=True, null=True)
    acronym = models.CharField(
        max_length=50, unique=True, verbose_name="Siglas únicas")
    year_start = models.IntegerField(
        blank=True, null=True, validators=YEAR_VALIDATORS)
    year_end = models.IntegerField(
        blank=True, null=True, validators=YEAR_VALIDATORS)
    is_public = models.BooleanField(
        blank=True, null=True, help_text="Es una institución pública?")
    is_centralized = models.BooleanField(
        blank=True, null=True,
        help_text="Gobierno centralizado")
    is_test = models.BooleanField(
        default=False, verbose_name="Institución de prueba",
        help_text="Ve todas las secciones aunque no estén publicadas y "
                  "no la detienen los cierres de periodo. Debe quedar "
                  "fuera de cálculos, indicadores y exportes.")

    def save(self, *args, **kwargs):
        from indicator.models import Axis, Sector, GeneralGroup
        from survey.models import GeneralPackage

        super().save(*args, **kwargs)
        periods = Period.objects.all()
        if self.year_start:
            periods = periods.filter(year__gte=self.year_start)
        if self.year_end:
            periods = periods.filter(year__lte=self.year_end)
        all_axes = Axis.objects.all()
        main_sectors = Sector.objects.filter(is_main=True)
        for period in periods:
            survey, s_created = self.surveys.get_or_create(period=period)
            self._preload_centralized(survey, s_created)
            for axis in all_axes:
                av, av_created = survey.axis_values.get_or_create(axis=axis)
                # Durante la coexistencia se setean ambos flujos (viejo
                # y nuevo); el viejo se retira en la fase de borrado.
                changed = False
                if not av.status_register_id:
                    av.status_register_id = 'pre_start'
                    changed = True
                if not av.status_id:
                    av.status_id = 'cp_pre_start'
                    changed = True
                if changed:
                    av.save()
            for sector in main_sectors:
                survey.population_quantities.get_or_create(sector=sector)

            has_packages = survey.packages.exists()
            # package, p_created = survey.packages.get_or_create(period=period)
            if not has_packages:
                package = survey.packages.create()
                package.status_sending_id = 'draft'
                package.status_id = 'bp_draft'
                package.save()

            # Paquete de preguntas generales (raíz del flujo gen) + sus
            # respuestas por grupo, creados eager como los axis_values.
            gen_pkg, _ = GeneralPackage.objects.get_or_create(survey=survey)
            if not gen_pkg.status_id:
                gen_pkg.status_id = 'gen_draft'
                gen_pkg.save()
            for general_group in GeneralGroup.objects.all():
                survey.general_group_responses.get_or_create(
                    general_group=general_group,
                    defaults={
                        'general_package': gen_pkg,
                        'status_register_id': 'pre_start',
                        'status_id': 'gen_draft',
                    })

    def _preload_centralized(self, survey, survey_created: bool) -> None:
        """Precarga la forma de gobierno que ya conoce el catálogo de
        instituciones como respuesta de la IES, para que no la vuelva a
        capturar. Solo al crear el survey o mientras nadie haya
        contestado: una respuesta capturada jamás se pisa.
        """
        from question.models import GeneralQuestion
        from survey.models import GeneralQuestionResponse

        if self.is_centralized is None:
            return
        question = GeneralQuestion.objects.filter(
            name='is_centralized').first()
        if question is None:
            return
        response, _ = GeneralQuestionResponse.objects.get_or_create(
            survey=survey, general_question=question)
        if not survey_created and response.value_boolean is not None:
            return
        response.value_boolean = self.is_centralized
        response.save(update_fields=['value_boolean'])

    def __str__(self):
        return self.acronym

    class Meta:
        verbose_name = "Institución"
        verbose_name_plural = "Instituciones"


class Instance(models.Model):
    institution = models.ForeignKey(
        Institution, on_delete=models.CASCADE, related_name='instances')
    name = models.CharField(
        max_length=255, verbose_name='Nombre de la instancia')
    acronym = models.CharField(
        max_length=50, blank=True, null=True,
        verbose_name='Siglas de la instancia')
    type_instance = models.CharField(
        max_length=20, choices=TYPE_INSTANCES,
        verbose_name='Tipo de instancia')
    order = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.institution.acronym})"

    class Meta:
        ordering = ['order']
        verbose_name = 'Dependencia'
        verbose_name_plural = 'Dependencias'


class User(AbstractUser):
    phone = models.CharField(max_length=100, blank=True)
    reviewer = models.BooleanField(
        default=False, verbose_name='Es revisora',
        help_text='Puede verificar las respuestas y buenas prácticas')
    password_changed = models.BooleanField(
        default=False, verbose_name='Contraseña cambiada')
    institution = models.ForeignKey(
        Institution, on_delete=models.CASCADE, blank=True, null=True,
        related_name='users')

    def get_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        if self.first_name or self.last_name:
            return f"{self.first_name or self.last_name}"
        return self.username or self.email

    @property
    def is_reviewer(self):
        if self.is_anonymous:
            return False
        return self.is_superuser or self.is_staff or self.reviewer

    @property
    def is_admin(self):
        if self.is_anonymous:
            return False
        return self.is_superuser or self.is_staff

    class Meta:
        verbose_name = "Persona usuaria"
        verbose_name_plural = "1. Personas usuarias"


class InvitationToken(models.Model):
    key = models.UUIDField(
        primary_key=True, default=uuid_lib.uuid4, editable=False)
    email = models.EmailField(
        verbose_name="Correo electrónico", blank=True, null=True)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Creado")
    viewed_at = models.DateTimeField(
        verbose_name="Fecha en que se vio", blank=True, null=True)
    used_at = models.DateTimeField(
        verbose_name="Fecha en que se usó",
        blank=True, null=True)
    user = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE)
    institution = models.ForeignKey(
        Institution, blank=True, null=True,
        on_delete=models.CASCADE, related_name='invitation_tokens')
    reviewer = models.BooleanField(
        default=False, verbose_name="Es revisora",
        help_text="Solo aplica para invitaciones sin institución")
    is_staff = models.BooleanField(
        default=False, verbose_name="Es staff")
    is_superuser = models.BooleanField(
        default=False, verbose_name="Es superusuario")
    email_sent = models.BooleanField(
        default=False, verbose_name="Correo enviado",
        help_text="El correo fue enviado exitosamente")

    class Meta:
        verbose_name = "Token de Invitación"
        verbose_name_plural = "Tokens de Invitación"

    def __str__(self):
        return "%s - %s" % (self.institution, self.key)


class PasswordRecoveryToken(models.Model):
    EXPIRY_HOURS = 24

    key = models.UUIDField(
        primary_key=True,
        default=uuid_lib.uuid4,
        editable=False,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recovery_tokens',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(
        verbose_name="Fecha en que se usó",
        blank=True,
        null=True,
    )

    def save(self, *args, **kwargs):
        from django.utils import timezone
        from datetime import timedelta
        if not self.pk or not self.expires_at:
            self.expires_at = timezone.now() + timedelta(
                hours=self.EXPIRY_HOURS
            )
        super().save(*args, **kwargs)

    def is_valid(self):
        from django.utils import timezone
        return (
            self.used_at is None
            and timezone.now() < self.expires_at
        )

    def mark_used(self):
        from django.utils import timezone
        self.used_at = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.user.email} - {self.key}"

    class Meta:
        verbose_name = "Token de Recuperación"
        verbose_name_plural = "Tokens de Recuperación"
        ordering = ['-created_at']


class Period(models.Model):
    year = models.IntegerField(
        primary_key=True, help_text="Año", editable=False)
    explanation = models.TextField(
        verbose_name="Recuento de fechas", blank=True, null=True)
    good_practices_published = models.BooleanField(
        verbose_name="Buenas prácticas publicadas", default=False)
    results_published = models.BooleanField(
        verbose_name="Resultados publicados", default=False)
    submission_deadline = models.DateField(
        verbose_name="Fecha límite de envío", blank=True, null=True,
        help_text="Último día para enviar buenas prácticas; al día "
                  "siguiente el periodo cierra solo.")
    gen_submission_deadline = models.DateField(
        verbose_name="Fecha límite de envío de generales",
        blank=True, null=True,
        help_text="Último día para enviar las preguntas generales; al "
                  "día siguiente el periodo cierra solo.")

    def __str__(self):
        return str(self.year)

    @property
    def is_bp_submission_closed(self) -> bool:
        """Fuente única del cierre de envío de buenas prácticas: cerrado
        si se publicó a mano o si ya pasó la fecha límite. El día límite
        cuenta como abierto (cierra al día siguiente, hora del servidor).
        """
        if self.good_practices_published:
            return True
        if self.submission_deadline:
            return timezone.localdate() > self.submission_deadline
        return False

    @property
    def is_gen_submission_closed(self) -> bool:
        """Cierre del envío de las preguntas generales. A diferencia de
        bp no hay bandera manual de publicación —gen no se publica—, así
        que solo pesa la fecha límite. El día límite cuenta como abierto.
        """
        if self.gen_submission_deadline:
            return timezone.localdate() > self.gen_submission_deadline
        return False

    class Meta:
        verbose_name = "Periodo"
        verbose_name_plural = "Periodos"


GROUP_CHOICES = [
    ("register", "Registro"),
    ("sending", "Envío"),
    ("validation", "Validación"),
]
ROLE_CHOICES = [
    ("validator", "Validador"),
    ("ies", "Institución"),
]


class StatusControl(models.Model):
    name = models.CharField(max_length=120, primary_key=True)
    group = models.CharField(
        max_length=10, choices=GROUP_CHOICES,
        verbose_name="grupo de status", default="petition")
    public_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    color = models.CharField(
        max_length=30, blank=True, null=True,
        help_text="https://vuetifyjs.com/en/styles/colors/")
    icon = models.CharField(
        max_length=40, blank=True, null=True,
        help_text="https://fonts.google.com/icons")
    order = models.IntegerField(default=4)
    is_default = models.BooleanField(
        default=False, verbose_name="Es status por defecto")

    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES,
        blank=True, null=True,
        verbose_name="rol asociado")
    can_send = models.BooleanField(
        default=False, verbose_name="Puede enviarse",
        help_text="Se puede enviar el paquete a la siguiente etapa")
    is_final = models.BooleanField(default=False)
    # is_public = models.BooleanField(default=True)
    priority = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.group} - {self.public_name}"

    class Meta:
        ordering = ["group", "order"]
        verbose_name = "Status de control"
        verbose_name_plural = "Status de control (TODOS)"
