"""
Tests de seguridad y cableado del motor de flujo.

Cubren:
- Pertenencia institucional (B1-B3): una IES ajena no puede
  transicionar, comentar, ver el timeline ni descartar objetos de otra
  institución; la IES dueña y las revisoras sí.
- Cableado del status inicial (B4): todo participante creado sin status
  recibe el default de su grupo; `assign_auto_status` promueve al status
  `auto_on_first_save` en la primera captura.
"""
from datetime import timedelta
from unittest.mock import patch

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from example.models import GoodPractice, GoodPracticePackage
from flow.models import FlowEvent, Status
from flow.notifications import _should_notify
from flow.seed import seed_flow
from flow.services import assign_auto_status, execute_transition
from ies.initial_data import InitStatus
from ies.models import Institution, Period, User
from indicator.models import Axis
from survey.models import AxisValue


class FlowSecurityTestCase(APITestCase):
    """Base: siembra el catálogo y crea dos IES con sus paquetes."""

    @classmethod
    def setUpTestData(cls):
        # Institution.save fija status_sending/status_register del flujo
        # viejo (StatusControl), que coexiste con flow.Status.
        InitStatus()
        seed_flow()
        cls.period = Period.objects.create(year=2025)

        cls.inst_a = Institution.objects.create(name='IES A', acronym='IESA')
        cls.inst_b = Institution.objects.create(name='IES B', acronym='IESB')

        cls.survey_a = cls.inst_a.surveys.get(period=cls.period)
        cls.survey_b = cls.inst_b.surveys.get(period=cls.period)
        cls.package_a = cls.survey_a.packages.first()
        cls.package_b = cls.survey_b.packages.first()

        cls.ies_a = User.objects.create_user(
            'iesa', password='x', institution=cls.inst_a)
        cls.ies_b = User.objects.create_user(
            'iesb', password='x', institution=cls.inst_b)
        cls.reviewer = User.objects.create_user(
            'rev', password='x', reviewer=True)

    def _transitions_url(self, obj):
        return reverse(
            'flow-transitions',
            args=['example', 'goodpracticepackage', obj.pk])

    def _events_url(self, obj):
        return reverse(
            'flow-events', args=['example', 'goodpracticepackage', obj.pk])


class TransitionOwnershipTests(FlowSecurityTestCase):

    def test_ies_ajena_no_transiciona(self):
        self.client.force_authenticate(self.ies_b)
        resp = self.client.post(
            self._transitions_url(self.package_a),
            {'target_status': 'bp_sent'})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_ies_propia_transiciona(self):
        self.client.force_authenticate(self.ies_a)
        resp = self.client.post(
            self._transitions_url(self.package_a),
            {'target_status': 'bp_sent'})
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.package_a.refresh_from_db()
        self.assertEqual(self.package_a.status_id, 'bp_sent')

    def test_reviewer_transiciona_objeto_de_otra_ies(self):
        # La revisora no pertenece a ninguna IES pero puede actuar sobre
        # cualquier objeto: se le pone el turno (bp_sent, role reviewer).
        self.package_b.status_id = 'bp_sent'
        self.package_b.save(update_fields=['status'])
        self.client.force_authenticate(self.reviewer)
        resp = self.client.post(
            self._transitions_url(self.package_b),
            {'target_status': 'bp_finished'})
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)


class EventOwnershipTests(FlowSecurityTestCase):

    def test_ies_ajena_no_comenta(self):
        self.client.force_authenticate(self.ies_b)
        resp = self.client.post(
            self._events_url(self.package_a), {'comment': 'hola'})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_ies_propia_comenta(self):
        self.client.force_authenticate(self.ies_a)
        resp = self.client.post(
            self._events_url(self.package_a), {'comment': 'hola'})
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_ies_ajena_no_ve_timeline(self):
        self.client.force_authenticate(self.ies_b)
        resp = self.client.get(self._events_url(self.package_a))
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_ies_propia_ve_timeline(self):
        self.client.force_authenticate(self.ies_a)
        resp = self.client.get(self._events_url(self.package_a))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)


