import logging
from django.http import HttpResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.db import transaction
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required



from core.forms import UsuarioLoginForm
from .decorators import role_required
from .models import *

# Create your views here.
logger = logging.getLogger(__name__)

# Vista para la página de inicio
def home(request):
    return render(request, 'core/home.html')  # Renderiza el template 'home.html'

# Vista para la página de login
@role_required(allowed_roles=[None])
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
                messages.success(request, "Has iniciado Sesion de forma exitosa ")

                if usuario.role.nombre_role == 'cocinero':
                    return redirect('homeUsuario')
                elif usuario.role.nombre_role == 'cliente':
                    return redirect('homeCliente')
                elif usuario.role.nombre_role != 'cliente':
                    return redirect(home)
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
@role_required(allowed_roles=['admin', 'usuario','cocinero'])
def listar_recetas(request):
    recetas = Recetas.objects.prefetch_related('receta_ingrediente__ingrediente').all()
    return render(request, 'core/recetas.html', {'recetas': recetas})

@role_required(allowed_roles=['cliente'])
def homeCliente(request):
    return render(request, 'core/users/homeCliente.html')  # Renderiza el template 'pedidos.html'

@role_required(allowed_roles=['cocinero'])
def homeUsuario(request):
    return render(request, 'core/users/homeUsuario.html')  # Renderiza el template 'pedidos.html'

def pedidos(request):
    return render(request, 'core/pedidos.html')  # Renderiza el template 'pedidos.html'
@role_required(allowed_roles=[])
def prueba(request):
    return render(request, 'core/pruebaLogin.html')  # eliminar despues 

def logout_view(request):
    logout(request)
    messages.success(request, "Has Cerrado Sesion de forma exitosa")    
    return redirect('login')
  

def listar_pedidos2(request):
    pedidos = Pedido.objects.all()
    pedido= pedido.objects.filter(id) # Obtén todos los pedidos de la base de datos
    return render(request, 'core/pedidos.html', {'pedidos': pedidos})   


def listar_pedidos(request):
    pedidos = Pedido.objects.all()  # Trae todos los pedidos

    # Obtener el id del pedido desde el parámetro GET
    pedido_id = request.GET.get('pedido_id')

    pedido = None
    if pedido_id:
        # Filtra el pedido con el id pasado como parámetro
        pedido = get_object_or_404(Pedido, id=pedido_id)

    return render(request, 'core/pedidos.html', {
        'pedidos': pedidos,
        'pedido': pedido,  # Si hay un pedido con el id solicitado, lo pasa a la plantilla
    })

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


@role_required(allowed_roles=['cocinero','admin'])
def listar_ingredientes(request):
    ingredientes = Ingrediente.objects.all()  # Obtener todos los ingredientes
    return render(request, 'core/stock.html', {'ingredientes': ingredientes})

@role_required(allowed_roles=['cocinero','admin'])
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

@role_required(allowed_roles=['admin'])
def crear_receta(request):
    if request.method == 'POST':
        pass
    return render(request, 'core/crearreceta.html')

@role_required(allowed_roles=['admin'])
def ingredientes_receta(request):
    # Obtener todos los ingredientes
    ingredientes = Ingrediente.objects.all()

    # Enviar los ingredientes al formulario de creación de recetas
    context = {
        'ingredientes': ingredientes
    }
    return render(request, 'core/crearreceta.html', context)


@role_required(allowed_roles=['admin'])
def guardar_receta(request):
    if request.method == 'POST':
        nombre_receta = request.POST.get('nombre_receta')  # El nombre de la receta desde el formulario
        descripcion = request.POST.get('descripcion_receta')

        # Obtener o crear la instancia de NombreReceta
        nombre_receta_obj, created = NombreReceta.objects.get_or_create(nombre=nombre_receta)

        # Ahora puedes crear la receta con la instancia de NombreReceta
        receta = Recetas(nombre_receta=nombre_receta_obj, descripcion=descripcion)
        receta.save()

        ingredientes_ids = request.POST.getlist('ingredientes')
        cantidades = request.POST.getlist('cantidad')
        unidades = request.POST.getlist('unidad')

        with transaction.atomic():
            for ingrediente_id, cantidad, unidad in zip(ingredientes_ids, cantidades, unidades):
                if cantidad:  # Verifica que haya una cantidad válida
                    ingrediente = Ingrediente.objects.get(id=ingrediente_id)
                    receta_ingrediente = RecetaIngrediente(
                        ingrediente=ingrediente,
                        cantidad=cantidad,
                        unidad=unidad
                    )
                    receta_ingrediente.save()

        return redirect('listar_recetas')  # Redirige a la vista que desees
    else:
        ingredientes = Ingrediente.objects.all()
        return render(request, 'core/crearreceta.html', {'ingredientes': ingredientes})


      
