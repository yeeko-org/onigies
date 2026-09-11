from decimal import Decimal
from functools import cached_property

from django.db import models

from ies.models import StatusControl, User

STANDARD_TYPE_NAMES = frozenset({'a_questions', 'b_questions', 'reach'})


class GeneralGroup(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    public_name = models.CharField(max_length=150)
    title = models.CharField(
        max_length=255, blank=True, verbose_name="Título del bloque")
    subtitle = models.CharField(
        max_length=255, blank=True, verbose_name="Subtítulo")
    instruction = models.TextField(
        blank=True, verbose_name="Instrucción para la IES")
    is_population = models.BooleanField(default=False)
    # Orden del instrumento, no de captura: el grupo `autoridades` se
    # sembró después que los demás y por id saldría al final.
    order = models.PositiveSmallIntegerField(
        default=0, verbose_name="Orden en el cuestionario")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']
        verbose_name = "Grupo de preguntas (Generales)"
        verbose_name_plural = "Grupos de preguntas (Generales)"


class Axis(models.Model):
    order = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, unique=True)
    short_name = models.CharField(max_length=100, blank=True, null=True)
    slug = models.CharField(max_length=55, blank=True, null=True)
    # logo = models.ImageField(blank=True, null=True, upload_to='axis_logos')
    icon = models.CharField(max_length=55, blank=True, null=True)
    color = models.CharField(max_length=55)
    hex_color = models.CharField(max_length=7, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']
        verbose_name = "Materia (Axis)"
        verbose_name_plural = "Materias (Axes)"


class Component(models.Model):

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    axis = models.ForeignKey(Axis, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.axis.name})"

    class Meta:
        verbose_name = "Componente"
        verbose_name_plural = "Componentes"


class Observable(models.Model):

    component = models.ForeignKey(
        Component, on_delete=models.CASCADE, related_name='observables')

    # CharField y no Decimal: "1.10" y "1.1" son el mismo Decimal, pero
    # son observables distintos del cuestionario (ver
    # docs/records/2026-07-04-seed-del-cuestionario.md).
    number = models.CharField(max_length=10)
    # Orden global de recorrido del cuestionario; lo asigna
    # load_questionnaire, no es editable a mano.
    order = models.IntegerField(default=0)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    init_question = models.TextField(blank=True, null=True)
    a_main_question = models.TextField(
        blank=True, null=True,
        verbose_name="Pregunta de armonización e institucionalización")
    a_main_subtitle = models.TextField(
        blank=True, null=True,
        verbose_name="Subtítulo de armonización e institucionalización")

    @cached_property
    def uses_default_weights(self) -> bool:
        """Los defaults del tipo se calibraron para el trío estándar; en
        cualquier otra combinación se captura fila por fila."""
        names = {row.question_type_id for row in self.type_weights.all()}
        return names == STANDARD_TYPE_NAMES

    @property
    def weights_pending(self) -> bool:
        """Aviso, nunca bloqueo."""
        return any(
            row.final_weight is None for row in self.type_weights.all())

    def weight_for(self, type_name: str) -> Decimal | None:
        """Pasa por el accesor inverso de la tabla puente para no
        importar `question` desde aquí: ya importa este módulo."""
        row = self.type_weights.filter(
            question_type_id=type_name).first()
        return row.final_weight if row else None

    def __str__(self):
        return f"{self.name} ({self.component.name})"

    class Meta:
        ordering = ['order']
        verbose_name = "Observable (Pregunta inicial)"
        verbose_name_plural = "Observables (Preguntas iniciales)"


class Sector(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    needs_name = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    is_main = models.BooleanField(
        default=True, verbose_name="Es sector principal")
    is_authority = models.BooleanField(
        default=False, verbose_name="Es autoridad")
    # Las 2 poblaciones que completan POB-ESTÁNDAR junto a las 10
    # `is_main`; quedan fuera de la composición del observable 1.7.
    is_standard_extra = models.BooleanField(
        default=False, verbose_name="Es población extra del estándar")
    # «Titular de la IES»: se captura como total 1 con number_women 0/1
    # (la respuesta «¿Mujer?»), no como conteo de población.
    is_ies_head = models.BooleanField(
        default=False, verbose_name="Es titular de la IES")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']
        verbose_name = "Sector"
        verbose_name_plural = "Sectores"
