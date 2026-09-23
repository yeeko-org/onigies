"""
Captura del cuestionario principal (flujo `cp`): aprovisionamiento
eager, la pregunta inicial y `cp_not_present`, la compuerta de contenido
por tipo, la compuerta de respuesta (fecha + generales validadas) y los
permisos IES/revisora de los endpoints.

El catálogo se construye a mano (un eje, tres observables) en vez de
`load_questionnaire`: las reglas se ven con un observable por forma.
"""
from datetime import timedelta

from django.db import connection
from django.test.utils import CaptureQueriesContext
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase

from answer.group_validation import group_completion
from answer.models import (
    AResponse, BResponse, GroupResponse, ObservableResponse, PlanResponse,
    ReachResponse, SpecialResponse)
from answer.services import InitValueError, set_init_value
from flow.models import FlowEvent, Status
from flow.permissions import user_can_edit_flow_content
from flow.seed import seed_flow
from flow.services import execute_transition, validate_transition
from ies.models import Institution, Period, User
from indicator.models import (
    Axis, Component, GeneralGroup, Observable, Sector)
from question.initial_data import InitQuestionTypes
from question.models import (
    AOption, AQuestion, BQuestion, GeneralQuestion, ObservableQuestionType,
    PlanQuestion, ReachQuestion, SpecialQuestion)
from survey.models import GeneralQuestionResponse


def status(name: str) -> Status:
    return Status.objects.get(name=name)


def force(obj, name: str) -> None:
    """Fija un status sin pasar por el motor (estado previo del caso)."""
    type(obj).objects.filter(pk=obj.pk).update(status_id=name)
    obj.refresh_from_db()


