# Generated by Django 5.1.3 on 2024-12-12 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_recetas_pais_recetas_precio_recetas_tiempo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recetas',
            name='precio',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=8),
        ),
    ]