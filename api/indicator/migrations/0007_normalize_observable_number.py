# Generated manually — normaliza Observable.number tras el cast a texto.
from decimal import Decimal, InvalidOperation

from django.db import migrations


def normalize_observable_numbers(apps, schema_editor) -> None:
    """Reescribe number con el string exacto del seed.

    En Postgres el cast numeric(4,2) -> texto produce "1.10", "4.70",
    etc., que no coinciden con los strings del seed ("1.1", "4.7"). El
    desambiguador es el componente (dentro de un mismo componente nunca
    coexisten dos observables con el mismo Decimal).
    """
    from question.seed_data import ALL_AXES

    Observable = apps.get_model('indicator', 'Observable')

    seed_map = {}
    for axis_data in ALL_AXES:
        for comp_data in axis_data['components']:
            key = (axis_data['order'], comp_data['name'])
            seed_map[key] = {
                Decimal(obs_data['number']): obs_data['number']
                for obs_data in comp_data['observables']
            }

    observables = Observable.objects.select_related(
        'component', 'component__axis')
    for observable in observables:
        try:
            db_decimal = Decimal(observable.number)
        except InvalidOperation:
            print(
                f"WARNING: observable id={observable.id} number="
                f"{observable.number!r} no es numérico; se deja como está."
            )
            continue
        key = (observable.component.axis.order, observable.component.name)
        seed_string = seed_map.get(key, {}).get(db_decimal)
        if seed_string is not None:
            new_value = seed_string
        else:
            new_value = observable.number.rstrip('0').rstrip('.')
            print(
                f"WARNING: observable id={observable.id} number="
                f"{observable.number!r} sin match en el seed "
                f"(componente {key}); normalizado a {new_value!r}."
            )
        if new_value != observable.number:
            observable.number = new_value
            observable.save(update_fields=['number'])


class Migration(migrations.Migration):

    dependencies = [
        ('indicator', '0006_alter_observable_options_observable_order_and_more'),
    ]

    operations = [
        migrations.RunPython(
            normalize_observable_numbers, migrations.RunPython.noop),
    ]