class CpCatalogTestCase(APITestCase):
    """Base: catálogo mínimo, periodo abierto, IES con generales
    validadas, otra IES y una revisora."""

    @classmethod
    def setUpTestData(cls):
        seed_flow()
        InitQuestionTypes()
        cls.yes, cls.no = (
            AOption.objects.create(text='Sí', value=1),
            AOption.objects.create(text='No', value=0))
        cls.main_sector = Sector.objects.create(name='Estudiantes')
        cls.extra_sector = Sector.objects.create(
            name='Público', is_main=False, is_standard_extra=True)

        axis = Axis.objects.create(name='Eje 1', color='blue', order=1)
        component = Component.objects.create(name='C1', axis=axis)
        cls.obs_std = Observable.objects.create(
            component=component, number='1.1', order=1, name='Estándar',
            init_question='¿Cuenta con la medida?')
        cls.obs_plan = Observable.objects.create(
            component=component, number='1.12', order=2, name='Planes')
        cls.obs_special = Observable.objects.create(
            component=component, number='1.14', order=3, name='Especial')

        cls.aq1 = AQuestion.objects.create(
            observable=cls.obs_std, text='Opción 1', order=1)
        cls.aq2 = AQuestion.objects.create(
            observable=cls.obs_std, text='Opción 2', order=2)
        cls.bq = BQuestion.objects.create(
            observable=cls.obs_std, text='¿En cuántas instancias?',
            includes_academic=True, includes_admin=True)
        cls.rq = ReachQuestion.objects.create(
            observable=cls.obs_std, text='¿A quién alcanza?',
            has_main_sectors=True, has_general_planning=True)
        cls.rq.others_sectors.add(cls.extra_sector)
        cls.pq = PlanQuestion.objects.create(
            observable=cls.obs_plan, text='¿Cuántos planes?', order=1)
        cls.sq = SpecialQuestion.objects.create(
            observable=cls.obs_special, text='Proyectos liderados')
        cls.bq_special = BQuestion.objects.create(
            observable=cls.obs_special, text='Instancias académicas',
            includes_academic=True, includes_admin=False)

        for observable, types in (
                (cls.obs_std, ('a_questions', 'b_questions', 'reach')),
                (cls.obs_plan, ('a_questions', 'b_questions', 'plans')),
                (cls.obs_special, ('a_questions', 'b_questions', 'special'))):
            for type_name in types:
                ObservableQuestionType.objects.create(
                    observable=observable, question_type_id=type_name)

        group = GeneralGroup.objects.create(
            name='estructuras', public_name='E')
        cls.gq_academic = GeneralQuestion.objects.create(
            general_group=group, name='academic_instances', text='Acad.')
        cls.gq_admin = GeneralQuestion.objects.create(
            general_group=group, name='admin_instances', text='Admin.')
        plans = GeneralGroup.objects.create(
            name='planes_estudio', public_name='P')
        cls.gq_media = GeneralQuestion.objects.create(
            general_group=plans, name='media_plans', text='Media',
            addl_config={'allow_no_apply': True})
        cls.gq_superior = GeneralQuestion.objects.create(
            general_group=plans, name='superior_plans', text='Superior',
            addl_config={'allow_no_apply': True})
        cls.gq_postgraduate = GeneralQuestion.objects.create(
            general_group=plans, name='postgraduate_plans', text='Posgrado',
            addl_config={'allow_no_apply': True})

        cls.period = Period.objects.create(
            year=2026, cp_open_at=timezone.now() - timedelta(days=1))
        cls.inst_a = Institution.objects.create(name='IES A', acronym='IESA')
        cls.inst_b = Institution.objects.create(name='IES B', acronym='IESB')
        cls.survey_a = cls.inst_a.surveys.get(period=cls.period)
        cls.survey_b = cls.inst_b.surveys.get(period=cls.period)
        for survey in (cls.survey_a, cls.survey_b):
            force(survey.general_package, 'gen_finished')

        cls.ies_a = User.objects.create_user(
            'iesa', password='x', institution=cls.inst_a)
        cls.ies_b = User.objects.create_user(
            'iesb', password='x', institution=cls.inst_b)
        cls.reviewer = User.objects.create_user(
            'rev', password='x', reviewer=True)

    def setUp(self):
        self.axis_value = self.survey_a.axis_values.get()
        self.obs_response = ObservableResponse.objects.get(
            survey=self.survey_a, observable=self.obs_std)
        self.group_a = self.obs_response.statuses.get(
            question_type_id='a_questions')
        self.group_b = self.obs_response.statuses.get(
            question_type_id='b_questions')
        self.group_reach = self.obs_response.statuses.get(
            question_type_id='reach')

    def gen_answer(self, question, value=None, no_apply=False) -> None:
        GeneralQuestionResponse.objects.update_or_create(
            survey=self.survey_a, general_question=question,
            defaults={'value_integer': value, 'no_apply': no_apply})

    def answer_a_complete(self) -> None:
        for question in (self.aq1, self.aq2):
            AResponse.objects.create(
                group_response=self.group_a, question=question,
                selected_option=self.yes)

    def transitions_url(self, obj) -> str:
        return reverse('flow-transitions', args=[
            'answer', type(obj).__name__.lower(), obj.pk])


class ProvisioningTests(CpCatalogTestCase):
    """Eager en `Institution.save`: un ObservableResponse por observable
    del eje y un GroupResponse por fila puente; idempotente."""

    def test_counts_after_create(self):
        self.assertEqual(
            ObservableResponse.objects.filter(survey=self.survey_a).count(), 3)
        self.assertEqual(GroupResponse.objects.filter(
            observable_response__survey=self.survey_a).count(), 9)
        self.assertEqual(self.obs_response.status_id, 'cp_pre_start')
        self.assertEqual(self.group_a.status_id, 'cp_pre_start')
        self.assertEqual(self.obs_response.axis_value, self.axis_value)

    def test_resave_is_idempotent_and_backfills(self):
        self.inst_a.save()
        self.assertEqual(GroupResponse.objects.filter(
            observable_response__survey=self.survey_a).count(), 9)
        # Una fila puente nueva se refleja en el siguiente guardado.
        ObservableQuestionType.objects.create(
            observable=self.obs_std, question_type_id='plans')
        self.inst_a.save()
        self.assertEqual(GroupResponse.objects.filter(
            observable_response__survey=self.survey_a).count(), 10)
        self.inst_a.save()
        self.assertEqual(GroupResponse.objects.filter(
            observable_response__survey=self.survey_a).count(), 10)


