# Generated by Django 5.1.3 on 2024-11-27 23:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_recetas_descripcion'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecetaModificada',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_modificacion', models.DateTimeField(auto_now_add=True)),
                ('receta_ingrediente', models.ManyToManyField(to='core.recetaingrediente')),
                ('receta_original', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modificaciones', to='core.recetas')),
                ('usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.usuario')),
            ],
        ),
        migrations.AddField(
            model_name='pedido',
            name='receta_modificada',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.recetamodificada'),
        ),
    ]
