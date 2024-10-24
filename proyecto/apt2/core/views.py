from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *

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
    recetas = Recetas.objects.prefetch_related('receta_ingrediente__ingrediente').all()
    return render(request, 'core/recetas.html', {'recetas': recetas})



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

def pedido_detalles(request,pedido_id):
    if request.method == 'POST':
        tipo_pedido = request.POST.get('tipo_orden')
        estado_pedido = request.POST.get('estado_pedido')
        receta_seleccionada = request.POST.get('id_receta')
        usuario_id = request.POST.get('id_usuario')

        nuevo_pedido = Pedido.objects.create(
            tipo_orden = tipo_pedido,
            estado = estado_pedido,
            receta_seleccionada = receta_seleccionada,
            usuario_id = usuario_id
        )
        nuevo_pedido.save() 

        return redirect('pedido_detalles', pedido_id = nuevo_pedido.id)
    
    return redirect('listar_pedidos')

def crear_pedido_view(request):
    recetas = Recetas.objects.all()
    usuarios = Usuario.objects.all()
    return render(request, 'crear_pedido.html', {'recetas': recetas, 'usuarios': usuarios})

def asignar_pedido(request,pedido_id):
    try:
        pedido = Pedido.objects.get(id = pedido_id)
    except pedido.DoesNotExist:
        return redirect('listar pedido')    
    if request.method == 'POST':
        pass
    return render(request, 'asignar_pedido.html',{'pedido': pedido})


def listar_ingredientes(request):
    ingredientes = Ingrediente.objects.all()  # Obtener todos los ingredientes
    return render(request, 'core/stock.html', {'ingredientes': ingredientes})
    
def guardar_ingrediente(request):
    if request.method == 'POST':
        nombre_ingrediente = request.POST.get('nombre_ingrediente')
        unidades = request.POST.get('unidades')
        cantidad = request.POST.get('cantidad')
        # Crear una nueva instancia de NombreIngrediente
        nuevo_nombre = NombreIngrediente.objects.create(nombre=nombre_ingrediente)

        # Guardar el nuevo ingrediente con la relación a NombreIngrediente
        Ingrediente.objects.create(nombre_ingrediente=nuevo_nombre, unidades=unidades, cantidad=cantidad)

    return redirect('stock')



