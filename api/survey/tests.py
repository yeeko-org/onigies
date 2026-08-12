"""Respuestas a preguntas generales: dónde aterriza el valor.

Cubre las tres piezas que quedaron atadas a `GeneralQuestionResponse`
cuando los valores escalares salieron de las columnas del Survey
(task-117): la compuerta de contenido, el upsert del serializer y la
precarga de la forma de gobierno.
"""
from django.test import TestCase

from api.views.survey.serializers import SurveySerializer
from flow.seed import seed_flow
from ies.initial_data import InitStatus
from ies.models import Institution, Period
from indicator.models import GeneralGroup
from question.models import GeneralQuestion
from survey.general_validation import (
    _answered_value, group_completion_issues)
from survey.models import GeneralQuestionResponse


class GeneralQuestionTestCase(TestCase):
    """Base: catálogo mínimo de preguntas generales y una IES.

    Los grupos y preguntas se construyen a mano en vez de correr
    `load_questionnaire`: lo que se prueba es el comportamiento por
    `addl_config` y `q_type`, no la redacción sembrada.
    """

    @classmethod
    def setUpTestData(cls):
        InitStatus()
        seed_flow()
        cls.period = Period.objects.create(year=2025)

        cls.group_structures = GeneralGroup.objects.create(
            name='estructuras', public_name='Estructuras')
        cls.group_plans = GeneralGroup.objects.create(
            name='planes_estudio', public_name='Planes de estudio')
        cls.group_government = GeneralGroup.objects.create(
            name='forma_gobierno', public_name='Forma de gobierno')

        cls.q_instances = GeneralQuestion.objects.create(
            general_group=cls.group_structures, name='academic_instances',
            text='Instancias académicas', order=1)
        cls.q_plans = GeneralQuestion.objects.create(
            general_group=cls.group_plans, name='media_plans',
            text='Planes de nivel medio superior', order=1,
            addl_config={'allow_no_apply': True})
        cls.q_centralized = GeneralQuestion.objects.create(
            general_group=cls.group_government, name='is_centralized',
            text='Forma de gobierno', q_type='boolean', order=1)

        # Institution.save aprovisiona el survey y sus grupos de
        # respuesta sobre los periodos y grupos que ya existen.
        cls.institution = Institution.objects.create(
            name='IES de prueba', acronym='IESP')
        cls.survey = cls.institution.surveys.get(period=cls.period)
        cls.responses = {
            response.general_group_id: response
            for response in cls.survey.general_group_responses.all()}


class GeneralValidationTests(GeneralQuestionTestCase):
    """Compuerta de contenido leyendo la fila de respuesta."""

    def test_missing_row_blocks(self):
        issues = group_completion_issues(
            self.responses['estructuras'])
        self.assertEqual(
            issues, ['Falta la respuesta: Instancias académicas'])

    def test_null_value_blocks(self):
        GeneralQuestionResponse.objects.create(
            survey=self.survey, general_question=self.q_instances)
        self.assertEqual(len(group_completion_issues(
            self.responses['estructuras'])), 1)

    def test_zero_is_an_answer(self):
        GeneralQuestionResponse.objects.create(
            survey=self.survey, general_question=self.q_instances,
            value_integer=0)
        self.assertEqual(
            group_completion_issues(self.responses['estructuras']), [])

    def test_empty_string_counts_as_empty(self):
        # La columna es entera: el `''` solo existe en memoria, así que
        # la lectura se prueba directa sobre el helper. Es la mitad
        # backend del acuerdo `'' == None` (la otra vive en el
        # serializer, que lo normaliza al entrar).
        response = GeneralQuestionResponse(
            survey=self.survey, general_question=self.q_instances)
        response.value_integer = ''
        self.assertIsNone(_answered_value(self.q_instances, response))

    def test_false_is_an_answer(self):
        GeneralQuestionResponse.objects.create(
            survey=self.survey, general_question=self.q_centralized,
            value_boolean=False)
        self.assertEqual(
            group_completion_issues(self.responses['forma_gobierno']), [])

    def test_no_apply_exempts_when_allowed(self):
        GeneralQuestionResponse.objects.create(
            survey=self.survey, general_question=self.q_plans,
            no_apply=True)
        self.assertEqual(
            group_completion_issues(self.responses['planes_estudio']), [])

    def test_no_apply_blocks_without_the_flag(self):
        GeneralQuestionResponse.objects.create(
            survey=self.survey, general_question=self.q_centralized,
            no_apply=True)
        self.assertEqual(
            group_completion_issues(self.responses['forma_gobierno']),
            ['Falta la respuesta: Forma de gobierno'])


class GeneralQuestionResponseSyncTests(GeneralQuestionTestCase):
    """Upsert de las respuestas anidadas en el Survey."""

    def _save(self, rows: list) -> None:
        serializer = SurveySerializer(
            self.survey, data={'question_responses': rows}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    def _row(self, question) -> GeneralQuestionResponse:
        return GeneralQuestionResponse.objects.get(
            survey=self.survey, general_question=question)

    def test_value_lands_in_its_typed_column(self):
        self._save([
            {'general_question': self.q_instances.pk, 'value_integer': 12},
            {'general_question': self.q_centralized.pk,
             'value_boolean': True},
        ])
        self.assertEqual(self._row(self.q_instances).value_integer, 12)
        self.assertIs(self._row(self.q_centralized).value_boolean, True)

    def test_empty_string_becomes_null(self):
        self._save([
            {'general_question': self.q_instances.pk, 'value_integer': ''}])
        self.assertIsNone(self._row(self.q_instances).value_integer)

    def test_no_apply_clears_both_values(self):
        self._save([
            {'general_question': self.q_plans.pk, 'value_integer': 7}])
        self._save([
            {'general_question': self.q_plans.pk, 'no_apply': True,
             'value_integer': 7}])
        row = self._row(self.q_plans)
        self.assertTrue(row.no_apply)
        self.assertIsNone(row.value_integer)
        self.assertIsNone(row.value_boolean)

    def test_second_write_updates_the_same_row(self):
        self._save([
            {'general_question': self.q_instances.pk, 'value_integer': 3}])
        self._save([
            {'general_question': self.q_instances.pk, 'value_integer': 5}])
        rows = GeneralQuestionResponse.objects.filter(
            survey=self.survey, general_question=self.q_instances)
        self.assertEqual(rows.count(), 1)
        self.assertEqual(rows.first().value_integer, 5)


class PreloadCentralizedTests(GeneralQuestionTestCase):
    """Precarga de la forma de gobierno que ya conoce el catálogo."""

    def _row(self, institution) -> GeneralQuestionResponse:
        return GeneralQuestionResponse.objects.get(
            survey__institution=institution,
            general_question=self.q_centralized)

    def test_row_created_with_the_institution_value(self):
        institution = Institution.objects.create(
            name='IES centralizada', acronym='IESC', is_centralized=True)
        self.assertIs(self._row(institution).value_boolean, True)

    def test_captured_answer_is_respected_on_resave(self):
        institution = Institution.objects.create(
            name='IES resave', acronym='IESR', is_centralized=True)
        row = self._row(institution)
        row.value_boolean = False
        row.save()

        institution.save()

        row.refresh_from_db()
        self.assertIs(row.value_boolean, False)

    def test_no_row_when_the_institution_says_nothing(self):
        institution = Institution.objects.create(
            name='IES sin dato', acronym='IESS')
        self.assertFalse(GeneralQuestionResponse.objects.filter(
            survey__institution=institution).exists())
