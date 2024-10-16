from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'),  # Ruta para la vista "home"
    path('stock', views.stock, name='stock'),  # Ruta para la vista "stock"
    path('register', views.register, name='register'),  # Ruta para la vista "register"
    path('pedidos',views.listar_pedidos, name='pedidos'), # Ruta para la vista "pedidos"
    path('prueba', views.prueba, name='prueba'),  # Ruta para la vista "recetas"
    path('logout/',views.logout_view, name='logout'),  # Ruta para la vista "recetas"
    path('listarecetas', views.listar_recetas, name='listar_recetas'), #Ruta para ver recetas
    #path('agregar-pedido/', views.agregar_pedido, name='agregar_pedido'),
    

    

]