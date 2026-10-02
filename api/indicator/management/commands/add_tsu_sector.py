"""
Alta de «Alumnado de nivel técnico superior» (TSU) en el periodo 2025.

Rubén creó el sector desde el catálogo; aquí se completan sus banderas,
se precarga su presencia como «No» explícito en cada survey 2025 y se
agrega la pregunta de planes de estudio TSU precargada como «No
aplica». El «No» y el «No aplica» eximen la compuerta de completitud,
así que los grupos ya completos no se rompen; las IES que sí tienen el
nivel lo cambian en la revisión.

Idempotente: todo va por `get_or_create` y nunca pisa filas que ya
existan, así que correrlo de nuevo no crea ni cambia respuestas.
"""
from django.core.management.base import BaseCommand
from django.db import transaction

from indicator.models import GeneralGroup, Sector
from question.models import GeneralQuestion, ReachQuestion
from survey.models import GeneralQuestionResponse, Survey

SECTOR_NAME = "Alumnado de nivel técnico superior"
PERIOD_YEAR = 2025
PLANS_GROUP = "planes_estudio"
REACH_OBSERVABLE = "1.16"
TSU_QUESTION = {
    "name": "technical_plans",
    "text": "Planes de estudio vigentes de nivel técnico superior "
            "(TSU, profesional asociado)",
    "hint": "",
    "label": "",
    "unit": "planes",
    "q_type": "integer",
    "order": 2,
    "addl_config": {"allow_no_apply": True},
}
# El TSU entra en el segundo lugar; los demás se recorren.
PLANS_ORDER = {
    "media_plans": 1,
    "technical_plans": 2,
    "superior_plans": 3,
    "postgraduate_plans": 4,
}


class Command(BaseCommand):
    help = ("Completa el sector TSU y precarga su presencia («No») y su "
            "pregunta de planes («No aplica») en los surveys 2025.")

    def handle(self, *args, **kwargs) -> None:
        with transaction.atomic():
            sector = self.ensure_sector()
            surveys = list(Survey.objects.filter(period__year=PERIOD_YEAR))
            self.stdout.write(f"Surveys {PERIOD_YEAR}: {len(surveys)}")
            self.ensure_quantities(sector, surveys)
            question = self.ensure_question()
            self.ensure_responses(question, surveys)
            self.ensure_reach_list(sector)
        self.stdout.write(self.style.SUCCESS("Listo."))

    def ensure_sector(self) -> Sector:
        sector, created = Sector.objects.get_or_create(name=SECTOR_NAME)
        # Empata con medio superior (6): la lista de alcance ordena por
        # (order, id), así que el TSU, de id mayor, cae entre medio
        # superior y licenciatura.
        sector.order = 6
        sector.is_main = True
        sector.is_authority = False
        sector.is_standard_extra = False
        sector.is_ies_head = False
        sector.needs_name = False
        sector.save()
        verb = "creado" if created else "existente, banderas aseguradas"
        self.stdout.write(f"Sector id={sector.pk}: {verb}")
        return sector

    def ensure_quantities(self, sector: Sector, surveys: list) -> None:
        created = filled = 0
        for survey in surveys:
            row, was_created = survey.population_quantities.get_or_create(
                sector=sector, defaults={"is_present": False})
            created += was_created
            # Institution.save ya pudo crear la fila con presencia nula
            # (sector is_main); nula bloquea la compuerta, el «No» no.
            if not was_created and row.is_present is None:
                row.is_present = False
                row.save(update_fields=["is_present"])
                filled += 1
        self.stdout.write(
            f"PopulationQuantity: {created} creadas (is_present=False), "
            f"{filled} nulas puestas en False, "
            f"{len(surveys) - created - filled} ya respondidas")

    def ensure_question(self) -> GeneralQuestion:
        group = GeneralGroup.objects.get(pk=PLANS_GROUP)
        defaults = {
            key: value for key, value in TSU_QUESTION.items()
            if key != "name"}
        question, created = GeneralQuestion.objects.get_or_create(
            general_group=group, name=TSU_QUESTION["name"],
            defaults=defaults)
        reordered = 0
        for name, order in PLANS_ORDER.items():
            reordered += GeneralQuestion.objects.filter(
                general_group=group, name=name).exclude(
                order=order).update(order=order)
        verb = "creada" if created else "existente"
        self.stdout.write(
            f"GeneralQuestion {question.name} id={question.pk}: {verb}; "
            f"{reordered} preguntas reordenadas")
        return question

    def ensure_responses(self, question: GeneralQuestion,
                         surveys: list) -> None:
        created = 0
        for survey in surveys:
            _, was_created = GeneralQuestionResponse.objects.get_or_create(
                survey=survey, general_question=question,
                defaults={"no_apply": True})
            created += was_created
        self.stdout.write(
            f"GeneralQuestionResponse: {created} creadas (no_apply=True), "
            f"{len(surveys) - created} ya existían")

    def ensure_reach_list(self, sector: Sector) -> None:
        # La lista de alcance de 1.16 es fija (has_main_sectors=False):
        # no se arma desde is_main, así que el TSU hay que sumarlo a mano.
        questions = ReachQuestion.objects.filter(
            observable__number=REACH_OBSERVABLE, has_main_sectors=False)
        if not questions.exists():
            self.stdout.write(self.style.WARNING(
                f"ReachQuestion {REACH_OBSERVABLE}: no se encontró con "
                "lista propia; se omite"))
            return
        for question in questions:
            if question.others_sectors.filter(pk=sector.pk).exists():
                verb = "ya estaba"
            else:
                question.others_sectors.add(sector)
                verb = "sector agregado"
            self.stdout.write(
                f"ReachQuestion {REACH_OBSERVABLE}: {verb}")
