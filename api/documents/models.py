from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils.text import slugify


class Generator(models.TextChoices):
    QUESTIONNAIRE_DOCX = (
        'questionnaire_docx', 'Cuestionario en Word, generado desde la base')


class PublicDocument(models.Model):
    """Documento descargable sin sesión: subido a mano o generado."""
    title = models.CharField(max_length=255, verbose_name="Título")
    # Forma parte de la URL pública que enlaza el sitio heredado:
    # cambiarlo rompe esos enlaces.
    slug = models.SlugField(
        max_length=120, unique=True, blank=True,
        verbose_name="Identificador en la URL",
        help_text="Se genera del título si se deja vacío")
    description = models.TextField(
        blank=True, default='', verbose_name="Descripción")
    file = models.FileField(
        upload_to='public_documents/', blank=True, verbose_name="Archivo")
    generator = models.CharField(
        max_length=40, choices=Generator.choices, blank=True, default='',
        verbose_name="Generador",
        help_text="Si se indica, el archivo se genera al descargarlo")
    is_published = models.BooleanField(
        default=False, verbose_name="Publicado")
    order = models.SmallIntegerField(default=5, verbose_name="Orden")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def clean(self):
        if bool(self.file) == bool(self.generator):
            raise ValidationError(
                "Un documento lleva archivo o generador, exactamente uno.")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._unique_slug()
        super().save(*args, **kwargs)

    def _unique_slug(self) -> str:
        base = slugify(self.title)[:100] or 'documento'
        slug, n = base, 2
        others = PublicDocument.objects.exclude(pk=self.pk)
        while others.filter(slug=slug).exists():
            slug, n = f'{base}-{n}', n + 1
        return slug

    class Meta:
        ordering = ['order', 'title']
        verbose_name = "Documento público"
        verbose_name_plural = "Documentos públicos"
        constraints = [
            models.CheckConstraint(
                condition=(
                    (Q(file='') & ~Q(generator=''))
                    | (~Q(file='') & Q(generator=''))),
                name='public_document_file_xor_generator',
            ),
        ]
