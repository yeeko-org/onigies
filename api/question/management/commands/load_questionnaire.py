"""Siembra idempotente del cuestionario 2026 completo.

Fuente de verdad: question/seed_data/ (transcrito de
docs/questions/all_questions_reduced.md). Re-correr el comando actualiza
textos y borra opciones/planes sobrantes; los ajustes hechos por admin se
pierden a propósito.

Prerrequisitos: load_sectors (sectores custom) y migrate_initial_data
(QuestionType). Supersede a load_main_axis para la jerarquía
Axis/Component/Observable (load_main_axis sigue siendo el dueño de
icon/color/short_name/hex_color).
"""
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from indicator.models import (
    Axis, Component, GeneralGroup, Observable, Sector)
from question.models import (
    AOption, AQuestion, BQuestion, PlanQuestion, ReachQuestion,
    SpecialQuestion)
from question.seed_data import ALL_AXES
from question.seed_data.catalogs import (
    A_OPTIONS, GENERAL_GROUPS, STANDARD_EXTRA_SECTORS)

EXPECTED_COUNTS = {1: 17, 2: 6, 3: 4, 4: 14}


class Command(BaseCommand):
    help = (
        "Carga el cuestionario 2026 completo: ejes, componentes, "
        "observables, preguntas A con opciones, preguntas de alcance, "
        "de transversalización (B), de planes, especiales, escala "
        "AOption y grupos generales."
    )

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            '--sync-institutions', action='store_true',
            help="Re-guarda cada Institution para generar los "
                 "GeneralGroupResponse de grupos nuevos en surveys "
                 "existentes.",
        )

    def handle(self, *args, **options) -> None:
        self._validate()
        with transaction.atomic():
            self._load_hierarchy()
            self._load_a_options()
            self._load_general_groups()
        if options['sync_institutions']:
            self._sync_institutions()
        else:
            self.stdout.write(self.style.WARNING(
                "Pendiente: correr con --sync-institutions para crear "
                "los GeneralGroupResponse en surveys existentes."))
        self.stdout.write(self.style.SUCCESS("Cuestionario cargado."))

    def _validate(self) -> None:
        """Falla antes de escribir si los datos están incompletos."""
        sector_names = set(
            Sector.objects.values_list('name', flat=True))
        missing_sectors = set(STANDARD_EXTRA_SECTORS) - sector_names
        for axis_data in ALL_AXES:
            numbers = []
            for comp in axis_data["components"]:
                for obs in comp["observables"]:
                    numbers.append(obs["number"])
                    reach = obs["reach"]
                    if reach and reach["populations"] != "standard":
                        missing_sectors |= (
                            set(reach["populations"]) - sector_names)
            expected = EXPECTED_COUNTS[axis_data["order"]]
            if len(numbers) != expected or len(set(numbers)) != expected:
                raise CommandError(
                    f"Eje {axis_data['order']}: se esperaban {expected} "
                    f"observables únicos, hay {len(numbers)}.")
        if missing_sectors:
            raise CommandError(
                "Sectores inexistentes (¿corriste load_sectors?): "
                f"{sorted(missing_sectors)}")

    def _load_hierarchy(self) -> None:
        created = updated = 0
        order = 0
        for axis_data in ALL_AXES:
            # No se tocan icon/color/short_name: los definió
            # load_main_axis y no vienen en el cuestionario.
            axis, _ = Axis.objects.update_or_create(
                order=axis_data["order"],
                defaults={
                    "name": axis_data["name"],
                    "description": axis_data["description"],
                },
            )
            for comp_data in axis_data["components"]:
                component, _ = Component.objects.get_or_create(
                    axis=axis, name=comp_data["name"])
                for obs_data in comp_data["observables"]:
                    order += 1
                    was_new = self._load_observable(
                        component, obs_data, order)
                    created += was_new
                    updated += not was_new
        self.stdout.write(
            f"Observables: {created} creados, {updated} actualizados.")

    def _load_observable(
            self, component: Component, obs_data: dict,
            order: int) -> bool:
        # Clave (component, number): number es el string del seed («1.1»,
        # «1.10» no colisionan porque nunca coexisten en el mismo
        # componente; ver PLAN_seed_cuestionario.md).
        observable, created = Observable.objects.update_or_create(
            component=component,
            number=obs_data["number"],
            defaults={
                "order": order,
                "name": obs_data["name"],
                "description": obs_data["description"],
                "init_question": obs_data["init_question"],
                "a_main_question": obs_data["a_main_question"],
                "reach_instances_question":
                    obs_data["reach_instances_question"],
            },
        )
        for index, text in enumerate(obs_data["a_options"], start=1):
            AQuestion.objects.update_or_create(
                observable=observable, order=index,
                defaults={"text": text},
            )
        stale = AQuestion.objects.filter(
            observable=observable, order__gt=len(obs_data["a_options"]))
        if stale.exists():
            self.stdout.write(self.style.WARNING(
                f"{obs_data['number']}: borrando {stale.count()} "
                "AQuestion sobrantes."))
            stale.delete()
        self._load_reach(observable, obs_data)
        self._load_b_question(observable, obs_data)
        self._load_plan_questions(observable, obs_data)
        self._load_special_question(observable, obs_data)
        return created

    def _load_reach(self, observable: Observable, obs_data: dict) -> None:
        reach = obs_data["reach"]
        if reach is None:
            # Caso especial diferido (ver PLAN_seed_cuestionario.md):
            # no se crea ReachQuestion todavía.
            return
        standard = reach["populations"] == "standard"
        question, _ = ReachQuestion.objects.update_or_create(
            observable=observable,
            defaults={
                "text": reach["text"],
                "has_main_sectors": standard,
                "has_general_planning": obs_data["has_general_planning"],
            },
        )
        # POB-ESTÁNDAR = sectores is_main + los 2 extra; las listas
        # custom van completas en others_sectors (has_main_sectors=False).
        names = (STANDARD_EXTRA_SECTORS if standard
                 else reach["populations"])
        question.others_sectors.set(
            Sector.objects.filter(name__in=names))

    def _load_b_question(
            self, observable: Observable, obs_data: dict) -> None:
        text = obs_data["reach_instances_question"]
        if not text:
            return
        includes_academic, includes_admin = obs_data.get(
            "b_includes", (True, True))
        BQuestion.objects.update_or_create(
            observable=observable, order=1,
            defaults={
                "text": text,
                "includes_academic": includes_academic,
                "includes_admin": includes_admin,
            },
        )

    def _load_plan_questions(
            self, observable: Observable, obs_data: dict) -> None:
        plan_questions = obs_data.get("plan_questions", [])
        for plan_data in plan_questions:
            PlanQuestion.objects.update_or_create(
                observable=observable, order=plan_data["order"],
                defaults={"text": plan_data["text"]},
            )
        stale = PlanQuestion.objects.filter(
            observable=observable, order__gt=len(plan_questions))
        if stale.exists():
            self.stdout.write(self.style.WARNING(
                f"{obs_data['number']}: borrando {stale.count()} "
                "PlanQuestion sobrantes."))
            stale.delete()

    def _load_special_question(
            self, observable: Observable, obs_data: dict) -> None:
        special_questions = obs_data.get("special_questions", [])
        if not special_questions:
            return
        # Una sola SpecialQuestion por observable (sin clave order propia).
        SpecialQuestion.objects.update_or_create(
            observable=observable,
            defaults={"text": special_questions[0]["text"]},
        )

    def _load_a_options(self) -> None:
        for option in A_OPTIONS:
            AOption.objects.update_or_create(
                value=option["value"], defaults={"text": option["text"]})

    def _load_general_groups(self) -> None:
        for group in GENERAL_GROUPS:
            GeneralGroup.objects.update_or_create(
                name=group["name"],
                defaults={
                    "public_name": group["public_name"],
                    "is_population": group["is_population"],
                    "fields": group["fields"],
                },
            )
        self.stdout.write(
            f"Grupos generales: {len(GENERAL_GROUPS)} asegurados.")

    def _sync_institutions(self) -> None:
        from ies.models import Institution
        total = 0
        for institution in Institution.objects.all():
            institution.save()
            total += 1
        self.stdout.write(
            f"Instituciones re-guardadas: {total} (GeneralGroupResponse "
            "asegurados).")
