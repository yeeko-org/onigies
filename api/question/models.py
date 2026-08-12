from django.db import models

from indicator.models import GeneralGroup, Observable, Sector

GENERAL_Q_TYPES = [
    ("integer", "Número entero"),
    ("boolean", "Sí / No"),
]


class QuestionType(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    weight_name = models.CharField(max_length=40)
    public_name = models.CharField(max_length=150)
    model_question = models.CharField(max_length=50, blank=True, null=True)
    default_weight = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True)
    model_response = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tipo de preguntas"
        verbose_name_plural = "Tipos de preguntas"


class AQuestion(models.Model):

    text = models.TextField()
    observable = models.ForeignKey(Observable, on_delete=models.CASCADE)
    # Clave natural del seed: (observable, order). Sin ella, corregir la
    # redacción de una opción duplicaría la fila al re-sembrar.
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"Pregunta: {self.text} ({self.observable.name})"

    class Meta:
        ordering = ['order']
        verbose_name = "Pregunta de institucionalización"
        verbose_name_plural = "Preguntas de institucionalización"


class AOption(models.Model):
    text = models.CharField(max_length=255)
    value = models.IntegerField()

    def __str__(self):
        return f"Opción de respuesta: {self.text} (Valor: {self.value})"

    class Meta:
        verbose_name = "Opción de respuesta de institucionalización"
        verbose_name_plural = "Opciones de respuesta de institucionalización"


class ReachQuestion(models.Model):

    text = models.TextField()
    observable = models.ForeignKey(Observable, on_delete=models.CASCADE)
    has_main_sectors = models.BooleanField(
        default=True, verbose_name="Tiene los sectores principales")
    others_sectors = models.ManyToManyField(Sector, blank=True)
    has_general_planning = models.BooleanField(
        default=False, verbose_name="Tiene la opción de planeación general")

    def __str__(self):
        return f"{self.text} ({self.observable.name})"

    class Meta:
        verbose_name = "Pregunta de alcance de población"
        verbose_name_plural = "Preguntas de alcance de población"


class PlanQuestion(models.Model):
    observable = models.ForeignKey(Observable, on_delete=models.CASCADE)
    text = models.TextField()
    # Clave natural del seed: (observable, order), mismo patrón de
    # AQuestion.
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"Pregunta de planes: {self.text} ({self.observable.name})"

    class Meta:
        ordering = ['order']
        verbose_name = "Pregunta de planes"
        verbose_name_plural = "Preguntas de planes"


class BQuestion(models.Model):

    observable = models.ForeignKey(Observable, on_delete=models.CASCADE)
    order = models.IntegerField(default=10)
    text = models.TextField()
    includes_academic = models.BooleanField(
        blank=True, null=True,
        verbose_name="Incluye entidades académicas")
    includes_admin = models.BooleanField(
        blank=True, null=True,
        verbose_name="Incluye dependencias administrativas")

    def __str__(self):
        return f"Pregunta cuerpo: {self.text} ({self.observable.name})"

    class Meta:
        verbose_name = "Pregunta de transversalización"
        verbose_name_plural = "Preguntas de transversalización"


class GeneralQuestion(models.Model):
    """Pregunta de la sección «Información de base», colgada de un
    GeneralGroup (`indicator.GeneralGroup`) en vez del observable.
    """

    general_group = models.ForeignKey(
        GeneralGroup, on_delete=models.CASCADE, related_name='questions')
    # Clave estable: mapea a la columna del Survey donde aterriza la
    # respuesta y ancla el comportamiento custom que vive en código;
    # cambiarla rompe la persistencia, por eso no se edita.
    name = models.CharField(max_length=100, verbose_name="Clave interna")
    text = models.TextField(verbose_name="Pregunta")
    hint = models.TextField(blank=True, verbose_name="Texto de ayuda")
    label = models.CharField(
        max_length=100, blank=True, verbose_name="Rótulo del campo")
    # Unidad de lo que se cuenta ("instancias", "planes"): sirve de
    # rótulo cuando no se capturó uno propio.
    unit = models.CharField(max_length=50, blank=True, verbose_name="Unidad")
    q_type = models.CharField(
        max_length=10, choices=GENERAL_Q_TYPES, default="integer",
        verbose_name="Tipo de respuesta")
    order = models.IntegerField(default=0)
    addl_config = models.JSONField(default=dict, blank=True)

    @property
    def effective_label(self) -> str:
        """Rótulo que ve la IES: el propio si existe, si no la unidad."""
        return self.label or self.unit

    def __str__(self):
        return f"Pregunta general: {self.text} ({self.general_group_id})"

    class Meta:
        ordering = ['order']
        unique_together = ('general_group', 'name')
        verbose_name = "Pregunta general (Información de base)"
        verbose_name_plural = "Preguntas generales (Información de base)"


class SpecialQuestion(models.Model):

    text = models.TextField()
    observable = models.ForeignKey(Observable, on_delete=models.CASCADE)

    def __str__(self):
        return f"Pregunta especial: {self.text} ({self.observable.name})"

    class Meta:
        verbose_name = "Pregunta especial"
        verbose_name_plural = "Preguntas especiales"



