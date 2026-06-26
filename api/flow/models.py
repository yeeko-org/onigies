"""
Modelos del motor de flujo de validación.

- Status: catálogo configurable de status por grupo (bp / cp / gen),
  con transiciones y reglas padre-hijo como M2M autorreferentes.
- FlowEvent: timeline genérico — cambios de status y/o comentarios
  sobre cualquier modelo participante.
- Attachment: adjuntos genéricos asociados a un objeto y opcionalmente
  a un FlowEvent.

La topología padre-hijo de los modelos participantes vive en
flow/registry.py (código, no BD).
"""
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q

from flow.upload_paths import resolve_upload_path

GROUP_CHOICES = [
    ("bp", "Buenas prácticas"),
    ("cp", "Cuestionario principal"),
    ("gen", "Preguntas generales"),
]
ROLE_CHOICES = [
    ("reviewer", "Revisora"),
    ("ies", "Institución"),
]
COMMENT_TYPE_CHOICES = [
    ("none", "Sin comentario"),
    ("optional", "Opcional"),
    ("required", "Obligatorio"),
]


class Status(models.Model):
    """
    Status del flujo de validación.

    `role` indica de quién es el turno: quién puede ejecutar las
    transiciones de salida (`next_statuses`). `role=None` significa
    status terminal: nadie lo mueve.
    """
    name = models.CharField(max_length=120, primary_key=True)
    group = models.CharField(
        max_length=10, choices=GROUP_CHOICES,
        verbose_name="Grupo (flujo)")
    public_name = models.CharField(
        max_length=255, verbose_name="Nombre del estado",
        help_text="Estado que muestra el chip (p.ej. 'Enviado')")
    action_name = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name="Nombre de la acción",
        help_text="Verbo del botón/menú que transiciona HACIA este "
                  "status (p.ej. 'Enviar a revisión'); vacío si nunca "
                  "es destino de una acción manual")
    description = models.TextField(blank=True, null=True)
    color = models.CharField(
        max_length=30, blank=True, null=True,
        help_text="https://vuetifyjs.com/en/styles/colors/")
    icon = models.CharField(
        max_length=40, blank=True, null=True,
        help_text="https://fonts.google.com/icons")
    order = models.IntegerField(default=4)
    is_default = models.BooleanField(
        default=False, verbose_name="Es status por defecto",
        help_text="Status inicial de su grupo (uno por grupo)")
    is_public = models.BooleanField(
        default=False, verbose_name="Es público",
        help_text="Los registros en este status se muestran en la "
                  "página pública")
    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES, blank=True, null=True,
        verbose_name="Turno de",
        help_text="Quién puede ejecutar las transiciones de salida; "
                  "vacío = status terminal")
    comment_type = models.CharField(
        max_length=10, choices=COMMENT_TYPE_CHOICES, default="none",
        verbose_name="Comentario",
        help_text="Si la transición a este status pide un comentario: "
                  "ninguno, opcional u obligatorio")
    requires_confirmation = models.BooleanField(
        default=False, verbose_name="Requiere confirmación",
        help_text="Antes de transicionar a este status, el frontend pide "
                  "una confirmación explícita")
    confirm_title = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name="Título de confirmación",
        help_text="Encabezado del diálogo de confirmación; si está vacío "
                  "el frontend deriva uno de action_name")
    confirm_text = models.TextField(
        blank=True, null=True, verbose_name="Texto de confirmación",
        help_text="Cuerpo del diálogo de confirmación")
    comment_prompt = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name="Rótulo del comentario",
        help_text="Etiqueta de la caja de comentario en el diálogo; "
                  "vacío = el frontend usa un genérico")
    propagates_up = models.BooleanField(
        default=False, verbose_name="Propaga hacia arriba",
        help_text="Al asignarse a un hijo, el padre también lo adopta")
    propagates_down = models.BooleanField(
        default=False, verbose_name="Propaga hacia abajo",
        help_text="Al asignarse, todos los hijos también lo adoptan")
    auto_on_first_save = models.BooleanField(
        default=False, verbose_name="Automático al primer guardado",
        help_text="Se asigna solo cuando la captura se guarda por "
                  "primera vez")
    content_editable = models.BooleanField(
        default=False, verbose_name="Contenido editable",
        help_text="En este status, quien tiene el turno (role) puede "
                  "editar valores; si no, solo puede transicionar")
    hint = models.TextField(
        blank=True, null=True, verbose_name="Sugerencia (frontend)",
        help_text="Guía de siguiente paso que el frontend muestra bajo el "
                  "control de status; distinta de description (tooltip)")
    # Reglas de UX evaluadas en el frontend ANTES de transicionar a este
    # status (lista de nombres en flowRules).
    entry_rules = models.JSONField(
        default=list, blank=True, verbose_name="Reglas de entrada (frontend)",
        help_text="Nombres de reglas del registry flowRules que deben "
                  "cumplirse para mover un objeto a este status")

    applicable_models = models.ManyToManyField(
        ContentType, blank=True, related_name='applicable_statuses',
        verbose_name="Modelos donde aplica")
    next_statuses = models.ManyToManyField(
        'self', symmetrical=False, blank=True,
        related_name='previous_statuses',
        verbose_name="Transiciones posibles")
    valid_child_statuses = models.ManyToManyField(
        'self', symmetrical=False, blank=True,
        related_name='valid_for_parent_statuses',
        verbose_name="Status válidos de los hijos",
        help_text="Para mover el padre a este status, todos sus hijos "
                  "deben estar en alguno de estos")

    def __str__(self):
        return f"{self.group} - {self.public_name}"

    class Meta:
        ordering = ["group", "order"]
        verbose_name = "Status de flujo"
        verbose_name_plural = "Status de flujo"
        constraints = [
            models.UniqueConstraint(
                fields=['group'], condition=Q(is_default=True),
                name='unique_default_per_group'),
        ]


class FlowEvent(models.Model):
    """
    Evento del timeline de un objeto del flujo.

    Con `to_status` es un cambio de status (con comentario opcional);
    con `to_status=None` es un comentario puro.
    """
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    target = GenericForeignKey('content_type', 'object_id')
    from_status = models.ForeignKey(
        Status, on_delete=models.PROTECT, blank=True, null=True,
        related_name='+', verbose_name="Status anterior")
    to_status = models.ForeignKey(
        Status, on_delete=models.PROTECT, blank=True, null=True,
        related_name='+', verbose_name="Status nuevo")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='flow_events')
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.to_status_id:
            return f"{self.target} → {self.to_status_id}"
        return f"Comentario en {self.target}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Evento de flujo"
        verbose_name_plural = "Eventos de flujo"
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]


class Attachment(models.Model):
    """Adjunto genérico de un objeto del flujo."""
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    target = GenericForeignKey('content_type', 'object_id')
    file = models.FileField(
        upload_to=resolve_upload_path, verbose_name="Archivo")
    event = models.ForeignKey(
        FlowEvent, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='attachments',
        help_text="Evento con el que se adjuntó, si aplica")
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        blank=True, null=True, related_name='flow_attachments')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.target} - {self.file.name}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Adjunto"
        verbose_name_plural = "Adjuntos"
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]
