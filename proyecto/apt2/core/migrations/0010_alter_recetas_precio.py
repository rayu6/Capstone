# Generated by Django 5.1.3 on 2024-12-12 23:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_alter_recetas_precio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recetas',
            name='precio',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]