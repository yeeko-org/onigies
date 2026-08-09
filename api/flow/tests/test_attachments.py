"""
Adjuntos del flujo: tope de tamaño en la subida y borrado del archivo
físico al borrarse el registro (`delete_attachment_file`, post_delete).

Todos los tests escriben en un MEDIA_ROOT temporal: el receptor borra de
verdad del storage y no debe tocar los archivos reales de `files/` en el api.
"""
import shutil
import tempfile

from django.core.files.storage import default_storage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import reverse
from rest_framework import status

from example.models import GoodPractice
from flow.models import Attachment
from flow.serializers import MAX_ATTACHMENT_SIZE

from .base import FlowSecurityTestCase

_MEDIA = tempfile.mkdtemp(prefix='onigies-attachments-')


@override_settings(MEDIA_ROOT=_MEDIA)
class AttachmentTests(FlowSecurityTestCase):
    """Subida (tope de 30 MB) y borrado físico de los adjuntos."""

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(_MEDIA, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.client.force_authenticate(self.ies_a)

    # --- helpers ---------------------------------------------------

    def _list_url(self, obj, model_name='goodpracticepackage'):
        return reverse(
            'flow-attachments', args=['example', model_name, obj.pk])

    def _detail_url(self, obj, attachment_id,
                    model_name='goodpracticepackage'):
        return reverse(
            'flow-attachment-detail',
            args=['example', model_name, obj.pk, attachment_id])

    def _upload(self, obj, name='evidencia.pdf', content=b'contenido',
                model_name='goodpracticepackage'):
        upload = SimpleUploadedFile(name, content)
        return self.client.post(
            self._list_url(obj, model_name), {'file': upload},
            format='multipart')

    # --- tope de tamaño --------------------------------------------

    def test_subida_mayor_a_30mb_se_rechaza(self):
        resp = self._upload(
            self.package_a, name='pesado.pdf',
            content=b'\0' * (MAX_ATTACHMENT_SIZE + 1))
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('file', resp.data)
        self.assertEqual(Attachment.objects.count(), 0)

    def test_subida_en_el_limite_se_acepta(self):
        # Exactamente el tope: el único tamaño donde `>` y `>=` difieren.
        resp = self._upload(
            self.package_a, name='justo.pdf',
            content=b'\0' * MAX_ATTACHMENT_SIZE)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Attachment.objects.count(), 1)

    def test_subida_de_tipo_raro_se_acepta(self):
        # No hay validación de extensión ni de content-type a propósito.
        resp = self._upload(
            self.package_a, name='instalador.exe', content=b'MZ\x90\0')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    # --- borrado del archivo físico --------------------------------

    def test_delete_borra_registro_y_archivo(self):
        resp = self._upload(self.package_a)
        attachment = Attachment.objects.get(pk=resp.data['id'])
        name = attachment.file.name
        self.assertTrue(default_storage.exists(name))

        resp = self.client.delete(
            self._detail_url(self.package_a, attachment.pk))
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Attachment.objects.filter(pk=attachment.pk).exists())
        self.assertFalse(default_storage.exists(name))

    def test_borrar_el_target_borra_los_archivos_en_cascada(self):
        practice = GoodPractice.objects.create(
            package=self.package_a, name='Práctica con adjuntos')
        names = []
        for i in range(2):
            resp = self._upload(
                practice, name=f'evidencia_{i}.pdf',
                model_name='goodpractice')
            self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
            names.append(
                Attachment.objects.get(pk=resp.data['id']).file.name)
        for name in names:
            self.assertTrue(default_storage.exists(name))

        practice.delete()

        self.assertEqual(Attachment.objects.count(), 0)
        for name in names:
            self.assertFalse(default_storage.exists(name))

    def test_delete_con_archivo_ya_ausente_no_falla(self):
        resp = self._upload(self.package_a)
        attachment = Attachment.objects.get(pk=resp.data['id'])
        name = attachment.file.name
        default_storage.delete(name)
        self.assertFalse(default_storage.exists(name))

        resp = self.client.delete(
            self._detail_url(self.package_a, attachment.pk))
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Attachment.objects.filter(pk=attachment.pk).exists())