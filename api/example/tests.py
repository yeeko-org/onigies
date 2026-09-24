from example.models import GoodPractice, GoodPracticePackage
from flow.models import Status
from flow.services import validate_transition
from flow.tests.base import FlowSecurityTestCase


class PracticeReviewTurnTests(FlowSecurityTestCase):
    """La revisión no dictamina una práctica mientras el paquete siga
    en turno de la IES (`flow.permissions.root_turn_errors`)."""

    def test_reviewer_waits_for_the_package_to_be_sent(self):
        for_ruling = Status.objects.get(name='bp_for_ruling')
        practice = GoodPractice.objects.create(
            package=self.package_a, name='Práctica X',
            status_id='bp_completed')
        GoodPracticePackage.objects.filter(pk=self.package_a.pk).update(
            status_id='bp_draft')
        practice.refresh_from_db()
        errors = validate_transition(self.reviewer, practice, for_ruling)
        self.assertEqual(
            errors, [GoodPracticePackage.root_not_sent_message])
        GoodPracticePackage.objects.filter(pk=self.package_a.pk).update(
            status_id='bp_sent')
        practice.refresh_from_db()
        self.assertEqual(
            validate_transition(self.reviewer, practice, for_ruling), [])
