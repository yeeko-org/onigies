from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from indicator.models import Axis, Component, Sector, GeneralGroup
from ies.models import Institution, Period, StatusControl, Instance, User
from question.models import GeneralQuestion
from flow.registry import FlowParticipant


class Comment(models.Model):
    text = models.TextField(verbose_name='Texto del comentario')
    status_register = models.ForeignKey(
        StatusControl, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "Comment"

    class Meta:
        abstract = True


class Survey(models.Model):

    institution = models.ForeignKey(
        Institution, on_delete=models.CASCADE, related_name='surveys')
    period = models.ForeignKey(
        Period, on_delete=models.CASCADE, related_name='surveys')
    instances = models.ManyToManyField(
        Instance, related_name='surveys',
        verbose_name='Instancias', blank=True)
    # Fuente histórica de la existencia de poblaciones (adr-0008). Ya no
    # se escribe: la existencia vive en PopulationQuantity.is_present
    # (adr-0012) y esta columna está en vías de borrarse.
    sectors_legacy = models.ManyToManyField(
        Sector, related_name='surveys',
        verbose_name='Sectores atendidos', blank=True)
    # Única respuesta de pregunta general que sigue viviendo en columna:
    # es operacional (enciende la columna no binaria de las tablas) y no
    # alimenta indicadores, así que quedó fuera de la mudanza a
    # GeneralQuestionResponse.
    measures_non_binary = models.BooleanField(
        blank=True, null=True,
        verbose_name='Registra o mide población no binaria')

    @property
    def sectors(self) -> list[int]:
        """Ids de los sectores presentes, derivados de las filas con
        `is_present` verdadero (adr-0012). Itera en Python para no
        romper el prefetch de `population_quantities`."""
        return [pq.sector_id for pq in self.population_quantities.all()
                if pq.is_present]

    @property
    def is_test(self) -> bool:
        """Delegación a la bandera de la institución. Los candados de
        cierre de periodo cuelgan del survey, no de la institución, así
        que se consulta desde aquí para no repetir el salto de FK."""
        return self.institution.is_test

    def __str__(self):
        return f"Survey: {self.institution.name} - {self.period}"

    class Meta:
        unique_together = ('institution', 'period')
        verbose_name = 'Respuestas anuales de una IES'
        verbose_name_plural = 'Respuestas anuales de las IES'


class AxisValue(FlowParticipant, models.Model):
    survey = models.ForeignKey(
        Survey, on_delete=models.CASCADE, related_name='axis_values')
    axis = models.ForeignKey(
        Axis, on_delete=models.CASCADE, related_name='axis_values')
    value = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True)
    status_register = models.ForeignKey(
        StatusControl, on_delete=models.CASCADE, blank=True, null=True)
    # Flujo nuevo; coexiste con status_register hasta verificar la
    # migración de datos (ver docs/records/2026-06-05-diseno-del-motor-de-flujo.md §5).
    status = models.ForeignKey(
        'flow.Status', on_delete=models.PROTECT, blank=True, null=True,
        related_name='+')
    flow_events = GenericRelation('flow.FlowEvent')
    flow_attachments = GenericRelation('flow.Attachment')

    def __str__(self):
        return f"{self.axis.name}: {self.value}"

    class Meta:
        verbose_name = 'Valor del eje'
        verbose_name_plural = 'Valores de los ejes'
        unique_together = ('survey', 'axis')


class ComponentValue(models.Model):
    survey = models.ForeignKey(
        Survey, on_delete=models.CASCADE, related_name='component_values')
    component = models.ForeignKey(
        Component, on_delete=models.CASCADE, related_name='component_values')
    value = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.component.name}: {self.value}"

    class Meta:
        verbose_name = 'Valor del componente'
        verbose_name_plural = 'Valores de los componentes'


class PopulationQuantity(models.Model):
    survey = models.ForeignKey(
        Survey, on_delete=models.CASCADE, related_name='population_quantities')
    sector = models.ForeignKey(
        Sector, on_delete=models.CASCADE, related_name='population_quantities')
    no_apply = models.BooleanField(default=False, verbose_name="No Aplica")
    # Opcional: solo los sectores con `needs_name` piden un texto libre;
    # el resto se identifica por el propio sector.
    name = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name='Nombre del sector')
    # Tri-estado: verdadero «está presente», falso un «no» explícito y
    # nulo la fila que nadie tocó (adr-0012).
    is_present = models.BooleanField(
        blank=True, null=True, verbose_name='Está presente')
    number_women = models.PositiveIntegerField(
        verbose_name='Número de mujeres', blank=True, null=True)
    number_men = models.PositiveIntegerField(
        verbose_name='Número de hombres', blank=True, null=True)
    number_non_binary = models.PositiveIntegerField(
        verbose_name='Número de personas no binarias',
        blank=True, null=True)

    def __str__(self):
        return f"{self.sector.name}: {self.number_men} hombres, {self.number_women} mujeres"

    class Meta:
        verbose_name = 'Cantidad de población por sector'
        verbose_name_plural = 'Cantidades de población por sector'


