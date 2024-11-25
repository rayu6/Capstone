from django.db import models

# Create your models here.

class Role(models.Model):
    id = models.AutoField(primary_key=True)  
    nombre_role = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre_role

class Usuario(models.Model):
    id = models.AutoField(primary_key=True) 
    nombre = models.CharField(max_length=45)
    correo = models.EmailField(max_length=255, unique=True)
    hash_pass = models.CharField(max_length=45)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class TipoDeOrden(models.Model):
    id = models.AutoField(primary_key=True)  
    nombre_tipo_de_orden = models.CharField(max_length=45)

    def __str__(self):
        return self.nombre_tipo_de_orden
    class Meta:
        verbose_name = "Tipo de orden"
        verbose_name_plural = "Tipo de orden"
class Estado(models.Model):
    id = models.AutoField(primary_key=True)  
    nombre_estado = models.CharField(max_length=45)  

    def __str__(self):
        return self.nombre_estado



class Pedido(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo_de_orden = models.ForeignKey(TipoDeOrden, on_delete=models.CASCADE)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    receta_pedido = models.ForeignKey('RecetaPedido', on_delete=models.CASCADE)

    def descontar_ingredientes_del_stock(self):
        receta_pedido = self.receta_pedido
        
        # recorrer ingredientes
        for receta_ingrediente in receta_pedido.recetas.receta_ingrediente.all():
            ingrediente = receta_ingrediente.ingrediente
            cantidad_usada = receta_ingrediente.cantidad 
            
            # descontar cantidad de stock, validar que no sobrepase el limite
            if ingrediente.cantidad >= cantidad_usada:
                ingrediente.cantidad -= cantidad_usada
                ingrediente.save()
            else:
                raise ValueError(f"No hay suficiente stock de {ingrediente.nombre_ingrediente.nombre}.")
    
    # sobrescribir el metodo save para descontar ingredientes despues de crear el pedido
    def save(self, *args, **kwargs):
        # Guardar el pedido
        super().save(*args, **kwargs)
        
        # aplicar fucnion descontar 
        self.descontar_ingredientes_del_stock()

    def __str__(self):
        return self.receta_pedido.recetas.nombre_receta.nombre


    

class Ingrediente(models.Model):
    id = models.AutoField(primary_key=True)  # Clave primaria
    unidades = models.CharField(max_length=255)
    cantidad = models.IntegerField(null=False, default=0)
    nombre_ingrediente = models.ForeignKey('NombreIngrediente', on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_ingrediente.nombre
    
class RecetaIngrediente(models.Model):
    id = models.AutoField(primary_key=True)  
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    unidad=models.CharField(max_length=100,null=False)
    ingrediente = models.ForeignKey('Ingrediente', on_delete=models.CASCADE,)
    
    def __str__(self):
        return f"{self.ingrediente.nombre_ingrediente.nombre} - {self.cantidad} - {self.unidad}"
    
class RecetaPedido(models.Model):
    id = models.AutoField(primary_key=True)  
    recetas=models.ForeignKey('Recetas',on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.recetas.nombre_receta}"
    

class NombreIngrediente(models.Model):
    id = models.AutoField(primary_key=True)  
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Recetas(models.Model):
    id = models.AutoField(primary_key=True) 
    descripcion = models.TextField()
    link = models.ImageField(upload_to='imagenes_recetas/', null=True, blank=True)
    nombre_receta = models.ForeignKey('NombreReceta', on_delete=models.CASCADE)
    receta_ingrediente = models.ManyToManyField(RecetaIngrediente)
    
    def __str__(self):
        return str(self.nombre_receta.nombre)  
    
    class Meta:
        verbose_name = "Recetas"
        verbose_name_plural = "Recetas"

class NombreReceta(models.Model):
    id = models.AutoField(primary_key=True)  
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre
    
