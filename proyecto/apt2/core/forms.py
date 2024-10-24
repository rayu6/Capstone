from django import forms
from .models import Recetas, RecetaIngrediente, NombreReceta, Ingrediente, Pedido

class RecetasForm(forms.ModelForm):
    class Meta:
        model = Recetas
        fields = ['descripcion', 'link', 'nombre_receta']

class RecetaIngredienteForm(forms.ModelForm):
    class Meta:
        model = RecetaIngrediente
        fields = ['ingrediente', 'cantidad', 'unidad']

class AsignarPedidoForm(forms.ModelForm):
    usuario_asignado = forms.ModelChoiceField(queryset=User.objects.all(), required= True)

    class Meta: 
        model = Pedido
        fields = ['usuario']
