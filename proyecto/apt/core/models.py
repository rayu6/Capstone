from django.db import models

# Create your models here.
class Ingrediente(models.Model):
    nombre = models.CharField(max_length=100)
    cantidad = models.IntegerField()

    def __str__(self):
        return self.nombre

class receta_ingrediente(models.Model):
    ingrediente_id = models.IntegerField()

    def __str__(self):
        return self.ingrediente_id