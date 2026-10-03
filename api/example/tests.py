from example.models import (
    Feature, FeatureGoodPractice, FeatureOption, GoodPractice,
    GoodPracticePackage)
from flow.models import Status
from flow.services import validate_transition
from flow.tests.base import FlowSecurityTestCase
from ies.models import User


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


class CriterionCommentsLockTests(FlowSecurityTestCase):
    """Candado de `FeatureGoodPractice.comments`, la nota privada de la
    revisión por criterio (task-70): solo la escribe la revisión con el
    paquete en su turno; la IES no la ve y su `''` se descarta."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        Feature.objects.create(name='Criterio 1')

    def setUp(self):
        practice = GoodPractice.objects.create(
            package=self.package_a, name='P', status_id='bp_completed')
        self.criterion = FeatureGoodPractice.objects.get(
            good_practice=practice)
        self.url = f'/api/feature_good_practice/{self.criterion.pk}/'
        self.set_package('bp_sent')

    def set_package(self, name):
        GoodPracticePackage.objects.filter(pk=self.package_a.pk).update(
            status_id=name)

    def set_note(self, text):
        FeatureGoodPractice.objects.filter(pk=self.criterion.pk).update(
            comments=text)

    def test_reviewer_in_turn_changes_the_note(self):
        self.client.force_authenticate(self.reviewer)
        response = self.client.patch(self.url, {'comments': 'nota'})
        self.assertEqual(response.status_code, 200, response.content)
        self.criterion.refresh_from_db()
        self.assertEqual(self.criterion.comments, 'nota')

    def test_reviewer_out_of_turn_cannot_change_the_note(self):
        self.set_note('nota')
        self.set_package('bp_need_changes')
        self.client.force_authenticate(self.reviewer)
        response = self.client.patch(self.url, {'comments': 'otra'})
        self.assertEqual(response.status_code, 403)
        self.criterion.refresh_from_db()
        self.assertEqual(self.criterion.comments, 'nota')

    def test_unchanged_note_passes_out_of_turn(self):
        self.set_note('nota')
        self.set_package('bp_need_changes')
        self.client.force_authenticate(self.reviewer)
        response = self.client.patch(
            self.url, {'comments': 'nota', 'has_attribute': True})
        self.assertEqual(response.status_code, 200, response.content)

    def test_ies_blank_comments_is_dropped_and_its_field_saved(self):
        """Regresión: el formulario de la IES reenvía `comments: ''`."""
        self.set_note('nota')
        self.set_package('bp_need_changes')
        self.client.force_authenticate(self.ies_a)
        response = self.client.patch(
            self.url, {'comments': '', 'justification': 'j'})
        self.assertEqual(response.status_code, 200, response.content)
        self.criterion.refresh_from_db()
        self.assertEqual(self.criterion.comments, 'nota')
        self.assertEqual(self.criterion.justification, 'j')


class GoodPracticeFenceTests(FlowSecurityTestCase):
    """`/api/good_practice/`: la revisión ve todas las prácticas; una IES
    solo las de su institución; sin sesión, nada. Regresión: una IES
    borró en la base de pruebas la práctica de otra institución."""

    def setUp(self):
        self.practice_a = GoodPractice.objects.create(
            package=self.package_a, name='Práctica A')
        self.practice_b = GoodPractice.objects.create(
            package=self.package_b, name='Práctica B')

    def url(self, practice=None):
        base = '/api/good_practice/'
        return f'{base}{practice.pk}/' if practice else base

    def test_anonymous_gets_401(self):
        self.assertEqual(self.client.get(self.url()).status_code, 401)

    def test_other_institution_cannot_read(self):
        self.client.force_authenticate(self.ies_b)
        response = self.client.get(self.url(self.practice_a))
        self.assertEqual(response.status_code, 404)

    def test_other_institution_cannot_delete(self):
        self.client.force_authenticate(self.ies_b)
        response = self.client.delete(self.url(self.practice_a))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(
            GoodPractice.objects.filter(pk=self.practice_a.pk).exists())

    def test_owner_patches_its_practice(self):
        self.client.force_authenticate(self.ies_a)
        response = self.client.patch(
            self.url(self.practice_a), {'name': 'Renombrada'})
        self.assertEqual(response.status_code, 200, response.content)
        self.practice_a.refresh_from_db()
        self.assertEqual(self.practice_a.name, 'Renombrada')

    def test_owner_creates_and_deletes_its_practice(self):
        self.client.force_authenticate(self.ies_a)
        response = self.client.post(
            self.url(), {'package': self.package_a.pk, 'name': 'Nueva'})
        self.assertEqual(response.status_code, 201, response.content)
        response = self.client.delete(
            self.url(GoodPractice.objects.get(pk=response.json()['id'])))
        self.assertEqual(response.status_code, 204)

    def test_cannot_create_in_another_institution_package(self):
        self.client.force_authenticate(self.ies_b)
        response = self.client.post(
            self.url(), {'package': self.package_a.pk, 'name': 'Intrusa'})
        self.assertEqual(response.status_code, 403)
        self.assertFalse(GoodPractice.objects.filter(name='Intrusa').exists())

    def test_cannot_move_own_practice_to_another_package(self):
        self.client.force_authenticate(self.ies_b)
        response = self.client.patch(
            self.url(self.practice_b), {'package': self.package_a.pk})
        self.assertEqual(response.status_code, 403)
        self.practice_b.refresh_from_db()
        self.assertEqual(self.practice_b.package_id, self.package_b.pk)

    def test_ies_list_sees_only_its_own(self):
        self.client.force_authenticate(self.ies_a)
        ids = self.listed_ids()
        self.assertIn(self.practice_a.pk, ids)
        self.assertNotIn(self.practice_b.pk, ids)

    def test_reviewer_list_sees_both(self):
        self.client.force_authenticate(self.reviewer)
        ids = self.listed_ids()
        self.assertIn(self.practice_a.pk, ids)
        self.assertIn(self.practice_b.pk, ids)

    def listed_ids(self):
        response = self.client.get(self.url())
        self.assertEqual(response.status_code, 200, response.content)
        rows = response.json()
        rows = rows if isinstance(rows, list) else rows['results']
        return {row['id'] for row in rows}


class CriterionFieldsTests(FlowSecurityTestCase):
    """`/api/feature_good_practice/`: el criterio no cambia de práctica,
    la IES no escribe la calificación y solo da de alta criterios en sus
    propias prácticas."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.feature = Feature.objects.create(name='Criterio 1')
        cls.option = FeatureOption.objects.create(
            feature=cls.feature, name='Alto', value=3)

    def setUp(self):
        self.practice = GoodPractice.objects.create(
            package=self.package_a, name='P')
        self.other_practice = GoodPractice.objects.create(
            package=self.package_b, name='Q')
        self.criterion = FeatureGoodPractice.objects.get(
            good_practice=self.practice)
        self.url = f'/api/feature_good_practice/{self.criterion.pk}/'

    def test_ies_cannot_rate(self):
        self.client.force_authenticate(self.ies_a)
        response = self.client.patch(
            self.url, {'final_option': self.option.pk, 'justification': 'j'})
        self.assertEqual(response.status_code, 200, response.content)
        self.criterion.refresh_from_db()
        self.assertIsNone(self.criterion.final_option_id)
        self.assertEqual(self.criterion.justification, 'j')

    def test_ies_cannot_move_the_criterion(self):
        self.client.force_authenticate(self.ies_a)
        response = self.client.patch(
            self.url, {'good_practice': self.other_practice.pk})
        self.assertEqual(response.status_code, 200, response.content)
        self.criterion.refresh_from_db()
        self.assertEqual(self.criterion.good_practice_id, self.practice.pk)

    def test_reviewer_rates(self):
        self.client.force_authenticate(self.reviewer)
        response = self.client.patch(
            self.url, {'final_option': self.option.pk})
        self.assertEqual(response.status_code, 200, response.content)
        self.criterion.refresh_from_db()
        self.assertEqual(self.criterion.final_option_id, self.option.pk)

    def create(self, user, practice):
        FeatureGoodPractice.objects.filter(good_practice=practice).delete()
        self.client.force_authenticate(user)
        return self.client.post('/api/feature_good_practice/', {
            'good_practice': practice.pk, 'feature': self.feature.pk})

    def test_ies_creates_a_missing_criterion_on_its_practice(self):
        response = self.create(self.ies_a, self.practice)
        self.assertEqual(response.status_code, 201, response.content)

    def test_ies_cannot_create_on_another_institution_practice(self):
        response = self.create(self.ies_a, self.other_practice)
        self.assertEqual(response.status_code, 403)
        self.assertFalse(FeatureGoodPractice.objects.filter(
            good_practice=self.other_practice).exists())

    def test_reviewer_cannot_create(self):
        response = self.create(self.reviewer, self.practice)
        self.assertEqual(response.status_code, 403)


