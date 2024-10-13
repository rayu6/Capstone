from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'),  # Ruta para la vista "home"
    path('stock', views.stock, name='stock'),  # Ruta para la vista "stock"
    path('register', views.register, name='register'),  # Ruta para la vista "register"
    path('recetas', views.recetas, name='recetas'),  # Ruta para la vista "recetas"
    path('pedidos',views.pedidos, name='pedidos'), # Ruta para la vista "pedidos"
    path('prueba', views.prueba, name='prueba'),  # Ruta para la vista "recetas"
    path('logout/',views.logout_view, name='logout'),  # Ruta para la vista "recetas"
    

    

]