from django.contrib import admin
from .models import Role, Usuario, TipoDeOrden, Estado, RecetaIngrediente, Pedido, RecetaPedido, Ingrediente, NombreIngrediente, Recetas, NombreReceta
# Register your models here.

admin.site.register(Role)
admin.site.register(Usuario)
admin.site.register(TipoDeOrden)
admin.site.register(Estado)
admin.site.register(RecetaIngrediente)
admin.site.register(Pedido)
admin.site.register(RecetaPedido)
admin.site.register(Ingrediente)
admin.site.register(NombreIngrediente)
admin.site.register(Recetas)
admin.site.register(NombreReceta)