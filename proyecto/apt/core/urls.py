from django.urls import path
from . import views  

urlpatterns = [
    path('', views.home, name='home'),  # Ruta para la vista "home"
    path('login', views.login, name='login'),  # Ruta para la vista "login"
    path('stock', views.stock, name='stock'),  # Ruta para la vista "stock"
    path('register', views.register, name='register'),  # Ruta para la vista "register"
    path('recetas', views.recetas, name='recetas'),  # Ruta para la vista "recetas"
    path('pedidos',views.pedidos, name='pedidos'), # Ruta para la vista "pedidos"
    
    
]