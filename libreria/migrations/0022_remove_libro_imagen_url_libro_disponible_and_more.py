# Generated by Django 5.0.6 on 2024-07-20 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libreria', '0021_perfil_avatar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='libro',
            name='imagen_url',
        ),
        migrations.AddField(
            model_name='libro',
            name='disponible',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='libro',
            name='isbn',
            field=models.CharField(max_length=13),
        ),
        migrations.AlterField(
            model_name='libro',
            name='precio',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='libro',
            name='sinopsis',
            field=models.TextField(default='Sin sinopsis'),
        ),
    ]