class PackageActionOwnershipTests(FlowSecurityTestCase):

    def test_ies_ajena_no_descarta(self):
        # El paquete queda fuera del get_queryset de la IES ajena, así que
        # get_object devuelve 404 (no revela existencia).
        self.client.force_authenticate(self.ies_b)
        url = reverse(
            'good_practice_package-discard', args=[self.package_a.pk])
        resp = self.client.post(url)
        self.assertIn(
            resp.status_code,
            (status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND))

    def test_ies_propia_descarta(self):
        self.client.force_authenticate(self.ies_a)
        url = reverse(
            'good_practice_package-discard', args=[self.package_a.pk])
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.package_a.refresh_from_db()
        self.assertEqual(self.package_a.status_id, 'bp_discarded')

    def test_list_solo_muestra_paquetes_propios(self):
        self.client.force_authenticate(self.ies_a)
        url = reverse('good_practice_package-list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        ids = {row['id'] for row in resp.data['results']}
        self.assertIn(self.package_a.pk, ids)
        self.assertNotIn(self.package_b.pk, ids)


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


class TestInstitutionPeriodLockTests(APITestCase):
    """
    `Institution.is_test` levanta el candado de cierre de periodo en los
    dos ganchos de flujo (bp y gen) y en los guards de vista de bp.

    No hereda de FlowSecurityTestCase porque necesita un periodo YA
    CERRADO al momento de crear las instituciones: `Institution.save`
    aprovisiona los surveys sobre los periodos existentes, así que el
    orden importa.
    """

    @classmethod
    def setUpTestData(cls):
        InitStatus()
        seed_flow()
        # Un día antes de hoy: el día límite todavía cuenta como abierto.
        yesterday = timezone.localdate() - timedelta(days=1)
        cls.period = Period.objects.create(
            year=2027, submission_deadline=yesterday,
            gen_submission_deadline=yesterday)

        cls.inst_real = Institution.objects.create(
            name='IES Real', acronym='REAL')
        cls.inst_test = Institution.objects.create(
            name='IES de prueba', acronym='TEST', is_test=True)

        cls.user_real = User.objects.create_user(
            'real', password='x', institution=cls.inst_real)
        cls.user_test = User.objects.create_user(
            'test', password='x', institution=cls.inst_test)
        cls.reviewer = User.objects.create_user(
            'rev', password='x', reviewer=True)

        cls.survey_real = cls.inst_real.surveys.get(period=cls.period)
        cls.survey_test = cls.inst_test.surveys.get(period=cls.period)

    def _status(self, name: str) -> Status:
        return Status.objects.get(name=name)

    def test_periodo_de_la_prueba_esta_cerrado(self):
        # Sostén de los demás: si el periodo dejara de estar cerrado, todo
        # lo que sigue pasaría por la razón equivocada.
        self.assertTrue(self.period.is_bp_submission_closed)
        self.assertTrue(self.period.is_gen_submission_closed)

    # --- gancho bp: GoodPracticePackage.validate_flow_transition ---

    def test_bp_ies_real_no_envia_con_periodo_cerrado(self):
        package = self.survey_real.packages.first()
        with self.assertRaises(ValueError) as ctx:
            execute_transition(
                self.user_real, package, self._status('bp_sent'))
        self.assertIn('ya cerró', ' '.join(ctx.exception.args[0]))
        package.refresh_from_db()
        self.assertEqual(package.status_id, 'bp_draft')

    def test_bp_ies_de_prueba_envia_con_periodo_cerrado(self):
        package = self.survey_test.packages.first()
        execute_transition(
            self.user_test, package, self._status('bp_sent'))
        package.refresh_from_db()
        self.assertEqual(package.status_id, 'bp_sent')

    # --- gancho gen: GeneralPackage.validate_flow_transition ---

    def test_gen_ies_real_no_envia_con_periodo_cerrado(self):
        package = self.survey_real.general_package
        with self.assertRaises(ValueError) as ctx:
            execute_transition(
                self.user_real, package, self._status('gen_sent'))
        self.assertIn('ya cerró', ' '.join(ctx.exception.args[0]))
        package.refresh_from_db()
        self.assertEqual(package.status_id, 'gen_draft')

    def test_gen_ies_de_prueba_envia_con_periodo_cerrado(self):
        package = self.survey_test.general_package
        execute_transition(
            self.user_test, package, self._status('gen_sent'))
        package.refresh_from_db()
        self.assertEqual(package.status_id, 'gen_sent')

    # --- la revisora dictamina después del cierre (ambos ganchos) ---
    # El cierre solo detiene a la IES: la revisión ocurre por definición
    # después de la fecha límite. Se usa una institución REAL para que el
    # escape que se ejercita sea `is_reviewer` y no `is_test`.

    def test_bp_revisora_dictamina_con_periodo_cerrado(self):
        package = self.survey_real.packages.first()
        package.status_id = 'bp_sent'
        package.save(update_fields=['status'])

        execute_transition(
            self.reviewer, package, self._status('bp_finished'))
        package.refresh_from_db()
        self.assertEqual(package.status_id, 'bp_finished')

    def test_gen_revisora_dictamina_con_periodo_cerrado(self):
        package = self.survey_real.general_package
        package.status_id = 'gen_sent'
        package.save(update_fields=['status'])

        execute_transition(
            self.reviewer, package, self._status('gen_finished'))
        package.refresh_from_db()
        self.assertEqual(package.status_id, 'gen_finished')

    # --- guards de vista de bp (discard / reopen) ---

    def test_discard_ies_real_bloqueado_con_periodo_cerrado(self):
        package = self.survey_real.packages.first()
        self.client.force_authenticate(self.user_real)
        url = reverse('good_practice_package-discard', args=[package.pk])
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('ya cerró', resp.data['detail'])

    def test_discard_ies_de_prueba_permitido_con_periodo_cerrado(self):
        package = self.survey_test.packages.first()
        self.client.force_authenticate(self.user_test)
        url = reverse('good_practice_package-discard', args=[package.pk])
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        package.refresh_from_db()
        self.assertEqual(package.status_id, 'bp_discarded')

    def test_reopen_ies_real_bloqueado_con_periodo_cerrado(self):
        package = self.survey_real.packages.first()
        self.client.force_authenticate(self.user_real)
        url = reverse('good_practice_package-reopen', args=[package.pk])
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('ya cerró', resp.data['detail'])

    def test_reopen_ies_de_prueba_permitido_con_periodo_cerrado(self):
        package = self.survey_test.packages.first()
        self.client.force_authenticate(self.user_test)
        url = reverse('good_practice_package-reopen', args=[package.pk])
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)