class InitValueTests(CpCatalogTestCase):
    """La pregunta inicial gobierna al observable y a sus grupos."""

    def group_statuses(self) -> set:
        return set(self.obs_response.statuses.values_list(
            'status_id', flat=True))

    def test_no_moves_tree_to_not_present_with_events(self):
        self.answer_a_complete()
        set_init_value(self.ies_a, self.obs_response, False)
        self.obs_response.refresh_from_db()
        self.assertFalse(self.obs_response.value)
        self.assertEqual(self.obs_response.status_id, 'cp_not_present')
        self.assertEqual(self.group_statuses(), {'cp_not_present'})
        self.assertEqual(FlowEvent.objects.filter(
            to_status_id='cp_not_present').count(), 4)
        # Las respuestas tipadas se conservan.
        self.assertEqual(self.group_a.a_responses.count(), 2)
        # El eje arranca la captura.
        self.axis_value.refresh_from_db()
        self.assertEqual(self.axis_value.status_id, 'cp_filling')

    def test_yes_after_no_reopens_to_filling(self):
        set_init_value(self.ies_a, self.obs_response, False)
        set_init_value(self.ies_a, self.obs_response, True)
        self.obs_response.refresh_from_db()
        self.assertEqual(self.obs_response.status_id, 'cp_filling')
        self.assertEqual(self.group_statuses(), {'cp_filling'})
        self.assertTrue(FlowEvent.objects.filter(
            object_id=self.group_a.pk, from_status_id='cp_not_present',
            to_status_id='cp_filling').exists())

    def test_null_after_no_also_reopens(self):
        set_init_value(self.ies_a, self.obs_response, False)
        set_init_value(self.ies_a, self.obs_response, None)
        self.obs_response.refresh_from_db()
        self.assertIsNone(self.obs_response.value)
        self.assertEqual(self.obs_response.status_id, 'cp_filling')

    def test_first_yes_promotes_observable_and_axis(self):
        set_init_value(self.ies_a, self.obs_response, True)
        self.obs_response.refresh_from_db()
        self.axis_value.refresh_from_db()
        self.assertEqual(self.obs_response.status_id, 'cp_filling')
        self.assertEqual(self.axis_value.status_id, 'cp_filling')
        # Los grupos siguen en reposo hasta que se capturen.
        self.assertEqual(self.group_statuses(), {'cp_pre_start'})

    def test_yes_starts_groups_without_capturable_content(self):
        """Un grupo cuyo tipo no tiene modelo de respuesta (population)
        nunca recibe un PATCH: el «Sí» lo promueve para que pueda
        completarse desde el menú como cualquier otro."""
        population = GroupResponse.objects.create(
            observable_response=self.obs_response,
            question_type_id='population')
        self.assertEqual(population.status_id, 'cp_pre_start')
        set_init_value(self.ies_a, self.obs_response, True)
        population.refresh_from_db()
        self.group_b.refresh_from_db()
        self.assertEqual(population.status_id, 'cp_filling')
        self.assertEqual(self.group_b.status_id, 'cp_pre_start')
        self.assertTrue(FlowEvent.objects.filter(
            object_id=population.pk, to_status_id='cp_filling').exists())
        # Y desde ahí el menú lo lleva a completado sin contenido.
        execute_transition(self.ies_a, population, status('cp_completed'))
        population.refresh_from_db()
        self.assertEqual(population.status_id, 'cp_completed')
        # Un segundo «Sí» no lo regresa.
        set_init_value(self.ies_a, self.obs_response, True)
        population.refresh_from_db()
        self.assertEqual(population.status_id, 'cp_completed')

    def test_no_blocked_when_a_group_is_under_review(self):
        for name in ('cp_need_changes', 'cp_in_adjustment', 'cp_adjusted',
                     'cp_approved', 'cp_partial', 'cp_partial_approved'):
            force(self.group_b, name)
            with self.assertRaises(InitValueError) as ctx:
                set_init_value(self.ies_a, self.obs_response, False)
            self.assertIn('en revisión', ctx.exception.args[0][0])
        force(self.group_b, 'cp_completed')
        set_init_value(self.ies_a, self.obs_response, False)
        self.obs_response.refresh_from_db()
        self.assertEqual(self.obs_response.status_id, 'cp_not_present')

    def test_blocked_when_axis_not_in_ies_turn(self):
        force(self.axis_value, 'cp_sent')
        with self.assertRaises(InitValueError):
            set_init_value(self.ies_a, self.obs_response, False)
        with self.assertRaises(InitValueError):
            set_init_value(self.ies_a, self.obs_response, True)

    def test_reopen_does_not_touch_axis_in_correction(self):
        set_init_value(self.ies_a, self.obs_response, False)
        force(self.axis_value, 'cp_need_changes')
        set_init_value(self.ies_a, self.obs_response, True)
        self.axis_value.refresh_from_db()
        self.assertEqual(self.axis_value.status_id, 'cp_need_changes')

    def test_reviewer_cannot_answer(self):
        with self.assertRaises(InitValueError):
            set_init_value(self.reviewer, self.obs_response, True)