class PracticeContentTurnTests(FlowSecurityTestCase):
    """El contenido de bp sigue el turno en el servidor, como cp: la IES
    escribe la práctica y sus criterios solo si la práctica es editable
    hoy (`user_can_edit_flow_content`); la revisión queda exenta del
    candado pero solo escribe la calificación, y lo demás se descarta."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        Feature.objects.create(name='Criterio 1')

    def setUp(self):
        self.practice = GoodPractice.objects.create(
            package=self.package_a, name='P', status_id='bp_completed')
        self.criterion = FeatureGoodPractice.objects.get(
            good_practice=self.practice)
        self.practice_url = f'/api/good_practice/{self.practice.pk}/'
        self.criterion_url = (
            f'/api/feature_good_practice/{self.criterion.pk}/')

    def set_package(self, name):
        GoodPracticePackage.objects.filter(pk=self.package_a.pk).update(
            status_id=name)

    def test_ies_cannot_patch_criterion_once_sent(self):
        self.set_package('bp_sent')
        self.client.force_authenticate(self.ies_a)
        response = self.client.patch(
            self.criterion_url, {'justification': 'tarde'})
        self.assertEqual(response.status_code, 403)
        self.criterion.refresh_from_db()
        self.assertIsNone(self.criterion.justification)

    def test_ies_patches_criterion_in_draft(self):
        self.set_package('bp_draft')
        self.client.force_authenticate(self.ies_a)
        response = self.client.patch(
            self.criterion_url, {'justification': 'j'})
        self.assertEqual(response.status_code, 200, response.content)
        self.criterion.refresh_from_db()
        self.assertEqual(self.criterion.justification, 'j')

    def test_ies_cannot_patch_practice_once_sent(self):
        self.set_package('bp_sent')
        self.client.force_authenticate(self.ies_a)
        response = self.client.patch(self.practice_url, {'name': 'Otra'})
        self.assertEqual(response.status_code, 403)
        self.practice.refresh_from_db()
        self.assertEqual(self.practice.name, 'P')

    def test_ies_cannot_delete_practice_once_sent(self):
        self.set_package('bp_sent')
        self.client.force_authenticate(self.ies_a)
        response = self.client.delete(self.practice_url)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(
            GoodPractice.objects.filter(pk=self.practice.pk).exists())

    def test_ies_final_value_is_dropped(self):
        self.client.force_authenticate(self.ies_a)
        response = self.client.patch(self.practice_url, {'final_value': 9})
        self.assertEqual(response.status_code, 200, response.content)
        self.practice.refresh_from_db()
        self.assertIsNone(self.practice.final_value)

    def test_reviewer_scores_practice_once_sent(self):
        self.set_package('bp_sent')
        self.client.force_authenticate(self.reviewer)
        response = self.client.patch(self.practice_url, {'final_value': 9})
        self.assertEqual(response.status_code, 200, response.content)
        self.practice.refresh_from_db()
        self.assertEqual(self.practice.final_value, 9)

    def test_reviewer_content_write_is_dropped(self):
        self.set_package('bp_sent')
        self.client.force_authenticate(self.reviewer)
        response = self.client.patch(self.practice_url, {'name': 'Otra'})
        self.assertEqual(response.status_code, 200, response.content)
        self.practice.refresh_from_db()
        self.assertEqual(self.practice.name, 'P')

    def test_ies_status_write_is_dropped(self):
        # El status solo cambia por el motor de flujo.
        self.set_package('bp_draft')
        self.client.force_authenticate(self.ies_a)
        response = self.client.patch(
            self.practice_url, {'status': 'bp_for_ruling'})
        self.assertEqual(response.status_code, 200, response.content)
        self.practice.refresh_from_db()
        self.assertEqual(self.practice.status_id, 'bp_completed')

    def assert_reviewer_cannot_delete(self, url, model, pk):
        self.set_package('bp_sent')
        self.client.force_authenticate(self.reviewer)
        for path in (url, f'{url}confirm-delete/'):
            response = self.client.delete(path)
            self.assertEqual(response.status_code, 403, path)
        self.assertTrue(model.objects.filter(pk=pk).exists())

    def test_reviewer_cannot_delete_practice(self):
        self.assert_reviewer_cannot_delete(
            self.practice_url, GoodPractice, self.practice.pk)

    def test_reviewer_cannot_delete_criterion(self):
        self.assert_reviewer_cannot_delete(
            self.criterion_url, FeatureGoodPractice, self.criterion.pk)


class AdminBpExemptionTests(FlowSecurityTestCase):
    """El admin (`is_admin`) queda fuera de las tres reglas de bp de la
    revisión: crea y borra prácticas y criterios, y su contenido no se
    descarta ni topa con el candado de turno. Todo con el envío ya
    enviado, fuera del turno de la IES."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        Feature.objects.create(name='Criterio 1')
        cls.admin = User.objects.create_user(
            'adm', password='x', is_staff=True)

    def setUp(self):
        GoodPracticePackage.objects.filter(pk=self.package_a.pk).update(
            status_id='bp_sent')
        self.practice = GoodPractice.objects.create(
            package=self.package_a, name='P', status_id='bp_completed')
        self.criterion = FeatureGoodPractice.objects.get(
            good_practice=self.practice)
        self.practice_url = f'/api/good_practice/{self.practice.pk}/'
        self.criterion_url = (
            f'/api/feature_good_practice/{self.criterion.pk}/')
        self.client.force_authenticate(self.admin)

    def test_admin_creates_a_practice(self):
        response = self.client.post('/api/good_practice/', {
            'package': self.package_a.pk, 'name': 'Del admin'})
        self.assertEqual(response.status_code, 201, response.content)

    def test_admin_deletes_a_practice(self):
        response = self.client.delete(self.practice_url)
        self.assertEqual(response.status_code, 204, response.content)
        self.assertFalse(
            GoodPractice.objects.filter(pk=self.practice.pk).exists())

    def test_admin_deletes_a_criterion(self):
        response = self.client.delete(self.criterion_url)
        self.assertEqual(response.status_code, 204, response.content)
        self.assertFalse(
            FeatureGoodPractice.objects.filter(pk=self.criterion.pk).exists())

    def test_admin_patches_content_once_sent(self):
        response = self.client.patch(self.practice_url, {'name': 'Otra'})
        self.assertEqual(response.status_code, 200, response.content)
        self.practice.refresh_from_db()
        self.assertEqual(self.practice.name, 'Otra')

    def test_admin_scores_the_practice(self):
        response = self.client.patch(self.practice_url, {'final_value': 9})
        self.assertEqual(response.status_code, 200, response.content)
        self.practice.refresh_from_db()
        self.assertEqual(self.practice.final_value, 9)
