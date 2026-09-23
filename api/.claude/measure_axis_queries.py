"""Sonda: queries y tiempo de GET /axis_value/<id>/ con la base local.

Uso (desde la raíz del repo): api/venv/bin/python api/.claude/measure_axis_queries.py [axis_value_id] [user_id]
"""
import os
import sys
import time

import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.db import connection, reset_queries  # noqa: E402
from django.test.utils import CaptureQueriesContext  # noqa: E402
from rest_framework.test import APIRequestFactory, force_authenticate  # noqa

from api.views.answer import AxisValueViewSet  # noqa: E402
from ies.models import User  # noqa: E402

axis_id = int(sys.argv[1]) if len(sys.argv) > 1 else 293
user_id = int(sys.argv[2]) if len(sys.argv) > 2 else 80
user = User.objects.get(pk=user_id)
view = AxisValueViewSet.as_view({'get': 'retrieve'})
factory = APIRequestFactory()


def run():
    request = factory.get(f'/api/axis_value/{axis_id}/')
    force_authenticate(request, user=user)
    reset_queries()
    with CaptureQueriesContext(connection) as ctx:
        start = time.perf_counter()
        response = view(request, pk=axis_id)
        response.render()
        elapsed = time.perf_counter() - start
    return response, len(ctx.captured_queries), elapsed, ctx


run()  # calentamiento (caches de ContentType, etc.)
response, n, elapsed, ctx = run()
data = response.data
groups = sum(len(o['group_responses']) for o in data['observable_responses'])
print(f'status={response.status_code} observables='
      f'{len(data["observable_responses"])} groups={groups}')
print(f'queries={n} time={elapsed * 1000:.0f}ms')
has_completion = all(
    'completion' in g for o in data['observable_responses']
    for g in o['group_responses'])
print(f'completion_in_groups={has_completion}')
if '-v' in sys.argv:
    for q in ctx.captured_queries:
        print(q['sql'][:160])
