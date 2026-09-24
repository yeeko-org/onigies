"""
Backfill del árbol de captura cp: por cada `AxisValue` crea, si faltan,
sus `ObservableResponse` y `GroupResponse` con `provision_cp_responses`.

Existe para no usar `resave_institutions` en producción:
`Institution.save()` también corre `_preload_centralized` y reescribe
`is_centralized`, un efecto que un deploy no debe tener. Este comando
solo toca el árbol cp. Idempotente: una segunda corrida no crea nada.
También lleva a `cp_approved` los grupos sin captura que siguen en
`cp_pre_start` o `cp_filling` (`approve_groups_without_capture`): los
nuevos ya nacen así, los anteriores a la regla no.
Dry-run por omisión (corre dentro de una transacción que se revierte y
reporta lo que crearía); `--apply` persiste, como pide `deploy-api` para
los comandos re-ejecutables que escriben datos.
"""
from django.core.management.base import BaseCommand
from django.db import transaction

from answer.models import (
    GroupResponse, ObservableResponse, approve_groups_without_capture,
    provision_cp_responses)
from survey.models import AxisValue


class Command(BaseCommand):
    help = ("Crea los ObservableResponse y GroupResponse faltantes de cada "
            "AxisValue (idempotente; no re-guarda instituciones).")

    def add_arguments(self, parser) -> None:
        parser.add_argument('--institution', type=int, help='Id de Institution')
        parser.add_argument('--period', type=int, help='Año del Period')
        parser.add_argument(
            '--apply', action='store_true',
            help='Persiste; sin él, solo reporta lo que crearía.')

    def handle(self, *args, **options) -> None:
        axis_values = AxisValue.objects.select_related('survey')
        if options['institution'] is not None:
            axis_values = axis_values.filter(
                survey__institution_id=options['institution'])
        if options['period'] is not None:
            axis_values = axis_values.filter(
                survey__period_id=options['period'])
        survey_ids = axis_values.values('survey_id')
        counted = {
            'ObservableResponse': ObservableResponse.objects.filter(
                survey_id__in=survey_ids),
            'GroupResponse': GroupResponse.objects.filter(
                observable_response__survey_id__in=survey_ids),
        }
        before = {name: qs.count() for name, qs in counted.items()}

        total = 0
        with transaction.atomic():
            for axis_value in axis_values.iterator():
                provision_cp_responses(axis_value.survey, axis_value)
                total += 1
            after = {name: qs.count() for name, qs in counted.items()}
            approved = approve_groups_without_capture(
                counted['GroupResponse'])
            if not options['apply']:
                transaction.set_rollback(True)

        if not options['apply']:
            self.stdout.write(self.style.WARNING(
                "Dry-run: nada se guardó. Usa --apply para persistir."))

        self.stdout.write(f"AxisValue recorridos: {total}")
        for name in counted:
            created = after[name] - before[name]
            msg = f"{name}: creados {created}, existentes {before[name]}"
            self.stdout.write(self.style.SUCCESS(msg))
        self.stdout.write(self.style.SUCCESS(
            f"GroupResponse sin captura llevados a cp_approved: {approved}"))