class ObservableFlowRulesTests(CpCatalogTestCase):
    """Reglas del motor alrededor del observable: pregunta inicial sin
    responder, `cp_not_present` como hijo válido y el hueco de la
    pospuesta."""

    def complete_groups(self, observable_response) -> None:
        observable_response.statuses.update(status_id='cp_completed')

    def test_null_value_blocks_completing_the_observable(self):
        force(self.obs_response, 'cp_filling')
        self.complete_groups(self.obs_response)
        errors = validate_transition(
            self.ies_a, self.obs_response, status('cp_completed'))
        self.assertEqual(
            errors, ['Falta responder la pregunta inicial del observable.'])
        set_init_value(self.ies_a, self.obs_response, True)
        self.obs_response.refresh_from_db()
        self.assertEqual(validate_transition(
            self.ies_a, self.obs_response, status('cp_completed')), [])

    def test_not_present_counts_as_valid_child_for_completed_and_sent(self):
        force(self.axis_value, 'cp_filling')
        set_init_value(self.ies_a, self.obs_response, False)
        for other in ObservableResponse.objects.filter(
                survey=self.survey_a).exclude(pk=self.obs_response.pk):
            other.value = True
            other.save()
            force(other, 'cp_filling')
            self.complete_groups(other)
            execute_transition(self.ies_a, other, status('cp_completed'))
        self.assertEqual(validate_transition(
            self.ies_a, self.axis_value, status('cp_sent')), [])
        execute_transition(self.ies_a, self.axis_value, status('cp_sent'))
        self.axis_value.refresh_from_db()
        self.assertEqual(self.axis_value.status_id, 'cp_sent')

    def test_not_present_has_no_manual_transitions(self):
        self.assertEqual(status('cp_not_present').next_statuses.count(), 0)
        self.assertIsNone(status('cp_not_present').role)

    def test_partial_approval_accepts_not_present_groups(self):
        force(self.axis_value, 'cp_in_review')
        force(self.obs_response, 'cp_partial')
        self.obs_response.value = True
        self.obs_response.save()
        self.obs_response.statuses.update(status_id='cp_partial_approved')
        force(self.group_reach, 'cp_not_present')
        self.assertEqual(validate_transition(
            self.reviewer, self.obs_response,
            status('cp_partial_approved')), [])
        force(self.group_reach, 'cp_filling')
        self.assertTrue(validate_transition(
            self.reviewer, self.obs_response,
            status('cp_partial_approved')))

    def test_reviewer_waits_for_the_axis_to_be_sent(self):
        """Un grupo completado ya tiene rol reviewer, pero la revisión
        no lo devuelve ni lo aprueba mientras el eje siga en turno de
        la IES; en cuanto el eje está en revisión, sí."""
        self.answer_a_complete()
        force(self.group_a, 'cp_completed')
        force(self.obs_response, 'cp_filling')
        force(self.axis_value, 'cp_filling')
        group = GroupResponse.objects.select_related(
            'observable_response__axis_value__status').get(
            pk=self.group_a.pk)
        errors = validate_transition(
            self.reviewer, group, status('cp_need_changes'), 'Falta.')
        self.assertEqual(len(errors), 1)
        self.assertIn('aún no se ha enviado a revisión', errors[0])
        # La IES no ve el mensaje (su turno sobre el grupo no existe,
        # pero la razón que recibe es la del rol, no la del eje).
        ies_errors = validate_transition(
            self.ies_a, group, status('cp_need_changes'), 'Falta.')
        self.assertFalse(
            any('enviado a revisión' in e for e in ies_errors))
        force(self.axis_value, 'cp_in_review')
        group.refresh_from_db()
        self.assertEqual(validate_transition(
            self.reviewer, group, status('cp_need_changes'), 'Falta.'),
            [])
        self.client.force_authenticate(self.reviewer)
        force(self.axis_value, 'cp_filling')
        response = self.client.post(self.transitions_url(group), {
            'target_status': 'cp_need_changes', 'comment': 'Falta.'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('aún no se ha enviado', response.data['detail'])

    def test_reviewer_waits_on_the_observable_too(self):
        self.obs_response.statuses.update(status_id='cp_approved')
        self.obs_response.value = True
        self.obs_response.save()
        force(self.obs_response, 'cp_completed')
        force(self.axis_value, 'cp_filling')
        errors = validate_transition(
            self.reviewer, self.obs_response, status('cp_approved'))
        self.assertEqual(len(errors), 1)
        self.assertIn('aún no se ha enviado a revisión', errors[0])
        force(self.axis_value, 'cp_in_review')
        self.obs_response.refresh_from_db()
        self.assertEqual(validate_transition(
            self.reviewer, self.obs_response, status('cp_approved')), [])

    def test_postponed_requires_resolved_groups(self):
        force(self.obs_response, 'cp_filling')
        self.obs_response.value = True
        self.obs_response.save()
        errors = validate_transition(
            self.ies_a, self.obs_response, status('cp_postponed'))
        self.assertTrue(errors)
        self.assertIn('elemento(s)', errors[0])
        self.obs_response.statuses.update(status_id='cp_postponed')
        force(self.group_a, 'cp_completed')
        self.assertEqual(validate_transition(
            self.ies_a, self.obs_response, status('cp_postponed')), [])


class GroupValidationTests(CpCatalogTestCase):
    """Compuerta de contenido por tipo: qué bloquea, qué advierte."""

    def errors(self, group) -> list:
        return group_completion(group).errors

    def test_a_requires_every_option_answered(self):
        self.assertEqual(len(self.errors(self.group_a)), 2)
        AResponse.objects.create(
            group_response=self.group_a, question=self.aq1,
            selected_option=self.no)
        self.assertEqual(
            self.errors(self.group_a), ['Falta responder: Opción 2'])
        AResponse.objects.create(
            group_response=self.group_a, question=self.aq2,
            selected_option=self.yes)
        self.assertEqual(self.errors(self.group_a), [])

    def test_b_requires_counts_within_gen_denominators(self):
        self.assertEqual(len(self.errors(self.group_b)), 2)
        row = BResponse.objects.create(
            group_response=self.group_b, question=self.bq,
            academic_instances_complying=5, admin_instances_complying=0)
        # Sin denominador en gen: pasa, pero advierte.
        completion = group_completion(self.group_b)
        self.assertEqual(completion.errors, [])
        self.assertEqual(len(completion.warnings), 2)
        self.gen_answer(self.gq_academic, 3)
        self.gen_answer(self.gq_admin, 2)
        self.assertEqual(len(self.errors(self.group_b)), 1)
        self.assertIn('rebasa', self.errors(self.group_b)[0])
        row.academic_instances_complying = 3
        row.save()
        self.assertEqual(self.errors(self.group_b), [])

    def test_b_academic_only_ignores_admin(self):
        response = ObservableResponse.objects.get(
            survey=self.survey_a, observable=self.obs_special)
        group = response.statuses.get(question_type_id='b_questions')
        BResponse.objects.create(
            group_response=group, question=self.bq_special,
            academic_instances_complying=1)
        self.assertEqual(self.errors(group), [])

    def test_reach_requires_sector_or_general_planning(self):
        self.assertEqual(len(self.errors(self.group_reach)), 1)
        row = ReachResponse.objects.create(
            group_response=self.group_reach, question=self.rq)
        self.assertEqual(len(self.errors(self.group_reach)), 1)
        row.not_focalized = True
        row.save()
        self.assertEqual(self.errors(self.group_reach), [])
        row.not_focalized = False
        row.save()
        row.sectors.add(self.main_sector)
        self.assertEqual(self.errors(self.group_reach), [])

    def test_plans_follow_levels_declared_in_gen(self):
        response = ObservableResponse.objects.get(
            survey=self.survey_a, observable=self.obs_plan)
        group = response.statuses.get(question_type_id='plans')
        # Sin gen: no bloquea, advierte por nivel.
        completion = group_completion(group)
        self.assertEqual(completion.errors, [])
        self.assertEqual(len(completion.warnings), 3)
        self.gen_answer(self.gq_media, no_apply=True)
        self.gen_answer(self.gq_superior, 10)
        self.gen_answer(self.gq_postgraduate, 4)
        self.assertEqual(len(self.errors(group)), 2)
        PlanResponse.objects.create(
            group_response=group, question=self.pq, superior_plans=11,
            postgraduate_plans=2)
        self.assertEqual(len(self.errors(group)), 1)
        self.assertIn('rebasa', self.errors(group)[0])

    def test_special_requires_total_and_complying(self):
        response = ObservableResponse.objects.get(
            survey=self.survey_a, observable=self.obs_special)
        group = response.statuses.get(question_type_id='special')
        self.assertEqual(len(self.errors(group)), 2)
        row = SpecialResponse.objects.create(
            group_response=group, question=self.sq, total=3, complying=5)
        self.assertEqual(len(self.errors(group)), 1)
        row.complying = 3
        row.save()
        self.assertEqual(self.errors(group), [])

    def test_hook_blocks_completed_not_postponed(self):
        force(self.group_a, 'cp_filling')
        self.assertTrue(validate_transition(
            self.ies_a, self.group_a, status('cp_completed')))
        self.assertEqual(validate_transition(
            self.ies_a, self.group_a, status('cp_postponed')), [])


class CaptureGateTests(CpCatalogTestCase):
    """Compuerta de respuesta: fecha de apertura y generales validadas.
    Las de prueba no están exentas; la revisión no está sujeta."""

    def value_url(self) -> str:
        return reverse(
            'observable_response-detail', args=[self.obs_response.pk])

    def patch_value(self, value=True):
        self.client.force_authenticate(self.ies_a)
        return self.client.patch(self.value_url(), {'value': value},
                                 format='json')

    def test_not_open_by_date(self):
        for open_at in (None, timezone.now() + timedelta(hours=1)):
            Period.objects.filter(pk=self.period.pk).update(cp_open_at=open_at)
            response = self.patch_value()
            self.assertEqual(response.status_code, 403)
            self.assertEqual(response.json()['code'], 'cp_not_open')
        Period.objects.filter(pk=self.period.pk).update(
            cp_open_at=timezone.now() - timedelta(days=1))
        self.assertEqual(self.patch_value().status_code, 200)

    def test_gen_not_validated(self):
        force(self.survey_a.general_package, 'gen_sent')
        response = self.patch_value()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['code'], 'gen_not_approved')

    def test_survey_payload_exposes_cp_capture(self):
        self.client.force_authenticate(self.ies_a)
        response = self.client.get(
            reverse('survey-detail', args=[self.survey_a.pk]))
        self.assertEqual(response.json()['cp_capture'], {
            'open': True, 'reason': None,
            'open_at': self.period.cp_open_at.isoformat()})
        force(self.survey_a.general_package, 'gen_draft')
        response = self.client.get(
            reverse('survey-detail', args=[self.survey_a.pk]))
        self.assertEqual(
            response.json()['cp_capture']['reason'], 'gen_not_approved')

    def test_test_institution_is_not_exempt(self):
        Institution.objects.filter(pk=self.inst_a.pk).update(is_test=True)
        Period.objects.filter(pk=self.period.pk).update(cp_open_at=None)
        response = self.patch_value()
        self.assertEqual(response.status_code, 403)

    def test_gate_closes_transitions_and_content_for_ies_only(self):
        Period.objects.filter(pk=self.period.pk).update(cp_open_at=None)
        self.period.refresh_from_db()
        force(self.group_a, 'cp_filling')
        force(self.axis_value, 'cp_filling')
        group = GroupResponse.objects.select_related(
            'observable_response__survey__period').get(pk=self.group_a.pk)
        self.assertTrue(validate_transition(
            self.ies_a, group, status('cp_postponed')))
        self.assertFalse(user_can_edit_flow_content(self.ies_a, group))
        # La revisora sigue transicionando lo que está en su turno.
        force(self.group_a, 'cp_completed')
        force(self.axis_value, 'cp_in_review')
        group.refresh_from_db()
        self.assertEqual(validate_transition(
            self.reviewer, group, status('cp_approved')), [])


class CaptureApiTests(CpCatalogTestCase):
    """Endpoints: alcance por institución, revisora solo lectura y el
    guardado por grupo promueve a `cp_filling`."""

    def group_url(self, group) -> str:
        return reverse('group_response-detail', args=[group.pk])

    def test_ies_only_sees_its_institution(self):
        self.client.force_authenticate(self.ies_b)
        response = self.client.get(
            reverse('axis_value-detail', args=[self.axis_value.pk]))
        self.assertEqual(response.status_code, 404)
        response = self.client.patch(
            self.group_url(self.group_b), {'b_responses': []}, format='json')
        self.assertEqual(response.status_code, 404)
        response = self.client.get(reverse('axis_value-list'))
        self.assertEqual(response.json()['total'], 1)

    def test_reviewer_reads_everything_but_writes_nothing(self):
        self.client.force_authenticate(self.reviewer)
        response = self.client.get(reverse('axis_value-list'))
        self.assertEqual(response.json()['total'], 2)
        response = self.client.get(
            reverse('axis_value-detail', args=[self.axis_value.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['observable_responses']), 3)
        response = self.client.patch(
            self.group_url(self.group_b), {'b_responses': []}, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['code'], 'reviewer_read_only')
        response = self.client.patch(
            reverse('observable_response-detail', args=[self.obs_response.pk]),
            {'value': True}, format='json')
        self.assertEqual(response.status_code, 403)

    def test_group_save_upserts_and_promotes(self):
        self.client.force_authenticate(self.ies_a)
        payload = {'b_responses': [{
            'question': self.bq.pk, 'academic_instances_complying': 2,
            'admin_instances_complying': 1}]}
        response = self.client.patch(
            self.group_url(self.group_b), payload, format='json')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'cp_filling')
        self.assertEqual(data['completion']['errors'], [])
        self.assertEqual(len(data['flow_events']), 1)
        # El estado propagado viaja en la misma respuesta.
        self.assertEqual(data['observable_status'], 'cp_filling')
        self.assertEqual(data['axis_status'], 'cp_filling')
        self.obs_response.refresh_from_db()
        self.axis_value.refresh_from_db()
        self.assertEqual(self.obs_response.status_id, 'cp_filling')
        self.assertEqual(self.axis_value.status_id, 'cp_filling')
        # Segundo guardado: actualiza la misma fila.
        payload['b_responses'][0]['academic_instances_complying'] = 4
        self.client.patch(self.group_url(self.group_b), payload, format='json')
        self.assertEqual(self.group_b.b_responses.count(), 1)
        self.assertEqual(
            self.group_b.b_responses.get().academic_instances_complying, 4)

    def test_group_rejects_wrong_type_and_foreign_question(self):
        self.client.force_authenticate(self.ies_a)
        response = self.client.patch(
            self.group_url(self.group_b),
            {'a_responses': [{'question': self.aq1.pk,
                              'selected_option': self.yes.pk}]},
            format='json')
        self.assertEqual(response.status_code, 400)
        response = self.client.patch(
            self.group_url(self.group_b),
            {'b_responses': [{'question': self.bq_special.pk,
                              'academic_instances_complying': 1}]},
            format='json')
        self.assertEqual(response.status_code, 400)

    def test_reach_not_focalized_only_where_offered(self):
        self.client.force_authenticate(self.ies_a)
        rq_plain = ReachQuestion.objects.create(
            observable=self.obs_std, text='Otra', has_general_planning=False)
        response = self.client.patch(
            self.group_url(self.group_reach),
            {'reach_responses': [{'question': rq_plain.pk,
                                  'not_focalized': True}]},
            format='json')
        self.assertEqual(response.status_code, 400)
        response = self.client.patch(
            self.group_url(self.group_reach),
            {'reach_responses': [{'question': self.rq.pk,
                                  'sectors': [self.main_sector.pk]}]},
            format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()['reach_responses'][0]['sectors'],
            [self.main_sector.pk])

    def test_group_not_editable_once_sent(self):
        force(self.axis_value, 'cp_sent')
        self.client.force_authenticate(self.ies_a)
        response = self.client.patch(
            self.group_url(self.group_b), {'b_responses': []}, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['code'], 'not_editable')

    def test_no_value_returns_tree_and_blocks_group_edit(self):
        self.client.force_authenticate(self.ies_a)
        response = self.client.patch(
            reverse('observable_response-detail', args=[self.obs_response.pk]),
            {'value': False}, format='json')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'cp_not_present')
        self.assertEqual(data['axis_status'], 'cp_filling')
        self.assertEqual(
            {g['status'] for g in data['group_responses']}, {'cp_not_present'})
        response = self.client.patch(
            self.group_url(self.group_b), {'b_responses': []}, format='json')
        self.assertEqual(response.status_code, 403)

    def test_axis_read_embeds_completion_per_group(self):
        self.answer_a_complete()
        self.gen_answer(self.gq_academic, 3)
        BResponse.objects.create(
            group_response=self.group_b, question=self.bq,
            academic_instances_complying=2, admin_instances_complying=1)
        self.client.force_authenticate(self.ies_a)
        with CaptureQueriesContext(connection) as ctx:
            response = self.client.get(
                reverse('axis_value-detail', args=[self.axis_value.pk]))
        self.assertEqual(response.status_code, 200)
        # La compuerta no consulta por grupo: el eje entero cabe en un
        # número fijo de queries (22 con este catálogo).
        self.assertLessEqual(len(ctx.captured_queries), 24)
        groups = {
            g['id']: g['completion']
            for o in response.json()['observable_responses']
            for g in o['group_responses']}
        self.assertEqual(groups[self.group_a.pk]['errors'], [])
        self.assertEqual(groups[self.group_b.pk]['errors'], [])
        self.assertIn(
            'Información base no declara instancias administrativas; el '
            'conteo no se pudo contrastar.',
            groups[self.group_b.pk]['warnings'])
        self.assertTrue(groups[self.group_reach.pk]['errors'])
