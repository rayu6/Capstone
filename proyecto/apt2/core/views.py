from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Recetas,NombreReceta
from .models import Pedido, Ingrediente
# Create your views here.

# Vista para la página de inicio
def home(request):
    return render(request, 'core/home.html')  # Renderiza el template 'home.html'

# Vista para la página de login
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # Inicia sesión para el usuario autenticado
            return redirect('/')  # Redirige a la página de inicio o a donde quieras
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')  # Mensaje de error si las credenciales son incorrectas

    return render(request, 'registration/login.html')  # Renderiza el formulario de login

# Vista para la página de login
@login_required
def stock(request):
    return render(request, 'core/stock.html')  # Renderiza el template 'stock.html'

def register(request):
    return render(request, 'registration/register.html')  # Renderiza el template 'stock.html'

# Vista para listar recetas
@login_required
def listar_recetas(request):
    recetas = Recetas.objects.all()  # Obtener todas las recetas de la base de datos
    ingredientes = Ingrediente.objects.all()
    return render(request, 'core/recetas.html', {'recetas': recetas,'ingredientes': ingredientes})

def guardar_receta(request):
    if request.method == 'POST':
        nombre_receta = request.POST.get('nombre_receta')
        descripcion_receta = request.POST.get('descripcion_receta')
        ingredientes_seleccionados = request.POST.getlist('ingredientes.id') 

        # Crear receta
        nuevo_nombre = NombreReceta.objects.create(
            nombre=nombre_receta
        )
        
        nueva_receta = Recetas.objects.create(
            nombre_receta=nuevo_nombre,   
            descripcion=descripcion_receta
  
        )
        ingredientes = Ingrediente.objects.filter(id__in=ingredientes_seleccionados)
        nueva_receta.receta_ingrediente.set(ingredientes)  
        # Agregar los ingredientes
          # Asignar los ingredientes
        nuevo_nombre
        nueva_receta.save()

        # Redirigir 
        return redirect('listar_recetas')

    # Si no es POST, redirigir a algún lugar
    return redirect('listar_recetas')

@login_required 
def pedidos(request):
    return render(request, 'core/pedidos.html')  # Renderiza el template 'pedidos.html'
def prueba(request):
    return render(request, 'core/pruebaLogin.html')  # eliminar despues 

def logout_view(request):
    logout(request)
    return redirect('prueba')

@login_required
def listar_pedidos(request):
    pedidos = Pedido.objects.all()  # Obtén todos los pedidos de la base de datos
    return render(request, 'core/pedidos.html', {'pedidos': pedidos})   

def listar_ingredientes(request):
    ingredientes = Ingrediente.objects.all()  # Obtener todos los ingredientes
    return render(request, 'core/stock.html', {'ingredientes': ingredientes})