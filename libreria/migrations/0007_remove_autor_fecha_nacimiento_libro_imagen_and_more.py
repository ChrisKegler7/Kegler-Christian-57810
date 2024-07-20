# Generated by Django 5.0.6 on 2024-07-13 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libreria', '0006_libro_imagen_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='autor',
            name='fecha_nacimiento',
        ),
        migrations.AddField(
            model_name='libro',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='libros/'),
        ),
        migrations.AlterField(
            model_name='libro',
            name='imagen_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]