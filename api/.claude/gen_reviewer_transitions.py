"""Diagnóstico: una revisora sin is_staff transiciona grupos y paquetes gen
por HTTP real (APIClient), dentro de una transacción que se revierte.

Uso (desde la raíz del repo):
    api/venv/bin/python api/manage.py shell -c "exec(open('api/.claude/gen_reviewer_transitions.py').read())"
"""
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework.test import APIClient

from survey.models import GeneralGroupResponse, GeneralPackage

User = get_user_model()
reviewer = User.objects.filter(
    reviewer=True, is_staff=False, is_superuser=False).first()
print('revisora:', reviewer.pk, reviewer.email, 'is_reviewer =',
      reviewer.is_reviewer)
client = APIClient()
client.force_authenticate(reviewer)


def post(model, pk, target, comment=''):
    url = f'/api/flow/survey/{model}/{pk}/transitions/'
    res = client.post(url, {'target_status': target, 'comment': comment},
                      format='json')
    body = getattr(res, 'data', None) or res.content[:300]
    return res.status_code, body


class Rollback(Exception):
    pass


CASES = [
    # (descripción, filtro de grupo, destino, comentario)
    ('grupo completado, paquete enviado → aprobar',
     dict(status_id='gen_completed', general_package__status_id='gen_sent'),
     'gen_approved', ''),
    ('grupo completado, paquete enviado → solicitar ajustes',
     dict(status_id='gen_completed', general_package__status_id='gen_sent'),
     'gen_need_changes', 'Prueba de diagnóstico'),
    ('grupo completado, paquete en borrador → aprobar (debe negarse)',
     dict(status_id='gen_completed', general_package__status_id='gen_draft'),
     'gen_approved', ''),
]

for label, filters, target, comment in CASES:
    group = GeneralGroupResponse.objects.filter(**filters).first()
    if group is None:
        print(f'- {label}: sin datos')
        continue
    try:
        with transaction.atomic():
            code, body = post('generalgroupresponse', group.pk, target,
                              comment)
            print(f'- {label} [grupo {group.pk}]: {code} {body}')
            raise Rollback
    except Rollback:
        pass

pkg = GeneralPackage.objects.filter(status_id='gen_sent').first()
for target, comment in [('gen_need_changes', 'Prueba'),
                        ('gen_finished', '')]:
    try:
        with transaction.atomic():
            code, body = post('generalpackage', pkg.pk, target, comment)
            print(f'- paquete {pkg.pk} gen_sent → {target}: {code} {body}')
            raise Rollback
    except Rollback:
        pass
