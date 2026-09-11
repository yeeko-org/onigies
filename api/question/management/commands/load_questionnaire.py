"""Siembra idempotente del cuestionario 2026 completo.

Fuente de verdad de la *estructura*: question/seed_data/ (transcrito de
docs/reference/cuestionario-2026-reducido.md). De los *textos* manda el
dashboard: el re-seed solo los escribe al crear la fila, salvo que se corra
con --overwrite-texts. Los textos de Axis y Component nunca se reescriben,
ni con la bandera: los edita el equipo del observatorio.

Prerrequisitos: load_sectors (sectores custom) y migrate_initial_data
(QuestionType). Supersede a load_main_axis para la jerarquía
Axis/Component/Observable (load_main_axis sigue siendo el dueño de
icon/color/short_name/hex_color).
"""
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from indicator.models import (
    Axis, Component, GeneralGroup, Observable, Sector)
from question.models import (
    AOption, AQuestion, BQuestion, GeneralQuestion, ObservableQuestionType,
    PlanQuestion, QuestionType, QuestionnaireSettings, ReachQuestion,
    SpecialQuestion)
from question.seed_data import ALL_AXES
from question.seed_data.catalogs import (
    A_OPTIONS, GENERAL_GROUPS, STANDARD_EXTRA_SECTORS)

EXPECTED_COUNTS = {1: 17, 2: 6, 3: 4, 4: 14}


