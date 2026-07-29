from django.core.management.base import BaseCommand
from django.db import transaction
from indicator.models import Axis


class Command(BaseCommand):
    help = (
        "Carga icon/color/short_name de Materias (Axis). "
        "load_questionnaire es el dueño de la jerarquía "
        "Axis/Component/Observable (name, description, order y demás "
        "textos del cuestionario); este comando solo aporta los "
        "metadatos visuales que load_questionnaire no toca."
    )

    # name solo aplica al crear (fallback si se corre antes de
    # load_questionnaire, que es el dueño de los nombres).
    AXES = [
        {"order": 1, "name": "Igualdad de género", "icon": "add",
         "color": "purple", "short_name": "Igualdad"},
        {"order": 2, "name": "Inclusión y no discriminación",
         "icon": "self_improvement", "color": "indigo",
         "short_name": "Inclusión"},
        {"order": 3, "name": "Cuidados corresponsables",
         "icon": "baby_changing_station", "color": "deep-purple",
         "short_name": "Cuidados"},
        {"order": 4,
         "name": "Una vida libre de discriminaciones y violencia",
         "icon": "volunteer_activism", "color": "pink",
         "short_name": "Vida libre"},
    ]

    def handle(self, *args, **kwargs) -> None:
        with transaction.atomic():
            for axis_data in self.AXES:
                axis, created = Axis.objects.get_or_create(
                    order=axis_data["order"],
                    defaults={"name": axis_data["name"]},
                )
                axis.icon = axis_data["icon"]
                axis.color = axis_data["color"]
                axis.short_name = axis_data["short_name"]
                axis.save(update_fields=[
                    "icon", "color", "short_name"])
                verb = "creado" if created else "actualizado"
                self.stdout.write(
                    self.style.SUCCESS(f"Eje {verb}: {axis.name}"))

