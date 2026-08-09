"""
Pertenencia institucional (B1-B3): una IES ajena no puede transicionar,
comentar, ver el timeline ni descartar objetos de otra institución; la
IES dueña y las revisoras sí.
"""
from django.urls import reverse
from rest_framework import status

from .base import FlowSecurityTestCase


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
