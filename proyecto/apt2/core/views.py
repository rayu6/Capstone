import logging
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, redirect,get_object_or_404
from django.db import transaction
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Recetas
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from core.forms import UsuarioLoginForm
from .decorators import role_required
from .models import *
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

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
                messages.error(request, "Usuario o contraseña incorrectos.")
                return HttpResponseRedirect(reverse(login))
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

def pedidos_por_usuario(request):
    recetas = Recetas.objects.prefetch_related('receta_ingrediente__ingrediente').all()
    return render(request, 'core/pedidosPorUsuario.html', {'recetas': recetas})

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
        # Obtener datos del formulario
        nombre_receta = request.POST.get('nombre_receta')
        descripcion = request.POST.get('descripcion_receta')
        link = request.POST.get('link') 

        # Obtener o crear la instancia de NombreReceta
        nombre_receta_obj, created = NombreReceta.objects.get_or_create(nombre=nombre_receta)

        # Crear y guardar link
        receta = Recetas(nombre_receta=nombre_receta_obj, descripcion=descripcion, link=link)
        receta.save()

        # Ingredientes seleccionados
        ingredientes_ids = request.POST.getlist('ingredientes')  # IDs de los ingredientes seleccionados
        with transaction.atomic():
            for ingrediente_id in ingredientes_ids:
                ingrediente = Ingrediente.objects.get(id=ingrediente_id)
                
                # Obtener la cantidad y unidad asociada al ingrediente
                cantidad = request.POST.get(f'cantidad_{ingrediente.id}')
                unidad = request.POST.get(f'unidad_{ingrediente.id}')

                if cantidad and unidad:  # unidad no vacío
                    # Crear y guardar 
                    receta_ingrediente = RecetaIngrediente.objects.create(
                        ingrediente=ingrediente,
                        cantidad=cantidad,
                        unidad=unidad  
                    )
                    receta.receta_ingrediente.add(receta_ingrediente)

        return redirect('listar_recetas')  
    else:
        ingredientes = Ingrediente.objects.all() 
        return render(request, 'core/crearreceta.html', {'ingredientes': ingredientes})


""" def test_signal(request):
    receta = Recetas.objects.first()
    if receta:
        print(f"🔍 Original descripcion: {receta.descripcion}")
        receta.descripcion = "Test update at now"
        receta.save()
        print(f"✏️ Nueva descripcion: {receta.descripcion}")

        # Notificar al grupo WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "recetas_group",  # Grupo al que queremos notificar
            {
                "type": "broadcast_db_update",  # Método en el consumidor
                "receta_id": 2,         # ID de la receta modificada
                "data": {"descripcion": receta.descripcion},  # Nuevos datos
            }
        )
        return JsonResponse({"status": "ok", "message": f"Updated receta {receta.id}"}) """

@csrf_exempt
@require_http_methods(["POST"])
def eliminar_ing_receta(request):
    try:
        id_ingrediente= request.POST.get('id')
        if not id_ingrediente:
            return JsonResponse({
                "status": "error",
                "message": "Se requiere el id"
            }, status=400)
        try:
            recetaingrediente  = get_object_or_404(RecetaIngrediente, id=id_ingrediente)
        except Recetas.DoesNotExist:
            return JsonResponse({
                "status": "error",
                "message": f"No se encontró la receta con id {id_ingrediente}"
            }, status=404)
        try:
            recetaingrediente.delete()
            return JsonResponse({
            "status": "ok",
            "message": f"deleted ingrediente {id_ingrediente}",
            "data": {
                "id": id_ingrediente
                # Itera sobre los ingredientes relacionados
            }
        })
        except:
            return JsonResponse({
            "status": "error",
            "message": f"Error: {str(e)}"
        }, status=500)
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": f"Error: {str(e)}"
        }, status=500)
        

