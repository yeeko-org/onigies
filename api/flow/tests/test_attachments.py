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

    def _download_url(self, obj, attachment_id,
                      model_name='goodpracticepackage'):
        return reverse(
            'flow-attachment-download',
            args=['example', model_name, obj.pk, attachment_id])

    def _upload(self, obj, name='evidencia.pdf', content=b'contenido',
                model_name='goodpracticepackage'):
        upload = SimpleUploadedFile(name, content)
        return self.client.post(
            self._list_url(obj, model_name), {'file': upload},
            format='multipart')

    # --- tope de tamaño --------------------------------------------

    def test_upload_over_30mb_is_rejected(self):
        resp = self._upload(
            self.package_a, name='pesado.pdf',
            content=b'\0' * (MAX_ATTACHMENT_SIZE + 1))
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('file', resp.data)
        self.assertEqual(Attachment.objects.count(), 0)

    def test_upload_at_the_limit_is_accepted(self):
        # Exactamente el tope: el único tamaño donde `>` y `>=` difieren.
        resp = self._upload(
            self.package_a, name='justo.pdf',
            content=b'\0' * MAX_ATTACHMENT_SIZE)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Attachment.objects.count(), 1)

    def test_upload_of_odd_type_is_accepted(self):
        # No hay validación de extensión ni de content-type a propósito.
        resp = self._upload(
            self.package_a, name='instalador.exe', content=b'MZ\x90\0')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    # --- borrado del archivo físico --------------------------------

    def test_delete_removes_record_and_file(self):
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

    def test_deleting_target_cascades_file_deletion(self):
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

    def test_delete_with_missing_file_does_not_fail(self):
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

    # --- descarga ---------------------------------------------------

    def test_download_redirects_to_file(self):
        # El endpoint nunca sirve el archivo: redirige a la URL del
        # storage, que en S3 es firmada y efímera.
        resp = self._upload(self.package_a)
        attachment = Attachment.objects.get(pk=resp.data['id'])

        resp = self.client.get(
            self._download_url(self.package_a, attachment.pk))
        self.assertEqual(resp.status_code, status.HTTP_302_FOUND)
        self.assertEqual(resp.headers['Location'], attachment.file.url)

    def test_download_without_redirect_returns_the_url(self):
        # El front manda el token por XHR y no puede seguir el 302 con
        # la cabecera Authorization: pide la URL y la abre.
        resp = self._upload(self.package_a)
        attachment = Attachment.objects.get(pk=resp.data['id'])

        resp = self.client.get(
            self._download_url(self.package_a, attachment.pk),
            {'redirect': 'false'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['url'], attachment.file.url)

    def test_download_from_other_ies_is_rejected(self):
        resp = self._upload(self.package_a)
        attachment = Attachment.objects.get(pk=resp.data['id'])

        self.client.force_authenticate(self.ies_b)
        resp = self.client.get(
            self._download_url(self.package_a, attachment.pk))
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_public_download_is_open_to_anyone(self):
        resp = self._upload(self.package_a)
        attachment = Attachment.objects.get(pk=resp.data['id'])
        Attachment.objects.filter(pk=attachment.pk).update(is_public=True)
        url = self._download_url(self.package_a, attachment.pk)

        self.client.force_authenticate(self.ies_b)
        self.assertEqual(
            self.client.get(url).status_code, status.HTTP_302_FOUND)

        # Público de verdad: sin sesión también se descarga.
        self.client.force_authenticate(None)
        self.assertEqual(
            self.client.get(url).status_code, status.HTTP_302_FOUND)

    def test_private_download_hides_existence_from_anonymous(self):
        # 404 y no 401: un id válido y uno inventado deben responder
        # igual, o desde fuera se pueden enumerar los adjuntos.
        resp = self._upload(self.package_a)
        attachment = Attachment.objects.get(pk=resp.data['id'])

        self.client.force_authenticate(None)
        resp = self.client.get(
            self._download_url(self.package_a, attachment.pk))
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_serializer_url_points_to_endpoint(self):
        # Nunca la URL del storage: la firmada caduca y no revalida
        # quién puede leer el adjunto.
        resp = self._upload(self.package_a)
        attachment = Attachment.objects.get(pk=resp.data['id'])

        resp = self.client.get(self._list_url(self.package_a))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        expected = self._download_url(self.package_a, attachment.pk)
        self.assertEqual(
            resp.data[0]['url'], f'http://testserver{expected}')