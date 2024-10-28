import logging
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages

from core.forms import UsuarioLoginForm
from .decorators import role_required
from .models import *

# Create your views here.
logger = logging.getLogger(__name__)

# Vista para la página de inicio
def home(request):
    return render(request, 'core/home.html')  # Renderiza el template 'home.html'

# Vista para la página de login
def login(request):
    logger.info("Vista login activada")
    if request.method == 'POST':
        logger.info("POST recibido en login")
        form = UsuarioLoginForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data['correo']
            password = form.cleaned_data['password']
            logger.info(f"Correo: {correo}, Password: {password}")

            try:
                usuario = Usuario.objects.get(correo=correo, hash_pass=password)
                logger.info(f"Usuario encontrado: {usuario.nombre}")
                # Almacena el ID del usuario y su rol en la sesión
                request.session['usuario_id'] = usuario.id
                request.session['role'] = usuario.role.nombre_role

                if usuario.role.nombre_role == 'usuario':
                    return redirect('homeUsuario')
            except Usuario.DoesNotExist:
                logger.warning("Usuario o contraseña incorrectos.")
                return HttpResponse("Correo o contraseña incorrectos.", status=401)
        else:
            logger.warning("Formulario no válido")
    return render(request, 'registration/login.html')  # Renderiza el formulario de lo

# Vista para la página de login
def stock(request):
    return render(request, 'core/stock.html')  # Renderiza el template 'stock.html'

def register(request):
    return render(request, 'registration/register.html')  # Renderiza el template 'stock.html'

# Vista para listar recetas
@role_required(allowed_roles=['admin', 'usuario'])
def listar_recetas(request):
    recetas = Recetas.objects.prefetch_related('receta_ingrediente__ingrediente').all()
    return render(request, 'core/recetas.html', {'recetas': recetas})

@role_required(allowed_roles=['usuario'])
def homeCliente(request):
    return render(request, 'core/users/homeCliente.html')  # Renderiza el template 'pedidos.html'

@role_required(allowed_roles=['usuario'])
def homeUsuario(request):
    return render(request, 'core/users/homeCliente.html')  # Renderiza el template 'pedidos.html'

def pedidos(request):
    return render(request, 'core/pedidos.html')  # Renderiza el template 'pedidos.html'
def prueba(request):
    return render(request, 'core/pruebaLogin.html')  # eliminar despues 

def logout_view(request):
    logout(request)
    return redirect('login')

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



