# Generated by Django 5.0.6 on 2024-07-16 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libreria', '0011_orden_ordenitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='libro',
            name='precio',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
