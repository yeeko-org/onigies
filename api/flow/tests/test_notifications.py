"""
S5: correo a la IES cuando el turno de un objeto RAÍZ vuelve a ella o el
objeto llega a un status final. Nunca a revisoras, nunca por
transiciones de hijo ni por propagación.
"""
from unittest.mock import patch

from django.urls import reverse
from rest_framework import status

from example.models import GoodPractice
from flow.models import Status
from flow.notifications import _should_notify
from ies.models import User

from .base import FlowSecurityTestCase


class TurnNotificationTests(FlowSecurityTestCase):

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
