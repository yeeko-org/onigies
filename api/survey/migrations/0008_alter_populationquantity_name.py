from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0007_alter_axisvalue_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='populationquantity',
            name='name',
            field=models.CharField(
                blank=True, max_length=255, null=True,
                verbose_name='Nombre del sector'),
        ),
    ]
