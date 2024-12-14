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


    class Meta: 
        model = Pedido
        fields = ['usuario']

class UsuarioLoginForm(forms.Form):
    correo = forms.EmailField(label="Correo", max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)