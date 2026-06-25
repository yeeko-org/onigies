"""
FK real ObservableResponse → AxisValue (padre del flujo cp).

Patrón canónico para un FK obligatorio sobre tabla con datos: se agrega
nullable, se rellena (cada respuesta toma el AxisValue de su survey cuyo
axis coincide con observable.component.axis) y se vuelve non-null. El
backfill es no-op si aún no hay respuestas.
"""
from django.db import migrations, models
import django.db.models.deletion


def backfill_axis_value(apps, schema_editor):
    AxisValue = apps.get_model('survey', 'AxisValue')
    ObservableResponse = apps.get_model('answer', 'ObservableResponse')

    av_map = {
        (av.survey_id, av.axis_id): av.id
        for av in AxisValue.objects.all()
    }
    to_update = []
    qs = ObservableResponse.objects.select_related('observable__component')
    for response in qs:
        axis_id = response.observable.component.axis_id
        av_id = av_map.get((response.survey_id, axis_id))
        if av_id is not None:
            response.axis_value_id = av_id
            to_update.append(response)
    ObservableResponse.objects.bulk_update(
        to_update, ['axis_value'], batch_size=500)


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0006_generalpackage_generalgroupresponse_general_package'),
        ('answer', '0002_groupresponse_status_observableresponse_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='observableresponse',
            name='axis_value',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='observable_responses',
                to='survey.axisvalue'),
        ),
        migrations.RunPython(
            backfill_axis_value, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='observableresponse',
            name='axis_value',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='observable_responses',
                to='survey.axisvalue'),
        ),
    ]
