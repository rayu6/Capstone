from django.db import models

# Create your models here.


class Role(models.Model):
    id = models.AutoField(primary_key=True)  # Clave primaria
    nombre_role = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre_role

class Usuario(models.Model):
    id = models.AutoField(primary_key=True)  # Clave primaria
    nombre = models.CharField(max_length=45)
    correo = models.EmailField(max_length=255, unique=True)
    hash_pass = models.CharField(max_length=45)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class TipoDeOrden(models.Model):
    id = models.AutoField(primary_key=True)  # Clave primaria
    nombre_tipo_de_orden = models.CharField(max_length=45)

    def __str__(self):
        return self.nombre_tipo_de_orden
    class Meta:
        verbose_name = "Tipo de orden"
        verbose_name_plural = "Tipo de orden"
class Estado(models.Model):
    id = models.AutoField(primary_key=True)  # Clave primaria
    nombre_estado = models.CharField(max_length=45)  # Añadí este campo ya que parece que falta en la imagen

    def __str__(self):
        return self.nombre_estado



class Pedido(models.Model):
    id = models.AutoField(primary_key=True)  # Clave primaria
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo_de_orden = models.ForeignKey(TipoDeOrden, on_delete=models.CASCADE)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    receta_pedido = models.ForeignKey('RecetaPedido', on_delete=models.CASCADE)


    

class Ingrediente(models.Model):
    id = models.AutoField(primary_key=True)  # Clave primaria
    unidades = models.CharField(max_length=255)
    nombre_ingrediente = models.ForeignKey('NombreIngrediente', on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_ingrediente.nombre
    
class RecetaIngrediente(models.Model):
    id = models.AutoField(primary_key=True)  # Clave primaria
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    unidad=models.CharField(max_length=100,null=False)
    ingrediente = models.ForeignKey('Ingrediente', on_delete=models.CASCADE,)
    
    def __str__(self):
         return f"{self.ingrediente.nombre_ingrediente.nombre} - {self.cantidad} -{self.unidad}"
    
class RecetaPedido(models.Model):
    id = models.AutoField(primary_key=True)  # Clave primaria
    recetas=models.ForeignKey('Recetas',on_delete=models.CASCADE)



class NombreIngrediente(models.Model):
    id = models.AutoField(primary_key=True)  # Clave primaria
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Recetas(models.Model):
    id = models.AutoField(primary_key=True)  # Clave primaria
    descripcion = models.CharField(max_length=255)
    link = models.CharField(max_length=255, null=True)
    nombre_receta = models.ForeignKey('NombreReceta', on_delete=models.CASCADE)
    
    receta_ingrediente = models.ManyToManyField(RecetaIngrediente)
    def __str__(self):
        return self.nombre_receta.nombre
    
    class Meta:
        verbose_name = "Recetas"
        verbose_name_plural = "Recetas"

class NombreReceta(models.Model):
    id = models.AutoField(primary_key=True)  # Clave primaria
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre
    
