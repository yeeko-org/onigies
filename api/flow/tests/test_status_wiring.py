"""
Cableado del status inicial (B4): todo participante creado sin status
recibe el default de su grupo; `assign_auto_status` promueve al status
`auto_on_first_save` en la primera captura. Incluye la regresión de
persistencia de `sent_at` en las transiciones de envío.
"""
from example.models import GoodPracticePackage
from flow.models import FlowEvent, Status
from flow.services import assign_auto_status, execute_transition
from indicator.models import Axis
from survey.models import AxisValue

from .base import FlowSecurityTestCase


class InitialStatusWiringTests(FlowSecurityTestCase):
    """B4: cableado del status inicial vía señal y assign_auto_status."""

    def test_paquete_sin_status_recibe_default(self):
        pkg = GoodPracticePackage.objects.create(survey=self.survey_a)
        self.assertEqual(pkg.status_id, 'bp_draft')

    def test_axis_value_sin_status_recibe_default(self):
        axis = Axis.objects.create(name='Eje 1', color='blue')
        av = AxisValue.objects.create(survey=self.survey_a, axis=axis)
        self.assertEqual(av.status_id, 'cp_pre_start')

    def test_assign_auto_status_promueve_a_filling(self):
        axis = Axis.objects.create(name='Eje 2', color='blue')
        av = AxisValue.objects.create(survey=self.survey_a, axis=axis)
        self.assertEqual(av.status_id, 'cp_pre_start')

        event = assign_auto_status(self.ies_a, av)
        av.refresh_from_db()
        self.assertEqual(av.status_id, 'cp_filling')
        self.assertIsNotNone(event)
        self.assertTrue(
            FlowEvent.objects.filter(
                object_id=av.pk, to_status_id='cp_filling').exists())

    def test_assign_auto_status_no_revierte_objeto_avanzado(self):
        axis = Axis.objects.create(name='Eje 3', color='blue')
        av = AxisValue.objects.create(survey=self.survey_a, axis=axis)
        av.status_id = 'cp_approved'
        av.save(update_fields=['status'])
        self.assertIsNone(assign_auto_status(self.ies_a, av))


class SentAtPersistenceTests(FlowSecurityTestCase):
    """
    Regresión: `_save_status` guardaba con `update_fields=['status']`, así
    que el hook de `GoodPracticePackage.save` fijaba `sent_at` en memoria
    pero nunca llegaba a la base. Por eso todas las aserciones leen de BD.
    """

    def _status(self, name: str) -> Status:
        return Status.objects.get(name=name)

    def test_envio_persiste_sent_at_en_bd(self) -> None:
        self.assertIsNone(self.package_a.sent_at)
        execute_transition(
            self.ies_a, self.package_a, self._status('bp_sent'))

        from_db = GoodPracticePackage.objects.get(pk=self.package_a.pk)
        self.assertEqual(from_db.status_id, 'bp_sent')
        self.assertIsNotNone(from_db.sent_at)

    def test_reenvio_no_pisa_el_sent_at_original(self) -> None:
        execute_transition(
            self.ies_a, self.package_a, self._status('bp_sent'))
        original = GoodPracticePackage.objects.get(
            pk=self.package_a.pk).sent_at
        self.assertIsNotNone(original)

        # El camino real pasa por la revisora y las prácticas; aquí solo
        # interesa el hook, así que se fija el status previo con .update()
        # (sin disparar save) y se transiciona el último paso.
        GoodPracticePackage.objects.filter(pk=self.package_a.pk).update(
            status_id='bp_need_changes')
        package = GoodPracticePackage.objects.get(pk=self.package_a.pk)
        execute_transition(
            self.ies_a, package, self._status('bp_resent'))

        from_db = GoodPracticePackage.objects.get(pk=self.package_a.pk)
        self.assertEqual(from_db.status_id, 'bp_resent')
        self.assertEqual(from_db.sent_at, original)