class Command(BaseCommand):
    help = (
        "Carga el cuestionario 2026 completo: ejes, componentes, "
        "observables, preguntas A con opciones, preguntas de alcance, "
        "de transversalidad orgánica (B), de planes, especiales, escala "
        "AOption y grupos generales."
    )

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            '--sync-institutions', action='store_true',
            help="Re-guarda cada Institution para generar los "
                 "GeneralGroupResponse de grupos nuevos en surveys "
                 "existentes.",
        )
        parser.add_argument(
            '--overwrite-texts', action='store_true',
            help="Reescribe los textos de observables y preguntas con "
                 "los del seed, pisando lo editado desde el dashboard.",
        )
        parser.add_argument(
            '--force', action='store_true',
            help="Resiembra aunque el cuestionario ya se haya sembrado "
                 "(ignora el candado de `seeded_at`).",
        )

    def handle(self, *args, **options) -> None:
        self.overwrite_texts = options['overwrite_texts']
        settings_row = self._check_seed_lock(options['force'])
        self.type_names = set(
            QuestionType.objects.values_list('name', flat=True))
        self.required_types = set(
            QuestionType.objects.filter(required=True)
            .values_list('name', flat=True))
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
        settings_row.seeded_at = timezone.now()
        settings_row.save()
        self.stdout.write(self.style.SUCCESS("Cuestionario cargado."))

    def _check_seed_lock(self, force: bool) -> QuestionnaireSettings:
        """El instrumento se siembra una vez: después manda el dashboard
        y una resiembra devolvería la estructura al estado del seed."""
        settings_row = QuestionnaireSettings.load()
        if settings_row.seeded_at and not force:
            fecha = timezone.localtime(
                settings_row.seeded_at).strftime('%d/%m/%Y %H:%M')
            raise CommandError(
                f"El cuestionario ya se sembró el {fecha}. Resembrar "
                "pisaría la estructura editada desde el dashboard; si "
                "de veras hace falta, corre con --force.")
        return settings_row

    def _text_defaults(self, texts: dict) -> dict:
        """Textos que van en `defaults`: ninguno, salvo con la bandera."""
        return texts if self.overwrite_texts else {}

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
        self._validate_hierarchy_keys()

    def _validate_hierarchy_keys(self) -> None:
        # Axis.order y Component.name son las claves naturales del seed y
        # se editan desde el dashboard: un rename duplicaría el árbol
        # entero (componentes, observables y preguntas) en vez de
        # actualizarlo.
        renamed = []
        for axis_data in ALL_AXES:
            axis = Axis.objects.filter(order=axis_data["order"]).first()
            if axis is None or not axis.component_set.exists():
                continue
            names = set(axis.component_set.values_list('name', flat=True))
            missing = {
                comp["name"] for comp in axis_data["components"]
            } - names
            if missing:
                renamed.append(
                    f"eje {axis_data['order']}: faltan {sorted(missing)}; "
                    f"existen {sorted(names)}")
        if renamed:
            raise CommandError(
                "Componentes renombrados desde el dashboard; corrige el "
                "seed o el nombre antes de resembrar:\n"
                + "\n".join(renamed))

    def _load_hierarchy(self) -> None:
        created = updated = 0
        order = 0
        for axis_data in ALL_AXES:
            # No se tocan icon/color/short_name: los definió
            # load_main_axis y no vienen en el cuestionario.
            axis, _ = Axis.objects.update_or_create(
                order=axis_data["order"],
                defaults={},
                create_defaults={
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
        # componente; ver el registro del seed del cuestionario).
        texts = {
            "name": obs_data["name"],
            "description": obs_data["description"],
            "init_question": obs_data["init_question"],
            "a_main_question": obs_data["a_main_question"],
            "a_main_subtitle": obs_data.get("a_main_subtitle"),
        }
        observable, created = Observable.objects.update_or_create(
            component=component,
            number=obs_data["number"],
            defaults={"order": order, **self._text_defaults(texts)},
            create_defaults={"order": order, **texts},
        )
        for index, text in enumerate(obs_data["a_options"], start=1):
            AQuestion.objects.update_or_create(
                observable=observable, order=index,
                defaults=self._text_defaults({"text": text}),
                create_defaults={"text": text},
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
        self._load_type_weights(observable, obs_data)
        return created

    def _load_reach(self, observable: Observable, obs_data: dict) -> None:
        reach = obs_data["reach"]
        if reach is None:
            # Caso especial diferido (ver el registro del seed del cuestionario):
            # no se crea ReachQuestion todavía.
            return
        standard = reach["populations"] == "standard"
        structure = {
            "has_main_sectors": standard,
            "has_general_planning": obs_data["has_general_planning"],
        }
        text = {"text": reach["text"]}
        question, _ = ReachQuestion.objects.update_or_create(
            observable=observable,
            defaults={**structure, **self._text_defaults(text)},
            create_defaults={**structure, **text},
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
        structure = {
            "includes_academic": includes_academic,
            "includes_admin": includes_admin,
        }
        BQuestion.objects.update_or_create(
            observable=observable, order=1,
            defaults={**structure, **self._text_defaults({"text": text})},
            create_defaults={**structure, "text": text},
        )

    def _load_plan_questions(
            self, observable: Observable, obs_data: dict) -> None:
        plan_questions = obs_data.get("plan_questions", [])
        for plan_data in plan_questions:
            text = {"text": plan_data["text"]}
            PlanQuestion.objects.update_or_create(
                observable=observable, order=plan_data["order"],
                defaults=self._text_defaults(text),
                create_defaults=text,
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
        text = {"text": special_questions[0]["text"]}
        SpecialQuestion.objects.update_or_create(
            observable=observable,
            defaults=self._text_defaults(text),
            create_defaults=text,
        )

    def _load_type_weights(
            self, observable: Observable, obs_data: dict) -> None:
        """Solo crea: la ponderación es del cliente y el dashboard pudo
        ampliar la aplicabilidad, así que ni se pisa `weight` ni se
        borran filas que el seed no conoce."""
        applicable = set(self.required_types)
        if obs_data["reach"] is not None:
            applicable.add('reach')
        if obs_data.get("plan_questions"):
            applicable.add('plans')
        if obs_data.get("special_questions"):
            applicable.add('special')
        if obs_data.get("population"):
            applicable.add('population')
        for name in sorted(applicable & self.type_names):
            ObservableQuestionType.objects.get_or_create(
                observable=observable, question_type_id=name)

    def _load_a_options(self) -> None:
        for option in A_OPTIONS:
            AOption.objects.update_or_create(
                value=option["value"], defaults={"text": option["text"]})

    def _load_general_groups(self) -> None:
        total_questions = 0
        for index, group in enumerate(GENERAL_GROUPS, start=1):
            # Los textos solo se siembran al crear: en filas existentes
            # el re-seed asegura estructura y respeta la redacción que
            # el cliente haya editado desde el catálogo.
            general_group, _ = GeneralGroup.objects.update_or_create(
                name=group["name"],
                defaults={
                    "is_population": group["is_population"],
                    "order": index,
                },
                create_defaults={
                    "is_population": group["is_population"],
                    "order": index,
                    "public_name": group["public_name"],
                    "title": group["title"],
                    "subtitle": group["subtitle"],
                    "instruction": group["instruction"],
                },
            )
            total_questions += self._load_general_questions(
                general_group, group["questions"])
        self.stdout.write(
            f"Grupos generales: {len(GENERAL_GROUPS)} asegurados, "
            f"{total_questions} preguntas.")

    def _load_general_questions(
            self, general_group: GeneralGroup, questions: list) -> int:
        """Clave natural (general_group, name): la clave estable es
        `name`, así que reescribir la redacción no duplica la fila.

        Los textos (text, hint, label, unit) solo se siembran al crear; en
        filas existentes el re-seed asegura estructura y respeta lo que
        el cliente haya editado desde el catálogo. `q_type`, `order` y
        `addl_config` sí se reescriben: anclan comportamiento que vive
        en código y no son editables.
        """
        names = [question["name"] for question in questions]
        for question in questions:
            structure = {
                "q_type": question.get("q_type", "integer"),
                "order": question["order"],
                "addl_config": question.get("addl_config", {}),
            }
            GeneralQuestion.objects.update_or_create(
                general_group=general_group, name=question["name"],
                defaults=structure,
                create_defaults={
                    **structure,
                    "text": question["text"],
                    "hint": question.get("hint", ""),
                    "label": question.get("label", ""),
                    "unit": question.get("unit", ""),
                },
            )
        stale = GeneralQuestion.objects.filter(
            general_group=general_group).exclude(name__in=names)
        if stale.exists():
            self.stdout.write(self.style.WARNING(
                f"{general_group.name}: borrando {stale.count()} "
                "GeneralQuestion sobrantes."))
            stale.delete()
        return len(questions)

    def _sync_institutions(self) -> None:
        from ies.models import Institution
        total = 0
        for institution in Institution.objects.all():
            institution.save()
            total += 1
        self.stdout.write(
            f"Instituciones re-guardadas: {total} (GeneralGroupResponse "
            "asegurados).")
