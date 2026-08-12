"""Diagnóstico desechable: migrate_evidences no resucita borrados."""
import shutil
import tempfile

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.test import override_settings

from example.models import Evidence, GoodPractice
from flow.management.commands.migrate_flow_data import Command
from flow.models import Attachment
from flow.tests.base import FlowSecurityTestCase

_MEDIA = tempfile.mkdtemp(prefix='onigies-migrate-')


@override_settings(MEDIA_ROOT=_MEDIA)
class MigrateOrphanTests(FlowSecurityTestCase):

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(_MEDIA, ignore_errors=True)
        super().tearDownClass()

    def test_no_resucita(self):
        practice = GoodPractice.objects.create(
            package=self.package_a, name='P')
        evidence = Evidence.objects.create(good_practice=practice)
        evidence.file.save('vieja.pdf', ContentFile(b'x'), save=True)
        name = evidence.file.name

        cmd = Command()
        cmd.migrate_evidences()
        attachment = Attachment.objects.get()
        self.assertEqual(attachment.file.name, name)

        # 2ª corrida: idempotente
        cmd.migrate_evidences()
        self.assertEqual(Attachment.objects.count(), 1)

        # La IES borra el adjunto (se lleva el archivo compartido)
        attachment.delete()
        self.assertFalse(default_storage.exists(name))
        self.assertTrue(Evidence.objects.filter(pk=evidence.pk).exists())

        # 3ª corrida: NO lo recrea
        cmd.migrate_evidences()
        self.assertEqual(Attachment.objects.count(), 0)