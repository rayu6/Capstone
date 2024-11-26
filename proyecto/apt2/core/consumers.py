import json
from venv import logger
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.shortcuts import get_object_or_404
from .models import Recetas, RecetaIngrediente, Usuario
from django.apps import apps

class RecetasConsumer(AsyncWebsocketConsumer):
    _temp_modifications = {}  # Diccionario para almacenar modificaciones temporales

    async def connect(self):
        await self.channel_layer.group_add("recetas_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("recetas_group", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')
        
        if action == 'temp_modify':
            # Maneja modificaciones temporales
            receta_id = data.get('receta_id')
            modifications = data.get('modifications')
            
            # Almacena las modificaciones temporales
            self._temp_modifications[receta_id] = modifications
            
            # Transmite las modificaciones a todos los clientes
            await self.channel_layer.group_send(
                "recetas_group",
                {
                    "type": "broadcast_temp_modification",
                    "receta_id": receta_id,
                    "modifications": modifications
                }
            )

    async def broadcast_temp_modification(self, event):
        await self.send(text_data=json.dumps({
            'type': 'temp_modification',
            'receta_id': event['receta_id'],
            'modifications': event['modifications']
        }))

    async def broadcast_db_update(self, event):
        print(f"📨 Processing broadcast_db_update: {event}")
        try:
            message = {
                'type': 'db_update',
                'receta_id': event['receta_id'],
                'data': event['data']
            }
            print(f"📝 Preparing message: {message}")
            await self.send(text_data=json.dumps(message))
            print("✅ Message sent to client successfully")
        except Exception as e:
            print(f"❌ Error in broadcast_db_update: {str(e)}")
            import traceback
            print(traceback.format_exc())

class PedidosConsumer(AsyncWebsocketConsumer):
    _temp_modifications = {}  # Diccionario para almacenar modificaciones temporales

    async def connect(self):
        await self.channel_layer.group_add("pedidos_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("pedidos_group", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')
        
        if action == 'temp_modify':
            # Maneja modificaciones temporales
            pedido_id = data.get('pedido_id')
            modifications = data.get('modifications')
            
            # Almacena las modificaciones temporales
            self._temp_modifications[pedido_id] = modifications
            
            # Transmite las modificaciones a todos los clientes
            await self.channel_layer.group_send(
                "pedidos_group",
                {
                    "type": "broadcast_temp_modification",
                    "pedido_id": pedido_id,
                    "modifications": modifications
                }
            )

    async def broadcast_temp_modification(self, event):
        await self.send(text_data=json.dumps({
            'type': 'temp_modification',
            'pedido_id': event['pedido_id'],
            'modifications': event['modifications']
        }))

    async def broadcast_db_update(self, event):
        print(f"📨 Processing broadcast_db_update: {event}")
        try:
            message = {
                'type': 'db_update',
                'pedido_id': event['pedido_id'],
                'data': event['data']
            }
            print(f"📝 Preparing message: {message}")
            await self.send(text_data=json.dumps(message))
            print("✅ Message sent to client successfully")
        except Exception as e:
            print(f"❌ Error in broadcast_db_update: {str(e)}")
            import traceback
            print(traceback.format_exc())

    async def nuevo_pedido_mensaje(self, event):
        # Manejar el mensaje recibido y enviarlo al cliente
        await self.send(text_data=json.dumps({
            'type': 'nuevo_pedido',
            'pedido': event['pedido']
        }))

# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.shortcuts import get_object_or_404
from django.apps import apps

class PedidosPorUsuarioConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("pedidos_por_usuario_group", self.channel_name)
        self.usuario = await self.get_usuario(1)
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("pedidos_por_usuario_group", self.channel_name)
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        
        if data.get('type') == 'nuevo_pedido_modificado':
            # Crear el pedido en la base de datos
            pedido_creado = await self.crear_pedido(
                data['receta_id'],
                data.get('modifications', None)
            )
            
            if pedido_creado:
                # Notificar a todos los clientes conectados
                await self.channel_layer.group_send(
                    "pedidos_group",  # Enviamos al grupo de pedidos general
                    {
                        "type": "nuevo_pedido_mensaje",  # Cambiamos el nombre del tipo
                        "pedido": await self.serializar_pedido(pedido_creado)
                    }
                )

    async def nuevo_pedido_mensaje(self, event):  # Añadimos este método
        # Enviar el nuevo pedido a todos los clientes
        await self.send(text_data=json.dumps({
            'type': 'nuevo_pedido',
            'pedido': event['pedido']
        }))
    
    @database_sync_to_async
    def get_usuario(self, usuario_id):
        return get_object_or_404(Usuario, id=usuario_id)
        
    @database_sync_to_async
    def crear_pedido(self, receta_id, modifications=None):
        try:
            # Obtenemos los modelos dinámicamente
            Pedido = apps.get_model('core', 'Pedido')
            RecetaPedido = apps.get_model('core', 'RecetaPedido')
            Recetas = apps.get_model('core', 'Recetas')
            Estado = apps.get_model('core', 'Estado')
            TipoDeOrden = apps.get_model('core', 'TipoDeOrden')
            
            # Crear RecetaPedido
            receta = Recetas.objects.get(id=receta_id)
            receta_pedido = RecetaPedido.objects.create(recetas=receta)
            
            # Crear Pedido
            pedido = Pedido.objects.create(
                usuario=self.usuario,
                tipo_de_orden=TipoDeOrden.objects.get(id=1),
                estado=Estado.objects.get(id=1),
                receta_pedido=receta_pedido
            )
            
            return pedido
        except Exception as e:
            print(f"Error al crear pedido: {str(e)}")
            return None
    
    @database_sync_to_async
    def serializar_pedido(self, pedido):
        return {
            'id': pedido.id,
            'usuario': str(pedido.usuario),
            'estado': str(pedido.estado),
            'tipo_de_orden': str(pedido.tipo_de_orden),
            'receta': str(pedido.receta_pedido.recetas.nombre_receta)
        }