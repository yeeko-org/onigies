"""Sonda de la compuerta de edición del cuestionario (task-131).

No entra en la suite (el nombre no casa con `python_files`); se corre a
mano desde la raíz del monorepo:

    api/venv/bin/pytest -c api/pytest.ini api/.claude/smoke_content_gate.py -q

Ejercita, contra los endpoints reales, lo que la suite todavía no cubre:
alta y baja de preguntas y de filas puente con el cuestionario abierto,
el 403 con el cuestionario cerrado, el `order` automático, la fila
puente que se crea sola y las banderas de ponderación del observable.
"""
from decimal import Decimal

from rest_framework.test import APITestCase

from ies.models import User
from indicator.models import Axis, Component, Observable
from question.models import (
    AQuestion, BQuestion, ObservableQuestionType, QuestionType,
    QuestionnaireSettings, ReachQuestion)


class ContentGateSmoke(APITestCase):

    @classmethod
    def setUpTestData(cls):
        axis = Axis.objects.create(order=1, name="Eje", color="teal")
        component = Component.objects.create(axis=axis, name="Componente")
        cls.observable = Observable.objects.create(
            component=component, number="1.1", name="Observable")
        cls.other = Observable.objects.create(
            component=component, number="1.2", name="Otro observable")
        # `model_question` no es decorativo: de ahí deduce el serializer
        # a qué tipo pertenece la pregunta que se acaba de crear.
        for order, (name, weight, model_question) in enumerate([
                ('a_questions', Decimal('5.00'), 'AQuestion'),
                ('reach', Decimal('2.50'), 'ReachQuestion'),
                ('b_questions', Decimal('2.50'), 'BQuestion'),
                ('plans', None, 'PlanQuestion')], start=1):
            QuestionType.objects.create(
                name=name, public_name=name, default_weight=weight,
                model_question=model_question, order=order,
                required=name in ('a_questions', 'b_questions'))
        AQuestion.objects.create(
            observable=cls.observable, order=1, text="Opción sembrada")
        cls.user = User.objects.create_user(
            username="revisora", email="revisora@onigies.mx",
            password="x", reviewer=True)

    def setUp(self):
        self.client.force_authenticate(self.user)
        QuestionnaireSettings.objects.update_or_create(
            pk=1, defaults={"content_open": True})

    def _close(self):
        QuestionnaireSettings.objects.update_or_create(
            pk=1, defaults={"content_open": False})

    # --- abierto -----------------------------------------------------
    def test_open_create_a_question_assigns_order_and_bridge(self):
        response = self.client.post('/api/catalogs/a_question/', {
            "observable": self.observable.pk, "text": "Opción nueva"})
        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(response.data["order"], 2)
        self.assertTrue(ObservableQuestionType.objects.filter(
            observable=self.observable,
            question_type_id='a_questions').exists())

    def test_open_create_b_question_flags(self):
        response = self.client.post('/api/catalogs/b_question/', {
            "observable": self.observable.pk, "text": "Instancias",
            "includes_academic": True, "includes_admin": False})
        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(response.data["order"], 1)
        self.assertFalse(response.data["includes_admin"])

    def test_open_patch_b_flags(self):
        b_question = BQuestion.objects.create(
            observable=self.observable, order=1, text="B",
            includes_academic=True, includes_admin=True)
        response = self.client.patch(
            f'/api/catalogs/b_question/{b_question.pk}/',
            {"includes_admin": False})
        self.assertEqual(response.status_code, 200, response.data)
        b_question.refresh_from_db()
        self.assertFalse(b_question.includes_admin)

    def test_open_patch_reach_flags(self):
        reach = ReachQuestion.objects.create(
            observable=self.observable, text="Alcance",
            has_main_sectors=True)
        response = self.client.patch(
            f'/api/catalogs/reach_question/{reach.pk}/',
            {"has_main_sectors": False, "has_general_planning": True})
        self.assertEqual(response.status_code, 200, response.data)
        reach.refresh_from_db()
        self.assertFalse(reach.has_main_sectors)
        self.assertTrue(reach.has_general_planning)

    def test_open_observable_is_not_editable_on_update(self):
        question = AQuestion.objects.get(observable=self.observable, order=1)
        response = self.client.patch(
            f'/api/catalogs/a_question/{question.pk}/',
            {"observable": self.other.pk})
        self.assertEqual(response.status_code, 200, response.data)
        question.refresh_from_db()
        self.assertEqual(question.observable_id, self.observable.pk)

    def test_open_delete_question(self):
        question = AQuestion.objects.get(observable=self.observable, order=1)
        response = self.client.delete(
            f'/api/catalogs/a_question/{question.pk}/')
        self.assertEqual(response.status_code, 204, response.data)

    def test_open_bridge_create_and_delete(self):
        response = self.client.post(
            '/api/catalogs/observable_question_type/', {
                "observable": self.observable.pk,
                "question_type": "plans", "weight": "3.50"})
        self.assertEqual(response.status_code, 201, response.data)
        row_id = response.data["id"]
        duplicate = self.client.post(
            '/api/catalogs/observable_question_type/', {
                "observable": self.observable.pk, "question_type": "plans"})
        self.assertEqual(duplicate.status_code, 400, duplicate.data)
        deleted = self.client.delete(
            f'/api/catalogs/observable_question_type/{row_id}/')
        self.assertEqual(deleted.status_code, 204, deleted.data)

    # --- cerrado -----------------------------------------------------
    def test_closed_blocks_create_and_delete(self):
        self._close()
        created = self.client.post('/api/catalogs/a_question/', {
            "observable": self.observable.pk, "text": "No debe entrar"})
        self.assertEqual(created.status_code, 403, created.data)
        question = AQuestion.objects.get(observable=self.observable, order=1)
        deleted = self.client.delete(
            f'/api/catalogs/a_question/{question.pk}/')
        self.assertEqual(deleted.status_code, 403, deleted.data)

    def test_closed_keeps_text_and_weight_editable(self):
        self._close()
        question = AQuestion.objects.get(observable=self.observable, order=1)
        response = self.client.patch(
            f'/api/catalogs/a_question/{question.pk}/',
            {"text": "Texto editado"})
        self.assertEqual(response.status_code, 200, response.data)
        row = ObservableQuestionType.objects.create(
            observable=self.observable, question_type_id='a_questions')
        weighted = self.client.patch(
            f'/api/catalogs/observable_question_type/{row.pk}/',
            {"weight": "7.00"})
        self.assertEqual(weighted.status_code, 200, weighted.data)

    def test_closed_freezes_b_flags(self):
        self._close()
        b_question = BQuestion.objects.create(
            observable=self.observable, order=1, text="B",
            includes_admin=True)
        response = self.client.patch(
            f'/api/catalogs/b_question/{b_question.pk}/',
            {"includes_admin": False})
        self.assertEqual(response.status_code, 200, response.data)
        b_question.refresh_from_db()
        self.assertTrue(b_question.includes_admin)

    # --- banderas de ponderación y ajustes ---------------------------
    def test_weight_flags_on_observable_detail(self):
        for name in ('a_questions', 'b_questions', 'reach'):
            ObservableQuestionType.objects.create(
                observable=self.observable, question_type_id=name)
        ObservableQuestionType.objects.create(
            observable=self.other, question_type_id='a_questions')
        standard = self.client.get(
            f'/api/catalogs/observable/{self.observable.pk}/')
        self.assertTrue(standard.data["uses_default_weights"])
        self.assertFalse(standard.data["weights_pending"])
        custom = self.client.get(
            f'/api/catalogs/observable/{self.other.pk}/')
        self.assertFalse(custom.data["uses_default_weights"])
        self.assertTrue(custom.data["weights_pending"])

    def test_settings_row_payload_and_toggle(self):
        listed = self.client.get('/api/catalogs/questionnaire_settings/')
        self.assertEqual(listed.status_code, 200, listed.data)
        row = listed.data["results"][0]
        self.assertEqual(
            set(row), {"id", "title", "content_open", "seeded_at"})
        toggled = self.client.patch(
            f'/api/catalogs/questionnaire_settings/{row["id"]}/',
            {"content_open": False})
        self.assertEqual(toggled.status_code, 200, toggled.data)
        self.assertFalse(QuestionnaireSettings.is_open())
        blocked = self.client.post(
            '/api/catalogs/questionnaire_settings/', {"content_open": True})
        self.assertEqual(blocked.status_code, 405, blocked.data)
        undeletable = self.client.delete(
            f'/api/catalogs/questionnaire_settings/{row["id"]}/')
        self.assertEqual(undeletable.status_code, 405, undeletable.data)

    def test_closing_is_one_way(self):
        row = QuestionnaireSettings.load()
        url = f'/api/catalogs/questionnaire_settings/{row.pk}/'
        closed = self.client.patch(url, {"content_open": False})
        self.assertEqual(closed.status_code, 200, closed.data)
        reopened = self.client.patch(url, {"content_open": True})
        self.assertEqual(reopened.status_code, 400, reopened.data)
        self.assertIn("content_open", reopened.data)
        self.assertFalse(QuestionnaireSettings.is_open())
