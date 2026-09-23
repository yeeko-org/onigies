"""
Sonda de la captura del cuestionario principal contra la base local.

Corre dentro de una transacción que se revierte al final: no deja rastro.
Uso (desde la raíz del repo):
    api/venv/bin/python api/manage.py shell -c "exec(open('api/.claude/smoke_cp_capture.py').read())"
Imprime ejemplos JSON reales para el contrato del frontend.
"""
import json

from django.db import transaction
from django.utils import timezone
from rest_framework.test import APIClient

from answer.models import GroupResponse, ObservableResponse
from flow.models import Status
from ies.models import Institution, Period, User
from survey.models import AxisValue


def show(label, response, limit=None):
    print(f'\n### {label} → {response.status_code}')
    text = json.dumps(response.json(), ensure_ascii=False, indent=1)
    print(text[:limit] if limit else text)


class Rollback(Exception):
    pass


try:
    with transaction.atomic():
        institution = Institution.objects.filter(
            is_test=False, users__isnull=False).first()
        ies_user = institution.users.first()
        reviewer = User.objects.filter(reviewer=True).first() \
            or User.objects.filter(is_superuser=True).first()
        period = Period.objects.order_by('-year').first()
        survey = institution.surveys.get(period=period)
        axis_value = survey.axis_values.order_by('axis__order').first()
        print('IES', institution.acronym, 'user', ies_user.username,
              'reviewer', reviewer.username, 'period', period.year,
              'axis_value', axis_value.pk)

        ies = APIClient()
        ies.force_authenticate(ies_user)
        rev = APIClient()
        rev.force_authenticate(reviewer)

        # Compuerta cerrada por fecha.
        r = ies.get(f'/api/axis_value/{axis_value.pk}/')
        print('cp_capture cerrado:', r.json()['cp_capture'])
        first_obs = r.json()['observable_responses'][0]
        r = ies.patch(f'/api/observable_response/{first_obs["id"]}/',
                      {'value': True}, format='json')
        show('PATCH value con compuerta cerrada (fecha)', r)

        period.cp_open_at = timezone.now()
        period.save()
        r = ies.patch(f'/api/observable_response/{first_obs["id"]}/',
                      {'value': True}, format='json')
        show('PATCH value con gen sin validar', r)

        survey.general_package.status_id = 'gen_finished'
        survey.general_package.save()

        r = ies.get(f'/api/axis_value/{axis_value.pk}/')
        data = r.json()
        print('cp_capture abierto:', data['cp_capture'])
        print('gen_denominators:', data['gen_denominators'])
        print('a_options:', data['a_options'])
        print('observables:', len(data['observable_responses']))
        obs0 = data['observable_responses'][0]
        print(json.dumps({k: v for k, v in data.items()
                          if k != 'observable_responses'},
                         ensure_ascii=False, indent=1))
        print('\n### observable_responses[0]')
        print(json.dumps(obs0, ensure_ascii=False, indent=1))

        # Booleano inicial: Sí.
        r = ies.patch(f'/api/observable_response/{obs0["id"]}/',
                      {'value': True}, format='json')
        show('PATCH value=True', r, 900)
        axis_value.refresh_from_db()
        print('axis status:', axis_value.status_id)

        # Grupo A: guardar respuestas.
        group_a = next(g for g in obs0['group_responses']
                       if g['question_type'] == 'a_questions')
        a_questions = obs0['observable_full']['a_questions']
        payload = {'a_responses': [
            {'question': q['id'], 'selected_option': 1}
            for q in a_questions[:-1]]}
        r = ies.patch(f'/api/group_response/{group_a["id"]}/',
                      payload, format='json')
        show('PATCH group A (incompleto)', r)

        # Completar con uno faltante → 400 del gancho.
        r = ies.post(
            f'/api/flow/answer/groupresponse/{group_a["id"]}/transitions/',
            {'target_status': 'cp_completed'}, format='json')
        show('transición cp_completed con faltante', r)

        payload = {'a_responses': [
            {'question': q['id'], 'selected_option': 2}
            for q in a_questions[-1:]]}
        ies.patch(f'/api/group_response/{group_a["id"]}/',
                  payload, format='json')
        r = ies.post(
            f'/api/flow/answer/groupresponse/{group_a["id"]}/transitions/',
            {'target_status': 'cp_completed'}, format='json')
        show('transición cp_completed completo', r)

        # Grupo B.
        group_b = next(g for g in obs0['group_responses']
                       if g['question_type'] == 'b_questions')
        bq = obs0['observable_full']['b_questions'][0]
        r = ies.patch(f'/api/group_response/{group_b["id"]}/',
                      {'b_responses': [{
                          'question': bq['id'],
                          'academic_instances_complying': 3,
                          'admin_instances_complying': 2}]},
                      format='json')
        show('PATCH group B', r, 1200)

        # Tipo equivocado.
        r = ies.patch(f'/api/group_response/{group_b["id"]}/',
                      {'a_responses': [{'question': a_questions[0]['id'],
                                        'selected_option': 1}]},
                      format='json')
        show('PATCH group B con a_responses', r)

        # Reach.
        group_r = next((g for g in obs0['group_responses']
                        if g['question_type'] == 'reach'), None)
        if group_r:
            rq = obs0['observable_full']['reach_questions'][0]
            r = ies.patch(f'/api/group_response/{group_r["id"]}/',
                          {'reach_responses': [{
                              'question': rq['id'],
                              'sectors': [s['id'] for s in rq['sectors'][:2]]}]},
                          format='json')
            show('PATCH group reach', r, 900)

        # «No» bloqueado: ya hay revisión? no; probamos el bloqueo por
        # revisión activa forzando un grupo a cp_approved.
        GroupResponse.objects.filter(pk=group_b['id']).update(
            status_id='cp_approved')
        r = ies.patch(f'/api/observable_response/{obs0["id"]}/',
                      {'value': False}, format='json')
        show('PATCH value=False con revisión activa', r)
        GroupResponse.objects.filter(pk=group_b['id']).update(
            status_id='cp_filling')

        r = ies.patch(f'/api/observable_response/{obs0["id"]}/',
                      {'value': False}, format='json')
        d = r.json()
        print('\n### PATCH value=False →', r.status_code, d['status'],
              [(g['question_type'], g['status']) for g in d['group_responses']],
              'a_responses conservadas:',
              len(next(g for g in d['group_responses']
                       if g['question_type'] == 'a_questions')['a_responses']))
        print('eventos observable:', [(e['from_status'], e['to_status'])
                                      for e in d['flow_events']])

        r = ies.patch(f'/api/observable_response/{obs0["id"]}/',
                      {'value': True}, format='json')
        d = r.json()
        print('### PATCH value=True (reabrir) →', r.status_code, d['status'],
              [(g['question_type'], g['status']) for g in d['group_responses']])

        # Revisora: lectura sí, escritura no.
        r = rev.get(f'/api/axis_value/{axis_value.pk}/')
        print('\nrevisora GET axis:', r.status_code)
        r = rev.patch(f'/api/group_response/{group_b["id"]}/',
                      {'b_responses': []}, format='json')
        show('revisora PATCH group', r)

        # Otra IES: 404.
        other = Institution.objects.filter(
            users__isnull=False).exclude(pk=institution.pk).first()
        if other:
            oc = APIClient()
            oc.force_authenticate(other.users.first())
            r = oc.get(f'/api/axis_value/{axis_value.pk}/')
            print('otra IES GET axis:', r.status_code)
            r = oc.patch(f'/api/group_response/{group_b["id"]}/',
                         {'b_responses': []}, format='json')
            print('otra IES PATCH group:', r.status_code)

        # Lista de ejes.
        r = ies.get('/api/axis_value/')
        show('GET /api/axis_value/ (IES)', r, 1500)

        # Login payload / survey.
        r = ies.get(f'/api/survey/{survey.pk}/')
        d = r.json()
        print('\n### survey retrieve: cp_capture', d['cp_capture'])
        print('axis_values[0]:', json.dumps(d['axis_values'][0],
                                            ensure_ascii=False))
        raise Rollback
except Rollback:
    print('\n(rollback)')
