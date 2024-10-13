from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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

@login_required
def recetas(request):
    return render(request, 'core/recetas.html')  # Renderiza el template 'recetas.html'
@login_required 
def pedidos(request):
    return render(request, 'core/pedidos.html')  # Renderiza el template 'pedidos.html'
def prueba(request):
    return render(request, 'core/pruebaLogin.html')  # eliminar despues 

def logout_view(request):
    logout(request)
    return redirect('prueba')