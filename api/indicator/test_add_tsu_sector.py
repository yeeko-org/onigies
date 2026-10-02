"""Alta del sector TSU (`add_tsu_sector`): correrlo de nuevo no duplica
ni pisa lo que la IES ya contestó."""
from io import StringIO

from django.core.management import call_command

from indicator.management.commands.add_tsu_sector import SECTOR_NAME
from indicator.models import Axis, Component, Observable, Sector
from question.models import GeneralQuestion, ReachQuestion
from survey.models import GeneralQuestionResponse, PopulationQuantity
from survey.tests import GeneralQuestionTestCase


class AddTsuSectorTests(GeneralQuestionTestCase):

    @classmethod
    def setUpTestData(cls):
        # La base trae `media_plans` (orden 1); se completa el grupo
        # como estaba antes del TSU.
        super().setUpTestData()
        for name, order in (('superior_plans', 2),
                            ('postgraduate_plans', 3)):
            GeneralQuestion.objects.create(
                general_group=cls.group_plans, name=name, text=name,
                order=order, addl_config={'allow_no_apply': True})
        # 1.16 trae lista de alcance propia, sin los sectores is_main.
        axis = Axis.objects.create(name='Eje 1', color='blue', order=1)
        component = Component.objects.create(name='C1', axis=axis)
        observable = Observable.objects.create(
            component=component, number='1.16', order=1, name='Permanencia')
        cls.reach = ReachQuestion.objects.create(
            observable=observable, text='¿En qué sectores del alumnado?',
            has_main_sectors=False)
        cls.reach.others_sectors.add(Sector.objects.create(
            name='Alumnado de nivel medio superior', is_main=True))

    def run_command(self):
        call_command('add_tsu_sector', stdout=StringIO())

    def plans_order(self) -> dict:
        return dict(GeneralQuestion.objects.filter(
            general_group=self.group_plans).values_list('name', 'order'))

    def test_second_run_changes_nothing(self):
        self.run_command()
        self.run_command()
        sector = Sector.objects.get(name=SECTOR_NAME)
        quantities = PopulationQuantity.objects.filter(
            survey=self.survey, sector=sector)
        self.assertEqual(quantities.count(), 1)
        self.assertIs(quantities.get().is_present, False)
        self.assertEqual(GeneralQuestion.objects.filter(
            name='technical_plans').count(), 1)
        self.assertEqual(self.plans_order(), {
            'media_plans': 1, 'technical_plans': 2,
            'superior_plans': 3, 'postgraduate_plans': 4})
        responses = GeneralQuestionResponse.objects.filter(
            survey=self.survey, general_question__name='technical_plans')
        self.assertEqual(responses.count(), 1)
        self.assertIs(responses.get().no_apply, True)
        others = self.reach.others_sectors
        self.assertEqual(others.count(), 2)
        self.assertTrue(others.filter(pk=sector.pk).exists())

    def test_existing_answers_are_not_overwritten(self):
        # Como en producción: el sector y la pregunta ya existen y la IES
        # ya contestó que tiene el nivel.
        sector = Sector.objects.create(name=SECTOR_NAME)
        question = GeneralQuestion.objects.create(
            general_group=self.group_plans, name='technical_plans',
            text='TSU', order=2, addl_config={'allow_no_apply': True})
        PopulationQuantity.objects.create(
            survey=self.survey, sector=sector, is_present=True)
        GeneralQuestionResponse.objects.create(
            survey=self.survey, general_question=question,
            no_apply=False, value_integer=5)
        self.run_command()
        quantity = PopulationQuantity.objects.get(
            survey=self.survey, sector=sector)
        self.assertIs(quantity.is_present, True)
        response = GeneralQuestionResponse.objects.get(
            survey=self.survey, general_question=question)
        self.assertIs(response.no_apply, False)
        self.assertEqual(response.value_integer, 5)

    def test_untouched_presence_becomes_explicit_no(self):
        # Institution.save deja la fila con presencia nula si la IES se
        # guardó después de que Rubén creó el sector.
        sector = Sector.objects.create(name=SECTOR_NAME)
        PopulationQuantity.objects.create(
            survey=self.survey, sector=sector, is_present=None)
        self.run_command()
        row = PopulationQuantity.objects.get(
            survey=self.survey, sector=sector)
        self.assertIs(row.is_present, False)
