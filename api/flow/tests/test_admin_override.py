"""Válvula de admin (adr-0023): `POST .../admin-transitions/` lleva un
hijo a un destino de la revisión fuera de `next_statuses`, solo con la
raíz del lado de la revisión, con comentario y respetando la regla de
hijos."""
from django.urls import reverse

from answer.models import ObservableResponse
from answer.tests import CpCatalogTestCase, force
from example.models import GoodPractice, GoodPracticePackage
from flow.models import FlowEvent
from flow.services import admin_target_names, is_admin_event
from flow.tests.base import FlowSecurityTestCase
from ies.models import User


def admin_url(app_label, model_name, pk):
    return reverse('flow-admin-transitions',
                   args=[app_label, model_name, pk])


class AdminOverrideTests(FlowSecurityTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.admin = User.objects.create_user(
            'adm', password='x', is_staff=True)

    def setUp(self):
        self.practice = GoodPractice.objects.create(
            package=self.package_a, name='P', status_id='bp_for_ruling')
        self.set_package('bp_sent')
        self.url = admin_url('example', 'goodpractice', self.practice.pk)

    def set_package(self, name):
        GoodPracticePackage.objects.filter(pk=self.package_a.pk).update(
            status_id=name)

    def post(self, user, url=None, **payload):
        self.client.force_authenticate(user)
        return self.client.post(url or self.url, payload)

    def test_reviewer_without_admin_is_forbidden(self):
        response = self.post(
            self.reviewer, target_status='bp_need_changes', comment='z')
        self.assertEqual(response.status_code, 403)
        self.practice.refresh_from_db()
        self.assertEqual(self.practice.status_id, 'bp_for_ruling')

    def test_admin_moves_terminal_practice_back_to_need_changes(self):
        response = self.post(
            self.admin, target_status='bp_need_changes', comment='error')
        self.assertEqual(response.status_code, 201, response.content)
        self.practice.refresh_from_db()
        self.assertEqual(self.practice.status_id, 'bp_need_changes')
        event = FlowEvent.objects.get(pk=response.json()['id'])
        self.assertEqual(event.comment, 'error')
        self.assertEqual(event.from_status_id, 'bp_for_ruling')
        self.assertEqual(event.to_status_id, 'bp_need_changes')

    def test_rejects_the_root(self):
        url = admin_url('example', 'goodpracticepackage', self.package_a.pk)
        response = self.post(
            self.admin, url, target_status='bp_need_changes', comment='z')
        self.assertEqual(response.status_code, 400)
        self.assertIn('nunca al envío mismo', response.json()['detail'])

    def test_rejects_while_root_is_in_ies_turn(self):
        self.set_package('bp_need_changes')
        response = self.post(
            self.admin, target_status='bp_rejected', comment='z')
        self.assertEqual(response.status_code, 400)
        self.assertIn('del lado de la revisión', response.json()['detail'])

    def test_rejects_ies_only_target(self):
        response = self.post(self.admin, target_status='bp_draft', comment='z')
        self.assertEqual(response.status_code, 400)
        self.assertIn('no es un destino válido', response.json()['detail'])

    def test_rejects_a_legal_target(self):
        GoodPractice.objects.filter(pk=self.practice.pk).update(
            status_id='bp_completed')
        response = self.post(
            self.admin, target_status='bp_rejected', comment='z')
        self.assertEqual(response.status_code, 400)
        self.assertIn('transición normal', response.json()['detail'])
        self.practice.refresh_from_db()
        self.assertEqual(self.practice.status_id, 'bp_completed')

    def test_requires_a_comment(self):
        response = self.post(self.admin, target_status='bp_need_changes')
        self.assertEqual(response.status_code, 400)
        self.assertIn('comment', response.json())
        self.practice.refresh_from_db()
        self.assertEqual(self.practice.status_id, 'bp_for_ruling')

    def test_normal_transitions_endpoint_still_rejects_off_graph(self):
        url = reverse('flow-transitions',
                      args=['example', 'goodpractice', self.practice.pk])
        response = self.post(
            self.admin, url, target_status='bp_rejected', comment='z')
        self.assertEqual(response.status_code, 400)
        self.practice.refresh_from_db()
        self.assertEqual(self.practice.status_id, 'bp_for_ruling')

    def test_admin_reason_is_not_deletable_and_only_admin_edits_it(self):
        response = self.post(
            self.admin, target_status='bp_need_changes', comment='error')
        event = FlowEvent.objects.get(pk=response.json()['id'])
        self.assertTrue(is_admin_event(event))
        url = reverse('flow-event-detail',
                      args=['example', 'goodpractice', self.practice.pk,
                            event.pk])
        self.client.force_authenticate(self.reviewer)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)
        self.assertIn('no se borra', response.json()['detail'])
        event.refresh_from_db()
        self.assertEqual(event.comment, 'error')
        response = self.client.patch(url, {'comment': 'pisado'})
        self.assertEqual(response.status_code, 403)
        self.assertIn('administración', response.json()['detail'])
        event.refresh_from_db()
        self.assertEqual(event.comment, 'error')
        self.client.force_authenticate(self.admin)
        response = self.client.patch(url, {'comment': 'corregido'})
        self.assertEqual(response.status_code, 200, response.content)
        event.refresh_from_db()
        self.assertEqual(event.comment, 'corregido')

    def test_on_graph_transition_comment_is_not_an_admin_event(self):
        event = FlowEvent.objects.create(
            target=self.practice, user=self.reviewer,
            from_status_id='bp_completed', to_status_id='bp_for_ruling',
            comment='dictamen')
        self.assertFalse(is_admin_event(event))


class AdminTargetCatalogTests(FlowSecurityTestCase):

    def test_gen_targets_are_derived_from_the_graph(self):
        self.assertEqual(set(admin_target_names('gen')), {
            'gen_completed', 'gen_sent', 'gen_adjusted', 'gen_resent',
            'gen_need_changes', 'gen_approved', 'gen_finished'})

    def test_status_rows_carry_their_group_admin_targets(self):
        self.client.force_authenticate(self.reviewer)
        response = self.client.get(reverse('flow-status-list'))
        self.assertEqual(response.status_code, 200)
        rows = response.json()
        rows = rows if isinstance(rows, list) else rows['results']
        by_group = {}
        for row in rows:
            by_group.setdefault(row['group'], []).append(row)
        for group, group_rows in by_group.items():
            expected = admin_target_names(group)
            for row in group_rows:
                self.assertEqual(row['admin_targets'], expected, row['name'])


class AdminOverrideChildrenRuleTests(CpCatalogTestCase):
    """La válvula salta `next_statuses` pero no la regla de hijos: un
    observable no se aprueba con un grupo aún en captura. Desde
    `cp_partial`, porque `cp_approved` no es uno de sus siguientes."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.admin = User.objects.create_user(
            'adm', password='x', is_staff=True)

    def test_children_rule_still_applies(self):
        force(self.axis_value, 'cp_sent')
        ObservableResponse.objects.filter(pk=self.obs_response.pk).update(
            value=True, status_id='cp_partial')
        force(self.group_a, 'cp_filling')
        force(self.group_b, 'cp_approved')
        force(self.group_reach, 'cp_approved')
        url = admin_url(
            'answer', 'observableresponse', self.obs_response.pk)
        self.client.force_authenticate(self.admin)
        payload = {'target_status': 'cp_approved', 'comment': 'z'}

        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 400, response.content)
        self.assertIn('elemento(s)', str(response.json()['detail']))

        force(self.group_a, 'cp_approved')
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 201, response.content)
