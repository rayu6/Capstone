from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/recetas/$', consumers.RecetasConsumer.as_asgi()),
    re_path(r'ws/pedidos/$', consumers.PedidosConsumer.as_asgi()),
]