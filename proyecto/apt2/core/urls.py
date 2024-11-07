from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'),  # Ruta para la vista "home"
    path('stock', views.listar_ingredientes, name='stock'),  # Ruta para la vista "stock"
    path('register', views.register, name='register'),  # Ruta para la vista "register"
    path('pedidos',views.listar_pedidos, name='pedidos'), # Ruta para la vista "pedidos"
    path('prueba', views.prueba, name='prueba'),  # Ruta para la vista "recetas"
    path('logout/',views.logout_view, name='logout'),  # Ruta para la vista "recetas"
    path('listarecetas/', views.listar_recetas, name='listar_recetas'), #Ruta para ver recetas
    path('guardar_ingrediente/', views.guardar_ingrediente, name='guardar_ingrediente'),
    path('login/', views.login, name='login'),  # Asegúrate de que el nombre coincide con el usado en el HTML
    path('home/', views.home, name='home'),     # Ruta de inicio después del login
    path('home/usuario', views.homeUsuario, name='homeUsuario'),     # Ruta de inicio después del login
    path('home/cliente', views.homeCliente, name='homeCliente'),     # Ruta de inicio después del login
    path('crearreceta/', views.ingredientes_receta, name='crear_receta'),
    path('guardar_receta/',views.guardar_receta, name='guardar_receta')
    #path('agregar-pedido/', views.agregar_pedido, name='agregar_pedido'),
    #path('pedido-crear/', views.crear_pedido, name='crear_pedido'),

    

]