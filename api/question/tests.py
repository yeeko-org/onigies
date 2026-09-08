"""Las dos primeras clases corren `load_questionnaire` completo: el
contrato del re-seed contra una base ya editada desde el dashboard no se
puede simular con un catálogo mínimo."""
from decimal import Decimal
from io import StringIO

from django.core.management import call_command
from django.db.models import Count
from django.test import TestCase

from indicator.models import Axis, Component, Observable
from question.initial_data import InitQuestionTypes
from question.models import AQuestion, ObservableQuestionType, QuestionType

# Conteos del instrumento 2026.
EXPECTED_TYPE_COUNTS = {
    'a_questions': 41,
    'b_questions': 41,
    'reach': 35,
    'plans': 1,
    'special': 1,
    'population': 1,
}


def run_seed(overwrite_texts: bool = False) -> None:
    """Corre load_questionnaire silenciando su salida."""
    args = ['--overwrite-texts'] if overwrite_texts else []
    call_command(
        'load_questionnaire', *args, stdout=StringIO(), stderr=StringIO())


def seed_questionnaire() -> None:
    """Prerrequisitos del comando más la siembra."""
    InitQuestionTypes()
    call_command('load_sectors', stdout=StringIO())
    run_seed()


class SeedTextOwnershipTests(TestCase):
    """De los textos manda el dashboard, salvo con --overwrite-texts."""

    EDITED_OBSERVABLE = "Pregunta A editada desde el dashboard"
    EDITED_QUESTION = "Opción A editada desde el dashboard"
    EDITED_AXIS = "Eje renombrado desde el dashboard"

    @classmethod
    def setUpTestData(cls) -> None:
        seed_questionnaire()

    def setUp(self) -> None:
        self.observable = Observable.objects.get(number='1.1')
        self.question = AQuestion.objects.filter(
            observable=self.observable).first()
        self.axis = Axis.objects.get(order=1)
        self.seeded_observable_text = self.observable.a_main_question
        self.seeded_question_text = self.question.text
        # update() y no save(): interesa el estado en base, sin que la
        # instancia en memoria enmascare lo que el re-seed escribió.
        Observable.objects.filter(pk=self.observable.pk).update(
            a_main_question=self.EDITED_OBSERVABLE)
        AQuestion.objects.filter(pk=self.question.pk).update(
            text=self.EDITED_QUESTION)
        Axis.objects.filter(pk=self.axis.pk).update(name=self.EDITED_AXIS)

    def _refresh(self) -> None:
        for obj in (self.observable, self.question, self.axis):
            obj.refresh_from_db()

    def test_reseed_keeps_edited_texts(self) -> None:
        run_seed()
        self._refresh()
        self.assertEqual(
            self.observable.a_main_question, self.EDITED_OBSERVABLE)
        self.assertEqual(self.question.text, self.EDITED_QUESTION)

    def test_overwrite_flag_restores_seed_texts(self) -> None:
        run_seed(overwrite_texts=True)
        self._refresh()
        self.assertEqual(
            self.observable.a_main_question, self.seeded_observable_text)
        self.assertEqual(self.question.text, self.seeded_question_text)

    def test_axis_name_survives_the_overwrite_flag(self) -> None:
        run_seed(overwrite_texts=True)
        self._refresh()
        self.assertEqual(self.axis.name, self.EDITED_AXIS)


class TypeWeightSyncTests(TestCase):
    """El re-seed repone la aplicabilidad y no pisa la ponderación."""

    MANUAL_WEIGHT = Decimal('15.00')

    @classmethod
    def setUpTestData(cls) -> None:
        seed_questionnaire()

    def setUp(self) -> None:
        self.deleted_observable = Observable.objects.get(number='1.1')
        ObservableQuestionType.objects.filter(
            observable=self.deleted_observable,
            question_type_id='a_questions').delete()
        self.weighted = ObservableQuestionType.objects.get(
            observable__number='1.2', question_type_id='b_questions')
        ObservableQuestionType.objects.filter(pk=self.weighted.pk).update(
            weight=self.MANUAL_WEIGHT)
        run_seed()

    def test_missing_row_is_recreated(self) -> None:
        self.assertTrue(ObservableQuestionType.objects.filter(
            observable=self.deleted_observable,
            question_type_id='a_questions').exists())

    def test_manual_weight_is_not_overwritten(self) -> None:
        self.weighted.refresh_from_db()
        self.assertEqual(self.weighted.weight, self.MANUAL_WEIGHT)

    def test_type_counts_after_reseed(self) -> None:
        counts = dict(
            ObservableQuestionType.objects
            .values_list('question_type_id')
            .annotate(total=Count('id')))
        self.assertEqual(counts, EXPECTED_TYPE_COUNTS)


class FinalWeightTests(TestCase):
    """Ponderación efectiva: la propia, si no la del tipo, si no nada."""

    @classmethod
    def setUpTestData(cls) -> None:
        axis = Axis.objects.create(order=1, name="Eje de prueba", color="teal")
        component = Component.objects.create(
            axis=axis, name="Componente de prueba")
        cls.observable = Observable.objects.create(
            component=component, number="1.1", name="Observable de prueba")
        cls.question_type = QuestionType.objects.create(
            name='a_questions', public_name="Tipo de prueba",
            default_weight=Decimal('60.00'), order=1, required=True)

    def test_own_weight_wins(self) -> None:
        row = ObservableQuestionType.objects.create(
            observable=self.observable, question_type=self.question_type,
            weight=Decimal('25.00'))
        self.assertEqual(row.final_weight, Decimal('25.00'))

    def test_falls_back_to_type_default(self) -> None:
        row = ObservableQuestionType.objects.create(
            observable=self.observable, question_type=self.question_type)
        self.assertEqual(row.final_weight, Decimal('60.00'))

    def test_weight_for_without_row_is_none(self) -> None:
        self.assertIsNone(self.observable.weight_for('plans'))
