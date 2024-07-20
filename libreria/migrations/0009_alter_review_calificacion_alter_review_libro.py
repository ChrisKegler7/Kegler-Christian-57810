# Generated by Django 5.0.6 on 2024-07-16 00:48

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libreria', '0008_libro_sinopsis'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='calificacion',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='review',
            name='libro',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reseñas', to='libreria.libro'),
        ),
    ]