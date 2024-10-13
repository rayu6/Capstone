from django.shortcuts import render

# Create your views here.

# Vista para la página de inicio
def home(request):
    return render(request, 'home.html')  # Renderiza el template 'home.html'

# Vista para la página de login
def login(request):
    return render(request, 'login.html')  # Renderiza el template 'login.html'

# Vista para la página de login
def stock(request):
    return render(request, 'stock.html')  # Renderiza el template 'stock.html'

def register(request):
    return render(request, 'register.html')  # Renderiza el template 'stock.html'

def recetas(request):
    return render(request, 'recetas.html')  # Renderiza el template 'recetas.html'
    
def pedidos(request):
    return render(request, 'pedidos.html')  # Renderiza el template 'pedidos.html'