class TurnNotificationTests(FlowSecurityTestCase):
    """
    S5: correo a la IES cuando el turno de un objeto RAÍZ vuelve a ella
    o el objeto llega a un status final. Nunca a revisoras, nunca por
    transiciones de hijo ni por propagación.
    """

    def setUp(self):
        # inst_a: dos usuarios activos con correo y uno inactivo.
        self.ies_a.email = 'a1@ies.mx'
        self.ies_a.save(update_fields=['email'])
        self.ies_a2 = User.objects.create_user(
            'iesa2', password='x', institution=self.inst_a,
            email='a2@ies.mx')
        User.objects.create_user(
            'iesaoff', password='x', institution=self.inst_a,
            email='off@ies.mx', is_active=False)

    def _st(self, name):
        return Status.objects.get(name=name)

    # --- predicado _should_notify (sin correo) ---

    def test_predicado_turno_vuelve_a_ies(self):
        self.assertTrue(_should_notify(
            self.package_a, self._st('bp_sent'),
            self._st('bp_need_changes')))

    def test_predicado_terminal(self):
        self.assertTrue(_should_notify(
            self.package_a, self._st('bp_sent'),
            self._st('bp_finished')))

    def test_predicado_no_turno_a_revisora(self):
        self.assertFalse(_should_notify(
            self.package_a, self._st('bp_draft'),
            self._st('bp_sent')))

    def test_predicado_no_reabrir_ies_a_ies(self):
        self.assertFalse(_should_notify(
            self.package_a, self._st('bp_discarded'),
            self._st('bp_draft')))

    def test_predicado_no_notifica_hijo(self):
        practice = GoodPractice.objects.create(
            package=self.package_a, name='Práctica X')
        self.assertFalse(_should_notify(
            practice, self._st('bp_completed'),
            self._st('bp_need_changes')))

    # --- integración (envío programado con on_commit) ---

    @patch('flow.notifications.send_simple_email')
    def test_need_changes_notifica_a_ies_activa(self, mock_send):
        self.package_a.status_id = 'bp_sent'
        self.package_a.save(update_fields=['status'])
        self.client.force_authenticate(self.reviewer)
        with self.captureOnCommitCallbacks(execute=True):
            resp = self.client.post(
                self._transitions_url(self.package_a),
                {'target_status': 'bp_need_changes',
                 'comment': 'Corrige la sección de resultados.'})
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        sent_to = {c.args[0] for c in mock_send.call_args_list}
        self.assertEqual(sent_to, {'a1@ies.mx', 'a2@ies.mx'})
        # el comentario de la revisión viaja en el cuerpo
        html = mock_send.call_args_list[0].args[2]
        self.assertIn('Corrige la sección de resultados.', html)

    @patch('flow.notifications.send_simple_email')
    def test_terminal_notifica_a_ies(self, mock_send):
        self.package_a.status_id = 'bp_sent'
        self.package_a.save(update_fields=['status'])
        self.client.force_authenticate(self.reviewer)
        with self.captureOnCommitCallbacks(execute=True):
            resp = self.client.post(
                self._transitions_url(self.package_a),
                {'target_status': 'bp_finished'})
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        sent_to = {c.args[0] for c in mock_send.call_args_list}
        self.assertEqual(sent_to, {'a1@ies.mx', 'a2@ies.mx'})

    @patch('flow.notifications.send_simple_email')
    def test_envio_a_revision_no_notifica(self, mock_send):
        self.client.force_authenticate(self.ies_a)
        with self.captureOnCommitCallbacks(execute=True):
            resp = self.client.post(
                self._transitions_url(self.package_a),
                {'target_status': 'bp_sent'})
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        mock_send.assert_not_called()

    @patch('flow.notifications.send_simple_email')
    def test_transicion_de_hijo_no_notifica(self, mock_send):
        practice = GoodPractice.objects.create(
            package=self.package_a, name='Práctica X')
        practice.status_id = 'bp_completed'
        practice.save(update_fields=['status'])
        self.client.force_authenticate(self.reviewer)
        with self.captureOnCommitCallbacks(execute=True):
            resp = self.client.post(
                reverse('flow-transitions',
                        args=['example', 'goodpractice', practice.pk]),
                {'target_status': 'bp_need_changes',
                 'comment': 'Ajusta esto.'})
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        mock_send.assert_not_called()