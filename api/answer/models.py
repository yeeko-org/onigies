from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from indicator.models import Observable, Sector
from question.models import (
    QuestionType, ReachQuestion, AQuestion, AOption, PlanQuestion,
    BQuestion, SpecialQuestion)
from survey.models import Survey
from flow.registry import FlowParticipant


class ObservableResponse(FlowParticipant, models.Model):
    flow_parent = 'axis_value'

    survey = models.ForeignKey(
        Survey, on_delete=models.CASCADE, related_name='observable_responses')
    observable = models.ForeignKey(
        Observable, on_delete=models.CASCADE, related_name='responses')
    axis_value = models.ForeignKey(
        'survey.AxisValue', on_delete=models.CASCADE,
        related_name='observable_responses')
    status = models.ForeignKey(
        'flow.Status', on_delete=models.PROTECT, blank=True, null=True,
        related_name='+')
    value = models.BooleanField(
        blank=True, null=True, verbose_name='Respuesta a pregunta inicial')
    flow_events = GenericRelation('flow.FlowEvent')
    flow_attachments = GenericRelation('flow.Attachment')

    def validate_flow_transition(self, user, target) -> list[str]:
        """Gancho del motor: sin la pregunta inicial respondida el
        observable no se da por completado; con la compuerta cerrada la
        IES no lo transiciona, y la revisión no lo transiciona mientras
        el eje siga en turno de la IES."""
        from answer.group_validation import VALIDATED_TARGETS
        from answer.services import review_turn_errors
        from survey.cp_gate import capture_lock_errors

        errors = capture_lock_errors(user, self.survey)
        errors += review_turn_errors(user, self.axis_value)
        if target.name in VALIDATED_TARGETS and self.value is None:
            errors.append(
                'Falta responder la pregunta inicial del observable.')
        return errors

    def __str__(self):
        return f"Response to '{self.observable}' ({self.survey})"

    class Meta:
        verbose_name = 'Respuesta observable'
        verbose_name_plural = 'Respuestas observables'
        constraints = [
            models.UniqueConstraint(
                fields=['survey', 'observable'],
                name='unique_observable_response_per_survey'),
        ]


class GroupResponse(FlowParticipant, models.Model):
    flow_parent = 'observable_response'

    observable_response = models.ForeignKey(
        ObservableResponse, on_delete=models.CASCADE,
        related_name='statuses')
    question_type = models.ForeignKey(
        QuestionType, on_delete=models.CASCADE,
        related_name='group_responses')
    status = models.ForeignKey(
        'flow.Status', on_delete=models.PROTECT, blank=True, null=True,
        related_name='+')
    value = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True)
    flow_events = GenericRelation('flow.FlowEvent')
    flow_attachments = GenericRelation('flow.Attachment')

    def validate_flow_transition(self, user, target) -> list[str]:
        """Gancho del motor: un grupo vacío no se da por completado ni
        por API directa (`answer.group_validation`); con la compuerta
        cerrada la IES no lo transiciona, y la revisión no lo transiciona
        mientras el eje siga en turno de la IES."""
        from answer.group_validation import completion_errors
        from answer.services import review_turn_errors
        from survey.cp_gate import capture_lock_errors

        observable_response = self.observable_response
        errors = capture_lock_errors(user, observable_response.survey)
        errors += review_turn_errors(user, observable_response.axis_value)
        return errors + completion_errors(self, target)

    def __str__(self):
        return (f"{self.question_type_id} de "
                f"{self.observable_response_id}")

    class Meta:
        verbose_name = 'Grupo de Respuestas (por tipo)'
        verbose_name_plural = 'Grupos de Respuestas (por tipo)'
        constraints = [
            models.UniqueConstraint(
                fields=['observable_response', 'question_type'],
                name='unique_group_response_per_type'),
        ]


CP_INITIAL_STATUS = 'cp_pre_start'


