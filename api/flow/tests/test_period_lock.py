"""
`Institution.is_test` levanta el candado de cierre de periodo en los dos
ganchos de flujo (bp y gen) y en los guards de vista de bp.
"""
from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from flow.models import Status
from flow.seed import seed_flow
from flow.services import execute_transition
from ies.initial_data import InitStatus
from ies.models import Institution, Period, User


class TestInstitutionPeriodLockTests(APITestCase):
    """
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