@csrf_exempt
@require_http_methods(["POST"])
def update_receta(request):
    try:
        receta_id = request.POST.get('id')
        nueva_descripcion = request.POST.get('descripcion')
        nuevo_nombre = request.POST.get('nombre_receta')
        nombre_receta=request.POST.get('ingredientes')
        data = json.loads(nombre_receta)
        if not receta_id:
            return JsonResponse({
                "status": "error",
                "message": "Se requiere el id"
            }, status=400)

        try:
            receta = Recetas.objects.get(id=receta_id)
        except Recetas.DoesNotExist:
            return JsonResponse({
                "status": "error",
                "message": f"No se encontró la receta con id {receta_id}"
            }, status=404)

        # Guardar valores anteriores
        descripcion_anterior = receta.descripcion
        nombre_anterior = receta.nombre_receta.nombre
        
        if data:
            for i in data:
                id_I=i['id']
                cantidad_i=i['cantidad']
                unidad_i=i['unidad']
                try:
                    recetaIngrediente=RecetaIngrediente.objects.get(id=id_I)
                    try:
                        recetaIngrediente.cantidad=cantidad_i
                        recetaIngrediente.save()
                    except:
                        print('error al guardar')
                    print(recetaIngrediente.cantidad)
                    print(unidad_i)
                except:
                    print('id inexistente')
                # recetaIngrediente.cantidad=cantidad_i
                # recetaIngrediente.save
        # Actualizar descripción si se proporcionó
        if nueva_descripcion:
            receta.descripcion = nueva_descripcion

        # Actualizar el nombre existente si se proporcionó
        if nuevo_nombre:
            # Actualizamos el nombre en el objeto NombreReceta existente
            nombre_receta_obj = receta.nombre_receta
            nombre_receta_obj.nombre = nuevo_nombre
            nombre_receta_obj.save()

        receta.save()
        

        print(f"🔍 Original nombre: {nombre_anterior}")
        print(f"✏️ Nuevo nombre: {receta.nombre_receta.nombre}")
        print(f"🔍 Original descripcion: {descripcion_anterior}")
        print(f"✏️ Nueva descripcion: {receta.descripcion}")

        # Notificar por WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "recetas_group",
            {
                "type": "broadcast_db_update",
                "receta_id": receta.id,
                "data": {
                    "descripcion": receta.descripcion,
                    "nombre_receta": receta.nombre_receta.nombre,
                    "cantidad":recetaIngrediente.cantidad
                }
            }
        )
        ingrediente = receta.receta_ingrediente.first()  # Obtén un ingrediente de ejemplo
        return JsonResponse({
            "status": "ok",
            "message": f"Updated receta {receta.id}",
            "data": {
                "id": receta.id,
                "nombre_anterior": nombre_anterior,
                "nombre_nuevo": receta.nombre_receta.nombre,
                "descripcion_anterior": descripcion_anterior,
                "descripcion_nueva": receta.descripcion,
                "ingrediente": [
            {   "id":ingrediente['id'],
                "nombre":ingrediente['ingrediente'],
                "cantidad":ingrediente['cantidad'],  # Suponiendo que tienes un campo `cantidad`
                "unidad": ingrediente['unidad']     # Suponiendo que tienes un campo `unidad`
            }
            for ingrediente in data  # Itera sobre los ingredientes relacionados
        ]
            }
        })


    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": f"Error: {str(e)}"
        }, status=500)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from core.models import Pedido, Estado  # Asegúrate de usar los modelos correctos

@csrf_exempt
@require_http_methods(["POST"])
def update_pedido_estado(request):
    try:
        # Datos hardcoded para la prueba
        pedido_id = request.POST.get('id') # ID del pedido
        nuevo_estado_id = request.POST.get('estado')  # Nuevo estado ('Pendiente')

        try:
            # Buscar el pedido
            pedido = Pedido.objects.get(id=pedido_id)
        except Pedido.DoesNotExist:
            return JsonResponse({
                "status": "error",
                "message": f"No se encontró el pedido con id {pedido_id}"
            }, status=404)

        # Guardar valores anteriores
        estado_anterior = pedido.estado.nombre_estado

        try:
            # Buscar el nuevo estado
            nuevo_estado = Estado.objects.get(id=nuevo_estado_id)
        except Estado.DoesNotExist:
            return JsonResponse({
                "status": "error",
                "message": f"No se encontró el estado con id {nuevo_estado_id}"
            }, status=404)

        # Actualizar el estado del pedido
        pedido.estado = nuevo_estado
        pedido.save()

        print(f"🔍 Estado anterior: {estado_anterior}")
        print(f"✏️ Nuevo estado: {pedido.estado.nombre_estado}")

        # Notificar por WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "pedidos_group",  # Asegúrate de que este grupo esté configurado en tu consumidor
            {
                "type": "broadcast_db_update",
                "pedido_id": pedido.id,
                "data": {
                    "estado": pedido.estado.nombre_estado
                }
            }
        )

        return JsonResponse({
            "status": "ok",
            "message": f"Updated pedido {pedido.id}",
            "data": {
                "id": pedido.id,
                "estado_anterior": estado_anterior,
                "estado_nuevo": pedido.estado.nombre_estado
            }
        })

    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": f"Error: {str(e)}"
        }, status=500)