def provision_cp_responses(survey, axis_value) -> None:
    """Crea, si faltan, el ObservableResponse de cada observable del eje
    y el GroupResponse de cada tipo que le aplica (fila puente
    `ObservableQuestionType`). Idempotente y en pocas consultas: lo
    llama `Institution.save` en cada guardado y el comando
    `provision_cp_responses` como backfill.

    `bulk_create` no dispara `post_save`, así que el status inicial se
    fija aquí y no por la señal de `flow`.
    """
    from question.models import ObservableQuestionType

    observable_ids = list(Observable.objects.filter(
        component__axis_id=axis_value.axis_id).values_list('id', flat=True))
    existing = set(ObservableResponse.objects.filter(
        survey=survey, observable_id__in=observable_ids,
    ).values_list('observable_id', flat=True))
    ObservableResponse.objects.bulk_create([
        ObservableResponse(
            survey=survey, observable_id=observable_id,
            axis_value=axis_value, status_id=CP_INITIAL_STATUS)
        for observable_id in observable_ids
        if observable_id not in existing
    ])

    responses = dict(ObservableResponse.objects.filter(
        survey=survey, observable_id__in=observable_ids,
    ).values_list('observable_id', 'id'))
    bridge = ObservableQuestionType.objects.filter(
        observable_id__in=observable_ids,
    ).values_list('observable_id', 'question_type_id')
    existing_groups = set(GroupResponse.objects.filter(
        observable_response_id__in=responses.values(),
    ).values_list('observable_response_id', 'question_type_id'))
    GroupResponse.objects.bulk_create([
        GroupResponse(
            observable_response_id=responses[observable_id],
            question_type_id=type_name, status_id=CP_INITIAL_STATUS)
        for observable_id, type_name in bridge
        if (responses[observable_id], type_name) not in existing_groups
    ])


class AResponse(models.Model):
    group_response = models.ForeignKey(
        GroupResponse, on_delete=models.CASCADE,
        related_name='a_responses')
    question = models.ForeignKey(
        AQuestion, on_delete=models.CASCADE, related_name='responses')
    selected_option = models.ForeignKey(
        AOption, on_delete=models.CASCADE,
        related_name='a_responses')

    def __str__(self):
        return f"Response to '{self.question.text}'"

    class Meta:
        verbose_name = 'Respuesta a pregunta A'
        verbose_name_plural = 'Respuestas a preguntas A'


class ReachResponse(models.Model):
    group_response = models.ForeignKey(
        GroupResponse, on_delete=models.CASCADE,
        related_name='reach_responses')
    question = models.ForeignKey(
        ReachQuestion, on_delete=models.CASCADE, related_name='responses')
    not_focalized = models.BooleanField(
        verbose_name='No focalizado en sectores específicos',
        default=False)
    sectors = models.ManyToManyField(
        Sector, related_name='reach_responses', blank=True)

    def __str__(self):
        return f"Response to '{self.question.text}'"

    class Meta:
        verbose_name = 'Respuesta de población'
        verbose_name_plural = 'Respuestas de población'


class PlanResponse(models.Model):
    group_response = models.ForeignKey(
        GroupResponse, on_delete=models.CASCADE,
        related_name='plan_responses')
    question = models.ForeignKey(PlanQuestion, on_delete=models.CASCADE)
    media_plans = models.IntegerField(
        blank=True, null=True, verbose_name='Planes de nivel medio superior')
    superior_plans = models.IntegerField(
        blank=True, null=True, verbose_name='Planes de nivel superior')
    postgraduate_plans = models.IntegerField(
        blank=True, null=True, verbose_name='Planes de nivel posgrado')
    percentage = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True,
        verbose_name='Porcentaje general')

    def __str__(self):
        return f"Plan Response to '{self.question.text}'"

    class Meta:
        verbose_name = 'Respuesta a pregunta de Planes'
        verbose_name_plural = 'Respuestas a preguntas de Planes'


class BResponse(models.Model):
    group_response = models.ForeignKey(
        GroupResponse, on_delete=models.CASCADE,
        related_name='b_responses')
    question = models.ForeignKey(
        BQuestion, on_delete=models.CASCADE, related_name='responses')
    academic_instances_complying = models.IntegerField(blank=True, null=True)
    admin_instances_complying = models.IntegerField(blank=True, null=True)
    percentage = models.DecimalField(
        max_digits=5, decimal_places=2,
        blank=True, null=True, verbose_name='Porcentaje general')

    def __str__(self):
        return f"Response to '{self.question.text}'"

    class Meta:
        verbose_name = 'Respuesta a pregunta B'
        verbose_name_plural = 'Respuestas a preguntas B'


class SpecialResponse(models.Model):
    group_response = models.ForeignKey(
        GroupResponse, on_delete=models.CASCADE,
        related_name='special_responses')
    question = models.ForeignKey(
        SpecialQuestion, on_delete=models.CASCADE,
        related_name='responses')
    total = models.IntegerField(blank=True, null=True)
    complying = models.IntegerField(blank=True, null=True)
    compliance_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name = 'Respuesta a pregunta especial'
        verbose_name_plural = 'Respuestas a preguntas especiales'