class GeneralQuestionResponse(models.Model):
    """Respuesta a una pregunta general por (survey, pregunta).

    Aquí vive el valor escalar: `q_type` de la pregunta dicta cuál de las
    dos columnas tipadas aplica. Se descartó un JSON único porque los
    indicadores y el ETL consultan estas columnas sin castear.

    Agregar una pregunta al catálogo ya no exige columnas en el Survey.
    La excepción es `measures_non_binary`, operacional, que se quedó como
    columna del Survey.
    """

    survey = models.ForeignKey(
        Survey, on_delete=models.CASCADE, related_name='question_responses')
    # PROTECT: una pregunta viva jamás se borra; si alguien lo intenta
    # con respuestas capturadas, tiene que doler y ser explícito.
    general_question = models.ForeignKey(
        GeneralQuestion, on_delete=models.PROTECT,
        related_name='responses')
    no_apply = models.BooleanField(default=False, verbose_name="No Aplica")
    value_integer = models.IntegerField(
        blank=True, null=True, verbose_name='Respuesta numérica')
    value_boolean = models.BooleanField(
        blank=True, null=True, verbose_name='Respuesta booleana')

    @property
    def value(self):
        """El valor que corresponde al tipo de la pregunta. El nulo es
        «sin responder» en ambos casos."""
        if self.general_question.q_type == 'boolean':
            return self.value_boolean
        return self.value_integer

    def __str__(self):
        return f"{self.general_question.name}: {self.value}"

    class Meta:
        unique_together = ('survey', 'general_question')
        verbose_name = 'Respuesta a pregunta general'
        verbose_name_plural = 'Respuestas a preguntas generales'


class GeneralPackage(FlowParticipant, models.Model):
    """
    Envío de las preguntas generales de un survey: raíz del flujo gen.

    1:1 con Survey; agrupa los GeneralGroupResponse. Guarda el status de envío
    """
    survey = models.OneToOneField(
        Survey, on_delete=models.CASCADE, related_name='general_package')
    status = models.ForeignKey(
        'flow.Status', on_delete=models.PROTECT, blank=True, null=True,
        related_name='+')
    sent_at = models.DateTimeField(blank=True, null=True)
    flow_events = GenericRelation('flow.FlowEvent')
    flow_attachments = GenericRelation('flow.Attachment')

    def save(self, *args, **kwargs):
        # Registra la fecha de envío la primera vez que el motor
        # transiciona a gen_sent o gen_resent (no se borra al reenviar).
        if (self.sent_at is None
                and self.status_id in ('gen_sent', 'gen_resent')):
            from django.utils import timezone
            self.sent_at = timezone.now()
        super().save(*args, **kwargs)

    def validate_flow_transition(self, user, target) -> list[str]:
        """Gancho del motor (flow.services.validate_transition): con el
        periodo cerrado la IES no puede transicionar el envío. La
        revisora sí sigue revisando después del cierre, y una
        institución de prueba nunca queda atrapada por el cierre."""
        if not self.survey.period.is_gen_submission_closed:
            return []
        if user.is_reviewer or self.survey.is_test:
            return []
        return ['El periodo de envío de las preguntas generales ya '
                'cerró; no puedes enviarlas a revisión.']

    def __str__(self):
        return (f"Envío de Preguntas Generales - "
                f"{self.survey.institution.acronym} - "
                f"{self.survey.period.year}")

    class Meta:
        verbose_name = "Envío de Preguntas Generales"
        verbose_name_plural = "Envíos de Preguntas Generales"


class GeneralGroupResponse(FlowParticipant, models.Model):
    flow_parent = 'general_package'

    survey = models.ForeignKey(
        Survey, on_delete=models.CASCADE,
        related_name='general_group_responses')
    general_package = models.ForeignKey(
        GeneralPackage, on_delete=models.CASCADE, blank=True, null=True,
        related_name='general_group_responses')
    general_group = models.ForeignKey(
        GeneralGroup, on_delete=models.CASCADE,
        related_name='general_group_responses')
    status_register = models.ForeignKey(
        StatusControl, on_delete=models.CASCADE)
    status = models.ForeignKey(
        'flow.Status', on_delete=models.PROTECT, blank=True, null=True,
        related_name='+')
    flow_events = GenericRelation('flow.FlowEvent')
    flow_attachments = GenericRelation('flow.Attachment')

    def validate_flow_transition(self, user, target) -> list[str]:
        """Gancho del motor (flow.services.validate_transition): un grupo
        con respuestas faltantes no puede darse por completado, ni
        siquiera por API directa. Reglas en `survey.general_validation`,
        espejo de la compuerta del frontend."""
        from survey.general_validation import completion_errors
        return completion_errors(self, target)

    def __str__(self):
        return (f"Respuesta del grupo general "
                f"'{self.general_group}' ({self.survey})")

    class Meta:
        verbose_name = 'Grupo de Respuestas General'
        verbose_name_plural = 'Grupos de Respuestas Generales'


class GeneralGroupComment(Comment):
    general_group_response = models.ForeignKey(
        GeneralGroupResponse, on_delete=models.CASCADE,
        related_name='comments')

    class Meta:
        verbose_name = 'Comentario a grupo de respuestas (General)'
        verbose_name_plural = 'Comentarios a grupos de respuestas (General)'
