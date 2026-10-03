"""Comentarios del timeline (task-70): alta, edición y borrado los
gobierna el turno de la RAÍZ; cada lado toca solo los de su lado, sin
importar la autoría."""
from django.urls import reverse

from example.models import GoodPractice, GoodPracticePackage
from flow.models import FlowEvent, Status
from flow.tests.base import FlowSecurityTestCase
from ies.models import User


class CommentEditTests(FlowSecurityTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.reviewer_2 = User.objects.create_user(
            'rev2', password='x', reviewer=True)

    def setUp(self):
        self.practice = GoodPractice.objects.create(
            package=self.package_a, name='P', status_id='bp_for_ruling')
        self.set_package('bp_sent')

    def set_package(self, name):
        GoodPracticePackage.objects.filter(pk=self.package_a.pk).update(
            status_id=name)

    def events_url(self, obj):
        return reverse('flow-events', args=['example', 'goodpractice', obj.pk])

    def event_url(self, obj, event):
        return reverse('flow-event-detail',
                       args=['example', 'goodpractice', obj.pk, event.pk])

    def reviewer_comment(self, text='nota de revisión'):
        return FlowEvent.objects.create(
            target=self.practice, user=self.reviewer, comment=text)

    def test_reviewer_edits_another_reviewers_comment_in_turn(self):
        event = self.reviewer_comment()
        self.client.force_authenticate(self.reviewer_2)
        response = self.client.patch(
            self.event_url(self.practice, event), {'comment': 'corregida'})
        self.assertEqual(response.status_code, 200, response.content)
        event.refresh_from_db()
        self.assertEqual(event.comment, 'corregida')

    def test_ies_cannot_edit_a_reviewer_comment(self):
        event = self.reviewer_comment()
        self.client.force_authenticate(self.ies_a)
        response = self.client.patch(
            self.event_url(self.practice, event), {'comment': 'pisada'})
        self.assertEqual(response.status_code, 403)
        event.refresh_from_db()
        self.assertEqual(event.comment, 'nota de revisión')

    def test_reviewer_loses_edit_and_delete_once_root_returns_to_ies(self):
        event = self.reviewer_comment()
        self.set_package('bp_need_changes')
        self.client.force_authenticate(self.reviewer)
        url = self.event_url(self.practice, event)
        self.assertEqual(
            self.client.patch(url, {'comment': 'tarde'}).status_code, 403)
        self.assertEqual(self.client.delete(url).status_code, 403)
        self.assertTrue(FlowEvent.objects.filter(pk=event.pk).exists())

    def test_delete_pure_comment_removes_the_row(self):
        event = self.reviewer_comment()
        self.client.force_authenticate(self.reviewer)
        response = self.client.delete(self.event_url(self.practice, event))
        self.assertEqual(response.status_code, 204)
        self.assertFalse(FlowEvent.objects.filter(pk=event.pk).exists())

    def test_delete_transition_comment_blanks_text_and_keeps_status(self):
        event = FlowEvent.objects.create(
            target=self.practice, user=self.reviewer,
            from_status_id='bp_completed', to_status_id='bp_for_ruling',
            comment='dictamen')
        self.client.force_authenticate(self.reviewer)
        response = self.client.delete(self.event_url(self.practice, event))
        self.assertEqual(response.status_code, 200, response.content)
        event.refresh_from_db()
        self.assertEqual(event.comment, '')
        self.assertEqual(event.to_status_id, 'bp_for_ruling')


class CommentRoundTests(FlowSecurityTestCase):
    """Editar y borrar valen solo en la ronda en curso: lo escrito antes
    de que la raíz volviera al lado de quien pide ya lo leyó la
    contraparte. Las vueltas se escriben como eventos en el paquete, que
    es lo que lee `round_started_at`."""

    def setUp(self):
        self.practice = GoodPractice.objects.create(
            package=self.package_a, name='P', status_id='bp_for_ruling')

    def move_package(self, user, from_name, to_name, comment=None):
        FlowEvent.objects.create(
            target=self.package_a, user=user, from_status_id=from_name,
            to_status_id=to_name, comment=comment)
        GoodPracticePackage.objects.filter(pk=self.package_a.pk).update(
            status_id=to_name)

    def comment(self, user, text):
        return FlowEvent.objects.create(
            target=self.practice, user=user, comment=text)

    def event_url(self, event):
        return reverse('flow-event-detail', args=[
            'example', 'goodpractice', self.practice.pk, event.pk])

    def test_reviewer_edits_only_the_current_round(self):
        self.move_package(self.ies_a, 'bp_draft', 'bp_sent')
        comment_a = self.comment(self.reviewer, 'A')
        self.move_package(
            self.reviewer, 'bp_sent', 'bp_need_changes', 'corrige')
        self.move_package(self.ies_a, 'bp_need_changes', 'bp_resent')
        comment_b = self.comment(self.reviewer, 'B')
        self.client.force_authenticate(self.reviewer)
        response = self.client.patch(
            self.event_url(comment_a), {'comment': 'A2'})
        self.assertEqual(response.status_code, 403)
        self.assertIn('ronda anterior', response.json()['detail'])
        self.assertEqual(
            self.client.delete(self.event_url(comment_a)).status_code, 403)
        response = self.client.patch(
            self.event_url(comment_b), {'comment': 'B2'})
        self.assertEqual(response.status_code, 200, response.content)

    def test_ies_edits_only_the_current_round(self):
        GoodPracticePackage.objects.filter(pk=self.package_a.pk).update(
            status_id='bp_draft')
        first = self.comment(self.ies_a, 'primera')
        self.move_package(self.ies_a, 'bp_draft', 'bp_sent')
        self.move_package(
            self.reviewer, 'bp_sent', 'bp_need_changes', 'corrige')
        second = self.comment(self.ies_a, 'segunda')
        self.client.force_authenticate(self.ies_a)
        self.assertEqual(self.client.patch(
            self.event_url(first), {'comment': 'x'}).status_code, 403)
        self.assertEqual(self.client.patch(
            self.event_url(second), {'comment': 'y'}).status_code, 200)

    def test_moves_within_the_same_side_do_not_open_a_round(self):
        self.move_package(self.ies_a, 'bp_draft', 'bp_sent')
        comment_a = self.comment(self.reviewer, 'A')
        self.move_package(self.reviewer, 'bp_sent', 'bp_resent')
        self.client.force_authenticate(self.reviewer)
        response = self.client.patch(
            self.event_url(comment_a), {'comment': 'A2'})
        self.assertEqual(response.status_code, 200, response.content)


class CommentRootTurnTests(FlowSecurityTestCase):
    """Regresión: el POST de comentarios sigue el turno de la RAÍZ, no el
    rol del status propio. Una práctica `bp_completed` (rol reviewer) bajo
    un paquete en `bp_draft` todavía no es de la revisión."""

    def setUp(self):
        self.practice = GoodPractice.objects.create(
            package=self.package_a, name='P', status_id='bp_completed')
        self.url = reverse(
            'flow-events', args=['example', 'goodpractice', self.practice.pk])
        self.client.force_authenticate(self.reviewer)

    def set_package(self, name):
        GoodPracticePackage.objects.filter(pk=self.package_a.pk).update(
            status_id=name)

    def test_reviewer_cannot_comment_while_package_is_draft(self):
        self.set_package('bp_draft')
        response = self.client.post(self.url, {'comment': 'pronto'})
        self.assertEqual(response.status_code, 403)

    def test_reviewer_comments_once_package_is_sent(self):
        self.set_package('bp_sent')
        response = self.client.post(self.url, {'comment': 'a tiempo'})
        self.assertEqual(response.status_code, 201, response.content)
