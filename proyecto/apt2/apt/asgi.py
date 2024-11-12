import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.conf import settings

from django.urls import re_path
from django.contrib.staticfiles.views import serve
# Configura el módulo de settings antes de cualquier otra importación
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apt.settings')
django_asgi_app = get_asgi_application()

# Ahora importa las rutas websocket
from core.routing import websocket_urlpatterns


application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # Si usas Daphne, puedes agregar la configuración para servir archivos estáticos en desarrollo
})

