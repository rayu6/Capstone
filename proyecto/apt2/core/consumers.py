import json
from venv import logger
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Recetas, RecetaIngrediente

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
