import json
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
        await self.send(text_data=json.dumps({
            'type': 'db_update',
            'receta_id': event['receta_id'],
            'data': event['data']
        }))